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
JOURNAL = runpy.run_path(str(BASE / "journal.py"))
PRODUCTION = runpy.run_path(str(BASE / "production.py"))
CONTENT = runpy.run_path(str(BASE / 'content.py'))
COSTS = runpy.run_path(str(BASE / 'costs.py'))
EXECUTOR_STATE = runpy.run_path(str(BASE / 'executor_state.py'))
ADMISSION = runpy.run_path(str(BASE / 'admission.py'))
MEDIA = runpy.run_path(str(BASE / "media_review.py"))


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
    paths = [BASE / name for name in ['plan.py', 'music.py', 'terms.py', 'workflow.py', 'project.py', 'journal.py', 'packet.py', 'production.py', 'media_review.py', 'capture_check.py', 'project_summary.py', 'content.py', 'engine_capture.py', 'engine_capture.cjs', 'editing.py', 'revisions.py', 'templates.py', 'environment.py', 'trials.py', 'passports.py', 'shots.py', 'blender_shot_worker.py']]
    paths.append(BASE.parent / 'references/tools.json')
    paths.extend(BASE / name for name in ['project_blockers.py','resources.py','costs.py','executor.py','executor_worker.py','executor_state.py','decision_checks.py','admission.py'])
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
    production = plan.get('production')
    if production:
        add('production-review', 'Owner confirms concept, sources, limits and bounded experimental execution',
            ['source-review', 'preflight'], blocked=production['production_blockers'])
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
        if production:
            steps[-1]['depends_on'].append('production-review')
    if video:
        outputs['final-video'] = {'kind': 'video-export', 'scene': None, 'file': None}
        add('assembly', 'Assemble selected scenes with one master audio timeline', scene_steps, ['final-video'])
        add('qa:final-video', 'Final encoded decode, timing/seams, audio sync/phase/loudness and hashes', ['assembly'], ['final-video'])
        add('listen:final-video', 'Human final soundtrack listening or confirmation of intentional silence', ['qa:final-video'], ['final-video'])
        qa.extend(['qa:final-video','listen:final-video'])
    if production:
        extra = []
        for kind in production['outputs']:
            if kind == 'mp4' and video:
                continue
            identity = 'production:' + kind
            outputs[identity] = {'kind': kind, 'scene': None, 'file': None}
            extra.append(identity)
        add('delivery-materials', 'Create separate stems, captions, first screen, thumbnail, copy, provenance, QA and resource log',
            ['production-review'] + scene_steps, extra)
        add('qa:delivery-materials', 'Inspect every separate delivery artifact; technical receipt and rights review are independent',
            ['delivery-materials'], extra)
        qa.append('qa:delivery-materials')
    add('delivery', 'Hand over existing outputs and disclose remaining limits', scene_steps + qa)
    add('owner-review', 'Separate creative acceptance of the final work', ['delivery'], optional=True)
    add('publication', 'Record a supplied publication outcome; this command never uploads', ['delivery'], optional=True)
    if production:
        steps[-1]['unmet'] = production['publication_blockers']
        if steps[-1]['unmet']:
            steps[-1]['state'] = 'blocked'
    # Keep authoring before dependent checks in the human read order.
    steps.sort(key=lambda s: (0 if s['id'] in ['source-review','preflight','production-review'] else
                              1 if s['id'].startswith('scene:') else
                              2 if s['id'].startswith(('qa:scene:', 'listen:')) else
                              3 if s['id']=='assembly' else 4 if s['id']=='qa:final-video' else
                              5 if s['id'] in ['listen:final-video','delivery-materials','qa:delivery-materials'] else 6 if s['id']=='delivery' else 7))
    data = {'schema_version': 2, 'project': {'goal': '', 'context': ''}, 'journal': [], 'journal_sha256': digest([]), 'brief': brief, 'plan': plan, 'plan_sha256': digest(plan), 'brief_sha256': digest(brief), 'packet_sha256': digest(packet),
            'production_packet': packet, 'planning_sources': planning_sources(),
            'steps': steps, 'inputs': {}, 'artifacts': outputs, 'history': []}
    event(data, 'init', note='Offline plan frozen; no production or QA performed')
    return data


def load(path):
    data = json.loads(path.read_text())
    if (data.get('schema_version') not in {1, 2} or digest(data['plan']) != data['plan_sha256'] or
            digest(data['brief']) != data['brief_sha256'] or digest(data['production_packet']) != data['packet_sha256']):
        raise ValueError('Unsupported/corrupted project or changed frozen plan; keep the original checkpoint')
    if data['schema_version']==2:
        JOURNAL['validate'](data)
        PRODUCTION['validate_stored'](data)
        CONTENT['validate_stored'](data,digest)
        COSTS['validate_stored'](data)
        ADMISSION['validate_stored'](data)
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
    if data['schema_version']==2:
        data['journal_sha256']=digest(data['journal'])
        JOURNAL['validate'](data)
        PRODUCTION['validate_stored'](data)
        CONTENT['validate_stored'](data,digest)
        COSTS['validate_stored'](data)
        ADMISSION['validate_stored'](data)
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
            if step['state']=='blocked' and step.get('waiting_for'):
                continue  # File/receipt changes never silently remove an explicit wait.
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
        # Receipts can depend on outputs that their check tasks do not directly require.
        invalidate(data, list(evidence_blockers(data, file_problems(data, root))))
    event(data, 'retain_input' if is_input else 'retain_output', identity=identity,
          previous=previous, retained=record)


def check_kind(step):
    return step.get('check_kind') or ('technical' if step['id'].startswith('qa:') else
            'listening' if step['id'].startswith('listen:') else
            'creative' if step['id']=='owner-review' else None)


def evidence_blockers(data, problems):
    view=JOURNAL['project'](data,problems)
    latest={(r['subject'],r['kind'],r['topic']):r['id'] for r in data.get('journal',[])}
    blockers={}
    for step in data['steps']:
        kind=check_kind(step)
        subjects={'output:'+f for f in step['required_outputs']}
        if step['id']=='owner-review' and 'final-video' in data['artifacts']:
            subjects.add('output:final-video')
        for row in [*view['effective'],*view['stale']]:
            if row['id']!=latest[(row['subject'],row['kind'],row['topic'])]:continue
            if row['kind']==kind and row['subject'] in subjects and (row['stale_reasons'] or row['result'] in {'fail','rejected','pending'}):
                blockers.setdefault(step['id'],[]).append({'entry':row['id'],'result':row['result'],
                    'reason':'stale evidence' if row['stale_reasons'] else 'unresolved observation'})
    return blockers


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
        if evidence_blockers(data,file_problems(data,root)).get(identity):
            raise ValueError('Current rejected, failed, pending or stale evidence blocks this check; record the actual resolution first')
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
    gates=evidence_blockers(data,problems)
    unresolved=[r for r in EXECUTOR_STATE['attempts'](data) if r['state']=='unresolved']
    recovery_steps={r['step'] for r in unresolved}
    ready = [s['id'] for s in data['steps'] if s['state']=='planned' and s['id'] not in gates and s['id'] not in recovery_steps and
             all(steps[d]['state']=='done' for d in s['depends_on'])] if not problems else []
    return {'project': data.get('project', {'goal': '', 'context': ''}), 'schema_version': data['schema_version'],
            'execution': 'not_started_by_project_cli', 'ready': ready,
            'costs': COSTS['report'](data) if 'costs' in data else None,
            'unresolved_attempts': [{'attempt':r['attempt'],'step':r['step'],'request_sha256':r['request_sha256']} for r in unresolved],
            'next_actions': [{'id':i,'label':steps[i]['label']} for i in ready],
            'waiting': {s['id']:{'party':s['waiting_for'],'reason':s['evidence']} for s in data['steps'] if s['state']=='blocked' and s.get('waiting_for')},
            'observations': JOURNAL['project'](data,problems), 'evidence_blockers':gates,
            'production': PRODUCTION['report'](data,problems,JOURNAL['project'](data,problems),root),
            'file_problems': problems, 'planning_sources_changed': data['planning_sources'] != planning_sources(),
            'recorded_done': [s['id'] for s in data['steps'] if s['state']=='done'],
            'blocked': {s['id']:s['unmet'] or s['evidence'] for s in data['steps'] if s['state']=='blocked'},
            'technical_handoff_recorded': steps.get('delivery',{}).get('state')=='done' and not problems,
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
    migrate = commands.add_parser('migrate');migrate.add_argument('project',type=Path)
    describe = commands.add_parser('describe');describe.add_argument('project',type=Path);describe.add_argument('--goal',required=True);describe.add_argument('--note',required=True)
    create = commands.add_parser('create');create.add_argument('project',type=Path);create.add_argument('--goal',required=True);create.add_argument('--note',required=True)
    asset = commands.add_parser('asset');asset.add_argument('project',type=Path);asset.add_argument('identity');asset.add_argument('--kind',required=True)
    task = commands.add_parser('task');task.add_argument('project',type=Path);task.add_argument('identity');task.add_argument('--label',required=True);task.add_argument('--after',action='append',default=[]);task.add_argument('--requires',action='append',default=[]);task.add_argument('--waiting-for');task.add_argument('--note',default='');task.add_argument('--check-kind',choices=['technical','listening','creative','provider','publication'])
    observe = commands.add_parser('observe');observe.add_argument('project',type=Path);observe.add_argument('subject');observe.add_argument('--kind',choices=JOURNAL['RESULTS'],required=True);observe.add_argument('--result',required=True);observe.add_argument('--actor',required=True);observe.add_argument('--provenance',choices=sorted(JOURNAL['PROVENANCE']),required=True);observe.add_argument('--note',required=True);observe.add_argument('--topic');observe.add_argument('--depends-on',action='append',default=[]);observe.add_argument('--url');observe.add_argument('--visibility',choices=['public','unlisted','private','unknown']);observe.add_argument('--observed-at')
    review = commands.add_parser('review');review.add_argument('project',type=Path);review.add_argument('subject');review.add_argument('--report',required=True,help='Retained input:/output: report ID');review.add_argument('--actor',required=True)
    log = commands.add_parser('journal');log.add_argument('project',type=Path);log.add_argument('--json',action='store_true')
    compose = commands.add_parser('compose');compose.add_argument('project',type=Path);compose.add_argument('spec',type=Path);compose.add_argument('--replace',action='store_true')
    board = commands.add_parser('board');board.add_argument('project',type=Path);board.add_argument('--json',action='store_true')
    bundle = commands.add_parser('bundle');bundle.add_argument('project',type=Path);bundle.add_argument('variant');bundle.add_argument('--output',type=Path,required=True);bundle.add_argument('--draft',action='store_true')
    idea = commands.add_parser('hypothesis');idea.add_argument('project',type=Path);idea.add_argument('spec',type=Path);idea.add_argument('--actor',required=True);idea.add_argument('--provenance',choices=sorted(JOURNAL['PROVENANCE']),required=True)
    metrics = commands.add_parser('outcome');metrics.add_argument('project',type=Path);metrics.add_argument('spec',type=Path);metrics.add_argument('--actor',required=True);metrics.add_argument('--provenance',choices=sorted(JOURNAL['PROVENANCE']),required=True)
    results = commands.add_parser('results');results.add_argument('project',type=Path);results.add_argument('--json',action='store_true');results.add_argument('--compare-age-hours',type=float);results.add_argument('--age-tolerance-hours',type=float,default=6)
    briefing = commands.add_parser('brief');briefing.add_argument('project',type=Path);briefing.add_argument('--json',action='store_true');briefing.add_argument('--limit',type=int,choices=range(1,11),default=3)
    blockers = commands.add_parser('blockers');blockers.add_argument('project',type=Path);blockers.add_argument('--json',action='store_true');blockers.add_argument('--limit',type=int,choices=range(1,21),default=5)
    projection = commands.add_parser('summary');projection.add_argument('project',type=Path);projection.add_argument('--json',action='store_true');projection.add_argument('--public',action='store_true');projection.add_argument('--title');projection.add_argument('--include',action='append',default=[]);projection.add_argument('--output',type=Path);projection.add_argument('--replace',action='store_true');projection.add_argument('--check',action='store_true')
    args = parser.parse_args()
    try:
        path = args.project.resolve()
        if args.command=='blockers':
            checkpoint_bytes=path.read_bytes();data=load(path);state=summary(data,path.parent)
            module=runpy.run_path(str(BASE/'project_blockers.py'))
            view=module['diagnose'](data,state,check_kind)
            view['checkpoint_sha256']=hashlib.sha256(checkpoint_bytes).hexdigest()
            if path.read_bytes()!=checkpoint_bytes:raise ValueError('Project changed during diagnosis; retry')
            print(json.dumps(view,indent=2,ensure_ascii=False) if args.json else module['markdown'](view,args.limit));return
        if args.command=='brief':
            checkpoint_bytes=path.read_bytes();data=load(path);state=summary(data,path.parent)
            module=runpy.run_path(str(BASE/'project_summary.py'))
            files=module['project'](data,path.parent,state['file_problems'],JOURNAL,hashlib.sha256(checkpoint_bytes).hexdigest())
            view=module['working_brief'](data,state,files,args.limit)
            diagnosis=runpy.run_path(str(BASE/'project_blockers.py'))['diagnose'](data,state,check_kind)
            view['completion']={'status':diagnosis['status'],**diagnosis['counts']}
            if path.read_bytes()!=checkpoint_bytes:raise ValueError('Project changed during brief generation; retry')
            print(json.dumps(view,indent=2,ensure_ascii=False) if args.json else module['brief_markdown'](view));return
        if args.command=='results':
            data=load(path);view=CONTENT['report'](data,JOURNAL,file_problems(data,path.parent),args.compare_age_hours,args.age_tolerance_hours)
            print(json.dumps(view,indent=2,allow_nan=False) if args.json else CONTENT['markdown'](view));return
        if args.command=='summary':
            checkpoint_bytes=path.read_bytes()
            data=load(path);module=runpy.run_path(str(BASE/'project_summary.py'))
            view=module['project'](data,path.parent,file_problems(data,path.parent),JOURNAL,
                hashlib.sha256(checkpoint_bytes).hexdigest(),public=args.public,title=args.title,include=args.include)
            if path.read_bytes()!=checkpoint_bytes:raise ValueError('Project changed during summary generation; retry')
            text=json.dumps(view,indent=2,ensure_ascii=False)+'\n' if args.json else module['markdown'](view)
            if args.output:module['export'](text,args.output,path,data,replace=args.replace,check=args.check)
            elif args.check:raise ValueError('--check requires --output')
            else:print(text,end='')
            return
        if args.command=='bundle':
            with locked(path):
                data=load(path);problems=file_problems(data,path.parent)
                view=PRODUCTION['report'](data,problems,JOURNAL['project'](data,problems),path.parent)
                if view is None:raise ValueError('No production composition')
                print(json.dumps(PRODUCTION['build_bundle'](data,view,args.variant,path.parent,args.output,
                    hashlib.sha256(path.read_bytes()).hexdigest(),runpy.run_path(str(BASE/'packet.py'))['cell'],args.draft),indent=2))
            return
        if args.command in {'status','resume','packet','journal','board'}:
            data = load(path)
            if args.command=='packet':
                print(data['production_packet'],end='');return
            if args.command=='journal':
                print(json.dumps({'observations':data.get('journal',[]),'history':data['history']},indent=2));return
            result = summary(data,path.parent)
            if args.command=='board':
                if result['production'] is None:raise ValueError('No composition; use compose first')
                if args.json:print(json.dumps(result['production'],indent=2))
                else:print(PRODUCTION['markdown'](result['production'],runpy.run_path(str(BASE/'packet.py'))['cell']),end='')
                return
            if args.json:
                print(json.dumps(result,indent=2));return
            print('Production checkpoint — manual records; no work executed by this command')
            print('Goal:',result['project']['goal'] or 'not recorded')
            print('Waiting:',json.dumps(result['waiting']))
            for row in result['observations']['effective']:
                print('Observation:',row['id'],row['subject'],row['kind'],row['result'],'—',row['note'])
            if result['observations']['stale']:print('Stale observations:',len(result['observations']['stale']))
            print('Recorded done:',len(result['recorded_done']), '/', len(data['steps']))
            print('Ready to continue:',', '.join(result['ready'][:5]) or 'none')
            if len(result['ready'])>5:print('Additional ready steps:',len(result['ready'])-5)
            print('File problems:',json.dumps(result['file_problems']))
            print('Blocked:',json.dumps(result['blocked']))
            if result['evidence_blockers']:print('Evidence blockers:',json.dumps(result['evidence_blockers']))
            if result['planning_sources_changed']:print('Planning sources changed; review the frozen plan. It was not recalculated.')
            if result['production']:
                print('Variants:',json.dumps({k:{'complete_local_handoff':v['complete_local_handoff'],'remaining':len(v['blockers'])} for k,v in result['production']['variants'].items()}))
            print('Output IDs:',', '.join(result['outputs']))
            return
        if not path.parent.is_dir():
            raise ValueError('Create the project parent directory explicitly first')
        with locked(path):
            if args.command=='create':
                if path.exists():raise ValueError('Project already exists; refusing to overwrite')
                if not args.goal.strip() or not args.note.strip():raise ValueError('Goal and note must be nonempty')
                brief={'blocks':[]};plan={'mode':'manual_production','execution':'not_started','blocks':[]};packet='Manual production project; no tool plan or capability qualification inferred.\n'
                data={'schema_version':2,'project':{'goal':args.goal,'context':args.note},'journal':[],
                      'brief':brief,'plan':plan,'brief_sha256':digest(brief),'plan_sha256':digest(plan),
                      'production_packet':packet,'packet_sha256':digest(packet),'planning_sources':planning_sources(),
                      'steps':[],'inputs':{},'artifacts':{},'history':[]}
                event(data,'create',note='Manual project, no production or QA performed')
            elif args.command=='init':
                if path.exists():raise ValueError('Project already exists; refusing to overwrite')
                data = initial(json.loads(args.brief.read_text()))
            else:
                data = load(path)
                if args.command in {'asset','task','observe','compose','review','hypothesis','outcome'} and data['schema_version']!=2:
                    raise ValueError('Run migrate explicitly before using project memory')
                if args.command=='hypothesis':
                    changed=CONTENT['hypothesis'](data,json.loads(args.spec.read_text()),args.actor,args.provenance,JOURNAL,file_problems(data,path.parent))
                    if not changed:print('Hypothesis unchanged');return
                    data['content_sha256']=digest(data['content']);event(data,'content_hypothesis',identity=data['content']['hypotheses'][-1]['id'])
                elif args.command=='outcome':
                    changed=CONTENT['outcome'](data,json.loads(args.spec.read_text()),args.actor,args.provenance,JOURNAL,file_problems(data,path.parent))
                    if not changed:print('Outcome unchanged');return
                    data['content_sha256']=digest(data['content']);event(data,'content_outcome',identity=data['content']['snapshots'][-1]['id'])
                elif args.command=='compose':
                    compiled=PRODUCTION['compile_project'](data,json.loads(args.spec.read_text()))
                    if data.get('production')==compiled:
                        print('Composition unchanged');return
                    if 'production' in data and not args.replace:raise ValueError('Existing composition differs; inspect and use --replace explicitly')
                    previous=data.get('production')
                    data['production']=compiled;data['production_sha256']=PRODUCTION['digest'](compiled)
                    event(data,'compose',previous=previous,production_sha256=data['production_sha256'])
                    old_bases=PRODUCTION['variant_bases'](previous) if previous else {}
                    new_bases=PRODUCTION['variant_bases'](compiled)
                    recheck={}
                    mats={m['id']:m for m in compiled['materials']}
                    for variant in compiled['variants']:
                        video=variant['delivery']['video']
                        if old_bases.get(variant['id'])!=new_bases[variant['id']] and video is not None and mats[video]['_pin'] is not None:
                            recheck.setdefault(mats[video]['subject'],[]).append(variant['id'])
                    for subject,variants in recheck.items():
                        row=JOURNAL['append'](data,subject,'technical','pending','project_cli','administrative_change',
                            'Cut/composition changed; check final video conformance for '+', '.join(variants)+'. No media QA performed by CLI.')
                        event(data,'composition_recheck',entry=row['id'],variants=variants)
                    invalidate(data,list(evidence_blockers(data,file_problems(data,path.parent))))
                elif args.command=='asset':
                    if not args.identity.strip() or not args.kind.strip() or args.identity in data['artifacts']:
                        raise ValueError('Use a new nonempty artifact ID/kind')
                    data['artifacts'][args.identity]={'kind':args.kind,'scene':None,'file':None}
                    event(data,'declare_artifact',identity=args.identity,kind=args.kind)
                elif args.command=='task':
                    steps={s['id']:s for s in data['steps']}
                    if not args.identity.strip() or not args.label.strip() or args.identity in steps:
                        raise ValueError('Use a new nonempty task ID/label')
                    if any(d not in steps for d in args.after) or any(a not in data['artifacts'] for a in args.requires):
                        raise ValueError('Task dependencies and output IDs must already exist')
                    if args.check_kind and not args.requires:raise ValueError('A check task requires at least one declared artifact')
                    if args.waiting_for is not None and (not args.waiting_for.strip() or not args.note.strip()):
                        raise ValueError('Waiting requires a party and reason')
                    data['steps'].append({'id':args.identity,'label':args.label,'depends_on':list(dict.fromkeys(args.after)),
                        'required_outputs':list(dict.fromkeys(args.requires)),'unmet':[],'state':'blocked' if args.waiting_for else 'planned',
                        'evidence':args.note,'waiting_for':args.waiting_for,'check_kind':args.check_kind,'optional':False,
                        'attestation':'operator_recorded_not_independently_verified'})
                    event(data,'add_task',step=args.identity)
                elif args.command=='review':
                    if args.report==args.subject or not args.actor.strip():
                        raise ValueError('Use distinct retained media/report subjects and an explicit actor')
                    media_pin=JOURNAL['pin'](data,args.subject)
                    report_pin=JOURNAL['pin'](data,args.report)
                    if media_pin is None or report_pin is None:
                        raise ValueError('Media and report must be retained files')
                    problems=file_problems(data,path.parent)
                    if any(t in problems for t in [args.subject,args.report]):
                        raise ValueError('Media/report bytes changed; retain the intended revisions explicitly')
                    report=MEDIA['validate'](MEDIA['read_json'](path.parent/report_pin['path'],report_pin['sha256']),media_pin)
                    if any(t in file_problems(data,path.parent) for t in [args.subject,args.report]):
                        raise ValueError('Media/report changed while importing; repeat on stable files')
                    for kind,result in MEDIA['receipts'](report).items():
                        row=JOURNAL['append'](data,args.subject,kind,result,args.actor,'supplied_report',
                            'Imported media report '+args.report+' sha256='+report_pin['sha256']+
                            '; technical QA combines metadata/decode with applicable visual/motion/sync reviews; judgments are supplied, not independently verified by project CLI.',
                            'media-review:'+kind,[args.report])
                        event(data,'import_media_review',entry=row['id'],report=args.report)
                    invalidate(data,list(evidence_blockers(data,file_problems(data,path.parent))))
                elif args.command=='observe':
                    # An observation of changed/missing bytes cannot claim to describe the retained revision.
                    targets=[args.subject,*args.depends_on]
                    if any(t in file_problems(data,path.parent) for t in targets):
                        raise ValueError('Observation files changed/missing; explicitly retain the intended revision first')
                    row=JOURNAL['append'](data,args.subject,args.kind,args.result,args.actor,args.provenance,args.note,
                        args.topic,args.depends_on,args.url,args.visibility,args.observed_at)
                    if row['result'] in {'fail','rejected','pending'}:
                        blocked=evidence_blockers(data,file_problems(data,path.parent))
                        invalidate(data,list(blocked))
                    event(data,'observe',entry=row['id'])
                elif args.command=='migrate':
                    if data['schema_version']==2:
                        print('Already schema version 2; unchanged');return
                    backup = Path(str(path) + '.v1.bak')
                    with os.fdopen(os.open(backup,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600),'wb') as stream:
                        stream.write(path.read_bytes());stream.flush();os.fsync(stream.fileno())
                    data.update(schema_version=2, project={'goal':'','context':''}, journal=[])
                    event(data,'migrate',from_version=1,backup=backup.name)
                elif args.command=='describe':
                    if data['schema_version']!=2:raise ValueError('Run migrate explicitly before using project memory')
                    if not args.goal.strip() or not args.note.strip():raise ValueError('Goal and note must be nonempty')
                    previous=dict(data['project'])
                    data['project']={'goal':args.goal,'context':args.note}
                    event(data,'describe',previous=previous,project=data['project'])
                elif args.command=='retain':retain(data,path.parent,args.identity,args.file,args.input,args.replace)
                else:mark(data,path.parent,args.step,args.state,args.evidence)
            save(path,data)
        print('Saved checkpoint:',path)
    except (OSError,ValueError,KeyError,TypeError,ImportError) as exc:
        parser.error(str(exc))


if __name__=='__main__':
    main()
