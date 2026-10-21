#!/usr/bin/env python3
"""Generate label-blinded local video controls; grade supplied answers, never call models."""
import argparse
import array
import hashlib
import json
import math
from pathlib import Path
import random
import re
import runpy
import secrets
import shutil
import subprocess
import sys
import tempfile
import wave

BASE=Path(__file__).resolve().parent
MEDIA=runpy.run_path(str(BASE/'media_review.py'))
require=MEDIA['require'];number=MEDIA['number'];read_json=MEDIA['read_json'];sha256=MEDIA['sha256']
WIDTH,HEIGHT,FPS,SECONDS=640,360,12,10
SCOPES=['content','visual','motion','listening','sync']
CATEGORIES={'freeze':'motion','blackout':'visual','missing_action':'content','av_sync':'sync','unreadable_text':'visual','audio_artifact':'listening'}
# Locally authored 5x7 block glyphs: no external fonts, media or voices.
FONT={
'A':['01110','10001','10001','11111','10001','10001','10001'],
'C':['01111','10000','10000','10000','10000','10000','01111'],
'D':['11110','10001','10001','10001','10001','10001','11110'],
'E':['11111','10000','10000','11110','10000','10000','11111'],
'L':['10000','10000','10000','10000','10000','10000','11111'],
'M':['10001','11011','10101','10101','10001','10001','10001'],
'N':['10001','11001','10101','10011','10001','10001','10001'],
'O':['01110','10001','10001','10001','10001','10001','01110'],
'P':['11110','10001','10001','11110','10000','10000','10000'],
'R':['11110','10001','10001','11110','10100','10010','10001'],
'S':['01111','10000','10000','01110','00001','00001','11110'],
'T':['11111','00100','00100','00100','00100','00100','00100'],
'V':['10001','10001','10001','10001','10001','01010','00100'],
'Y':['10001','10001','01010','00100','00100','00100','00100'],
' ':['00000']*7}


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()


def write(path,value):
    with path.open('x') as stream:json.dump(value,stream,indent=2,allow_nan=False);stream.write('\n')


def event(category,start,end):
    return {'category':category,'kind':CATEGORIES[category],'start':start,'end':end}


def recipes():
    return [
        ('clean',[],['Continuous reference']),
        ('freeze',[event('freeze',4,5.25)],['Authored whole-frame hold interrupts required movement']),
        ('black',[event('blackout',5,6)],['Authored black interval interrupts required view']),
        ('missing',[event('missing_action',2,3)],['Door stays shut after required opening command']),
        ('sync',[event('av_sync',2,3),event('av_sync',8,9)],['Both beeps delayed by 0.65 seconds']),
        ('tiny',[event('unreadable_text',0,10)],['Main heading reduced to 7px high at low contrast; human readability confirmation pending']),
        ('cut',[],['Allowed hard cut at 5 seconds; movement continues']),
        ('hold',[],['Allowed final-state hold from 8.5 seconds'])]


def frame(kind,index):
    t=index/FPS
    if kind=='black' and 5<=t<6:return bytes(WIDTH*HEIGHT*3)
    if kind=='freeze' and 4<=t<5.25:t=4
    if kind=='hold' and t>=8.5:t=8.5
    bg=(15,23,36) if kind!='cut' or t<5 else (33,19,46)
    pixels=bytearray(bytes(bg)*(WIDTH*HEIGHT))
    def rect(x,y,w,h,color):
        x,y,w,h=map(int,(x,y,w,h));a,b=max(0,x),min(WIDTH,x+w)
        if b<=a:return
        line=bytes(color)*(b-a)
        for row in range(max(0,y),min(HEIGHT,y+h)):
            start=(row*WIDTH+a)*3;pixels[start:start+len(line)]=line
    def label(value,x,y,scale,color):
        for ch in value:
            for row,bits in enumerate(FONT[ch]):
                for col,bit in enumerate(bits):
                    if bit=='1':rect(x+col*scale,y+row*scale,scale,scale,color)
            x+=6*scale
    light=(227,235,245);cyan=(38,220,211)
    if kind=='tiny':label('READY TO RECORD',275,35,1,(24,32,46))
    else:label('READY TO RECORD',95,24,5,light)
    label('DOOR',420,95,3,light)
    opened=2<=t<8 and kind!='missing'
    rect(422,125,154,100,cyan if opened else (180,65,77))
    rect(430,133,138,84,bg)
    gap=min(1,max(0,(t-2)*2)) if opened else 0
    panel=int(66*(1-gap))
    rect(433,137,panel,76,(115,135,158));rect(565-panel,137,panel,76,(115,135,158))
    label('OPEN' if opened else 'CLOSED',430 if opened else 411,235,3,light)
    pulse=any(start<=t<start+.25 for start in (2,8))
    rect(48,112,72,72,light if pulse else (45,60,80));label('MOVE',50,215,3,light)
    rect(48,294,544,4,(85,105,132))
    x=50+500*max(0,min(1,(t-3)/3))
    rect(x,265,32,28,(246,168,55));rect(x+5,270,22,18,(255,211,126))
    rect(48,333,544,6,(45,60,80));rect(48,333,int(544*t/10),6,cyan)
    return pixels


def audio(path,delay):
    rate=16000;samples=array.array('h')
    for i in range(rate*SECONDS):
        t=i/rate;value=0
        for onset in (2+delay,8+delay):
            u=t-onset
            if 0<=u<.15:
                gain=min(1,u/.005,(.15-u)/.005)
                value+=int(8000*gain*math.sin(2*math.pi*880*u))
        samples.append(value)
    if sys.byteorder!='little':samples.byteswap()
    with wave.open(str(path),'wb') as stream:
        stream.setnchannels(1);stream.setsampwidth(2);stream.setframerate(rate);stream.writeframes(samples.tobytes())


def brief():
    return ('Inspect the actual clip with audio at normal 640x360 playback size. The main heading must read READY TO RECORD. '
            'A command light flashes and a short beep starts together at about 2s and 8s. The door opens after the first cue and closes after the second. '
            'The orange card must move smoothly left to right between 3s and 6s. One hard cut to another clean view is allowed; a static final state after 8.5s is allowed. '
            'Check content, visual legibility, motion continuity, sound clarity and cue synchronisation. No spoken narration is present. '
            'Report observations with timestamps; use unknown for unsupported or unobserved checks. Do not infer that a clip is faulty just because this is a test. '
            'Return the answers-template JSON with your actual reviewer/version, input method, coverage and run kind. Finding categories are freeze, blackout, missing_action, av_sync, unreadable_text, audio_artifact. '
            'Use a separate finding for each occurrence. Notes explain observed evidence. Do not inspect operator files or fixture-generating source while reviewing. '
            'A supplied declaration of modality is not independent proof that bytes reached a model.')


def probe_controls(root,cases,gold):
    rows={}
    for case in cases:
        path=Path(root)/'reviewer'/case['file']
        common=['ffmpeg','-v','error','-nostdin','-protocol_whitelist','file,pipe','-i',str(path)]
        decoded=subprocess.run(common+['-map','0:v:0','-an','-vf','select=eq(n\\,30)+eq(n\\,51)+eq(n\\,57)+eq(n\\,66)+eq(n\\,108)+eq(n\\,114)',
            '-fps_mode','passthrough','-pix_fmt','rgb24','-f','rawvideo','-'],capture_output=True,check=True,timeout=30).stdout
        stride=WIDTH*HEIGHT*3;require(len(decoded)==stride*6,'Probe frame count differs from fixture recipe')
        frames=[decoded[i*stride:(i+1)*stride] for i in range(6)]
        def mae(a,b):return sum(abs(x-y) for x,y in zip(a,b))/len(a)
        def crop(data,left,top,right,bottom):
            values=[]
            for y in range(top,bottom):
                for x in range(left,right):
                    i=(y*WIDTH+x)*3;values.append(sum(data[i:i+3])/3)
            return values
        header=crop(frames[0],80,18,570,80);door=crop(frames[0],452,145,555,202)
        flashes=subprocess.run(common+['-map','0:v:0','-an','-vf','crop=2:2:70:140,scale=1:1,format=gray','-f','rawvideo','-'],capture_output=True,check=True,timeout=30).stdout
        flash_onsets=[i/FPS for i,v in enumerate(flashes) if v>160 and (i==0 or flashes[i-1]<=160)]
        pcm=subprocess.run(common+['-map','0:a:0','-vn','-ar','16000','-ac','1','-f','s16le','-'],capture_output=True,check=True,timeout=30).stdout
        samples=array.array('h');samples.frombytes(pcm)
        if sys.byteorder!='little':samples.byteswap()
        onsets=[];last=-16000
        for i,value in enumerate(samples):
            if abs(value)>=2000:
                if i-last>16000*.3:onsets.append(i/16000)
                last=i
        require(len(onsets)==2 and len(flash_onsets)==2,'Encoded cue count differs from fixture recipe')
        rows[case['id']]={'audio_cue_onsets_seconds':onsets,'flash_onsets_seconds':flash_onsets,
                         'audio_minus_flash_seconds':[round(a-v,6) for a,v in zip(onsets,flash_onsets)],
                         'motion_pair_mae':round(mae(frames[1],frames[2]),6),'final_hold_pair_mae':round(mae(frames[4],frames[5]),6),
                         'header_luma_range':round(max(header)-min(header),3),'door_center_mean':round(sum(door)/len(door),3),
                         'mid_luma_mean':round(sum(frames[3])/len(frames[3]),3)}
    by_recipe={gold[k]['recipe']:v for k,v in rows.items()}
    for case in cases:
        delay=.65 if gold[case['id']]['recipe']=='sync' else 0
        require(all(abs(v-delay)<.05 for v in rows[case['id']]['audio_minus_flash_seconds']),'Encoded cue timing differs from recipe')
    require(by_recipe['freeze']['motion_pair_mae']<.05 and by_recipe['clean']['motion_pair_mae']>.1,'Encoded motion-control separation failed')
    require(by_recipe['black']['mid_luma_mean']<2,'Black interval did not survive encoding')
    require(by_recipe['tiny']['header_luma_range']<40 and by_recipe['clean']['header_luma_range']>100,'Header contrast control separation failed')
    require(by_recipe['missing']['door_center_mean']-by_recipe['clean']['door_center_mean']>60,'Door-state control separation failed')
    require(by_recipe['hold']['final_hold_pair_mae']<.05,'Final hold did not survive encoding')
    return {'scope':'encoded_fixture_measurements_not_perceptual_review','semantic_label_validation':'pending_human','cases':rows}


def build(output,seed=None):
    for tool in ['ffmpeg','ffprobe']:require(shutil.which(tool),tool+' must already be installed')
    output=Path(output).absolute();require(output.parent.is_dir(),'Create the output parent explicitly')
    output.mkdir()  # Refuse existing directories, even an empty one.
    reviewer=output/'reviewer';operator=output/'operator';reviewer.mkdir();operator.mkdir()
    source_snapshot=Path(__file__).read_bytes()
    (operator/'generator.py').write_bytes(source_snapshot)
    salt=str(seed) if seed is not None else secrets.token_hex(16)
    selected=[];gold={};qa={}
    with tempfile.TemporaryDirectory(prefix='.control-build-',dir=output) as work:
        raw=Path(work)/'frames.rgb';wav=Path(work)/'cues.wav'
        for kind,events,notes in recipes():
            identity='c_'+hashlib.sha256((salt+':'+kind).encode()).hexdigest()[:12]
            name=identity+'.mp4';target=reviewer/name
            with raw.open('wb') as stream:
                for i in range(FPS*SECONDS):stream.write(frame(kind,i))
            audio(wav,.65 if kind=='sync' else 0)
            args=['ffmpeg','-v','error','-nostdin','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{WIDTH}x{HEIGHT}',
                  '-framerate',str(FPS),'-i',str(raw),'-i',str(wav),'-map','0:v:0','-map','1:a:0','-t',str(SECONDS),
                  '-c:v','libx264','-preset','veryfast','-crf','18','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','64k','-movflags','+faststart',str(target)]
            subprocess.run(args,check=True,capture_output=True,timeout=45)
            report=MEDIA['build'](target)
            require(report['technical']['result']=='pass','Encoded control did not complete technical decode')
            require(target.stat().st_size<=25*1024*1024,'Encoded control unexpectedly large')
            selected.append({'id':identity,'file':name,'sha256':report['source']['sha256'],'duration_seconds':report['source']['duration_seconds'],
                             'width':WIDTH,'height':HEIGHT,'fps':FPS})
            gold[identity]={'recipe':kind,'events':events,'notes':notes};qa[identity]=report
    random.Random(salt).shuffle(selected)
    manifest={'schema_version':1,'model_evaluation':'not_performed','label_validation':'authored_not_human_verified',
              'generator_sha256':hashlib.sha256(source_snapshot).hexdigest(),
              'runtime':{'media_review_sha256':sha256(BASE/'media_review.py'),**{name:subprocess.run([name,'-version'],capture_output=True,check=True,timeout=10).stdout.decode().splitlines()[0] for name in ['ffmpeg','ffprobe']}},'seed':salt,'cases':selected,'publication_authorized':False}
    task={'schema_version':1,'brief':brief(),'cases':selected}
    write(operator/'suite.json',manifest);write(operator/'gold.json',gold);write(operator/'encoded-qa.json',qa);write(reviewer/'task.json',task)
    write(operator/'perturbation-qa.json',probe_controls(output,selected,gold))
    files={str(p.relative_to(output)):sha256(p) for p in sorted(output.rglob('*')) if p.is_file()}
    suite_hash=digest(files)
    answers={'schema_version':1,'suite_sha256':suite_hash,'reviewer':{'actor':'not_recorded','version':'not_recorded','run_kind':'not_run'},
             'cases':[{'id':c['id'],'source_sha256':c['sha256'],'method':'audio_video','coverage_type':'sampled','sampled_fps':None,
                       'coverage':[],'checks':{k:'unknown' for k in SCOPES},'findings':[]} for c in selected]}
    write(reviewer/'answers-template.json',answers);files['reviewer/answers-template.json']=sha256(reviewer/'answers-template.json')
    write(output/'freeze.json',{'schema_version':1,'suite_sha256':suite_hash,'files':files})
    return {'suite':str(output),'suite_sha256':suite_hash,'clips':8,'model_evaluation':'not_performed','label_validation':'authored_not_human_verified',
            'reviewer_packet':str(reviewer),'operator_gold':str(operator),'publication_authorized':False}


def verify(root):
    root=Path(root).resolve(strict=True);frozen=read_json(root/'freeze.json')
    require(frozen.get('schema_version')==1 and isinstance(frozen.get('files'),dict),'Unsupported control freeze')
    require(4<=len(frozen['files'])<=20,'Unexpected frozen file count')
    for name,expected in frozen['files'].items():
        path=root/name
        require(not Path(name).is_absolute() and '..' not in Path(name).parts and path.resolve().is_relative_to(root),'Unsafe frozen path')
        require(not any((root/Path(*Path(name).parts[:i])).is_symlink() for i in range(1,len(Path(name).parts)+1)),'Symlinked frozen file')
        require(path.is_file() and path.stat().st_size<=25*1024*1024 and sha256(path)==expected,'Frozen source/gold hash mismatch: '+name)
    core={k:v for k,v in frozen['files'].items() if k!='reviewer/answers-template.json'}
    require(digest(core)==frozen['suite_sha256'],'Suite identity differs from frozen files')
    manifest=read_json(root/'operator/suite.json');gold=read_json(root/'operator/gold.json');task=read_json(root/'reviewer/task.json')
    require(manifest['schema_version']==1 and len(manifest['cases'])==8 and manifest['model_evaluation']=='not_performed' and manifest['label_validation']=='authored_not_human_verified','Invalid control manifest')
    ids=[c['id'] for c in manifest['cases']]
    require(len(set(ids))==8 and set(ids)==set(gold),'Control/gold case sets differ')
    require(set(task)=={'schema_version','brief','cases'} and task['schema_version']==1 and isinstance(task['brief'],str) and task['brief'].strip() and task['cases']==manifest['cases'],'Reviewer task differs from frozen cases')
    expected={'operator/suite.json','operator/gold.json','operator/generator.py','operator/encoded-qa.json','operator/perturbation-qa.json','reviewer/task.json','reviewer/answers-template.json'}
    for c in manifest['cases']:
        require(re.fullmatch('c_[0-9a-f]{12}',c['id']) and c['file']==c['id']+'.mp4','Unsafe control ID/name')
        name='reviewer/'+c['file'];expected.add(name)
        require(frozen['files'].get(name)==c['sha256'] and 9.9<=c['duration_seconds']<=10.1,'Control pin/duration mismatch')
    require(set(frozen['files'])==expected,'Unexpected or missing frozen sources')
    actual={str(p.relative_to(root)) for p in (root/'reviewer').rglob('*') if p.is_file() or p.is_symlink()}
    require(actual=={name for name in expected if name.startswith('reviewer/')},'Unexpected file in label-blinded reviewer packet')
    require({g['recipe'] for g in gold.values()}=={r[0] for r in recipes()},'Gold recipe set differs')
    for g in gold.values():
        require(isinstance(g['events'],list) and len(g['events'])<=4,'Invalid gold events')
        for e in g['events']:
            require(set(e)=={'category','kind','start','end'} and e['category'] in CATEGORIES and e['kind']==CATEGORIES[e['category']] and number(e['start']) and number(e['end']) and 0<=e['start']<e['end']<=SECONDS,'Invalid gold event')
    require(frozen['files'].get('operator/generator.py')==manifest['generator_sha256'],'Generator snapshot differs from manifest')
    template=read_json(root/'reviewer/answers-template.json')
    require(template['suite_sha256']==frozen['suite_sha256'],'Answer template has a different suite identity')
    return manifest,gold,task,frozen


def supported(kind,method):
    return method in {'audio_video','video','frames'} if kind=='visual' else method in {'audio_video','audio'} if kind=='listening' else method=='audio_video' if kind=='sync' else method in {'audio_video','video'}


def load_answers(root,path):
    manifest,gold,task,frozen=verify(root)
    path=Path(path).resolve(strict=True);require(path.is_file() and path.stat().st_size<=8*1024*1024,'Use a regular answers JSON up to 8 MiB')
    answer_pin=sha256(path);answers=read_json(path,answer_pin)
    require(isinstance(answers,dict) and set(answers)=={'schema_version','suite_sha256','reviewer','cases'} and type(answers['schema_version']) is int and answers['schema_version']==1,'Invalid answer fields/schema')
    require(answers['suite_sha256']==frozen['suite_sha256'],'Answers refer to a different frozen suite')
    who=answers['reviewer']
    require(isinstance(who,dict) and set(who)=={'actor','version','run_kind'} and who['run_kind'] in {'not_run','synthetic_control','human','model'},'Explicit reviewer/run kind required')
    require(all(isinstance(who[k],str) and 0<len(who[k].strip())<=512 for k in ['actor','version']),'Explicit reviewer/version required')
    if who['run_kind']!='not_run':require(all(who[k]!='not_recorded' for k in ['actor','version']),'Record the actual reviewer/version')
    rows=answers['cases'];sources={c['id']:c for c in manifest['cases']}
    require(isinstance(rows,list) and len(rows)==len(sources),'Answers must cover the complete frozen case set; use unknown for unavailable checks')
    seen=set()
    for row in rows:
        require(isinstance(row,dict) and set(row)=={'id','source_sha256','method','coverage_type','sampled_fps','coverage','checks','findings'},'Invalid answer case fields')
        identity=row['id'];require(isinstance(identity,str) and identity in sources and identity not in seen,'Duplicate or unknown answer case')
        seen.add(identity);duration=sources[identity]['duration_seconds']
        require(row['source_sha256']==sources[identity]['sha256'],'Answer source revision differs')
        require(row['method'] in {'audio_video','video','audio','frames','transcript'} and row['coverage_type'] in {'continuous','sampled'},'Record actual input method and coverage type')
        require(row['sampled_fps'] is None or (number(row['sampled_fps']) and 0<row['sampled_fps']<=240),'Invalid sampled fps')
        require(row['coverage_type']!='continuous' or row['sampled_fps'] is None,'Continuous coverage cannot also declare a sampled fps')
        require(row['method'] not in {'frames','transcript'} or row['coverage_type']=='sampled','Frames/transcripts are not continuous audiovisual review')
        require(isinstance(row['coverage'],list) and len(row['coverage'])<=100,'Invalid coverage intervals')
        for span in row['coverage']:
            require(isinstance(span,list) and len(span)==2 and all(number(v) for v in span) and 0<=span[0]<span[1]<=duration,'Coverage outside encoded clip')
        checks=row['checks'];require(isinstance(checks,dict) and set(checks)==set(SCOPES) and all(v in {'pass','fail','unknown'} for v in checks.values()),'Use explicit pass/fail/unknown for all checks')
        findings=row['findings'];require(isinstance(findings,list) and len(findings)<=100,'Invalid findings')
        for f in findings:
            require(isinstance(f,dict) and set(f)=={'category','start','end','note'} and f['category'] in CATEGORIES,'Unknown finding category/fields')
            require(number(f['start']) and number(f['end']) and 0<=f['start']<f['end']<=duration,'Finding timestamps outside clip')
            require(any(a<=f['start']<f['end']<=b for a,b in row['coverage']),'Finding outside actually reviewed coverage')
            require(isinstance(f['note'],str) and 0<len(f['note'].strip())<=4096,'Finding needs observed evidence')
            require(checks[CATEGORIES[f['category']]]!='pass','A finding cannot contradict a passed check')
        for kind,result in checks.items():
            require(result!='fail' or any(CATEGORIES[f['category']]==kind for f in findings),'A failed check needs a timestamped finding')
        if who['run_kind']=='not_run':require(not row['coverage'] and not findings and all(v=='unknown' for v in checks.values()),'Unrun template cannot claim observations')
    return manifest,gold,frozen,answers,answer_pin


def effective_checks(row,duration):
    result={}
    for kind,status in row['checks'].items():
        sufficient=(supported(kind,row['method']) and row['coverage_type']=='continuous' and row['method'] not in {'frames','transcript'} and MEDIA['full_coverage'](row['coverage'],duration))
        result[kind]=status if (status=='fail' and supported(kind,row['method'])) or sufficient else 'unknown'
    return result


def event_covered(label,coverage):
    start,end=label['start'],label['end']
    spans=[[max(start,a)-start,min(end,b)-start] for a,b in coverage if min(end,b)>max(start,a)]
    return MEDIA['full_coverage'](spans,end-start)


def match_event(finding,label):
    if finding['category']!=label['category']:return False
    overlap=max(0,min(finding['end'],label['end'])-max(finding['start'],label['start']))
    if finding['category']=='unreadable_text':return overlap>0
    union=max(finding['end'],label['end'])-min(finding['start'],label['start'])
    return abs(finding['start']-label['start'])<=.5 and overlap/union>=.25


def score(root,path):
    manifest,gold,frozen,answers,answer_pin=load_answers(root,path);sources={c['id']:c for c in manifest['cases']}
    counts=dict(true_positive=0,false_positive=0,false_negative=0,unassessed_events=0,
                false_pass_cases=0,false_alarm_cases=0,clean_correct_cases=0,sufficient_cases=0,total_cases=len(sources),total_gold_events=0)
    cases=[]
    for row in answers['cases']:
        labels=gold[row['id']]['events'];counts['total_gold_events']+=len(labels)
        effective=effective_checks(row,sources[row['id']]['duration_seconds'])
        findings=[f for f in row['findings'] if supported(CATEGORIES[f['category']],row['method'])]
        edges={i:[j for j,label in enumerate(labels) if match_event(f,label)] for i,f in enumerate(findings)}
        matched={}
        def assign(i,seen):
            for j in edges[i]:
                if j in seen:continue
                seen.add(j)
                if j not in matched or assign(matched[j],seen):matched[j]=i;return True
            return False
        for i in edges:assign(i,set())
        missed=[label for j,label in enumerate(labels) if j not in matched]
        fn_labels=[label for label in missed if effective[label['kind']]!='unknown' and event_covered(label,row['coverage'])]
        unassessed_labels=[label for label in missed if label not in fn_labels]
        fn=len(fn_labels);unassessed=len(unassessed_labels)
        fp=len(findings)-len(matched);sufficient=all(v!='unknown' for v in effective.values())
        false_pass=bool(labels) and all(v=='pass' for v in effective.values())
        false_alarm=not labels and bool(fp)
        clean_correct=not labels and all(v=='pass' for v in effective.values())
        for key,value in [('true_positive',len(matched)),('false_positive',fp),('false_negative',fn),('unassessed_events',unassessed),
                          ('false_pass_cases',int(false_pass)),('false_alarm_cases',int(false_alarm)),('clean_correct_cases',int(clean_correct)),('sufficient_cases',int(sufficient))]:counts[key]+=value
        cases.append({'id':row['id'],'effective_checks':effective,'true_positive':len(matched),'false_positive':fp,'false_negative':fn,
                      'unassessed_events':unassessed,'false_pass':false_pass,'false_alarm':bool(false_alarm),'sufficient':sufficient,
                      'unsupported_findings':len(row['findings'])-len(findings),
                      'matched':[{'expected':labels[j],'observed':findings[i]} for j,i in sorted(matched.items())],
                      'missed':fn_labels,
                      'unassessed':unassessed_labels,
                      'unmatched_findings':[f for i,f in enumerate(findings) if i not in matched.values()]})
    precision=counts['true_positive']/(counts['true_positive']+counts['false_positive']) if counts['true_positive']+counts['false_positive'] else None
    return {'schema_version':1,'suite_sha256':frozen['suite_sha256'],'answers_sha256':answer_pin,'scorer_sha256':sha256(Path(__file__)),
            'reviewer':answers['reviewer'],'attestation':'supplied_answers_not_independently_verified_input_delivery',
            'model_evaluation':'supplied_model_answers' if answers['reviewer']['run_kind']=='model' else 'not_performed',
            'label_validation':manifest['label_validation'],'qualification':'diagnostic_only','publication_authorized':False,
            'counts':counts,'precision':precision,'recall_all_authored_events':counts['true_positive']/counts['total_gold_events'] if counts['total_gold_events'] else None,
            'matching_rule':{'transient_start_tolerance_seconds':.5,'minimum_temporal_iou':.25,'persistent_category_any_overlap':['unreadable_text'],'assignment':'one_to_one'},
            'cases':cases,'limits':['Authored labels await independent human validation, particularly normal-size text readability.',
                                   'Label-blinded packet only; public recipes are not an unseen/causal benchmark.',
                                   'Tones/graphics do not qualify natural footage, speech, languages or general creative judgment.',
                                   'Abstentions and insufficient modality/coverage never become correct passes.']}


def observations(root,path,identity):
    manifest,gold,frozen,answers,answer_pin=load_answers(root,path)
    require(answers['reviewer']['run_kind']!='not_run','No actual review in the template')
    row=next((c for c in answers['cases'] if c['id']==identity),None);require(row is not None,'Unknown case')
    source=next(c for c in manifest['cases'] if c['id']==identity);effective=effective_checks(row,source['duration_seconds'])
    reviews=[]
    for kind in SCOPES:
        if not supported(kind,row['method']) or row['method'] not in MEDIA['METHODS'][kind]:continue
        result={'pass':'accepted','fail':'rejected','unknown':'pending'}[effective[kind]]
        findings=[{'start':f['start'],'end':f['end'],'severity':'error','note':f['category']+': '+f['note'],
                   'action':'Inspect and correct this interval before accepting the clip.','reshoot':False}
                  for f in row['findings'] if CATEGORIES[f['category']]==kind]
        reviews.append({'kind':kind,'actor':answers['reviewer']['actor'],'reviewer_version':answers['reviewer']['version'],
                        'provenance':'supplied_report','method':row['method'],'coverage_type':row['coverage_type'],'coverage':row['coverage'],
                        'sampled_fps':row['sampled_fps'],'result':result,'findings':findings})
    return {'source_sha256':row['source_sha256'],'reviews':reviews}


def markdown(result):
    cell=runpy.run_path(str(BASE/'packet.py'))['cell']
    lines=['# Video perception control results','', 'Qualification: diagnostic only. Authored labels await independent human verification.',
           'Reviewer: '+cell(result['reviewer']['actor']+' / '+result['reviewer']['version']),
           'Model evaluation: '+cell(result['model_evaluation']),'', '| Measure | Count |','| --- | --- |']
    lines+=['| '+cell(k)+' | '+str(v)+' |' for k,v in result['counts'].items()]
    lines+=['', '| Case | TP | FP | FN | Unassessed events | False pass | Sufficient coverage/modality |','| --- | --- | --- | --- | --- | --- | --- |']
    for c in result['cases']:lines.append('| '+' | '.join(cell(c[k]) for k in ['id','true_positive','false_positive','false_negative','unassessed_events','false_pass','sufficient'])+' |')
    lines+=['']+['- '+cell(limit) for limit in result['limits']]+['']
    return '\n'.join(lines)


def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    make=sub.add_parser('build');make.add_argument('output',type=Path);make.add_argument('--seed',type=int)
    check=sub.add_parser('verify');check.add_argument('suite',type=Path)
    for command in ['score','observations']:
        grade=sub.add_parser(command);grade.add_argument('suite',type=Path);grade.add_argument('answers',type=Path)
        if command=='score':grade.add_argument('--format',choices=['json','markdown'],default='json')
        else:grade.add_argument('--case',required=True)
    args=parser.parse_args()
    try:
        if args.command=='build':result=build(args.output,args.seed)
        elif args.command=='score':result=score(args.suite,args.answers)
        elif args.command=='observations':result=observations(args.suite,args.answers,args.case)
        else:
            manifest,gold,task,frozen=verify(args.suite)
            result={'status':'frozen_bytes_verified','clips':len(manifest['cases']),'suite_sha256':frozen['suite_sha256'],'model_evaluation':'not_performed','label_validation':manifest['label_validation']}
        if args.command=='score' and args.format=='markdown':print(markdown(result),end='')
        else:print(json.dumps(result,indent=2,allow_nan=False))
    except (OSError,ValueError,TypeError,KeyError,RecursionError,subprocess.SubprocessError) as exc:parser.exit(2,str(exc)+'\n')


if __name__=='__main__':main()
