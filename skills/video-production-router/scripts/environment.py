#!/usr/bin/env python3
"""Read-only local prerequisite snapshot. No installs, model loads, accounts or execution grants."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import re
import runpy
import shutil
import subprocess

VERSION_PROBES = {'python3':['--version'], 'node':['--version'],
                  'ffmpeg':['-version'], 'ffprobe':['-version'],
                  'blender':['--version'], 'rhubarb':['--version']}


def text(value, label):
    if not isinstance(value,str) or not value.strip(): raise ValueError(label+' requires text')
    return value


def number(value, label):
    if type(value) not in (int,float) or not math.isfinite(value) or value<0:
        raise ValueError(label+' must be a finite nonnegative number')
    return value


def keys(value, required, optional=()):
    if not isinstance(value,dict) or set(value)-set(required)-set(optional) or not set(required)<=set(value):
        raise ValueError('Expected fields: '+', '.join(required))


def validate(spec):
    keys(spec,['id','platforms','architectures','min_memory_gib','min_free_disk_gib',
               'programs','models','manual_checks','rights','cost'],['backends'])
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,79}',text(spec['id'],'id')):
        raise ValueError('Use a short alphanumeric environment ID')
    for name in ['platforms','architectures']:
        rows=spec[name]
        if not isinstance(rows,list) or any(not isinstance(v,str) or not v.strip() for v in rows) or len(set(rows))!=len(rows):
            raise ValueError(name+' requires distinct names')
    for name in ['min_memory_gib','min_free_disk_gib']: number(spec[name],name)
    backends=spec.get('backends',[])
    if not isinstance(backends,list) or any(v not in {'cpu','cuda','metal'} for v in backends) or len(set(backends))!=len(backends):
        raise ValueError('backends must be distinct cpu/cuda/metal names')
    for name in ['programs','models','manual_checks']:
        if not isinstance(spec[name],list): raise ValueError(name+' requires a list')
    seen=set()
    for row in spec['programs']:
        keys(row,['name'],['minimum_version'])
        if row['name'] not in VERSION_PROBES or row['name'] in seen:
            raise ValueError('Use distinct allowlisted program names; no command strings/arguments')
        seen.add(row['name'])
        if row.get('minimum_version') is not None and (not isinstance(row['minimum_version'],str) or
                not re.fullmatch(r'\d+(?:\.\d+){1,3}',row['minimum_version'])):
            raise ValueError('minimum_version must be a numeric version')
    for label in ['models','manual_checks']:
        seen=set()
        for row in spec[label]:
            keys(row,['id','path','sha256'] if label=='models' else ['id','status','basis'])
            ident=text(row['id'],label+' ID')
            if ident in seen:raise ValueError('Duplicate '+label+' ID')
            seen.add(ident)
            if label=='models':
                text(row['path'],'model path')
                if row['sha256'] is not None and (not isinstance(row['sha256'],str) or not re.fullmatch('[a-f0-9]{64}',row['sha256'])):
                    raise ValueError('sha256 must be lowercase SHA256 or null')
            else:
                if row['status'] not in {'pass','fail','unknown'}:raise ValueError('Manual status must be pass/fail/unknown')
                text(row['basis'],'manual evidence/basis')
    rights=spec['rights'];keys(rights,['status','basis'])
    if rights['status'] not in {'unknown','allowed','restricted'}:raise ValueError('Invalid rights status')
    text(rights['basis'],'rights basis')
    cost=spec['cost'];keys(cost,['status','amount','currency','basis'])
    if cost['status'] not in {'unknown','free_local','quoted'}:raise ValueError('Invalid cost status')
    text(cost['currency'],'currency/unit');text(cost['basis'],'cost basis')
    if cost['status']=='unknown':
        if cost['amount'] is not None:raise ValueError('Unknown cost must remain null')
    else:
        number(cost['amount'],'cost amount')
        if cost['status']=='free_local' and cost['amount']!=0:raise ValueError('free_local amount must be zero')
    return spec


def memory_gib():
    try:return os.sysconf('SC_PHYS_PAGES')*os.sysconf('SC_PAGE_SIZE')/2**30
    except (ValueError,OSError):
        if platform.system()=='Darwin':
            try:
                p=subprocess.run(['/usr/sbin/sysctl','-n','hw.memsize'],capture_output=True,text=True,timeout=3,check=True)
                return int(p.stdout.strip())/2**30
            except (OSError,ValueError,subprocess.SubprocessError):pass
    return None


def version_tuple(value):
    match=re.search(r'(?<!\d)(\d+\.\d+(?:\.\d+){0,2})(?!\d)',value)
    if not match:return None
    values=[int(n) for n in match[1].split('.')]
    return tuple(values+[0]*(4-len(values)))


def technical_status(checks):
    if any(c['status']=='fail' for c in checks):return 'needs_preparation'
    if any(c['status']=='unknown' for c in checks):return 'unknown'
    return 'ready'


def inspect(spec, root, probe_versions=False, probe_hardware=False, observe_resources=False):
    validate(spec)
    checks=[];probes=[]
    system={'platform':platform.system(),'architecture':platform.machine(),
            'memory_gib':memory_gib(),'free_disk_gib':shutil.disk_usage(root).free/2**30}
    if observe_resources:
        system['resource_observation']=runpy.run_path(str(Path(__file__).with_name('resources.py')))['snapshot']([root])
    def check(ident,status,note):checks.append({'id':ident,'status':status,'note':note})
    for name,key in [('platforms','platform'),('architectures','architecture')]:
        check(key,'pass' if not spec[name] or system[key] in spec[name] else 'fail',
              'Observed '+system[key]+'; allowed: '+(', '.join(spec[name]) or 'not constrained'))
    for field,observed in [('min_memory_gib','memory_gib'),('min_free_disk_gib','free_disk_gib')]:
        actual=system[observed];wanted=spec[field]
        status='pass' if wanted==0 or actual is not None and actual>=wanted else 'unknown' if actual is None else 'fail'
        check(observed,status,f'Required {wanted} GiB; observed {actual}. Memory is total, not free or model capacity.')
    for backend in spec.get('backends',[]):
        if backend=='cpu':check('backend:cpu','pass','Host CPU available; framework/model execution not checked');continue
        if backend=='metal' and system['platform']!='Darwin' or backend=='cuda' and system['platform']=='Darwin' and system['architecture']=='arm64':
            check('backend:'+backend,'fail','Requested backend is incompatible with this native platform');continue
        if not probe_hardware:
            check('backend:'+backend,'unknown','No hardware probe requested; backend/framework not inferred');continue
        try:
            if backend=='cuda':
                exe=shutil.which('nvidia-smi')
                if not exe:raise ValueError('NVIDIA query unavailable')
                argv=[exe,'--query-gpu=name,memory.total,driver_version','--format=csv,noheader,nounits']
                probes.append({'program':'nvidia-smi','arguments':argv[1:]})
                result=subprocess.run(argv,capture_output=True,text=True,timeout=5,check=True).stdout.strip()
                if not result:raise ValueError('No GPU returned')
                note='NVIDIA driver reports GPU name, memory MiB, driver: '+result[:1500]+'; CUDA toolkit/framework/model not checked'
            else:
                argv=['/usr/sbin/system_profiler','SPDisplaysDataType','-json']
                probes.append({'program':'system_profiler','arguments':argv[1:]})
                result=json.loads(subprocess.run(argv,capture_output=True,text=True,timeout=10,check=True).stdout)
                displays=result.get('SPDisplaysDataType',[])
                supported=[r.get('sppci_model','GPU') for r in displays if any('metal' in str(k).lower() and
                    (str(v).lower()=='spdisplays_metal_supported' or re.fullmatch(r'metal\s+[1-9]\d*',str(v).lower()))
                    for k,v in r.items())]
                if not supported:raise ValueError('Metal hardware not confirmed')
                note='Metal hardware reported: '+', '.join(supported)+'; PyTorch MPS/framework/model not checked'
            check('backend:'+backend,'pass',note)
        except (OSError,ValueError,TypeError,subprocess.SubprocessError):
            check('backend:'+backend,'unknown','Hardware query failed/unavailable; framework/model not tested')
    for row in spec['programs']:
        name=row['name'];path=shutil.which(name);minimum=row.get('minimum_version');ident='program:'+name
        app=Path('/Applications/Blender.app/Contents/MacOS/Blender')
        if path is None and name=='blender' and app.is_file():path=str(app)
        if path is None:check(ident,'fail','Executable not found on PATH');continue
        if not probe_versions:
            check(ident,'unknown' if minimum else 'pass','Executable found; version not executed/verified');continue
        argv=[path,*VERSION_PROBES[name]];probes.append({'program':name,'arguments':VERSION_PROBES[name]})
        try:
            p=subprocess.run(argv,capture_output=True,text=True,timeout=5,check=True)
            output=(p.stdout+'\n'+p.stderr).strip()[:4096]
            version=version_tuple(output)
            status='unknown' if version is None else 'fail' if minimum and version<version_tuple(minimum) else 'pass'
            check(ident,status,'Observed: '+output+'; minimum: '+str(minimum))
        except (OSError,subprocess.SubprocessError):
            check(ident,'unknown','Version probe failed or timed out; no runtime qualification')
    for row in spec['models']:
        path=Path(row['path']);path=path if path.is_absolute() else root/path
        try:
            if not path.is_file():raise FileNotFoundError()
            before=path.stat();checksum=None
            if row['sha256']:
                with path.open('rb') as stream:checksum=hashlib.file_digest(stream,'sha256').hexdigest()
            after=path.stat()
            stable=(before.st_size,before.st_mtime_ns)==(after.st_size,after.st_mtime_ns)
            status='pass' if stable and after.st_size>0 and (row['sha256'] is None or checksum==row['sha256']) else 'fail'
            check('model:'+row['id'],status,'Regular file present; '+('expected hash checked' if checksum else 'hash not required/checked')+'; inference not performed')
        except OSError:check('model:'+row['id'],'fail','Model file missing or unreadable; no download attempted')
    for row in spec['manual_checks']:
        check('manual:'+row['id'],row['status'],'Operator-supplied prerequisite: '+row['basis'])
    technical=technical_status(checks)
    next_step=('prepare_environment' if technical=='needs_preparation' else 'resolve_unknown_prerequisites' if technical=='unknown'
               else 'resolve_rights_restriction' if spec['rights']['status']=='restricted'
               else 'review_rights_and_cost' if spec['rights']['status']=='unknown' or spec['cost']['status']=='unknown'
               else 'ready_to_attempt_with_separate_authority')
    return {'schema':'framewright-environment-v1','id':spec['id'],
            'requirements':spec,
            'observed_at':datetime.now(timezone.utc).isoformat(),'system':system,'checks':checks,
            'technical_status':technical,'rights':spec['rights'],'cost':spec['cost'],
            'executed_probes':probes,'next_step':next_step,'execution_authorized':False,
            'scope':'Snapshot of declared prerequisites, not inference/render/export success or legal clearance. No accounts, model loads, network or installs.'}


def validate_report(value):
    if not isinstance(value,dict) or value.get('schema')!='framewright-environment-v1':raise ValueError('Expected an environment snapshot')
    validate(value.get('requirements'))
    if not isinstance(value.get('checks'),list) or any(not isinstance(c,dict) or c.get('status') not in {'pass','fail','unknown'} for c in value['checks']):
        raise ValueError('Invalid environment checks')
    if value.get('technical_status')!=technical_status(value['checks']) or value.get('execution_authorized') is not False:
        raise ValueError('Inconsistent environment result')
    rights=value.get('rights');keys(rights,['status','basis']);text(rights['basis'],'rights basis')
    if rights['status'] not in {'unknown','allowed','restricted'}:raise ValueError('Invalid snapshot rights')
    cost=value.get('cost');keys(cost,['status','amount','currency','basis'])
    text(cost['basis'],'cost basis');text(cost['currency'],'currency/unit')
    if cost['status'] not in {'unknown','quoted','free_local'}:raise ValueError('Invalid snapshot cost')
    if cost['status']=='unknown':
        if cost['amount'] is not None:raise ValueError('Unknown snapshot cost must remain null')
    else:
        number(cost['amount'],'snapshot cost')
        if cost['status']=='free_local' and cost['amount']!=0:raise ValueError('Invalid free-local amount')
    if not isinstance(value.get('manifest_sha256'),str) or not re.fullmatch('[a-f0-9]{64}',value['manifest_sha256']):
        raise ValueError('Snapshot needs manifest hash')
    when=datetime.fromisoformat(value['observed_at'])
    if when.tzinfo is None:raise ValueError('Environment time needs timezone')
    return value


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('manifest',type=Path)
    p.add_argument('--output',type=Path);p.add_argument('--probe-versions',action='store_true',
        help='Execute only fixed version queries for selected trusted installed programs; never accepts arbitrary commands')
    p.add_argument('--probe-hardware',action='store_true',help='Run fixed local GPU driver/system queries; never load a model')
    p.add_argument('--observe-resources',action='store_true',help='Observe available memory/swap with optional psutil; never install it')
    a=p.parse_args()
    try:
        raw=a.manifest.read_bytes();spec=json.loads(raw)
        report=inspect(spec,a.manifest.resolve().parent,a.probe_versions,a.probe_hardware,a.observe_resources)
        report['manifest_sha256']=hashlib.sha256(raw).hexdigest()
        if a.manifest.read_bytes()!=raw:raise ValueError('Manifest changed during inspection')
        rendered=json.dumps(report,indent=2,allow_nan=False)+'\n'
        if a.output:
            with a.output.open('x') as stream:stream.write(rendered)
        print(rendered,end='')
    except (OSError,ValueError,KeyError,TypeError) as exc:p.error(str(exc))


if __name__=='__main__':main()
