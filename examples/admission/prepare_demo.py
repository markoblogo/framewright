#!/usr/bin/env python3
"""Prepare a NEW private original-silence route gate demo; do not execute the worker."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import wave

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'skills/video-production-router/scripts'

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('folder',type=Path);a=p.parse_args()
 try:
  folder=a.folder.resolve()
  if folder.is_relative_to(ROOT) or folder.exists():raise ValueError('Choose a new folder outside the repository; generated media stay private')
  folder.mkdir(parents=True);project=folder/'project.json'
  def call(script,*args):
   result=subprocess.run([sys.executable,str(BASE/script),*map(str,args)],capture_output=True,text=True)
   if result.returncode:raise ValueError(script+' failed: '+result.stderr[-800:])
   return result.stdout
  def write(name,value):
   path=folder/name
   with path.open('x') as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')
   return path
  call('project.py','create',project,'--goal','Synthetic selected-route inspection','--note','Original fixture;no film,paid call or publication')
  source=folder/'silence.wav'
  with wave.open(str(source),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(8000);f.writeframes(b'\0\0'*8000)
  call('project.py','retain',project,'source',source,'--input')
  call('project.py','asset',project,'report','--kind','review-report')
  call('project.py','task',project,'inspect','--label','Inspect original synthetic source','--requires','report')
  profile=folder/'profile.json';call('intake.py','init',profile);call('intake.py','preference',profile,'--options','free-only')
  brief=write('brief.json',{'idea':'Inspect supplied original source before editing','language':'en','duration_seconds':10,'format':'16:9','narration':False,'visual_source':'supplied','source_rights':'owner','deadline':'flexible'})
  comparison=write('routes.json',json.loads(call('intake.py','routes',profile,brief)))
  requirements=write('requirements.json',{'id':'local-inspection','platforms':[],'architectures':[],'min_memory_gib':0,'min_free_disk_gib':0,'programs':[{'name':'ffmpeg'},{'name':'ffprobe'}],'models':[],'manual_checks':[],'rights':{'status':'allowed','basis':'Original generated silence;local inspection only'},'cost':{'status':'free_local','amount':0,'currency':'USD','basis':'Local software provider fee only;not project/labour cost'}})
  for identity,path,kind in [('routes',comparison,'route-comparison'),('requirements',requirements,'environment-manifest')]:
   call('project.py','asset',project,identity,'--kind',kind);call('project.py','retain',project,identity,path)
  spec=write('selection.json',json.loads((Path(__file__).parent/'selection.json').read_text()))
  selected=json.loads(call('admission.py','select',project,spec,'--output',folder/'bound-selection.json'))
  print(json.dumps({'project':str(project),'selection':selected,'worker_executed':False},indent=2))
 except (OSError,ValueError,subprocess.SubprocessError) as e:p.error(str(e))

if __name__=='__main__':main()
