#!/usr/bin/env python3
"""Append-only project cost evidence. No provider calls, purchases or currency conversion."""
import argparse
from datetime import datetime,timezone
from decimal import Decimal, InvalidOperation, localcontext
import hashlib
import json
from pathlib import Path
import re
import runpy

KINDS={'limit','estimate','reserve','usage','settle','adjust','unknown','release'}

def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=True).encode()).hexdigest()

def amount(value,negative=False):
 if value is None:return None
 if not isinstance(value,str) or len(value)>64 or not re.fullmatch(r'-?\d+(?:\.\d{1,12})?',value):raise ValueError('Use an exact decimal string or null')
 try:n=Decimal(value)
 except InvalidOperation:raise ValueError('Invalid decimal')
 if not n.is_finite() or (n<0 and not negative):raise ValueError('Nonnegative finite amount required')
 return n

def validate_event(e):
 required={'id','kind','amount','unit','operation','supplier','category','basis','provenance'}
 optional={'receipt','tags','task','subject','pin','observed_at','recorded_at'}
 if not isinstance(e,dict) or not required<=set(e) or set(e)-required-optional:raise ValueError('Invalid cost event fields')
 if e['kind'] not in KINDS:raise ValueError('Unknown cost event kind')
 for key in ['id','unit','supplier','category','basis']:
  if not isinstance(e[key],str) or not e[key].strip():raise ValueError('Cost event needs '+key)
 if not re.fullmatch(r'[A-Za-z0-9._:/-]{1,100}',e['unit']):raise ValueError('Use an explicit currency or credit unit')
 if e['provenance'] not in {'owner_report','operator_observation','supplied_report','independent_check'}:raise ValueError('Record evidence provenance')
 if e['kind']=='limit':
  if e['operation'] is not None:raise ValueError('Project cap is not an operation')
 elif not isinstance(e['operation'],str) or not e['operation'].strip():raise ValueError('Use a distinct operation/attempt ID')
 n=amount(e['amount'],e['kind']=='adjust')
 if e['kind'] in {'reserve','limit','settle','adjust'} and n is None:raise ValueError('Known amount required')
 if e['kind'] in {'release','unknown'} and n is not None:raise ValueError('No amount for this event kind')
 if e.get('receipt') is not None and (not isinstance(e['receipt'],str) or not e['receipt'].strip()):raise ValueError('Invalid receipt identity')
 if e['kind'] in {'settle','adjust'} and not e.get('receipt'):raise ValueError('Settlement/adjustment needs supplier receipt identity')
 if 'tags' in e and (not isinstance(e['tags'],list) or any(not isinstance(t,str) or not t for t in e['tags']) or len(set(e['tags']))!=len(e['tags'])):raise ValueError('Tags are distinct dimensions,not charges')
 for name in ['observed_at','recorded_at']:
  if e.get(name) and datetime.fromisoformat(e[name]).tzinfo is None:raise ValueError('Cost timestamp needs timezone')
 return e

def validate_stored(data):
 if 'costs' not in data:return
 c=data['costs']
 if not isinstance(c,dict) or c.get('schema')!='framewright-project-costs-v1' or c.get('events') is None or data.get('costs_sha256')!=digest(c):raise ValueError('Cost ledger integrity mismatch')
 seen=set();receipts=set()
 for e in c['events']:
  validate_event(e)
  if e['id'] in seen:raise ValueError('Duplicate cost event')
  seen.add(e['id'])
  if e.get('receipt'):
   key=(e['supplier'],e['receipt'])
   if key in receipts:raise ValueError('Duplicate supplier receipt')
   receipts.add(key)


def report(data):
 with localcontext() as context:
  context.prec=128
  return _report(data)


def _report(data):
 validate_stored(data)
 limits={};ops={}
 for e in data.get('costs',{}).get('events',[]):
  n=amount(e['amount'],e['kind']=='adjust');unit=e['unit']
  if e['kind']=='limit':limits[unit]=n;continue
  o=ops.setdefault(e['operation'],{'unit':unit,'estimate':None,'reserve':None,'usage':None,'settle':None,'adjust':Decimal(0),'unknown':False,'released':False})
  if o['unit']!=unit:raise ValueError('An operation cannot mix units')
  kind=e['kind']
  if kind in {'estimate','reserve','usage','settle'}:o[kind]=n
  if kind=='adjust':o['adjust']+=n
  if kind=='unknown' or kind=='usage' and n is None:o['unknown']=True
  if kind=='settle' or kind=='release':o['unknown']=False
  if kind=='release':o['released']=True
  elif kind in {'usage','unknown'}:o['released']=False
 units={}
 for unit in sorted(set(limits)|{o['unit'] for o in ops.values()}):
  values=[o for o in ops.values() if o['unit']==unit];reserved=Decimal(0);settled=Decimal(0);observed=Decimal(0);adjusted=Decimal(0);exposure=Decimal(0);unknown=0;unbounded=False
  for o in values:
   if o['usage'] is not None:observed+=o['usage']
   if o['unknown']:unknown+=1
   if o['settle'] is not None:
    settled+=o['settle'];adjusted+=o['adjust'];exposure+=o['settle']+o['adjust']
    if o['unknown']:unbounded=True
   elif not o['released']:
    if o['reserve'] is not None:reserved+=o['reserve']
    known=[n for n in [o['reserve'],o['usage']] if n is not None]
    if known:exposure+=max(known)
    if o['unknown'] and o['reserve'] is None:unbounded=True
  cap=limits.get(unit)
  units[unit]={'approved':str(cap) if cap is not None else None,'reserved':str(reserved),'observed':str(observed),'settled':str(settled),'adjustments':str(adjusted),'known_exposure':str(exposure),'unknown_operations':unknown,'remaining':str(cap-exposure) if cap is not None and not unbounded else None,'over_cap':cap is not None and exposure>cap,'estimated':None if any(o['estimate'] is None for o in values) else str(sum((o['estimate'] for o in values),Decimal(0)))}
 return {'schema':'framewright-project-cost-report-v1','units':units,'execution_authorized':False,'scope':'Recorded caps/usage/bills are separate; columns are not additive. Unknown exposure blocks admission. No FX conversion,provider enforcement or permission to spend.'}


def record(data,event,P):
 with localcontext() as context:
  context.prec=128
  return _record(data,event,P)


def _record(data,event,P):
 if data.get('schema_version')!=2:raise ValueError('Migrate project to schema v2 first')
 validate_stored(data);e=json.loads(json.dumps(event));validate_event(e)
 events=data.get('costs',{}).get('events',[])
 if len(events)>=10000:raise ValueError('Cost event bound reached')
 for prior in events:
  same_id=e['id']==prior['id'];same_receipt=e.get('receipt') and (e['supplier'],e['receipt'])==(prior['supplier'],prior.get('receipt'))
  if same_id or same_receipt:
   clean=lambda v:{k:x for k,x in v.items() if k not in {'id','recorded_at','pin'}}
   if clean(e)==clean(prior):return False
   raise ValueError('Conflicting event/receipt; append a distinct reconciliation or adjustment')
 if e.get('task') and e['task'] not in {s['id'] for s in data['steps']}:raise ValueError('Unknown project task')
 if e.get('subject'):
  e['pin']=P['JOURNAL']['pin'](data,e['subject'])
 prior=[r for r in events if r['operation']==e['operation'] and e['operation'] is not None]
 if prior and any((r['unit'],r['supplier'],r['category'],r.get('task'),r.get('subject'),r.get('pin'))!=(e['unit'],e['supplier'],e['category'],e.get('task'),e.get('subject'),e.get('pin')) for r in prior):raise ValueError('Operation binding changed; use a new attempt ID')
 if e['kind']=='reserve':
  if any(r['kind'] in {'reserve','settle','release'} for r in prior):raise ValueError('Use a new attempt; do not reuse an existing reservation')
  remaining=report(data)['units'].get(e['unit'],{}).get('remaining')
  if remaining is None or amount(e['amount'])>Decimal(remaining):raise ValueError('Missing/unknown/insufficient recorded budget; reservation refused')
 if e['kind']=='settle':
  refunds=sum((amount(r['amount'],True) for r in prior if r['kind']=='adjust'),Decimal(0))
  if amount(e['amount'])+refunds<0:raise ValueError('Corrected settlement is below existing refunds; reconcile adjustments first')
 if e['kind']=='adjust':
  settlements=[r for r in prior if r['kind']=='settle']
  if not settlements:raise ValueError('Adjustment requires a reconciled operation')
  total=amount(settlements[-1]['amount'])+sum((amount(r['amount'],True) for r in prior if r['kind']=='adjust'),Decimal(0))+amount(e['amount'],True)
  if total<0:raise ValueError('Refund exceeds recorded charge')
 e['recorded_at']=datetime.now(timezone.utc).isoformat()
 data.setdefault('costs',{'schema':'framewright-project-costs-v1','events':[]})['events'].append(e)
 data['costs_sha256']=digest(data['costs']);P['event'](data,'cost_event',identity=e['id'],kind=e['kind'],operation=e['operation'])
 return True


def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('project',type=Path);p.add_argument('--event',type=Path)
 a=p.parse_args();P=runpy.run_path(str(Path(__file__).with_name('project.py')))
 try:
  path=a.project.resolve(strict=True)
  with P['locked'](path):
   d=P['load'](path)
   if a.event and record(d,json.loads(a.event.read_text()),P):P['save'](path,d)
   print(json.dumps(report(d),indent=2,allow_nan=False))
 except (OSError,ValueError,KeyError,TypeError) as e:p.error(str(e))

if __name__=='__main__':main()
