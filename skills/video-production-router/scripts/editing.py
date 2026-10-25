#!/usr/bin/env python3
"""Local source inspection, cut-only time maps and join review. No ASR/model calls."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys


def load(path):
    with Path(path).open(encoding='utf-8') as f:
        return json.load(f)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def file_hash(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def number(value, label, positive=False):
    if type(value) not in (int, float) or not math.isfinite(value) or value < 0 or (positive and value == 0):
        raise ValueError(label + ' must be finite and ' + ('positive' if positive else 'nonnegative'))
    return value


def text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(label + ' must be nonempty text')
    return value


def run(args):
    return subprocess.run(args, check=True, capture_output=True, text=True, timeout=120).stdout


def probe(path):
    raw = json.loads(run(['ffprobe', '-v', 'error', '-protocol_whitelist', 'file,pipe',
                          '-show_format', '-show_streams', '-of', 'json', str(path)]))
    streams = raw.get('streams', [])
    video = next((s for s in streams if s.get('codec_type') == 'video' and not s.get('disposition', {}).get('attached_pic')), None)
    audio = next((s for s in streams if s.get('codec_type') == 'audio'), None)
    if not video and not audio:
        raise ValueError('No audio/video stream: ' + str(path))
    duration = number(float(raw.get('format', {}).get('duration', 'nan')), 'media duration', True)
    return {'duration_seconds': duration, 'video': video, 'audio': audio}


def timed_rows(rows, duration, label):
    if not isinstance(rows, list):
        raise ValueError(label + ' must be a list')
    ids = set()
    for row in rows:
        rid = text(row.get('id'), label + ' id')
        if rid in ids:
            raise ValueError('Duplicate ' + label + ' id')
        ids.add(rid)
        start = number(row.get('start'), label + ' start')
        end = number(row.get('end'), label + ' end', True)
        if end <= start or end > duration + 1e-6:
            raise ValueError(label + ' interval exceeds source or is empty')
        text(row.get('text'), label + ' text')
    return rows


def inventory(spec, base):
    sources = spec.get('sources')
    if not isinstance(sources, list) or not sources:
        raise ValueError('sources must be a nonempty list')
    result, ids = [], set()
    for source in sources:
        sid = text(source.get('id'), 'source id')
        if sid in ids:
            raise ValueError('Duplicate source id')
        ids.add(sid)
        name = text(source.get('path'), 'source path')
        if '://' in name:
            raise ValueError('Only explicit local media paths are supported')
        path = (base / name).resolve()
        if not path.is_file():
            raise ValueError('Missing media: ' + str(path))
        pin = file_hash(path)
        media = probe(path)
        transcript = source.get('transcript', [])
        observations = source.get('observations', [])
        for key, rows in [('transcript', transcript), ('observations', observations)]:
            timed_rows(rows, media['duration_seconds'], key)
        if (transcript or observations) and source.get('evidence_sha256') != pin:
            raise ValueError('Supplied transcript/observations need matching evidence_sha256: ' + sid)
        if file_hash(path) != pin:
            raise ValueError('Source changed during inspection: ' + sid)
        result.append({'id': sid, 'path': str(path), 'sha256': pin, 'bytes': path.stat().st_size,
                       **media, 'transcript': transcript, 'observations': observations,
                       'review': {'content': 'not_performed', 'visual': 'not_performed',
                                  'listening': 'not_performed', 'motion': 'not_performed'},
                       'evidence_status': 'supplied_unverified' if transcript or observations else 'not_supplied'})
    return {'schema': 'framewright-edit-inventory-v1', 'sources': result,
            'publication_authorized': False, 'automatic_model_calls': 0}


def make_map(spec, base):
    inv = inventory(spec, base)
    sources = {s['id']: s for s in inv['sources']}
    edits = spec.get('edits')
    if not isinstance(edits, list) or not edits:
        raise ValueError('edits must be a nonempty list in playback order')
    segments, cursor = [], 0.0
    for i, edit in enumerate(edits, 1):
        if set(edit) - {'source', 'in_seconds', 'out_seconds', 'reason'}:
            raise ValueError('Only cut-only edits supported; no speed, overlap, transition or extra edit fields')
        sid = edit.get('source')
        if sid not in sources:
            raise ValueError('Unknown edit source')
        start = number(edit.get('in_seconds'), 'edit in_seconds')
        end = number(edit.get('out_seconds'), 'edit out_seconds', True)
        if end <= start or end > sources[sid]['duration_seconds'] + 1e-6:
            raise ValueError('Edit exceeds actual source duration or is empty')
        reason = text(edit.get('reason'), 'edit reason')
        duration = end - start
        segments.append({'segment': i, 'source': sid, 'source_start': start, 'source_end': end,
                         'output_start': cursor, 'output_end': cursor + duration, 'reason': reason})
        cursor += duration
    unselected = []
    for sid, source in sources.items():
        edge = 0
        for seg in sorted((s for s in segments if s['source'] == sid), key=lambda s: s['source_start']):
            if seg['source_start'] > edge:
                unselected.append({'source': sid, 'start': edge, 'end': seg['source_start'], 'reason': 'Not selected by this edit list'})
            edge = max(edge, seg['source_end'])
        if edge < source['duration_seconds']:
            unselected.append({'source': sid, 'start': edge, 'end': source['duration_seconds'], 'reason': 'Not selected by this edit list'})
    result = {'schema': 'framewright-edit-map-v1', 'sources': inv['sources'],
              'segments': segments, 'unselected_source_intervals': unselected, 'duration_seconds': cursor,
              'timing': 'seconds; half-open intervals; cuts only; speed=1',
              'semantic_review_performed': False, 'publication_authorized': False,
              'automatic_model_calls': 0}
    result['map_sha256'] = digest(result)
    return result


def checked_map(path):
    value = load(path)
    if value.get('schema') != 'framewright-edit-map-v1':
        raise ValueError('Expected an edit map from the map command')
    if value.get('map_sha256') != digest({k: v for k, v in value.items() if k != 'map_sha256'}):
        raise ValueError('Map changed; regenerate it from the plan')
    for source in value['sources']:
        if file_hash(source['path']) != source['sha256']:
            raise ValueError('Source changed; regenerate inventory and map: ' + source['id'])
    return value


def remap(value, extra=None):
    sources = {s['id']: s for s in value['sources']}
    inputs = []
    for source in value['sources']:
        inputs += [dict(c, source=source['id'], kind='subtitle') for c in source['transcript']]
    if extra is not None:
        if not isinstance(extra, list):
            raise ValueError('Extra cues must be a list')
        seen = set()
        for c in extra:
            if c.get('source') not in sources or c.get('kind') not in {'subtitle', 'overlay'}:
                raise ValueError('Each cue needs a known source and kind subtitle|overlay')
            source = sources[c['source']]
            timed_rows([c], source['duration_seconds'], 'cue')
            key = (c['source'], c['id'])
            if key in seen or any((x['source'], x['id']) == key for x in inputs):
                raise ValueError('Duplicate cue id within source')
            seen.add(key)
            if c.get('source_sha256') != source['sha256']:
                raise ValueError('Extra cue source_sha256 does not match source')
        inputs += extra
    result, removed = [], []
    for cue in inputs:
        occurrences = []
        for seg in value['segments']:
            if seg['source'] != cue['source']:
                continue
            start = max(cue['start'], seg['source_start'])
            end = min(cue['end'], seg['source_end'])
            if start >= end:
                continue
            clipped = start > cue['start'] or end < cue['end']
            occurrences.append({'cue_id': cue['id'], 'source': cue['source'], 'segment': seg['segment'],
                                'kind': cue['kind'], 'text': cue['text'],
                                'original_start': cue['start'], 'original_end': cue['end'],
                                'retained_source_start': start, 'retained_source_end': end,
                                'start': seg['output_start'] + start - seg['source_start'],
                                'end': seg['output_start'] + end - seg['source_start'],
                                'needs_review': clipped,
                                'reason': 'Cue crosses a removed boundary; review text/word edge' if clipped else None})
        if occurrences:
            result.extend(occurrences)
        else:
            removed.append({'source': cue['source'], 'cue_id': cue['id'], 'kind': cue['kind'],
                            'text': cue['text'], 'start': cue['start'], 'end': cue['end'],
                            'reason': 'No retained overlap; check meaning in context'})
    result.sort(key=lambda x: (x['start'], x['end'], x['segment']))
    return {'schema': 'framewright-retimed-cues-v1', 'map_sha256': value['map_sha256'],
            'cues': result, 'removed_cues': removed, 'semantic_review_performed': False,
            'publication_authorized': False}


def srt_text(result):
    cues = [c for c in result['cues'] if c['kind'] == 'subtitle']
    if any(c['needs_review'] for c in cues):
        raise ValueError('Clipped subtitle text needs review; align source cues to retained speech before SRT export')
    def stamp(seconds):
        ms = round(seconds * 1000)
        h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); sec, ms = divmod(ms, 1000)
        return f'{h:02}:{m:02}:{sec:02},{ms:03}'
    previous_end, chunks = -1, []
    for i, c in enumerate(cues, 1):
        start, end = round(c['start'] * 1000), round(c['end'] * 1000)
        if end <= start or start < previous_end:
            raise ValueError('Subtitle overlap or sub-millisecond cue; review before SRT export')
        if '\n\n' in c['text'] or '-->' in c['text'] or '\r' in c['text']:
            raise ValueError('Unsupported SRT text delimiter')
        previous_end = end
        chunks.append(f"{i}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}\n")
    return '\n'.join(chunks)


def ffmpeg(args):
    run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-filter_threads', '1', '-filter_complex_threads', '1', *args])


def review_part(source, start, duration, output, video):
    # This is a review proxy, never the retained final master. Video is frame-quantized.
    encoded_duration = max(1, math.ceil(duration * 24 - 1e-9)) / 24 if video else duration
    args = ['-protocol_whitelist', 'file,pipe', '-threads', '1', '-ss', str(start), '-i', source['path']]
    if video and not source['video']:
        args += ['-f', 'lavfi', '-i', 'color=c=0x20242a:s=640x360:r=24']
    silent_index = 2 if video and not source['video'] else 1
    if not source['audio']:
        args += ['-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo']
    if video:
        video_map = '0:' + str(source['video']['index']) if source['video'] else '1:v:0'
        args += ['-map', video_map, '-vf',
                 f'trim=duration={duration},scale=640:360:force_original_aspect_ratio=decrease,pad=640:360:(ow-iw)/2:(oh-ih)/2,'
                 'setsar=1,fps=fps=24:start_time=0,tpad=stop_mode=clone:stop_duration=0.05',
                 '-c:v', 'ffv1', '-threads', '1', '-pix_fmt', 'yuv420p']
    else:
        args += ['-vn']
    audio_map = '0:' + str(source['audio']['index']) if source['audio'] else f'{silent_index}:a:0'
    args += ['-map', audio_map, '-af', f'atrim=duration={duration},aresample=48000:first_pts=0,apad=whole_dur={encoded_duration},atrim=duration={encoded_duration}',
             '-ar', '48000', '-ac', '2', '-c:a', 'pcm_s16le', '-t', str(encoded_duration), str(output)]
    ffmpeg(args)
    return encoded_duration


def join_pack(value, output, context=1, only=None):
    import os
    import tempfile
    number(context, 'context', True)
    if not .1 <= context <= 5:
        raise ValueError('context must be between 0.1 and 5 seconds on each side')
    count = len(value['segments']) - 1
    if only is not None and not 1 <= only <= count:
        raise ValueError('join must name an existing boundary (1-based)')
    if count > 20 and only is None:
        raise ValueError('More than 20 joins; select one with --join')
    if output.exists():
        raise ValueError('Output already exists; choose a new revision')
    sources = {s['id']: s for s in value['sources']}
    cues = remap(value)['cues']
    report = {'schema': 'framewright-join-review-v1', 'map_sha256': value['map_sha256'],
              'publication_authorized': False, 'automatic_model_calls': 0, 'joins': [],
              'scope': 'Encoded review proxies only; no listening, semantic or final-film approval'}
    # Stage the whole pack. Failure never leaves a partly usable review directory.
    with tempfile.TemporaryDirectory(prefix='.editing-', dir=output.resolve().parent) as tmp:
        stage = Path(tmp) / 'pack'; stage.mkdir()
        for n in range(1, count + 1):
            if only is not None and n != only:
                continue
            left, right = value['segments'][n-1:n+1]
            folder = stage / f'join-{n:03}'; folder.mkdir()
            ls, rs = sources[left['source']], sources[right['source']]
            video = bool(ls['video'] or rs['video'])
            ld = min(context, left['source_end'] - left['source_start'])
            rd = min(context, right['source_end'] - right['source_start'])
            left_start = left['source_end'] - ld
            handles = [(ls, left_start, ld), (rs, right['source_start'], rd)]
            durations = []
            for i, (source, start, duration) in enumerate(handles):
                part = folder / (f'part-{i}.mkv' if video else f'part-{i}.wav')
                durations.append(review_part(source, start, duration, part, video))
            (folder/'concat.txt').write_text("file 'part-0." + ('mkv' if video else 'wav') + "'\nfile 'part-1." + ('mkv' if video else 'wav') + "'\n")
            preview = folder/('preview.mp4' if video else 'preview.wav')
            encode = ['-c:v', 'libx264', '-threads', '1', '-preset', 'fast', '-crf', '20', '-pix_fmt', 'yuv420p',
                      '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart'] if video else ['-c:a', 'pcm_s16le']
            ffmpeg(['-protocol_whitelist', 'file,pipe', '-f', 'concat', '-safe', '1', '-i', str(folder/'concat.txt'), *encode, str(preview)])
            # Detect decode failures, not perceptual/semantic defects.
            ffmpeg(['-protocol_whitelist', 'file,pipe', '-i', str(preview), '-f', 'null', '-'])
            details = probe(preview)
            if abs(details['duration_seconds'] - sum(durations)) > (2/24 if video else .01):
                raise ValueError('Review duration differs from the expected handles')
            ffmpeg(['-i', str(preview), '-filter_complex', 'showwavespic=s=960x140:colors=0x4a9aa2',
                    '-frames:v', '1', str(folder/'waveform.png')])
            samples = []
            if video:
                frame_count = int(details['video']['nb_frames'])
                cut_frame = round(durations[0] * 24)
                if frame_count <= cut_frame:
                    raise ValueError('Review video is missing the right side of the join')
                sample_frames = [0, max(0, cut_frame-1), cut_frame, frame_count-1]
                samples = [n/24 for n in sample_frames]
                for i, frame in enumerate(sample_frames):
                    # Decode by frame index: timestamp seeking can miss a rounded final frame.
                    ffmpeg(['-i', str(preview), '-vf', f'select=eq(n\\,{frame}),scale=240:135',
                            '-fps_mode', 'vfr', '-frames:v', '1', str(folder/f'frame-{i}.png')])
                args = []
                for i in range(4):
                    args += ['-i', str(folder/f'frame-{i}.png')]
                ffmpeg([*args, '-filter_complex', 'hstack=inputs=4', '-frames:v', '1', str(folder/'frames.png')])
            words = []
            for side, seg, a, b, offset in [('left', left, left['output_end']-ld, left['output_end'], 0),
                                             ('right', right, right['output_start'], right['output_start']+rd, durations[0])]:
                for c in cues:
                    if c['segment'] == seg['segment'] and c['start'] < b and c['end'] > a:
                        words.append(dict(c, side=side, preview_start=offset+max(c['start'],a)-a,
                                          preview_end=offset+min(c['end'],b)-a))
            write(folder/'words.json', {'cues': words, 'timing_note': 'Nominal source seconds; video proxies quantize handles to 24fps. Listen for word edges.'})
            synthetic = [s['id'] for s in (ls,rs) if not s['audio']]
            entry = {'join': n, 'output_cut_seconds': right['output_start'], 'preview_cut_seconds': durations[0],
                     'preview_file': str(preview.relative_to(stage)), 'preview_sha256': file_hash(preview),
                     'duration_seconds': details['duration_seconds'], 'requested_context_seconds': context,
                     'proxy_padding_seconds': [durations[0]-ld, durations[1]-rd],
                     'source_handles': [{'source': s['id'], 'start': a, 'end': a+d} for s,a,d in handles],
                     'synthetic_silence': synthetic, 'synthetic_background': [s['id'] for s in (ls,rs) if video and not s['video']],
                     'frame_sample_seconds': samples, 'decode': 'pass', 'listening': 'pending',
                     'visual_review': 'pending' if video else 'not_applicable', 'semantic_review': 'pending',
                     'normalization': '640x360,24fps,stereo48k' if video else 'PCM stereo48k'}
            report['joins'].append(entry)
            (folder/'concat.txt').unlink()
            for part in folder.glob('part-*'):
                part.unlink()
            for frame in folder.glob('frame-*.png'):
                frame.unlink()
        for source in value['sources']:
            if file_hash(source['path']) != source['sha256']:
                raise ValueError('Source changed while preparing review')
        write(stage/'report.json', report)
        lines = ['# Cut review', '', 'Review proxies. Decode passed; listening, meaning and picture still require review.',
                 'Use report.json for source/output times. Read words.json as supplied, unverified transcript evidence.', '']
        for j in report['joins']:
            name = f"join-{j['join']:03}"
            lines += [f"## Join {j['join']} at {j['output_cut_seconds']:.3f}s", '',
                      f"[Play context]({j['preview_file']}); cut at {j['preview_cut_seconds']:.3f}s in preview.", '',
                      f"[Waveform]({name}/waveform.png) · [Words and source times]({name}/words.json)", '']
            if j['frame_sample_seconds']:
                lines += [f'[Four frames: first, before cut, after cut, last]({name}/frames.png)', '']
            if j['synthetic_silence']:
                lines += ['No source audio; silence inserted for: ' + ', '.join(j['synthetic_silence']), '']
            lines += ['Check: complete words and qualifications; natural breath; justified visual change; click/pop or sync issue.', '']
        (stage/'review.md').write_text('\n'.join(lines), encoding='utf-8')
        if output.exists():
            raise ValueError('Output appeared during rendering; choose a new revision')
        os.rename(stage, output)
    return report


def write(path, value):
    encoded = json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n'
    with Path(path).open('x', encoding='utf-8') as f:
        f.write(encoded)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ['inspect', 'map', 'retime', 'joins']:
        p = sub.add_parser(name); p.add_argument('spec', type=Path); p.add_argument('--output', type=Path, required=True)
        if name == 'joins':
            p.add_argument('--context', type=float, default=1); p.add_argument('--join', type=int)
        if name == 'retime':
            p.add_argument('--cues', type=Path); p.add_argument('--srt', type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError('Output already exists; choose a new revision')
    if args.command == 'inspect':
        write(args.output, inventory(load(args.spec), args.spec.resolve().parent))
    elif args.command == 'map':
        write(args.output, make_map(load(args.spec), args.spec.resolve().parent))
    elif args.command == 'retime':
        result = remap(checked_map(args.spec), load(args.cues) if args.cues else None)
        subtitles = srt_text(result) if args.srt else None
        if args.srt and (args.srt.exists() or args.srt.resolve() == args.output.resolve()):
            raise ValueError('SRT path must be new and distinct')
        if args.srt:
            with args.srt.open('x', encoding='utf-8') as f:
                f.write(subtitles)
        write(args.output, result)
    elif args.command == 'joins':
        join_pack(checked_map(args.spec), args.output, args.context, args.join)
    print(json.dumps({'command': args.command, 'output': str(args.output), 'publication_authorized': False}))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError, AttributeError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        print('Error: ' + str(exc), file=sys.stderr)
        sys.exit(1)
