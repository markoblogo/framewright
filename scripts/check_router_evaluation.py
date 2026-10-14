#!/usr/bin/env python3
"""Verify retained evaluation packets, not model behaviour or shell safety."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path


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


def check_packet(root):
    root = Path(root)
    manifest = json.loads((root / 'manifest.json').read_text())
    require(manifest.get('schema_version') == 1, 'Unknown evaluation schema')
    files = manifest.get('files', {})
    require({'cases.json', 'results.json', 'grades.json'} <= files.keys(), 'Missing evidence files')
    for name, digest in files.items():
        require(Path(name).name == name and name not in {'.', '..'}, 'Unsafe evidence filename')
        require(hashlib.sha256((root / name).read_bytes()).hexdigest() == digest, f'Hash mismatch: {name}')
    cases = indexed(json.loads((root / 'cases.json').read_text()), 'cases')
    results = indexed(json.loads((root / 'results.json').read_text()), 'results')
    grades = indexed(json.loads((root / 'grades.json').read_text())['cases'], 'grades')
    require(cases and cases.keys() == results.keys() == grades.keys(), 'Incomplete case set')
    passed = 0
    for identity, case in cases.items():
        result, grade = results[identity], grades[identity]
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('packets', nargs='*', type=Path)
    parser.add_argument('--root', type=Path, help='Discover date/run packets without hardcoding dates')
    args = parser.parse_args()
    packets = args.packets + ([p.parent for p in sorted(args.root.glob('*/*/manifest.json'))] if args.root else [])
    if not packets:
        parser.error('No evidence packets found')
    for packet in packets:
        print(f'{packet.name}: {check_packet(packet)}')
