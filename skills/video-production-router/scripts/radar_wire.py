"""radar-framewright/v1 wire protocol. Stdlib, local explicit delivery only.

Identical vendored protocol is shipped by each independent receiver. Hashes detect
corruption; producer authentication relies on owner-controlled local directories.
"""
import copy
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
from contextlib import contextmanager
from datetime import datetime

VERSION='radar-framewright/v1'
LIMIT=1024*1024
ROLES={'radar','framewright'}
KINDS={'idea_menu','association','production_status','analytics_snapshot','receipt'}
HEX=re.compile(r'[0-9a-f]{64}')
KEY=re.compile(r'[A-Za-z0-9][A-Za-z0-9:_.-]{0,159}')


def canonical(value):
    return json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode('utf-8')


def digest(value):return hashlib.sha256(canonical(value)).hexdigest()


def timestamp(value):
    t=datetime.fromisoformat(value.replace('Z','+00:00'))
    if t.tzinfo is None:raise ValueError('Timezone required')
    return t


def message(kind,producer,entity,revision,sequence,occurred,payload):
    row=dict(schema_version=VERSION,kind=kind,producer=producer,entity_key=entity,
             source_revision={'sha256':revision,'sequence':sequence},occurred_at=occurred,
             payload=payload,payload_sha256=digest(payload))
    row['message_id']=digest({k:row[k] for k in ['schema_version','kind','producer','entity_key','source_revision','payload_sha256']})
    validate(row);return row


def validate(row):
    fields={'schema_version','kind','producer','entity_key','source_revision','occurred_at','payload','payload_sha256','message_id'}
    if not isinstance(row,dict) or set(row)!=fields or row['schema_version']!=VERSION:raise ValueError('Unknown schema/fields')
    if row['kind'] not in KINDS or row['producer'] not in ROLES or not KEY.fullmatch(row['entity_key']):raise ValueError('Invalid kind/producer/entity')
    rev=row['source_revision']
    if not isinstance(rev,dict) or set(rev)!={'sha256','sequence'} or not HEX.fullmatch(rev['sha256']) or type(rev['sequence']) is not int or rev['sequence']<0:raise ValueError('Invalid revision')
    timestamp(row['occurred_at'])
    if not isinstance(row['payload'],dict) or len(canonical(row))>LIMIT:raise ValueError('Invalid payload/size')
    if row['payload_sha256']!=digest(row['payload']):raise ValueError('Payload hash mismatch')
    expected=digest({k:row[k] for k in ['schema_version','kind','producer','entity_key','source_revision','payload_sha256']})
    if row['message_id']!=expected:raise ValueError('Message ID mismatch')
    return row


def read(path):
    p=Path(path)
    if p.is_symlink() or not p.is_file() or p.stat().st_size>LIMIT:raise ValueError('Unsafe/missing/oversized JSON file')
    raw=p.read_bytes()
    if len(raw)>LIMIT:raise ValueError('Oversized JSON')
    return json.loads(raw,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('Nonfinite JSON')))


def directory(root,role):
    root=Path(root).absolute()
    if role not in ROLES or not root.is_dir():raise ValueError('Exchange root unavailable; no fallback created')
    if any(p.is_symlink() for p in [root,*root.parents]):raise ValueError('Symlink exchange root')
    p=root/role
    if p.is_symlink():raise ValueError('Symlink role directory')
    p.mkdir(mode=0o700,exist_ok=True)
    for name in ['outbox','receipts']:
        q=p/name
        if q.is_symlink():raise ValueError('Symlink exchange directory')
        q.mkdir(mode=0o700,exist_ok=True)
    return p


def atomic(path,value,immutable=False):
    path=Path(path)
    if path.is_symlink():raise ValueError('Symlink output')
    body=canonical(value)+b'\n'
    if len(body)>LIMIT:raise ValueError('Local exchange state capacity exceeded; no partial write')
    if immutable and path.exists():
        if path.read_bytes()!=body:raise ValueError('Immutable record conflict')
        return
    temp=None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent,prefix='.write-',delete=False) as f:
            temp=Path(f.name);os.chmod(temp,0o600);f.write(body);f.flush();os.fsync(f.fileno())
        if immutable:
            try:os.link(temp,path)
            except FileExistsError:
                if path.read_bytes()!=body:raise ValueError('Immutable record conflict')
        else:os.replace(temp,path)
        fd=os.open(path.parent,os.O_RDONLY)
        try:os.fsync(fd)
        finally:os.close(fd)
    finally:
        if temp is not None:temp.unlink(missing_ok=True)


@contextmanager
def locked(folder):
    fd=os.open(folder/'exchange.lock',os.O_CREAT|os.O_RDWR|getattr(os,'O_NOFOLLOW',0),0o600)
    with os.fdopen(fd,'a') as f:
        fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB);yield


def state(root,role):
    root=Path(root).absolute()
    if role not in ROLES or not root.is_dir() or any(p.is_symlink() for p in [root,*root.parents]):raise ValueError('Exchange root unavailable/unsafe')
    folder=root/role
    if folder.is_symlink():raise ValueError('Unsafe role directory')
    p=folder/'state.json'
    return read(p) if p.exists() else {'version':VERSION,'processed':{},'data':{},'acks':{}}


def publish(root,role,row):
    validate(row)
    if row['producer']!=role:raise ValueError('Producer differs from owned outbox')
    p=directory(root,role)/'outbox'/(row['message_id']+'.json')
    atomic(p,row,immutable=True);return p


def receive(root,role,row,apply):
    """Persist application+processed marker together, then ack; retry cannot reapply.

    Pending/rejected handlers operate on a copy and cannot partly mutate data.
    Receipt delivery stores acknowledgement only and never acknowledges a receipt.
    """
    folder=directory(root,role)
    try:
        validate(row)
        if row['producer']==role:raise ValueError('Wrong sender')
    except (ValueError,TypeError,KeyError,RecursionError) as e:
        return {'result':'rejected','reason':str(e),'message_id':row.get('message_id') if isinstance(row,dict) else None}
    with locked(folder):
        saved=state(root,role);identity=row['message_id'];kind=row['kind'];payload=row['payload']
        if kind=='receipt':
            if set(payload)!={'message_id','result','reason'} or not isinstance(payload['message_id'],str) or not HEX.fullmatch(payload['message_id']) or payload['result'] not in {'applied','duplicate','pending','rejected'} or not isinstance(payload['reason'],str):raise ValueError('Invalid receipt')
            if not (folder/'outbox'/(payload['message_id']+'.json')).is_file():return {'result':'pending','reason':'Unknown outbound message','message_id':identity}
            saved['acks'][identity]=copy.deepcopy(row);atomic(folder/'state.json',saved)
            return {'result':'applied','reason':'Acknowledgement stored; no reply','message_id':identity}
        if identity in saved['processed']:
            result,reason='duplicate','Previously committed'
        else:
            candidate=copy.deepcopy(saved['data'])
            try:result,reason=apply(candidate,row)
            except (ValueError,KeyError,TypeError) as e:result,reason='rejected',str(e)
            if result not in {'applied','pending','rejected'}:raise ValueError('Invalid receiver result')
            if result=='applied':
                saved['data']=candidate;saved['processed'][identity]={'kind':kind,'revision':row['source_revision'],'occurred_at':row['occurred_at']}
                atomic(folder/'state.json',saved)
        outcome={'message_id':identity,'result':result,'reason':reason}
        # Stable acknowledgement for the same result; original event timestamp retained.
        ack=message('receipt',role,'ack:'+identity,digest(outcome),0,row['occurred_at'],outcome)
        atomic(folder/'receipts'/(ack['message_id']+'.json'),ack,immutable=True)
        publish(root,role,ack)
        return outcome


def fields(obj,required,optional=()):
    if not isinstance(obj,dict) or not set(required)<=set(obj) or set(obj)-set(required)-set(optional):raise ValueError('Invalid payload fields')


def key(value):
    if not isinstance(value,str) or not KEY.fullmatch(value):raise ValueError('Invalid identity')
    return value


def sha(value):
    if not isinstance(value,str) or not HEX.fullmatch(value):raise ValueError('Invalid hash')
    return value


def text(value):
    if not isinstance(value,str) or not value.strip() or len(value)>8000:raise ValueError('Invalid text')


def url(value):
    from urllib.parse import urlsplit
    p=urlsplit(value)
    if p.scheme not in {'http','https'} or not p.hostname or p.username or p.password:raise ValueError('Invalid URL')


def menu_payload(p):
    from datetime import date
    fields(p,{'packet_sha256','as_of','ideas'});sha(p['packet_sha256']);date.fromisoformat(p['as_of'])
    if not isinstance(p['ideas'],list) or len(p['ideas'])>100:raise ValueError('Invalid menu size')
    seen=set()
    for idea in p['ideas']:
        fields(idea,{'id','title','question','hypothesis','format','sources','constraints'})
        key(idea['id'])
        if idea['id'] in seen:raise ValueError('Duplicate idea')
        seen.add(idea['id'])
        for k in ['title','question','hypothesis','format']:text(idea[k])
        if not isinstance(idea['sources'],list) or not isinstance(idea['constraints'],list):raise ValueError('Invalid source/constraints')
        for source in idea['sources']:
            fields(source,{'url','checked_at','supports'});url(source['url']);timestamp(source['checked_at']);text(source['supports'])
        for c in idea['constraints']:text(c)
    return p


def association_payload(p):
    fields(p,{'project_id','radar_idea_id','research_revision','idea_sha256','selected_at','link_mode','owner_approval','timing_basis'})
    key(p['project_id']);key(p['radar_idea_id']);sha(p['research_revision']);sha(p['idea_sha256']);timestamp(p['selected_at']);text(p['timing_basis'])
    if p['owner_approval'] is not True or p['link_mode'] not in {'retrospective_observation','prospective_hypothesis'}:raise ValueError('Owner-approved link mode required')
    return p


def status_payload(p):
    fields(p,{'project_id','radar_idea_id','research_revision','source_journal_sha256','status','outputs','publications'})
    key(p['project_id']);key(p['radar_idea_id']);sha(p['research_revision']);sha(p['source_journal_sha256'])
    if p['status'] not in {'selected','started','blocked','ready_for_review','accepted','published'}:raise ValueError('Invalid production status')
    if not isinstance(p['outputs'],list) or not isinstance(p['publications'],list):raise ValueError('Invalid production lists')
    for output in p['outputs']:
        fields(output,{'id','sha256','bytes','accepted'});key(output['id']);sha(output['sha256'])
        if type(output['bytes']) is not int or output['bytes']<0 or type(output['accepted']) is not bool:raise ValueError('Invalid output')
    for publication in p['publications']:
        fields(publication,{'platform','video_id','url','output_id','receipt_id','provenance','recorded_at','master_sha256'})
        if publication['platform']!='youtube' or not re.fullmatch(r'[A-Za-z0-9_-]{11}',publication['video_id']):raise ValueError('Only YouTube publications supported in v1')
        from urllib.parse import urlsplit,parse_qs
        parsed=urlsplit(publication['url'])
        actual=(parsed.path.strip('/') if parsed.hostname in {'youtu.be','www.youtu.be'} else parse_qs(parsed.query).get('v',[''])[0] if parsed.hostname in {'youtube.com','www.youtube.com','m.youtube.com'} and parsed.path=='/watch' else None)
        if actual!=publication['video_id']:raise ValueError('Publication URL/video identity mismatch')
        url(publication['url']);key(publication['output_id']);key(publication['receipt_id']);sha(publication['master_sha256']);timestamp(publication['recorded_at'])
        if publication['provenance'] not in {'owner_report','operator_observation','supplied_report','independent_check'}:raise ValueError('Invalid publication provenance')
        if not any(o['id']==publication['output_id'] and o['sha256']==publication['master_sha256'] for o in p['outputs']):raise ValueError('Publication/output mismatch')
    if p['status']=='published' and not p['publications']:raise ValueError('Published requires receipt')
    return p


def analytics_payload(p):
    import math
    from datetime import date
    from zoneinfo import ZoneInfo
    fields(p,{'project_id','video_id','channel_id','as_of','published_at','period_start','period_end','timezone','window','availability','metrics','currency','source_sha256','source_kind','report_label'})
    key(p['project_id']);sha(p['source_sha256']);timestamp(p['as_of']);timestamp(p['published_at']);ZoneInfo(p['timezone'])
    if not re.fullmatch(r'[A-Za-z0-9_-]{11}',p['video_id']) or not re.fullmatch(r'UC[A-Za-z0-9_-]{22}',p['channel_id']):raise ValueError('Invalid video/channel')
    a,z=map(date.fromisoformat,[p['period_start'],p['period_end']])
    if not a<=z<=timestamp(p['as_of']).date() or timestamp(p['as_of'])<timestamp(p['published_at']):raise ValueError('Invalid analytics period')
    if p['window']!='calendar_report' or p['source_kind'] not in {'retained_youtube_api','synthetic_fixture'} or p['availability'] not in {'REPORTED','NOT_AVAILABLE','ACCESS_FAILED','AUTH_REQUIRED'}:raise ValueError('Invalid observation source/status')
    allowed={'views','average_view_duration_seconds','average_percentage_viewed','impressions_ctr_percent','estimated_revenue'}
    if not isinstance(p['metrics'],dict) or set(p['metrics'])!=allowed:raise ValueError('Explicit nullable metrics required')
    for k,v in p['metrics'].items():
        if v is not None and (type(v) not in (int,float) or not math.isfinite(v) or v<0 or k=='views' and type(v) is not int or k=='impressions_ctr_percent' and v>100):raise ValueError('Invalid metric')
    if p['availability']!='REPORTED' and any(v is not None for v in p['metrics'].values()):raise ValueError('Unavailable metrics must be null')
    if p['currency'] is not None and not re.fullmatch(r'[A-Z]{3}',p['currency']):raise ValueError('Invalid currency')
    if p['metrics']['estimated_revenue'] is not None and p['currency'] is None:raise ValueError('Revenue needs currency, including zero')
    text(p['report_label']);return p


def drain(root,role,apply):
    """Bounded pull from the peer outbox; never write peer state or directories."""
    state(root,role)  # validates existing root even with no messages
    peer='radar' if role=='framewright' else 'framewright'
    folder=Path(root)/peer/'outbox'
    if folder.is_symlink() or (Path(root)/peer).is_symlink():raise ValueError('Unsafe peer directory')
    if not folder.exists():return []
    paths=sorted(folder.glob('*.json'))
    if len(paths)>250:raise ValueError('Outbox rotation required; bounded pull limit exceeded')
    rows=[];outcomes=[]
    for path in paths:
        try:
            row=read(path);validate(row)
            if path.stem!=row['message_id'] or row['producer']!=peer:raise ValueError('Outbox identity mismatch')
            rows.append(row)
        except (OSError,ValueError,TypeError,KeyError):outcomes.append({'result':'rejected','reason':'Invalid peer message'})
    order={'idea_menu':0,'association':0,'production_status':1,'analytics_snapshot':2,'receipt':3}
    for row in sorted(rows,key=lambda r:(order[r['kind']],r['source_revision']['sequence'],r['message_id'])):
        outcomes.append(receive(root,role,row,apply))
    return outcomes
