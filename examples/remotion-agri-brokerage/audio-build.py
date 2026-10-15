from pathlib import Path
import json,hashlib,textwrap,subprocess
import numpy as np,soundfile as sf
from synthesize import LINES,validate_rows
b=Path(__file__).parent;sr=48000;voice=np.zeros((30*sr,2));rows=json.loads((b/'audio/voice-lines.json').read_text());validate_rows(rows,LINES);last=0
for r in rows:
 p=b/'audio'/f"{r['id']}.wav"
 if hashlib.sha256(p.read_bytes()).hexdigest()!=r['sha256'] or r['clipped_samples']:raise ValueError('Raw voice mismatch/clipping')
 raw=subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','f32le','-ar',str(sr),'-ac','2','-'],capture_output=True,check=True).stdout
 a=np.frombuffer(raw,dtype='<f4').reshape(-1,2);i=round(r['start']*sr);end=i+len(a)
 if i<last or end>len(voice):raise ValueError('Voice overlap/overflow')
 voice[i:end]=a;last=end;r['end']=end/sr
sf.write(b/'audio/voice-timeline.wav',voice,sr,subtype='PCM_24')
def stamp(t):
 n=round(t*1000);return f'{n//3600000:02}:{n//60000%60:02}:{n//1000%60:02},{n%1000:03}'
(b/'Agri-Brokerage-EN.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(r['start'])} --> {stamp(r['end'])}\n"+'\n'.join(textwrap.wrap(r['text'],56)) for i,r in enumerate(rows))+'\n')
print('Verified voice-only timeline;last speech',last/sr)
