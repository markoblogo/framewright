#!/usr/bin/env python3
"""Package only this project's router; smoke-test it outside the checkout."""
import argparse
import hashlib
import json
import re
import posixpath
from urllib.parse import quote
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def build(root, output):
    version = (root / 'VERSION').read_text().strip()
    output = output.resolve()
    if output.is_relative_to(root.resolve()):
        raise ValueError('Release output must be outside the checkout')
    output.mkdir(parents=True, exist_ok=True)
    skill = root / 'skills/video-production-router'
    files = [skill / 'SKILL.md']
    for folder, suffixes in [('references', {'.json', '.md'}), ('scripts', {'.py', '.cjs'})]:
        files.extend(p for p in (skill / folder).iterdir() if p.is_file() and p.suffix in suffixes)
    if any(p.is_symlink() for p in files):
        raise ValueError('Do not package symlinked source')
    archive = output / f'framewright-router-{version}.zip'
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for p in sorted(files):
            name = 'video-production-router/' + p.relative_to(skill).as_posix()
            if p.suffix == '.md':
                def release_link(match):
                    link = match.group(1)
                    if '://' in link or link.startswith(('#', 'mailto:')):
                        return match.group(0)
                    path, separator, anchor = link.partition('#')
                    destination = (p.parent / path).resolve()
                    if destination.is_relative_to(skill.resolve()):
                        return match.group(0)
                    if not destination.is_relative_to(root.resolve()) or not destination.is_file():
                        raise ValueError('Unresolvable release documentation link: ' + link)
                    url = 'https://github.com/markoblogo/framewright/blob/v' + version + '/' + quote(destination.relative_to(root.resolve()).as_posix(), safe='/')
                    return '](' + url + (separator + anchor if separator else '') + ')'
                # Preserve core offline references; pin optional source/case links to this release.
                content = re.sub(r'\]\(([^)]+)\)', release_link, p.read_text())
                z.writestr(zipfile.ZipInfo.from_file(p, name), content, compress_type=zipfile.ZIP_DEFLATED)
            else:
                z.write(p, name)
        z.write(root / 'LICENSE', 'video-production-router/LICENSE')
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (output / 'SHA256SUMS').write_text(f'{digest}  {archive.name}\n')
    # The installed skill must work without the repository or its private media.
    with tempfile.TemporaryDirectory() as directory:
        target = Path(directory)
        with zipfile.ZipFile(archive) as z:
            names = set(z.namelist())
            for name in names:
                if not name.endswith('.md'):
                    continue
                for link in re.findall(r'\]\(([^)]+)\)', z.read(name).decode()):
                    if '://' in link or link.startswith(('#', 'mailto:')):
                        continue
                    destination = posixpath.normpath(posixpath.join(posixpath.dirname(name), link.split('#')[0]))
                    if destination not in names:
                        raise ValueError('Broken installed documentation link: ' + name + ': ' + link)
            z.extractall(target)
        brief = target / 'brief.json'
        brief.write_text(json.dumps({'blocks': [{'id': 'ui', 'input': 'react-ui', 'preferred_tool': 'flute', 'deliverables': ['video-export', 'still-export']}], 'music': {'direction': 'music-first', 'audio_source': 'authorised-demo.wav'}}))
        run = subprocess.run([sys.executable, str(target / 'video-production-router/scripts/plan.py'), str(brief)], check=True, capture_output=True, text=True)
        plan = json.loads(run.stdout)
        if plan['blocks'][0]['tools'] != ['flute', 'ffmpeg'] or plan['execution'] != 'not_started' or plan['music']['timeline_owner'] != 'locked_music':
            raise ValueError('Standalone routing smoke check failed')
        packet = subprocess.run([sys.executable, str(target / 'video-production-router/scripts/plan.py'), str(brief),
                                 '--format', 'markdown'], check=True, capture_output=True, text=True)
        if not all(text in packet.stdout for text in ['# Production plan', 'still-export', 'permission_gates', 'not_started']):
            raise ValueError('Standalone production packet smoke check failed')
        project = target / 'production.json'
        project_cli = target / 'video-production-router/scripts/project.py'
        subprocess.run([sys.executable, str(project_cli), 'init', str(brief), str(project)], check=True, capture_output=True, text=True)
        resumed = subprocess.run([sys.executable, str(project_cli), 'resume', str(project), '--json'], check=True, capture_output=True, text=True)
        if json.loads(resumed.stdout)['ready'] != ['source-review', 'preflight']:
            raise ValueError('Standalone project checkpoint smoke check failed')
        # The new memory/journal must work from the standalone ZIP as well.
        manual = target / 'manual-production.json'
        subprocess.run([sys.executable,str(project_cli),'create',str(manual),
                        '--goal','Paused review fixture','--note','Offline package smoke'],
                       check=True,capture_output=True,text=True)
        subprocess.run([sys.executable,str(project_cli),'observe',str(manual),'project',
                        '--kind','decision','--result','deferred','--topic','owner-recording',
                        '--actor','operator','--provenance','supplied_report','--note','Fixture, no voice supplied'],
                       check=True,capture_output=True,text=True)
        remembered = subprocess.run([sys.executable,str(project_cli),'resume',str(manual),'--json'],
                                    check=True,capture_output=True,text=True)
        if json.loads(remembered.stdout)['observations']['effective'][0]['result']!='deferred':
            raise ValueError('Standalone production journal smoke check failed')
        composition = target / 'composition.json'
        composition.write_text(json.dumps({'schema_version':1,'materials':[],
            'scenes':[{'id':'demo','tell':'Fixture review','show':'Await real capture','materials':[],
                       'narration':{'text':'','material':None},'missing':['Capture pending']}],
            'variants':[{'id':'short','kind':'short','canvas':{'width':1080,'height':1920,'fps':30},
                'edits':[{'scene':'demo','material':None,'duration_seconds':2,'framing':'Portrait planned'}],
                'music':None,'tasks':[],
                'delivery':{k:None for k in ['video','thumbnail','subtitles','title','description']}}]}))
        subprocess.run([sys.executable,str(project_cli),'compose',str(manual),str(composition)],
                       check=True,capture_output=True,text=True)
        board = subprocess.run([sys.executable,str(project_cli),'board',str(manual),'--json'],
                               check=True,capture_output=True,text=True)
        if json.loads(board.stdout)['variants']['short']['complete_local_handoff']:
            raise ValueError('Standalone board promoted an unfinished cut')
        kit = target / 'draft-kit'
        subprocess.run([sys.executable,str(project_cli),'bundle',str(manual),'short','--output',str(kit),'--draft'],
                       check=True,capture_output=True,text=True)
        receipt=json.loads((kit/'manifest.json').read_text())
        if receipt['complete_local_handoff'] or receipt['publication_authorized'] or receipt['files']:
            raise ValueError('Standalone draft kit invented delivery or publication')
        search_cli = target / 'video-production-router/scripts/search.py'
        found = subprocess.run([sys.executable, str(search_cli), '--task', 'narration', '--language', 'uk',
                                '--evidence', 'tested', '--rights', 'commercial'], check=True, capture_output=True, text=True)
        rows = json.loads(found.stdout)['results']
        if not any(row['id']=='supertonic3' and not row['rights']['asset_clearance'] for row in rows):
            raise ValueError('Standalone arsenal discovery smoke check failed')
        combined = subprocess.run([sys.executable, str(search_cli), '--task', 'video', '--input', 'book-art',
                                   '--style', 'paper-cut', '--feature', 'paper-cut-regroup', '--feature', 'narration',
                                   '--language', 'uk', '--combinations', '--evidence', 'tested'],
                                  check=True, capture_output=True, text=True)
        if not any(set(c['tools'])=={'remotion','supertonic3'} for c in json.loads(combined.stdout)['combinations']):
            raise ValueError('Standalone arsenal combination smoke check failed')
        spec = target / 'workflow.json'
        spec.write_text(json.dumps({'scenario':'repackaging','sources':[
            {'id':'owner-clip','kind':'video','origin':'placeholder,not inspected',
             'audio_policy':'remove','video_rights':{'status':'unknown'}}],
            'brief':{'blocks':[{'id':'recut','input':'video','duration_seconds':3}]}}))
        workflow = subprocess.run([sys.executable, str(target / 'video-production-router/scripts/workflow.py'), str(spec)],
                                  check=True, capture_output=True, text=True)
        report = json.loads(workflow.stdout)
        if not report['publication_blockers'] or report['execution_authorized']:
            raise ValueError('Standalone studio workflow gates failed')
        subprocess.run([sys.executable, str(target / 'video-production-router/scripts/library.py'), '--help'],
                       check=True, capture_output=True, text=True)
    print(f'PASS: standalone package {archive.name}; SHA-256 {digest}')
    return archive


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    build(ROOT, args.output)
