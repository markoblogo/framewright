#!/usr/bin/env python3
"""Restore a pinned Blender shot, patch one declared control and render an explicit frame range locally."""
import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import runpy
import subprocess
import time
import wave

BASE=Path(__file__).resolve().parent
C=runpy.run_path(str(BASE/'passports.py'));T=C['T'];P=T['P'];J=T['J']
WORKER=BASE/'blender_shot_worker.py'


def sha(path):
    with Path(path).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()


def vector(value,label,color=False):
    C['vec'](value,label)
    if color and any(n<0 or n>1 for n in value):raise ValueError('Color components must be in0..1')


def integer(value,label,lo,hi):
    if type(value) is not int or not lo<=value<=hi:raise ValueError(label+' outside supported integer bounds')


def validate(spec):
    T['keys'](spec,['id','version','scene','resources','canvas','frames','engine','settings','audio','bindings'])
    T['identity'](spec['id']);T['identity'](spec['version']);T['text'](spec['scene'],'scene subject')
    if not isinstance(spec['resources'],list) or any(not isinstance(s,str) for s in spec['resources']) or len(set(spec['resources']))!=len(spec['resources']):raise ValueError('Distinct resource subjects required')
    c=spec['canvas'];T['keys'](c,['width','height','fps'])
    for k in ['width','height']:
        integer(c[k],k,16,3840)
        if c[k]%2:raise ValueError('Even dimensions required')
    if type(c['fps']) is not int or c['fps'] not in {12,24,25,30,50,60}:raise ValueError('Use supported integer fps for exact48kHz audio/frame mapping')
    f=spec['frames'];T['keys'](f,['start','end']);integer(f['start'],'start',0,28799);integer(f['end'],'end',1,28800)
    if f['end']<=f['start']:raise ValueError('Use a positive end-exclusive frame range')
    e=spec['engine'];T['keys'](e,['name','device','samples','seed'])
    if e['name']!='CYCLES' or e['device']!='CPU':raise ValueError('Only pinned Cycles CPU is currently supported')
    integer(e['samples'],'samples',1,256);integer(e['seed'],'seed',0,2147483647)
    s=spec['settings'];T['keys'](s,['camera','actions','lights'])
    c=s['camera'];T['keys'](c,['object','location','rotation_euler','lens']);T['text'](c['object'],'camera')
    vector(c['location'],'camera position');vector(c['rotation_euler'],'camera rotation');T['number'](c['lens'],'lens')
    if not 1<=c['lens']<=500:raise ValueError('Lens outside1..500mm')
    if not isinstance(s['actions'],dict) or not isinstance(s['lights'],dict) or not s['lights']:raise ValueError('Action map and area-light map required')
    for name,action in s['actions'].items():T['identity'](name);T['text'](action,'action name')
    for name,value in s['lights'].items():
        T['identity'](name);T['keys'](value,['energy','color','location','size'])
        T['number'](value['energy'],'light energy');T['number'](value['size'],'light size')
        if value['energy']>100000 or not 0<value['size']<=100:raise ValueError('Light outside bounded range')
        vector(value['color'],'light color',True);vector(value['location'],'light location')
    if spec['audio'] is not None:
        a=spec['audio'];T['keys'](a,['subject','gain_db','offset_seconds']);T['text'](a['subject'],'audio subject')
        if type(a['gain_db']) not in (int,float) or not math.isfinite(a['gain_db']) or not -60<=a['gain_db']<=12:raise ValueError('Audio gain must be -60..12dB')
        T['number'](a['offset_seconds'],'audio offset')
    if not isinstance(spec['bindings'],list):raise ValueError('Passport bindings must be a list')
    seen=set()
    for b in spec['bindings']:
        T['keys'](b,['passport','object']);T['text'](b['passport'],'passport')
        if b['object'] is not None:T['text'](b['object'],'bound object')
        if b['passport'] in seen:raise ValueError('Duplicate passport binding')
        seen.add(b['passport'])
    json.dumps(spec,allow_nan=False)


def blockers(data,project,record):
    result=T['changed'](data,project,record['pins'])
    if record['worker_sha256']!=sha(WORKER):result.append('Trusted worker changed; prepare a new shot version')
    for b in record['spec']['bindings']:
        state=C['state'](data,project,b['passport'])
        if state['state']!='approved':result.append(b['passport']+': '+state['state'])
    return result


def prepare(data,project,spec,output,actor,parent=None,change=None):
    validate(spec);T['text'](actor,'actor');key='shot:'+spec['id']+':'+spec['version']
    if key in data['artifacts']:raise ValueError('Shot version exists; retain a new version')
    refs=[spec['scene'],*spec['resources']]
    if spec['audio']:refs.append(spec['audio']['subject'])
    pins={s:T['current'](data,project,s)[0] for s in refs}
    for b in spec['bindings']:
        _,path=T['current'](data,project,b['passport']);passport=T['read_json'](path)
        if passport.get('schema')!='framewright-passport-v1' or passport.get('project')!=str(project):raise ValueError('Binding requires this project passport')
        C['validate'](passport['spec']);pins[b['passport']]=J['pin'](data,b['passport']);pins.update(passport['pins'])
    if parent:pins[parent]=T['current'](data,project,parent)[0]
    record={'schema':'framewright-shot-v1','project':str(project),'subject':'output:'+key,
            'spec':spec,'pins':pins,'worker_sha256':sha(WORKER),'parent':parent,'change':change,
            'execution_started':False,'visual_identity_checked':False}
    T['write'](output,record);subject=T['register'](data,project,key,output,'shot-card')
    J['append'](data,subject,'decision','proposed',actor,'operator_observation',
                'Pinned shot settings; no render or visual consistency approval','shot-definition',pins)
    P['event'](data,'shot_prepare',subject=subject)
    return record


def patch(data,project,subject,parameter,value,version,output,actor):
    record=T['checked'](data,project,subject,'framewright-shot-v1');spec=record['spec'];validate(spec)
    # Blender names commonly contain dots (.001); keep dictionary keys intact.
    allowed={'settings.camera.'+k:['settings','camera',k] for k in ['location','rotation_euler','lens']}
    for name in spec['settings']['lights']:
        allowed.update({'settings.lights.'+name+'.'+k:['settings','lights',name,k] for k in ['energy','color','location','size']})
    allowed.update({'settings.actions.'+name:['settings','actions',name] for name in spec['settings']['actions']})
    if spec['audio']:allowed.update({'audio.'+k:['audio',k] for k in ['gain_db','offset_seconds']})
    if parameter not in allowed:raise ValueError('Only one declared camera/action/light/audio control can be patched')
    T['identity'](version)
    if version==spec['version']:raise ValueError('Patch needs a new version')
    new=copy.deepcopy(spec);new['version']=version;row=new
    parts=allowed[parameter]
    for key in parts[:-1]:row=row[key]
    old=row[parts[-1]]
    if old==value:raise ValueError('Patch has no change')
    row[parts[-1]]=value
    return prepare(data,project,new,output,actor,subject,{'parameter':parameter,'before':old,'after':value})



def audio_window(offset_seconds,start,end,fps):
    # Round the source offset once; integer frame deltas stay sample-exact.
    return round(offset_seconds*48000)+start*(48000//fps),(end-start)*(48000//fps)


def run(argv,timeout=180):
    return subprocess.run(argv,capture_output=True,text=True,check=True,timeout=timeout).stdout


def render(data,project,subject,start,end,attempt,output,execute,blender,ffmpeg,ffprobe,actor,timeout):
    record=T['checked'](data,project,subject,'framewright-shot-v1');spec=record['spec'];validate(spec)
    start=spec['frames']['start'] if start is None else start;end=spec['frames']['end'] if end is None else end
    if not spec['frames']['start']<=start<end<=spec['frames']['end']:raise ValueError('Render range exceeds saved shot')
    if end-start>240 or (end-start)*spec['canvas']['width']*spec['canvas']['height']>300000000:raise ValueError('Preview exceeds bounded frame/pixel limit')
    T['identity'](attempt);gate=blockers(data,project,record)
    planned={'execution_started':False,'subject':subject,'frames':{'start':start,'end':end},'blockers':gate,
             'output':str(output),'required_tools':['Blender4.5-compatible Cycles CPU','ffmpeg','ffprobe'],
             'audio':'pinned source' if spec['audio'] else 'intentional silence'}
    if not execute:return planned
    if gate:raise ValueError('Shot not ready: '+'; '.join(gate))
    if not blender:raise ValueError('Explicit trusted --blender executable required')
    if timeout<1 or timeout>1800:raise ValueError('Timeout must be1..1800seconds')
    T['text'](actor,'actor');rid=spec['id']+':'+spec['version']+':'+attempt
    if 'shot-render:'+rid in data['artifacts']:raise ValueError('Attempt exists; use a new ID')
    if output.exists() or output.is_symlink() or not output.parent.is_dir():raise ValueError('Use a new render folder with an existing parent')
    _,scene=T['current'](data,project,spec['scene'])
    resources=[str(T['current'](data,project,s)[1].resolve()) for s in spec['resources']]
    if spec['audio']:resources.append(str(T['current'](data,project,spec['audio']['subject'])[1].resolve()))
    version=run([blender,'--version'],15).splitlines()[0]
    output.mkdir();job={'spec':spec,'scene':str(scene.resolve()),'resources':resources,
                        'start':start,'end':end,'output':str(output.resolve())}
    T['write'](output/'job.json',job);clock=time.perf_counter()
    argv=[blender,'--factory-startup','--disable-autoexec','--background',str(scene.resolve()),'--threads','2',
          '--python-exit-code','1','--python',str(WORKER),'--',str((output/'job.json').resolve())]
    try:
        with (output/'blender.log').open('w') as log:
            subprocess.run(argv,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=timeout)
        fps=spec['canvas']['fps'];duration=(end-start)/fps
        pattern=str(output.resolve()/'frame_%06d.png')
        hashes=run([ffmpeg,'-v','error','-framerate',str(fps),'-start_number',str(start+1),'-i',pattern,
                    '-frames:v',str(end-start),'-pix_fmt','rgb24','-f','framemd5','-'])
        frame_hashes=[line.split(',')[-1].strip() for line in hashes.splitlines() if line and not line.startswith('#')]
        if len(frame_hashes)!=end-start:raise ValueError('Rendered frame count mismatch')
        movie=output/'preview.mp4';encode=[ffmpeg,'-v','error','-framerate',str(fps),'-start_number',str(start+1),'-i',pattern]
        if spec['audio']:
            a=spec['audio'];_,source=T['current'](data,project,a['subject']);audio=output/'audio.wav'
            first,length=audio_window(a['offset_seconds'],start,end,fps)
            run([ffmpeg,'-v','error','-protocol_whitelist','file,pipe','-i',str(source.resolve()),'-vn',
                 '-af',f'aresample=48000,atrim=start_sample={first}:end_sample={first+length},asetpts=PTS-STARTPTS,volume={a["gain_db"]}dB,apad=whole_len={length},atrim=end_sample={length}',
                 '-ac','2','-ar','48000','-c:a','pcm_s16le',str(audio)])
            with wave.open(str(audio),'rb') as wav:
                pcm=wav.readframes(wav.getnframes());count=wav.getnframes()
            if count!=(end-start)*(48000//fps):raise ValueError('Audio does not follow exact frame/sample clock')
            audio_info={'pcm_sha256':hashlib.sha256(pcm).hexdigest(),'frames':count,'sample_rate':48000,'start_sample':first,'settings':a}
            encode+=['-i',str(audio),'-c:a','aac','-b:a','128k']
        else:audio_info=None;encode+=['-an']
        run(encode+['-frames:v',str(end-start),'-t',str(duration),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(movie)])
        run([ffmpeg,'-v','error','-protocol_whitelist','file,pipe','-i',str(movie),'-f','null','-'])
        probe=json.loads(run([ffprobe,'-v','error','-count_frames','-show_streams','-show_format','-of','json',str(movie)]))
        video=next(s for s in probe['streams'] if s['codec_type']=='video')
        if int(video['nb_read_frames'])!=end-start or (video['width'],video['height'])!=(spec['canvas']['width'],spec['canvas']['height']):raise ValueError('Encoded video shape/count mismatch')
        if bool([s for s in probe['streams'] if s['codec_type']=='audio'])!=bool(spec['audio']):raise ValueError('Encoded audio policy mismatch')
        problems=T['changed'](data,project,record['pins'])
        if problems:raise ValueError('Source changed during render: '+'; '.join(problems))
        pins={subject:T['current'](data,project,subject)[0],**record['pins']}
        outputs={}
        for label,path,kind in [('video',movie,'video'),('states',output/'state.json','report'),('job',output/'job.json','report')]+([('audio',output/'audio.wav','audio')] if spec['audio'] else []):
            key='shot-'+label+':'+rid;s=T['register'](data,project,key,path,kind);outputs[label]=s;pins[s]=J['pin'](data,s)
        report={'schema':'framewright-shot-render-v1','project':str(project),'id':rid,'shot':subject,
                'subject':'output:shot-render:'+rid,'pins':pins,'worker_sha256':sha(WORKER),'blender':version,
                'frames':{'start':start,'end':end},'source_rgb_md5':{str(start+i):h for i,h in enumerate(frame_hashes)},
                'outputs':outputs,'audio':audio_info,'elapsed_seconds':time.perf_counter()-clock,
                'technical_checks':{'full_decode':'pass','frame_count':'pass','dimensions':'pass','audio_policy':'pass'},
                'creative_review':'pending','listening_review':'pending' if spec['audio'] else 'intentional_silence',
                'visual_identity_checked':False,'publication_authorized':False}
        T['write'](output/'render-report.json',report);result=T['register'](data,project,'shot-render:'+rid,output/'render-report.json','shot-render')
        J['append'](data,result,'decision','proposed',actor,'operator_observation',
                    'Local render and scoped decode/clock checks complete; picture/listening approval pending','shot-render',pins)
        P['event'](data,'shot_render',subject=result)
        return report
    except Exception as exc:
        (output/'FAILED.txt').write_text(type(exc).__name__+': '+str(exc)+'\n')
        raise


def main():
    p=argparse.ArgumentParser(description=__doc__);cmd=p.add_subparsers(dest='command',required=True)
    a=cmd.add_parser('prepare');a.add_argument('project',type=Path);a.add_argument('spec',type=Path);a.add_argument('--output',type=Path,required=True);a.add_argument('--actor',required=True)
    a=cmd.add_parser('patch');a.add_argument('project',type=Path);a.add_argument('subject');a.add_argument('--parameter',required=True);a.add_argument('--value',required=True);a.add_argument('--version',required=True);a.add_argument('--output',type=Path,required=True);a.add_argument('--actor',required=True)
    a=cmd.add_parser('render');a.add_argument('project',type=Path);a.add_argument('subject');a.add_argument('--start',type=int);a.add_argument('--end',type=int);a.add_argument('--attempt',required=True);a.add_argument('--output',type=Path,required=True);a.add_argument('--execute',action='store_true');a.add_argument('--blender');a.add_argument('--ffmpeg',default='ffmpeg');a.add_argument('--ffprobe',default='ffprobe');a.add_argument('--actor',default='operator');a.add_argument('--timeout',type=int,default=300)
    args=p.parse_args()
    try:
        project=args.project.resolve()
        with P['locked'](project):
            data=P['load'](project)
            if data['schema_version']!=2:raise ValueError('Explicit schema-2 migration required')
            if args.command=='prepare':result=prepare(data,project,T['read_json'](args.spec),args.output,args.actor)
            elif args.command=='patch':result=patch(data,project,args.subject,args.parameter,json.loads(args.value),args.version,args.output,args.actor)
            else:result=render(data,project,args.subject,args.start,args.end,args.attempt,args.output,args.execute,args.blender,args.ffmpeg,args.ffprobe,args.actor,args.timeout)
            if args.command!='render' or args.execute:P['save'](project,data)
            print(json.dumps(result if args.command=='render' else {'subject':result['subject'],'execution_started':False},indent=2,allow_nan=False))
    except (OSError,ValueError,KeyError,TypeError,subprocess.SubprocessError) as exc:p.error(str(exc))


if __name__=='__main__':main()
