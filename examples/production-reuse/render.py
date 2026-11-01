#!/usr/bin/env python3
"""Source-preserving photo/clip montage, explicit crops and frozen copy per aspect.
Requires an explicit private plan; no network, model download or publication.
"""
import argparse,json,hashlib,subprocess,time,shutil,runpy
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
FONT='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def label(path,title,subtitle,w,h):
 image=Image.new('RGBA',(w,h));d=ImageDraw.Draw(image);size=round(w*.052 if w>h else w*.085);font=ImageFont.truetype(FONT,size)
 maxw=w-2*int(w*.065)-16;words=title.split();lines=[];line=''
 for word in words:
  if line and d.textlength(line+' '+word,font=font)>maxw:lines.append(line);line=word
  else:line=(line+' '+word).strip()
 if line:lines.append(line)
 while (len(lines)>3 or any(d.textlength(x,font=font)>maxw for x in lines) or (h*.72 if w>h else h*.74)+size*1.14*len(lines)+h*.09>h*.94) and size>18:
  size-=2;font=ImageFont.truetype(FONT,size);lines=[];line=''
  for word in words:
   if line and d.textlength(line+' '+word,font=font)>maxw:lines.append(line);line=word
   else:line=(line+' '+word).strip()
  if line:lines.append(line)
 if len(lines)>3 or any(d.textlength(line,font=font)>maxw for line in lines):raise ValueError('Title exceeds template bound')
 subfont=ImageFont.truetype(FONT,max(16,round(size*.38)))
 if subtitle and d.textlength(subtitle,font=subfont)>maxw:raise ValueError('Subtitle exceeds template bound')
 x=int(w*.065);y=int(h*.72 if w>h else h*.74);height=int((size*1.14)*len(lines)+h*.09)
 if y+height>h*.94:raise ValueError('Caption exceeds safe area')
 d.rounded_rectangle((x-12,y-12,w-x,y+height),radius=9,fill=(5,12,20,225));d.rectangle((x-12,y-12,x-6,y+height),fill='#219cfa')
 for line in lines:d.text((x+8,y),line,font=font,fill='#f2f5f8');y+=round(size*1.14)
 if subtitle:d.text((x+8,y+10),subtitle,font=subfont,fill='#d6e4ed')
 image.save(path)
 return {'title_lines':len(lines),'font_size':size,'safe_area':True,'subtitle_present':bool(subtitle)}
def render(plan,root,aspect,enforce_caption_timing=False):
 d=json.loads(plan.read_text())
 if enforce_caption_timing:
  timing=runpy.run_path(str(Path(__file__).with_name('caption_timing.py')))['inspect'](d,24)
  failed=[str(x['shot']) for x in timing['shots'] if x['status']!='pass']
  if failed:raise ValueError('Caption reading time too short in shot(s) '+', '.join(failed)+'; shorten copy or explicitly replan timing and narration')
 w,h=(1280,720) if aspect=='16x9' else (720,1280);out=root.resolve()/aspect
 if out.exists():raise ValueError('Use a new output directory')
 out.mkdir(parents=True);timings=[];parts=[];sources={}
 def run(args,stage):
  t=time.monotonic();p=subprocess.run(args,capture_output=True,text=True,timeout=180)
  if p.returncode:raise ValueError(stage+': '+p.stderr[-1500:])
  timings.append({'stage':stage,'elapsed_seconds':round(time.monotonic()-t,3)})
  (out/'progress.json').write_text(json.dumps({'timings':timings,'completed_stage':stage},indent=2)+'\n')
 for i,s in enumerate(d['shots']):
  media=Path(s['file']);sources[str(media)]=sha(media);seconds=s['duration'];overlay=out/f'copy-{i}.png';label(overlay,s['title'],s.get('subtitle',''),w,h)
  args=['ffmpeg','-v','error','-nostdin','-threads','2','-filter_complex_threads','1']
  if s['kind']=='photo':args+=['-loop','1','-framerate','24']
  else:args+=['-ss',str(s.get('offset',0))]
  args+=['-i',str(media),'-loop','1','-i',str(overlay)]
  # All sources cover the canvas; animated crop retains the original artwork pixels.
  frames=round(seconds*24)
  if s['kind']=='photo':
   filt=f"[0:v]scale={w*2}:{h*2}:force_original_aspect_ratio=increase,crop={w*2}:{h*2},zoompan=z='1.02+0.06*on/{frames}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s={w}x{h}:fps=24[v]"
  else:filt=f"[0:v]fps=24,scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}[v]"
  dest=out/f'part-{i}.mp4';filt+=f';[v][1:v]overlay=0:0:shortest=1,fade=t=in:st=0:d=0.2,fade=t=out:st={max(0,seconds-.2)}:d=0.2,format=yuv420p[out]'
  args+=['-filter_complex',filt,'-map','[out]','-an','-t',str(seconds),'-c:v','libx264','-preset','veryfast','-crf','19','-threads','2',str(dest)]
  run(args,'shot-'+str(i));parts.append(dest)
 (out/'parts.txt').write_text(''.join("file '"+str(f)+"'\n" for f in parts))
 total=sum(s['duration'] for s in d['shots']);master=out/'one-artist-two-cities.mp4'
 voice=Path(d['voice']);score=Path(d['score']);sources[str(voice)]=sha(voice);sources[str(score)]=sha(score)
 run(['ffmpeg','-v','error','-nostdin','-threads','2','-filter_complex_threads','1','-f','concat','-safe','0','-i',str(out/'parts.txt'),'-i',str(voice),'-i',str(score),'-filter_complex',f'[1:a]apad,atrim=duration={total}[voice];[2:a]atrim=duration={total},volume=0.20,afade=t=out:st={total-2}:d=2[music];[voice][music]amix=inputs=2:normalize=0,loudnorm=I=-17:TP=-1.2:LRA=10[a]','-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-t',str(total),'-movflags','+faststart',str(master)],'assemble')
 run(['ffmpeg','-v','error','-i',str(master),'-f','null','-'],'full-decode')
 if any(sha(path)!=value for path,value in sources.items()):raise ValueError('Source changed during production')
 report={'aspect':aspect,'resolution':[w,h],'duration_seconds':total,'fps':24,'sha256':sha(master),'sources':sources,'timings':timings,'source_audio_used':False,'creative_review':'pending','listening_review':'pending','publication_authorized':False,'reuse_scope':d['reuse_scope']}
 (out/'render.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'file':str(master),'duration':total,'stages':timings}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('plan',type=Path);p.add_argument('output',type=Path);p.add_argument('--aspect',choices=['16x9','9x16'],required=True);p.add_argument('--enforce-caption-timing',action='store_true',help='Reject too-short English copy before creating outputs; no automatic retiming');a=p.parse_args();render(a.plan,a.output,a.aspect,a.enforce_caption_timing)
