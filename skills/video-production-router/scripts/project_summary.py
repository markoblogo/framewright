"""Read-only projection of retained files and latest journal records."""
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qs, urlencode
import re


def project(data, root, problems, journal, checkpoint_sha256, *, public=False, title=None, include=()):
    subjects = {'input:'+k: v for k,v in data['inputs'].items()}
    subjects.update({'output:'+k:v['file'] for k,v in data['artifacts'].items()})
    if public and (not title or not title.strip() or not include):
        raise ValueError('Public summary requires --title and explicit --include subjects')
    selected = list(dict.fromkeys(include)) if include else list(subjects)
    if any(s not in subjects for s in selected):
        raise ValueError('Unknown summary subject')
    latest = {(r['subject'],r['kind'],r.get('topic')):r for r in data.get('journal',[])}
    projected = journal['project'](data,problems)
    stale = {r['id'] for r in projected['stale']}
    files=[]
    for subject in selected:
        pin=subjects[subject]
        state='declared' if pin is None else 'current'
        if subject in problems:
            if problems[subject]=='changed bytes/hash':state='changed'
            else:
                try:
                    (root/pin['path']).stat();state='unavailable'
                except FileNotFoundError:state='missing'
                except OSError:state='unavailable'
        rows=[]
        for r in latest.values():
            if r['subject']!=subject:continue
            row={k:r[k] for k in ('id','kind','result','provenance','recorded_at')}
            row['stale']=r['id'] in stale
            if r.get('observed_at'):row['observed_at']=r['observed_at']
            if r['kind']=='publication':
                row['visibility']=r.get('visibility','unknown')
                if not public or row['visibility']=='public':
                    u=urlsplit(r['url']);query=''
                    if u.hostname in {'youtube.com','www.youtube.com','m.youtube.com'} and u.path=='/watch':
                        v=parse_qs(u.query).get('v',[''])[0]
                        if re.fullmatch(r'[A-Za-z0-9_-]{11}',v):query=urlencode({'v':v})
                    row['url']=urlunsplit((u.scheme,u.netloc,u.path,query,''))
            rows.append(row)
        row={'subject':subject,'state':state,'sha256':pin['sha256'] if pin else None,'observations':rows}
        if not public and pin:row['path']=pin['path']
        files.append(row)
    return {'schema_version':1,'title':title or data.get('project',{}).get('goal','Project status'),
            'checkpoint_sha256':checkpoint_sha256,'journal_sha256':data.get('journal_sha256'),
            'scope':'explicit_public_selection' if public else 'local_project',
            'files':files,'project_decisions':[] if public else [{**{k:r[k] for k in ('id','topic','result','provenance','recorded_at')},'stale':r['id'] in stale} for r in latest.values() if r['subject']=='project' and r['kind']=='decision'],'note':'Derived from retained revisions and recorded observations. Unknown is not approval; publication is separately recorded, not independently verified.'}


def cell(value):
    return str(value).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('|','&#124;').replace('\n',' ').replace('\r',' ')


def markdown(view):
    lines=['# '+cell(view['title']),'',view['note'],'', '| File ID | File state | Latest recorded observations |','|---|---|---|']
    for f in view['files']:
        states='; '.join(r['kind']+': '+r['result']+(' (STALE)' if r['stale'] else '') for r in f['observations']) or 'unknown'
        lines.append('| '+cell(f['subject'])+' | '+f['state']+' | '+cell(states)+' |')
    if view['project_decisions']:
        lines.extend(['','Project decisions:'])
        for r in view['project_decisions']:lines.append('- '+cell(r['topic'])+': '+r['result']+(' (STALE)' if r['stale'] else ''))
    for f in view['files']:
        for r in f['observations']:
            if 'url' in r:lines.extend(['','Publication ('+cell(r['visibility'])+'): '+cell(r['url'])])
    lines.extend(['','Checkpoint SHA256: '+view['checkpoint_sha256'],'Journal SHA256: '+str(view['journal_sha256']),''])
    return '\n'.join(lines)


def export(text, output, checkpoint, data, *, replace=False, check=False):
    output=Path(output)
    protected={checkpoint.resolve(),checkpoint.with_suffix(checkpoint.suffix+'.lock').resolve()}
    protected.update((checkpoint.parent/p['path']).resolve() for p in data['inputs'].values())
    protected.update((checkpoint.parent/a['file']['path']).resolve() for a in data['artifacts'].values() if a['file'])
    if output.is_symlink() or output.resolve() in protected:
        raise ValueError('Summary output must not overwrite a checkpoint, lock or retained source')
    if check:
        if not output.is_file() or output.read_text()!=text:raise ValueError('Generated summary is out of date')
        return
    if output.exists() and not replace:raise ValueError('Summary exists; inspect and use --replace')
    with output.open('w' if replace else 'x') as stream:stream.write(text)


def working_brief(data, status, files, limit=3):
    """Combine existing resume/journal facts; never infer an approved creative action."""
    latest={r['id'] for r in {(r['subject'],r['kind'],r['topic']):r for r in data.get('journal',[])}.values()}
    accepted=[{k:r[k] for k in ('id','subject','kind','topic','note','provenance')} for r in status['observations']['effective']
              if (r['kind']=='decision' or r['kind']=='creative') and r['result']=='accepted']
    changes=[{'subject':f['subject'],'state':f['state']} for f in files['files'] if f['state'] not in {'current','declared'}]
    unretained=[f['subject'] for f in files['files'] if f['state']=='declared']
    rechecks=[{'receipt':r['id'],'subject':r['subject'],'kind':r['kind'],'reason':'stale_revision'} for r in status['observations']['stale'] if r['id'] in latest]
    rechecks.extend({'receipt':r['id'],'subject':r['subject'],'kind':r['kind'],'reason':r['result']} for r in status['observations']['effective'] if r['kind'] in {'technical','listening','creative','provider'} and r['result'] in {'pending','fail','rejected'})
    waiting=[{'task':k,**v} for k,v in status['waiting'].items()]
    blockers=[{'task':k,'reason':v} for k,v in status['blocked'].items() if k not in status['waiting']]
    blockers.extend({'task':r['step'],'reason':'Unresolved executor attempt '+r['attempt']} for r in status.get('unresolved_attempts',[]))
    revisions={}
    for e in data['history']:
        if e['action'] in {'retain_input','retain_output'} and e.get('previous'):
            subject=('input:' if e['action']=='retain_input' else 'output:')+e['identity']
            revisions.pop(subject,None);revisions[subject]={'subject':subject,'recorded_at':e['utc']}
    recent=list(reversed(list(revisions.values())))
    if changes:kind,label='file_review','Review changed, missing or unavailable retained files before production'
    elif status['evidence_blockers']:kind,label='evidence_review','Review stale or unresolved checks before dependent work'
    elif status.get('unresolved_attempts'):kind,label='operation_recovery','Reconcile the interrupted executor attempt before repeating work'
    elif status['next_actions']:kind,label='ready_task',status['next_actions'][0]['label']
    elif waiting:kind,label='waiting','Obtain the explicitly recorded input or decision; keep the wait in force'
    elif blockers:kind,label='blocked','Resolve the recorded constraint before dependent production; no authority inferred'
    elif rechecks:kind,label='evidence_review','Review the unresolved recorded checks; do not infer final acceptance'
    else:kind,label='no_recorded_next_action','Agree the next task; no production action is currently recorded as ready'
    sections={'accepted':accepted,'file_changes':changes,'recent_revisions':recent,'not_retained':unretained,'needs_recheck':rechecks,'waiting':waiting,'blockers':blockers,'ready_tasks':status['next_actions']}
    return {'schema_version':1,'goal':status['project']['goal'] or 'not recorded','execution':'not_started',
            **{k:v[:limit] for k,v in sections.items()},'counts':{k:len(v) for k,v in sections.items()},
            'planning_sources_changed':status['planning_sources_changed'],
            'proposed_next':{'kind':kind,'label':label,'task':status['next_actions'][0]['id'] if kind=='ready_task' else None,'status':'proposal_not_execution_authority'},
            'note':'Local working brief from the same checkpoint. Recorded acceptance is not independent verification. Recent replacements are historical, not changes since a known session. Creative advice must be labelled separately; no work, approval or replan performed.'}


def brief_markdown(view):
    lines=['# Working brief','', 'Goal: '+cell(view['goal']),'']
    if view.get('completion'):
        lines+=['Completion diagnosis: '+cell(view['completion']['status'])+'; '+str(view['completion']['blockers'])+' blockers. Use project.py blockers PROJECT for reasons.','']
    for key,label in [('accepted','Accepted work'),('file_changes','Current file problems'),('recent_revisions','Most recent recorded replacements'),('not_retained','Declared, not retained'),('needs_recheck','Checks to review'),('waiting','Explicit waits'),('blockers','Recorded constraints'),('ready_tasks','Recorded ready tasks')]:
        rows=view[key];total=view['counts'][key]
        lines.append(label+' ('+str(total)+')'+(': showing '+str(len(rows)) if len(rows)<total else '')+':')
        if not rows:lines.append('- None recorded')
        for r in rows:
            if key=='accepted':text=r['subject']+' / '+r['topic']+': '+r['note']+' ['+r['provenance']+']'
            elif key=='file_changes':text=r['subject']+': '+r['state']
            elif key=='recent_revisions':text=r['subject']+' at '+r['recorded_at']
            elif key=='not_retained':text=r
            elif key=='needs_recheck':text=r['subject']+' / '+r['kind']+': '+r['reason']
            elif key=='blockers':text=r['task']+': '+str(r['reason'])
            elif key=='waiting':text=r['party']+' — '+r['task']+': '+r['reason']
            else:text=r['id']+': '+r['label']
            lines.append('- '+cell(text))
        lines.append('')
    lines.extend(['Proposed next step (not approval): '+cell(view['proposed_next']['label']),''])
    if view['planning_sources_changed']:lines.extend(['Tool sources changed; the frozen plan has been preserved.',''])
    lines.extend([view['note'],''])
    return '\n'.join(lines)
