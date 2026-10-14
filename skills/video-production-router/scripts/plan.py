#!/usr/bin/env python3
"""Offline block/layer shortlist. Never installs, renders, publishes or calls a model."""
import argparse
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path

DEFAULTS = {'source-project': 'brag', 'react-ui': 'flute', 'book-art': 'hyperframes', 'brand': 'remotion', 'data': 'remotion', 'object': 'anatomy', 'composition': 'hyperframes', 'video': 'ffmpeg'}
MAIN_ROLES = {'orchestrator', 'renderer', 'illustrator', 'finisher'}
PREFERRED_ROLES = {'narration': 'voice', 'audio-qa': 'audio', 'audio-mix': 'audio', 'media-mux': 'finisher', 'still-export': 'finisher'}


def capability(tool, feature, language, paid):
    cap = next((x for x in tool['features'] if x['id'] == feature), None)
    if not cap or cap['status'] not in {'tested', 'documented'}:
        return None
    if cap.get('requires_paid') and not paid:
        return None
    status = cap['status']
    if feature == 'narration':
        if language not in cap.get('documented_languages', []):
            return None
        if language not in cap.get('tested_languages', []):
            status = 'documented'
    return dict(feature=feature, tool=tool['id'], evidence=status, source=cap['source'], note=cap['note'])


def frames(value, fps):
    try:
        number = Decimal(str(value)) * fps
        if not number.is_finite() or number <= 0 or number != number.to_integral_value():
            raise ValueError('Durations must be positive whole frame counts at the selected fps')
        return int(number)
    except (InvalidOperation, TypeError) as exc:
        raise ValueError('Invalid duration') from exc


def plan(brief, registry):
    if not isinstance(brief, dict):
        raise ValueError('Brief must be a JSON object')
    tools = {t['id']: t for t in registry['tools']}
    blocks = brief.get('blocks')
    if not isinstance(blocks, list) or not blocks:
        raise ValueError('Provide a nonempty blocks list; first decompose the natural-language brief')
    minimum = brief.get('minimum_evidence', 'documented')
    if minimum not in {'tested', 'documented'}:
        raise ValueError('minimum_evidence must be tested or documented')
    canvas = brief.get('canvas', {'width': 1920, 'height': 1080, 'fps': 30})
    if not isinstance(canvas, dict) or set(canvas) != {'width', 'height', 'fps'} or not all(type(v) is int and v > 0 for v in canvas.values()):
        raise ValueError('canvas needs positive integer width, height and fps')
    if type(brief.get('allow_paid', False)) is not bool:
        raise ValueError('allow_paid must be a boolean (planning constraint, not purchase authority)')
    result, ids, cursor = [], set(), 0
    for block in blocks:
        if not isinstance(block, dict):
            raise ValueError('Each block must be a JSON object')
        identity = block.get('id')
        kind = block.get('input')
        if not isinstance(identity, str) or not identity or identity in ids:
            raise ValueError('Block IDs must be unique nonempty strings')
        ids.add(identity)
        if kind not in DEFAULTS:
            raise ValueError(f'Unknown input: {kind}')
        assets = block.get('assets', [])
        if not isinstance(assets, list) or any(a not in DEFAULTS for a in assets):
            raise ValueError('assets must be a list of recognised input kinds')
        available = {kind, *assets}
        effects, deliverables = block.get('effects', []), block.get('deliverables', ['video-export'])
        if not all(isinstance(v, list) and all(isinstance(x, str) and x for x in v) for v in (effects, deliverables)):
            raise ValueError('effects and deliverables must be lists of feature IDs')
        requested = list(dict.fromkeys(effects + deliverables))
        if canvas['height'] > canvas['width']:
            requested.append('vertical-format')
        requested = list(dict.fromkeys(requested))
        language = block.get('language', brief.get('language', 'en'))
        if not isinstance(language, str) or not language:
            raise ValueError('language must be a nonempty string')
        paid = brief.get('allow_paid', False)
        style = block.get('style', '')
        if not isinstance(style, str):
            raise ValueError('style must be a string')
        def acceptable(cap):
            return cap is not None and (minimum != 'tested' or cap['evidence'] == 'tested')
        def fits(tool):
            return not tool['inputs'] or bool(available.intersection(tool['inputs'])) or (tool['role'] == 'finisher' and any(capability(t, 'video-export', language, paid) for t in selected))
        candidates = [t for t in tools.values() if t['role'] in MAIN_ROLES and kind in t['inputs']]
        preferred = block.get('preferred_tool')
        if preferred is not None:
            if preferred not in tools or tools[preferred]['role'] not in MAIN_ROLES:
                raise ValueError('preferred_tool must name a known picture/orchestration/finishing tool')
            candidates = [tools[preferred]] if kind in tools[preferred]['inputs'] else []
        candidates.sort(key=lambda t: (-sum(acceptable(capability(t, f, language, paid)) for f in effects), -(style in t['styles']), -(t['id'] == DEFAULTS[kind]), t['id']))
        primary = candidates[0] if candidates else None
        selected = [primary] if primary else []
        coverage, unmet, needs_test = [], [], []
        for feature in requested:
            cap = next((c for t in selected if acceptable(c := capability(t, feature, language, paid))), None)
            if cap is None and primary is not None:
                providers = [t for t in tools.values() if fits(t) and acceptable(capability(t, feature, language, paid))]
                providers.sort(key=lambda t: (t['role'] != PREFERRED_ROLES.get(feature), capability(t, feature, language, paid)['evidence'] != 'tested', t['id']))
                if providers:
                    provider = providers[0]
                    if provider not in selected:
                        selected.append(provider)
                    cap = capability(provider, feature, language, paid)
            if cap:
                coverage.append(cap)
                if cap['evidence'] != 'tested':
                    needs_test.append(feature)
            else:
                unmet.append(feature)
        if primary is None:
            unmet.append('input-compatible-primary')
        duration = frames(block['duration_seconds'], canvas['fps']) if 'duration_seconds' in block else None
        overlap = block.get('overlap_frames', 0)
        if type(overlap) is not int or overlap < 0 or (not result and overlap):
            raise ValueError('Invalid overlap_frames')
        if overlap and (duration is None or result[-1]['duration_frames'] is None or overlap >= min(duration, result[-1]['duration_frames'])):
            raise ValueError('Overlap must be smaller than both known adjacent durations')
        start = cursor - overlap if cursor is not None else None
        cursor = start + duration if start is not None and duration is not None else None
        result.append({'id': identity, 'input': kind, 'style': style, 'style_match': bool(primary and style in primary['styles']), 'primary_tool': primary['id'] if primary else preferred, 'tools': [t['id'] for t in selected], 'coverage': coverage, 'unmet': unmet, 'requires_feature_test': needs_test, 'start_frame': start, 'duration_frames': duration, 'overlap_frames': overlap, 'known_limits': {t['id']: t['limitations'] for t in selected}, 'handoff': {'canvas': canvas, 'picture': 'local clip or image/SVG asset; validate actual codec/alpha/colour compatibility', 'audio': 'separate narration/music/stems; declare trim, gain and ownership before common mix'}})
    if 'duration_seconds' in brief and (cursor is None or frames(brief['duration_seconds'], canvas['fps']) != cursor):
        raise ValueError('Declared total duration must match the known block timeline including overlaps')
    blocked = any(x['unmet'] for x in result)
    return {'schema_version': 1, 'status': 'blocked' if blocked else 'proposed', 'qualification': 'planning_only', 'execution': 'not_started', 'minimum_evidence': minimum, 'canvas': canvas, 'duration_frames': cursor, 'blocks': result, 'assembly': {'tool': 'ffmpeg', 'evidence': 'documented', 'qualification': 'new multi-block combinations need an integration test; individual successes do not qualify a chain', 'steps': ['normalise actual size/fps/colour/alpha and frame boundaries', 'assemble picture and a single master audio timeline', 'inspect encoded transitions, sync, loudness, peaks, thumbnail and metadata', 'retain native exports, final hashes and per-block evidence']}, 'notes': ['Styles are preferences, not fixed renderer limits or quality scores.', 'Read the cited installed-version docs before execution.', 'Paid availability in a plan is not purchase/account/publication authorisation.', 'Missing durations require timing decisions; no final timeline is claimed.'] if cursor is None else ['No model evaluation, rendering or publication was performed by this planner.', 'Style matching does not qualify a new combination.', 'Paid availability is a planning constraint, not purchase authority; engine licences and total cost need separate review.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('brief', type=Path)
    args = parser.parse_args()
    try:
        registry = json.loads((Path(__file__).resolve().parents[1] / 'references/tools.json').read_text())
        result = plan(json.loads(args.brief.read_text()), registry)
    except (ValueError, KeyError, TypeError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
