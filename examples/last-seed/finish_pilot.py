"""Assemble and measure an explicit local pilot; no approval or publishing."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import time

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('directory', type=Path)
p.add_argument('--frames', default='eevee-pilot-v3')
p.add_argument('--name', default='last-seed-pilot-v3')
a = p.parse_args()
root = a.directory.resolve()
if Path(a.frames).name != a.frames or Path(a.name).name != a.name:
    raise ValueError('Use local directory and output basenames')
frames = root / a.frames
out = root / (a.name + '.mp4')
qa_path = root / (a.name + '-qa.json')
if out.exists() or qa_path.exists():
    raise ValueError('Keep retained versions; choose a new output name')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

report = json.loads((frames / 'render-report.json').read_text())
expected = list(range(1, 181))
if [f['frame'] for f in report['frames']] != expected:
    raise ValueError('Need exactly 180 ordered frames')
for f in report['frames']:
    if sha(frames / f"frame_{f['frame']:06d}.png") != f['sha256']:
        raise ValueError('Frame drift since rendering')
started = time.monotonic()
command = ['ffmpeg', '-nostdin', '-v', 'error', '-n', '-framerate', '24',
           '-start_number', '1', '-i', str(frames / 'frame_%06d.png'),
           '-i', str(root / 'sound.wav'), '-t', '7.5', '-threads', '2',
           '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p',
           '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', str(out)]
subprocess.run(command, check=True, timeout=180, capture_output=True)
meta = json.loads(subprocess.check_output(
    ['ffprobe', '-v', 'error', '-count_frames', '-show_streams',
     '-show_format', '-of', 'json', str(out)], timeout=60))
v = next(s for s in meta['streams'] if s['codec_type'] == 'video')
audio = next(s for s in meta['streams'] if s['codec_type'] == 'audio')
checks = {
    'frame_count': int(v['nb_read_frames']) == 180,
    'dimensions': (v['width'], v['height']) == (1280, 720),
    'frame_rate': v['avg_frame_rate'] == '24/1',
    'video_extent': abs(float(v['duration']) - 7.5) < .001,
    'audio_extent': abs(float(audio['duration']) - 7.5) < .05,
    'audio_format': int(audio['sample_rate']) == 48000 and audio['channels'] == 2,
}
decode = subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-i',
                         str(out), '-f', 'null', '-'], capture_output=True, timeout=60)
checks['full_decode'] = decode.returncode == 0 and not decode.stderr
volume = subprocess.run(['ffmpeg', '-nostdin', '-v', 'info', '-i', str(out),
                         '-vn', '-af', 'volumedetect', '-f', 'null', '-'],
                        capture_output=True, text=True, check=True, timeout=60)
levels = [s.strip() for s in volume.stderr.splitlines()
          if 'mean_volume:' in s or 'max_volume:' in s]
qa = {'output_sha256': sha(out), 'source_sha256': report['source_sha256'],
      'sound_sha256': sha(root / 'sound.wav'), 'checks': checks,
      'render_engine': report['engine'], 'executor_admission': False,
      'render_seconds': report['elapsed_seconds'],
      'assembly_and_qa_seconds': time.monotonic() - started,
      'volume_observations': levels, 'human_viewing': 'pending',
      'human_listening': 'pending', 'owner_acceptance': 'pending',
      'publication': 'not_authorised', 'automatic_model_calls': 0}
with qa_path.open('x') as f:
    json.dump(qa, f, indent=2)
    f.write('\n')
if not all(checks.values()):
    raise ValueError('Technical check failed; inspect saved QA before review')
print(json.dumps(qa, indent=2))
