#!/usr/bin/env python3
"""Bind one selected route action to current local execution prerequisites. Never dispatch."""
import argparse
from datetime import datetime,timezone
import hashlib
from fractions import Fraction
import json
import math
from pathlib import Path
import re
import runpy
import shutil
import tempfile
import subprocess

BASE=Path(__file__).resolve().parent
ENV=runpy.run_path(str(BASE/'environment.py'))
RES=runpy.run_path(str(BASE/'resources.py'))
COST=runpy.run_path(str(BASE/'costs.py'))
TOOLS={'local-media-review':'review-report','review-clip':'review-preview'}

def expected_output(spec):
 return {'identity':spec['output'],'kind':TOOLS[spec['tool']],
         'format':'json' if spec['tool']=='local-media-review' else 'mp4',
         'max_bytes':spec['limits']['max_output_bytes']}
ARGUMENTS={'start','end','context','request','after_start','after_end','observe_resources'}

def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=True).encode()).hexdigest()

def implementation():
 paths=[BASE/n for n in ['admission.py','executor.py','executor_clip_worker.py','environment.py','resources.py','costs.py','editing.py','media_review.py']]
 paths.append(BASE.parent/'references/intake-cost-facets.json')
 return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}

def validate_stored(data):
 if 'execution_routes' not in data:return
 bindings=data['execution_routes']
 if not isinstance(bindings,dict) or data.get('execution_routes_sha256')!=digest(bindings):raise ValueError('Execution selection integrity mismatch')
 steps={s['id'] for s in data['steps']}
 for task,row in bindings.items():
  if task not in steps or not isinstance(row,dict) or set(row)!={'subject','pin'} or not isinstance(row['subject'],str) or not row['subject'].startswith('output:') or not isinstance(row['pin'],dict):raise ValueError('Invalid task selection binding')
  if row['subject'][7:] not in data['artifacts']:raise ValueError('Selection artifact missing')

def read_subject(data,root,subject,P):
 pin=P['JOURNAL']['pin'](data,subject)
 if pin is None:raise ValueError('Retain the selection source first')
 path=(root/pin['path']).resolve(strict=True)
 if path.stat().st_size>8*1024*1024 or P['file_record'](path,root)!=pin:raise ValueError('Pinned selection source changed/too large')
 return json.loads(path.read_text()),pin

def validate_spec(spec):
 fields={'id','route_subject','route_id','stage_role','environment_subject','step','tool','source','output','arguments','limits'}
 if not isinstance(spec,dict) or set(spec)!=fields:raise ValueError('Use explicit selection fields')
 if not isinstance(spec['id'],str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,63}',spec['id']):raise ValueError('Use a short new selection ID')
 for key in fields-{'arguments','limits','id'}:
  if not isinstance(spec[key],str) or not spec[key].strip():raise ValueError('Selection needs '+key)
 if spec['tool'] not in TOOLS:raise ValueError('Selected-route execution currently supports local inspection/review-clip only')
 args=spec['arguments']
 if not isinstance(args,dict) or set(args)!=ARGUMENTS or type(args['observe_resources'])!=bool:raise ValueError('Bind all supported local arguments explicitly')
 if any(args[k] is not None for k in ['request','after_start','after_end']):raise ValueError('Revision-comparison selection is not implemented')
 if type(args['context']) not in (int,float) or not math.isfinite(args['context']) or not .1<=args['context']<=5:raise ValueError('Context must be0.1–5seconds')
 if spec['tool']=='review-clip':
  a,b=args['start'],args['end']
  if any(type(n) not in (int,float) or not math.isfinite(n) for n in [a,b]) or a<0 or b<=a or b-a+2*args['context']>30:raise ValueError('Bind a valid bounded review interval')
 elif args['start'] is not None or args['end'] is not None:raise ValueError('Inspection does not take an interval')
 limits=spec['limits']
 if not isinstance(limits,dict) or set(limits)!={'worker_seconds','max_output_bytes','min_available_memory_gib','provider_fee_max','unit'}:raise ValueError('Explicit execution limits required')
 if type(limits['worker_seconds']) not in (int,float) or not math.isfinite(limits['worker_seconds']) or not 1<=limits['worker_seconds']<=180:raise ValueError('Worker timeout must be1–180seconds')
 if type(limits['max_output_bytes'])!=int or not 1<=limits['max_output_bytes']<=1024**3:raise ValueError('Bound output bytes1–1GiB')
 ram=limits['min_available_memory_gib']
 if ram is not None and (type(ram) not in (int,float) or not math.isfinite(ram) or ram<0):raise ValueError('Use declared available-memory requirement or null')
 if COST['amount'](limits['provider_fee_max']) is None or not isinstance(limits['unit'],str) or not limits['unit'].strip():raise ValueError('Known fee limit and unit required')
 return spec

def select(data,project,spec,output,P):
 validate_stored(data);validate_spec(spec)
 if data.get('schema_version')!=2:raise ValueError('Migrate project first')
 if P['file_problems'](data,project.parent):raise ValueError('Resolve retained file drift before selection')
 task=next((s for s in data['steps'] if s['id']==spec['step']),None)
 if task is None or task['state']!='planned' or task.get('waiting_for') or task['unmet']:raise ValueError('Select an existing planned task without a recorded wait/constraint')
 if spec['output'] not in task['required_outputs'] or data['artifacts'][spec['output']]['kind']!=TOOLS[spec['tool']] or data['artifacts'][spec['output']]['file'] is not None:raise ValueError('Output must be declared,unretained and compatible with this action')
 comparison,route_pin=read_subject(data,project.parent,spec['route_subject'],P)
 if comparison.get('schema')!='framewright-intake-route-comparison-v1':raise ValueError('Retain an actual intake route comparison')
 routes=[r for r in comparison['routes'] if r['id']==spec['route_id']]
 if len(routes)!=1:raise ValueError('Choose one route actually present in the comparison')
 stages=[s for s in routes[0]['stages'] if s['role']==spec['stage_role']]
 if len(stages)!=1 or stages[0]['tool']!='ffmpeg' or not stages[0].get('candidate') or stages[0]['candidate'].get('id')!='ffmpeg' or stages[0]['candidate'].get('cost_kind')!='free_local':raise ValueError('No selected-stage local FFmpeg adapter; no silent tool/provider substitution')
 if comparison.get('selection_policy') not in {'free-only','both'}:raise ValueError('Retain the selection policy')
 env,env_pin=read_subject(data,project.parent,spec['environment_subject'],P);ENV['validate'](env)
 if not {'ffmpeg','ffprobe'}<={p['name'] for p in env['programs']}:raise ValueError('Declare ffmpeg and ffprobe prerequisites')
 source_pin=P['JOURNAL']['pin'](data,spec['source'])
 identity='admission:'+spec['id']
 if identity in data['artifacts'] or spec['step'] in data.get('execution_routes',{}):raise ValueError('Task already selected; use a new reviewed task/selection ID')
 contract={'schema':'framewright-execution-selection-v1','selection':spec,'pins':{spec['route_subject']:route_pin,spec['environment_subject']:env_pin,spec['source']:source_pin},'implementation':implementation(),'expected_output':expected_output(spec),'scope':'One local action associated with the selected stage; not execution/qualification of the whole recipe','publication_authorized':False}
 if output.exists():raise ValueError('Use a new selection output file')
 # A pinned output may not alias another already-retained artifact/input.
 protected=[(project.parent/p['path']).resolve() for p in [*data['inputs'].values(),*[a['file'] for a in data['artifacts'].values() if a['file']]]]
 if output.resolve()==project.resolve() or output.resolve() in protected:raise ValueError('Do not overwrite project evidence')
 with output.open('x') as f:json.dump(contract,f,indent=2,allow_nan=False);f.write('\n')
 data['artifacts'][identity]={'kind':'execution-selection','scene':None,'file':None}
 P['event'](data,'declare_artifact',identity=identity,kind='execution-selection')
 P['retain'](data,project.parent,identity,output,False,False)
 subject='output:'+identity
 data.setdefault('execution_routes',{})[spec['step']]={'subject':subject,'pin':P['JOURNAL']['pin'](data,subject)}
 data['execution_routes_sha256']=digest(data['execution_routes'])
 P['event'](data,'select_execution_route',step=spec['step'],route=spec['route_id'],stage=spec['stage_role'],subject=subject,pins=contract['pins'],note='Explicit local operator selection;execute flag still required;no full-route or publication grant')
 return {'selection_subject':subject,'state':'selected_not_executed'}

def check(data,project,step,P,invocation=None):
 validate_stored(data)
 binding=data.get('execution_routes',{}).get(step)
 if binding is None:return None
 blockers=[];evidence={};root=project.parent
 if P['JOURNAL']['pin'](data,binding['subject'])!=binding['pin']:raise ValueError('Selected contract revision changed; select a new reviewed task')
 contract,_=read_subject(data,root,binding['subject'],P)
 if contract.get('schema')!='framewright-execution-selection-v1':raise ValueError('Invalid execution contract schema')
 spec=validate_spec(contract['selection'])
 if contract.get('expected_output')!=expected_output(spec):raise ValueError('Expected output contract is inconsistent')
 if spec['step']!=step:raise ValueError('Selection belongs to another task')
 task=next((t for t in data['steps'] if t['id']==step),None)
 artifact=data['artifacts'].get(spec['output'],{})
 if task is None or spec['output'] not in task['required_outputs'] or artifact.get('kind')!=TOOLS[spec['tool']]:blockers.append('Declared task/output contract changed')
 if artifact.get('file') is not None:blockers.append('Expected output already retained; review it rather than redispatch')
 for subject,pin in contract['pins'].items():
  if P['JOURNAL']['pin'](data,subject)!=pin or P['file_record']((root/pin['path']),root)!=pin:blockers.append('Revision changed: '+subject)
 if implementation()!=contract['implementation']:blockers.append('Selected adapter/cost-classification implementation changed')
 if invocation:
  wanted={k:spec[k] for k in ['step','tool','source','output']};wanted.update(spec['arguments'])
  if any(getattr(invocation,k)!=v for k,v in wanted.items()):blockers.append('Invocation differs from selected arguments/tool/source/output')
 state=P['summary'](data,root)
 if step not in state['ready']:blockers.append('Task dependencies,waits,evidence or unresolved attempt block execution')
 # Do not inspect different/new requirements or source after an earlier pin mismatch.
 if not blockers:
  env,_=read_subject(data,root,spec['environment_subject'],P)
  snapshot=ENV['inspect'](env,root,probe_versions=True,observe_resources=True)
  evidence['environment']=snapshot
  if snapshot['technical_status']!='ready':blockers.append('Declared runtime prerequisites are not confirmed')
  if snapshot['rights']['status']!='allowed':blockers.append('Source-use rights remain unresolved/restricted')
  fee=snapshot['cost'];facets=json.loads((BASE.parent/'references/intake-cost-facets.json').read_text())
  known_zero=facets['tools']['ffmpeg']['kind']=='free_local' and fee['status']=='free_local' and fee['amount']==0 and fee['currency']==spec['limits']['unit']
  if not known_zero:blockers.append('Only confirmed local software fee zero in the same unit is admitted;no paid dispatcher')
  evidence['cost']={'local_provider_fee':'0' if known_zero else None,'unit':spec['limits']['unit'],'limit':spec['limits']['provider_fee_max'],'project':COST['report'](data),'scope':'Local software fee only; no paid reservation/dispatch,labour or whole-route total inferred'}
  wanted=spec['limits']['min_available_memory_gib'];available=snapshot['system']['resource_observation']['memory']['available_bytes']
  if wanted is not None and wanted>0 and (available is None or available/2**30<wanted):blockers.append('Declared available RAM requirement is unmet or unknown')
  if snapshot['system']['free_disk_gib']*2**30<spec['limits']['max_output_bytes']:blockers.append('Free disk is below declared output allowance')
  scratch=Path(tempfile.gettempdir())
  try:
   scratch_free=shutil.disk_usage(scratch).free
   evidence['scratch']={'path':str(scratch),'free_bytes':scratch_free,'status':'observed'}
   floor=max(spec['limits']['max_output_bytes'],snapshot['requirements']['min_free_disk_gib']*2**30)
   if scratch_free<floor:blockers.append('Scratch volume is below declared disk/output floor')
  except OSError:
   evidence['scratch']={'path':str(scratch),'free_bytes':None,'status':'unavailable'}
   blockers.append('Scratch volume free space unavailable')
  if not blockers:
   source=(root/contract['pins'][spec['source']]['path']).resolve(strict=True)
   try:
    raw=subprocess.run(['ffprobe','-v','error','-protocol_whitelist','file,pipe','-show_format','-show_streams','-of','json',str(source)],capture_output=True,text=True,timeout=10,check=True)
    media=json.loads(raw.stdout);streams=media.get('streams',[]);duration=float(media.get('format',{}).get('duration','nan'))
    if not math.isfinite(duration) or duration<=0 or not any(s.get('codec_type') in {'audio','video'} for s in streams):raise ValueError('No usable timed media')
    if spec['tool']=='local-media-review' and (duration>P['MEDIA']['MAX_SECONDS'] or contract['pins'][spec['source']]['bytes']>P['MEDIA']['MAX_BYTES']):raise ValueError('Inspection exceeds source limits')
    if spec['tool']=='review-clip' and (not any(s.get('codec_type')=='video' for s in streams) or spec['arguments']['end']>duration):raise ValueError('Review interval/video does not match source')
    evidence['source']={'duration_seconds':duration,'stream_types':[s.get('codec_type') for s in streams]}
   except (OSError,ValueError,subprocess.SubprocessError):blockers.append('Actual media/interval preflight failed')
 if any(s in P['file_problems'](data,root) for s in [binding['subject'],*contract['pins']]):blockers.append('Pinned evidence changed during preflight')
 return {'schema':'framewright-execution-admission-v1','checked_at':datetime.now(timezone.utc).isoformat(),'step':step,'selection_subject':binding['subject'],'selection_pin':binding['pin'],'pins':contract['pins'],'limits':spec['limits'],'expected_output':contract['expected_output'],'result':'blocked' if blockers else 'admitted_local_action','blockers':blockers,'evidence':evidence,'execution_started':False,'scope':'Fresh admission for one allowlisted local action;not full-route quality,host workload qualification or publication authority'}


def validate_output(gate,path,report):
 expected=gate['expected_output']
 if not path.is_file() or not 0<path.stat().st_size<=expected['max_bytes']:raise ValueError('Produced file violates selected size/type contract')
 if expected['format']=='json':
  raw=json.loads(path.read_text())
  if raw!=report or raw.get('type')!='media-review':raise ValueError('Produced JSON is not the expected inspection report')
 else:
  result=subprocess.run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(path)],capture_output=True,text=True,timeout=10,check=True)
  raw=json.loads(result.stdout);video=next((s for s in raw['streams'] if s.get('codec_type')=='video'),None)
  if not video or video.get('codec_name')!='h264' or (video.get('width'),video.get('height'))!=(640,360) or Fraction(video.get('avg_frame_rate','0/1'))!=24:raise ValueError('Review proxy differs from fixed local adapter format')
  duration=float(raw['format']['duration'])
  if 'mp4' not in raw['format'].get('format_name','') or not math.isfinite(duration) or abs(duration-report['duration'])>2/24+.01:raise ValueError('Review proxy container/duration differs from declared interval')


def main():
 p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
 s=sub.add_parser('select');s.add_argument('project',type=Path);s.add_argument('spec',type=Path);s.add_argument('--output',type=Path,required=True)
 c=sub.add_parser('check');c.add_argument('project',type=Path);c.add_argument('--step',required=True)
 a=p.parse_args();P=runpy.run_path(str(BASE/'project.py'))
 try:
  project=a.project.resolve(strict=True)
  with P['locked'](project):
   data=P['load'](project)
   if a.command=='select':result=select(data,project,json.loads(a.spec.read_text()),a.output,P);P['save'](project,data)
   else:
    result=check(data,project,a.step,P)
    if result is None:raise ValueError('Task has no selected route')
   print(json.dumps(result,indent=2,allow_nan=False))
 except (OSError,ValueError,KeyError,TypeError,subprocess.SubprocessError) as e:p.error(str(e))

if __name__=='__main__':main()
