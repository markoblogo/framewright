#!/usr/bin/env python3
"""Local production checkpoints. Never install, render, decode, upload or replan."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import runpy
import tempfile

BASE = Path(__file__).resolve().parent


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True).encode()).hexdigest()


def file_record(path, root):
    path = path.resolve(strict=True)
    if not path.is_file():
        raise ValueError('Retain a regular file, not a directory')
    before = path.stat()
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    after = path.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise ValueError('File changed while hashing')
    return {'path': os.path.relpath(path, root), 'bytes': after.st_size,
            'sha256': h.hexdigest(), 'inspection': 'not_decoded_by_project_cli'}


def planning_sources():
    paths = [BASE / name for name in ['plan.py', 'music.py', 'terms.py']]
    paths.append(BASE.parent / 'references/tools.json')
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def event(data, action, **details):
    data['history'].append({'utc': datetime.now(timezone.utc).isoformat(),
                            'action': action, **details})


def initial(brief):
    registry = json.loads((BASE.parent / 'references/tools.json').read_text())
    plan = runpy.run_path(str(BASE / 'plan.py'))['plan'](brief, registry)
    packet = runpy.run_path(str(BASE / 'packet.py'))['markdown'](brief, plan, registry)
    steps, outputs, qa = [], {}, []

    def add(identity, label, dependencies=(), files=(), blocked=None, optional=False):
        steps.append({'id': identity, 'label': label, 'depends_on': list(dependencies),
                      'required_outputs': list(files), 'unmet': blocked or [],
                      'state': 'blocked' if blocked else 'planned', 'evidence': '',
                      'optional': optional, 'attestation': 'operator_recorded_not_independently_verified'})

    add('source-review', 'Check product facts, authorised assets and input identities')
    add('preflight', 'Check versions, licences, runtime/resources and authority')
    scene_steps = []
    video = False
    for index, (source, block) in enumerate(zip(brief['blocks'], plan['blocks']), 1):
        scene = f'scene:{index}'
        scene_steps.append(scene)
        files = []
        for kind in dict.fromkeys(source.get('deliverables', ['video-export'])):
            identity = scene + ':' + kind
            outputs[identity] = {'kind': kind, 'scene': block['id'], 'file': None}
            files.append(identity)
            check = 'qa:' + identity
            add(check, f'Inspect {kind} independently; follow saved packet/full handoff', [scene], [identity])
            qa.append(check)
            if kind == 'narration':
                listen = 'listen:' + scene
                add(listen, 'Human pronunciation, pauses, stress and intonation review', [check], [identity])
                qa.append(listen)
            video = video or kind == 'video-export'
        add(scene, f"Author scene: {block['id']}", ['source-review', 'preflight'], files, block['unmet'])
    if video:
        outputs['final-video'] = {'kind': 'video-export', 'scene': None, 'file': None}
        add('assembly', 'Assemble selected scenes with one master audio timeline', scene_steps, ['final-video'])
        add('qa:final-video', 'Final encoded decode, timing/seams, audio sync/phase/loudness and hashes', ['assembly'], ['final-video'])
        add('listen:final-video', 'Human final soundtrack listening or confirmation of intentional silence', ['qa:final-video'], ['final-video'])
        qa.extend(['qa:final-video','listen:final-video'])
    add('delivery', 'Hand over existing outputs and disclose remaining limits', scene_steps + qa)
    add('owner-review', 'Separate creative acceptance of the final work', ['delivery'], optional=True)
    add('publication', 'Record a supplied publication outcome; this command never uploads', ['delivery'], optional=True)
    # Keep authoring before dependent checks in the human read order.
    steps.sort(key=lambda s: (0 if s['id'] in ['source-review','preflight'] else
                              1 if s['id'].startswith('scene:') else
                              2 if s['id'].startswith(('qa:scene:', 'listen:')) else
                              3 if s['id']=='assembly' else 4 if s['id']=='qa:final-video' else
                              5 if s['id']=='listen:final-video' else 6 if s['id']=='delivery' else 7))
    data = {'schema_version': 1, 'brief': brief, 'plan': plan, 'plan_sha256': digest(plan), 'brief_sha256': digest(brief), 'packet_sha256': digest(packet),
            'production_packet': packet, 'planning_sources': planning_sources(),
            'steps': steps, 'inputs': {}, 'artifacts': outputs, 'history': []}
    event(data, 'init', note='Offline plan frozen; no production or QA performed')
    return data


def load(path):
    data = json.loads(path.read_text())
    if (data.get('schema_version') != 1 or digest(data['plan']) != data['plan_sha256'] or
            digest(data['brief']) != data['brief_sha256'] or digest(data['production_packet']) != data['packet_sha256']):
        raise ValueError('Unsupported/corrupted project or changed frozen plan; keep the original checkpoint')
    return data


@contextmanager
def locked(path):
    # macOS/Linux: OS releases flock on crash; a leftover lock file is harmless.
    import fcntl
    fd = os.open(str(path) + '.lock', os.O_CREAT | os.O_RDWR, 0o600)
    with os.fdopen(fd, 'a') as stream:
        try:
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise ValueError('Another writer holds this project; retry after it finishes') from exc
        yield


def save(path, data):
    # Same-directory rename keeps the old complete checkpoint until the new one is flushed.
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent,
                                         prefix='.' + path.name, suffix='.tmp', delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(data, stream, ensure_ascii=True, indent=2)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def file_problems(data, root):
    problems = {}
    records = [('input:' + k, v) for k,v in data['inputs'].items()]
    records += [('output:' + k, v['file']) for k,v in data['artifacts'].items() if v['file']]
    for identity, row in records:
        try:
            actual = file_record(root / row['path'], root)
            if (actual['bytes'],actual['sha256']) != (row['bytes'],row['sha256']):
                problems[identity] = 'changed bytes/hash'
        except (OSError, ValueError) as exc:
            problems[identity] = str(exc)
    return problems


def invalidate(data, roots):
    affected = set(roots)
    while True:
        more = {s['id'] for s in data['steps'] if affected.intersection(s['depends_on'])}
        if more.issubset(affected):
            break
        affected |= more
    old = []
    for step in data['steps']:
        if step['id'] in affected:
            target = 'blocked' if step['unmet'] else 'planned'
            if step['state'] != target or step['evidence']:
                old.append(dict(step))
            step['state'] = target
            step['evidence'] = ''
    if old:
        event(data, 'invalidate', previous_steps=old)


def retain(data, root, identity, path, is_input, replace):
    record = file_record(path, root)
    if not identity.strip():
        raise ValueError('File identity must be nonempty')
    if is_input:
        previous = data['inputs'].get(identity)
    else:
        if identity not in data['artifacts']:
            raise ValueError('Unknown output ID; use status/manifest output IDs')
        previous = data['artifacts'][identity]['file']
    if previous == record:
        return
    if previous and not replace:
        raise ValueError('Existing pin differs; inspect changes and use --replace explicitly')
    if is_input:
        # New/replaced input can affect the entire production; never reuse old approvals silently.
        invalidate(data, [s['id'] for s in data['steps']])
        data['inputs'][identity] = record
    else:
        invalidate(data, [s['id'] for s in data['steps'] if identity in s['required_outputs']])
        data['artifacts'][identity]['file'] = record
    event(data, 'retain_input' if is_input else 'retain_output', identity=identity,
          previous=previous, retained=record)


def mark(data, root, identity, state, evidence):
    steps = {s['id']:s for s in data['steps']}
    if identity not in steps:
        raise ValueError('Unknown step ID')
    step = steps[identity]
    if state in {'done','blocked'} and not evidence.strip():
        raise ValueError('Provide --evidence for a manual done/blocked claim')
    if state != 'blocked' and step['unmet']:
        raise ValueError('Frozen plan has unmet requirements; create a revised project, do not override')
    if state == 'done':
        if file_problems(data, root):
            raise ValueError('Retained evidence changed/missing; inspect status before continuing')
        if any(steps[d]['state'] != 'done' for d in step['depends_on']):
            raise ValueError('Dependencies are not done')
        if any(data['artifacts'][f]['file'] is None for f in step['required_outputs']):
            raise ValueError('Required output files have not been retained')
    if step['state'] != state or step['evidence'] != evidence:
        invalidate(data, [identity])
        step['state'], step['evidence'] = state, evidence
        event(data, 'mark', step=identity, state=state, evidence=evidence,
              note='Manual operator record; no decoder, listening or external verification run')


def summary(data, root):
    steps = {s['id']:s for s in data['steps']}
    problems = file_problems(data, root)
    ready = [s['id'] for s in data['steps'] if s['state']=='planned' and
             all(steps[d]['state']=='done' for d in s['depends_on'])] if not problems else []
    return {'execution': 'not_started_by_project_cli', 'ready': ready,
            'file_problems': problems, 'planning_sources_changed': data['planning_sources'] != planning_sources(),
            'recorded_done': [s['id'] for s in data['steps'] if s['state']=='done'],
            'blocked': {s['id']:s['unmet'] or s['evidence'] for s in data['steps'] if s['state']=='blocked'},
            'technical_handoff_recorded': steps['delivery']['state']=='done' and not problems,
            'outputs': {k:v['file'] is not None for k,v in data['artifacts'].items()},
            'note': 'Done means operator-recorded, not independently verified. Frozen plan is retained; no automatic replan.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    init = commands.add_parser('init');init.add_argument('brief',type=Path);init.add_argument('project',type=Path)
    status = commands.add_parser('status', aliases=['resume']);status.add_argument('project',type=Path);status.add_argument('--json',action='store_true')
    packet = commands.add_parser('packet');packet.add_argument('project',type=Path)
    pin = commands.add_parser('retain');pin.add_argument('project',type=Path);pin.add_argument('identity');pin.add_argument('file',type=Path);pin.add_argument('--input',action='store_true');pin.add_argument('--replace',action='store_true')
    update = commands.add_parser('mark');update.add_argument('project',type=Path);update.add_argument('step');update.add_argument('--state',choices=['planned','blocked','done'],required=True);update.add_argument('--evidence',default='')
    args = parser.parse_args()
    try:
        path = args.project.resolve()
        if args.command in {'status','resume','packet'}:
            data = load(path)
            if args.command=='packet':
                print(data['production_packet'],end='');return
            result = summary(data,path.parent)
            if args.json:
                print(json.dumps(result,indent=2));return
            print('Production checkpoint — manual records; no work executed by this command')
            print('Recorded done:',len(result['recorded_done']), '/', len(data['steps']))
            print('Ready to continue:',', '.join(result['ready'][:5]) or 'none')
            if len(result['ready'])>5:print('Additional ready steps:',len(result['ready'])-5)
            print('File problems:',json.dumps(result['file_problems']))
            print('Blocked:',json.dumps(result['blocked']))
            if result['planning_sources_changed']:print('Planning sources changed; review the frozen plan. It was not recalculated.')
            print('Output IDs:',', '.join(result['outputs']))
            return
        if not path.parent.is_dir():
            raise ValueError('Create the project parent directory explicitly first')
        with locked(path):
            if args.command=='init':
                if path.exists():raise ValueError('Project already exists; refusing to overwrite')
                data = initial(json.loads(args.brief.read_text()))
            else:
                data = load(path)
                if args.command=='retain':retain(data,path.parent,args.identity,args.file,args.input,args.replace)
                else:mark(data,path.parent,args.step,args.state,args.evidence)
            save(path,data)
        print('Saved checkpoint:',path)
    except (OSError,ValueError,KeyError,TypeError,ImportError) as exc:
        parser.error(str(exc))


if __name__=='__main__':
    main()
