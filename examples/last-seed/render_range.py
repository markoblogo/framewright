"""Dispatch one explicitly requested Last Seed range through admission/executor."""
import argparse,json,os,subprocess,sys
from pathlib import Path
BASE=Path(__file__).resolve().parents[2]/'skills/video-production-router/scripts'
p=argparse.ArgumentParser();p.add_argument('directory',type=Path);p.add_argument('--name',required=True);p.add_argument('--start',type=int,required=True);p.add_argument('--end',type=int,required=True);p.add_argument('--shot',default='output:shot:last-seed:v1');p.add_argument('--execute',action='store_true');a=p.parse_args();root=a.directory.resolve();project=root/'project.json'
if not a.execute:print('Explicit --execute required; nothing started');sys.exit(0)
env={**os.environ,'PATH':str(root/'bin')+os.pathsep+os.environ['PATH']}
def cli(script,*args):
 r=subprocess.run([sys.executable,str(BASE/script),*map(str,args)],capture_output=True,text=True,env=env)
 if r.returncode:raise RuntimeError(script+': '+r.stderr[-1800:])
 try:return json.loads(r.stdout)
 except json.JSONDecodeError:return r.stdout
cli('project.py','asset',project,a.name,'--kind','shot-preview');cli('project.py','task',project,a.name,'--label','Pilot range '+a.name,'--requires',a.name)
selection={'id':a.name,'route_subject':'output:routes','route_id':'local-saved-shot','stage_role':'picture','environment_subject':'output:environment','step':a.name,'tool':'saved-blender-shot','source':a.shot,'output':a.name,'arguments':{'start':a.start,'end':a.end,'context':1,'request':None,'after_start':None,'after_end':None,'observe_resources':False},'limits':{'worker_seconds':180,'max_output_bytes':500*1024**2,'min_available_memory_gib':None,'provider_fee_max':'0','unit':'USD'}}
path=root/(a.name+'-selection.json')
with path.open('x') as f:json.dump(selection,f,indent=2)
cli('admission.py','select',project,path,'--output',root/(a.name+'-contract.json'))
result=cli('executor.py',project,'--step',a.name,'--source',a.shot,'--output',a.name,'--tool','saved-blender-shot','--start',a.start,'--end',a.end,'--execute')
with (root/(a.name+'-result.json')).open('x') as f:json.dump(result,f,indent=2)
print(json.dumps(result,indent=2))
