#!/usr/bin/env python3
"""Private local audio catalogue. No uploads, downloads, generation or automatic rights grants."""
import argparse
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import re
import runpy
import subprocess
import time

BASE = Path(__file__).resolve().parent
CHECKPOINT = runpy.run_path(str(BASE / 'project.py'))
EXTENSIONS = {'.wav', '.mp3', '.flac', '.m4a', '.ogg', '.aiff', '.aif', '.opus'}


def private_path(path):
    path = path.absolute()
    if path.is_symlink():
        raise ValueError('Refuse a symlinked catalogue output')
    resolved = path.resolve()
    for parent in resolved.parents:
        if (parent / '.git').exists():
            if not any(resolved.is_relative_to(parent / sub) for sub in ('local', '.framewright')):
                raise ValueError('Private catalogue inside Git must use ignored local/ or .framewright/')
            break
    if not resolved.parent.is_dir():
        raise ValueError('Create the private catalogue parent explicitly')
    return resolved


def load(path):
    data = json.loads(path.read_text())
    if data.get('schema_version') != 1 or not isinstance(data.get('tracks'), list):
        raise ValueError('Unsupported catalogue')
    return data


def finite(value, positive=False):
    n = float(value)
    if not math.isfinite(n) or (positive and n <= 0):
        raise ValueError('Expected finite ' + ('positive ' if positive else '') + 'number')
    return n


def pin(path):
    return CHECKPOINT['file_record'](path, path.parent)


def verify(row, root):
    path = root / row['path']
    resolved = path.resolve()
    if not resolved.is_relative_to(root.resolve()) or path.is_symlink():
        raise ValueError('Source escaped declared folder or became a symlink')
    record = pin(path)
    if (record['bytes'], record['sha256']) != (row['bytes'], row['id']):
        raise ValueError('Source bytes/hash changed; rescan before reuse')
    return path


def scan(folder, previous, args):
    root = folder.resolve(strict=True)
    if not root.is_dir():
        raise ValueError('Choose a local audio folder')
    retained = {(r['id'], r['path']): r for r in previous.get('previous_unavailable', []) + previous.get('tracks', [])}
    old = {r['id']: r for r in retained.values()}
    tracks, errors = [], []
    begun = time.monotonic()
    candidates = 0
    for directory, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if not (Path(directory) / d).is_symlink())
        for name in sorted(files):
            path = Path(directory) / name
            if path.suffix.lower() not in EXTENSIONS or path.is_symlink():
                continue
            candidates += 1
            if candidates > args.max_files or time.monotonic() - begun > args.wall_seconds:
                raise ValueError('Scan budget reached; previous catalogue retained. Use a smaller folder or explicit larger bound')
            try:
                if path.stat().st_size > args.max_file_mb * 1024 * 1024:
                    errors.append({'path': str(path.relative_to(root)), 'error': 'file exceeds max_file_mb'}); continue
                record = pin(path)
                remaining = args.wall_seconds - (time.monotonic() - begun)
                if remaining <= 0:
                    raise ValueError('Scan wall-time budget reached')
                output = subprocess.run([args.ffprobe, '-v', 'error', '-protocol_whitelist', 'file',
                    '-select_streams', 'a:0', '-show_entries',
                    'format=duration,format_name:stream=codec_name,sample_rate,channels:format_tags=genre',
                    '-of', 'json', str(path)], capture_output=True, text=True,
                    timeout=min(10, remaining), check=True)
                metadata = json.loads(output.stdout)
                if not metadata.get('streams'):
                    raise ValueError('No audio stream')
                row = {'id': record['sha256'], 'path': str(path.relative_to(root)), 'bytes': record['bytes'],
                       'duration_seconds': finite(metadata['format']['duration'], positive=True),
                       'format': metadata['format'].get('format_name'), 'stream': metadata['streams'][0],
                       'mood': None, 'genre': None, 'bpm': None, 'loudness': None,
                       'origin': 'local recording; authorship not inferred', 'rights': {'status': 'unknown'},
                       'annotation_basis': 'operator supplied; not independently verified'}
                for key in ('mood', 'genre', 'bpm', 'origin', 'rights', 'loudness'):
                    if row['id'] in old:
                        row[key] = old[row['id']].get(key, row[key])
                # Container tags are useful hints, not verified classifications.
                row['embedded_tags'] = metadata['format'].get('tags', {})
                if args.analyze_seconds:
                    remaining = args.wall_seconds - (time.monotonic() - begun)
                    if remaining <= 0:
                        raise ValueError('Scan wall-time budget reached')
                    sound = subprocess.run([args.ffmpeg, '-nostdin', '-v', 'info', '-threads', '1',
                        '-protocol_whitelist', 'file', '-i', str(path), '-map', '0:a:0', '-vn',
                        '-t', str(args.analyze_seconds), '-af', 'volumedetect', '-f', 'null', '-'],
                        capture_output=True, text=True, timeout=min(30, remaining), check=True)
                    match = re.search(r'mean_volume:\s*(-?[0-9.]+) dB', sound.stderr)
                    peak = re.search(r'max_volume:\s*(-?[0-9.]+) dB', sound.stderr)
                    row['loudness'] = {'method': 'FFmpeg volumedetect; sample window, not LUFS/true peak',
                        'window_seconds': min(row['duration_seconds'], args.analyze_seconds),
                        'mean_dbfs': finite(match[1]) if match else None,
                        'sample_peak_dbfs': finite(peak[1]) if peak else None}
                after = pin(path)
                if (after['sha256'], after['bytes']) != (row['id'], row['bytes']):
                    raise ValueError('Source changed during scan')
                tracks.append(row)
            except (OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
                errors.append({'path': str(path.relative_to(root)), 'error': str(exc)})
    # Even the final probe/traversal may exhaust the global budget. Propagate
    # this stop before returning anything that the caller could persist.
    if time.monotonic() - begun >= args.wall_seconds:
        raise ValueError('Scan budget reached; previous catalogue retained. Use a smaller folder or explicit larger bound')
    return {'schema_version': 1, 'root': str(root), 'updated_utc': datetime.now(timezone.utc).isoformat(),
            'tracks': tracks, 'errors': errors, 'previous_unavailable': [r for r in retained.values()
               if (r['id'], r['path']) not in {(t['id'], t['path']) for t in tracks}],
            'analysis_wall_seconds': round(time.monotonic() - begun, 4),
            'tool_versions': {'ffprobe': subprocess.run([args.ffprobe, '-version'], capture_output=True,
                  text=True, check=True, timeout=5).stdout.splitlines()[0]},
            'publication_authorized': False}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    s = sub.add_parser('scan'); s.add_argument('folder', type=Path); s.add_argument('index', type=Path)
    s.add_argument('--max-files', type=int, default=100); s.add_argument('--wall-seconds', type=int, default=120)
    s.add_argument('--max-file-mb', type=int, default=200); s.add_argument('--analyze-seconds', type=int, default=0)
    s.add_argument('--ffprobe', default='ffprobe'); s.add_argument('--ffmpeg', default='ffmpeg')
    a = sub.add_parser('annotate'); a.add_argument('index', type=Path); a.add_argument('id')
    for key in ('mood', 'genre', 'origin', 'evidence'): a.add_argument('--' + key)
    a.add_argument('--bpm', type=float); a.add_argument('--rights', choices=['unknown', 'granted', 'noncommercial_only', 'denied'])
    f = sub.add_parser('find'); f.add_argument('index', type=Path)
    f.add_argument('--use', choices=['private-test', 'commercial', 'noncommercial'], default='private-test')
    f.add_argument('--mood'); f.add_argument('--genre'); f.add_argument('--bpm', type=float)
    f.add_argument('--bpm-tolerance', type=float, default=10); f.add_argument('--duration', type=float)
    args = p.parse_args()
    try:
        if args.command == 'find':
            data = load(args.index); matches, errors = [], []
            if args.duration is not None: finite(args.duration, positive=True)
            if args.bpm is not None: finite(args.bpm, positive=True)
            if finite(args.bpm_tolerance) < 0: raise ValueError('bpm-tolerance must be nonnegative')
            for row in data['tracks']:
                try: verify(row, Path(data['root']))
                except (OSError, ValueError) as exc:
                    errors.append({'id': row['id'], 'error': str(exc)}); continue
                status = row['rights'].get('status', 'unknown')
                allowed = status == 'granted' or (args.use == 'noncommercial' and status == 'noncommercial_only')
                if status == 'denied' or (args.use != 'private-test' and (not allowed or not row['rights'].get('evidence'))): continue
                if any(getattr(args, k) and getattr(args, k).casefold() != (row.get(k) or '').casefold() for k in ('mood', 'genre')): continue
                if args.bpm is not None and (row['bpm'] is None or abs(row['bpm'] - args.bpm) > args.bpm_tolerance): continue
                matches.append({**row, 'fit': 'trim' if args.duration and row['duration_seconds'] >= args.duration else
                    'loop_needs_seam_review' if args.duration else 'duration_not_requested'})
            print(json.dumps({'tracks': matches, 'file_problems': errors, 'publication_authorized': False,
                'rights_basis': 'operator record, not independent clearance'}, indent=2, allow_nan=False)); return
        path = private_path(args.index)
        with CHECKPOINT['locked'](path):
            data = load(path) if path.exists() else {'tracks': []}
            if args.command == 'scan':
                if any(getattr(args, k) <= 0 for k in ('max_files', 'wall_seconds', 'max_file_mb')) or not 0 <= args.analyze_seconds <= 30:
                    raise ValueError('Positive scan bounds required; analysis window 0..30 seconds')
                data = scan(args.folder, data, args)
            else:
                rows = [r for r in data['tracks'] if r['id'] == args.id]
                if not rows: raise ValueError('Unknown track id')
                for row in rows:
                    verify(row, Path(data['root']))
                    for key in ('mood', 'genre', 'origin'):
                        if getattr(args, key) is not None: row[key] = getattr(args, key)
                    if args.bpm is not None: row['bpm'] = finite(args.bpm, positive=True)
                    if args.rights:
                        if args.rights in {'granted', 'noncommercial_only'} and not (args.evidence or '').strip():
                            raise ValueError('A rights claim requires --evidence')
                        row['rights'] = {'status': args.rights, 'evidence': args.evidence}
                data['updated_utc'] = datetime.now(timezone.utc).isoformat()
            CHECKPOINT['save'](path, data)
            os.chmod(path, 0o600)
        print(json.dumps({'saved': str(path), 'tracks': len(data['tracks']), 'errors': data.get('errors', [])}))
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        p.error(str(exc))


if __name__ == '__main__':
    main()
