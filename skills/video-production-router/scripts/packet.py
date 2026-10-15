"""Render an offline plan as a reviewable production handoff, never a QA receipt."""
import html
import json
import re


def cell(value):
    """Treat brief content as text, not Markdown/HTML instructions."""
    text = html.escape(str(value), quote=False).replace('\n', ' ').replace('\r', ' ')
    return re.sub(r'([\\`*_{}\[\]()#+!:|>~])', r'\\\1', text)


def checks(lines, items, status='planned'):
    lines.extend(f'- [ ] {status}: {item}' for item in items)


def markdown(brief, plan, registry):
    canvas = plan['canvas']
    fps = canvas['fps']
    lines = ['# Production plan', '',
             f"Status: **{plan['status']}** · execution: **{plan['execution']}** · qualification: **planning_only**.",
             'No assets were inspected and no checks were verified by this command. Filenames below are suggestions, not delivered files.', '',
             f"Canvas: {canvas['width']}×{canvas['height']} · {fps} fps · total: " +
             (f"{plan['duration_frames']} frames ({plan['duration_frames'] / fps:g}s)." if plan['duration_frames'] is not None else 'unknown; timing decisions required.'), '',
             '## Scene timeline', '', '| Scene | Frames (end-exclusive) | Duration | Overlap | Input kind | Tool chain |',
             '| --- | --- | --- | --- | --- | --- |']
    for block in plan['blocks']:
        start, duration = block['start_frame'], block['duration_frames']
        span = f'{start}–{start + duration}' if start is not None and duration is not None else 'unknown'
        lines.append(f"| {cell(block['id'])} | {span} | {str(duration / fps) + 's' if duration is not None else 'unknown'} | {block['overlap_frames']} frames | {cell(block['input'])} | {cell(' → '.join(block['tools']) or 'blocked')} |")
    lines += ['', '## Before production', '']
    checks(lines, ['Compare source claims, title, attribution and CTA against the named product source.',
                   'Identify actual authorised artwork, fonts, components and media; input kinds are not inspected files.',
                   'Check selected versions, installed guides/APIs, dependencies and licence eligibility.',
                   'Confirm resource availability, input rights and execution authority; allow_paid is not spending permission.'])
    lines += ['', 'Cost/setup estimates are unavailable. This view does not enforce a spending, download or runtime budget.', '']
    any_video = False
    for index, (source, block) in enumerate(zip(brief['blocks'], plan['blocks']), 1):
        identity = cell(block['id'])
        stem = f"{index:02d}-" + (re.sub(r'[^a-zA-Z0-9_-]+', '-', block['id']).strip('-') or 'scene')
        lines += [f'## Scene {index}: {identity}', '', f"Primary: {cell(block['primary_tool'] or 'none')}. Style: {cell(block['style'] or 'unspecified')}; match: {str(block['style_match']).lower()} (preference, not a quality guarantee).",
                  f"Required source kind: {cell(block['input'])}. Language: {cell(source.get('language', brief.get('language', 'en')))}."]
        voice_choice = source.get('preferred_voice', brief.get('preferred_voice'))
        if voice_choice:
            lines.append(f'Explicit voice choice: {cell(voice_choice)} (preserved even if unsupported).')
        if source.get('preferred_tool'):
            lines.append(f"Explicit picture choice: {cell(source['preferred_tool'])}.")
        if source.get('assets'):
            lines.append('Additional declared input kinds: ' + cell(', '.join(source['assets'])) + ' (availability unverified).')
        lines += ['', '| Requirement | Provider | Evidence | Source key |', '| --- | --- | --- | --- |']
        for cap in block['coverage']:
            lines.append(f"| {cell(cap['feature'])} | {cell(cap['tool'])} | {cell(cap['evidence'])} | {cell(cap['source'])} |")
        for cap in block['coverage']:
            if cap['note']:
                lines.append(f"\nProvider note ({cell(cap['feature'])}): {cell(cap['note'])}")
        if block['unmet']:
            lines += ['', '**Blocked requirements:** ' + cell(', '.join(block['unmet'])) + '. No fallback was executed.']
        if block['requires_feature_test']:
            lines += ['', '**Feature test required:** ' + cell(', '.join(block['requires_feature_test'])) + '.']
        found = {c['feature']: c for c in block['coverage']}
        requested = list(dict.fromkeys(source.get('deliverables', ['video-export'])))
        lines += ['', '### Intended outputs and QA', '']
        for output in requested:
            if output not in found:
                checks(lines, [f'{cell(output)} has no eligible provider; resolve the unmet requirement before promising an artifact.'], 'blocked')
                continue
            provider = found[output]['tool']
            if output == 'video-export':
                any_video = True
                lines += [f'**{stem}.mp4** — proposed scene export via {cell(provider)}; codec/container must be verified.', '']
                checks(lines, ['Decode the complete encoded video; inspect dimensions, fps, duration/frame boundaries, codec and colour.',
                               'Inspect scene action, camera, crop, occlusion, title/CTA legibility at full and reduced size.',
                               'Inspect encoded transition/effect timing across adjacent frames; verify holds and seams.',
                               'If audio is present, inspect encoded sync, loudness, true peaks and human listening; otherwise confirm intentional silence.',
                               'Retain native and final export size/SHA-256 with QA evidence.'])
            elif output == 'still-export':
                provenance = ('extracted encoded frame; select and retain its exact time/frame and final-video source' if provider == 'ffmpeg' else
                              'proposed native still; verify the installed renderer supports this exact export')
                lines += [f'**{stem}-still.png** — {cell(provider)}; {provenance}.', '']
                if provider == 'ffmpeg':
                    checks(lines, ['Provide or render the intermediate video, decode it and retain its hash before extracting the selected frame.'])
                checks(lines, ['Inspect this image independently: source identity/rights, decoded format/dimensions and crop.',
                               'Read all titles/labels/CTA at intended size and a reduced preview; inspect edges and clipping.',
                               'Record the image provenance, size and SHA-256 separately from video QA.'])
            elif output == 'narration':
                lines += [f'**{stem}-narration.wav** — proposed synthetic speech via {cell(provider)}; singing is not implied.', '']
                checks(lines, ['Compare spoken copy with approved script/source claims; disclose synthetic speech as required by model terms.',
                               'Measure decoded speech duration/sample rate and placement; check clipping, pronunciation, pauses, stress and intonation.',
                               'Keep speech separate until the common mix; human listening remains required.'])
            else:
                lines += [f'**{cell(output)}** — proposed via {cell(provider)}; output filename/format require a production decision.', '']
                checks(lines, ['Define an output-specific acceptance check with the selected guide before execution.'])
        features = set(source.get('effects', [])) | set(requested)
        if any(any(token in f.lower() for token in ('alpha', 'transparen')) for f in features):
            checks(lines, ['For every alpha-bearing video/still: decode channels/alpha and composite on light/dark backgrounds; inspect matte, halos and opacity.'])
        if 'three-scene' in block['tools']:
            checks(lines, ['Check WebGL readiness, absolute-time seek/reseek, visible object action/camera, geometry, occlusion and cover/CTA hold; no physics qualification is implied.'])
        if block['known_limits']:
            lines += ['', '### Retained tool limits', '']
            for tool, limits in block['known_limits'].items():
                lines.extend(f'- {cell(tool)}: {cell(limit)}' for limit in limits)
        lines.append('')
    if any_video:
        lines += ['## Final assembly', '', f"Proposed owner: {cell(plan['assembly']['tool'])}. New combinations require an integration test; component evidence does not qualify the chain.",
                  'Suggested final file: **final-video.mp4** (not yet created).', '']
        checks(lines, ['Normalise actual size/fps/colour/alpha and frame boundaries; inspect encoded seams and transitions.',
                       'Use one master audio timeline; declare trims, gains and source preservation before mixing.',
                       'For multiple stems, inspect relative alignment, polarity/phase and stereo/mono cancellation.',
                       'Decode final video/audio; check sync, loudness, true peaks, human listening and retain size/SHA-256.',
                       'Inspect each requested still independently; deliver only existing files under current authority.'])
    if plan.get('music'):
        music = plan['music']
        lines += ['', '## Independent music plan', '']
        # Keep all independent gates and references visible; do not reinterpret them.
        lines += ['```json', json.dumps(music, ensure_ascii=True, indent=2), '```', '']
        checks(lines, ['Resolve the music plan’s source, rights/account and publication gates before provider execution.'])
    lines += ['', '## Handoff status', '',
              'All QA above is planned or blocked. Human listening, creative acceptance and publication are separate decisions; none is inferred here.',
              'This packet covers common export checks, not the complete tool/effect contract. Read references/handoff.md and selected recipes before execution.', '',
              'Source keys resolve in references/tools.json; local evidence and scope live in references/catalog.json.']
    selected_sources = sorted({c['source'] for b in plan['blocks'] for c in b['coverage']})
    for key in selected_sources:
        record = registry.get('sources', {}).get(key, {})
        lines.append(f"- {cell(key)}: {cell(record.get('url', 'see registry'))}")
    return '\n'.join(lines) + '\n'
