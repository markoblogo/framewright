#!/usr/bin/env python3
"""Freeze accepted-film design contracts and prepare typed, independently reviewed variants."""
import argparse
import copy
import json
import math
from pathlib import Path
import runpy
import sys
import subprocess
import tempfile

BASE=Path(__file__).resolve().parent
R=runpy.run_path(str(BASE/'revisions.py'));P=R['P'];E=R['E'];J=R['J']


def finite(value,label):
    if type(value) not in (int,float) or not math.isfinite(value):raise ValueError(label+' must be finite')
    return value


def validate_design(spec):
    if not isinstance(spec,dict) or set(spec)!={'id','renderer','canvas','style','fields','scenes'}:
        raise ValueError('Design needs id, renderer, canvas, style, fields and scenes')
    R['identity'](spec['id']);E['text'](spec['renderer'],'renderer description')
    canvas=spec['canvas']
    if not isinstance(canvas,dict) or set(canvas)!={'width','height','fps'}:raise ValueError('Explicit canvas required')
    for k in ['width','height']:
        if type(canvas[k]) is not int or not 16<=canvas[k]<=8192:raise ValueError('Invalid canvas size')
    if not 1<=finite(canvas['fps'],'fps')<=120:raise ValueError('Invalid fps')
    if not isinstance(spec['style'],dict) or not spec['style']:raise ValueError('Freeze nonempty fixed style')
    fields=spec['fields']
    if not isinstance(fields,dict) or not fields:raise ValueError('Declare content fields')
    for name,f in fields.items():
        R['identity'](name)
        if not isinstance(f,dict) or type(f.get('required')) is not bool:raise ValueError('Explicit field required flag needed')
        kind=f.get('type');allowed={'type','required'}
        if kind=='text':
            allowed|={'max_chars','long_after','example'}
            if type(f.get('max_chars')) is not int or not 2<=f['max_chars']<=10000:raise ValueError('Text needs max_chars in 2–10000')
            if type(f.get('long_after')) is not int or not 1<=f['long_after']<f['max_chars']:raise ValueError('Text needs a valid long_after threshold')
            E['text'](f.get('example'),'text example')
            if len(f['example'])>f['max_chars']:raise ValueError('Text example exceeds maximum')
        elif kind=='number':
            allowed|={'minimum','maximum','example'}
            if finite(f.get('minimum'),'minimum')>finite(f.get('maximum'),'maximum'):raise ValueError('Reversed numeric bounds')
            if not f['minimum']<=finite(f.get('example'),'number example')<=f['maximum']:raise ValueError('Number example out of bounds')
        elif kind=='media':
            allowed|={'kind','fallback'}
            if f.get('kind') not in {'image','video','audio'}:raise ValueError('Media kind must be image, video or audio')
            if not f['required'] and f.get('fallback') not in {'omit','silence'}:raise ValueError('Optional media requires omit/silence fallback')
            if f.get('fallback')=='silence' and f['kind']!='audio':raise ValueError('Only audio supports silence fallback')
        else:raise ValueError('Unknown content field type')
        if set(f)-allowed:raise ValueError('Unsupported field properties; content cannot override fixed design')
    if not isinstance(spec['scenes'],list) or not spec['scenes']:raise ValueError('Declare scenes')
    ids=set()
    for scene in spec['scenes']:
        if not isinstance(scene,dict) or set(scene)!={'id','duration_seconds','bindings','layout','long_text_layout','missing_media_layout'}:raise ValueError('Scene needs identity, duration, bindings and explicit layout alternatives')
        sid=R['identity'](scene['id'])
        if sid in ids:raise ValueError('Duplicate scene id')
        ids.add(sid);E['number'](scene['duration_seconds'],'scene duration',True)
        for k in ['layout','long_text_layout','missing_media_layout']:E['text'](scene[k],k)
        if not isinstance(scene['bindings'],dict) or not scene['bindings']:raise ValueError('Scene needs field bindings')
        for target,field in scene['bindings'].items():
            R['identity'](target)
            if not isinstance(field,str) or field not in fields:raise ValueError('Unknown content field binding')
    # Reject non-JSON/NaN fixed-style data before any output file is opened.
    E['digest'](spec)


def extract(data,project,subject,spec,output):
    R['check_project'](data);validate_design(spec)
    pin,path=R['media'](data,project,subject)
    if not E['probe'](path)['video']:raise ValueError('Template seed must contain video')
    current=J['project'](data,P['file_problems'](data,project.parent))['effective']
    creative=[r for r in current if r['subject']==subject and r['kind']=='creative']
    if not creative or any(r['result']!='accepted' for r in creative):raise ValueError('A current accepted creative receipt is required for this exact source')
    key='template:'+spec['id']
    if key in data['artifacts']:raise ValueError('Template ID exists; freeze a new version')
    value={'schema':'framewright-template-v1','id':spec['id'],'baseline':{'subject':subject,'pin':pin,
           'acceptance_receipt':creative[-1]['id'],'project_at_extraction':str(project.resolve())},
           'design':spec,'design_review':'pending','variant_approvals_inherited':False,'publication_authorized':False}
    value['template_sha256']=E['digest'](value)
    E['write'](output,value);ref=R['register'](data,project,key,output,'production-template')
    row=J['append'](data,ref,'decision','proposed','framewright','administrative_change',
                    'Design contract frozen from accepted media; template design, renderer adaptation and new variants need separate review',
                    'template:'+spec['id'],[subject])
    P['event'](data,'template_extract',entry=row['id'],identity=spec['id'])
    return value


def checked_template(path):
    t=E['load'](path)
    if t.get('schema')!='framewright-template-v1' or t.get('template_sha256')!=E['digest']({k:v for k,v in t.items() if k!='template_sha256'}):
        raise ValueError('Template changed; freeze a new revision from its design source')
    validate_design(t['design']);return t


def instantiate(t,values,base):
    design=t['design'];fields=design['fields']
    if not isinstance(values,dict) or set(values)-set(fields):raise ValueError('Values may contain only declared content fields')
    content={};blockers=[]
    for name,f in fields.items():
        v=values.get(name)
        if v is None:
            if f['required']:raise ValueError('Missing required field: '+name)
            content[name]=None;continue
        if f['type']=='text':
            E['text'](v,name)
            if len(v)>f['max_chars']:raise ValueError('Text exceeds declared maximum: '+name)
            content[name]=v
        elif f['type']=='number':
            if not f['minimum']<=finite(v,name)<=f['maximum']:raise ValueError('Number out of bounds: '+name)
            content[name]=v
        else:
            if not isinstance(v,dict) or set(v)!={'path','origin','rights_status','rights_evidence'}:raise ValueError('Media needs path, origin, rights_status and rights_evidence')
            name_path=E['text'](v['path'],'media path')
            if '://' in name_path:raise ValueError('Only explicitly selected local media; no fetching')
            path=(base/name_path).resolve();E['text'](v['origin'],'origin')
            if v['rights_status'] not in {'unknown','granted','denied','noncommercial_only'}:raise ValueError('Unknown rights status')
            if v['rights_status']=='denied':raise ValueError('Denied media cannot be instantiated')
            if v['rights_status'] in {'granted','noncommercial_only'}:E['text'](v['rights_evidence'],'rights evidence')
            if f['kind']=='image':
                streams=json.loads(E['run'](['ffprobe','-v','error','-protocol_whitelist','file,pipe','-show_streams','-of','json',str(path)]))['streams']
                eligible=path.suffix.lower() in {'.png','.jpg','.jpeg','.webp','.avif'} and any(x.get('codec_type')=='video' and x.get('width',0)>0 for x in streams)
            else:
                meta=E['probe'](path)
                eligible=bool(meta['audio']) if f['kind']=='audio' else bool(meta['video'])
            if not eligible:raise ValueError('Wrong media kind: '+name)
            content[name]={**v,'path':str(path),'sha256':E['file_hash'](path),'kind':f['kind'],
                           'rights_assessment':'supplied declaration, not independently verified'}
            if v['rights_status']!='granted':blockers.append(name+': resolve rights for the new intended use')
    scenes=[]
    for scene in design['scenes']:
        bound={target:copy.deepcopy(content[field]) for target,field in scene['bindings'].items()}
        long=any(fields[field]['type']=='text' and content[field] is not None and len(content[field])>fields[field]['long_after'] for field in scene['bindings'].values())
        missing=any(fields[field]['type']=='media' and content[field] is None for field in scene['bindings'].values())
        scenes.append({'id':scene['id'],'duration_seconds':scene['duration_seconds'],'content':bound,
                       'layout':{'base':scene['layout'],'text':scene['long_text_layout'] if long else scene['layout'],
                                 'media':scene['missing_media_layout'] if missing else scene['layout']},
                       'fallbacks':{field:fields[field].get('fallback','omit') for field in scene['bindings'].values() if content[field] is None}})
    return {'schema':'framewright-template-variant-v1','template_sha256':t['template_sha256'],
            'canvas':copy.deepcopy(design['canvas']),'style':copy.deepcopy(design['style']),
            'renderer':design['renderer'],'values':content,'scenes':scenes,'publication_blockers':blockers,
            'render':'not_performed','layout_review':'pending','creative_review':'pending',
            'timing_review':'pending; remeasure new narration','publication_authorized':False}


def stress(t,values,base,output):
    if output.exists():raise ValueError('Stress directory exists; choose a new revision')
    defaults={n:f.get('example') for n,f in t['design']['fields'].items()}
    defaults.update(values or {});cases={}
    for case in ['short-text','long-text','missing-optional-media']:
        v=copy.deepcopy(defaults)
        for name,f in t['design']['fields'].items():
            if f['type']=='text':
                v[name]=('Short title'[:f['long_after']] if case=='short-text' else ('Long international headline with numbers and details. '*300)[:f['max_chars']] if case=='long-text' else f['example'])
            elif f['type']=='media' and not f['required'] and case=='missing-optional-media':v[name]=None
        cases[case]=instantiate(t,v,base)
    with tempfile.TemporaryDirectory(prefix='.template-',dir=output.resolve().parent) as tmp:
        stage=Path(tmp)/'pack';stage.mkdir()
        for name,v in cases.items():E['write'](stage/(name+'.json'),v)
        report={'schema':'framewright-template-check-v1','template_sha256':t['template_sha256'],
                'cases':{n:{'data_validation':'pass','render':'not_performed','layout_review':'pending','file':n+'.json','sha256':E['file_hash'](stage/(n+'.json'))} for n in cases},
                'publication_authorized':False,'scope':'Input validation and layout selection; no renderer/visual-quality qualification'}
        E['write'](stage/'report.json',report)
        if output.exists():raise ValueError('Output appeared during preparation')
        stage.rename(output)
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('extract');p.add_argument('project',type=Path);p.add_argument('subject');p.add_argument('design',type=Path);p.add_argument('--output',type=Path,required=True)
    p=sub.add_parser('instantiate');p.add_argument('template',type=Path);p.add_argument('values',type=Path);p.add_argument('--output',type=Path,required=True)
    p=sub.add_parser('check');p.add_argument('template',type=Path);p.add_argument('--values',type=Path);p.add_argument('--output',type=Path,required=True)
    a=parser.parse_args()
    if a.command=='extract':
        project=a.project.resolve()
        with P['locked'](project):
            data=P['load'](project);extract(data,project,a.subject,E['load'](a.design),a.output);P['save'](project,data)
    elif a.command=='instantiate':E['write'](a.output,instantiate(checked_template(a.template),E['load'](a.values),a.values.resolve().parent))
    else:stress(checked_template(a.template),E['load'](a.values) if a.values else None,a.values.resolve().parent if a.values else a.template.resolve().parent,a.output)
    print(json.dumps({'command':a.command,'publication_authorized':False}))


if __name__=='__main__':
    try:main()
    except (ValueError,OSError,KeyError,TypeError,AttributeError,subprocess.SubprocessError) as exc:
        print('Error: '+str(exc),file=sys.stderr);sys.exit(1)
