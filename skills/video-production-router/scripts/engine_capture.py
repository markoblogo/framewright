#!/usr/bin/env python3
"""Plan, then explicitly execute a local canvas capture. No installation or hosting."""
import argparse
from array import array
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys


def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()


def validate(c, root):
    from urllib.parse import urlsplit
    allowed={'url','adapter','canvas','width','height','duration_seconds','fps','audio','repeat','seek_seconds','bot','expect_motion','hook','hook_sha256','timeout_seconds','browser_args'}
    if not isinstance(c,dict) or set(c)-allowed:raise ValueError('Unknown capture options; use the documented contract')
    u=urlsplit(c.get('url',''))
    if u.scheme not in {'http','https'} or not u.hostname or u.username or u.password:raise ValueError('HTTP(S) scene URL without credentials required')
    if c.get('adapter') not in {'contract','playmcp'} or c.get('audio') not in {'none','game'}:raise ValueError('Explicit adapter and audio policy required')
    if not isinstance(c.get('canvas'),str) or not c['canvas'].strip():raise ValueError('Canvas selector required')
    c={'width':1280,'height':720,'fps':30,'repeat':1,'seek_seconds':0,'bot':True,'expect_motion':True,'timeout_seconds':45,'browser_args':[],**c}
    for k,lo,hi in [('width',64,3840),('height',64,2160),('fps',1,60),('repeat',1,100)]:
        if type(c[k]) is not int or not lo<=c[k]<=hi:raise ValueError('Invalid '+k)
    for k,lo,hi in [('duration_seconds',1,300),('seek_seconds',0,86400),('timeout_seconds',1,120)]:
        if type(c.get(k)) not in (int,float) or not math.isfinite(c[k]) or not lo<=c[k]<=hi:raise ValueError('Invalid '+k)
    if c['duration_seconds']*c['repeat']>7200:raise ValueError('Final capture limited to two hours')
    for k in ['bot','expect_motion']:
        if type(c[k]) is not bool:raise ValueError('Boolean '+k+' required')
    if c['width']%2 or c['height']%2 or c['duration_seconds']*c['fps']<2:raise ValueError('Even output dimensions and at least two frames required')
    if not isinstance(c['browser_args'],list) or not all(isinstance(x,str) for x in c['browser_args']):raise ValueError('browser_args must be strings')
    if any(x.startswith(('--user-data-dir','--profile-directory','--load-extension','--disable-extensions-except','--remote-debugging')) for x in c['browser_args']):raise ValueError('Capture must use a fresh profile without added extensions or debugging endpoints')
    if c.get('hook'):
        p=(root/c['hook']).resolve(strict=True)
        if not p.is_file() or sha(p)!=c.get('hook_sha256'):raise ValueError('Trusted local hook requires its exact SHA256')
        c['hook']=str(p)
    elif c.get('hook_sha256'):raise ValueError('hook_sha256 requires hook')
    return c


def run(command, **kwargs):
    return subprocess.run(command,check=True,capture_output=True,timeout=kwargs.pop('timeout',180),**kwargs).stdout


def seam_report(source, ffmpeg, fps, audio, expect_motion):
    # Decode small luma samples across the full source, not screenshots of the DOM.
    raw=run([ffmpeg,'-v','error','-i',str(source),'-an','-vf','scale=64:36,format=gray','-f','rawvideo','-'])
    n=64*36;frames=[raw[i:i+n] for i in range(0,len(raw)-n+1,n)]
    if len(frames)<2:raise ValueError('Not enough decoded frames for motion/seam QA')
    diff=lambda a,b:sum(abs(x-y) for x,y in zip(a,b))/n
    adjacent=[diff(a,b) for a,b in zip(frames,frames[1:])]
    boundary=diff(frames[-1],frames[0]);typical=sum(adjacent)/len(adjacent)
    motion=max(adjacent)>.1
    if expect_motion and not motion:raise ValueError('Encoded capture contains no measured motion')
    result={'decoded_fps':fps,'decoded_samples':len(frames),'motion_detected':motion,'seam_luma_mae':boundary,
            'adjacent_luma_mae':typical,'visual_seam':'pass' if boundary<=max(10,typical*2.5) else 'warn',
            'scope':'Numeric luma screen only; no visual or listening acceptance inferred','audio_seam':'not_applicable'}
    if audio=='game':
        pcm=run([ffmpeg,'-v','error','-i',str(source),'-vn','-ac','1','-ar','12000','-f','f32le','-'])
        samples=array('f');samples.frombytes(pcm)
        if sys.byteorder!='little':samples.byteswap()
        if len(samples)<2:raise ValueError('No decoded game audio')
        rms=math.sqrt(sum(x*x for x in samples)/len(samples))
        if rms<1e-5:raise ValueError('Captured game audio is silent')
        jump=abs(samples[-1]-samples[0]);stride=max(1,len(samples)//120000)
        ordered=sorted(abs(samples[i]-samples[i-1]) for i in range(1,len(samples),stride))
        reference=ordered[int(.99*(len(ordered)-1))]
        result.update(audio_rms=rms,audio_boundary_jump=jump,audio_adjacent_p99=reference,
                      audio_seam='pass' if jump<=max(.02,reference*2) else 'warn')
    return result


def execute(c, out, browser, puppeteer, ffmpeg='ffmpeg', ffprobe='ffprobe', node='node'):
    for tool in (ffmpeg,ffprobe,node):
        if not shutil.which(tool):raise ValueError('Required local runtime unavailable: '+tool)
    if not browser.is_file() or not puppeteer.exists():raise ValueError('Supply installed browser and Puppeteer module paths; no installation is performed')
    out.mkdir(parents=True,exist_ok=False)
    report={'schema_version':1,'execution':'failed','config':c,'automatic_model_calls':0,'provider_credits':0}
    try:
        (out/'config.json').write_text(json.dumps(c,allow_nan=False))
        run([node,str(Path(__file__).with_suffix('.cjs')),str(out/'config.json'),str(out),str(browser),str(puppeteer)],timeout=c['duration_seconds']+c['timeout_seconds']*5+60)
        native=json.loads((out/'browser-report.json').read_text())
        report['browser']=native
        if native.get('errors'):raise ValueError('Browser page errors; inspect private report')
        source=out/'source.webm'
        probe=json.loads(run([ffprobe,'-v','error','-show_format','-show_streams','-of','json',str(source)]))
        streams=probe['streams']
        if 'duration' in probe['format']:seconds=float(probe['format']['duration'])
        else:
            packets=json.loads(run([ffprobe,'-v','error','-show_entries','packet=pts_time,duration_time','-of','json',str(source)]))['packets']
            starts=[float(p['pts_time']) for p in packets if 'pts_time' in p]
            ends=[float(p['pts_time'])+float(p.get('duration_time',0)) for p in packets if 'pts_time' in p]
            if not starts:raise ValueError('Capture has no encoded timestamps')
            seconds=max(ends)-min(starts)
        if abs(seconds-c['duration_seconds'])>max(.3,2/c['fps']):raise ValueError('Encoded duration outside capture tolerance')
        video=next((s for s in streams if s['codec_type']=='video'),None)
        if video is None or (video['width'],video['height'])!=(c['width'],c['height']):raise ValueError('Canvas dimensions differ from requested output')
        has_audio=any(s['codec_type']=='audio' for s in streams)
        if has_audio!=(c['audio']=='game'):raise ValueError('Encoded audio tracks differ from policy')
        cycle=out/'cycle.mp4'
        command=[ffmpeg,'-v','error','-i',str(source),'-map','0:v:0','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-r',str(c['fps'])]
        command+=['-map','0:a:0','-c:a','aac','-b:a','192k'] if has_audio else ['-an']
        run(command+['-movflags','+faststart',str(cycle)])
        report['loop']=seam_report(cycle,ffmpeg,c['fps'],c['audio'],c['expect_motion'])
        final=out/'capture.mp4'
        if c['repeat']==1:shutil.copyfile(cycle,final)
        else:
            listing=out/'concat.txt';listing.write_text("file 'cycle.mp4'\n"*c['repeat'])
            run([ffmpeg,'-v','error','-f','concat','-safe','1','-i',str(listing),'-c','copy','-movflags','+faststart',str(final)])
        run([ffmpeg,'-v','error','-xerror','-i',str(final),'-f','null','-'],timeout=max(180,c['duration_seconds']*c['repeat']))
        final_probe=json.loads(run([ffprobe,'-v','error','-show_format','-of','json',str(final)]))
        final_seconds=float(final_probe['format']['duration'])
        if abs(final_seconds-c['duration_seconds']*c['repeat'])>max(.5,c['repeat']*2/c['fps']):raise ValueError('Repeated output duration drifted')
        report.update(execution='recorded',source_sha256=sha(source),cycle_sha256=sha(cycle),output_sha256=sha(final),output_seconds=final_seconds,full_decode='pass',
                      creative_acceptance='not_performed',listening_acceptance='not_performed',publication='not_performed')
    except Exception as exc:
        detail=exc.stderr.decode(errors='replace')[-4000:] if isinstance(exc,subprocess.CalledProcessError) and exc.stderr else str(exc)
        report['error']=detail
        raise
    finally:
        (out/'capture-report.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('config',type=Path);p.add_argument('--execute',action='store_true');p.add_argument('--output',type=Path);p.add_argument('--browser',type=Path);p.add_argument('--puppeteer-module',type=Path);p.add_argument('--ffmpeg',default='ffmpeg');p.add_argument('--ffprobe',default='ffprobe');p.add_argument('--node',default='node');a=p.parse_args()
    try:
        c=validate(json.loads(a.config.read_text()),a.config.resolve().parent)
        if not a.execute:result={'execution':'not_started','config':c,'output_seconds':c['duration_seconds']*c['repeat'],'required_local_tools':['node','puppeteer-core','Chrome/Chromium','ffmpeg','ffprobe'],'note':'No browser, network, media or paid API executed. Trusted hook runs only with --execute.'}
        else:
            if not all([a.output,a.browser,a.puppeteer_module]):raise ValueError('--execute requires --output, --browser and --puppeteer-module')
            result=execute(c,a.output.resolve(),a.browser.resolve(),a.puppeteer_module.resolve(),a.ffmpeg,a.ffprobe,a.node)
        print(json.dumps(result,indent=2,allow_nan=False))
    except (ValueError,OSError,KeyError,subprocess.SubprocessError) as exc:p.exit(1,str(exc)+'\n')
if __name__=='__main__':main()
