"""Explicit revision-bound replacement of a creative review;never marks old work done."""
from collections import Counter
from pathlib import Path
import runpy
PREFIX='review-supersession:'

def candidates(data,state,check_kind):
    steps={s['id']:s for s in data['steps']}
    selected=runpy.run_path(str(Path(__file__).with_name('final_selection.py')))['view'](data,state)
    if not selected or selected['state']!='accepted_recorded':return {}
    current=state['observations']['effective']
    latest={(r['subject'],r['kind'],r['topic']):r for r in data.get('journal',[])}
    result={}
    for r in current:
        if r['kind']!='decision' or r['subject']!='project' or r['result']!='accepted' or not r['topic'].startswith(PREFIX):continue
        if latest.get(('project','decision',r['topic']),{}).get('id')!=r['id']:continue
        old=r['topic'][len(PREFIX):];new=r.get('replacement_task');a=steps.get(old);b=steps.get(new)
        recorded=next((i for i,h in enumerate(data['history']) if h['action']=='supersede_review' and h.get('entry')==r['id']),None)
        if recorded is not None and any(h['action']=='mark' and h.get('step')==old for h in data['history'][recorded+1:]):continue
        if not a or not b or old==new or check_kind(a)!='creative' or check_kind(b)!='creative':continue
        if a['state'] not in {'planned','blocked'} or a['unmet'] or not a['required_outputs'] or not b['required_outputs'] or b['state']!='done' or b['unmet']:continue
        if any(steps[d]['state']!='done' for d in b['depends_on']):continue
        old_kinds=Counter(data['artifacts'][i]['kind'] for i in a['required_outputs'])
        new_kinds=Counter(data['artifacts'][i]['kind'] for i in b['required_outputs'])
        if old_kinds-new_kinds:continue
        subjects={'output:'+i for i in b['required_outputs']}
        if selected['subject'] not in subjects or selected['subject'] in {'output:'+i for i in a['required_outputs']}:continue
        # An exact pin per replacement output; extra/missing pins cannot narrow the scope.
        if set(r['pins'])!=subjects or any(r['pins'][s]!=data['artifacts'][s[7:]]['file'] for s in subjects):continue
        if any(s in state['file_problems'] for s in subjects):continue
        valid=True
        for subject in subjects:
            rows=[v for v in current if v['subject']==subject and v['kind']=='creative']
            stale=[v for v in state['observations']['stale'] if v['subject']==subject and v['kind']=='creative' and latest.get((v['subject'],v['kind'],v['topic']),{}).get('id')==v['id']]
            if not rows or any(v['result']!='accepted' for v in rows) or stale:valid=False
        if valid:result[old]={'task':old,'replacement_task':new,'receipt':r['id'],'note':r['note'],'original_state':a['state'],'original_waiting_for':a.get('waiting_for'),'original_evidence':a['evidence']}
    return result

def historical_pairs(data,history,check_kind):
    old={( 'output:'+i,'creative') for s in data['steps'] if s['id'] in history for i in s['required_outputs']}
    active={( 'output:'+i,check_kind(s)) for s in data['steps'] if s['id'] not in history for i in s['required_outputs']}
    return old-active

def supersede(data,state,old,new,actor,note,P):
    if not actor.strip() or not note.strip():raise ValueError('Explicit actor and supersession reason required')
    steps={s['id']:s for s in data['steps']}
    if old not in steps or new not in steps:raise ValueError('Unknown review task')
    # Validate the proposed relation without mutating any existing task or receipt.
    previous=data['journal'][:]
    row=P['JOURNAL']['append'](data,'project','decision','accepted',actor,'operator_observation',note,PREFIX+old,['output:'+i for i in steps[new]['required_outputs']])
    row['replacement_task']=new
    try:
        proposed={**state,'observations':P['JOURNAL']['project'](data,state['file_problems'])}
        if old not in candidates(data,proposed,P['check_kind']):raise ValueError('Replacement must be a completed current accepted creative review containing the selected final;old review must be distinct and unfinished')
    except Exception:
        data['journal']=previous
        raise
    P['event'](data,'supersede_review',entry=row['id'],step=old,replacement_task=new,note='Historical classification only;old task/receipts unchanged,dependencies not completed')
