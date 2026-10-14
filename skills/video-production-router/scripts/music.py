#!/usr/bin/env python3
"""Plan three music/video directions; no provider calls, downloads or rendering."""
import argparse
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path


def plan_music(spec, registry):
    if not isinstance(spec, dict):
        raise ValueError('music must be an object')
    direction = spec.get('direction')
    if direction not in {'brief-first', 'video-first', 'music-first'}:
        raise ValueError('music.direction must be brief-first, video-first or music-first')
    mode = spec.get('mode', 'existing' if direction == 'music-first' else 'instrumental')
    if mode not in {'instrumental', 'song', 'existing'}:
        raise ValueError('music.mode must be instrumental, song or existing')
    provider = spec.get('provider', 'existing' if mode == 'existing' else None)
    profiles = {t['id']: t for t in registry['tools'] if t['role'] == 'music-provider'}
    if provider is not None and provider != 'existing' and provider not in profiles:
        raise ValueError('Unknown music provider; retain an explicit supported choice')
    if provider == 'existing' and mode != 'existing':
        raise ValueError('An existing provider cannot generate music; use mode existing with audio_source')
    if direction == 'music-first' and mode != 'existing':
        raise ValueError('music-first locks an existing audio source; generate/select it before this stage')
    required_source = 'audio_source' if mode == 'existing' else 'video_source' if direction == 'video-first' else None
    if required_source and (not isinstance(spec.get(required_source), str) or not spec[required_source].strip()):
        raise ValueError(f'{direction} needs {required_source}; source references are not automatically read or uploaded')
    if direction == 'video-first' and (not isinstance(spec.get('video_source'), str) or not spec['video_source'].strip()):
        raise ValueError('video-first needs video_source')
    if mode == 'song' and (not isinstance(spec.get('lyrics'), str) or not spec['lyrics'].strip()):
        raise ValueError('Song mode needs authorised lyrics; draft/review them before generation')
    for flag in ('inputs_authorized', 'lyrics_authorized'):
        if flag in spec and type(spec[flag]) is not bool:
            raise ValueError(f'{flag} must be a boolean')
    cues = spec.get('cues', [])
    if not isinstance(cues, list):
        raise ValueError('music.cues must be a list')
    previous = Decimal('-1')
    for cue in cues:
        if not isinstance(cue, dict) or not isinstance(cue.get('event'), str) or not cue['event'].strip():
            raise ValueError('Each cue needs a time_seconds and nonempty event')
        try:
            stamp = Decimal(str(cue['time_seconds']))
        except (KeyError, InvalidOperation) as exc:
            raise ValueError('Invalid cue time_seconds') from exc
        if not stamp.is_finite() or stamp < 0 or stamp < previous:
            raise ValueError('Cue times must be finite, nonnegative and ordered')
        previous = stamp
    purpose = spec.get('intended_use', 'private-test')
    if purpose not in {'private-test', 'noncommercial', 'commercial'}:
        raise ValueError('Unknown music.intended_use')
    rights = spec.get('rights', {})
    if not isinstance(rights, dict) or rights.get('status', 'unknown') not in {'unknown', 'noncommercial_only', 'commercial_granted'}:
        raise ValueError('Invalid rights record')
    status = rights.get('status', 'unknown')
    evidence = rights.get('evidence')
    if status != 'unknown' and (not isinstance(evidence, str) or not evidence.strip()):
        raise ValueError('A rights claim needs its evidence reference, not just a plan name')
    usage = 'local_evaluation_only' if purpose == 'private-test' else 'rights_review_required'
    if purpose == 'commercial' and status == 'noncommercial_only':
        usage = 'commercial_not_permitted_by_record'
    elif purpose == 'commercial' and status == 'commercial_granted':
        usage = 'commercial_claim_recorded_requires_review'
    elif purpose == 'noncommercial' and status != 'unknown':
        usage = 'noncommercial_compatible_with_record'
    gates = []
    if not spec.get('inputs_authorized', False):
        gates.append('confirm input rights before upload or generation')
    if mode == 'song' and not spec.get('lyrics_authorized', False):
        gates.append('confirm original/licensed lyrics before generation')
    if mode != 'existing':
        gates.append('inspect current account model, credits and approved download availability; no purchases implied')
    visual = spec.get('visual_source', 'external-renderer')
    if visual not in {'external-renderer', 'native-export', 'generated-scenes'}:
        raise ValueError('Unknown music.visual_source')
    visual_feature = {'native-export': 'song-card-video', 'generated-scenes': 'music-video-generation'}.get(visual)
    if provider == 'suno' and visual == 'generated-scenes':
        visual_feature = 'video-cover-art'
    profile = profiles.get(provider)
    feature = next((f for f in profile['features'] if f['id'] == visual_feature), None) if profile else None
    return {
        'direction': direction, 'mode': mode, 'provider': provider,
        'provider_choice': 'explicit' if 'provider' in spec else 'choose_after_account_and_rights_check' if mode != 'existing' else 'existing_source',
        'execution': 'not_started', 'technical_status': 'source_declared_not_decoded' if mode == 'existing' else 'documented_requires_account_check',
        'timeline_owner': {'brief-first': 'storyboard', 'video-first': 'locked_picture', 'music-first': 'locked_music'}[direction],
        'audio_role': 'foreground_song' if mode == 'song' else 'music_bed' if mode == 'instrumental' else 'existing_music',
        'source_reference': spec.get(required_source) if required_source else spec.get('video_source'),
        'cues': cues, 'usage_status': usage, 'intended_use': purpose, 'rights': rights,
        'publication_authorized': False, 'permission_gates': gates,
        'native_visuals': {'requested': visual, 'feature': visual_feature, 'evidence': feature['status'] if feature else 'not_selected' if visual == 'external-renderer' else 'unknown', 'source': feature.get('source') if feature else None, 'requires_paid_feature': bool(feature and feature.get('requires_paid'))},
        'handoff': ['freeze the actual approved audio version; retain source and download provenance', 'measure real duration; prompt length is not an exact edit contract', 'video-first: fit music to picture cues; music-first: fit cuts to verified musical sections', 'keep narration, sung vocals, music and SFX separate; do not substitute TTS for singing', 'classify exported video as song/lyric card, cover loop or generated scene before reuse', 'preserve required branding/provenance; normalise dimensions/fps without claiming new detail', 'verify encoded sync, lyrics by listening, loudness, peaks and crop; retain local hashes'],
        'qualification': 'planning_only; technical availability and usage rights are independent'
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('brief', type=Path)
    args = parser.parse_args()
    try:
        registry = json.loads((Path(__file__).resolve().parents[1] / 'references/tools.json').read_text())
        result = plan_music(json.loads(args.brief.read_text()), registry)
    except (ValueError, OSError, TypeError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2))
