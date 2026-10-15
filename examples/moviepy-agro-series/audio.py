from pathlib import Path
import os,json,hashlib
os.environ['FFMPEG_BINARY']=os.environ.get('FFMPEG_BINARY','ffmpeg')
from moviepy import AudioFileClip,CompositeAudioClip,afx
from synthesize import v as pinned_voice
from inputs import verified_input
p=Path(__file__).parent;r=json.loads((p/'audio/voice-lines.json').read_text())
expected=['opening','market','brokerage','execution','workspace','languages','library','future']
if [(x['id'],x['text'],x['start']) for x in r]!=pinned_voice.LINES:raise ValueError('Incomplete or mismatched narration manifest')
opened=[];tracks=[];srt=[]
def stamp(t):
 ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000);return f'{h:02}:{m:02}:{s:02},{ms:03}'
for i,row in enumerate(r):
 f=p/'audio'/f"{row['id']}.wav"
 if hashlib.sha256(f.read_bytes()).hexdigest()!=row['sha256']:raise ValueError('Changed speech WAV')
 if row['start']+row['seconds']>60:raise ValueError('Speech overrun')
 if i+1<len(r) and row['start']+row['seconds']>r[i+1]['start']:raise ValueError('Speech overlap')
 a=AudioFileClip(str(f),fps=48000);opened.append(a);tracks.append(a.with_start(row['start']))
 srt.append(f"{i+1}\n{stamp(row['start'])} --> {stamp(row['start']+row['seconds'])}\n{row['text']}\n")
bed=verified_input('music',os.environ['FRAMEWRIGHT_MEDIA_ROOT']);a=AudioFileClip(str(bed),fps=48000);opened.append(a);music=a.with_effects([afx.AudioLoop(duration=60),afx.MultiplyVolume(.18),afx.AudioFadeIn(1),afx.AudioFadeOut(2)])
mix=CompositeAudioClip(tracks+[music]).with_duration(60);mix.write_audiofile(str(p/'Mix-premaster.wav'),fps=48000,codec='pcm_s24le',logger=None);mix.close()
for a in opened:a.close()
(p/'Agro-Library-English.srt').write_text('\n'.join(srt));(p/'music-provenance.json').write_text(json.dumps({'source':str(bed),'sha256':hashlib.sha256(bed.read_bytes()).hexdigest(),'rights':'original author-project instrumental stem;owner-authorised reuse','volume_multiplier':.18,'new_music_generation':False},indent=2))
