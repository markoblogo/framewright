from pathlib import Path
import json,subprocess
p=Path(__file__).parent
src=p/'capture.mp4'
if __import__('hashlib').sha256(src.read_bytes()).hexdigest()!='05a2d2ffd5342ccea190acd1b89204ad5e831818ed6ac5ae53004eb593c23454':raise ValueError('Different capture:replan and inspect all segment boundaries before editing')
# Selected only after inspecting the source; later black frames are rejected.
segments=[('hero',18,7),('catalogue',38.5,7),('brokerage',51.4,8),('execution',78.2,8),('editions',12,6),('cta',18,6)]
(p/'segments').mkdir(exist_ok=True)
for name,start,seconds in segments:
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(start),'-i',str(src),'-t',str(seconds),'-an','-vf',('trim=duration=0.4,' if name=='execution' else '')+'crop=2498:1444:0:356,scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=white,fps=30,setsar=1'+(',tpad=stop_mode=clone:stop_duration=7.6' if name=='execution' else ''),'-c:v','libx264','-crf','18','-threads','2','-pix_fmt','yuv420p',str(p/'segments'/f'{name}.mp4')],check=True)
(p/'segments/list.txt').write_text(''.join("file '"+str(p/'segments'/f'{n}.mp4')+"'\n" for n,_,_ in segments))
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(p/'segments/list.txt'),'-c','copy',str(p/'Screen-Assembly.mp4')],check=True)
json.dump([dict(scene=n,source_start=s,seconds=d,source_duration=.4 if n=='execution' else d,freeze_seconds=7.6 if n=='execution' else 0) for n,s,d in segments],(p/'scene-map.json').open('w'),indent=2)
