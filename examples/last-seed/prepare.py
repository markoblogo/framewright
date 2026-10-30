"""Prepare the authorised pilot locally; no renderer or provider is launched here."""
import argparse
import json
import math
import os
from pathlib import Path
import random
import shutil
import struct
import subprocess
import sys
import wave

ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'skills/video-production-router/scripts'
p=argparse.ArgumentParser();p.add_argument('directory',type=Path);p.add_argument('--blender',type=Path,required=True);a=p.parse_args();dest=a.directory.resolve()
if (dest/'project.json').exists():raise ValueError('Project exists; resume it instead of preparing again')
if not (dest/'last-seed.blend').exists():raise ValueError('Create and inspect the original scene first')
(dest/'bin').mkdir(exist_ok=True);(dest/'bin/blender').symlink_to(a.blender.resolve())
env={**os.environ,'PATH':str(dest/'bin')+os.pathsep+os.environ['PATH']}
def cli(name,*args):
 r=subprocess.run([sys.executable,str(BASE/name),*map(str,args)],env=env,capture_output=True,text=True)
 if r.returncode:raise RuntimeError(r.stderr[-2000:])
 try:return json.loads(r.stdout)
 except json.JSONDecodeError:return r.stdout

def write(name,value):
 path=dest/name
 with path.open('x') as f:json.dump(value,f,indent=2);f.write('\n')
 return path
# Original stereo ambience and event cues. No samples or external music.
rate=48000;rng=random.Random(24);samples=bytearray();peak=0;low=0
for i in range(360000):
 t=i/rate;fade=min(1,t/.18,(7.5-t)/.5);low=.97*low+.03*rng.uniform(-1,1)
 pad=.013*math.sin(2*math.pi*130.813*t)+.007*math.sin(2*math.pi*196*t)+.004*math.sin(2*math.pi*261.626*t)
 v=(pad+low*.035)*fade
 dt=t-.97
 if 0<=dt<.14:v+=.08*rng.uniform(-1,1)*math.exp(-dt*30)
 dt=t-1.2
 if 0<=dt<.08:v+=.018*math.sin(2*math.pi*740*dt)*math.exp(-dt*60)
 dt=t-2.8333333333
 if 0<=dt<.42:v+=.16*math.sin(2*math.pi*(1800*dt-1200*dt*dt))*math.exp(-dt*16)+.035*rng.uniform(-1,1)*math.exp(-dt*22)
 dt=t-3.5
 if 0<=dt<3.5:v+=.012*math.sin(2*math.pi*523.25*dt)*math.sin(math.pi*dt/3.5)**2
 left=v;right=v*.95+.0025*math.sin(2*math.pi*196*t+.4)*fade
 peak=max(peak,abs(left),abs(right));samples.extend(struct.pack('<hh',int(left*32767),int(right*32767)))
with wave.open(str(dest/'sound.wav'),'wb') as f:f.setparams((2,2,rate,0,'NONE',''));f.writeframes(samples)
write('sound-cues.json',{'duration':7.5,'original_synthesis':True,'peak_linear':peak,'events':[{'time':.97,'event':'seed contact'},{'time':1.2,'event':'nozzle relay'},{'time':2.8333333333,'event':'water impact'},{'time':3.5,'event':'growth harmonic'}],'listening':'pending_owner_review','tonejs':'not_tested_in_this_pilot'})
project=dest/'project.json';cli('project.py','create',project,'--goal','The Last Seed: 7.5-second seed, drop and sprout pilot','--note','Owner authorised pilot; full film, approval and publication remain separate')
cli('project.py','observe',project,'project','--kind','decision','--result','accepted','--actor','owner','--provenance','owner_report','--topic','pilot-scope','--note','Owner requested The Last Seed pilot, 6–8 seconds, seed, drop and first sprout; record development and tests. This approves production scope, not unseen output.')
shutil.copyfile(Path(__file__).with_name('create_scene.py'),dest/'create-scene.py')
for identity,path in [('scene',dest/'last-seed.blend'),('sound',dest/'sound.wav'),('builder',dest/'create-scene.py')]:cli('project.py','retain',project,identity,path,'--input')
profile=dest/'profile.json';cli('intake.py','init',profile);cli('intake.py','preference',profile,'--options','free-only')
brief=write('brief.json',{'idea':'The Last Seed: a cinematic original greenhouse macro; seed falls, water lands, a sprout unfolds. Stylised compressed growth, not scientific time-lapse footage.',
 'language':'en','duration_seconds':7.5,'format':'16:9','visual_source':'supplied','source_rights':'Original local geometry, materials, animation and synthetic audio authored for this production','deadline':'pilot before full film','narration':False,'preferred_route':'local-saved-shot','constraints':{'allow_uploads':False,'allow_installation':False},
 'scenes':[{'id':'seed','purpose':'Establish a fragile seed physically arriving in dry soil'},{'id':'drop','purpose':'Make the water impact visibly cause the change'},{'id':'sprout','purpose':'Reveal the first sign of renewed life'}]})
write('proposal.json',cli('intake.py','brief',profile,brief,'--project',project))
route=write('routes.json',cli('intake.py','routes',profile,brief))
requirements=write('environment.json',{'id':'last-seed-cpu','platforms':[],'architectures':[],'min_memory_gib':0,'min_free_disk_gib':1,'programs':[{'name':'blender','minimum_version':'4.5'},{'name':'ffmpeg'},{'name':'ffprobe'}],'models':[],'manual_checks':[],'rights':{'status':'allowed','basis':'Original self-contained pilot geometry and sound; no external media or models'},'cost':{'status':'free_local','amount':0,'currency':'USD','basis':'Existing local software; excludes labour and hardware'}})
for identity,path,kind in [('routes',route,'route-comparison'),('environment',requirements,'environment-manifest')]:cli('project.py','asset',project,identity,'--kind',kind);cli('project.py','retain',project,identity,path)
cli('shots.py','prepare',project,dest/'shot-spec.json','--output',dest/'shot-v1.json','--actor','framewright')
cli('project.py','task',project,'owner-review','--label','View and listen to Last Seed pilot','--waiting-for','owner','--note','Pilot acceptance is pending; do not start full film')
print(json.dumps({'project':str(project),'sound_peak':peak,'route':'local-saved-shot','execution':'prepared_not_rendered'},indent=2))
