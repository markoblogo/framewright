#!/usr/bin/env python3
"""Explicit internal Blender repeatability probe. Generates only original local test assets."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import struct
import subprocess
import sys
import wave

BASE=Path(__file__).resolve().parents[2]/'skills/video-production-router/scripts'
HERE=Path(__file__).resolve().parent
GOAL='Internal deterministic Blender stage validation'


def sha(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--blender',required=True);p.add_argument('--execute',action='store_true');p.add_argument('--resume',action='store_true')
    a=p.parse_args();root=a.output.resolve()
    if not a.execute:
        print(json.dumps({'execution_started':False,'planned':'Original3s scene, repeated full render, matching subrange, one light patch and range render','output':str(root)}));return
    if root.exists():
        if not a.resume:raise ValueError('Choose a new output folder or explicitly --resume this fixture')
        if json.loads((root/'project.json').read_text())['project']['goal']!=GOAL:raise ValueError('Not this probe project')
    else:root.mkdir()
    project=root/'project.json'
    def cli(script,*args):
        proc=subprocess.run([sys.executable,str(BASE/script),*map(str,args)],capture_output=True,text=True)
        if proc.returncode:raise RuntimeError(proc.stderr[-5000:])
        return proc.stdout
    if not (root/'stage.blend').exists():
        with (root/'create-scene.log').open('x') as log:
            subprocess.run([a.blender,'--factory-startup','--disable-autoexec','--background','--python-exit-code','1',
                '--python',str(HERE/'create_scene.py'),'--',str(root)],stdout=log,stderr=subprocess.STDOUT,check=True,timeout=120)
    if not (root/'sound.wav').exists():
        with wave.open(str(root/'sound.wav'),'wb') as f:
            f.setnchannels(2);f.setsampwidth(2);f.setframerate(48000)
            values=[]
            for i in range(144000):
                t=i/48000;fade=max(0,min(1,t/.2,(3-t)/.3))
                v=int(2800*fade*(.5*math.sin(2*math.pi*180*t)+.2*math.sin(2*math.pi*270*t)))
                values.append(struct.pack('<hh',v,v))
            f.writeframes(b''.join(values))
    if not project.exists():cli('project.py','create',project,'--goal',GOAL,'--note','Original abstract fixture; no external publishing or character canon approval')
    for ident,name in [('scene','stage.blend'),('sound','sound.wav')]:cli('project.py','retain',project,ident,root/name,'--input')
    if not (root/'shot-v1.json').exists():cli('shots.py','prepare',project,root/'shot-spec.json','--output',root/'shot-v1.json','--actor','internal-test')
    originals={name:sha(root/name) for name in ['stage.blend','sound.wav','shot-v1.json']}
    reports={}
    for attempt,version,start,end in [('full-a','v1',0,36),('full-b','v1',0,36),('subset','v1',12,24),('light-patch','v2',12,24),('camera-b','v3',12,24)]:
        if version=='v2' and not (root/'shot-v2.json').exists():
            cli('shots.py','patch',project,'output:shot:stage:v1','--parameter','settings.lights.Key.energy','--value','1400',
                '--version','v2','--output',root/'shot-v2.json','--actor','internal-test')
        if version=='v3' and not (root/'shot-v3.json').exists():
            spec=json.loads((root/'shot-spec.json').read_text());spec['version']='v3'
            c=spec['settings']['camera'];c['location'][0]*=-1;c['rotation_euler'][1]*=-1;c['rotation_euler'][2]*=-1
            path=root/'camera-b-spec.json'
            with path.open('x') as stream:json.dump(spec,stream,indent=2)
            cli('shots.py','prepare',project,path,'--output',root/'shot-v3.json','--actor','internal-test')
        folder=root/attempt
        if not folder.exists():
            cli('shots.py','render',project,'output:shot:stage:'+version,'--attempt',attempt,'--start',start,'--end',end,
                '--output',folder,'--execute','--blender',a.blender,'--actor','internal-test')
        # Reports/copies still need verification when resuming; never accept a partial/failed folder.
        report=json.loads((folder/'render-report.json').read_text())
        import runpy
        helper=runpy.run_path(str(BASE/'trials.py'));data=helper['P']['load'](project)
        helper['checked'](data,project,report['subject'],'framewright-shot-render-v1')
        reports[attempt]=report;print('Verified retained attempt:',attempt,flush=True)
    first=reports['full-a'];second=reports['full-b'];sub=reports['subset'];patch=reports['light-patch']
    assert first['source_rgb_md5']==second['source_rgb_md5'],'Repeat rendered pixels differ'
    assert all(first['source_rgb_md5'][i]==v for i,v in sub['source_rgb_md5'].items()),'Subrange pixels differ from same absolute full-shot frames'
    changed=sum(v!=patch['source_rgb_md5'][i] for i,v in sub['source_rgb_md5'].items())
    assert changed==12,'Expected all light-patched frames to change'
    assert len(set(first['source_rgb_md5'].values()))>1,'Action did not move'
    def pcm(folder):
        with wave.open(str(root/folder/'audio.wav'),'rb') as f:return f.readframes(f.getnframes())
    assert pcm('full-a')==pcm('full-b'),'Repeat audio differs'
    assert pcm('full-a')[48000*4:96000*4]==pcm('subset'),'Subrange audio clock differs'
    assert pcm('subset')==pcm('light-patch'),'Light patch changed sound'
    assert pcm('subset')==pcm('camera-b'),'Camera change changed sound'
    assert all(v!=reports['camera-b']['source_rgb_md5'][i] for i,v in sub['source_rgb_md5'].items()),'Alternate camera did not change the view'
    states={k:json.loads((root/k/'state.json').read_text())['states'] for k in reports}
    by_frame={r['frame']:r for r in states['full-a']}
    assert all(by_frame[r['frame']]==r for r in states['subset']),'Restored camera/action/light state differs'
    assert all(r['lights']['Key']['energy']==1400 for r in states['light-patch'])
    assert all({k:v for k,v in r.items() if k!='lights'}=={k:v for k,v in states['light-patch'][i].items() if k!='lights'} for i,r in enumerate(states['subset']))
    assert all(sha(root/name)==value for name,value in originals.items()),'Original retained input modified'
    receipt={'schema':'framewright-blender-probe-v2','date':datetime.now(timezone.utc).date().isoformat(),'blender':first['blender'],
             'scope':'One original36frame480x27012fps Cycles CPU fixture, same machine/build',
             'repeated_source_frames_equal':36,'subrange_source_frames_equal':12,'patched_frames_changed':changed,
             'repeated_pcm_equal':True,'subrange_pcm_sample_aligned':True,'light_patch_preserves_pcm':True,
             'camera_action_state_preserved':True,'original_inputs_unchanged':True,
             'camera_setups_checked':2,'alternate_camera_preserves_pcm':True,
             'elapsed_seconds':{k:v['elapsed_seconds'] for k,v in reports.items()},
             'technical_checks':{k:v['technical_checks'] for k,v in reports.items()},
             'source_hashes':originals,'visual_identity_checked':False,'creative_acceptance':False,
             'listening_acceptance':False,'external_publication':False,'paid_calls':0}
    path=root/'probe-receipt-v2.json'
    if path.exists():raise ValueError('Receipt already exists; preserve it')
    path.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':main()
