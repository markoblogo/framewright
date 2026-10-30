#!/usr/bin/env python3
"""Bounded saved-shot bridge. Reuses shots.py; never saves the project from the worker."""
import json
import os
from pathlib import Path
import runpy
import shutil
import signal
import sys
import threading

BASE=Path(__file__).resolve().parent

def shots():return runpy.run_path(str(BASE/'shots.py'))

def runtime():
    result={}
    for name in ('blender','ffmpeg','ffprobe'):
        path=shutil.which(name)
        if path is None and name=='blender':
            app=Path('/Applications/Blender.app/Contents/MacOS/Blender')
            if app.is_file():path=str(app)
        if path is None:raise ValueError('Installed executable required: '+name)
        path=Path(path).resolve(strict=True)
        import hashlib
        with path.open('rb') as f:checksum=hashlib.file_digest(f,'sha256').hexdigest()
        result[name]={'path':str(path),'sha256':checksum}
    return result

def preflight(data,project,subject,start,end):
    S=shots();T=S['T'];record=T['checked'](data,project,subject,'framewright-shot-v1')
    spec=record['spec'];S['validate'](spec)
    if any(type(n) not in (int,float) or not float(n).is_integer() for n in (start,end)):
        raise ValueError('Saved-shot bounds are integer frames, not seconds')
    plan=S['render'](data,project,subject,int(start),int(end),'preflight',project.parent/'unused',False,None,'ffmpeg','ffprobe','framewright',180)
    if plan['blockers']:raise ValueError('; '.join(plan['blockers']))
    return {'pins':{subject:T['current'](data,project,subject)[0],**record['pins']},
            'canvas':spec['canvas'],'frames':{'start':int(start),'end':int(end)},'audio':bool(spec['audio'])}

def folder_bytes(folder):
    total=0
    for p in folder.rglob('*'):
        if p.is_symlink():raise ValueError('Render output contains symlink')
        if p.is_file():total+=p.stat().st_size
    return total

def retain(data,project,source,folder,report,P):
    """Register only the fixed renderer outputs, verifying its source and output pins."""
    S=shots();T=S['T'];record=T['checked'](data,project,source,'framewright-shot-v1')
    if json.loads((folder/'render-report.json').read_text())!=report or report['shot']!=source or report['project']!=str(project):
        raise ValueError('Shot receipt does not describe this execution')
    dependencies={source:T['current'](data,project,source)[0],**record['pins']}
    files=[('video','preview.mp4','video'),('states','state.json','report'),('job','job.json','report')]
    if record['spec']['audio']:files.append(('audio','audio.wav','audio'))
    rid=record['spec']['id']+':'+record['spec']['version']+':'+folder.name.removeprefix('executor-shot-')
    if report['id']!=rid or report['subject']!='output:shot-render:'+rid:raise ValueError('Unexpected render attempt identity')
    expected={label:'output:shot-'+label+':'+rid for label,_,_ in files}
    if report['outputs']!=expected:raise ValueError('Unexpected shot output identities')
    pins={**dependencies,**{expected[label]:P['file_record'](folder/name,project.parent) for label,name,_ in files}}
    if pins!=report['pins']:raise ValueError('Shot receipt source/output pins differ')
    for label,name,kind in files:T['register'](data,project,expected[label][7:],folder/name,kind)
    subject=T['register'](data,project,report['subject'][7:],folder/'render-report.json','shot-render')
    P['JOURNAL']['append'](data,subject,'decision','proposed','framewright','operator_observation',
        'Bounded local render checked; viewing/listening approval pending','shot-render',pins)
    return subject

def main():
    project,subject,start,end,attempt,folder,encoded_runtime,max_bytes=sys.argv[1:]
    project=Path(project);folder=Path(folder);tools=json.loads(encoded_runtime);max_bytes=int(max_bytes)
    # The wrapper owns the process group, inherited host lock and independent deadline.
    # Stop excessive scratch growth; one in-flight write can exceed this sampled bound.
    stop=threading.Event()
    def watch():
        while not stop.wait(.1):
            try:exceeded=folder_bytes(folder)>max_bytes
            except OSError:continue
            except ValueError:exceeded=True
            if exceeded:os.killpg(os.getpgrp(),signal.SIGKILL)
    watcher=threading.Thread(target=watch,daemon=True);watcher.start()
    try:
        if runtime()!=tools:raise ValueError('Selected executables changed before render')
        S=shots();data=S['P']['load'](project)
        report=S['render'](data,project,subject,int(float(start)),int(float(end)),attempt,folder,True,
            tools['blender']['path'],tools['ffmpeg']['path'],tools['ffprobe']['path'],'framewright',180)
        if folder_bytes(folder)>max_bytes:raise ValueError('Render bundle exceeds selected byte allowance')
        print(json.dumps(report,allow_nan=False))
    finally:stop.set();watcher.join(timeout=1)

if __name__=='__main__':main()
