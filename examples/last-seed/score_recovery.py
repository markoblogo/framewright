"""Original event-scored instrumental and licensed mechanical Foley, separate stems."""
import argparse,json,subprocess,wave,hashlib
from pathlib import Path
import numpy as np
p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('sfx',type=Path);p.add_argument('output',type=Path);a=p.parse_args();a.output.mkdir(exist_ok=False);sr=48000;duration=48.5;N=round(sr*duration);rng=np.random.default_rng(3011);music=np.zeros((N,2),np.float64);sfx=np.zeros_like(music);events=[]
def put(dest,signal,start,gain=1,pan=0):
 at=round(start*sr);length=min(len(signal),len(dest)-at)
 if at<0 or length<=0:return
 if signal.ndim==1:signal=np.column_stack((signal*(1-.3*pan),signal*(1+.3*pan)))
 dest[at:at+length]+=signal[:length]*gain

def piano(note,start,length=4,gain=.025,pan=0):
 t=np.arange(round(length*sr))/sr;freq=440*2**((note-69)/12);v=np.zeros(len(t))
 for h,amp in [(1,1),(2,.32),(3,.12),(4,.07),(6,.025)]:v+=amp*np.sin(2*np.pi*freq*h*(1+.00012*h*h)*t)*np.exp(-t*(.65+.28*h))
 v*=np.minimum(1,t/.012)*np.minimum(1,(length-t)/.28);put(music,v,start,gain,pan);events.append({'instrument':'soft_piano','note':note,'time':start})

def strings(notes,start,length,gain=.015,tension=False):
 t=np.arange(round(length*sr))/sr;v=np.zeros(len(t));v2=np.zeros(len(t));attack=np.minimum(1,t/(.8 if tension else 1.6));release=np.minimum(1,(length-t)/1.0);env=np.maximum(0,attack*release)
 if tension:env*=.45+.55*(t/length);env*=.74+.26*np.sin(2*np.pi*(5.2+.3*t)*t)
 for note in notes:
  f=440*2**((note-69)/12)
  for h in [1,2,3,4,5]:
   amp=1/h**1.8;v+=amp*np.sin(2*np.pi*f*h*t+.012*np.sin(2*np.pi*4.7*t));v2+=amp*np.sin(2*np.pi*f*h*1.0012*t+.014*np.sin(2*np.pi*4.9*t))
 put(music,np.column_stack((v,v2))*env[:,None],start,gain/len(notes));events.append({'instrument':'bowed_tension' if tension else 'soft_strings','notes':notes,'time':start,'length':length})
# Sparse minor opening, a tentative sprout, threatened survival, then a warm release.
strings([36,43,51],0,10,.018)
for note,start in [(48,.5),(55,3.4),(51,6.2),(50,8.3)]:piano(note,start,4,.028,-.25)
strings([48,55,62],10,7.5,.018)
for note,start in [(63,11.2),(67,13.4),(70,15.2)]:piano(note,start,3,.025,.18)
strings([34,41,49],17.5,4.1,.019)
strings([36,37,54],21.0,5.7,.030,True)
for note,start in [(36,21.6),(37,23.1),(42,24.6)]:piano(note,start,2,.022,-.18)
strings([48,55,64],28.2,6.3,.023)
for note,start in [(64,28.6),(67,30.1),(72,31.9),(74,33.1)]:piano(note,start,4.2,.033,.2)
strings([48,55,60,64],33.5,8,.029)
strings([48,53,60,64],40.0,5.5,.027)
strings([48,55,62,64],44,4.5,.026)
for note,start in [(67,34.2),(72,36.0),(76,37.8),(74,40.6),(72,42.6),(67,44.3),(72,45.8)]:piano(note,start,4,.031,(note%3-1)*.35)
# Soft stereo room tail, with headroom and a deliberate breath after the release click.
for delay,gain,swap in [(.113,.17,True),(.283,.13,False),(.467,.09,True),(.733,.06,False)]:
 shift=round(delay*sr);music[shift:]+=music[:-shift,::-1 if swap else 1].copy()*gain
full_t=np.arange(N)/sr;duck=1-.50*np.exp(-((full_t-26.85)/.43)**2);fade=np.minimum(1,full_t/.6)*np.minimum(1,(duration-full_t)/2.2);music*=np.maximum(0,duck*fade)[:,None]
# Recorded Foley: decode preview derivatives to retained local PCM; licence/author manifest stays beside sources.
def decode(path):
 raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-ar',str(sr),'-ac','2','-f','f32le','-']);return np.frombuffer(raw,np.float32).reshape(-1,2).astype(np.float64)
def normalise(x):return x/max(.0001,float(np.max(np.abs(x))))
def slowed(x,factor):
 pos=np.arange(0,len(x)-1,factor);return np.column_stack([np.interp(pos,np.arange(len(x)),x[:,ch]) for ch in range(2)])
creak=normalise(slowed(decode(a.sfx/'metal-door-creak.mp3'),.78));ratchet=normalise(slowed(decode(a.sfx/'creaky-ratchet.mp3'),.87))
def clip(x,length):
 y=x[:round(length*sr)].copy();n=len(y);edge=np.minimum(1,np.arange(n)/(.025*sr))*np.minimum(1,(n-np.arange(n))/(.055*sr));return y*edge[:,None]
put(sfx,clip(creak,1.6),21.5,.14);put(sfx,clip(ratchet,1.6),21.5,.12)
put(sfx,clip(creak[round(.6*sr):],1.3),23.15,.10);put(sfx,clip(ratchet[round(2*sr):],2.1),24.6,.16);put(sfx,clip(creak,2.1),24.6,.14)
# Rain and contact foley are authored, deterministic noise/ticks; retained pilot effects remain untouched.
noise=rng.normal(0,1,N);rain=np.column_stack((noise,np.roll(noise,353)))*(.0025+.0025*(full_t>28.5))[:,None];sfx+=rain
with wave.open(str(a.root/'sound.wav'),'rb') as f:
 if (f.getframerate(),f.getnchannels(),f.getsampwidth())!=(sr,2,2):raise ValueError('Unexpected pilot PCM')
 pilot=np.frombuffer(f.readframes(f.getnframes()),'<i2').reshape(-1,2).astype(float)/32768
put(sfx,pilot,10,.90)
for at,gain in [(26.7,.17),(29.35,.07),(30.55,.055),(31.92,.06)]:
 t=np.arange(round(.16*sr))/sr;v=(rng.normal(0,1,len(t))*.7+np.sin(2*np.pi*(1600 if at>28 else 330)*t)) * np.exp(-t*(40 if at>28 else 70));put(sfx,v,at,gain)
sfx*=np.maximum(0,np.minimum(1,full_t/.2)*np.minimum(1,(duration-full_t)/.8))[:,None]
for name,signal in [('music',music),('effects',sfx),('mix',music+sfx)]:
 peak=float(np.max(np.abs(signal)))
 if peak>=.98:raise ValueError(f'{name} clips: {peak}')
 with wave.open(str(a.output/(name+'.wav')),'wb') as f:f.setparams((2,2,sr,0,'NONE',''));f.writeframes((signal*32767).astype('<i2').tobytes())
report={'duration':duration,'sample_rate':sr,'channels':2,'music':'original local composition; soft piano and bowed synthetic strings','sections':[{'start':0,'mood':'loneliness/exhaustion'},{'start':10,'mood':'tentative hope'},{'start':17.5,'mood':'loss/decline'},{'start':21.5,'mood':'threat/tension'},{'start':26.7,'mood':'release/breath'},{'start':28.5,'mood':'relief/renewed hope'}],'events':events,'foley':json.loads((a.sfx/'manifest.json').read_text()),'peak_linear':float(np.max(np.abs(music+sfx))),'sha256':{name:hashlib.sha256((a.output/(name+'.wav')).read_bytes()).hexdigest() for name in ['music','effects','mix']},'human_listening':'pending'}
(a.output/'score.json').write_text(json.dumps(report,indent=2)+'\n');print('audio_peak',report['peak_linear'])
