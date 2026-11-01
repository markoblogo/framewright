#!/usr/bin/env python3
"""Read-only English-copy timing heuristic; never retimes a plan or voice track."""
import argparse,json,math,sys
from pathlib import Path
POLICY={'id':'english-caption-v1','words_per_second':2.5,'characters_per_second':15,'minimum_hold_seconds':2,'transition_allowance_seconds':0.4}
def finite(value,name,positive=False):
 if type(value) not in (int,float) or not math.isfinite(value) or value<0 or (positive and value==0):raise ValueError(name+' must be finite and '+('positive' if positive else 'nonnegative'))
 return value
def inspect(plan,fps=24):
 finite(fps,'fps',True)
 if not isinstance(plan,dict) or not isinstance(plan.get('shots'),list) or not plan['shots']:raise ValueError('Nonempty shots required')
 rows=[]
 for i,s in enumerate(plan['shots']):
  duration=finite(s['duration'],'shot duration',True)
  parts=[s.get('title',''),s.get('subtitle','')]
  if any(not isinstance(v,str) for v in parts):raise ValueError('Caption text must be strings')
  text=' '.join(' '.join(parts).split());words=len(text.split());chars=sum(not c.isspace() for c in text)
  hold=max(POLICY['minimum_hold_seconds'],words/POLICY['words_per_second'],chars/POLICY['characters_per_second']) if text else 0
  required=math.ceil((hold+(POLICY['transition_allowance_seconds'] if text else 0))*fps-1e-9)/fps
  rows.append({'shot':i,'words':words,'nonspace_characters':chars,'available_seconds':duration,'minimum_seconds':required,'status':'pass' if duration+1e-9>=required else 'too_short','narration_timing':'not_assessed'})
 return {'policy':POLICY,'fps':fps,'shots':rows,'status':'pass' if all(x['status']=='pass' for x in rows) else 'needs_copy_or_timing_change','scope':'English reading-time heuristic only; not human acceptance, layout, narration fit or automatic retiming','plan_modified':False}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('plan',type=Path);p.add_argument('--fps',type=float,default=24);a=p.parse_args()
 result=inspect(json.loads(a.plan.read_text()),a.fps);print(json.dumps(result,indent=2));return 0 if result['status']=='pass' else 2
if __name__=='__main__':
 try:sys.exit(main())
 except (ValueError,KeyError,TypeError,OSError) as e:print('Error: '+str(e),file=sys.stderr);sys.exit(1)
