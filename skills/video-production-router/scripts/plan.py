#!/usr/bin/env python3
"""Offline block/layer shortlist. Never installs, renders, publishes or calls a model."""
import argparse
from decimal import Decimal, InvalidOperation
import json
import runpy
from itertools import combinations
from pathlib import Path

DEFAULTS = {'source-project': 'brag', 'react-ui': 'flute', 'book-art': 'hyperframes', 'brand': 'remotion', 'data': 'remotion', 'object': 'anatomy', 'composition': 'hyperframes', 'video': 'ffmpeg'}
MAIN_ROLES = {'orchestrator', 'renderer', 'illustrator', 'finisher'}
PREFERRED_ROLES = {'narration': 'voice', 'audio-qa': 'audio', 'audio-mix': 'audio', 'media-mux': 'finisher', 'still-export': 'finisher'}


def capability(tool, feature, language, paid, canvas=None):
    cap = next((x for x in tool['features'] if x['id'] == feature), None)
    if not cap or cap['status'] not in {'tested', 'documented'}:
        return None
    if cap.get('requires_paid') and not paid:
        return None
    status = cap['status']
    if status == 'tested' and any(
        owner.get('tested_canvases') and canvas not in owner['tested_canvases']
        for owner in (tool, cap)
    ):
        status = 'documented'
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
    music = runpy.run_path(str(Path(__file__).with_name('music.py')))['plan_music'](brief['music'], registry) if 'music' in brief else None
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
        effects = runpy.run_path(str(Path(__file__).with_name('terms.py')))['normalize_effects'](effects)
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
        def activated(tool):
            gate = tool.get('activation')
            return not gate or bool(set(requested).intersection(gate['features'])) or style in gate['styles']
        candidates = [t for t in tools.values() if t['role'] in MAIN_ROLES and kind in t['inputs'] and activated(t)]
        preferred = block.get('preferred_tool')
        if preferred is not None:
            if preferred not in tools or tools[preferred]['role'] not in MAIN_ROLES:
                raise ValueError('preferred_tool must name a known picture/orchestration/finishing tool')
            candidates = [tools[preferred]] if kind in tools[preferred]['inputs'] else []
        preferred_voice = block.get('preferred_voice', brief.get('preferred_voice'))
        if preferred_voice is not None and (not isinstance(preferred_voice, str) or preferred_voice not in tools or tools[preferred_voice]['role'] != 'voice'):
            raise ValueError('preferred_voice must name a known voice tool')
        caps = {(t['id'], f): capability(t, f, language, paid, canvas) for t in tools.values() for f in set(requested + ['video-export'])}
        def chain_solution(main):
            # Exact subsets are small for this curated catalogue. Compare complete
            # chains, not a greedy alphabetical path or only direct capabilities.
            extras = sorted((t for t in tools.values() if t != main and activated(t) and t['role'] not in {'music-provider', 'preproduction'} and (
                any(acceptable(caps[t['id'], f]) for f in requested) or
                (t['role'] in {'renderer', 'orchestrator'} and acceptable(caps[t['id'], 'video-export']))
            )), key=lambda t: (t['role'] == 'finisher', t['id']))
            best = None
            for count in range(len(extras) + 1):
                for subset in combinations(extras, count):
                    chain = [main, *subset]
                    has_picture = any(t['role'] in {'renderer', 'orchestrator'} and acceptable(caps[t['id'], 'video-export']) for t in chain)
                    if any(t['inputs'] and not available.intersection(t['inputs']) and not (t['role'] == 'finisher' and has_picture) for t in subset):
                        continue
                    found = {}
                    for feature in requested:
                        choices = [t for t in chain if acceptable(caps[t['id'], feature]) and (feature != 'narration' or preferred_voice is None or t['id'] == preferred_voice)]
                        choices.sort(key=lambda t: (caps[t['id'], feature]['evidence'] != 'tested', t != main, t['role'] != PREFERRED_ROLES.get(feature), t['id']))
                        if choices:
                            found[feature] = caps[choices[0]['id'], feature]
                    rank = (-len(found), -sum(c['evidence'] == 'tested' for c in found.values()), len(chain), tuple(t['id'] for t in chain))
                    if best is None or rank < best[0]:
                        best = (rank, chain, found)
            return best
        solutions = [(chain_solution(t), t) for t in candidates]
        solutions.sort(key=lambda item: (*item[0][0][:3], -sum(acceptable(caps[item[1]['id'], f]) for f in set(effects)), -(style in item[1]['styles']), -(item[1]['id'] == DEFAULTS[kind]), item[1]['id'], item[0][0][3]))
        if solutions:
            solution, primary = solutions[0]
            _, selected, found = solution
        else:
            primary, selected, found = None, [], {}
        coverage = [found[f] for f in requested if f in found]
        unmet = [f for f in requested if f not in found]
        needs_test = [c['feature'] for c in coverage if c['evidence'] != 'tested']
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
    still_only = all(set(b.get('deliverables', ['video-export'])) == {'still-export'} for b in blocks)
    return {'schema_version': 1, 'status': 'blocked' if blocked else 'proposed', 'qualification': 'planning_only', 'execution': 'not_started', 'music': music, 'minimum_evidence': minimum, 'canvas': canvas, 'duration_frames': cursor, 'blocks': result, 'assembly': ({'tool': None, 'evidence': 'planning_only', 'qualification': 'Still-only delivery: no video assembly is proposed.', 'steps': ['validate native image format, dimensions, visual content and hashes']} if still_only else {'tool': 'ffmpeg', 'evidence': 'documented', 'qualification': 'new multi-block combinations need an integration test; individual successes do not qualify a chain', 'steps': ['normalise actual size/fps/colour/alpha and frame boundaries', 'assemble picture and a single master audio timeline', 'inspect encoded transitions, sync, loudness, peaks, thumbnail and metadata', 'retain native exports, final hashes and per-block evidence']}), 'notes': ['Styles are preferences, not fixed renderer limits or quality scores.', 'Read the cited installed-version docs before execution.', 'Paid availability in a plan is not purchase/account/publication authorisation.', 'Missing durations require timing decisions; no final timeline is claimed.'] if cursor is None else ['No model evaluation, rendering or publication was performed by this planner.', 'Style matching does not qualify a new combination.', 'Paid availability is a planning constraint, not purchase authority; engine licences and total cost need separate review.']}


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
