"""Assemble an explicit, local narrative rough cut from retained frames. No publication."""
import argparse,hashlib,json,math,random,struct,subprocess,wave
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser();p.add_argument('directory',type=Path);p.add_argument('--hero',required=True);p.add_argument('--frames',required=True);p.add_argument('--name',required=True);p.add_argument('--patch',type=Path);p.add_argument('--score',type=Path);a=p.parse_args();r=a.directory.resolve();out=r/a.name
if out.exists():raise ValueError('New output directory required')
out.mkdir();order=[('ground',2),('rain',2),('S02',3),('S03',3),('hero',7.5),('S05',4),('roof',7),('water',5),('recover',7),('up',8)];segments=[];sources=[]
def call(cmd):
 z=subprocess.run(cmd,capture_output=True,text=True,timeout=240)
 if z.returncode:raise RuntimeError(z.stderr[-2000:])
 return z.stdout
for name,duration in order:
 target=out/(name+'.mp4');segments.append(target)
 if name=='hero':
  path=r/a.hero;call(['ffmpeg','-v','error','-nostdin','-n','-i',str(path),'-an','-c:v','copy',str(target)]);sources.append({'shot':name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()});continue
 folder=(r/'film-patch-v6/S03') if name=='S03' else (r/'film-render-v4'/name if name.startswith('S') else r/a.frames/name)
 if a.patch and (a.patch/name).is_dir():folder=a.patch/name
 files=sorted(folder.glob('frame_*.png'));expected={'S02':48,'S03':36,'S05':60}.get(name,round(duration*12))
 if len(files)!=expected or [x.name for x in files]!=[f'frame_{i:06d}.png' for i in range(1,expected+1)]:raise ValueError('Incomplete frame sequence '+name)
 actual=[hashlib.sha256(x.read_bytes()).hexdigest() for x in files]
 report=json.loads((folder.parent/'render-report.json').read_text());row=next(x for x in report['shots'] if x['shot']==name)
 if actual!=[x['sha256'] for x in row['frames']]:raise ValueError('Retained frame hash drift '+name)
 sources.append({'shot':name,'frames':expected,'sha256':actual})
 filt=f'setpts={duration/(expected/12):.8f}*PTS,scale=1280:720:flags=lanczos,fps=24'
 if name=='ground':filt+=',fade=t=in:st=0:d=0.35'
 if name=='up':
  im=Image.new('RGBA',(1280,720));d=ImageDraw.Draw(im);font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Georgia Bold.ttf',96);text='The Last Seed';box=d.textbbox((0,0),text,font=font);d.text(((1280-box[2])/2,295),text,font=font,fill=(12,26,30,255),stroke_width=1,stroke_fill=(230,240,230,255));im.save(out/'title.png')
  cmd=['ffmpeg','-v','error','-nostdin','-n','-framerate','12','-i',str(folder/'frame_%06d.png'),'-loop','1','-i',str(out/'title.png'),'-filter_complex_threads','1','-filter_complex',f"[0:v]{filt}[v];[v]fade=t=out:st=5.7:d=1.7:color=white[sky];[sky][1:v]overlay=0:0:enable='gte(t,4.6)',fade=t=out:st=7.4:d=0.6:color=white"]
 else:cmd=['ffmpeg','-v','error','-nostdin','-n','-framerate','12','-i',str(folder/'frame_%06d.png'),'-vf',filt]
 cmd+=['-frames:v',str(round(duration*24)),'-threads','2','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-an',str(target)];call(cmd)
# Original restrained score and authored event sounds; no external music or speech.
rate=48000;total=48.5;rng=random.Random(3010);low=0;peak=0
if not a.score:
 with wave.open(str(r/'sound.wav'),'rb') as f:
  if (f.getnchannels(),f.getsampwidth(),f.getframerate())!=(2,2,rate):raise ValueError('Unexpected retained sound format')
  pilot=f.readframes(f.getnframes())
 with wave.open(str(out/'sound.wav'),'wb') as f:
  f.setparams((2,2,rate,0,'NONE',''));chunk=bytearray()
  for i in range(round(rate*total)):
   t=i/rate;noise=rng.uniform(-1,1);low=.98*low+.02*noise;env=max(0,min(1,t/.4,(total-t)/1.4));warm=max(0,min(1,(t-33.5)/7));rain=.009 if t<28.5 else .016
   v=rain*(noise-low)+.012*low+.003*math.sin(math.tau*130.81*t)+.003*warm*math.sin(math.tau*196*t)+.004*warm*math.sin(math.tau*261.63*t)
   dt=t-21.5
   if 0<=dt<5.2:
    jam=1.6<=dt<3.1;v+=(.025 if jam else .014)*math.sin(math.tau*(73+9*math.sin(dt*10))*dt)*(1+.3*math.sin(dt*45))
    v+=.009*noise*(.5+.5*math.sin(dt*63))
   for at,amp,freq,decay in [(26.7,.11,510,45),(29.37,.07,1300,26),(30.62,.065,1600,24),(31.87,.06,1900,25)]:
    q=t-at
    if 0<=q<.3:v+=amp*math.exp(-q*decay)*(math.sin(math.tau*freq*q)+.25*noise)
   left=right=0
   if 10<=t<17.5:left,right=struct.unpack_from('<hh',pilot,(i-rate*10)*4);left/=32768;right/=32768
   left=env*(left+v);right=env*(right+v*.97+.002*low);peak=max(peak,abs(left),abs(right))
   if peak>=1:raise ValueError('Audio clipped')
   chunk.extend(struct.pack('<hh',round(left*32767),round(right*32767)))
   if len(chunk)>=192000:f.writeframes(chunk);chunk.clear()
  if chunk:f.writeframes(chunk)
if a.score:
 import shutil
 with wave.open(str(a.score),'rb') as f:
  if (f.getframerate(),f.getnchannels(),f.getsampwidth(),f.getnframes())!=(48000,2,2,round(total*48000)):raise ValueError('Score extent/format mismatch')
 shutil.copy2(a.score,out/'sound.wav')
 with wave.open(str(a.score),'rb') as f:
  data=f.readframes(f.getnframes());peak=max(abs(x[0]) for x in struct.iter_unpack('<h',data))/32768
concat=out/'concat.txt';concat.write_text(''.join("file '"+str(x).replace("'","'\\''")+"'\n" for x in segments));final=out/'the-last-seed-recovery.mp4'
call(['ffmpeg','-v','error','-nostdin','-n','-f','concat','-safe','0','-i',str(concat),'-i',str(out/'sound.wav'),'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-t',str(total),'-movflags','+faststart',str(final)])
meta=json.loads(call(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(final)]));v=next(x for x in meta['streams'] if x['codec_type']=='video');au=next(x for x in meta['streams'] if x['codec_type']=='audio');call(['ffmpeg','-v','error','-xerror','-i',str(final),'-f','null','-'])
checks={'full_decode':True,'duration':abs(float(v['duration'])-total)<.001,'frames':int(v['nb_read_frames'])==1164,'720p24':(v['width'],v['height'],v['avg_frame_rate'])==(1280,720,'24/1'),'48k_stereo':(au['sample_rate'],au['channels'])==('48000',2)}
if not all(checks.values()):raise ValueError(checks)
qa={'checks':checks,'duration_seconds':total,'peak_linear':peak,'sources':sources,'shots':order,'sha256':hashlib.sha256(final.read_bytes()).hexdigest(),'status':'rough_cut','native_new_shots':'960x540 at12fps; upscaled/frame repeated for draft only','soundtrack':'separately retained event-scored music and Foley' if a.score else 'original flat bed','human_visual_acceptance':'pending','human_listening':'pending','publication':'not_authorised','executor_admission':False}
(out/'qa.json').write_text(json.dumps(qa,indent=2)+'\n');print(json.dumps({k:v for k,v in qa.items() if k!='sources'},indent=2))
