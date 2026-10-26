#!/usr/bin/env python3
"""Pinned experiment cards and local A/B review packs in the existing project journal. Never runs providers."""
import argparse
import copy
from datetime import datetime, timezone
import html
import json
import math
from pathlib import Path
import re
import runpy
import shutil

BASE=Path(__file__).resolve().parent
P=runpy.run_path(str(BASE/'project.py'));J=P['JOURNAL']
ENV=runpy.run_path(str(BASE/'environment.py'))


def text(value,label):return ENV['text'](value,label)
def keys(value,required,optional=()):return ENV['keys'](value,required,optional)
def number(value,label):return ENV['number'](value,label)


def identity(value):
    if not isinstance(value,str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,79}',value):
        raise ValueError('Use a short alphanumeric ID')
    return value


def read_json(path):
    value=json.loads(path.read_text());json.dumps(value,allow_nan=False);return value


def current(data,project,subject):
    pin=J['pin'](data,subject)
    if pin is None:raise ValueError('A retained file is required: '+subject)
    path=project.parent/pin['path']
    if P['file_record'](path,project.parent)!=pin:raise ValueError('Changed retained bytes: '+subject)
    return pin,path


def changed(data,project,pins):
    reasons=[]
    for subject,old in pins.items():
        try:
            pin,_=current(data,project,subject)
            if pin!=old:reasons.append(subject+': retained revision replaced')
        except (OSError,ValueError):reasons.append(subject+': missing or changed retained file')
    return reasons


def checked(data,project,subject,schema):
    _,path=current(data,project,subject);record=read_json(path)
    if record.get('schema')!=schema or record.get('project')!=str(project):raise ValueError('Wrong record/project')
    problems=changed(data,project,record['pins'])
    if problems:raise ValueError('Stale dependencies: '+'; '.join(problems))
    return record


def write(path,value):
    with path.open('x') as stream:stream.write(json.dumps(value,indent=2,allow_nan=False)+'\n')


def register(data,project,ident,path,kind):
    if ident in data['artifacts']:raise ValueError('Artifact ID already exists; choose a new attempt')
    data['artifacts'][ident]={'kind':kind,'scene':None,'file':None}
    P['retain'](data,project.parent,ident,path,False,False)
    return 'output:'+ident


def validate_spec(spec):
    keys(spec,['id','tool','capability','question','sources','baseline','candidate','criteria','limits'])
    identity(spec['id']);text(spec['tool'],'tool');text(spec['capability'],'bounded capability');text(spec['question'],'question')
    sources=spec['sources']
    if not isinstance(sources,list) or not sources or any(not isinstance(s,str) for s in sources) or len(set(sources))!=len(sources):
        raise ValueError('Use distinct retained source subjects')
    for arm in ['baseline','candidate']:
        keys(spec[arm],['method','settings']);text(spec[arm]['method'],arm+' method')
        if not isinstance(spec[arm]['settings'],dict):raise ValueError('settings must be an object, never executable commands')
    if not isinstance(spec['criteria'],list) or not spec['criteria']:raise ValueError('Explicit criteria required')
    seen=set()
    for c in spec['criteria']:
        keys(c,['id','kind','description']);identity(c['id']);text(c['description'],'criterion')
        if c['id'] in seen or c['kind'] not in {'technical','listening','creative'}:raise ValueError('Distinct criteria and explicit review kinds required')
        seen.add(c['id'])
    if not any(c['kind']=='technical' for c in spec['criteria']):raise ValueError('At least one technical criterion required')
    limits=spec['limits'];keys(limits,['max_cost','currency','max_seconds']);text(limits['currency'],'currency/unit')
    for field in ['max_cost','max_seconds']:
        if limits[field] is not None:number(limits[field],field)
    json.dumps(spec,allow_nan=False)


def plan(data,project,spec,output,actor):
    validate_spec(spec);text(actor,'actor');rid=spec['id'];key='trial:'+rid
    if key in data['artifacts']:raise ValueError('Trial ID already exists; preserve the old definition')
    pins={s:current(data,project,s)[0] for s in spec['sources']}
    record={'schema':'framewright-trial-v1','project':str(project),'subject':'output:'+key,
            'spec':spec,'pins':pins,'execution_authorized':False,'qualification':'not_tested'}
    write(output,record)
    subject=register(data,project,key,output,'trial-card')
    J['append'](data,subject,'decision','proposed',actor,'operator_observation',
                'Bounded experiment planned; no execution or QA performed','trial-definition:'+rid,spec['sources'])
    P['event'](data,'trial_plan',identity=rid)
    return record


def evaluate(spec,arms,data,project):
    blockers=[];checks=[]
    for arm,row in arms.items():
        if row['environment'] is None:blockers.append(arm+': environment snapshot absent')
        else:
            _,path=current(data,project,row['environment']);env=ENV['validate_report'](read_json(path))
            if env['technical_status']!='ready':blockers.append(arm+': environment '+env['technical_status'])
            age=(datetime.now(timezone.utc)-datetime.fromisoformat(env['observed_at'])).total_seconds()
            if age< -300 or age>86400:blockers.append(arm+': environment snapshot outside 24-hour comparison window')
            if env['rights']['status']!='allowed':blockers.append(arm+': rights '+env['rights']['status'])
            if env['cost']['status']=='unknown':blockers.append(arm+': environment cost unknown')
        for criterion in spec['criteria']:
            value=row['checks'][criterion['id']]
            checks.append({'arm':arm,**criterion,**value})
            # A failed baseline is useful comparison evidence, not a failed candidate.
            if value['result']=='pending' or arm=='candidate' and value['result']=='fail':
                blockers.append(arm+': '+criterion['id']+' '+value['result'])
        if row['elapsed_seconds'] is None:blockers.append(arm+': elapsed time unknown')
        if row['cost']['amount'] is None:blockers.append(arm+': actual cost unknown')
        if row['cost']['currency']!=spec['limits']['currency']:blockers.append(arm+': incomparable cost currency/unit')
    for metric,limit in [('cost','max_cost'),('elapsed_seconds','max_seconds')]:
        if metric=='cost' and any(v['cost']['currency']!=spec['limits']['currency'] for v in arms.values()):
            continue  # Never add incomparable currencies/credit units.
        values=[v['cost']['amount'] if metric=='cost' else v[metric] for v in arms.values()]
        if spec['limits'][limit] is not None and all(v is not None for v in values):
            if sum(values)>spec['limits'][limit]:blockers.append('Reported total '+metric+' exceeds declared limit')
    return checks,blockers


def markdown(report):
    def cell(value):return str(value).replace('|','\\|').replace('\n',' ')
    rows=['# Experiment comparison: '+report['id'],'',report['capability'],'',
          'Supplied observations; CLI did not assess media quality or run either method.','',
          '| Arm | Criterion | Kind | Result | Note |','| --- | --- | --- | --- | --- |']
    for c in report['checks']:rows.append('| '+' | '.join(cell(c[k]) for k in ['arm','description','kind','result','note'])+' |')
    rows+=['','## Time and cost','']
    for arm,r in report['arms'].items():rows.append(f"- {arm}: {r['elapsed_seconds']} seconds; {r['cost']['amount']} {r['cost']['currency']}")
    rows+=['','## Remaining checks','']+[('- '+s) for s in report['blockers'] or ['Owner review required; no automatic catalogue promotion']]
    rows+=['','No production approval, spending or publication authority.','']
    return '\n'.join(rows)


def review_html(report,media):
    esc=lambda x:html.escape(str(x),quote=True)
    parts=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width">',
           '<title>Local experiment comparison</title><body><h1>'+esc(report['id'])+'</h1>',
           '<p>'+esc(report['capability'])+'</p><p>Supplied observations. No automatic quality verdict.</p>']
    for arm,name in media.items():
        suffix=Path(name).suffix.lower();url=esc(name)
        tag='video' if suffix in {'.mp4','.mov','.webm'} else 'audio' if suffix in {'.wav','.mp3','.m4a','.ogg'} else 'img' if suffix in {'.png','.jpg','.jpeg','.webp'} else None
        parts.append('<h2>'+esc(arm)+'</h2>')
        if tag=='img':parts.append('<img alt="'+esc(arm)+'" src="'+url+'" style="max-width:100%">')
        elif tag:parts.append('<'+tag+' controls preload="metadata" src="'+url+'" style="max-width:100%"></'+tag+'>')
        parts.append('<p><a href="'+url+'" download>Retained '+esc(arm)+' file</a></p>')
    parts+=['<pre style="white-space:pre-wrap">'+esc(markdown(report))+'</pre>','</body></html>']
    return '\n'.join(parts)


def compare(data,project,card_subject,result_subject,folder,actor,provenance):
    text(actor,'actor')
    if provenance not in J['PROVENANCE']:raise ValueError('Explicit provenance required')
    card=checked(data,project,card_subject,'framewright-trial-v1');spec=card['spec'];validate_spec(spec)
    result_pin,result_path=current(data,project,result_subject);result=read_json(result_path)
    keys(result,['id','baseline','candidate']);attempt=identity(result['id']);rid=spec['id']
    key='trial-result:'+rid+':'+attempt
    if key in data['artifacts']:raise ValueError('Attempt ID exists; preserve history with a new attempt ID')
    if folder.exists() or folder.is_symlink() or not folder.parent.is_dir():raise ValueError('Use a new comparison folder with an existing parent')
    pins={card_subject:current(data,project,card_subject)[0],result_subject:result_pin,**card['pins']}
    arms={arm:result[arm] for arm in ['baseline','candidate']}
    for arm,row in arms.items():
        keys(row,['output','sources','environment','elapsed_seconds','cost','checks'])
        if row['sources']!=spec['sources']:raise ValueError('Both arms must attest to the same pinned sources')
        if row['elapsed_seconds'] is not None:number(row['elapsed_seconds'],'elapsed seconds')
        keys(row['cost'],['amount','currency']);text(row['cost']['currency'],'currency/unit')
        if row['cost']['amount'] is not None:number(row['cost']['amount'],'actual cost')
        if not isinstance(row['checks'],dict) or set(row['checks'])!={c['id'] for c in spec['criteria']}:
            raise ValueError('Report every criterion exactly once for both arms')
        subjects=[row['output']]
        if row['environment'] is not None:subjects.append(row['environment'])
        for check in row['checks'].values():
            keys(check,['result','note','evidence']);text(check['note'],'check note')
            if check['result'] not in {'pass','fail','pending'}:raise ValueError('Invalid check result')
            ev=check['evidence']
            if not isinstance(ev,list) or any(not isinstance(s,str) for s in ev) or len(set(ev))!=len(ev):raise ValueError('Evidence needs distinct retained subjects')
            if check['result']!='pending' and not ev:raise ValueError('Pass/fail observations need retained evidence')
            subjects+=ev
        for s in dict.fromkeys(subjects):pins[s]=current(data,project,s)[0]
    checks,blockers=evaluate(spec,arms,data,project)
    report={'schema':'framewright-trial-comparison-v1','project':str(project),'id':rid+'/'+attempt,
            'subject':'output:'+key,'trial_subject':card_subject,'tool':spec['tool'],
            'capability':spec['capability'],'arms':arms,'checks':checks,'blockers':blockers,
            'pins':pins,'qualification':'not_promoted','execution_authorized':False,
            'attestation':'Supplied observations, not independently verified by CLI','files':{}}
    folder.mkdir()
    try:
        media={}
        for arm,row in arms.items():
            source_pin,source=current(data,project,row['output']);suffix=source.suffix.lower()
            if suffix not in {'.mp4','.mov','.webm','.wav','.mp3','.m4a','.ogg','.png','.jpg','.jpeg','.webp','.txt'}:suffix='.bin'
            name=arm+suffix;target=folder/name;shutil.copyfile(source,target)
            actual=P['file_record'](target,project.parent)
            if actual['sha256']!=source_pin['sha256'] or actual['bytes']!=source_pin['bytes']:raise ValueError('Media changed during copying')
            subject=register(data,project,'trial-media:'+rid+':'+attempt+':'+arm,target,data['artifacts'].get(row['output'].removeprefix('output:'),{}).get('kind','trial-media'))
            pins[subject]=J['pin'](data,subject);media[arm]=name
        md=folder/'comparison.md';md.write_text(markdown(report))
        page=folder/'review.html';page.write_text(review_html(report,media))
        for label,path in [('notes',md),('review',page)]:
            subject=register(data,project,'trial-'+label+':'+rid+':'+attempt,path,'text')
            pins[subject]=J['pin'](data,subject)
        problems=changed(data,project,pins)
        if problems:raise ValueError('Files changed during comparison: '+'; '.join(problems))
        output=folder/'comparison.json';report['files']=media;write(output,report)
        subject=register(data,project,key,output,'trial-comparison')
        J['append'](data,card_subject,'decision','proposed',actor,provenance,
                    'A/B comparison '+attempt+'; supplied checks, no automatic qualification',
                    'trial:'+rid,[subject,*pins])
        P['event'](data,'trial_compare',identity=rid,attempt=attempt)
        return report
    except Exception:
        shutil.rmtree(folder)
        raise


def status(data,project,subject):
    _,path=current(data,project,subject);card=read_json(path)
    if card.get('schema')!='framewright-trial-v1' or card.get('project')!=str(project):raise ValueError('Expected trial card for this project')
    spec=card['spec'];validate_spec(spec)
    view={'trial':spec['id'],'tool':spec['tool'],'capability':spec['capability'],
          'state':'planned','blockers':[],'eligible_for_manual_scoped_update':False,
          'qualification':'not_promoted','execution_authorized':False}
    problems=changed(data,project,card['pins'])
    rows=[r for r in data['journal'] if r['subject']==subject and r['topic']=='trial:'+spec['id']]
    if not rows:view['blockers']=['No comparison recorded']
    else:
        row=rows[-1];problems+=changed(data,project,row['pins'])
        if not problems:
            reports=[s for s in row['pins'] if s.startswith('output:trial-result:')]
            if len(reports)!=1:raise ValueError('Invalid comparison receipt')
            report_subject=reports[0];report=checked(data,project,report_subject,'framewright-trial-comparison-v1')
            if report['trial_subject']!=subject:raise ValueError('Comparison belongs to another trial')
            _,blockers=evaluate(spec,report['arms'],data,project)
            view.update(state='needs_review' if blockers else 'ready_for_owner_review',comparison=report_subject,blockers=blockers)
            reviews=[r for r in data['journal'] if r['subject']==report_subject and r['kind']=='creative' and r['topic']=='trial-review']
            review=reviews[-1] if reviews else None
            accepted=(review and review['result']=='accepted' and review['provenance']=='owner_report'
                      and not changed(data,project,review['pins']))
            if not accepted:view['blockers'].append('Current owner-reported trial-review acceptance required')
            if not blockers and accepted:
                view.update(state='scoped_evidence_ready',eligible_for_manual_scoped_update=True)
                view['proposed_scope']={'tool':spec['tool'],'capability':spec['capability'],
                                        'evidence':report_subject,'note':'Manual catalogue review only; no broader features or provider enabled'}
    if problems:view.update(state='stale',blockers=problems)
    return view


def main():
    p=argparse.ArgumentParser(description=__doc__);cmd=p.add_subparsers(dest='command',required=True)
    a=cmd.add_parser('plan');a.add_argument('project',type=Path);a.add_argument('spec',type=Path);a.add_argument('--output',type=Path,required=True);a.add_argument('--actor',required=True)
    a=cmd.add_parser('compare');a.add_argument('project',type=Path);a.add_argument('trial');a.add_argument('results');a.add_argument('--output',type=Path,required=True);a.add_argument('--actor',required=True);a.add_argument('--provenance',choices=sorted(J['PROVENANCE']),required=True)
    a=cmd.add_parser('status');a.add_argument('project',type=Path);a.add_argument('trial');a.add_argument('--json',action='store_true')
    args=p.parse_args()
    try:
        project=args.project.resolve()
        with P['locked'](project):
            data=copy.deepcopy(P['load'](project))
            if data['schema_version']!=2:raise ValueError('Explicit migration required')
            if args.command=='status':
                view=status(data,project,args.trial)
                print(json.dumps(view,indent=2,allow_nan=False) if args.json else '\n'.join([
                    '# Trial: '+view['trial'],view['state'],view['capability'],
                    *['- '+s for s in view['blockers']],'No automatic catalogue update or execution authority.']))
                return
            if args.command=='plan':
                output=plan(data,project,read_json(args.spec),args.output,args.actor)
            else:output=compare(data,project,args.trial,args.results,args.output,args.actor,args.provenance)
            P['save'](project,data)
            print(json.dumps({'subject':output['subject'],'qualification':output['qualification'],'execution_authorized':False},indent=2))
    except (OSError,ValueError,KeyError,TypeError) as exc:p.error(str(exc))


if __name__=='__main__':main()
