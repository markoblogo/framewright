from pathlib import Path
import json,hashlib,math
import numpy as np
import soundfile as sf
import subprocess
p=Path(__file__).parent
rows=json.loads((p/'audio/voice-lines.json').read_text())
if len(rows)!=6 or [r['id'] for r in rows]!=['opening','library','brokerage','execution','languages','cta']:raise ValueError('Incomplete voice manifest')
a=np.zeros(42*48000);srt=[]
def stamp(t):
 ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000);return f'{h:02}:{m:02}:{s:02},{ms:03}'
for i,r in enumerate(rows):
 f=p/'audio'/f"{r['id']}.wav"
 if hashlib.sha256(f.read_bytes()).hexdigest()!=r['sha256']:raise ValueError('Changed voice WAV')
 x=np.frombuffer(subprocess.check_output(['ffmpeg','-hide_banner','-loglevel','error','-i',str(f),'-ar','48000','-ac','1','-f','f32le','-']),dtype='<f4');start=round(r['start']*48000)
 if start+len(x)>len(a):raise ValueError('Voice exceeds film')
 a[start:start+len(x)]+=x
 srt.append(f"{i+1}\n{stamp(r['start'])} --> {stamp(r['start']+len(x)/48000)}\n{r['text']}\n")
sf.write(p/'Narration-raw.wav',np.column_stack([a,a]),48000,subtype='PCM_24');(p/'AMI-Books-English.srt').write_text('\n'.join(srt))
