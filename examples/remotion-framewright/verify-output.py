"""Check actual encoded deliverable metadata, not source constants."""
import json
from pathlib import Path
import subprocess
p=Path('outputs/Framewright-Remotion-1080p.mp4')
r=subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)],check=True,capture_output=True,text=True)
a=json.loads(r.stdout)
Path('outputs/ffprobe.json').write_text(r.stdout)
v=next(s for s in a['streams'] if s['codec_type']=='video')
s=next(s for s in a['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1920,1080,'30/1',900)
assert v['codec_name']=='h264' and s['codec_name']=='aac'
assert abs(float(a['format']['duration'])-30)<.1
assert int(s['channels'])==2
print('PASS: H264 1920x1080 30fps / 900 frames / 30 seconds; stereo AAC present')
