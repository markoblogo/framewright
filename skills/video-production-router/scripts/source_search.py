#!/usr/bin/env python3
"""Local lexical retrieval over explicitly supplied, revision-bound content evidence."""
import argparse
import json
from pathlib import Path
import re
import runpy

E=runpy.run_path(str(Path(__file__).with_name('editing.py')))


def import_whisper(source,transcript,receipt,identity):
    """Adapt a retained local run; never execute ASR or correct recognised words."""
    source=source.resolve(strict=True);transcript=transcript.resolve(strict=True);receipt=receipt.resolve(strict=True)
    pins={p:E['file_hash'](p) for p in (source,transcript,receipt)}
    r=E['load'](receipt);raw=E['load'](transcript)
    if not isinstance(r,dict) or not isinstance(raw,dict):raise ValueError('ASR receipt and raw result must be objects')
    if r.get('schema')!='framewright-local-whisper-receipt-v1' or r.get('timing_origin')!='source_playback_zero':
        raise ValueError('Use a local Whisper receipt with original-source playback timing')
    if r.get('source_sha256')!=pins[source] or r.get('transcript_sha256')!=pins[transcript]:
        raise ValueError('ASR receipt does not match source/transcript bytes')
    model=r.get('model')
    if not isinstance(model,dict) or not model.get('package') or not model.get('version') or not model.get('weights'):
        raise ValueError('Retained ASR model/package/version and weight identity required')
    segments=raw.get('segments')
    if not isinstance(segments,list) or not segments:raise ValueError('Nonempty Whisper segments required')
    rows=[{'id':f'asr-{i:04d}','start':s['start'],'end':s['end'],'text':s['text']} for i,s in enumerate(segments,1)]
    item={'id':E['text'](identity,'source ID'),'path':str(source),'evidence_sha256':pins[source],
          'transcript':rows,'observations':[],'annotation_provenance':{
              'method':'local_asr_unverified','scope':'Raw recognised text; no listening, pronunciation, visual or semantic approval.',
              'model':model,'receipt_sha256':pins[receipt]}}
    # Validate all segment intervals against the actual source, without shifting or clamping.
    E['inventory']({'sources':[item]},source.parent)
    for p,pin in pins.items():
        if E['file_hash'](p)!=pin:raise ValueError('ASR inputs changed during import')
    return {'sources':[item],'evidence_files':[{'path':str(p),'sha256':pins[p]} for p in (transcript,receipt)]}


def build(specpath):
    specpath=specpath.resolve(strict=True);spec_hash=E['file_hash'](specpath);spec=E['load'](specpath);base=specpath.parent
    if not isinstance(spec,dict) or not isinstance(spec.get('sources'),list) or not spec['sources']:raise ValueError('Explicit nonempty sources required')
    rows=[];ids=set()
    for source in spec['sources']:
        sid=E['text'](source.get('id'),'source id')
        if sid in ids:raise ValueError('Duplicate source ID')
        ids.add(sid)
        provenance=source.get('annotation_provenance')
        if not isinstance(provenance,dict) or not provenance.get('method') or not provenance.get('scope'):raise ValueError('Annotation method and scope required')
        if source.get('kind')=='image':
            name=E['text'](source.get('path'),'image path')
            if '://' in name:raise ValueError('Only local sources supported')
            path=(base/name).resolve(strict=True);pin=E['file_hash'](path)
            if source.get('evidence_sha256')!=pin:raise ValueError('Image observation needs matching source hash')
            if source.get('transcript'):raise ValueError('Still-image speech is not inferred')
            obs=source.get('observations',[])
            if not isinstance(obs,list):raise ValueError('Observations must be a list')
            seen=set()
            for r in obs:
                rid=E['text'](r.get('id'),'observation ID');E['text'](r.get('text'),'observation')
                if rid in seen or set(r)!={'id','text'}:raise ValueError('Still observations need unique IDs and text only')
                seen.add(rid)
            row={'id':sid,'path':str(path),'sha256':pin,'kind':'image','duration_seconds':None,'transcript':[],'observations':obs}
        else:
            row=E['inventory']({'sources':[source]},base)['sources'][0];row['kind']='timed_media'
        row['annotation_provenance']=provenance;rows.append(row)
    evidence=[]
    for item in spec.get('evidence_files',[]):
        path=(base/E['text'](item.get('path'),'evidence path')).resolve(strict=True)
        if E['file_hash'](path)!=item.get('sha256'):raise ValueError('Evidence sidecar hash differs')
        evidence.append({'path':str(path),'sha256':item['sha256']})
    if E['file_hash'](specpath)!=spec_hash:raise ValueError('Source specification changed during indexing')
    result={'schema':'framewright-source-evidence-index-v1','spec':{'path':str(specpath),'sha256':spec_hash},
            'sources':rows,'evidence_files':evidence,'retrieval':'lexical_only_over_supplied_annotations',
            'automatic_model_calls':0,'publication_authorized':False,
            'note':'No ASR, OCR, visual recognition or acoustic/semantic verification is performed by this indexer.'}
    result['index_sha256']=E['digest'](result);return result


def search(index,query,kind='any'):
    if index.get('schema')!='framewright-source-evidence-index-v1':raise ValueError('Unsupported index')
    unsigned={k:v for k,v in index.items() if k!='index_sha256'}
    if E['digest'](unsigned)!=index.get('index_sha256'):raise ValueError('Index changed; rebuild explicitly')
    for row in [index['spec'],*index['sources'],*index['evidence_files']]:
        if E['file_hash'](Path(row['path']))!=row['sha256']:raise ValueError('Source or annotations changed; rebuild and review selections')
    words=re.findall(r'\w+',E['text'](query,'query').casefold())
    if not words or kind not in {'any','transcript','observations'}:raise ValueError('Use text query and supported evidence kind')
    results=[]
    for source in index['sources']:
        for channel in ['transcript','observations']:
            if kind not in {'any',channel}:continue
            for row in source[channel]:
                tokens=set(re.findall(r'\w+',row['text'].casefold()))
                if not set(words).issubset(tokens):continue
                results.append({'source':source['id'],'source_sha256':source['sha256'],'evidence_id':row['id'],
                    'channel':channel,'start':row.get('start'),'end':row.get('end'),'text':row['text'],
                    'annotation_provenance':source['annotation_provenance'],'qualification':'candidate_requires_review'})
    return {'schema':'framewright-source-search-v1','index_sha256':index['index_sha256'],'query':query,'kind':kind,
            'status':'candidates_found' if results else 'not_found_in_index','results':results,
            'scope':'All query tokens must match one supplied annotation; no semantic search. Not found does not establish absence from the media.',
            'automatic_model_calls':0,'publication_authorized':False}


def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    a=sub.add_parser('index');a.add_argument('spec',type=Path);a.add_argument('--output',type=Path,required=True)
    a=sub.add_parser('search');a.add_argument('index',type=Path);a.add_argument('--query',required=True);a.add_argument('--kind',choices=['any','transcript','observations'],default='any');a.add_argument('--output',type=Path,required=True)
    a=sub.add_parser('import-whisper');a.add_argument('source',type=Path);a.add_argument('--transcript',type=Path,required=True);a.add_argument('--receipt',type=Path,required=True);a.add_argument('--source-id',required=True);a.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    try:
        if a.command=='import-whisper':result=import_whisper(a.source,a.transcript,a.receipt,a.source_id)
        elif a.command=='index':result=build(a.spec)
        else:result=search(E['load'](a.index),a.query,a.kind)
        with a.output.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2,ensure_ascii=False,allow_nan=False);f.write('\n')
        print(json.dumps({'output':str(a.output),'sources':len(result.get('sources',[])), 'results':len(result.get('results',[])),'automatic_model_calls':0}))
    except (OSError,ValueError,KeyError,TypeError) as exc:p.exit(2,str(exc)+'\n')


if __name__=='__main__':main()
