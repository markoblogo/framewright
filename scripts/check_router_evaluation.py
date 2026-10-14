#!/usr/bin/env python3
"""Verify retained evaluation packets, not model behaviour or shell safety."""
import argparse
from collections import Counter
import hashlib
import json
import re
from pathlib import Path, PurePosixPath
import zipfile


def require(condition, message):
    if not condition:
        raise ValueError(message)


def indexed(rows, label):
    require(isinstance(rows, list), f'{label}: expected a list')
    result = {}
    for row in rows:
        identity = row.get('id') if isinstance(row, dict) else None
        require(isinstance(identity, str) and identity and identity not in result, f'{label}: incomplete or duplicate case set')
        result[identity] = row
    return result


def verify_files(root, manifest, required):
    files = manifest.get('files', {})
    require(isinstance(files, dict) and required <= files.keys(), 'Missing evidence files')
    for name, digest in files.items():
        require(Path(name).name == name and name not in {'.', '..'}, 'Unsafe evidence filename')
        require(hashlib.sha256((root / name).read_bytes()).hexdigest() == digest, f'Hash mismatch: {name}')


def check_calibration(root):
    root = Path(root)
    manifest = json.loads((root / 'manifest.json').read_text())
    require(manifest.get('schema_version') == 1, 'Unknown calibration schema')
    verify_files(root, manifest, {'gold.json', 'cases.json', 'grades.json'})
    gold = json.loads((root / 'gold.json').read_text())
    cases = indexed(json.loads((root / 'cases.json').read_text()), 'calibration cases')
    grades = indexed(json.loads((root / 'grades.json').read_text())['cases'], 'calibration grades')
    require(gold and gold.keys() == cases.keys() == grades.keys(), 'Incomplete calibration case set')
    if manifest.get('blind_ids') is True:
        require(all(re.fullmatch(r'c-[0-9a-f]{12}', identity) for identity in gold), 'Blind calibration needs opaque IDs')
        require({'freeze.json', 'input.json'} <= manifest['files'].keys(), 'Missing frozen calibration inputs')
        frozen = json.loads((root / 'freeze.json').read_text())
        require(frozen['gold_sha256'] == hashlib.sha256((root / 'gold.json').read_bytes()).hexdigest(), 'Frozen calibration gold mismatch')
        inputs = json.loads((root / 'input.json').read_text())
        require({x['case']['id'] for x in inputs} == gold.keys() and len(inputs) == len(gold), 'Calibration input case set differs')
        batches = {f'batch-{i // 6 + 1}.json': hashlib.sha256((json.dumps(inputs[i:i + 6], indent=2) + '\n').encode()).hexdigest() for i in range(0, len(inputs), 6)}
        require(batches == frozen['input_sha256'], 'Frozen calibration input mismatch')
    correct = 0
    for identity, expected in gold.items():
        require(type(expected.get('expected_pass')) is bool and expected.get('group') in {'required', 'forbidden'}, 'Invalid calibration gold')
        for group in ('required', 'forbidden'):
            require(Counter(x.get('criterion') for x in grades[identity].get(group, [])) == Counter(cases[identity][group]), 'Invalid calibration criteria')
        rows = grades[identity][expected['group']]
        require(len(rows) == 1 and rows[0]['criterion'] == expected['criterion'], 'Invalid calibration target')
        require(rows[0].get('verdict') in {'PASS', 'FAIL', 'INSUFFICIENT_EVIDENCE'}, 'Invalid calibration verdict')
        correct += int((rows[0]['verdict'] == 'PASS') == expected['expected_pass'])
    counts = {'controls': len(gold), 'correct': correct}
    require(counts == manifest.get('counts') and correct == len(gold), 'Grader calibration failed')
    return counts


def check_snapshot(root, manifest):
    name = manifest.get('source_snapshot')
    require(name in manifest['files'] and 'freeze.json' in manifest['files'], 'Missing retained source snapshot')
    frozen = json.loads((root / 'freeze.json').read_text())['source_tree_sha256']
    require(isinstance(frozen, dict) and frozen, 'Empty source snapshot specification')
    expected = {}
    for source, digest in frozen.items():
        path = PurePosixPath(source)
        require(path.parts[:2] == ('skills', 'video-production-router') and '..' not in path.parts, 'Unsafe frozen source path')
        expected[str(path.relative_to('skills'))] = digest
    with zipfile.ZipFile(root / name) as archive:
        members = archive.infolist()
        require(len({i.filename for i in members}) == len(members), 'Duplicate snapshot member')
        require({i.filename for i in members} == expected.keys(), 'Snapshot member set differs from frozen source')
        require(sum(i.file_size for i in members) <= 8 * 1024 * 1024, 'Source snapshot is unexpectedly large')
        for item in members:
            require((item.external_attr >> 16) & 0o170000 != 0o120000, 'Snapshot symlinks are not supported')
            require(hashlib.sha256(archive.read(item)).hexdigest() == expected[item.filename], f'Source hash mismatch: {item.filename}')


def check_packet(root):
    root = Path(root)
    manifest = json.loads((root / 'manifest.json').read_text())
    require(manifest.get('schema_version') in {1, 2, 3}, 'Unknown evaluation schema')
    verify_files(root, manifest, {'cases.json', 'results.json', 'grades.json'})
    if manifest['schema_version'] >= 2:
        check_snapshot(root, manifest)
    if manifest['schema_version'] == 3:
        name = manifest.get('calibration')
        require(isinstance(name, str) and Path(name).name == name and name not in {'.', '..'}, 'Invalid calibration path')
        require(hashlib.sha256((root / name / 'manifest.json').read_bytes()).hexdigest() == manifest.get('calibration_manifest_sha256'), 'Calibration manifest hash mismatch')
        require(json.loads((root / name / 'manifest.json').read_text()).get('blind_ids') is True, 'Qualification needs blind calibration IDs')
        check_calibration(root / name)
        for shared in ('protocol.txt', 'grader-config.json'):
            require(shared in manifest['files'], f'Missing shared grader evidence: {shared}')
            require((root / shared).read_bytes() == (root / name / shared).read_bytes(), f'Calibration and actor grading differ: {shared}')
    cases = indexed(json.loads((root / 'cases.json').read_text()), 'cases')
    results = indexed(json.loads((root / 'results.json').read_text()), 'results')
    grades = indexed(json.loads((root / 'grades.json').read_text())['cases'], 'grades')
    require(cases and cases.keys() == results.keys() == grades.keys(), 'Incomplete case set')
    passed = 0
    for identity, case in cases.items():
        result, grade = results[identity], grades[identity]
        if manifest['schema_version'] == 3:
            modes = case.get('required_modes', {})
            require(modes.keys() == set(case['required']) and all(v in {'plan', 'observed', 'decision'} for v in modes.values()), f'{identity}: missing typed criteria')
        require(isinstance(result.get('answer'), str) and result['answer'].strip(), f'{identity}: missing answer')
        execution = result['execution']
        ok = execution.get('exit_code') == 0 and execution.get('turn_completed') is True and execution.get('workspace_unchanged') is True
        for group in ('required', 'forbidden'):
            rows = grade.get(group, [])
            require(Counter(x.get('criterion') for x in rows) == Counter(case[group]), f'{identity}: incomplete or duplicate {group} criteria')
            for row in rows:
                require(row.get('verdict') in {'PASS', 'FAIL', 'INSUFFICIENT_EVIDENCE'} and isinstance(row.get('evidence'), str) and row['evidence'].strip(), f'{identity}: unsupported grade')
                ok = ok and row['verdict'] == 'PASS'
        for review in ('route_review', 'trace_review'):
            require(result.get(review, {}).get('verdict') in {'PASS', 'FAIL', 'INSUFFICIENT_EVIDENCE'}, f'{identity}: missing {review}')
            ok = ok and result[review]['verdict'] == 'PASS'
        started, completed = {}, {}
        require(isinstance(result.get('trace'), list), f'{identity}: missing trace')
        for event in result['trace']:
            item = event.get('item', {})
            if item.get('type') != 'command_execution':
                continue
            bucket = started if event['type'] == 'item.started' else completed if event['type'] == 'item.completed' else None
            if bucket is not None:
                require(item.get('id') not in bucket, f'{identity}: duplicate command event')
                bucket[item['id']] = item
        require(started.keys() == completed.keys(), f'{identity}: Unfinished command trace')
        for key in started:
            require(started[key]['command'] == completed[key]['command'] and isinstance(completed[key].get('exit_code'), int), f'{identity}: inconsistent command completion')
        passed += int(ok)
    counts = {'cases': len(cases), 'passed': passed}
    require(manifest.get('counts') == counts, 'Declared counts disagree with retained evidence')
    return counts


def check_qualification(repo, path):
    repo = Path(repo).resolve()
    record = json.loads(Path(path).read_text())
    require(record.get('schema_version') == 1 and record.get('status') == 'model_checked_planning_scope' and record.get('scope') == 'synthetic_read_only_planning', 'Unsupported qualification scope')
    relative = record.get('packet')
    require(isinstance(relative, str) and relative and not Path(relative).is_absolute() and '..' not in Path(relative).parts, 'Unsafe qualification packet path')
    packet = (repo / relative).resolve()
    require(packet.is_relative_to(repo), 'Qualification packet escapes repository')
    manifest = json.loads((packet / 'manifest.json').read_text())
    require(manifest.get('schema_version') == 3, 'Qualification needs calibrated grading and source snapshot')
    counts = check_packet(packet)
    require(counts['cases'] == counts['passed'], 'Incomplete behavioural qualification')
    cases = indexed(json.loads((packet / 'cases.json').read_text()), 'qualification cases')
    expected = record.get('case_ids', [])
    require(isinstance(expected, list) and len(set(expected)) == len(expected) and set(expected) == cases.keys(), 'Qualification case set differs')
    baseline = json.loads((repo / 'skills/video-production-router/references/scenarios.json').read_text())['cases']
    require({c['id'] for c in baseline} <= cases.keys(), 'Qualification case set misses baseline scenarios')
    freeze = json.loads((packet / 'freeze.json').read_text())
    require(freeze.get('protocol_version') == 2, 'Qualification needs typed planning criteria')
    require(freeze['case_sha256'] == hashlib.sha256((packet / 'cases.json').read_bytes()).hexdigest(), 'Frozen case hash mismatch')
    require(freeze['protocol_sha256'] == hashlib.sha256((packet / 'protocol.txt').read_bytes()).hexdigest(), 'Frozen protocol hash mismatch')
    require(record.get('model') == freeze['model'] and record.get('reasoning_effort') == freeze['effort'], 'Qualification model/config differs')
    inputs = indexed(json.loads((packet / 'inputs.json').read_text()), 'qualification inputs')
    require(inputs.keys() == cases.keys() == freeze['prompt_sha256'].keys(), 'Qualification prompt case set differs')
    for identity, row in inputs.items():
        require(hashlib.sha256(row['prompt'].encode()).hexdigest() == freeze['prompt_sha256'][identity], f'Prompt hash mismatch: {identity}')
    results = indexed(json.loads((packet / 'results.json').read_text()), 'qualification results')
    for identity, row in inputs.items():
        fixtures = row.get('fixtures', {})
        before = results[identity]['execution']['files_before']
        require(isinstance(fixtures, dict) and fixtures.keys() == {p for p in before if not p.startswith('router/')}, f'{identity}: fixture set differs')
        for name, text in fixtures.items():
            require(hashlib.sha256(text.encode()).hexdigest() == before[name], f'Fixture hash mismatch: {identity}/{name}')
    sources = freeze['source_tree_sha256']
    expected_router = {'router/' + Path(p).relative_to('skills/video-production-router').as_posix() for p in sources}
    hidden = 'router/references/scenarios.json'
    expected_router.discard(hidden)
    for identity, result in results.items():
        execution = result['execution']
        for phase in ('files_before', 'files_after'):
            actual = {p for p in execution[phase] if p.startswith('router/')}
            require(hidden not in actual, f'{identity}: Hidden gold in actor workspace')
            require(actual == expected_router, f'{identity}: actor router file set differs from snapshot')
    current_sources = {str(p.relative_to(repo)) for p in (repo / 'skills/video-production-router').rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    require(current_sources == sources.keys(), 'Current source set differs from evaluated snapshot')
    for source, digest in sources.items():
        require(hashlib.sha256((repo / source).read_bytes()).hexdigest() == digest, f'Current source drift: {source}')
        # Scenario gold is deliberately withheld from actor contexts.
        relative = Path(source).relative_to('skills/video-production-router').as_posix()
        if relative == 'references/scenarios.json':
            continue
        actor_path = 'router/' + relative
        for identity, result in results.items():
            execution = result['execution']
            require(execution['files_before'] == execution['files_after'], f'{identity}: changed actor workspace')
            require(execution['files_before'].get(actor_path) == digest, f'{identity}: mixed evaluated sources')
    return {'status': record['status'], 'scope': record['scope'], 'cases': counts['cases']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('packets', nargs='*', type=Path)
    parser.add_argument('--root', type=Path, help='Discover date/run packets without hardcoding dates')
    parser.add_argument('--qualification', type=Path, help='Check scoped qualification against current sources')
    args = parser.parse_args()
    packets = args.packets + ([p.parent for p in sorted(args.root.glob('*/*/manifest.json'))] if args.root else [])
    if not packets and not args.qualification:
        parser.error('No evidence packets found')
    for packet in packets:
        print(f'{packet.name}: {check_packet(packet)}')
    if args.qualification:
        print(check_qualification(args.qualification.resolve().parent, args.qualification))
