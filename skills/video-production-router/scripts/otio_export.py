#!/usr/bin/env python3
"""Optional straight-cut OTIO handoff using the official library. No render/install/upload."""
import argparse
from fractions import Fraction
import json
from pathlib import Path
import runpy
from urllib.parse import quote, urlsplit

E=runpy.run_path(str(Path(__file__).with_name('editing.py')))


def keys(row,allowed):
    if not isinstance(row,dict) or set(row)-set(allowed):raise ValueError('Unsupported fields; effects/retiming must be explicitly baked')


def integer(value,label):
    if type(value)!=int or value<0:raise ValueError(label+' must be a nonnegative integer')
    return value


def available_frames(stream,rate):
    if stream.get('codec_type')=='video' and str(stream.get('nb_frames','')).isdigit():
        return Fraction(int(stream['nb_frames']))
    if stream.get('duration_ts') is not None and stream.get('time_base'):
        return int(stream['duration_ts'])*Fraction(stream['time_base'])*rate
    raise ValueError('Exact stream extent unavailable; provide a timed encoded intermediate')


def inspect_spec(path):
    path=path.resolve(strict=True);pin=E['file_hash'](path);spec=E['load'](path)
    keys(spec,{'schema','name','rate','duration_frames','media','tracks','project_id','variant_id','declared_baked_features'})
    if spec.get('schema')!='framewright-otio-export-v1':raise ValueError('Unsupported export schema')
    E['text'](spec.get('name'),'timeline name');rate=integer(spec.get('rate'),'rate')
    total=integer(spec.get('duration_frames'),'duration_frames')
    if not 1<=rate<=120 or total<1:raise ValueError('Use a positive bounded integer frame rate and duration')
    if not isinstance(spec.get('media'),list) or not spec['media']:raise ValueError('Explicit media required')
    media={}
    for item in spec['media']:
        keys(item,{'id','path','sha256'});identity=E['text'](item.get('id'),'media ID')
        if identity in media:raise ValueError('Duplicate media ID')
        name=E['text'](item.get('path'),'media path');relative=Path(name)
        if relative.is_absolute() or '..' in relative.parts or urlsplit(name).scheme:raise ValueError('Use package-local relative media paths')
        file=(path.parent/relative).resolve(strict=True)
        if not file.is_relative_to(path.parent):raise ValueError('Media resolves outside package')
        if E['file_hash'](file)!=item.get('sha256'):raise ValueError('Media revision changed: '+identity)
        media[identity]={**item,'absolute_path':str(file),'probe':E['probe'](file)}
    if not isinstance(spec.get('tracks'),list) or not spec['tracks']:raise ValueError('Explicit tracks required')
    seen=set();track_ids=set()
    for track in spec['tracks']:
        keys(track,{'id','kind','items'});tid=E['text'](track.get('id'),'track ID')
        if tid in track_ids or track.get('kind') not in {'video','audio'}:raise ValueError('Unique track IDs and audio/video kinds required')
        track_ids.add(tid)
        if not isinstance(track.get('items'),list) or not track['items']:raise ValueError('Nonempty track items required')
        length=0
        for item in track['items']:
            keys(item,{'id','type','media','in_frames','duration_frames'})
            identity=E['text'](item.get('id'),'item ID')
            if identity in seen:raise ValueError('Unique item IDs required')
            seen.add(identity);duration=integer(item.get('duration_frames'),'item duration')
            if duration<1:raise ValueError('Positive item duration required')
            length+=duration
            if item.get('type')=='gap':
                if 'media' in item or 'in_frames' in item:raise ValueError('Gaps cannot bind media')
                continue
            if item.get('type')!='clip' or item.get('media') not in media:raise ValueError('Clip must bind retained media')
            start=integer(item.get('in_frames'),'source in');info=media[item['media']]['probe']
            stream=info[track['kind']]
            if not stream:raise ValueError('Source lacks requested stream kind')
            if float(stream.get('start_time',0))!=0:raise ValueError('Bake nonzero stream origins first')
            if track['kind']=='video':
                # First bounded profile: common CFR, zero-based encoded intermediates.
                if Fraction(stream.get('avg_frame_rate','0/1'))!=rate or Fraction(stream.get('r_frame_rate','0/1'))!=rate:
                    raise ValueError('Bake mismatched/VFR video to the timeline frame rate first')
            if start+duration>available_frames(stream,rate):raise ValueError('Source range exceeds retained media')
        if length!=total:raise ValueError('Every track must cover declared duration; use explicit gaps')
    baked=spec.get('declared_baked_features',[])
    if not isinstance(baked,list) or any(not isinstance(x,str) or not x.strip() for x in baked):raise ValueError('Baked features must be explicit text entries')
    if E['file_hash'](path)!=pin:raise ValueError('Specification changed during inspection')
    return {'spec':spec,'spec_path':str(path),'spec_sha256':pin,'media':media}


def library():
    try:import opentimelineio as otio
    except ImportError as exc:raise ValueError('Optional OpenTimelineIO package missing; install explicitly in a separate environment') from exc
    return otio


def make_timeline(checked):
    o=library();s=checked['spec'];rate=s['rate']
    tr=lambda start,duration:o.opentime.TimeRange(o.opentime.RationalTime(start,rate),o.opentime.RationalTime(duration,rate))
    metadata={'project_id':s.get('project_id',''),'variant_id':s.get('variant_id',''),'export_profile':'common-CFR-straight-cuts-with-explicit-gaps','spec_sha256':checked['spec_sha256'],'declared_baked_features':s.get('declared_baked_features',[])}
    tl=o.schema.Timeline(name=s['name'],global_start_time=o.opentime.RationalTime(0,rate),metadata={'framewright':metadata})
    for track in s['tracks']:
        t=o.schema.Track(name=track['id'],kind=o.schema.TrackKind.Video if track['kind']=='video' else o.schema.TrackKind.Audio)
        for item in track['items']:
            if item['type']=='gap':clip=o.schema.Gap(name=item['id'],source_range=tr(0,item['duration_frames']))
            else:
                m=checked['media'][item['media']]
                ref=o.schema.ExternalReference(target_url=quote(Path(m['path']).as_posix(),safe='/'),available_range=tr(0,float(available_frames(m['probe'][track['kind']],rate))),metadata={'framewright':{'material_id':m['id'],'sha256':m['sha256']}})
                clip=o.schema.Clip(name=item['id'],media_reference=ref,source_range=tr(item['in_frames'],item['duration_frames']),metadata={'framewright':{'clip_id':item['id'],'material_id':m['id'],'sha256':m['sha256']}})
            t.append(clip)
        tl.tracks.append(t)
    return tl


def signature(tl,rate):
    rows=[]
    for track in tl.tracks:
        items=[]
        for item in track:
            span=track.range_of_child(item)
            row={'id':item.name,'type':item.schema_name(),'timeline_start':span.start_time.rescaled_to(rate).value,'duration':span.duration.rescaled_to(rate).value}
            if hasattr(item,'media_reference'):row.update(target_url=item.media_reference.target_url,source_in=item.source_range.start_time.rescaled_to(rate).value,material=dict(item.media_reference.metadata['framewright']))
            items.append(row)
        rows.append({'id':track.name,'kind':track.kind,'items':items})
    return {'duration_frames':tl.duration().rescaled_to(rate).value,'rate':rate,'tracks':rows}


def export(spec,output):
    checked=inspect_spec(spec);output=output.resolve();base=Path(checked['spec_path']).parent
    if output.parent!=base or output.suffix!='.otio':raise ValueError('Write .otio beside the package specification')
    if output.exists():raise ValueError('Output exists; choose a new revision')
    o=library();timeline=make_timeline(checked)
    encoded=o.adapters.write_to_string(timeline,adapter_name='otio_json')
    back=o.adapters.read_from_string(encoded,adapter_name='otio_json')
    expected=signature(timeline,checked['spec']['rate'])
    if signature(back,checked['spec']['rate'])!=expected:raise ValueError('Round-trip structure changed')
    for m in checked['media'].values():
        if E['file_hash'](m['absolute_path'])!=m['sha256']:raise ValueError('Media changed during export')
    if E['file_hash'](spec)!=checked['spec_sha256']:raise ValueError('Specification changed during export')
    with output.open('x',encoding='utf-8') as f:f.write(encoded)
    reopened=o.adapters.read_from_file(str(output),adapter_name='otio_json')
    if signature(reopened,checked['spec']['rate'])!=expected:raise ValueError('Written-file round-trip differs')
    return {'schema':'framewright-otio-export-receipt-v1','otio_version':o.__version__,'output':output.name,'sha256':E['file_hash'](output),'spec_sha256':checked['spec_sha256'],'media':[{'id':m['id'],'path':m['path'],'sha256':m['sha256']} for m in checked['media'].values()],'roundtrip':expected,'editor_import':'not_tested','render_parity':'not_tested','publication_authorized':False}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('spec',type=Path);p.add_argument('--output',type=Path,required=True);p.add_argument('--receipt',type=Path,required=True);a=p.parse_args()
    try:
        if a.receipt.exists() or a.receipt.resolve()==a.output.resolve() or a.receipt.resolve()==a.spec.resolve():raise ValueError('Use a distinct new receipt path')
        r=export(a.spec,a.output)
        with a.receipt.open('x',encoding='utf-8') as f:json.dump(r,f,indent=2,allow_nan=False);f.write('\n')
        print(json.dumps({'output':str(a.output),'tracks':len(r['roundtrip']['tracks']),'frames':r['roundtrip']['duration_frames'],'roundtrip':'pass'}))
    except (OSError,ValueError,KeyError,TypeError,RuntimeError) as exc:p.exit(2,str(exc)+'\n')


if __name__=='__main__':main()
