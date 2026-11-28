#!/usr/bin/env python3
"""Read-only studio budgets and business priorities from one existing project checkpoint.
Uses pinned inputs and the existing cost ledger. Does not generate, purchase or publish.
"""
import argparse,copy
from datetime import datetime,timezone,date
from decimal import Decimal,localcontext
import hashlib,json,runpy
from pathlib import Path
BASE=Path(__file__).resolve().parent
C=runpy.run_path(str(BASE/'costs.py'))
R=runpy.run_path(str(BASE/'relationships.py'))
CATEGORIES={'client':0,'partner':0,'own_production':1,'editorial':2,'own_research':3}
STATES={'active','queued','waiting','paused','done'}
def timestamp(value):
 d=datetime.fromisoformat(value)
 if d.tzinfo is None:raise ValueError('Timestamp needs timezone')
 return d

def read_profile(data,root):
 pin=data['inputs'].get('studio-management')
 if not pin:raise ValueError('Retain studio-management input in the existing project first')
 p=(root/pin['path']).resolve();raw=p.read_bytes()
 if len(raw)!=pin['bytes'] or hashlib.sha256(raw).hexdigest()!=pin['sha256']:raise ValueError('Studio management input changed; explicitly retain its new revision')
 profile=json.loads(raw)
 if profile.get('schema_version')!=1:raise ValueError('Unsupported studio management schema')
 return profile

def validate(profile):
 services=profile.get('services');work=profile.get('work')
 if not isinstance(services,list) or not isinstance(work,list):raise ValueError('Services and work must be lists')
 ids=set();units=set();workids=set()
 for service in services:
  if not isinstance(service.get('id'),str) or not service['id'] or service['id'] in ids:raise ValueError('Duplicate/empty service ID')
  ids.add(service['id'])
  for pool in service.get('pools',[]):
   if not pool.get('id') or pool.get('unit') in units or not pool.get('unit'):raise ValueError('Distinct credit unit required per pool')
   units.add(pool['unit']);C['amount'](pool.get('opening_balance'));timestamp(pool['observed_at'])
   if pool.get('expires_on'):date.fromisoformat(pool['expires_on'])
   if pool.get('nonexpiring') is not None and type(pool.get('nonexpiring')) is not bool:raise ValueError('nonexpiring must be a boolean')
   refresh=pool.get('refresh',{})
   if refresh.get('cadence','unknown') not in {'daily','monthly','weekly','rolling','one_time','unknown'}:raise ValueError('Unknown refresh cadence')
   if refresh.get('rollover','unknown') not in {'yes','no','unknown'}:raise ValueError('Unknown rollover rule')
   C['amount'](refresh.get('amount'))
   if refresh.get('next_reset_at'):timestamp(refresh['next_reset_at'])
   models=pool.get('eligible_models')
   if models is not None and (not isinstance(models,list) or any(not isinstance(x,str) or not x for x in models)):raise ValueError('Models must be null(unknown), [], or explicit names; use ["*"] for unrestricted')
   for grant in pool.get('grants',[]):
    C['amount'](grant.get('amount'));timestamp(grant['observed_at'])
    if grant.get('status') not in {'confirmed','conditional'}:raise ValueError('Grant status required')
 for row in work:
  if not row.get('id') or row['id'] in workids:raise ValueError('Duplicate/empty work ID')
  workids.add(row['id'])
  if row.get('category') not in CATEGORIES or row.get('status') not in STATES:raise ValueError('Unknown work category/state')
  if type(row.get('priority')) is not int or not 1<=row['priority']<=5:raise ValueError('Priority must be1..5')
  if not row.get('next_step') or not isinstance(row.get('blockers'),list):raise ValueError('Next step and explicit blockers required')
  for field in ('deadline','target_date'):
   if row.get(field):date.fromisoformat(row[field])
  for budget in row.get('budgets',[]):
   if budget.get('unit') not in units or budget.get('state') not in {'proposed','authorized'}:raise ValueError('Unknown budget pool/state')
   if C['amount'](budget.get('amount')) is None:raise ValueError('Known allocation amount required')
 if sum(r['status']=='active' for r in work)>5:raise ValueError('At most five active business work items')
 R['validate'](profile)

def report(data,profile,now,root=None):
 validate(profile);costs=C['report'](data)['units'];pools=[];known_units=set()
 for service in profile['services']:
  for pool in service.get('pools',[]):
   unit=pool['unit'];known_units.add(unit);ledger=costs.get(unit,{})
   opening=C['amount'](pool.get('opening_balance'));observed=timestamp(pool['observed_at'])
   grants=[g for g in pool.get('grants',[]) if g['status']=='confirmed' and timestamp(g['observed_at'])<=now]
   grant_amount=sum((C['amount'](g['amount']) for g in grants if g['amount'] is not None),Decimal(0))
   unknown_funding=any(g['amount'] is None for g in grants)
   exposure=Decimal(ledger.get('known_exposure','0'));unknown=int(ledger.get('unknown_operations',0));unbounded=unit in costs and ledger.get('remaining') is None
   # Remaining from the cost report can be null because no cap exists, not because a known reserve is unbounded.
   events=[e for e in data.get('costs',{}).get('events',[]) if e['unit']==unit]
   unbounded=bool(ledger.get('approved') is not None and ledger.get('remaining') is None)
   if ledger.get('approved') is None and unknown:
    operations={}
    for e in events:
     if e['operation'] is None:continue
     op=operations.setdefault(e['operation'],{'unknown':False,'reserved':False,'settled':False})
     if e['kind']=='reserve':op['reserved']=True
     if e['kind']=='settle':op.update(unknown=False,settled=True)
     if e['kind']=='release':op.update(unknown=False,reserved=False)
     if e['kind']=='unknown' or e['kind']=='usage' and e['amount'] is None:op['unknown']=True
    unbounded=any(o['unknown'] and (o['settled'] or not o['reserved']) for o in operations.values())
   forecast=None if opening is None or unknown_funding or unbounded else opening+grant_amount-exposure
   proposed=sum((C['amount'](b['amount']) for w in profile['work'] if w['status'] not in {'done','paused'} for b in w.get('budgets',[]) if b['unit']==unit and b['state']=='proposed'),Decimal(0))
   allocated=sum((C['amount'](b['amount']) for w in profile['work'] if w['status'] not in {'done','paused'} for b in w.get('budgets',[]) if b['unit']==unit and b['state']=='authorized'),Decimal(0))
   expires=pool.get('expires_on');expiry=('valid' if pool.get('nonexpiring') is True else 'unknown') if not expires else ('expired' if now.date()>=date.fromisoformat(expires) else 'valid')
   refresh=pool.get('refresh',{});reset=refresh.get('next_reset_at');refresh_status='needs_current_balance' if reset and now>=timestamp(reset) else 'current_window' if reset else 'reset_unknown'
   pools.append({'refresh':refresh,'refresh_status':refresh_status,'service':service['id'],'pool':pool['id'],'unit':unit,'observed_opening_balance':str(opening) if opening is not None else None,'observed_at':pool['observed_at'],'confirmed_topups':str(grant_amount),'settled':ledger.get('settled','0'),'pending_exposure':str(exposure-Decimal(ledger.get('settled','0'))-Decimal(ledger.get('adjustments','0'))),'known_exposure':str(exposure),'unknown_operations':unknown,'forecast_remaining':str(forecast) if forecast is not None else None,'budget_remaining':ledger.get('remaining'),'proposed_allocations':str(proposed),'authorized_allocations':str(allocated),'overallocated':forecast is not None and proposed+allocated>forecast,'expires_on':expires,'expiry_status':expiry,'eligible_models':pool.get('eligible_models'),'renewal':pool.get('renewal','unknown'),'future_observation':observed>now,'source_provenance':pool.get('provenance','unknown'),'balance_kind':'Forecast from opening snapshot and local costs;not a fresh provider balance'})
 def order(w):return (CATEGORIES[w['category']],w['priority'],w.get('deadline') or '9999-12-31',w.get('target_date') or '9999-12-31',w['id'])
 work=sorted(profile['work'],key=order)
 ready=[w for w in work if w['status']=='active' and not w['blockers']]
 waiting=[w for w in work if w['status']=='waiting' or w['blockers'] and w['status'] not in {'paused','done'}]
 options=[]
 for service in profile['services']:
  for quote in service.get('quotes',[]):
   price=C['amount'](quote.get('credits'));model=quote.get('model') or quote.get('operation')
   if price is None or price<=0:continue
   candidates=[]
   for pool in pools:
    models=pool['eligible_models']
    if pool['service']!=service['id'] or models is None or '*' not in models and model not in models:continue
    fresh=not pool['future_observation'] and pool['expiry_status']=='valid' and pool['refresh_status']!='needs_current_balance'
    funding=C['amount'](pool['forecast_remaining']);cap=C['amount'](pool['budget_remaining'])
    n=None if not fresh or funding is None or cap is None else max(Decimal(0),min(funding,cap))//price
    candidates.append({'unit':pool['unit'],'budgeted_attempts':str(n) if n is not None else None,'availability':'budget_fits' if n is not None and n>0 else 'budget_not_assigned_or_insufficient' if n==0 else 'verify_balance_expiry_or_reset'})
   options.append({'service':service['id'],'model':model,'configuration':quote,'pools':candidates,'provider_availability':'not_verified','scope':'Quoted attempts within local bounds,not guaranteed successful generations;do not combine candidate pools.'})
 return {**R['report'](data,profile,now,root),'schema':'framewright-studio-management-v1','today_options':options,'services':[{'id':x['id'],'name':x.get('name',x['id']),'terms':x.get('terms','Unknown'),'open_questions':x.get('open_questions',[])} for x in profile['services']],'as_of':now.isoformat(),'budgets':pools,'unmapped_cost_units':sorted(set(costs)-known_units),'plan':{'ready':ready,'waiting':waiting,'queued':[w for w in work if w['status']=='queued' and not w['blockers']],'paused':[w for w in work if w['status']=='paused'],'done':[w for w in work if w['status']=='done']},'execution_authorized':False,'scope':'Business priorities and separate credit pools over the existing project/cost ledger. Allocations are plans,not reservations. No cross-unit total,provider calls,automatic renewals or automatic scheduling.'}

def admit(view,unit,value,model):
 n=C['amount'](value)
 if n is None or n<=0:raise ValueError('Positive known quote required')
 pool=next((p for p in view['budgets'] if p['unit']==unit),None)
 if not pool:raise ValueError('Unknown credit pool')
 if pool['future_observation'] or pool['expiry_status']!='valid' or pool.get('refresh_status')=='needs_current_balance':raise ValueError('Credit observation/expiry needs verification before reservation')
 models=pool['eligible_models']
 if models is None or '*' not in models and model not in models:raise ValueError('Model not verified for this pool')
 if pool['forecast_remaining'] is None or pool['budget_remaining'] is None:raise ValueError('Unknown funding/exposure or no explicit cost limit')
 if n>Decimal(pool['forecast_remaining']) or n>Decimal(pool['budget_remaining']):raise ValueError('Quote exceeds pool or recorded budget remaining')
 return {'allowed':True,'unit':unit,'amount':str(n),'model':model,'execution_authorized':False,'note':'Local budget admission only; quote, actual debit pool and retry outcome still need provider verification.'}

def render_html(view):
 from html import escape as h
 def text(value):return h(str(value if value is not None else 'Unknown'))
 cells=[]
 for p in view['budgets']:
  cells.append('<tr>'+''.join('<td>'+text(p[k])+'</td>' for k in ['service','pool','observed_opening_balance','known_exposure','forecast_remaining','budget_remaining','proposed_allocations','expires_on'])+'</tr>')
 options=[]
 for option in view.get('today_options',[]):
  fits=[p for p in option['pools'] if p['availability']=='budget_fits']
  if fits:options.append('<li>'+text(option['service'])+' · '+text(option['model'])+' · quote '+text(option['configuration'].get('credits'))+' · '+text('; '.join(p['budgeted_attempts']+' attempt(s) in '+p['unit'] for p in fits))+'</li>')
 work=[]
 for service in view.get('services',[]):
  quota=[p for p in view['budgets'] if p['service']==service['id']]
  refresh='; '.join(p['pool']+': '+str(p['refresh'].get('cadence','unknown'))+', rollover '+str(p['refresh'].get('rollover','unknown'))+', next reset '+str(p['refresh'].get('next_reset_at') or 'unknown') for p in quota)
  work.append('<details><summary>'+text(service['name'])+' · conditions and quota refresh</summary><p>'+text(service['terms'])+'</p><p class="note">'+text(refresh)+'</p></details>')
 if options:work.append('<h2>Quoted options in current budgets</h2><p class="note">Local financial fit only. Check current provider access,exact settings and debit pool before submitting. Do not add alternative pools together.</p><ul>'+''.join(options)+'</ul>')
 for state,rows in view['plan'].items():
  if not rows:continue
  work.append('<h2>'+text(state.title())+'</h2>')
  for row in rows:
   deadline=('Committed deadline: '+str(row.get('deadline'))) if row.get('deadline') else ('Internal target: '+str(row.get('target_date'))) if row.get('target_date') else 'Date not committed'
   work.append('<article><small>'+text(row['category'])+' · P'+text(row['priority'])+' · '+text(deadline)+'</small><h3>'+text(row['title'])+'</h3><p>'+text(row['next_step'])+'</p>'+('<p class="wait">Waiting: '+text('; '.join(row['blockers']))+'</p>' if row['blockers'] else '')+'</article>')
 return '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Framewright · Production plan and budgets</title><style>body{margin:0;background:#090b0c;color:#e9eeeb;font:16px/1.6 system-ui,sans-serif}main{max-width:1180px;margin:auto;padding:32px 20px}h1{font-size:clamp(28px,5vw,48px);line-height:1.15}h2{margin-top:40px}small,.note{color:#abb5af}article{overflow-wrap:anywhere;border:1px solid #303936;padding:18px;margin:14px 0;border-radius:10px}h3{margin:6px 0}.wait{color:#e9c98f}.scroll{overflow:auto}table{border-collapse:collapse;min-width:900px;width:100%}th,td{padding:12px;text-align:left;border-bottom:1px solid #303936}th{color:#b5ebd6}.note{max-width:850px}</style><main><p>FRAMEWRIGHT / PRIVATE STUDIO</p><h1>Production plan<br>and resource budgets</h1><p class="note">As of '+text(view['as_of'])+'. Opening balances are dated observations. Forecasts deduct recorded exposure. Separate credit pools are never added together. A plan does not start production or authorize spending.</p><h2>Resources</h2><div class="scroll"><table><thead><tr>'+''.join('<th>'+x+'</th>' for x in ['Service','Pool','Opening','Exposure','Forecast left','Budget left','Proposed','Expires'])+'</tr></thead><tbody>'+''.join(cells)+'</tbody></table></div><p class="note">Unknown remains unknown. Proposed allocations are not reservations. Provider costs and expiry must be rechecked before each submission.</p>'+(R['html'](view['relationships']) if view.get('relationships') else '')+''.join(work)+'</main></html>'

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('project',type=Path);p.add_argument('--at');p.add_argument('--check-unit');p.add_argument('--amount');p.add_argument('--model');p.add_argument('--reserve',type=Path);p.add_argument('--html',type=Path);p.add_argument('--relationship',help='Show one linked relationship; shared account budgets remain account-wide');a=p.parse_args()
 try:
  P=runpy.run_path(str(BASE/'project.py'));path=a.project.resolve(strict=True)
  now=timestamp(a.at) if a.at else datetime.now(timezone.utc)
  if a.reserve:
   with P['locked'](path):
    data=P['load'](path);profile=read_profile(data,path.parent);view=report(data,profile,now,path.parent);e=json.loads(a.reserve.read_text())
    if e.get('kind')!='reserve':raise ValueError('Use existing costs.py for non-reservation receipt events')
    if a.at:raise ValueError('Reservation uses current time; --at is read-only planning only')
    candidate=copy.deepcopy(data);changed=C['record'](candidate,e,P)
    check=admit(view,e['unit'],e['amount'],a.model) if changed else {'allowed':True,'duplicate':True,'execution_authorized':False}
    if changed:P['save'](path,candidate)
    view=report(candidate,profile,now,path.parent);view['admission']=check
  else:
   data=P['load'](path);profile=read_profile(data,path.parent);view=report(data,profile,now,path.parent)
   if a.check_unit:view['admission']=admit(view,a.check_unit,a.amount,a.model)
  if a.relationship:
   rows=[r for r in view['relationships'] if r['id']==a.relationship]
   if not rows:raise ValueError('Unknown relationship ID')
   view['relationships']=rows;view['selected_relationship']=a.relationship
   view['correspondence_attention']=[r for r in view['correspondence_attention'] if r['relationship_id']==a.relationship]
   linked=set(rows[0]['work_ids'])
   view['plan']={state:[w for w in items if w['id'] in linked] for state,items in view['plan'].items()}
  if a.html:
   destination=a.html.resolve()
   protected={path,*[(path.parent/v['path']).resolve() for v in data['inputs'].values()],*[(path.parent/v['file']['path']).resolve() for v in data['artifacts'].values() if v.get('file')]}
   protected.update((path.parent/w['project_file']).resolve() for w in profile['work'] if w.get('project_file'))
   if destination in protected:raise ValueError('HTML output cannot overwrite retained project inputs/artifacts')
   destination.write_text(render_html(view),encoding='utf-8')
  print(json.dumps(view,ensure_ascii=False,indent=2,allow_nan=False))
 except (OSError,ValueError,KeyError,TypeError) as e:p.error(str(e))
if __name__=='__main__':
 with localcontext() as context:
  context.prec=128
  main()
