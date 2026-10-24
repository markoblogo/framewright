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
