"""Assemble the authorised revised local rough cut; no publishing."""
from pathlib import Path
import argparse,json,subprocess,hashlib,math,random,wave,struct
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser();p.add_argument('directory',type=Path);p.add_argument('--frames',default='film-render-v4');p.add_argument('--name',default='film-draft-v2');p.add_argument('--patch',type=Path);a=p.parse_args();r=a.directory.resolve();source=r/a.frames;out=r/a.name
if out.exists():raise ValueError('Use a new draft revision')
out.mkdir();report=json.loads((source/'render-report.json').read_text());by={s['shot']:s for s in report['shots']}
if a.patch:
 patch=json.loads((a.patch/'render-report.json').read_text())
 for row in patch['shots']:by[row['shot']]=row
 report['elapsed_seconds']+=patch['elapsed_seconds']
order=[('S01',3),('S02',4),('S03',3),('S04',7.5),('S05',5),('S06',7.5),('S07',5),('S08',5)];segments=[]
def call(cmd,timeout=180):
 z=subprocess.run(cmd,capture_output=True,text=True,timeout=timeout)
 if z.returncode:raise RuntimeError(z.stderr[-2500:])
 return z.stdout
font='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
def text_image(name,text,size,y):
 im=Image.new('RGBA',(1280,720));d=ImageDraw.Draw(im);f=ImageFont.truetype(font,size);box=d.textbbox((0,0),text,font=f);x=(1280-box[2])/2
 d.rounded_rectangle((x-28,y-14,x+box[2]+28,y+box[3]+18),radius=10,fill=(0,0,0,205));d.text((x,y),text,font=f,fill=(255,255,245,255));path=out/(name+'.png');im.save(path);return path
for shot,dur in order:
 target=out/(shot+'.mp4');segments.append(target)
 if shot=='S04':
  call(['ffmpeg','-v','error','-nostdin','-n','-i',str(r/'pilot-grain-v1.mp4'),'-an','-c:v','copy',str(target)])
  def streamhash(path):return call(['ffmpeg','-v','error','-i',str(path),'-map','0:v:0','-c:v','copy','-f','hash','-hash','sha256','-']).strip()
  if streamhash(target)!=streamhash(r/'pilot-grain-v1.mp4'):raise ValueError('Pilot packet drift')
  continue
 row=by[shot];folder=a.patch/shot if a.patch and (a.patch/shot).is_dir() else source/shot;expected=round(dur*12)
 if [f['frame'] for f in row['frames']]!=list(range(1,expected+1)):raise ValueError('Incomplete shot '+shot)
 for f in row['frames']:
  if hashlib.sha256((folder/f"frame_{f['frame']:06d}.png").read_bytes()).hexdigest()!=f['sha256']:raise ValueError('Frame drift')
 cmd=['ffmpeg','-v','error','-nostdin','-n','-framerate','12','-i',str(folder/'frame_%06d.png')]
 base='scale=1280:720:flags=lanczos,fps=24'
 if shot in ('S02','S03','S08'):
  title={'S02':'One seed left.','S03':'The last water.','S08':'The Last Seed'}[shot];png=text_image(shot,title,82 if shot=='S08' else 52,160 if shot=='S08' else (60 if shot=='S03' else 595))
  cmd+=['-loop','1','-i',str(png)]
  enable="between(t,0.7,5)" if shot=='S08' else "between(t,0.15,2.8)"
  filt=f'[0:v]{base}[v];[v][1:v]overlay=0:0:enable=\'{enable}\''
  if shot=='S08':filt+=',fade=t=out:st=4:d=1'
  cmd+=['-filter_complex_threads','1','-filter_complex',filt]
 else:cmd+=['-vf',base+(',fade=t=in:st=0:d=0.6' if shot=='S01' else '')]
 cmd+=['-frames:v',str(round(dur*24)),'-threads','2','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-an','-movflags','+faststart',str(target)];call(cmd)
# Controlled original ambience. Preserve the approved pilot WAV at unity gain.
rate=48000;rng=random.Random(29);low=0;peak=0
with wave.open(str(r/'sound.wav'),'rb') as f:
 assert f.getframerate()==rate and f.getnchannels()==2 and f.getsampwidth()==2
 pilot=f.readframes(f.getnframes())
audio=out/'draft-sound.wav'
with wave.open(str(audio),'wb') as f:
 f.setparams((2,2,rate,0,'NONE',''));chunk=bytearray()
 for i in range(rate*40):
  t=i/rate;low=.985*low+.015*rng.uniform(-1,1)
  if 10<=t<17.5:
   n=i-rate*10;l,rr=struct.unpack_from('<hh',pilot,n*4);chunk.extend(struct.pack('<hh',l,rr));peak=max(peak,abs(l)/32768,abs(rr)/32768)
  else:
   env=min(1,t/.6,(40-t)/1.2)
   if t<10:env*=min(1,(10-t)/.25)
   else:env*=min(1,(t-17.5)/.3)
   dawn=max(0,min(1,(t-22.5)/7.5));hum=max(0,1-max(0,t-18)/4.5)
   v=env*(.027*low+.007*math.sin(2*math.pi*130.81*t)+.005*math.sin(2*math.pi*196*t)+.004*hum*math.sin(2*math.pi*61*t)+.006*dawn*math.sin(2*math.pi*261.63*t))
   for when in [3.1,5.9,7.3]:
    dt=t-when
    if 0<=dt<.13:v+=.025*rng.uniform(-1,1)*math.exp(-dt*35)
   l=int(v*32767);rr=int((v*.97+.0015*low)*32767);chunk.extend(struct.pack('<hh',l,rr));peak=max(peak,abs(l)/32768,abs(rr)/32768)
  if len(chunk)>=192000:f.writeframes(chunk);chunk.clear()
 if chunk:f.writeframes(chunk)
concat=out/'concat.txt';concat.write_text(''.join("file '"+str(p).replace("'","'\\''")+"'\n" for p in segments))
final=out/'the-last-seed-rough-cut.mp4';call(['ffmpeg','-v','error','-nostdin','-n','-f','concat','-safe','0','-i',str(concat),'-i',str(audio),'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-t','40','-movflags','+faststart',str(final)])
meta=json.loads(call(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(final)]));v=next(s for s in meta['streams'] if s['codec_type']=='video');au=next(s for s in meta['streams'] if s['codec_type']=='audio')
call(['ffmpeg','-v','error','-xerror','-i',str(final),'-f','null','-'])
checks={'full_decode':True,'duration_40s':abs(float(v['duration'])-40)<.001,'frames960':int(v['nb_read_frames'])==960,'format720p24':v['width']==1280 and v['height']==720 and v['avg_frame_rate']=='24/1','audio48k_stereo':au['sample_rate']=='48000' and au['channels']==2,'source_frame_hashes':True,'revised_pilot_bitstream_preserved_in_segment':True}
if not all(checks.values()):raise ValueError(checks)
qa={'id':a.name,'stage':'rough_cut_not_final','checks':checks,'native_new_shots':'960x540/12fps/8samples; upscaled and frame-repeated to720p24 for draft assembly','pilot_revision':'New pointed grain/hardware render with original7.5s action timing; original WAV placed at10s at unity gain. Revised picture pending approval','original_audio_peak_linear':peak,'render_seconds':report['elapsed_seconds'],'output_sha256':hashlib.sha256(final.read_bytes()).hexdigest(),'human_viewing':'pending','human_listening':'pending','creative_acceptance':'pending','publication':'not_authorised','manual_eevee':True,'shots':order}
(out/'qa.json').write_text(json.dumps(qa,indent=2)+'\n');print(json.dumps(qa,indent=2))
