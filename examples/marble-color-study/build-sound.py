from pathlib import Path
import json,subprocess,os,numpy as np
P=Path(__file__).resolve().parent;SR=48000;D=42;N=SR*D;T=np.arange(N)/SR;F=os.environ.get('FRAMEWRIGHT_FFMPEG','ffmpeg');rng=np.random.default_rng(20261025)

def decode(src,start=0,filters='anull'):
 cmd=[F,'-v','error','-ss',str(start),'-i',str(src),'-t',str(D),'-af',filters+',apad,atrim=duration=42','-ar',str(SR),'-ac','2','-f','f32le','pipe:1']
 x=np.frombuffer(subprocess.check_output(cmd),dtype='<f4').reshape(-1,2).copy();assert x.shape==(N,2) and np.isfinite(x).all();return x

def write(name,x):
 subprocess.run([F,'-v','error','-y','-f','f32le','-ar',str(SR),'-ac','2','-i','pipe:0','-c:a','pcm_s24le',str(P/'final/sound'/name)],input=np.asarray(x,dtype='<f4').tobytes(),check=True)

def smooth(a,b):
 z=np.clip((T-a)/(b-a),0,1);return (z*z*(3-2*z))[:,None]

def delay(x,s):
 n=round(s*SR);y=np.zeros_like(x);y[n:]=x[:-n];return y

def rms(x):return float(np.sqrt(np.mean(x*x)))

def bandnoise(n,low,high):
 x=rng.normal(size=n);f=np.fft.rfftfreq(n,1/SR);h=(1-np.exp(-(f/low)**4))*np.exp(-(f/high)**4);x=np.fft.irfft(np.fft.rfft(x)*h,n);return x/(rms(x)+1e-9)

piano=decode(P/'sound/source-music.mp3',16)
cold=decode(P/'sound/source-music.mp3',16,'highpass=f=260,lowpass=f=2800')
octave=decode(P/'sound/source-music.mp3',16,'aresample=48000,asetrate=24000,aresample=48000,atempo=2,highpass=f=45,lowpass=f=850')
amb=decode(P/'sound/source-ambience.mp3',8,'highpass=f=140,lowpass=f=6000')
warm=smooth(13,15);red=smooth(25,27.2)
# One retained theme: orchestration changes on the picture's exact cue curve.
isolation=cold+.36*delay(cold,.23)+.17*delay(cold[:,::-1],.49)
shelter=1.25*piano+.35*octave+.22*delay(piano[:,::-1],.17)
anxiety=.32*cold+.80*octave+.16*delay(cold,.33)
score=(isolation*(1-warm)+shelter*warm)*(1-red)+anxiety*red
score*=2.1
# A slow bass texture makes tension grow without a jump-scare or a new unrelated song.
rumble=bandnoise(N,43,155);pulse=.32+.68*((1+np.sin(2*np.pi*1.35*T))*.5)**5
score+=np.column_stack([rumble,rumble])*.013*pulse[:,None]*red
wind=bandnoise(N,170,1400);windr=np.roll(wind,round(.013*SR));env=(.0025+.0045*smooth(26,30))
fx=np.column_stack([wind,windr])*env
# Keep ambience alive early, let it retreat as the traveler notices the danger.
amb*=.010/(rms(amb)+1e-9);amb*=1+.45*warm-.78*red;fx+=amb
contacts=[]
for k,at in enumerate(np.arange(3.0,27.9,.6)):
 n=round(.16*SR);tt=np.arange(n)/SR;crunch=bandnoise(n,370,4200)*np.exp(-tt*35);thump=np.sin(2*np.pi*(82*tt+1.2*(1-np.exp(-tt*18))))*np.exp(-tt*30);step=(crunch*.013+thump*.028)*np.minimum(tt/.006,1)
 start=round(at*SR);pan=np.clip(-.55+(at-3)/25, -.7,.7);lr=np.array([np.cos((pan+1)*np.pi/4),np.sin((pan+1)*np.pi/4)]);fx[start:start+n]+=step[:,None]*lr;contacts.append(round(float(at),2))
# Soft hand/lantern movement at the visible lift; no stock UI click.
at=28.1;n=round(.45*SR);tt=np.arange(n)/SR;ring=sum(np.sin(2*np.pi*f*tt)*np.exp(-tt*(8+i*3))/(i+2) for i,f in enumerate([1740,2327,3190]));ring*=.009*np.minimum(tt/.004,1);start=round(at*SR);fx[start:start+n]+=np.column_stack([ring*.7,ring])
fade=smooth(0,.65)*(1-smooth(39.8,42))
score*=fade;fx*=fade
premix=score+fx
assert np.isfinite(premix).all()
raw_peak=float(np.max(np.abs(premix)));gain=min(1,.75/(raw_peak+1e-12))
score*=gain;fx*=gain;premix=score+fx
assert np.max(np.abs(premix))<1
for name,x in [('score-stem.wav',score),('effects-stem.wav',fx),('premix.wav',premix)]:write(name,x)
# Recombination and mono sum are explicit technical checks, not listening approval.
mono=premix.mean(axis=1);corr=float(np.corrcoef(premix.T)[0,1]);mono_delta=float(20*np.log10((rms(mono)+1e-12)/(rms(premix)+1e-12)))
report={'premix_headroom_gain':gain,'raw_peak_before_headroom':raw_peak,'direction':'video-first','picture_cues':{'warm_crossfade':[13,15],'anxiety_crossfade':[25,27.2],'stop':[27.5,28],'lantern_lift':[27.7,29.2],'music_tail':[39.8,42]},'seconds':D,'sample_rate':SR,'channels':2,'score':'Retained CC BY4.0 ambient piano excerpt16–58s, cohesive filtered/octave/reverb arrangements','ambience':'Retained CC0 night field recording, stylised fiction bed','original_sfx':['procedural soft footsteps','bandlimited tension/wind','lantern handling ring'],'footstep_contacts':contacts,'stem_alignment':'Both stems start at sample0 and contain2016000 samples','recombination_max_error':float(np.max(np.abs((score+fx)-premix))),'stereo_correlation':corr,'mono_rms_delta_db':mono_delta,'peak_before_loudness_dbfs':float(20*np.log10(np.max(np.abs(premix)))),'listening':'pending owner; no model listening claim','new_paid_calls':0}
(P/'final/sound/mix-design.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
