#!/usr/bin/env python3
"""Create one bounded, local review proxy using the existing editing helpers."""
import json
from pathlib import Path
import runpy
import sys

E = runpy.run_path(str(Path(__file__).resolve().parent / 'editing.py'))
source, output = map(Path, sys.argv[1:3])
start, end, context = map(float, sys.argv[3:6])
meta = E['probe'](source)
if not meta['video']:
    raise ValueError('Review clip requires a video stream')
if end > meta['duration_seconds']:
    raise ValueError('Requested interval exceeds source duration')
a, b = max(0, start-context), min(meta['duration_seconds'], end+context)
if b-a > 30:
    raise ValueError('Review preview cannot exceed 30 seconds')
part = output.with_suffix('.mkv')
duration = E['review_part']({'path': str(source), **meta}, a, b-a, part, True)
E['ffmpeg'](['-threads', '1', '-i', str(part), '-c:v', 'libx264', '-threads', '1',
             '-crf', '20', '-c:a', 'aac', '-movflags', '+faststart', str(output)])
E['ffmpeg'](['-threads', '1', '-i', str(output), '-f', 'null', '-'])
print(json.dumps({'interval': {'start': a, 'end': b},
                  'requested': {'start': start, 'end': end, 'context': context}, 'duration': duration,
                  'audio': 'source' if meta['audio'] else 'synthetic_silence',
                  'decode': 'pass', 'scope': 'review proxy; no creative or listening approval'}))
