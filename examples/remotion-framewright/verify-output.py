"""Check actual encoded deliverable metadata, not source constants."""
import json
from pathlib import Path
import subprocess
p = Path('outputs/Framewright-Remotion-1080p.mp4')
r = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(p)], check=True, capture_output=True, text=True)
a = json.loads(r.stdout)
Path('outputs/ffprobe.json').write_text(r.stdout)
v = next((s for s in a['streams'] if s['codec_type'] == 'video'))
s = next((s for s in a['streams'] if s['codec_type'] == 'audio'))
if not (v['width'], v['height'], v['r_frame_rate'], int(v['nb_frames'])) == (1920, 1080, '30/1', 900):
    raise ValueError('Encoded output does not match the reference delivery contract')
if not (v['codec_name'] == 'h264' and s['codec_name'] == 'aac'):
    raise ValueError('Encoded output does not match the reference delivery contract')
if not abs(float(a['format']['duration']) - 30) < 0.1:
    raise ValueError('Encoded output does not match the reference delivery contract')
if not int(s['channels']) == 2:
    raise ValueError('Encoded output does not match the reference delivery contract')
print('PASS: H264 1920x1080 30fps / 900 frames / 30 seconds; stereo AAC present')
image = Path('outputs/Framewright-Remotion-thumbnail.png')
import struct
header = image.read_bytes()[:24]
if len(header) != 24 or header[:8] != b'\x89PNG\r\n\x1a\n' or header[12:16] != b'IHDR' or struct.unpack('>II', header[16:24]) != (1920, 1080):
    raise ValueError('Reference thumbnail must be a 1920x1080 PNG')
print('PASS: native PNG thumbnail is 1920x1080')
