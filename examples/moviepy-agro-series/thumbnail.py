from pathlib import Path
import os
os.environ['FFMPEG_BINARY']=os.environ.get('FFMPEG_BINARY','ffmpeg')
from moviepy import VideoFileClip,ImageClip,ColorClip,CompositeVideoClip
from PIL import Image,ImageDraw,ImageFont
import numpy as np
p=Path(__file__).parent
font='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
def title(t,size,color,pos):
 f=ImageFont.truetype(font,size);b=f.getbbox(t);im=Image.new('RGBA',(b[2]-b[0]+8,b[3]-b[1]+12),(0,0,0,0));ImageDraw.Draw(im).text((4-b[0],6-b[1]),t,font=f,fill=color)
 return ImageClip(np.asarray(im)).with_duration(1).with_position(pos)
v=VideoFileClip(str(Path(os.environ['FRAMEWRIGHT_MEDIA_ROOT'])/'ami-books-landing-pilot-20261015/Screen-Assembly.mp4'),audio=False)
art=ImageClip(v.get_frame(1)).cropped(x1=740,x2=1920,y1=0,y2=1080).resized(width=640).with_duration(1).with_position((640,110))
base=ColorClip((1280,720),color=(7,20,30),duration=1)
film=CompositeVideoClip([base,art,title('AMI BOOKS',26,'#d3ae62',(58,60)),title('REAL MARKETS.',62,'white',(58,205)),title('PRACTICAL BOOKS.',57,'white',(58,295)),title('ONE LIBRARY.',56,'#d3ae62',(58,400)),title('ENGLISH + UKRAINIAN',22,'white',(58,566)),title('books.1d3x.com',25,'#d3ae62',(58,624))],size=(1280,720))
film.save_frame(str(p/'Agro-Library-YouTube.png'),t=0,with_mask=False);film.close();v.close()
im=Image.open(p/'Agro-Library-YouTube.png').convert('RGB');im.save(p/'Agro-Library-YouTube.jpg',quality=94);im.resize((320,180)).save(p/'Thumbnail-reduced.png')
