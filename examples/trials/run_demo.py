#!/usr/bin/env python3
"""Synthetic text-only example: no render, model, provider or creative approval."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import time

BASE=Path(__file__).resolve().parents[2]/'skills/video-production-router/scripts'


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    root=a.output.resolve();root.mkdir()  # Explicit new folder; never overwrite a project.
    project=root/'project.json'
    def put(name,value):
        path=root/name;path.write_text(json.dumps(value,indent=2)+'\n' if isinstance(value,dict) else value);return path
    def cli(script,*args):
        return subprocess.run([sys.executable,str(BASE/script),*map(str,args)],capture_output=True,text=True,check=True)
    cli('project.py','create',project,'--goal','Synthetic experiment-workbench example','--note','Text fixtures only, not media production')
    source=put('source.txt','Preserve this marker: FIREFLY\n')
    cli('project.py','retain',project,'source',source,'--input')
    manifest=put('environment-manifest.json',{'id':'text-fixture','platforms':[],'architectures':[],
        'min_memory_gib':0,'min_free_disk_gib':0,'programs':[{'name':'python3','minimum_version':None}],
        'models':[],'manual_checks':[], 'rights':{'status':'allowed','basis':'Original synthetic text fixture'},
        'cost':{'status':'free_local','amount':0,'currency':'USD','basis':'No provider/model calls'}})
    env=root/'environment.json';cli('environment.py',manifest,'--output',env)
    cli('project.py','retain',project,'environment',env,'--input')
    spec=put('trial-spec.json',{'id':'marker','tool':'synthetic-text-control','capability':'Preserve a source marker in a text fixture',
        'question':'Can the candidate preserve the marker lost by the baseline?', 'sources':['input:source'],
        'baseline':{'method':'Synthetic omitted-marker fixture','settings':{}},
        'candidate':{'method':'Synthetic preserved-marker fixture','settings':{}},
        'criteria':[{'id':'marker','kind':'technical','description':'Output contains FIREFLY'}],
        'limits':{'max_cost':0,'currency':'USD','max_seconds':60}})
    cli('trials.py','plan',project,spec,'--output',root/'trial.json','--actor','synthetic-example')
    observations={'id':'control-1'}
    for arm,content in [('baseline','Marker omitted\n'),('candidate',source.read_text())]:
        start=time.perf_counter();path=put(arm+'.txt',content);passed='FIREFLY' in path.read_text()
        elapsed=time.perf_counter()-start
        log=put(arm+'-check.json',{'fixture_only':True,'contains_marker':passed})
        cli('project.py','asset',project,arm,'--kind','text');cli('project.py','retain',project,arm,path)
        cli('project.py','retain',project,arm+'-check',log,'--input')
        observations[arm]={'output':'output:'+arm,'sources':['input:source'],'environment':'input:environment',
            'elapsed_seconds':elapsed,'cost':{'amount':0,'currency':'USD'},
            'checks':{'marker':{'result':'pass' if passed else 'fail','note':'Measured text membership only; no media QA',
                                'evidence':['input:'+arm+'-check']}}}
    observation=put('observations.json',observations)
    cli('project.py','retain',project,'observations',observation,'--input')
    cli('trials.py','compare',project,'output:trial:marker','input:observations','--output',root/'comparison',
        '--actor','synthetic-example','--provenance','supplied_report')
    result=cli('trials.py','status',project,'output:trial:marker','--json')
    print(result.stdout,end='');print('Local report:',root/'comparison/review.html')


if __name__=='__main__':main()
