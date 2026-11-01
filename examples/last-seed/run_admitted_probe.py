#!/usr/bin/env python3
"""Bounded internal Eevee trial on an existing Last Seed pilot; never changes its checkpoint."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'skills/video-production-router/scripts'

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--source-directory',type=Path,required=True)
 p.add_argument('--audio-source',type=Path,required=True)
 p.add_argument('--output',type=Path,required=True)
 p.add_argument('--blender',type=Path,required=True)
 p.add_argument('--execute',action='store_true');a=p.parse_args()
 root=a.output.resolve();source=a.source_directory.resolve()
 if not a.execute:
  print(json.dumps({'execution_started':False,'scope':'Three3frame Eevee renders plus one interrupted6frame attempt and explicit retry; existing film untouched'}));return
 if root.exists() or root.is_relative_to(ROOT):raise ValueError('New private folder outside checkout required')
 blender=a.blender.resolve(strict=True);root.mkdir(parents=True);(root/'bin').mkdir();(root/'bin/blender').symlink_to(blender)
 env={**os.environ,'PATH':str(root/'bin')+os.pathsep+os.environ['PATH']}
 def write(name,obj):
  path=root/name;path.write_text(json.dumps(obj,indent=2)+'\n');return path
 def cli(script,*args,ok=True):
  r=subprocess.run([sys.executable,str(BASE/script),*map(str,args)],capture_output=True,text=True,env=env,timeout=240)
  if (r.returncode==0)!=ok:raise RuntimeError(script+': '+r.stderr[-1400:])
  if not ok:return {'exit_code':r.returncode,'stderr':r.stderr[-1400:]}
  try:return json.loads(r.stdout)
  except json.JSONDecodeError:return r.stdout
 shutil.copyfile(source/'last-seed.blend',root/'last-seed.blend')
 shutil.copyfile(a.audio_source.resolve(strict=True),root/'sound.wav')
 project=root/'project.json';cli('project.py','create',project,'--goal','R03 bounded admitted Eevee production-scene recovery','--note','Internal trial only; original production and reviews untouched')
 for key,name in [('scene','last-seed.blend'),('sound','sound.wav')]:cli('project.py','retain',project,key,root/name,'--input')
 spec=json.loads((source/'shot-spec.json').read_text());spec.update(id='last-seed-eevee',version='v1')
 spec['engine']={'name':'BLENDER_EEVEE_NEXT','device':'AUTO','samples':8,'seed':0}
 spec['canvas'].update(width=480,height=270)
 cli('shots.py','prepare',project,write('spec.json',spec),'--output',root/'shot.json','--actor','internal-test')
 key=next(iter(spec['settings']['lights']));cli('shots.py','patch',project,'output:shot:last-seed-eevee:v1','--parameter',f'settings.lights.{key}.energy','--value',spec['settings']['lights'][key]['energy']*1.5,'--version','v2','--output',root/'light.json','--actor','internal-test')
 profile=root/'profile.json';cli('intake.py','init',profile);cli('intake.py','preference',profile,'--options','free-only')
 brief=write('brief.json',{'idea':'Restore a saved original Last Seed pilot and verify Eevee interruption/retry','language':'en','duration_seconds':1,'format':'16:9','narration':False,'visual_source':'supplied','source_rights':'owner','deadline':'flexible'})
 routes=write('routes.json',cli('intake.py','routes',profile,brief))
 requirements=write('environment.json',{'id':'eevee-local','platforms':[],'architectures':[],'min_memory_gib':0,'min_free_disk_gib':.25,'programs':[{'name':'blender','minimum_version':'4.5'},{'name':'ffmpeg'},{'name':'ffprobe'}],'models':[],'manual_checks':[],'rights':{'status':'allowed','basis':'Original Last Seed scene/audio; internal owner-authorised test'},'cost':{'status':'free_local','amount':0,'currency':'USD','basis':'Existing local software; excludes labour/hardware'}})
 for key,path,kind in [('routes',routes,'route-comparison'),('environment',requirements,'environment-manifest')]:
  cli('project.py','asset',project,key,'--kind',kind);cli('project.py','retain',project,key,path)
 commands={};results={}
 for name,version,end in [('baseline','v1',71),('repeat','v1',71),('light','v2',71),('recovery','v1',74)]:
  cli('project.py','asset',project,name,'--kind','shot-preview');cli('project.py','task',project,name,'--label',name,'--requires',name)
  selection={'id':name,'route_subject':'output:routes','route_id':'local-saved-shot','stage_role':'picture','environment_subject':'output:environment','step':name,'tool':'saved-blender-shot','source':f'output:shot:last-seed-eevee:{version}','output':name,'arguments':{'start':68,'end':end,'context':1,'request':None,'after_start':None,'after_end':None,'observe_resources':False},'limits':{'worker_seconds':180,'max_output_bytes':32*1024**2,'min_available_memory_gib':None,'provider_fee_max':'0','unit':'USD'}}
  cli('admission.py','select',project,write(name+'-selection.json',selection),'--output',root/(name+'-contract.json'))
  cmd=[sys.executable,str(BASE/'executor.py'),str(project),'--step',name,'--source',selection['source'],'--output',name,'--tool','saved-blender-shot','--start','68','--end',str(end),'--execute'];commands[name]=cmd
  if name=='recovery':break
  r=subprocess.run(cmd,capture_output=True,text=True,env=env,timeout=220)
  write(name+'-process.json',{'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
  if r.returncode:raise RuntimeError(name+': '+r.stderr[-1200:])
  results[name]=json.loads(r.stdout);print(name+' checked',flush=True)
 # Interrupt only this executor, after real Blender starts rendering a frame.
 previous=set(root.glob('executor-shot-*'));cmd=commands['recovery']
 child=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,env=env)
 marker=None
 try:
  deadline=time.monotonic()+100
  while time.monotonic()<deadline:
   for folder in set(root.glob('executor-shot-*'))-previous:
    log=folder/'blender.log'
    if log.exists() and ('Rendering' in log.read_text(errors='replace') or list(folder.glob('frame_*.png'))):marker=folder;break
   if marker or child.poll() is not None:break
   time.sleep(.1)
  if not marker:raise RuntimeError('No native-render evidence before interruption')
  child.send_signal(signal.SIGTERM);stdout,stderr=child.communicate(timeout=15)
 finally:
  if child.poll() is None:child.send_signal(signal.SIGTERM);child.communicate(timeout=15)
 write('interruption.json',{'returncode':child.returncode,'stdout':stdout,'stderr':stderr,'folder':str(marker)})
 assert child.returncode!=0
 def snapshot():return {str(p.relative_to(marker)):[p.stat().st_size,p.stat().st_mtime_ns] for p in marker.rglob('*') if p.is_file()}
 first=snapshot();time.sleep(1);assert first==snapshot(),'Interrupted worker still writing'
 data=json.loads(project.read_text());assert data['artifacts']['recovery']['file'] is None
 blocked=subprocess.run(cmd,capture_output=True,text=True,env=env,timeout=60)
 assert blocked.returncode!=0
 write('implicit-retry-blocked.json',{'returncode':blocked.returncode,'stderr':blocked.stderr})
 state=cli('executor_state.py',project);write('state-after-interruption.json',state)
 attempt=next(x for x in state['attempts'] if x['step']=='recovery');identity=attempt['attempt']
 if attempt['state']=='unresolved':
  evidence=write('reconciliation.json',{'scope':'Operator local inspection','attempt':identity,'outcome':'failed','output_not_retained':True,'folder_stopped_writing':True,'native_render_log':str(marker/'blender.log')})
  cli('project.py','asset',project,'reconciliation','--kind','report');cli('project.py','retain',project,'reconciliation',evidence)
  cli('executor_state.py',project,'--reconcile',identity,'--outcome','failed','--evidence','output:reconciliation')
 elif attempt['state']!='failed':raise ValueError('Unexpected interruption state')
 r=subprocess.run(cmd+['--retry-of',identity],capture_output=True,text=True,env=env,timeout=220)
 write('retry-process.json',{'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
 if r.returncode:raise RuntimeError('Explicit retry failed: '+r.stderr[-1000:])
 results['recovery']=json.loads(r.stdout)
 receipts={k:json.loads(Path(v['receipt']).read_text()) for k,v in results.items()}
 assert receipts['baseline']['source_rgb_md5']==receipts['repeat']['source_rgb_md5']
 assert all(receipts['recovery']['source_rgb_md5'][k]==v for k,v in receipts['baseline']['source_rgb_md5'].items())
 states={k:json.loads(Path(v['receipt']).with_name('state.json').read_text()) for k,v in results.items()}
 assert all(v['engine']=='BLENDER_EEVEE_NEXT' and v['requested_engine']==spec['engine'] for v in states.values())
 assert states['baseline']['states']==states['repeat']['states']
 assert all({k:v for k,v in row.items() if k!='lights'}=={k:v for k,v in states['light']['states'][i].items() if k!='lights'} for i,row in enumerate(states['baseline']['states']))
 assert receipts['baseline']['audio']['pcm_sha256']==receipts['light']['audio']['pcm_sha256']
 assert receipts['baseline']['source_rgb_md5']!=receipts['light']['source_rgb_md5']
 data=json.loads(project.read_text());assert all(t['state']=='planned' for t in data['steps'])
 result={'schema':'framewright-admitted-eevee-probe-v1','scope':'Retained Last Seed pilot;480x27024fps8samples, fixed declared camera; not full film or final-quality qualification','source_sha256':hashlib.sha256((root/'last-seed.blend').read_bytes()).hexdigest(),'engine':spec['engine'],'repeat_rgb_equal':True,'light_changes_rgb':True,'light_preserves_pcm':True,'interrupted_output_unretained':True,'interrupted_folder_stable':True,'implicit_retry_blocked':True,'explicit_retry_produced':True,'interrupted_attempt':identity,'initial_interruption_state':attempt['state'],'outputs_review_pending':True,'original_checkpoint_access':'not_opened_or_written','external_calls':0,'release_created':False,'renders':{k:{'elapsed_seconds':v['elapsed_seconds'],'frames':v['frames'],'technical_checks':v['technical_checks']} for k,v in receipts.items()}}
 write('probe-result.json',result);print(json.dumps(result,indent=2))

if __name__=='__main__':main()
