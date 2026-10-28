#!/usr/bin/env python3
"""Durable local executor intents and explicit reconciliation in the existing journal."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import runpy
import uuid


def host_lock_path():
 # Fixed POSIX location: TMPDIR selects scratch space, never executor identity.
 return Path('/tmp') / ('framewright-executor-' + str(os.getuid()) + '.lock')

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=True).encode()).hexdigest()

def attempts(data):
 rows={}
 for e in data['history']:
  if e['action']=='executor_intent':
   if e['attempt'] in rows:raise ValueError('Duplicate executor intent')
   rows[e['attempt']]={**e,'state':'unresolved'}
  elif e['action'] in {'executor_terminal','executor_reconciled'}:
   r=rows.get(e['attempt'])
   if r is None or r['state']!='unresolved':raise ValueError('Unexpected executor resolution')
   r.update(state=e['state'],resolution=e)
 return list(rows.values())


def begin(data,step,payload,pins,P,retry_of=None):
 rows=[r for r in attempts(data) if r['step']==step]
 if any(r['state']=='unresolved' for r in rows):raise ValueError('Unresolved prior attempt; reconcile its actual outcome before dispatch')
 request_digest=digest({'payload':payload,'pins':pins})
 if rows:
  prior=rows[-1]
  if retry_of!=prior['attempt'] or prior['state'] not in {'failed','not-submitted'}:
   raise ValueError('Prior attempt exists; select a reconciled failed/not-submitted attempt explicitly with --retry-of')
  if prior['request_sha256']!=request_digest:raise ValueError('Retry request changed; create a new reviewed task instead')
 elif retry_of:raise ValueError('No prior attempt for this task')
 for subject,pin in pins.items():
  if P['JOURNAL']['pin'](data,subject)!=pin:raise ValueError('Changed request revision')
 identity=uuid.uuid4().hex
 P['event'](data,'executor_intent',attempt=identity,step=step,request_sha256=request_digest,payload=payload,pins=pins,retry_of=retry_of)
 return identity


def finish(data,identity,state,P,**details):
 if state not in {'produced','failed'}:raise ValueError('Invalid local terminal state')
 row=next((r for r in attempts(data) if r['attempt']==identity),None)
 if row is None or row['state']!='unresolved':raise ValueError('No unresolved executor intent')
 P['event'](data,'executor_terminal',attempt=identity,state=state,**details)


def reconcile(data,root,identity,outcome,evidence,P):
 if outcome not in {'failed','not-submitted','produced'}:raise ValueError('Invalid reconciliation outcome')
 row=next((r for r in attempts(data) if r['attempt']==identity),None)
 if row is None or row['state']!='unresolved':raise ValueError('Only unresolved attempts can be reconciled')
 if not evidence.startswith('output:') or evidence in P['file_problems'](data,root):raise ValueError('Retain current recovery evidence first')
 pin=P['JOURNAL']['pin'](data,evidence)
 if outcome=='produced':
  output=row['payload']['output']
  if not data['artifacts'].get(output,{}).get('file'):raise ValueError('Retain the found output separately before reconciling production')
 P['event'](data,'executor_reconciled',attempt=identity,state=outcome,evidence=evidence,pin=pin,
            output_pin=data['artifacts'].get(row['payload']['output'],{}).get('file') if outcome=='produced' else None,
            attestation='Explicit operator-supplied recovery evidence;not independent provider verification or creative acceptance')


def report(data,root,P):
 problems=P['file_problems'](data,root);effective=P['JOURNAL']['project'](data,problems)['effective']
 result=[]
 for row in attempts(data):
  output='output:'+row['payload']['output'];reviews={}
  for kind in ['technical','listening','creative']:
   values=[r['result'] for r in effective if r['subject']==output and r['kind']==kind]
   reviews[kind]=next((v for v in ['fail','rejected','pending','pass','accepted'] if v in values),None)
  stale=[]
  bound=dict(row['pins'])
  if row.get('resolution',{}).get('output_pin'):bound[output]=row['resolution']['output_pin']
  for s,pin in bound.items():
   try:
    if s in problems or P['JOURNAL']['pin'](data,s)!=pin:stale.append(s)
   except ValueError:stale.append(s)
  result.append({'attempt':row['attempt'],'step':row['step'],'state':row['state'],'request_sha256':row['request_sha256'],'stale_inputs':stale,'reviews':reviews,
   'proposed_next':'reconcile_actual_outcome' if row['state']=='unresolved' else 'review_changed_inputs' if stale else 'inspect_existing_output_and_reviews' if row['state']=='produced' else 'explicit_retry_or_replan'})
 return {'schema':'framewright-executor-state-v1','attempts':result,'execution_authorized':False,'scope':'Read-only proposed next steps; produced is not accepted. No automatic retry,provider query,spend or publication.'}


def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('project',type=Path);p.add_argument('--reconcile');p.add_argument('--outcome',choices=['failed','not-submitted','produced']);p.add_argument('--evidence')
 a=p.parse_args();P=runpy.run_path(str(Path(__file__).with_name('project.py')))
 try:
  path=a.project.resolve(strict=True)
  with P['locked'](path):
   d=P['load'](path)
   if a.reconcile:
    if not a.outcome or not a.evidence:raise ValueError('Reconciliation needs outcome and retained evidence')
    reconcile(d,path.parent,a.reconcile,a.outcome,a.evidence,P);P['save'](path,d)
   elif a.outcome or a.evidence:raise ValueError('Use --reconcile with an attempt ID')
   print(json.dumps(report(d,path.parent,P),indent=2,allow_nan=False))
 except (OSError,ValueError,KeyError,TypeError) as e:p.error(str(e))

if __name__=='__main__':main()
