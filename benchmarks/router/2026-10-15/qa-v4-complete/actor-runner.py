from pathlib import Path
import concurrent.futures,json,os,signal,subprocess,time,hashlib,sys
root=Path(__file__).resolve().parent
cases=json.loads((root/'cases.json').read_text())

def isolation_args():
    paths=set()
    for root in [Path.home()/'.codex/skills',Path.home()/'.agents/skills']:
        if root.exists():
            for path in root.rglob('SKILL.md'):paths.update([str(path),str(path.resolve())])
            for child in root.iterdir():
                if (child/'SKILL.md').is_file():paths.update([str(child/'SKILL.md'),str((child/'SKILL.md').resolve())])
    toggles=[{'path':p,'enabled':False} for p in sorted(paths)]
    return ['-c','skills.config=['+','.join('{path='+json.dumps(x['path'])+',enabled=false}' for x in toggles)+']']

base=['codex','exec','--ignore-user-config','--ignore-rules','--ephemeral','--skip-git-repo-check','-m','gpt-6.1-sol','-c','model_reasoning_effort="medium"','-c','project_doc_max_bytes=0','-c','web_search="disabled"','-c','features.apps=false','-c','features.plugins=false','-c','features.multi_agent=false','-c','features.skip_host_skill_discovery=true','-c','shell_environment_policy.inherit="none"','-c','shell_environment_policy.set.PATH="/opt/homebrew/bin:/usr/bin:/bin"','-s','read-only','--json']
base+=isolation_args()
def snapshot(d):
    return {str(p.relative_to(d)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(d.rglob('*')) if p.is_file()}
def run(case):
    identity=case['id'];d=root/'runs'/identity;e=root/'evidence'/identity;e.mkdir(parents=True,exist_ok=True)
    if (e/'execution.json').exists():return identity+' retained (not rerun)'
    with (e/'RUNNING.lock').open('x') as lock:lock.write('Reserved before actor launch')
    before=snapshot(d);start=time.monotonic()
    env={k:v for k,v in os.environ.items() if k in {'PATH','HOME','LANG','TMPDIR'}}; env['CODEX_HOME']=os.environ['FRAMEWRIGHT_EVAL_CODEX_HOME']
    with (e/'events.jsonl').open('w') as out,(e/'stderr.txt').open('w') as err:
        p=subprocess.Popen(base+['-C',str(d),'-o',str(e/'answer.txt'),'-'],stdin=subprocess.PIPE,stdout=out,stderr=err,text=True,env=env,start_new_session=True)
        try:p.communicate((root/(identity+'-prompt.txt')).read_text(),timeout=240);code=p.returncode
        except subprocess.TimeoutExpired:
            os.killpg(p.pid,signal.SIGKILL);p.wait();code=124
    after=snapshot(d)
    events=[]
    for line in (e/'events.jsonl').read_text().splitlines():
        try:events.append(json.loads(line))
        except json.JSONDecodeError:pass
    usage=[x.get('usage') for x in events if x.get('type')=='turn.completed']
    result={'id':identity,'exit_code':code,'duration_seconds':round(time.monotonic()-start,2),'turn_completed':any(x.get('type')=='turn.completed' for x in events),'usage':usage,'files_before':before,'files_after':after,'workspace_unchanged':before==after,'answer_present':(e/'answer.txt').is_file() and bool((e/'answer.txt').read_text().strip())}
    (e/'execution.json').write_text(json.dumps(result,indent=2)+'\n')
    return f"{identity}: exit={code} complete={result['turn_completed']} unchanged={before==after} {result['duration_seconds']}s"
selected=cases[:1] if '--smoke' in sys.argv else cases
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    for result in pool.map(run,selected):print(result,flush=True)
