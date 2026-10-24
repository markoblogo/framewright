"""Revision-bound manual observations. No decoding, network or execution authority."""
import copy
from datetime import datetime, timezone
import hashlib
import json
from urllib.parse import urlsplit

RESULTS = {
    'technical': {'pass', 'fail', 'pending'},
    'listening': {'accepted', 'rejected', 'pending'},
    'creative': {'accepted', 'rejected', 'pending'},
    'decision': {'accepted', 'rejected', 'deferred', 'proposed'},
    'publication': {'published', 'removed', 'pending'},
    'provider': {'approved', 'rejected', 'pending'},
    'metrics': {'recorded'},
}
PROVENANCE = {'owner_report', 'operator_observation', 'supplied_report', 'independent_check', 'administrative_change'}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True).encode()).hexdigest()


def pin(data, subject):
    if subject == 'project':
        return None
    kind, sep, identity = subject.partition(':')
    if sep and kind == 'input' and identity in data['inputs']:
        row = data['inputs'][identity]
    elif sep and kind == 'output' and identity in data['artifacts']:
        row = data['artifacts'][identity]['file']
    else:
        raise ValueError('Unknown observation subject; use project or input:/output: ID')
    if row is None:
        raise ValueError('Retain the subject file before recording an observation')
    return copy.deepcopy(row)


def validate(data):
    rows = data['journal']
    if not isinstance(rows, list) or data.get('journal_sha256') != digest(rows):
        raise ValueError('Journal integrity mismatch; preserve the checkpoint and original receipts')
    for index, row in enumerate(rows, 1):
        if (row['id'] != f'e{index:06d}' or row['kind'] not in RESULTS or
                row['result'] not in RESULTS[row['kind']] or row['provenance'] not in PROVENANCE):
            raise ValueError('Invalid journal identity, kind, result or provenance')
        if not all(isinstance(row[k], str) and row[k].strip() for k in ['subject','topic','actor','note','recorded_at']):
            raise ValueError('Incomplete journal observation')
        if row['subject'] != 'project' and row['subject'] not in row['pins']:
            raise ValueError('Observation lacks its artifact revision')


def append(data, subject, kind, result, actor, provenance, note, topic=None,
           dependencies=(), url=None, visibility=None, observed_at=None):
    if topic is not None and not topic.strip():
        raise ValueError('Observation topic must be nonempty when supplied')
    if kind not in RESULTS or result not in RESULTS[kind]:
        raise ValueError('Result does not belong to the selected observation kind')
    if provenance not in PROVENANCE or not actor.strip() or not note.strip():
        raise ValueError('Explicit actor, provenance and nonempty note are required')
    if kind=='decision' and (not topic or not topic.strip()):
        raise ValueError('Decisions require an explicit topic')
    if subject == 'project' and kind != 'decision':
        raise ValueError('Only decisions may be project-wide; bind checks/publication to a retained file')
    if url:
        parsed = urlsplit(url)
        if parsed.scheme not in {'http','https'} or not parsed.hostname or parsed.username or parsed.password:
            raise ValueError('Use an HTTP(S) publication URL without embedded credentials')
    if kind == 'publication':
        if not url or (result == 'published' and visibility not in {'public','unlisted','private','unknown'}):
            raise ValueError('Publication requires URL and published observations require explicit visibility')
        if result == 'removed' and not any(r['kind']=='publication' and r['result']=='published' and
                r['subject']==subject and r.get('url')==url and
                r['pins'].get(subject)==pin(data,subject) for r in data['journal']):
            raise ValueError('Record publication of this exact retained revision before its removal')
        topic = url  # Different uploads must not silently replace one another.
    elif url or visibility:
        raise ValueError('URL/visibility belong only to publication observations')
    if observed_at:
        when = datetime.fromisoformat(observed_at)
        if when.tzinfo is None:raise ValueError('Observation time must include a timezone')
        observed_at = when.isoformat()
    pins = {}
    for identity in dict.fromkeys([subject, *dependencies]):
        record = pin(data, identity)
        if record is not None:pins[identity] = record
    row = {'id': f"e{len(data['journal'])+1:06d}", 'subject': subject, 'kind': kind,
           'result': result, 'topic': topic or kind, 'actor': actor, 'provenance': provenance,
           'note': note, 'observed_at': observed_at, 'recorded_at': datetime.now(timezone.utc).isoformat(),
           'pins': pins, 'attestation': 'manual_record_not_independently_verified_by_cli'}
    if subject=='project':row['project_sha256']=digest(data['project'])
    if url:row.update(url=url,visibility=visibility or 'unknown')
    data['journal'].append(row)
    return row


def project(data, problems):
    rows = data.get('journal', [])
    latest = {(r['subject'],r['kind'],r['topic']):r['id'] for r in rows}
    current, stale, superseded = [], [], []
    for row in rows:
        reasons = []
        if row.get('project_sha256') and row['project_sha256']!=digest(data['project']):
            reasons.append('project goal/context changed')
        for subject, recorded in row['pins'].items():
            try:
                if pin(data, subject) != recorded:reasons.append(subject + ': retained revision changed')
            except ValueError:
                reasons.append(subject + ': no current retained revision')
            if subject in problems:reasons.append(subject + ': ' + problems[subject])
        item = {**row, 'stale_reasons': reasons}
        if reasons:stale.append(item)
        elif row['id'] == latest[(row['subject'],row['kind'],row['topic'])]:current.append(item)
        else:superseded.append(item)
    return {'effective': current, 'stale': stale, 'superseded': superseded,
            'note': 'Latest recorded observation per subject/kind/topic; no fact or authority inferred. Stale latest entries never resurrect older approvals.'}
