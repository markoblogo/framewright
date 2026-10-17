#!/usr/bin/env python3
"""Shared experimental intake for recuts, sourced stories and hybrid films. Offline."""
import argparse
import json
import math
from pathlib import Path
import runpy

BASE = Path(__file__).resolve().parent
SCENARIOS = {'repackaging', 'insight', 'hybrid'}


def positive(value, label, zero=False):
    if type(value) not in (int, float) or not math.isfinite(value) or value < 0 or (not zero and value == 0):
        raise ValueError(f'{label} must be a finite ' + ('nonnegative' if zero else 'positive') + ' number')
    return value


def text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{label} needs nonempty text')
    return value


def rights(value, label, purpose, blockers):
    if not isinstance(value, dict) or value.get('status', 'unknown') not in {'unknown', 'granted', 'noncommercial_only', 'denied'}:
        raise ValueError(f'{label}: invalid rights record')
    status = value.get('status', 'unknown')
    if status in {'granted', 'noncommercial_only'}:
        text(value.get('evidence'), f'{label} rights evidence')
    if status in {'unknown', 'denied'} or (purpose == 'commercial' and status == 'noncommercial_only'):
        blockers.append(f'{label}: {status} rights for {purpose}; owner resolution required')


def assess(spec):
    if not isinstance(spec, dict) or spec.get('scenario') not in SCENARIOS:
        raise ValueError('scenario must be repackaging, insight or hybrid')
    purpose = spec.get('intended_use', 'commercial')
    if purpose not in {'commercial', 'noncommercial', 'private-test'}:
        raise ValueError('Unknown intended_use')
    sources = spec.get('sources')
    if not isinstance(sources, list) or not sources:
        raise ValueError('Declare sources; references are never fetched by this command')
    by_id, publication, production = {}, [], []
    for s in sources:
        if not isinstance(s, dict):
            raise ValueError('Each source must be an object')
        sid = text(s.get('id'), 'Source id')
        if sid in by_id:
            raise ValueError('Duplicate source id')
        by_id[sid] = s
        if s.get('kind') not in {'video', 'audio', 'image', 'text', 'reference'}:
            raise ValueError('Unknown source kind')
        text(s.get('origin'), f'{sid} origin')
        # Provenance describes where; it never grants permission, including own recordings.
        if s['kind'] == 'video':
            rights(s.get('video_rights', {}), sid + ':video', purpose, publication)
            if s.get('audio_policy') not in {'remove', 'replace', 'keep'}:
                raise ValueError('Video needs explicit audio_policy remove, replace or keep')
            if s['audio_policy'] == 'keep':
                rights(s.get('audio_rights', {}), sid + ':audio', purpose, publication)
        else:
            rights(s.get('rights', {}), sid + ':' + s['kind'], purpose, publication)
    kinds = {s['kind'] for s in sources}
    for s in sources:
        records = [s.get('video_rights', {}), s.get('audio_rights', {})] if s['kind'] == 'video' else [s.get('rights', {})]
        if any(r.get('status') == 'denied' for r in records if isinstance(r, dict)):
            # Removed source audio is not reused, so only retained media can block execution.
            retained = [s.get('video_rights', {})] + ([s.get('audio_rights', {})] if s.get('audio_policy') == 'keep' else []) if s['kind'] == 'video' else records
            if any(r.get('status') == 'denied' for r in retained):
                production.append(s['id'] + ': use denied; remove or resolve before execution')
    if spec['scenario'] == 'repackaging' and 'video' not in kinds:
        raise ValueError('Repackaging needs a declared video source')
    if spec['scenario'] == 'insight' and 'text' not in kinds:
        raise ValueError('Insight needs a declared text/article source')
    if spec['scenario'] == 'hybrid' and ('video' not in kinds or not kinds.intersection({'text', 'image'})):
        raise ValueError('Hybrid needs existing video plus text/image for new scenes')
    claims = spec.get('claims', [])
    if not isinstance(claims, list):
        raise ValueError('claims must be a list')
    for c in claims:
        if not isinstance(c, dict) or c.get('source') not in by_id:
            raise ValueError('Each claim must name a declared source')
        text(c.get('text'), 'Claim text')
        text(c.get('locator'), 'Claim source locator')
        if c.get('review', 'pending') not in {'pending', 'verified', 'rejected'}:
            raise ValueError('Unknown claim review')
        if c.get('review', 'pending') != 'verified':
            production.append('fact review: ' + c['text'])
    if spec['scenario'] in {'insight', 'hybrid'} and not claims:
        production.append('retain sourced claims and their human verification before writing factual copy')
    edits = spec.get('edits', [])
    if not isinstance(edits, list):
        raise ValueError('edits must be a list in final playback order')
    total = 0
    for e in edits:
        if not isinstance(e, dict) or e.get('source') not in by_id or by_id[e['source']]['kind'] != 'video':
            raise ValueError('Each edit must reference a declared video')
        start = positive(e.get('in_seconds'), 'in_seconds', zero=True)
        end = positive(e.get('out_seconds'), 'out_seconds')
        if end <= start:
            raise ValueError('Edit end must exceed start')
        if 'duration_seconds' in by_id[e['source']] and end > positive(by_id[e['source']]['duration_seconds'], 'source duration'):
            raise ValueError('Edit exceeds declared source duration')
        text(e.get('reason'), 'Edit selection reason')
        total += end - start
    if 'video' in kinds and not edits:
        production.append('review source duration, scene/transcript evidence and an ordered edit decision list')
    limits = spec.get('limits', {})
    if not isinstance(limits, dict):
        raise ValueError('limits must be an object')
    for k in ['wall_minutes', 'max_input_seconds', 'max_output_seconds', 'max_work_mb', 'max_download_mb', 'paid_calls']:
        if k not in limits:
            production.append('declare limit: ' + k)
        else:
            positive(limits[k], k, zero=k in {'max_download_mb', 'paid_calls'})
    if total > limits.get('max_output_seconds', float('inf')):
        production.append('edit duration exceeds max_output_seconds (new scenes also need a timeline check)')
    for s in sources:
        if 'duration_seconds' in s and positive(s['duration_seconds'], 'source duration') > limits.get('max_input_seconds', float('inf')):
            production.append(s['id'] + ': declared duration exceeds max_input_seconds')
    acceptance = spec.get('acceptance', [])
    if not isinstance(acceptance, list) or any(not isinstance(x, str) or not x.strip() for x in acceptance):
        raise ValueError('acceptance must be a list of nonempty checks')
    if not acceptance:
        production.append('predeclare quality acceptance checks')
    return {'scenario': spec['scenario'], 'qualification': 'experimental_planning_only',
            'execution_authorized': False, 'publication_authorized': False,
            'source_inspection': 'not_performed', 'production_blockers': production,
            'publication_blockers': publication, 'limits': limits,
            'budget_enforcement': 'declarations_only; no runner executes or enforces these limits',
            'shared_stages': ['source/rights review', 'facts/transcript/scenes', 'concept/storyboard',
                              'edit decisions', 'scene/layer tool plan', 'audio selection and mix', 'delivery QA'],
            'edit_decisions': edits, 'acceptance': acceptance,
            'integration_gate': 'A/B/C remain untested end-to-end; owner confirmation and bounded experiment required',
            'outputs': {k: {'state': 'planned', 'file': None, 'qa': 'not_run'} for k in
                        ['mp4', 'audio-stems', 'subtitles', 'first-screen', 'thumbnail', 'youtube-copy',
                         'provenance', 'technical-qa', 'time-resource-log']}}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('spec', type=Path)
    p.add_argument('--format', choices=['json', 'brief'], default='json', help='brief can be passed to project.py init')
    args = p.parse_args()
    try:
        spec = json.loads(args.spec.read_text())
        brief = dict(spec['brief'])
        if 'production' in brief:
            raise ValueError('Declare production in the workflow specification, not nested brief')
        brief['production'] = {k: v for k, v in spec.items() if k != 'brief'}
        # Unqualified capabilities cannot be silently accepted in these experimental scenarios.
        brief['minimum_evidence'] = 'tested'
        planner = runpy.run_path(str(BASE / 'plan.py'))['plan']
        registry = json.loads((BASE.parent / 'references/tools.json').read_text())
        route = planner(brief, registry)
        report = dict(route['production'])
        report['route_plan'] = route
        print(json.dumps(brief if args.format == 'brief' else report, indent=2, allow_nan=False))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        p.error(str(exc))


if __name__ == '__main__':
    main()
