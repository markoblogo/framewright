#!/usr/bin/env python3
"""Inspect a bounded returned OTIO cut; stage new review gates, never inherit approval."""
import argparse
import json
from pathlib import Path
import runpy
import sys
from urllib.parse import unquote, urlsplit

BASE=Path(__file__).resolve().parent
O=runpy.run_path(str(BASE/'otio_export.py'))
R=runpy.run_path(str(BASE/'revisions.py'))
P=R['P'];E=R['E'];J=R['J']


def pin(path):
    path=Path(path).resolve(strict=True);row=P['file_record'](path,path.parent)
    return {'path':str(path),'bytes':row['bytes'],'sha256':row['sha256']}


def recheck(pins):
    for old in pins:
        if pin(old['path'])!=old:raise ValueError('Dependency changed: '+old['path'])


def frame(value,rate):
    if value is None or value.rate!=rate:raise ValueError('Only explicit common-rate frame ranges supported')
    n=value.rescaled_to(rate).value
    if not isinstance(n,(int,float)) or not 0<=n<=100000000 or int(n)!=n:raise ValueError('Invalid or fractional frame range')
    return int(n)


def metadata_fingerprint(t,o):
    # Digest opaque metadata without executing/interpreting it or copying journal notes.
    raw=json.loads(o.adapters.write_to_string(t,adapter_name='otio_json'));values=[]
    def walk(v,path=''):
        if isinstance(v,dict):
            if v.get('metadata'):values.append({'path':path,'metadata':v['metadata']})
            for k,x in v.items():
                if k!='metadata':walk(x,path+'/'+k)
        elif isinstance(v,list):
            for n,x in enumerate(v):walk(x,path+'/'+str(n))
    walk(raw)
    return P['digest'](values)


def canonical(path,checked,o,pins):
    if path.stat().st_size>20*1024*1024:raise ValueError('OTIO exceeds bounded20MiB profile')
    t=o.adapters.read_from_file(str(path),adapter_name='otio_json');rate=checked['spec']['rate']
    if not isinstance(t,o.schema.Timeline):raise ValueError('Expected one Timeline')
    if t.global_start_time is not None and frame(t.global_start_time,rate)!=0:raise ValueError('Nonzero global timecode unsupported')
    if t.tracks.source_range is not None:raise ValueError('Stack source ranges unsupported; flatten explicitly first')
    if t.tracks.effects:raise ValueError('Stack effects unsupported; bake explicitly first')
    if not t.tracks.enabled:raise ValueError('Disabled stack unsupported')
    expected={x['id']:x['kind'] for x in checked['spec']['tracks']}
    if list(expected.values()).count('video')>1:raise ValueError('Return profile supports at most one picture track')
    if len(t.tracks)!=len(expected):raise ValueError('Changed track set; explicit remapping required')
    known={m['sha256']:m for m in checked['media'].values()}
    if len(known)!=len(checked['media']):raise ValueError('Ambiguous retained media hashes')
    roots=[Path(checked['spec_path']).parent,path.parent.resolve()];rows={};refs={}
    for tr in t.tracks:
        kind='video' if tr.kind==o.schema.TrackKind.Video else 'audio' if tr.kind==o.schema.TrackKind.Audio else None
        if tr.name not in expected or expected[tr.name]!=kind or tr.name in rows:raise ValueError('Track names/kinds require explicit unambiguous mapping')
        if tr.source_range is not None:raise ValueError('Track source ranges unsupported; flatten explicitly first')
        if tr.effects or len(tr)>10000:raise ValueError('Track effects/oversized edit unsupported')
        items=[];cursor=0
        for item in tr:
            if item.effects:raise ValueError('Effects/retiming unsupported; bake explicitly first')
            if not isinstance(item,(o.schema.Clip,o.schema.Gap)):raise ValueError('Nested cuts/transitions unsupported')
            span=item.source_range
            if span is None:raise ValueError('Explicit source ranges required')
            duration=frame(span.duration,rate)
            if duration<1:raise ValueError('Empty item unsupported')
            if isinstance(item,o.schema.Clip):
                if len(item.media_references())!=1 or not isinstance(item.media_reference,o.schema.ExternalReference):raise ValueError('One external media reference required')
                url=urlsplit(item.media_reference.target_url)
                if url.scheme not in {'','file'} or (url.netloc and not (url.scheme=='file' and url.netloc=='localhost')):raise ValueError('Remote media references forbidden')
                name=unquote(url.path)
                if not name or '\\' in name:raise ValueError('Unsupported local media path')
                f=Path(name);f=(f if f.is_absolute() else path.parent/f).resolve(strict=True)
                if not any(f.is_relative_to(root) for root in roots):raise ValueError('Media outside explicit source/return folders')
                record=pin(f);m=known.get(record['sha256'])
                if m is None:raise ValueError('Unknown or changed source media;basename/metadata is not identity')
                pins[str(f)]=record;refs[str(f)]=m['id'];start=frame(span.start_time,rate)
                stream=m['probe'][kind]
                if start+duration>O['checked_stream_frames'](stream,kind,rate):raise ValueError('Returned range exceeds retained source')
                items.append({'material':m['id'],'sha256':m['sha256'],'at':cursor,'in':start,'duration':duration,'enabled':bool(tr.enabled and item.enabled)})
            cursor+=duration
        rows[tr.name]={'kind':kind,'items':items,'extent':cursor,'enabled':bool(tr.enabled)}
    total=frame(t.duration(),rate)
    if not total:raise ValueError('Empty timeline unsupported')
    return {'frames':total,'rate':rate,'tracks':rows},refs,metadata_fingerprint(t,o)


def intervals(before,after):
    """Compare piecewise source-to-timeline mappings, with implicit trailing silence."""
    out=[];end=max(before['frames'],after['frames'])
    def at(items,n,limit):
        if n>=limit:return None
        for r in items:
            if r['enabled'] and r['at']<=n<r['at']+r['duration']:return (r['sha256'],r['in']+n-r['at'])
        return None
    for name,b in before['tracks'].items():
        a=after['tracks'][name];cuts={0,end,before['frames'],after['frames']}
        for track in [b,a]:
            for r in track['items']:cuts.update([r['at'],r['at']+r['duration']])
        cuts=sorted(cuts);spans=[]
        for x,y in zip(cuts,cuts[1:]):
            if x==y or at(b['items'],x,before['frames'])==at(a['items'],x,after['frames']):continue
            if spans and spans[-1]['end']==x:spans[-1]['end']=y
            else:spans.append({'start':x,'end':y})
        if spans:out.append({'track':name,'kind':b['kind'],'ranges':spans})
    return out


def inspect(spec,baseline,after):
    spec=spec.resolve(strict=True);baseline=baseline.resolve(strict=True);after=after.resolve(strict=True)
    if baseline==after:raise ValueError('Preserve the baseline under a distinct path')
    pins={str(p):pin(p) for p in [spec,baseline,after]};checked=O['inspect_spec'](spec);o=O['library']()
    # Baseline must actually represent the supplied retained export specification.
    native=o.adapters.read_from_file(str(baseline),adapter_name='otio_json')
    if O['signature'](native,checked['spec']['rate'])!=O['signature'](O['make_timeline'](checked),checked['spec']['rate']):raise ValueError('Baseline does not match retained specification')
    b,_,bm=canonical(baseline,checked,o,pins)
    if any(not tr['enabled'] or any(not c['enabled'] for c in tr['items']) for tr in b['tracks'].values()):raise ValueError('Baseline enabled state differs from retained specification')
    a,refs,am=canonical(after,checked,o,pins);changed=intervals(b,a)
    recheck(pins.values())
    return {'schema':'framewright-otio-return-v1','inputs':{'spec':pins[str(spec)],'baseline':pins[str(baseline)],'after':pins[str(after)]},'file_pins':sorted(pins.values(),key=lambda x:x['path']),
            'before':b,'after':a,'returned_media':refs,'delta':{'duration_frames':a['frames']-b['frames'],'timeline_changed':bool(changed or a['frames']!=b['frames']),'changed_ranges':changed},
            'metadata':{'different':bm!=am,'scope':'Opaque metadata is not approval or interpreted effect/conformance evidence'},
            'review_requirements':['technical','listening','creative'],'review_scope':'New candidate needs rendered conformance,full listening and creative review;range checks do not approve picture/sound',
            'approval_inherited':False,'publication_authorized':False}


def stage(project,report_path,rid,subjects,render_subject,output):
    rid=R['identity'](rid);project=project.resolve(strict=True);output=output.resolve()
    if output.exists():raise ValueError('Use a new packet path')
    report_pin=pin(report_path);report=E['load'](report_path)
    if report.get('schema')!='framewright-otio-return-v1':raise ValueError('Unsupported return report')
    prefix='otio-return:'+rid
    with P['locked'](project):
        data=P['load'](project);R['check_project'](data)
        if any(k==prefix or k.startswith(prefix+':') for k in [*data['artifacts'],*(x['id'] for x in data['steps'])]):raise ValueError('Return ID already exists')
        source_pins={};paths={}
        if len(set(subjects.values()))!=3:raise ValueError('Use distinct specification/baseline/returned subjects')
        for role,subject in subjects.items():
            old,path=R['media'](data,project,subject)
            if pin(path)!=report['inputs'][role]:raise ValueError('Report does not match retained project subjects')
            source_pins[subject]=old;paths[role]=path
        rp,render=R['media'](data,project,render_subject)
        if render_subject in source_pins:raise ValueError('Render must be a distinct retained subject')
        # Recompute: report fields cannot remove checks or forge a benign delta.
        fresh=inspect(paths['spec'],paths['baseline'],paths['after'])
        if fresh!=report:raise ValueError('Report changed or no longer matches current source revisions')
        if pin(report_path)!=report_pin:raise ValueError('Report changed during intake')
        meta=E['probe'](render);checked=O['inspect_spec'](paths['spec']);rate=report['after']['rate'];total=report['after']['frames']
        picture_tracks=[t for t in report['after']['tracks'].values() if t['kind']=='video']
        pictures=[checked['media'][c['material']] for t in picture_tracks for c in t['items']]
        if picture_tracks and not pictures:raise ValueError('Picture tracks need a retained picture-format reference')
        stream=meta['video'] if picture_tracks else meta['audio']
        if O['checked_stream_frames'](stream,'video' if picture_tracks else 'audio',rate)!=total:raise ValueError('Rendered candidate extent does not match returned cut')
        if picture_tracks:
            v=meta['video'];base=pictures[0]['probe']['video']
            if (v['width'],v['height'])!=(base['width'],base['height']) or O['Fraction'](v['avg_frame_rate'])!=rate or O['Fraction'](v['r_frame_rate'])!=rate:raise ValueError('Rendered candidate format does not match bounded profile')
        if any(t['kind']=='audio' for t in report['after']['tracks'].values()) and not meta['audio']:raise ValueError('Returned audio tracks require a rendered audio stream')
        if R['media'](data,project,render_subject)[0]!=rp:raise ValueError('Rendered candidate changed during intake')
        recheck(report['file_pins'])
        # New aliases isolate this returned candidate from approvals of all prior outputs.
        registered=[]
        for suffix,file,kind in [('comparison',report_path,'editor-return-comparison'),('timeline',paths['after'],'editor-return-timeline'),('render',render,'editor-return-candidate')]:
            registered.append(R['register'](data,project,prefix+':'+suffix,file,kind))
        input_paths={str(p.resolve()) for p in paths.values()}
        for n,row in enumerate(report['file_pins']):
            if row['path'] not in input_paths:
                registered.append(R['register'](data,project,prefix+':media:'+str(n),Path(row['path']),'editor-return-media'))
        candidate='output:'+prefix+':render'
        packet={'schema':'framewright-otio-return-packet-v1','project':str(project),'id':rid,'comparison':registered[0],'timeline':registered[1],'candidate':candidate,
                'source_subjects':subjects,'render_supplied_as':render_subject,'source_pins':{**source_pins,render_subject:rp},'comparison_pin':report_pin,
                'delta':report['delta'],'review_requirements':report['review_requirements'],'render_binding':'Operator-supplied file;format/extent checked,not picture/audio conformance',
                'approval_inherited':False,'publication_authorized':False}
        E['write'](output,packet);packet_subject=R['register'](data,project,prefix,output,'editor-return-packet')
        dependencies=[*source_pins,render_subject,*registered,packet_subject]
        received=prefix+':received'
        data['steps'].append({'id':received,'label':'Retain external-editor candidate and comparison','depends_on':[],'required_outputs':[prefix,prefix+':timeline',prefix+':render'],
                              'unmet':[],'state':'done','evidence':'Explicit staging only;no review/acceptance inherited','waiting_for':None,'check_kind':None,'optional':False,'attestation':'operator_recorded_not_independently_verified'})
        for kind in report['review_requirements']:
            J['append'](data,candidate,kind,'pending','otio-return','administrative_change',
                        'Returned edit needs its own '+kind+' review. Prior output approvals remain scoped to prior revisions.',dependencies=dependencies)
            data['steps'].append({'id':prefix+':review-'+kind,'label':'Review returned edit: '+kind,'depends_on':[received],'required_outputs':[prefix+':render'],
                                  'unmet':[],'state':'blocked','evidence':'New returned render; explicit review required,not inherited from the baseline',
                                  'waiting_for':'operator' if kind=='technical' else 'owner','check_kind':kind,'optional':False,'attestation':'operator_recorded_not_independently_verified'})
        J['append'](data,packet_subject,'decision','proposed','otio-return','administrative_change','External edit staged as a separate candidate;select/review it explicitly.','editor-return:'+rid,dependencies)
        P['event'](data,'otio_return_staged',identity=rid,subject=candidate)
        recheck(report['file_pins']);recheck([report_pin]);R['media'](data,project,render_subject)
        P['save'](project,data)
    return packet


def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    q=sub.add_parser('inspect');q.add_argument('spec',type=Path);q.add_argument('--baseline',type=Path,required=True);q.add_argument('--after',type=Path,required=True);q.add_argument('--output',type=Path,required=True)
    q=sub.add_parser('stage');q.add_argument('project',type=Path);q.add_argument('report',type=Path);q.add_argument('--id',required=True)
    q.add_argument('--spec-subject',required=True);q.add_argument('--baseline-subject',required=True);q.add_argument('--after-subject',required=True);q.add_argument('--render-subject',required=True);q.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    try:
        if a.command=='inspect':
            if a.output.exists():raise ValueError('Use a new report path')
            r=inspect(a.spec,a.baseline,a.after);E['write'](a.output,r)
            result={'report':str(a.output),'delta_frames':r['delta']['duration_frames'],'timeline_changed':r['delta']['timeline_changed']}
        else:
            r=stage(a.project,a.report,a.id,{'spec':a.spec_subject,'baseline':a.baseline_subject,'after':a.after_subject},a.render_subject,a.output)
            result={'packet':str(a.output),'candidate':r['candidate'],'review_requirements':r['review_requirements']}
        print(json.dumps({**result,'approval_inherited':False,'publication_authorized':False}))
    except (OSError,ValueError,KeyError,TypeError,AttributeError,RuntimeError) as exc:p.exit(2,str(exc)+'\n')

if __name__=='__main__':main()
