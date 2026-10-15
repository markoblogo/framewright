from pathlib import Path
import subprocess,json
p=Path(__file__).parent;t=(p/'loudnorm-measure.txt').read_text();m=json.JSONDecoder().raw_decode(t[t.rfind('{'):])[0];f=f"loudnorm=I=-16:TP=-2:LRA=9:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(p/'Narration-raw.wav'),'-af',f,'-ar','48000','-c:a','pcm_s24le',str(p/'Narration-master.wav')],check=True)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(p/'AMI-Books-OpenScreen-native.mp4'),'-an','-vf','fps=30','-c:v','libx264','-threads','2','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(p/'AMI-Books-Picture-1080p.mp4')],check=True)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(p/'AMI-Books-Picture-1080p.mp4'),'-i',str(p/'Narration-master.wav'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-t','42','-movflags','+faststart',str(p/'AMI-Books-1080p.mp4')],check=True)
