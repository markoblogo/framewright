from pathlib import Path
import hashlib,json,math,numpy as np,soundfile as sf
import subprocess,textwrap
from synthesize import LINES,validate_rows
from audio_checks import validate_peak
b=Path(__file__).parent;sr=48000;N=32*sr;music=np.zeros((N,2));fx=np.zeros((N,2));voice=np.zeros((N,2));rows=json.loads((b/'audio/voice-lines.json').read_text())
validate_rows(rows,LINES)
def put(dest,start,a,gain=1,pan=0):
 i=round(start*sr);n=min(len(a),N-i)
 if n>0:dest[i:i+n]+=a[:n,None]*gain*np.array([math.sqrt((1-pan)/2),math.sqrt((1+pan)/2)])
for beat in range(64):
 x=np.arange(int(.36*sr))/sr;freq=440*2**(([45,52,57,59,45,52,55,59][beat%8]-69)/12);tone=(np.sin(2*np.pi*freq*x)+.12*np.sin(2*np.pi*freq*2*x))*np.minimum(x/.012,1)*np.exp(-x*10)
 put(music,beat*.5,tone,.055,(-.2 if beat%2 else .2))
 if beat%8==0:
  x=np.arange(int(3.7*sr))/sr;pad=sum(np.sin(2*np.pi*440*2**((n-69)/12)*x) for n in [45,52,57])/3;env=np.minimum(x/.5,1)*np.minimum((3.7-x)/.9,1);put(music,beat*.5,pad*env,.026)
for k,t in enumerate([.6,1,1.4,2.7,4.9,5.35,5.8,10.7,11.4,12.1,12.8,16.8,17.7,18.2,18.7,19.4,22.4]):
 x=np.arange(int(.15*sr))/sr;a=(np.sin(2*np.pi*(430+k*25)*x)+.2*np.sin(2*np.pi*130*x))*np.minimum(x/.002,1)*np.exp(-x*55);put(fx,t,a,.055)
last=0
for r in rows:
 path=b/'audio'/f"{r['id']}.wav"
 if hashlib.sha256(path.read_bytes()).hexdigest()!=r['sha256']:raise ValueError('Voice WAV/metadata mismatch:'+r['id'])
 if r['clipped_samples']:raise ValueError('Clipped raw voice:'+r['id'])
 a,hz=sf.read(b/'audio'/f"{r['id']}.wav");g=math.gcd(sr,hz);a=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',str(b/'audio'/f"{r['id']}.wav"),'-f','f64le','-ac','1','-ar',str(sr),'-'],capture_output=True,check=True).stdout,dtype='<f8');start=round(r['start']*sr);end=start+len(a)
 if start<last or end>N:raise ValueError('Voice overlap or overflow')
 voice[start:end]+=a[:,None];last=end;r['end']=end/sr
 # speech carve in background,including margins
 l=max(0,start-int(.1*sr));z=min(N,end+int(.15*sr));music[l:z]*=.55
fade=np.minimum(np.arange(N)/sr/.35,1)*np.minimum((N-1-np.arange(N))/sr/.4,1);music*=fade[:,None];fx*=fade[:,None]
exports=[('voice-timeline',voice),('music-original',music),('effects-original',fx),('pre-master',voice+music+fx)]
# Check every floating-point stem and their sum before any integer PCM write.
for name,a in exports:
 if not np.isfinite(a).all():raise ValueError('Nonfinite PCM:'+name)
 validate_peak(float(np.max(np.abs(a))))
for name,a in exports:sf.write(b/'audio'/f'{name}.wav',a,sr,subtype='PCM_24')
(b/'audio/voice-lines-timed.json').write_text(json.dumps(rows,indent=2)+'\n')
def stamp(t):
 n=round(t*1000);return f'{n//3600000:02}:{n//60000%60:02}:{n//1000%60:02},{n%1000:03}'
(b/'Contract-Execution-EN.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(r['start'])} --> {stamp(r['end'])}\n{r['text']}" for i,r in enumerate(rows))+'\n')
print('Voice ends',last/sr,'of32 seconds;no overlaps')

p=b/'Contract-Execution-EN.srt';blocks=p.read_text().split('\n\n');p.write_text('\n\n'.join('\n'.join(x.splitlines()[:2]+textwrap.wrap(' '.join(x.splitlines()[2:]).replace('M N seven R.','MN7R.'),56)) for x in blocks if x.strip())+'\n')
