#!/usr/bin/env python3
"""Revision-bound change requests and comparison packs in the existing project journal."""
import argparse
import json
import os
from pathlib import Path
import re
import runpy
import sys
import tempfile
import subprocess

BASE=Path(__file__).resolve().parent
P=runpy.run_path(str(BASE/'project.py'))
E=runpy.run_path(str(BASE/'editing.py'))
J=P['JOURNAL']


def identity(value):
    if not isinstance(value,str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,79}',value):
        raise ValueError('Use a short alphanumeric ID with dots, underscores or hyphens')
    return value


def media(data,project,subject):
    pin=J['pin'](data,subject)
    if pin is None or subject in P['file_problems'](data,project.parent):
        raise ValueError('Retained file is missing or changed: '+subject)
    return pin,(project.parent/pin['path']).resolve()


def register(data,project,key,path,kind):
    if key in data['artifacts']:
        raise ValueError('Artifact ID already exists: '+key)
    data['artifacts'][key]={'kind':kind,'scene':None,'file':None}
    P['event'](data,'declare_artifact',identity=key,kind=kind)
    P['retain'](data,project.parent,key,path,False,False)
    return 'output:'+key


def check_project(data):
    if data['schema_version']!=2:
        raise ValueError('Migrate the project explicitly before using its journal')


def checked_record(data,project,path,schema):
    record=E['load'](path)
    if record.get('schema')!=schema or Path(record['project']).resolve()!=project.resolve():
        raise ValueError('Record belongs to another schema/project')
    pin,actual=media(data,project,record['subject'])
    if actual!=path.resolve() or pin['sha256']!=E['file_hash'](path):
        raise ValueError('Record is not its retained revision')
    for subject,old in record['pins'].items():
        current,_=media(data,project,subject)
        if current!=old:
            raise ValueError('Revision dependency changed: '+subject)
    return record


def request(data,project,subject,spec,output,actor):
    check_project(data);E['text'](actor,'actor')
    if set(spec)!={'id','start','end','defect','desired','preserve'}:
        raise ValueError('Change needs id, start, end, defect, desired and preserve')
    rid=identity(spec['id']);key='revision:'+rid
    if key in data['artifacts']:
        raise ValueError('Revision ID already exists; choose a new request')
    pin,path=media(data,project,subject);duration=E['probe'](path)['duration_seconds']
    a=E['number'](spec['start'],'start');b=E['number'](spec['end'],'end',True)
    if b<=a or b>duration:raise ValueError('Requested interval exceeds baseline')
    for k in ['defect','desired']:E['text'](spec[k],k)
    preserve=spec['preserve']
    if not isinstance(preserve,list) or not preserve or any(not isinstance(s,str) or not s.strip() for s in preserve) or len(set(preserve))!=len(preserve):
        raise ValueError('preserve needs distinct nonempty requirements')
    value={'schema':'framewright-revision-request-v1','project':str(project.resolve()),
           'id':rid,'subject':'output:'+key,'baseline_subject':subject,'baseline':pin,
           'change':spec,'pins':{subject:pin},'result':'proposed','publication_authorized':False}
    E['write'](output,value)
    record_subject=register(data,project,key,output,'revision-request')
    row=J['append'](data,record_subject,'decision','proposed',actor,'operator_observation',
                    'Requested change: '+spec['defect']+'; desired: '+spec['desired'],
                    'revision:'+rid,[subject])
    P['event'](data,'revision_request',entry=row['id'],identity=rid)
    return value


def literal(value):
    import html
    return re.sub(r'([\\`*_{}\[\]()#!|])',r'\\\1',html.escape(str(value))).replace('\n',' ')


def comparison(data,project,request_path,after_subject,output,context,after_start=None,after_end=None):
    check_project(data);req=checked_record(data,project,request_path,'framewright-revision-request-v1')
    if after_subject==req['baseline_subject']:
        raise ValueError('Retain after under a distinct artifact ID; preserve the baseline')
    bp,before=media(data,project,req['baseline_subject']);ap,after=media(data,project,after_subject)
    metas=[E['probe'](p) for p in [before,after]]
    E['number'](context,'context',True)
    if not .1<=context<=5:raise ValueError('Context must be 0.1–5 seconds')
    if (after_start is None)!=(after_end is None):raise ValueError('Provide both after range bounds')
    a,b=req['change']['start'],req['change']['end']
    aa,ab=(a,b) if after_start is None else (after_start,after_end)
    E['number'](aa,'after start');E['number'](ab,'after end',True)
    if ab<=aa or ab>metas[1]['duration_seconds']:raise ValueError('After interval exceeds media')
    intervals=[(max(0,a-context),min(metas[0]['duration_seconds'],b+context)),
               (max(0,aa-context),min(metas[1]['duration_seconds'],ab+context))]
    if max(end-start for start,end in intervals)>30:raise ValueError('Select a narrower change; review excerpts are limited to 30 seconds')
    if output.exists():raise ValueError('Comparison directory exists; choose a new revision')
    rid=req['id'];n=1
    while f'revision-compare:{rid}:{n}' in data['artifacts']:n+=1
    key=f'revision-compare:{rid}:{n}';video=bool(metas[0]['video'] or metas[1]['video'])
    files={};sides={}
    with tempfile.TemporaryDirectory(prefix='.revision-',dir=output.resolve().parent) as tmp:
        stage=Path(tmp)/'pack';stage.mkdir()
        for side,path,meta,pin,bounds,target in zip(['before','after'],[before,after],metas,[bp,ap],intervals,[(a,b),(aa,ab)]):
            start,end=bounds;part=stage/(side+('.mkv' if video else '.wav'))
            source={'path':str(path),**meta}
            duration=E['review_part'](source,start,end-start,part,video)
            preview=stage/(side+('.mp4' if video else '.wav'))
            if video:
                E['ffmpeg'](['-threads','1','-i',str(part),'-c:v','libx264','-threads','1','-crf','20','-c:a','aac',
                             '-movflags','+faststart',str(preview)]);part.unlink()
                idx=max(0,min(round((target[0]-start)*24),round(duration*24)-1))
                picture=stage/(side+'.png')
                E['ffmpeg'](['-threads','1','-i',str(preview),'-vf',f'select=eq(n\\,{idx})',
                             '-fps_mode','vfr','-frames:v','1',str(picture)])
                if not picture.exists():raise ValueError('Comparison keyframe could not be decoded')
                files[picture.name]=E['file_hash'](picture)
            E['ffmpeg'](['-threads','1','-i',str(preview),'-f','null','-'])
            files[preview.name]=E['file_hash'](preview)
            sides[side]={'subject':req['baseline_subject'] if side=='before' else after_subject,'pin':pin,
                         'start':start,'end':end,'change_start':target[0],'change_end':target[1],
                         'preview_file':preview.name,'preview_duration_seconds':duration,
                         'proxy_padding_seconds':duration-(end-start),'synthetic_silence':not bool(meta['audio']),
                         'synthetic_background':video and not bool(meta['video'])}
        report={'schema':'framewright-revision-comparison-v1','project':str(project.resolve()),'id':rid,
                'subject':'output:'+key,'request_subject':req['subject'],'change':req['change'],
                'pins':{req['subject']:J['pin'](data,req['subject']),req['baseline_subject']:bp,after_subject:ap},
                **sides,'files':files,'result':'pending','decode':'pass',
                'duration_delta_seconds':metas[1]['duration_seconds']-metas[0]['duration_seconds'],
                'bytes_identical':bp['sha256']==ap['sha256'],'publication_authorized':False,
                'preservation_checks':'not_performed; manual evidence required'}
        lines=['# Revision comparison','',literal(req['change']['defect']),'',
               'Desired: '+literal(req['change']['desired']),'',
               f"[Before]({sides['before']['preview_file']}) · [After]({sides['after']['preview_file']})",'']
        if video:lines+=['![Before](before.png)','![After](after.png)','']
        lines+=['Review both excerpts with sound. Decode is technical evidence only.','',
                'Preserve: '+', '.join(literal(s) for s in req['change']['preserve']),
                '', 'Clips are normalized review proxies; see report.json for source times and padding.']
        (stage/'review.md').write_text('\n'.join(lines),encoding='utf-8')
        files['review.md']=E['file_hash'](stage/'review.md')
        for name in files:
            subject='output:'+key+':'+name
            pin=P['file_record'](stage/name,project.parent)
            pin['path']=os.path.relpath((output/name).resolve(),project.parent)
            report['pins'][subject]=pin
        E['write'](stage/'report.json',report)
        # Recheck original and request pins before binding the generated pack.
        checked_record(data,project,request_path,'framewright-revision-request-v1');media(data,project,after_subject)
        if output.exists():raise ValueError('Comparison directory appeared during rendering')
        stage.rename(output)
    for name in files:
        register(data,project,key+':'+name,output/name,'comparison-media')
    register(data,project,key,output/'report.json','revision-comparison')
    row=J['append'](data,req['subject'],'decision','proposed','framewright','administrative_change',
                    'Comparison prepared; change and preservation review pending','revision:'+rid,
                    [*report['pins'],report['subject']])
    P['event'](data,'revision_comparison',entry=row['id'],identity=rid)
    return report


def review(data,project,report_path,checks,result,actor,provenance):
    check_project(data);report=checked_record(data,project,report_path,'framewright-revision-comparison-v1')
    # Review of an older comparison must not supersede the current attempt.
    decisions=J['project'](data,P['file_problems'](data,project.parent))['effective']
    latest=[r for r in decisions if r['subject']==report['request_subject'] and r['topic']=='revision:'+report['id']]
    if not latest or report['subject'] not in latest[-1]['pins']:
        raise ValueError('This comparison is not the current attempt')
    for name,pin in report['files'].items():
        path=report_path.parent/name
        if Path(name).name!=name or E['file_hash'](path)!=pin:raise ValueError('Comparison media changed')
    if set(checks)!={'change','preserve'} or not isinstance(checks['preserve'],list):raise ValueError('Provide change and preservation checks')
    wanted=report['change']['preserve'];actual=[r.get('requirement') for r in checks['preserve']]
    if len(actual)!=len(set(actual)) or set(actual)!=set(wanted):raise ValueError('Verify every preservation requirement exactly once')
    rows=[checks['change'],*checks['preserve']]
    for row in rows:
        if row.get('result') not in {'pass','fail','unknown'}:raise ValueError('Check result must be pass, fail or unknown')
        E['text'](row.get('note'),'check note')
    if result=='accepted' and any(r['result']!='pass' for r in rows):raise ValueError('Acceptance needs a passed change and all preservation checks')
    rid=report['id'];n=1
    while f'revision-review:{rid}:{n}' in data['artifacts']:n+=1
    key=f'revision-review:{rid}:{n}';path=report_path.parent/f'verification-{n:03}.json'
    evidence={'schema':'framewright-revision-verification-v1','comparison':report['subject'],
              'actor':actor,'provenance':provenance,'result':result,'checks':checks,
              'attestation':'supplied manual review; not independently verified by CLI'}
    # Validate the journal entry on the in-memory project before creating files.
    if provenance not in J['PROVENANCE']:raise ValueError('Unsupported review provenance')
    E['text'](actor,'reviewer')
    E['write'](path,evidence);subject=register(data,project,key,path,'revision-verification')
    row=J['append'](data,report['request_subject'],'decision','proposed' if result=='pending' else result,
                    actor,provenance,'Change '+checks['change']['result']+'; preservation checks recorded. '+checks['change']['note'],
                    'revision:'+rid,[*report['pins'],report['subject'],subject])
    P['event'](data,'revision_review',entry=row['id'],identity=rid)
    return row


def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('request');p.add_argument('project',type=Path);p.add_argument('subject');p.add_argument('spec',type=Path)
    p.add_argument('--output',required=True,type=Path);p.add_argument('--actor',default='framewright')
    p=sub.add_parser('compare');p.add_argument('project',type=Path);p.add_argument('request',type=Path)
    p.add_argument('--after',required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--context',type=float,default=1);p.add_argument('--after-start',type=float);p.add_argument('--after-end',type=float)
    p=sub.add_parser('review');p.add_argument('project',type=Path);p.add_argument('report',type=Path)
    p.add_argument('--checks',type=Path,required=True);p.add_argument('--result',choices=['accepted','rejected','pending'],required=True)
    p.add_argument('--actor',required=True);p.add_argument('--provenance',choices=sorted(J['PROVENANCE']),required=True)
    args=parser.parse_args();project=args.project.resolve()
    with P['locked'](project):
        data=P['load'](project)
        if args.command=='request':request(data,project,args.subject,E['load'](args.spec),args.output,args.actor)
        elif args.command=='compare':comparison(data,project,args.request,args.after,args.output,args.context,args.after_start,args.after_end)
        else:review(data,project,args.report,E['load'](args.checks),args.result,args.actor,args.provenance)
        P['save'](project,data)
    print(json.dumps({'command':args.command,'publication_authorized':False}))


if __name__=='__main__':
    try:main()
    except (ValueError,OSError,KeyError,TypeError,AttributeError,subprocess.SubprocessError) as exc:
        print('Error: '+str(exc),file=sys.stderr);sys.exit(1)
