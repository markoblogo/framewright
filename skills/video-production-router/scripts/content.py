"""Project-local content hypotheses and supplied outcome snapshots. No analytics access."""
import copy
from datetime import datetime
import math
import re


def validate_stored(data, digest):
    c=data.get('content')
    if c is None:return
    if c.get('schema_version')!=1 or data.get('content_sha256')!=digest(c):raise ValueError('Content record integrity mismatch')
    receipts={r['id']:r for r in data['journal']}
    ids=set()
    for h in c['hypotheses']:
        if h['id'] in ids or h['receipt'] not in receipts:raise ValueError('Invalid hypothesis identity/receipt')
        ids.add(h['id'])
    seen=set()
    for s in c['snapshots']:
        if s['id'] in seen or s['hypothesis'] not in ids or s['receipt'] not in receipts or s['publication'] not in receipts:raise ValueError('Invalid outcome identity/receipt')
        seen.add(s['id'])


def storage(data):
    return data.setdefault('content',{'schema_version':1,'hypotheses':[],'snapshots':[]})


def text(v,name):
    if not isinstance(v,str) or not v.strip():raise ValueError('Nonempty '+name+' required')
    return v


def identity(v):
    if not isinstance(v,str) or not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_.:-]{0,100}',v):raise ValueError('Use a stable content ID')
    return v


def current_pin(data,subject,journal,problems):
    if not isinstance(subject,str) or not subject.startswith(('input:','output:')):raise ValueError('Evidence requires a retained input:/output: ID')
    pin=journal['pin'](data,subject)
    if pin is None or subject in problems:raise ValueError('Retain current evidence bytes before recording content')
    return pin


def hypothesis(data,spec,actor,provenance,journal,problems):
    keys={'id','statement','audience','format','target','source'}
    if not isinstance(spec,dict) or set(spec)!=keys:raise ValueError('Hypothesis requires id, statement, audience, format, target and source')
    identity(spec['id'])
    for k in ['statement','audience','format']:text(spec[k],k)
    target=spec['target']
    if not isinstance(target,str) or not target.startswith('output:') or target[7:] not in data['artifacts']:raise ValueError('Declare target output first')
    src=spec['source']
    if not isinstance(src,dict) or set(src)!={'kind','subject'} or src['kind'] not in {'youtube_trends','youtube_radar','owner_idea','other'}:raise ValueError('Explicit hypothesis source kind/subject required')
    current_pin(data,src['subject'],journal,problems)
    c=storage(data)
    for h in c['hypotheses']:
        if h['id']==spec['id']:
            if h['spec']!=spec:raise ValueError('Hypothesis is immutable; use a new ID for a revision')
            return False
    receipt=journal['append'](data,'project','decision','proposed',actor,provenance,
        'Content hypothesis recorded; no creative approval or audience outcome inferred.',
        'content-hypothesis:'+spec['id'],[src['subject']])
    c['hypotheses'].append({'id':spec['id'],'spec':copy.deepcopy(spec),'receipt':receipt['id'],
        'timing':'retrospective' if data['artifacts'][target[7:]]['file'] else 'before_retained_master'})
    return True


def report(data,journal,problems,compare_age=None,tolerance=6):
    if compare_age is not None and (not math.isfinite(compare_age) or compare_age<0):raise ValueError('Comparison age must be finite and nonnegative')
    if not math.isfinite(tolerance) or tolerance<0:raise ValueError('Age tolerance must be finite and nonnegative')
    c=data.get('content',{'hypotheses':[],'snapshots':[]})
    projection=journal['project'](data,problems);stale={r['id'] for r in projection['stale']}
    latest={(r['subject'],r['kind'],r['topic']):r['id'] for r in data['journal']}
    receipts={r['id']:r for r in data['journal']}
    result=[]
    for h in c['hypotheses']:
        pubs=[]
        for p in data['journal']:
            if p['kind']!='publication' or p['result']!='published' or p['subject']!=h['spec']['target']:continue
            current=latest[(p['subject'],p['kind'],p['topic'])]==p['id']
            newer=next(r for r in data['journal'] if r['id']==latest[(p['subject'],p['kind'],p['topic'])])
            state='published' if current else 'removed' if newer['result']=='removed' else 'superseded'
            pubs.append({'receipt':p['id'],'master_sha256':p['pins'][p['subject']]['sha256'],'url':p['url'],'visibility':p['visibility'],'publication_state':state,'stale':p['id'] in stale or not current,
                         'snapshots':[],'metrics_status':'unknown','selected_snapshot':None})
        for pub in pubs:
            candidates=[]
            for snap in c['snapshots']:
                if snap['hypothesis']!=h['id'] or snap['publication']!=pub['receipt']:continue
                spec=snap['spec'];age=None
                if spec.get('published_at'):age=(when(spec['as_of'],'as_of')-when(spec['published_at'],'published_at')).total_seconds()/3600
                is_stale=pub['stale'] or snap['receipt'] in stale or h['receipt'] in stale
                reason='not_requested'
                if compare_age is not None:
                    reason='stale_evidence' if is_stale else 'window_not_lifetime' if spec['window']!='lifetime' else 'upload_time_unknown' if age is None else 'outside_age_tolerance' if abs(age-compare_age)>tolerance else 'eligible'
                receipt=receipts[snap['receipt']]
                evidence=spec['evidence']
                row={'provenance':receipt['provenance'],'recorded_at':receipt['recorded_at'],'evidence_subject':evidence,'evidence_sha256':receipt['pins'][evidence]['sha256'],
                     'period_start':spec.get('period_start'),'period_end':spec.get('period_end'),'id':snap['id'],'receipt':snap['receipt'],'as_of':spec['as_of'],'window':spec['window'],'age_hours':age,'metrics':snap['metrics'],'stale':is_stale,'comparison':reason}
                pub['snapshots'].append(row)
                if reason=='eligible':candidates.append(row)
            if candidates:
                best=min(candidates,key=lambda s:(abs(s['age_hours']-compare_age),s['as_of'],s['id']))
                best['comparison']='selected';pub['selected_snapshot']=best['id']
            if any(not s['stale'] for s in pub['snapshots']):pub['metrics_status']='supplied'
            elif pub['snapshots']:pub['metrics_status']='stale'
        result.append({'source_sha256':receipts[h['receipt']]['pins'][h['spec']['source']['subject']]['sha256'],'recorded_at':receipts[h['receipt']]['recorded_at'],'id':h['id'],**h['spec'],'timing':h['timing'],'stale':h['receipt'] in stale,'publications':pubs})
    return {'schema_version':1,'hypotheses':result,'comparison':{'age_hours':compare_age,'tolerance_hours':tolerance},
            'note':'Supplied observations, not causal attribution or independently verified channel analytics. Unknown metrics are not zero.'}


def markdown(view):
    lines=['# Content hypotheses and outcomes','',view['note'],'']
    for h in view['hypotheses']:
        lines.extend([h['id']+': '+h['statement'],'Timing: '+h['timing']+('; STALE source' if h['stale'] else '')])
        for p in h['publications']:
            lines.append('Publication '+p['receipt']+': '+p['metrics_status'])
            for s in p['snapshots']:lines.append('  '+s['id']+': '+str(s['metrics'])+'; comparison: '+str(s['comparison']))
        if not h['publications']:lines.append('Publication: unknown')
        lines.append('')
    return '\n'.join(lines)


def when(value,name):
    try:t=datetime.fromisoformat(value)
    except (ValueError,TypeError):raise ValueError('Invalid '+name+' timestamp') from None
    if t.tzinfo is None or t.utcoffset() is None:raise ValueError(name+' requires timezone')
    return t


def outcome(data,spec,actor,provenance,journal,problems):
    required={'id','hypothesis','publication','evidence','as_of','window','metrics'}
    optional={'published_at','period_start','period_end'}
    if not isinstance(spec,dict) or not required<=set(spec) or set(spec)-required-optional:raise ValueError('Invalid outcome fields')
    identity(spec['id']);c=storage(data)
    h=next((h for h in c['hypotheses'] if h['id']==spec['hypothesis']),None)
    if h is None:raise ValueError('Unknown hypothesis')
    p=next((r for r in data['journal'] if r['id']==spec['publication']),None)
    if p is None or p['kind']!='publication' or p['result']!='published' or p['subject']!=h['spec']['target']:raise ValueError('Outcome must reference the hypothesis target publication receipt')
    projection=journal['project'](data,problems)
    effective={r['id'] for r in projection['effective']}
    stale={r['id'] for r in projection['stale']}
    if p['id'] not in effective:raise ValueError('Publication is removed, superseded or stale; cannot bind new metrics')
    if h['receipt'] in stale:raise ValueError('Hypothesis source is stale; record a new hypothesis')
    evidence=spec['evidence']
    if evidence==p['subject']:raise ValueError('Metrics require separate retained source evidence')
    current_pin(data,evidence,journal,problems)
    as_of=when(spec['as_of'],'as_of')
    published=when(spec['published_at'],'published_at') if spec.get('published_at') else None
    if published and as_of<published:raise ValueError('Snapshot predates publication')
    for old in c['snapshots']:
        prior=old['spec'].get('published_at')
        if old['publication']==p['id'] and published and prior and when(prior,'published_at')!=published:
            raise ValueError('Conflicting actual upload time; review and record a corrected publication receipt first')
    if spec['window'] not in {'lifetime','period','unknown'}:raise ValueError('Explicit lifetime, period or unknown metric window required')
    if spec['window']=='period':
        start=when(spec.get('period_start'),'period_start');end=when(spec.get('period_end'),'period_end')
        if not start<end<=as_of or (published and start<published):raise ValueError('Invalid snapshot period')
    elif spec.get('period_start') or spec.get('period_end'):raise ValueError('Period bounds require period window')
    raw=spec['metrics']
    numeric={'views','average_view_duration_seconds','average_percentage_viewed','impressions_ctr_percent','estimated_revenue','rpm'}
    if not isinstance(raw,dict) or set(raw)-numeric-{'currency','monetization'}:raise ValueError('Unknown metric fields')
    m={k:raw.get(k) for k in sorted(numeric)}
    for k,v in m.items():
        if v is None:continue
        if type(v) not in (int,float) or not math.isfinite(v) or v<0 or (k=='views' and type(v) is not int) or (k=='impressions_ctr_percent' and v>100):raise ValueError('Invalid metric '+k)
    m['monetization']=raw.get('monetization','unknown')
    if m['monetization'] not in {'unknown','enabled','disabled','not_eligible','not_available'}:raise ValueError('Invalid monetization status')
    m['currency']=raw.get('currency')
    if m['currency'] is not None and (not isinstance(m['currency'],str) or not re.fullmatch('[A-Z]{3}',m['currency'])):raise ValueError('Use explicit three-letter currency')
    if any(m[k] is not None for k in ['estimated_revenue','rpm']) and not m['currency']:raise ValueError('Revenue/RPM including zero require currency')
    for old in c['snapshots']:
        if old['id']==spec['id']:
            if old['spec']!=spec:raise ValueError('Snapshot is immutable; use a new ID')
            return False
    r=journal['append'](data,p['subject'],'metrics','recorded',actor,provenance,
        'Supplied analytics snapshot; no independent platform verification or causal attribution.',
        'content-outcome:'+spec['id'],[evidence,h['spec']['source']['subject']],observed_at=spec['as_of'])
    c['snapshots'].append({'id':spec['id'],'hypothesis':h['id'],'publication':p['id'],'receipt':r['id'],'spec':copy.deepcopy(spec),'metrics':m})
    return True
