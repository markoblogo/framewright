#!/usr/bin/env python3
"""R01 internal probe: original scene through selected admission and the sequential executor."""
import argparse
import json
import math
import os
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import wave

ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'skills/video-production-router/scripts'

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--output',type=Path,required=True);p.add_argument('--blender',type=Path,required=True)
 p.add_argument('--execute',action='store_true');a=p.parse_args();root=a.output.resolve()
 if not a.execute:
  print(json.dumps({'execution_started':False,'plan':'Original fixture; four sequential bounded renders, one light edit, no publication','output':str(root)}));return
 if root.exists() or root.is_relative_to(ROOT):raise ValueError('New private output folder outside repository required')
 blender=a.blender.resolve(strict=True);root.mkdir(parents=True);binpath=root/'bin';binpath.mkdir();(binpath/'blender').symlink_to(blender)
 env={**os.environ,'PATH':str(binpath)+os.pathsep+os.environ['PATH']}
 def cli(script,*args):
  r=subprocess.run([sys.executable,str(BASE/script),*map(str,args)],capture_output=True,text=True,env=env,timeout=240)
  if r.returncode:raise RuntimeError(script+': '+r.stderr[-1200:])
  try:return json.loads(r.stdout)
  except json.JSONDecodeError:return r.stdout
 def write(name,value):
  f=root/name;f.write_text(json.dumps(value,indent=2)+'\n');return f
 with (root/'create.log').open('x') as log:
  subprocess.run([str(blender),'--factory-startup','--disable-autoexec','--background','--python-exit-code','1','--python',str(Path(__file__).with_name('create_scene.py')),'--',str(root)],stdout=log,stderr=subprocess.STDOUT,timeout=120,check=True)
 with wave.open(str(root/'sound.wav'),'wb') as f:
  f.setnchannels(2);f.setsampwidth(2);f.setframerate(48000)
  f.writeframes(b''.join(struct.pack('<hh',*[int(1000*math.sin(2*math.pi*180*i/48000))]*2) for i in range(144000)))
 project=root/'project.json';cli('project.py','create',project,'--goal','R01 saved-shot executor probe','--note','Original internal fixture; no release or publication')
 for identity,name in [('scene','stage.blend'),('sound','sound.wav')]:cli('project.py','retain',project,identity,root/name,'--input')
 cli('shots.py','prepare',project,root/'shot-spec.json','--output',root/'shot-v1.json','--actor','internal-test')
 cli('shots.py','patch',project,'output:shot:stage:v1','--parameter','settings.lights.Key.energy','--value','1400','--version','v2','--output',root/'shot-v2.json','--actor','internal-test')
 profile=root/'profile.json';cli('intake.py','init',profile);cli('intake.py','preference',profile,'--options','free-only')
 brief=write('brief.json',{'idea':'Restore an original saved Blender shot and correct only its light','language':'en','duration_seconds':3,'format':'16:9','narration':False,'visual_source':'supplied','source_rights':'owner','deadline':'flexible'})
 route=write('routes.json',cli('intake.py','routes',profile,brief))
 requirements=write('environment.json',{'id':'blender-cpu','platforms':[],'architectures':[],'min_memory_gib':0,'min_free_disk_gib':.1,'programs':[{'name':'blender','minimum_version':'4.5'},{'name':'ffmpeg'},{'name':'ffprobe'}],'models':[],'manual_checks':[],'rights':{'status':'allowed','basis':'Original local fixture authored by repository example'},'cost':{'status':'free_local','amount':0,'currency':'USD','basis':'Installed local software only; no whole-production cost claim'}})
 for identity,path,kind in [('routes',route,'route-comparison'),('environment',requirements,'environment-manifest')]:
  cli('project.py','asset',project,identity,'--kind',kind);cli('project.py','retain',project,identity,path)
 reports={};states={};render_results={}
 for name,version,start,end in [('baseline','v1',12,18),('repeat','v1',12,18),('subset','v1',14,17),('light','v2',14,17)]:
  cli('project.py','asset',project,name,'--kind','shot-preview');cli('project.py','task',project,name,'--label',name,'--requires',name)
  selection={'id':name,'route_subject':'output:routes','route_id':'local-saved-shot','stage_role':'picture','environment_subject':'output:environment','step':name,'tool':'saved-blender-shot','source':'output:shot:stage:'+version,'output':name,'arguments':{'start':start,'end':end,'context':1,'request':None,'after_start':None,'after_end':None,'observe_resources':False},'limits':{'worker_seconds':180,'max_output_bytes':32*1024**2,'min_available_memory_gib':None,'provider_fee_max':'0','unit':'USD'}}
  cli('admission.py','select',project,write(name+'-selection.json',selection),'--output',root/(name+'-contract.json'))
  result=cli('executor.py',project,'--step',name,'--source',selection['source'],'--output',name,'--tool','saved-blender-shot','--start',start,'--end',end,'--execute')
  render_results[name]=result
  receipt=json.loads(Path(result['receipt']).read_text());reports[name]=receipt
  states[name]=json.loads(Path(result['receipt']).with_name('state.json').read_text())['states']
  print('Checked '+name,flush=True)
 a,b,c,d=[reports[n] for n in ('baseline','repeat','subset','light')]
 assert a['source_rgb_md5']==b['source_rgb_md5']
 assert all(a['source_rgb_md5'][k]==v for k,v in c['source_rgb_md5'].items())
 assert all(d['source_rgb_md5'][k]!=v for k,v in c['source_rgb_md5'].items())
 assert a['audio']['pcm_sha256']==b['audio']['pcm_sha256']
 assert c['audio']['pcm_sha256']==d['audio']['pcm_sha256']
 with wave.open(str(Path(render_results['baseline']['file']).with_name('audio.wav')),'rb') as f:pcm=f.readframes(f.getnframes())
 with wave.open(str(Path(render_results['subset']['file']).with_name('audio.wav')),'rb') as f:sub=f.readframes(f.getnframes())
 assert pcm[2*4000*4:5*4000*4]==sub
 assert states['baseline']==states['repeat']
 assert states['baseline'][2:5]==states['subset']
 assert all({k:v for k,v in row.items() if k!='lights'}=={k:v for k,v in states['light'][i].items() if k!='lights'} for i,row in enumerate(states['subset']))
 assert all(r['lights']['Key']['energy']==1400 for r in states['light'])
 data=json.loads(project.read_text())
 assert all(next(t for t in data['steps'] if t['id']==n)['state']=='planned' for n in reports)
 result={'schema':'framewright-executor-shot-probe-v1','blender':a['blender'],'scope':'Original480x27012fps Cycles CPU scene;18frames across4sequential runs',
  'repeat_frames_equal':6,'subset_frames_equal':3,'light_changed_frames':3,'repeat_pcm_equal':True,'subset_pcm_sample_aligned':True,'light_preserves_pcm':True,'light_preserves_camera_action':True,
  'outputs_review_pending':True,'paid_calls':0,'publication_authorized':False,'release_created':False,
  'elapsed_render_seconds':{k:v['elapsed_seconds'] for k,v in reports.items()},'technical_checks':{k:v['technical_checks'] for k,v in reports.items()}}
 write('executor-probe.json',result);print(json.dumps(result,indent=2))

if __name__=='__main__':main()
