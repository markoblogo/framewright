#!/usr/bin/env python3
"""Offline producer intake: explicit preferences and supplied, unverified options."""
import argparse
import json
import math
import os
from pathlib import Path
import platform
import runpy
import shutil
import sys
import tempfile

BASE=Path(__file__).resolve().parent
ENV=runpy.run_path(str(BASE/'environment.py'))
REFS=BASE.parent/'references'


def read(path):
    with path.open(encoding='utf-8') as f:return json.load(f)


def profile(path):
    p=read(path)
    if not isinstance(p,dict) or set(p)!={'schema','options','subscriptions','sharing'} or p['schema']!='framewright-intake-v1':
        raise ValueError('Invalid local profile schema')
    if p['options'] not in {'both','free-only'} or p['sharing'] not in {'off','interested'} or not isinstance(p['subscriptions'],dict):
        raise ValueError('Invalid preferences')
    if any(not isinstance(k,str) or not k.strip() or v not in {'unknown','available','unavailable'} for k,v in p['subscriptions'].items()):
        raise ValueError('Subscriptions require named unknown/available/unavailable states')
    return p


def replace(path,value):
    temp=None
    try:
        with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',dir=path.parent,delete=False) as f:
            temp=Path(f.name);json.dump(value,f,indent=2,ensure_ascii=False);f.write('\n');f.flush();os.fsync(f.fileno())
        os.replace(temp,path)
    finally:
        if temp is not None:temp.unlink(missing_ok=True)


def propose(p,brief,options,catalog=None):
    if not isinstance(brief,dict) or not isinstance(brief.get('idea'),str) or not brief['idea'].strip():
        raise ValueError('A nonempty idea is required')
    questions=[]
    for key in ['duration_seconds','format','language','source_rights','deadline']:
        if brief.get(key) is None or brief.get(key)=='':questions.append(key)
    if p['options']=='both' and (brief.get('budget') is None or brief.get('budget')==''):
        questions.append('budget')
    rows=options.get('routes') if isinstance(options,dict) else None
    if not isinstance(rows,list):raise ValueError('Options must contain a routes list')
    entries={}
    if catalog is not None:
        if not isinstance(catalog,dict) or catalog.get('schema')!='framewright-provider-terms-v1' or not isinstance(catalog.get('providers'),dict):
            raise ValueError('Invalid provider terms catalogue')
        entries=catalog['providers']
    clean=[];seen=set()
    for r in rows:
        if not isinstance(r,dict) or not {'id','label','cost_kind','cost','currency','evidence'} <= set(r) or set(r)-{'id','label','cost_kind','cost','currency','evidence','provider_id'}:
            raise ValueError('Each route requires id, label, cost_kind, cost, currency, evidence')
        if 'provider_id' in r and (not isinstance(r['provider_id'],str) or not r['provider_id'].strip()):raise ValueError('Invalid provider ID')
        if any(not isinstance(r[k],str) or not r[k].strip() for k in ['id','label','currency']):raise ValueError('Route fields require text')
        if r['id'] in seen:raise ValueError('Duplicate route ID')
        seen.add(r['id'])
        if r['cost_kind'] not in {'free_local','free_quota','paid','unknown'} or r['evidence'] not in {'tested_scoped','documented','unknown'}:
            raise ValueError('Invalid cost kind or evidence')
        value=r['cost']
        if value is not None and (type(value) not in (int,float) or not math.isfinite(value) or value<0):raise ValueError('Invalid cost')
        if r['cost_kind']=='free_local' and value!=0:raise ValueError('Free local requires explicit zero provider cost')
        if r['cost_kind']=='unknown' and value is not None:raise ValueError('Unknown cost must remain null')
        if p['options']=='free-only' and r['cost_kind'] in {'paid','unknown'}:continue
        entry=entries.get(r.get('provider_id'))
        if r.get('provider_id') and catalog is not None and entry is None:raise ValueError('Unknown provider ID')
        if entry is not None and (not isinstance(entry,dict) or entry.get('cost_kind')!=r['cost_kind']):raise ValueError('Provider terms do not match route cost kind')
        clean.append({**r,'qualification':'supplied_option_not_verified',
                      'quota_terms':'unknown' if r['cost_kind']=='free_quota' else 'not_assessed',
                      'time_estimate':'unknown','rights':'unknown',
                      **({'provider_terms':entry,'terms_status':'historical_recheck_required',
                          'account_access':'user_declared_not_verified' if r['provider_id'] in p['subscriptions'] else 'unknown',
                          'account_declaration':p['subscriptions'].get(r['provider_id'],'unknown')} if entry is not None else {})})
    return {'schema':'framewright-intake-proposal-v1','questions':questions,'routes':clean,
            'selection_policy':p['options'],'execution':'not_authorized','sharing':'not_started',
            'note':'Supplied options are not verified, priced, ranked, connected or automatically executed.'}


def recommend(p,brief,task):
    """Discover task candidates, not complete production routes or access guarantees."""
    questions=propose(p,brief,{'routes':[]})['questions']
    search=runpy.run_path(str(BASE/'search.py'))
    registry=read(REFS/'tools.json');ledger=read(REFS/'review-ledger.json');facets=read(REFS/'arsenal-facets.json')
    known_tasks={t for row in facets['tools'].values() for t in row['tasks']}
    if task not in known_tasks:raise ValueError('Unknown task; choose an indexed arsenal task')
    costs=read(REFS/'intake-cost-facets.json')
    terms=read(REFS/'provider-terms-pilot.json')
    if costs.get('schema')!='framewright-intake-cost-facets-v1' or terms.get('schema')!='framewright-provider-terms-v1':raise ValueError('Invalid intake catalogue')
    inventory=search['inventory'](registry,ledger,facets)
    for identity,cost in costs['tools'].items():
        if identity not in inventory:raise ValueError('Cost facet references unknown tool: '+identity)
        if cost['kind']=='free_quota' and cost.get('provider_id') not in terms['providers']:raise ValueError('Missing provider terms: '+identity)
    query={'task':task,'features':[],'evidence':'any','tool':None,'text':'','style':None,'input':None,
           'rights':'any','language':brief.get('language') if task=='narration' else None,'include_fallbacks':False,'allow_paid':p['options']=='both',
           'canvas':{'width':1920,'height':1080,'fps':30},'combinations':False,'voice':None,'limit':len(inventory),'explain':False}
    found=search['search'](query,registry,ledger,facets)['results']
    candidates=[];excluded_unknown=0
    for row in found:
        cost=costs['tools'].get(row['id'],{'kind':'unknown'})
        if p['options']=='free-only' and cost['kind'] not in {'free_local','free_quota'}:
            excluded_unknown+=1;continue
        item={'id':row['id'],'name':row['name'],'task':task,'evidence':row['evidence'],
              'evidence_scope':row['evidence_scope'],'disposition':row['disposition'],
              'task_capabilities':row['task_capabilities'],'evidence_references':row['reference'],
              'cost_kind':cost['kind'],'cost':None,'rights':'review_required','access':'unknown',
              'qualification':'candidate_only','limitations':row['limits'],
              'retained_rights_note':row['rights']['retained_terms']}
        if 'basis' in cost:item['cost_basis']=cost['basis']
        if cost['kind']=='free_quota':
            pid=cost['provider_id'];item['provider_terms']=terms['providers'][pid]
            item['terms_status']='historical_recheck_required'
            item['account_declaration']=p['subscriptions'].get(pid,'unknown')
            item['access']='user_declared_not_verified' if pid in p['subscriptions'] else 'unknown'
        candidates.append(item)
    return {'schema':'framewright-intake-candidates-v1','task':task,'questions':questions,
            'candidates':candidates,'excluded_unclassified_cost':excluded_unknown,
            'selection_policy':p['options'],'execution':'not_authorized',
            'note':'Explicit task matches only; evidence applies to retained component scope, not the entire production. Costs, access, rights and compatibility require review.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    a=sub.add_parser('init');a.add_argument('profile',type=Path)
    a=sub.add_parser('preference');a.add_argument('profile',type=Path);a.add_argument('--options',choices=['both','free-only'],required=True)
    a=sub.add_parser('subscription');a.add_argument('profile',type=Path);a.add_argument('service');a.add_argument('--status',choices=['unknown','available','unavailable'],required=True)
    a=sub.add_parser('inspect');a.add_argument('--disk-root',type=Path,required=True)
    a=sub.add_parser('propose');a.add_argument('profile',type=Path);a.add_argument('brief',type=Path);a.add_argument('routes',type=Path);a.add_argument('--catalog',type=Path)
    a=sub.add_parser('recommend');a.add_argument('profile',type=Path);a.add_argument('brief',type=Path);a.add_argument('--task',required=True)
    a=sub.add_parser('routes');a.add_argument('profile',type=Path);a.add_argument('brief',type=Path);a.add_argument('--format',choices=['json','markdown'],default='json')
    a=sub.add_parser('brief');a.add_argument('profile',type=Path);a.add_argument('brief',type=Path);a.add_argument('--source-index',type=Path);a.add_argument('--project',type=Path);a.add_argument('--format',choices=['json','markdown'],default='json')
    args=parser.parse_args()
    try:
        if args.command=='init':
            p={'schema':'framewright-intake-v1','options':'both','subscriptions':{},'sharing':'off'}
            fd=os.open(args.profile,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
            with os.fdopen(fd,'w',encoding='utf-8') as f:json.dump(p,f,indent=2);f.write('\n')
            result={'created':str(args.profile),'network_calls':0}
        elif args.command=='preference':
            p=profile(args.profile);p['options']=args.options;replace(args.profile,p);result={'options':p['options'],'network_calls':0}
        elif args.command=='subscription':
            if not args.service.strip() or len(args.service)>80:raise ValueError('Use a short service name, never a credential')
            p=profile(args.profile);p['subscriptions'][args.service]=args.status;replace(args.profile,p)
            result={'service':args.service,'status':args.status,'basis':'user_declared_not_verified','network_calls':0}
        elif args.command=='inspect':
            disk=shutil.disk_usage(args.disk_root)
            result={'platform':platform.system(),'architecture':platform.machine(),'memory_gib':ENV['memory_gib'](),
                    'disk_root':str(args.disk_root.resolve()),'free_disk_gib':disk.free/2**30,
                    'internet_speed':'not_measured','subscriptions':'not_inspected','network_calls':0,
                    'scope':'Snapshot; total memory and free disk do not prove runtime capability.'}
        elif args.command=='recommend':result=recommend(profile(args.profile),read(args.brief),args.task)
        elif args.command=='brief':
            producer=runpy.run_path(str(BASE/'producer_brief.py'))
            result=producer['build'](profile(args.profile),read(args.brief),recommend,args.source_index,args.project)
            if args.format=='markdown':print(producer['markdown'](result));return
        elif args.command=='routes':
            routing=runpy.run_path(str(BASE/'intake_routes.py'))
            result=routing['compare'](profile(args.profile),read(args.brief),recommend)
            if args.format=='markdown':print(routing['markdown'](result));return
        else:result=propose(profile(args.profile),read(args.brief),read(args.routes),read(args.catalog) if args.catalog else None)
        print(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False))
    except (OSError,ValueError,TypeError,KeyError) as exc:parser.exit(2,str(exc)+'\n')

if __name__=='__main__':main()
