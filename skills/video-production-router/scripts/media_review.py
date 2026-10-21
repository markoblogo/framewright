#!/usr/bin/env python3
"""Local audio/video measurements plus explicit, revision-bound review observations."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
import runpy
import shutil
import subprocess
import tempfile

BASE=Path(__file__).resolve().parent
MAX_BYTES=1024*1024*1024
MAX_SECONDS=20*60
MAX_JSON_BYTES=8*1024*1024
PROVENANCE={'owner_report','operator_observation','supplied_report','independent_check'}
METHODS={'visual':{'video','audio_video','frames'},'motion':{'video','audio_video'},
         'sync':{'audio_video'},'listening':{'audio','audio_video'},
         'content':{'audio','video','audio_video'}}


def require(test,message):
    if not test:raise ValueError(message)


def number(value):
    return type(value) in (int,float) and math.isfinite(value)


def text(value):
    return isinstance(value,str) and 0<len(value.strip())<=4096


def sha256(path):
    with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()


def read_json(path,expected_sha256=None):
    path=Path(path).resolve(strict=True)
    require(path.is_file() and path.stat().st_size<=MAX_JSON_BYTES,'Use a regular JSON file no larger than 8 MiB')
    def bad(value):raise ValueError('Non-finite JSON number: '+value)
    with path.open('rb') as stream:raw=stream.read(MAX_JSON_BYTES+1)
    require(len(raw)<=MAX_JSON_BYTES,'Use a JSON file no larger than 8 MiB')
    if expected_sha256:require(hashlib.sha256(raw).hexdigest()==expected_sha256,'Report bytes changed; retain the intended report revision')
    return json.loads(raw,parse_constant=bad)


def applicable(source):
    scopes=['content']
    if source['has_video']:scopes+=['visual','motion']
    if source['has_audio']:scopes+=['listening']
    if source['has_audio'] and source['has_video']:scopes+=['sync']
    return scopes


def full_coverage(spans,duration):
    end=0
    for a,b in sorted(spans):
        if a>end+1e-6:return False
        end=max(end,b)
    return end>=duration-1e-6


def validate_reviews(reviews,source):
    require(isinstance(reviews,list) and len(reviews)<=64,'Use at most 64 explicit reviews')
    seen=set()
    for row in reviews:
        require(isinstance(row,dict) and {'kind','actor','reviewer_version','provenance','method','coverage_type','coverage','result','findings'}<=set(row) and set(row)<={'kind','actor','reviewer_version','provenance','method','coverage_type','coverage','result','findings','sampled_fps'},'Invalid review fields')
        kind=row['kind'];require(kind in applicable(source) and kind not in seen,'Review kind must be applicable and unique; consolidate multiple reviewers explicitly')
        seen.add(kind)
        require(row['provenance'] in PROVENANCE and text(row['actor']) and text(row['reviewer_version']),'Explicit reviewer, version and provenance required')
        require(row['method'] in METHODS[kind],'Review input method cannot support this kind of assessment')
        if row['method']=='audio_video':require(source['has_audio'] and source['has_video'],'Audio/video input needs both streams')
        if row['method']=='audio':require(source['has_audio'],'Audio method needs audio')
        if row['method'] in {'video','frames'}:require(source['has_video'],'Visual method needs video')
        require(row['result'] in {'accepted','rejected','pending'},'Invalid review result')
        require(row['coverage_type'] in {'continuous','sampled'},'Explicit coverage type required')
        require(row.get('sampled_fps') is None or (number(row['sampled_fps']) and 0<row['sampled_fps']<=240),'Invalid optional sampled fps')
        require(row['coverage_type']!='continuous' or row.get('sampled_fps') is None,'Continuous review cannot declare a sampled fps')
        require(row['method']!='frames' or row['coverage_type']=='sampled','Frame sheets are sampled, not continuous video')
        spans=row['coverage'];require(isinstance(spans,list) and len(spans)<=100,'Invalid coverage')
        for span in spans:
            require(isinstance(span,list) and len(span)==2 and all(number(v) for v in span) and 0<=span[0]<span[1]<=source['duration_seconds']+1e-6,'Coverage must be within this media revision')
        require(row['result']=='pending' or bool(spans),'A completed review must record covered intervals')
        require(isinstance(row['findings'],list) and len(row['findings'])<=100,'Invalid findings')
        for finding in row['findings']:
            require(isinstance(finding,dict) and set(finding)=={'start','end','severity','note','action','reshoot'},'Invalid finding fields')
            a,b=finding['start'],finding['end']
            require((a is None and b is None) or (number(a) and number(b) and 0<=a<=b<=source['duration_seconds']),'Finding timestamps outside source')
            require(finding['severity'] in {'info','warning','error'} and text(finding['note']) and text(finding['action']) and type(finding['reshoot']) is bool,'Explicit severity, finding, action and reshoot decision required')
            require(a is None or any(sa<=a<=b<=sb for sa,sb in spans),'Finding timestamp is outside reviewed coverage')
            require(row['result']!='accepted' or (finding['severity']!='error' and not finding['reshoot']),'An accepted review cannot retain an error or reshoot request')


def summarise(report):
    source=report['source'];results={kind:'pending' for kind in applicable(source)}
    findings=[]
    for row in report['reviews']:
        result=row['result']
        if result=='accepted' and (row['coverage_type']!='continuous' or not full_coverage(row['coverage'],source['duration_seconds'])):
            result='pending'
        results[row['kind']]=result
        findings.extend(dict(f,kind=row['kind'],actor=row['actor']) for f in row['findings'])
    streams=report['technical']['streams']
    multiple=any(sum(s.get('codec_type')==kind and not s.get('disposition',{}).get('attached_pic') for s in streams)>1 for kind in ['audio','video'])
    if multiple:results={k:'pending' if v=='accepted' else v for k,v in results.items()}
    unresolved=[k for k,v in results.items() if v!='accepted']
    if multiple:unresolved.append('multiple_streams_review_separate_derivatives')
    if report['technical']['result']!='pass':unresolved.insert(0,'technical')
    return {'technical_result':report['technical']['result'],'results':results,
            'perceptual_result':'rejected' if 'rejected' in results.values() else 'pending' if 'pending' in results.values() else 'accepted',
            'unresolved':unresolved,'findings':findings,'reshoot':[f for f in findings if f['reshoot']],
            'note':'Measurements, supplied review judgments and owner acceptance are separate; no publication authority.'}


def validate(report,pin=None):
    json.dumps(report,allow_nan=False)  # Reject non-finite values even inside nested measurements.
    require(isinstance(report,dict) and set(report)=={'schema_version','type','generated_at','execution','publication_authorized','source','technical','reviews','summary'},'Invalid media report fields')
    require(type(report['schema_version']) is int and report['schema_version']==1 and report['type']=='media-review','Unsupported media report')
    require(report['execution']=='local_measurements_and_supplied_observations' and report['publication_authorized'] is False,'Report cannot grant execution/publication authority')
    require(text(report['generated_at']),'Report timestamp required')
    require(datetime.fromisoformat(report['generated_at']).tzinfo is not None,'Timestamp needs a timezone')
    source=report['source']
    require(isinstance(source,dict) and set(source)=={'path','sha256','bytes','duration_seconds','has_audio','has_video'},'Invalid source binding')
    require(text(source['path']) and isinstance(source['sha256'],str) and re.fullmatch('[0-9a-f]{64}',source['sha256']) and type(source['bytes']) is int and 0<source['bytes']<=MAX_BYTES,'Invalid source hash/bytes')
    require(number(source['duration_seconds']) and 0<source['duration_seconds']<=MAX_SECONDS,'Unsupported media duration; maximum 20 minutes')
    require(type(source['has_audio']) is bool and type(source['has_video']) is bool and (source['has_audio'] or source['has_video']),'Audio/video stream flags required')
    if pin:require((source['sha256'],source['bytes'])==(pin['sha256'],pin['bytes']),'Report belongs to a different media revision')
    tech=report['technical']
    require(isinstance(tech,dict) and set(tech)=={'result','decode','streams','calibration','calibration_status'},'Invalid technical result')
    require(isinstance(tech['streams'],list) and 0<len(tech['streams'])<=16 and all(isinstance(s,dict) and type(s.get('index')) is int and isinstance(s.get('codec_type'),str) for s in tech['streams']),'Invalid stream metadata')
    require(all(isinstance(s.get('disposition',{}),dict) for s in tech['streams']),'Invalid stream disposition')
    require(source['has_audio']==any(s['codec_type']=='audio' for s in tech['streams']) and source['has_video']==any(s['codec_type']=='video' and not s.get('disposition',{}).get('attached_pic') for s in tech['streams']),'Stream metadata does not match source flags')
    require(tech['result'] in {'pass','fail'} and isinstance(tech['decode'],dict) and set(tech['decode'])=={'result','error','decoded_seconds','video_frames'},'Invalid decode result')
    decoded=tech['decode']['decoded_seconds'];frames=tech['decode']['video_frames']
    require(decoded is None or (number(decoded) and decoded>=0),'Invalid decoded duration')
    require(frames is None or (type(frames) is int and frames>=0),'Invalid decoded frame count')
    if tech['result']=='pass':
        require(decoded is not None and decoded>0 and decoded+max(.25,source['duration_seconds']*.01)>=source['duration_seconds'],'No complete decoded-duration evidence')
        require(not source['has_video'] or (frames is not None and frames>0),'No decoded video-frame evidence')
    require(tech['result']==tech['decode']['result'] and isinstance(tech['decode']['error'],str),'Technical result must describe the retained decode result')
    require((tech['result']=='pass' and not tech['decode']['error']) or (tech['result']=='fail' and text(tech['decode']['error'])),'Decode result/error mismatch')
    short=source['duration_seconds']<=60 and source['bytes']<=100*1024*1024
    allowed=({'not_performed_decode_failed'} if tech['result']=='fail' else
             {'performed','failed'} if short else {'outside_short_capture_limits'})
    require(tech['calibration_status'] in allowed,'Calibration status contradicts decode result or short-capture limits')
    if tech['calibration_status']=='performed':
        c=tech['calibration'];require(isinstance(c,dict) and c.get('sha256')==source['sha256'] and c.get('source_unchanged') is True and c.get('perceptual_review')=='not_performed','Calibration must match source and cannot claim perception')
        require(source['duration_seconds']<=60 and source['bytes']<=100*1024*1024,'Calibration exceeds short-capture limits')
        for name in ['audio','video']:
            if source['has_'+name]:require(isinstance(c.get(name),dict),'Performed calibration needs measurements for each source stream')
            require(c.get(name) is None or isinstance(c[name],dict),'Invalid calibration measurement type')
        if isinstance(c.get('audio'),dict):
            channels=c['audio'].get('channels')
            require(isinstance(channels,list) and 0<len(channels)<=8,'Invalid calibration channels')
            require(all(isinstance(ch,dict) and isinstance(ch.get('flags'),list) and all(isinstance(v,str) for v in ch['flags']) for ch in channels),'Invalid channel flags')
        if isinstance(c.get('video'),dict):
            require(isinstance(c['video'].get('flags'),list) and all(isinstance(v,str) for v in c['video']['flags']),'Invalid video flags')
    else:require(tech['calibration'] is None,'Unperformed calibration must be null')
    validate_reviews(report['reviews'],source)
    require(report['summary']==summarise(report),'Report summary differs from its measurements/reviews')
    return report


def build(path,observations=None):
    path=Path(path).resolve(strict=True)
    require(path.is_file() and 0<path.stat().st_size<=MAX_BYTES,'Use a regular local media file no larger than 1 GiB')
    for tool in ('ffmpeg','ffprobe'):require(shutil.which(tool),tool+' is not installed; nothing will be downloaded')
    before={'sha256':sha256(path),'bytes':path.stat().st_size}
    try:
        proc=subprocess.run(['ffprobe','-v','error','-protocol_whitelist','file,pipe','-show_entries','format=duration:stream=index,codec_type,codec_name,width,height,avg_frame_rate,sample_rate,channels:stream_disposition=attached_pic','-of','json',str(path)],capture_output=True,check=True,timeout=30)
        probe=json.loads(proc.stdout)
        duration=float(probe.get('format',{}).get('duration',0))
        require(math.isfinite(duration) and 0<duration<=MAX_SECONDS,'Use audio/video with known duration up to 20 minutes; still images are not supported')
        streams=probe.get('streams',[]);require(len(streams)<=16,'At most 16 streams supported')
        source={'path':str(path),**before,'duration_seconds':duration,
                'has_audio':any(s.get('codec_type')=='audio' for s in streams),
                'has_video':any(s.get('codec_type')=='video' and not s.get('disposition',{}).get('attached_pic') for s in streams)}
        require(source['has_audio'] or source['has_video'],'No timed audio/video stream found')
        require(all(int(s.get('width',0))*int(s.get('height',0))<=8192*8192 for s in streams if s.get('codec_type')=='video'),'Video dimensions exceed local inspection limits')
        with tempfile.TemporaryFile() as errors, tempfile.TemporaryFile() as progress:
            try:
                decoded=subprocess.run(['ffmpeg','-v','error','-xerror','-nostdin','-threads','2','-protocol_whitelist','file,pipe','-i',str(path),'-map','0:v?','-map','0:a?','-progress','pipe:1','-nostats','-f','null','-'],stdout=progress,stderr=errors,timeout=180)
                errors.seek(0,2);size=errors.tell();errors.seek(max(0,size-3000))
                message=errors.read().decode(errors='replace').strip()
                progress.seek(0,2);size=progress.tell();progress.seek(max(0,size-8192))
                tail=progress.read().decode(errors='replace')
                times=re.findall(r'^out_time_us=(\d+)$',tail,re.M);counts=re.findall(r'^frame=(\d+)$',tail,re.M)
                seconds=int(times[-1])/1000000 if times else None;frames=int(counts[-1]) if counts else None
                if decoded.returncode and not message:message='Decoder failed'
                if not message and ('progress=end' not in tail or not seconds or seconds+max(.25,duration*.01)<duration or (source['has_video'] and not frames)):
                    message='Full decoded duration/frame evidence missing or shorter than metadata; inspect source and timing'
                decode={'result':'fail' if message else 'pass','error':message,'decoded_seconds':seconds,'video_frames':frames}
            except subprocess.TimeoutExpired:
                decode={'result':'fail','error':'Decode exceeded 180s local limit; no complete decode claimed','decoded_seconds':None,'video_frames':None}
    except subprocess.TimeoutExpired as exc:raise ValueError('Metadata inspection timed out') from exc
    except subprocess.CalledProcessError as exc:raise ValueError('Cannot inspect media metadata: '+exc.stderr.decode(errors='replace')[-1200:]) from exc
    require(sha256(path)==before['sha256'] and path.stat().st_size==before['bytes'],'Source changed during decode; repeat on a stable file')
    calibration=None
    status='not_performed_decode_failed' if decode['result']=='fail' else 'outside_short_capture_limits'
    if decode['result']=='pass' and duration<=60 and before['bytes']<=100*1024*1024:
        try:
            calibration=runpy.run_path(str(BASE/'capture_check.py'))['inspect'](path)
            status='performed'
        except ValueError:status='failed'
    require(sha256(path)==before['sha256'] and path.stat().st_size==before['bytes'],'Source changed during inspection; repeat on a stable file')
    reviews=[]
    if observations is not None:
        require(isinstance(observations,dict) and set(observations)=={'source_sha256','reviews'},'Observations need source_sha256 and reviews only')
        require(observations['source_sha256']==before['sha256'],'Observations belong to a different media revision')
        reviews=observations['reviews']
    report={'schema_version':1,'type':'media-review','generated_at':datetime.now(timezone.utc).isoformat(),
            'execution':'local_measurements_and_supplied_observations','publication_authorized':False,
            'source':source,'technical':{'result':decode['result'],'decode':decode,'streams':streams,'calibration':calibration,'calibration_status':status},'reviews':reviews}
    validate_reviews(reviews,source);report['summary']=summarise(report)
    return validate(report)


def receipts(report):
    validate(report)
    results=report['summary']['results'];creative=[v for k,v in results.items() if k!='listening']
    playback=[results[k] for k in ['visual','motion','sync'] if k in results]
    technical=('fail' if report['technical']['result']=='fail' or 'rejected' in playback else
               'pending' if 'pending' in playback else 'pass')
    rows={'technical':technical,
          'creative':'rejected' if 'rejected' in creative else 'pending' if 'pending' in creative else 'accepted'}
    if report['source']['has_audio']:rows['listening']=results['listening']
    return rows


def markdown(report):
    validate(report);cell=runpy.run_path(str(BASE/'packet.py'))['cell']
    lines=['# Media review','', 'Local measurements and supplied observations. No automatic publication approval.','',
           'Source: '+cell(report['source']['path']), 'SHA-256: '+report['source']['sha256'],'',
           'Technical decode: '+report['technical']['result'], 'Short-recording calibration: '+report['technical']['calibration_status'],'',
           '| Review | Result |','| --- | --- |']
    lines += ['| '+cell(k)+' | '+cell(v)+' |' for k,v in report['summary']['results'].items()]
    lines += ['', '## Review coverage','']
    for r in report['reviews']:
        lines.append('- '+cell(f"{r['kind']}: {r['actor']} ({r['reviewer_version']}), {r['method']}, {r['coverage_type']}, fps {r.get('sampled_fps', 'not recorded')}, {r['coverage']}; declared {r['result']}. Supplied provenance: {r['provenance']}"))
    lines += ['', '## Findings and next actions','']
    lines.append('- Stream metadata: '+cell(json.dumps(report['technical']['streams'],ensure_ascii=False)))
    if report['technical']['decode']['error']:lines.append('- '+cell(report['technical']['decode']['error']))
    c=report['technical']['calibration']
    if c:
        audio=c.get('audio')
        if isinstance(audio,dict):
            lines+=['', '| Audio channel | Sample peak dBFS | RMS dBFS | Flags |', '| --- | --- | --- | --- |']
            for channel in audio.get('channels',[]):
                if isinstance(channel,dict):
                    lines.append('| '+' | '.join(cell(v) for v in [channel.get('channel'),channel.get('sample_peak_dbfs'),channel.get('rms_dbfs'),', '.join(channel.get('flags',[])) or 'none recorded'])+' |')
        video=c.get('video')
        if isinstance(video,dict):
            lines+=['', '- '+cell(f"Video: {video.get('width')} × {video.get('height')}; fps {video.get('average_frame_rate')}; sampled luma frames {video.get('sampled_luma_frames')}. This is not a motion/quality verdict."),
                    '- Video flags: '+cell(', '.join(video.get('flags',[])) or 'none recorded')]
    for f in report['summary']['findings']:
        lines.append('- '+cell(f"{f['kind']} {f['start']}–{f['end']}s [{f['severity']}]: {f['note']} → {f['action']}; reshoot requested: {f['reshoot']}"))
    lines+=['', 'Unresolved: '+cell(', '.join(report['summary']['unresolved']) or 'none recorded'),
            'Reshoot decisions: '+str(len(report['summary']['reshoot']))+' supplied requests; unreviewed areas remain unknown.',
            '', 'The local technical field covers metadata/full decode; the imported QA gate also requires applicable visual, motion and sync reviews. Import never finishes tasks.', '']
    return '\n'.join(lines)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file',nargs='?');parser.add_argument('--observations',type=Path)
    parser.add_argument('--read',type=Path,help='Validate/display a saved report; no media decoding')
    parser.add_argument('--format',choices=['json','markdown'],default='json')
    args=parser.parse_args()
    try:
        require(bool(args.file)!=bool(args.read),'Supply a media file or --read REPORT')
        require(not args.read or not args.observations,'--read does not merge observations')
        report=validate(read_json(args.read)) if args.read else build(args.file,read_json(args.observations) if args.observations else None)
        print(markdown(report),end='') if args.format=='markdown' else print(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False))
    except (OSError,ValueError,TypeError,KeyError,RecursionError) as exc:parser.exit(2,str(exc)+'\n')


if __name__=='__main__':main()
