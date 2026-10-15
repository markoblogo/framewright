from pathlib import Path
import os,json,subprocess
p=Path(__file__).parent;ff=os.environ.get('FFMPEG_BINARY','ffmpeg')
r=subprocess.run([ff,'-hide_banner','-i',str(p/'Mix-premaster.wav'),'-af','loudnorm=I=-16:TP=-2.5:LRA=9:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
(p/'loudnorm-measure.txt').write_text(r.stderr);m=json.JSONDecoder().raw_decode(r.stderr[r.stderr.rfind('{'):])[0]
f=f"loudnorm=I=-16:TP=-2.5:LRA=9:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
subprocess.run([ff,'-hide_banner','-loglevel','error','-y','-i',str(p/'Mix-premaster.wav'),'-af',f,'-ar','48000','-ac','2','-c:a','pcm_s24le',str(p/'Soundtrack-master.wav')],check=True)
subprocess.run([ff,'-hide_banner','-loglevel','error','-y','-i',str(p/'Agro-Library-Picture-1080p.mp4'),'-i',str(p/'Soundtrack-master.wav'),'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-t','60','-movflags','+faststart',str(p/'Agro-Library-1080p.mp4')],check=True)
