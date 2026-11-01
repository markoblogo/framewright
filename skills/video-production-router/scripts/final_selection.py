"""Explicit revision-bound final choice; other project work remains unchanged."""
TOPIC='final-selection'
REQUIRED={'technical':'pass','listening':'accepted','creative':'accepted'}

def assessment(data,state,subject,pins):
 reasons=[]
 if not subject.startswith('output:') or data['artifacts'].get(subject[7:],{}).get('kind')!='video':
  reasons.append('Select a retained video output')
 if subject in state['file_problems']:reasons.append('Selected file changed or unavailable')
 current=state['observations']['effective'];stale=state['observations']['stale']
 latest={(r['subject'],r['kind'],r['topic']):r for r in data.get('journal',[])}
 for r in stale:
  if latest.get((r['subject'],r['kind'],r['topic']),{}).get('id')==r['id'] and r['subject']==subject and r['kind'] in REQUIRED:
   reasons.append('Stale '+r['kind']+' review')
 reviews={}
 for kind,result in REQUIRED.items():
  rows=[r for r in current if r['subject']==subject and r['kind']==kind]
  reviews[kind]=[{k:r[k] for k in ('id','result','actor','provenance','note','recorded_at')} for r in rows]
  if not rows or any(r['result']!=result for r in rows):reasons.append('Current '+kind+' approval required')
 if pins is None:reasons.append('Selection revision is stale')
 return reasons,reviews

def view(data,state):
 rows=[r for r in data.get('journal',[]) if r['kind']=='decision' and r['topic']==TOPIC]
 if not rows:return None
 choice=rows[-1];subject=choice['subject']
 effective={r['id'] for r in state['observations']['effective']}
 pins=choice['pins'] if choice['id'] in effective and choice['result']=='accepted' else None
 reasons,reviews=assessment(data,state,subject,pins)
 return {'subject':subject,'selection_receipt':choice['id'],'sha256':choice['pins'].get(subject,{}).get('sha256'),
         'retained_file':dict(choice['pins'][subject]) if subject in choice['pins'] else None,
         'other_observations':[{k:r[k] for k in ('id','kind','topic','result','actor','provenance','note','recorded_at','url','visibility') if k in r} for r in state['observations']['effective'] if r['subject']==subject and r['kind'] in {'provider','publication'}],
         'state':'needs_review' if reasons else 'accepted_recorded','reasons':reasons,'reviews':reviews,
         'note':'Exact-version recorded choice; no independent QA, task cancellation, execution or publication authority.'}

def select(data,state,subject,actor,note,P):
 pin=P['JOURNAL']['pin'](data,subject)
 reasons,_=assessment(data,state,subject,pin)
 if reasons:raise ValueError('; '.join(reasons))
 row=P['JOURNAL']['append'](data,subject,'decision','accepted',actor,'operator_observation',note,TOPIC)
 P['event'](data,'select_final',entry=row['id'],subject=subject,note='Explicit operator selection; other tasks and approvals unchanged')
