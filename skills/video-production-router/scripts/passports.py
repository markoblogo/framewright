#!/usr/bin/env python3
"""Versioned character/environment passports in the existing project. No automatic visual identity checks."""
import argparse
import json
from pathlib import Path
import runpy

BASE=Path(__file__).resolve().parent
T=runpy.run_path(str(BASE/'trials.py'));P=T['P'];J=T['J']


def vec(value,label):
    if not isinstance(value,list) or len(value)!=3:raise ValueError(label+' needs three numbers')
    for n in value:
        if type(n) not in (int,float):raise ValueError(label+' needs numbers')
    # Also rejects NaN/Infinity, without forbidding negative coordinates.
    json.dumps(value,allow_nan=False)


def validate(spec):
    common=['id','version','kind','name','references','dimensions_m','materials','constraints']
    if not isinstance(spec,dict) or spec.get('kind') not in {'character','environment'}:raise ValueError('Character or environment passport required')
    T['keys'](spec,common+[spec['kind']]);T['identity'](spec['id']);T['identity'](spec['version']);T['text'](spec['name'],'name')
    if not isinstance(spec['references'],list) or any(not isinstance(s,str) for s in spec['references']) or len(set(spec['references']))!=len(spec['references']):raise ValueError('References need distinct retained subjects')
    if spec['dimensions_m'] is not None:
        vec(spec['dimensions_m'],'dimensions_m')
        if any(n<=0 for n in spec['dimensions_m']):raise ValueError('Dimensions must be positive metres')
    if not isinstance(spec['materials'],list) or not isinstance(spec['constraints'],list):raise ValueError('Materials/constraints need lists')
    seen=set()
    for row in spec['materials']:
        T['keys'](row,['id','description','subject']);T['identity'](row['id']);T['text'](row['description'],'material description')
        if row['id'] in seen:raise ValueError('Duplicate material ID')
        seen.add(row['id'])
        if row['subject'] is not None:T['text'](row['subject'],'material subject')
    for c in spec['constraints']:T['text'](c,'constraint')
    if spec['kind']=='character':
        c=spec['character'];T['keys'](c,['proportions','clothing','palette','rig','actions'])
        for k in ['proportions','clothing']:
            if not isinstance(c[k],str):raise ValueError(k+' must be text; empty means unresolved')
        if not isinstance(c['palette'],list) or any(not isinstance(s,str) or not s.strip() for s in c['palette']):raise ValueError('Palette needs text values')
        T['keys'](c['rig'],['required','subject','note'])
        if type(c['rig']['required']) is not bool:raise ValueError('Rig required must be boolean')
        T['text'](c['rig']['note'],'rig note')
        if c['rig']['subject'] is not None:T['text'](c['rig']['subject'],'rig subject')
        if not isinstance(c['actions'],list):raise ValueError('Actions need a list')
        seen=set()
        for a in c['actions']:
            T['keys'](a,['id','subject','note']);T['identity'](a['id']);T['text'](a['note'],'action note')
            if a['id'] in seen:raise ValueError('Duplicate action ID')
            seen.add(a['id'])
            if a['subject'] is not None:T['text'](a['subject'],'action subject')
    else:
        e=spec['environment'];T['keys'](e,['layout','lighting','anchors'])
        if any(not isinstance(e[k],str) for k in ['layout','lighting']):raise ValueError('Layout and lighting must be text')
        if not isinstance(e['anchors'],list):raise ValueError('Anchors need a list')
        seen=set()
        for a in e['anchors']:
            T['keys'](a,['id','position_m','description']);T['identity'](a['id']);vec(a['position_m'],'anchor position');T['text'](a['description'],'anchor description')
            if a['id'] in seen:raise ValueError('Duplicate anchor ID')
            seen.add(a['id'])
    json.dumps(spec,allow_nan=False)


def sources(spec):
    result=list(spec['references'])+[r['subject'] for r in spec['materials'] if r['subject']]
    if spec['kind']=='character':
        c=spec['character']
        if c['rig']['subject']:result.append(c['rig']['subject'])
        result += [a['subject'] for a in c['actions'] if a['subject']]
    return list(dict.fromkeys(result))


def missing(spec):
    result=[]
    if not spec['references']:result.append('Approved visual reference not supplied')
    if spec['dimensions_m'] is None:result.append('Dimensions/scale unresolved')
    if not spec['materials']:result.append('Materials not described')
    if not spec['constraints']:result.append('Continuity constraints not described')
    if spec['kind']=='character':
        c=spec['character']
        for k in ['proportions','clothing']:
            if not c[k].strip():result.append(k+' unresolved')
        if not c['palette']:result.append('Palette unresolved')
        if c['rig']['required'] and not c['rig']['subject']:result.append('Required rig not retained')
        result += ['Action not retained: '+a['id'] for a in c['actions'] if not a['subject']]
    else:
        for k in ['layout','lighting']:
            if not spec['environment'][k].strip():result.append(k+' unresolved')
        if not spec['environment']['anchors']:result.append('Spatial anchors unresolved')
    return result


def create(data,project,spec,output,actor,supersedes=None):
    validate(spec);T['text'](actor,'actor');key='passport:'+spec['id']+':'+spec['version']
    if key in data['artifacts']:raise ValueError('Passport version already exists; use a new version')
    pins={s:T['current'](data,project,s)[0] for s in sources(spec)}
    if supersedes:
        _,path=T['current'](data,project,supersedes);old=T['read_json'](path)
        if old.get('schema')!='framewright-passport-v1' or old.get('project')!=str(project) or old['spec']['id']!=spec['id'] or old['spec']['kind']!=spec['kind']:
            raise ValueError('Superseded passport must be the same family/kind/project')
        if old['spec']['version']==spec['version']:raise ValueError('Use a new version')
        pins[supersedes]=J['pin'](data,supersedes)
    record={'schema':'framewright-passport-v1','project':str(project),'subject':'output:'+key,
            'spec':spec,'pins':pins,'supersedes':supersedes,'visual_identity_checked':False,'rights_cleared':False}
    T['write'](output,record);subject=T['register'](data,project,key,output,'entity-passport')
    J['append'](data,subject,'decision','proposed',actor,'operator_observation',
                'Passport '+spec['id']+' '+spec['version']+' created; visual consistency and rights not verified',
                'passport-definition',pins)
    P['event'](data,'passport_create',subject=subject)
    return record


def state(data,project,subject):
    _,path=T['current'](data,project,subject);record=T['read_json'](path)
    if record.get('schema')!='framewright-passport-v1' or record.get('project')!=str(project):raise ValueError('Expected passport in this project')
    validate(record['spec']);issues=T['changed'](data,project,record['pins']);unresolved=missing(record['spec'])
    rows=[r for r in data['journal'] if r['subject']==subject and r['kind']=='creative' and r['topic']=='passport-review']
    review=rows[-1] if rows else None
    approved=bool(review and review['result']=='accepted' and review['provenance']=='owner_report' and not T['changed'](data,project,review['pins']))
    status='stale' if issues else 'incomplete' if unresolved else 'approved' if approved else 'rejected' if review and review['result']=='rejected' else 'draft'
    return {'subject':subject,'id':record['spec']['id'],'version':record['spec']['version'],'kind':record['spec']['kind'],
            'state':status,'missing':unresolved,'stale_reasons':issues,'visual_identity_checked':False,'rights_cleared':False,
            'review':review['id'] if review else None,'note':'Canonical description and manual decision only; no automatic identity or asset-rights verification'}


def uses(data,project,subject):
    state(data,project,subject);result=[]
    for key,artifact in data['artifacts'].items():
        if artifact['kind']!='shot-card' or not artifact['file']:continue
        try:
            _,path=T['current'](data,project,'output:'+key);r=T['read_json'](path)
            if any(b['passport']==subject for b in r['spec']['bindings']):
                result.append({'shot':'output:'+key,'stale_reasons':T['changed'](data,project,r['pins'])})
        except (OSError,ValueError,KeyError,TypeError):result.append({'shot':'output:'+key,'status':'unreadable; usage unknown'})
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__);cmd=p.add_subparsers(dest='command',required=True)
    a=cmd.add_parser('create');a.add_argument('project',type=Path);a.add_argument('spec',type=Path);a.add_argument('--output',type=Path,required=True);a.add_argument('--actor',required=True);a.add_argument('--supersedes')
    for name in ['status','uses']:
        a=cmd.add_parser(name);a.add_argument('project',type=Path);a.add_argument('subject');a.add_argument('--json',action='store_true')
    args=p.parse_args()
    try:
        project=args.project.resolve()
        with P['locked'](project):
            data=P['load'](project)
            if data['schema_version']!=2:raise ValueError('Explicit schema-2 migration required')
            if args.command=='create':
                record=create(data,project,T['read_json'](args.spec),args.output,args.actor,args.supersedes);P['save'](project,data)
                result={'subject':record['subject'],'state':state(data,project,record['subject'])['state']}
            else:result=state(data,project,args.subject) if args.command=='status' else uses(data,project,args.subject)
            print(json.dumps(result,indent=2,allow_nan=False))
    except (OSError,ValueError,KeyError,TypeError) as exc:p.error(str(exc))


if __name__=='__main__':main()
