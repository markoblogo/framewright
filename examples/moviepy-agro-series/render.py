from pathlib import Path
import os,json,subprocess,time
import numpy as np
from PIL import Image,ImageDraw,ImageFont
os.environ['FFMPEG_BINARY']=os.environ.get('FFMPEG_BINARY','ffmpeg')
from moviepy import VideoFileClip,ImageClip,TextClip,ColorClip,CompositeVideoClip,concatenate_videoclips,vfx
p=Path(__file__).parent;s=json.loads((p/'sources.json').read_text());root=Path(os.environ['FRAMEWRIGHT_MEDIA_ROOT'])
paths={r['id']:str(root/r['local_output']) for r in s}
for row in s:
 if __import__('hashlib').sha256(Path(paths[row['id']]).read_bytes()).hexdigest()!=row['sha256']:raise ValueError('Changed source:'+row['id'])
FONT='/System/Library/Fonts/Supplemental/Arial.ttf';BOLD='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
BG=(7,20,30);GOLD='#d3ae62';scene_dir=p/'scenes';scene_dir.mkdir(exist_ok=True)
DURS=[6,7.5,7.5,7.5,7.5,8.5,10.5,8.5]
TITLES=['The work behind the deal.','Understand the physical market.','Connect people, products and terms.','Turn agreement into execution.','Bring the workflow together.','Practical knowledge. Two languages.','Your next guide is here.','One library. More to come.']
SUBS=['PRACTICAL GUIDES FOR PHYSICAL COMMODITY MARKETS','SPOT-MARKET HANDBOOK · ENGLISH','AGRI-COMMODITY BROKERAGE · ENGLISH','CONTRACT EXECUTION OFFICER HANDBOOK','MN7R PRODUCT GUIDE','ENGLISH + UKRAINIAN EDITIONS','EXPLORE BOOKS.1D3X.COM','BOOKS.1D3X.COM']
all_ids=list(paths)[:6]
def text(t,size=52,color='white',font=BOLD):
 f=ImageFont.truetype(font,size);box=f.getbbox(t)
 im=Image.new('RGBA',(box[2]-box[0]+8,box[3]-box[1]+12),(0,0,0,0))
 ImageDraw.Draw(im).text((4-box[0],6-box[1]),t,font=f,fill=color)
 return ImageClip(np.asarray(im))
def shell(layers,d,i):
 base=ColorClip((1920,1080),color=BG,duration=d)
 head=text('AMI BOOKS',23,GOLD).with_position((80,30)).with_duration(d)
 title=text(TITLES[i],52).with_position((80,78)).with_duration(d)
 sub=text(SUBS[i],22,GOLD,FONT).with_position((80,142)).with_duration(d)
 return CompositeVideoClip([base,head,title,sub]+layers,size=(1920,1080)).with_duration(d)
def vid(eid,t,d,wh):
 v=VideoFileClip(paths[eid],audio=False,target_resolution=wh)
 return v,v.subclipped(t,t+d)
start=time.monotonic();render_metrics=[]
for i,d in enumerate(DURS):
 if os.environ.get('REUSE_SCENES')=='1':continue
 holders=[];layers=[]
 if i==0:
  labels=['SPOT MARKETS','BROKERAGE','EXECUTION','THE WORKSPACE','БРОКЕРИДЖ','СПОТОВИЙ РИНОК']
  for j,eid in enumerate(all_ids):
   v,c=vid(eid,3,d,(560,315));holders.append(v);x=80+j%3*600;y=240+j//3*380
   layers+=[c.with_position((x,y)),text(labels[j],20,GOLD).with_position((x,y+327)).with_duration(d)]
 elif i in [1,2,3,4]:
  eid=all_ids[i-1];t={1:3,2:4,3:5,4:4}[i];v,c=vid(eid,t,d,(1536,864));holders.append(v);layers=[c.with_position((192,190))]
 elif i==5:
  for j,eid in enumerate(all_ids[4:6]):
   v,c=vid(eid,4,d,(880,495));holders.append(v);layers.append(c.with_position((60+j*920,330)))
  layers+=[text('BROKERAGE',27,GOLD).with_position((60,850)).with_duration(d),text('SPOT MARKETS',27,GOLD).with_position((980,850)).with_duration(d)]
 elif i==6:
  v=VideoFileClip(paths['ami-books-openscreen'],audio=False,target_resolution=(1536,864));holders.append(v)
  c=concatenate_videoclips([v.subclipped(7.2,12.45),v.subclipped(14.2,19.45)],method='chain');layers=[c.with_position((192,190))]
 else:
  v=VideoFileClip(paths['ami-books-openscreen'],audio=False,target_resolution=(1536,864));holders.append(v)
  still=ImageClip(v.get_frame(1.5)).with_duration(d).with_position((192,190));layers=[still]
  layers.append(ColorClip((1920,80),color=BG,duration=d).with_position((0,1000)))
  layers.append(text('New titles will join the collection.',30).with_position(('center',1010)).with_duration(d))
 scene=shell(layers,d,i);out=scene_dir/f'{i:02}.mp4';ts=time.monotonic();scene.write_videofile(str(out),fps=30,codec='libx264',audio=False,threads=2,preset='veryfast',ffmpeg_params=['-crf','18','-pix_fmt','yuv420p'],logger=None)
 render_metrics.append({'scene':i,'seconds':d,'wall_seconds':round(time.monotonic()-ts,2)})
 if i==0:scene.save_frame(str(p/'Agro-Library-native-poster.png'),t=1.0)
 scene.close()
 for v in holders:v.close()
 print('scene',i,'complete',flush=True)
clips=[VideoFileClip(str(scene_dir/f'{i:02}.mp4'),audio=False) for i in range(8)]
film=concatenate_videoclips([c if i==0 else c.with_effects([vfx.CrossFadeIn(.5)]) for i,c in enumerate(clips)],method='compose',padding=-.5)
if abs(film.duration-60)>.001:raise ValueError('Transition duration drift')
# Keep editorial headings crisp while picture layers dissolve underneath.
headers=[film,ColorClip((1920,190),color=BG,duration=60)]
starts=[0,5.75,12.75,19.75,26.75,33.75,41.75,51.75]
for i,st in enumerate(starts):
 en=starts[i+1] if i+1<len(starts) else 60
 for layer in [text('AMI BOOKS',23,GOLD).with_position((80,30)),text(TITLES[i],52).with_position((80,78)),text(SUBS[i],22,GOLD,FONT).with_position((80,142))]:headers.append(layer.with_start(st).with_duration(en-st))
film=CompositeVideoClip(headers,size=(1920,1080)).with_duration(60)

film.write_videofile(str(p/'Agro-Library-Picture-1080p.mp4'),fps=30,codec='libx264',audio=False,threads=2,preset='veryfast',ffmpeg_params=['-crf','18','-pix_fmt','yuv420p','-movflags','+faststart'],logger=None)
film.close()
for c in clips:c.close()
(p/('assembly-metrics.json' if os.environ.get('REUSE_SCENES')=='1' else 'render-metrics.json')).write_text(json.dumps({'scenes':render_metrics,'total_wall_seconds':round(time.monotonic()-start,2),'transition_overlap':.5,'duration':60},indent=2))
