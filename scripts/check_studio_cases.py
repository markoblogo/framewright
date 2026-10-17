#!/usr/bin/env python3
"""Run frozen synthetic studio briefs through the public CLI; no media/model calls."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def check(packet):
    frozen = json.loads((packet / 'freeze.json').read_text())
    case_file = packet / 'cli-cases.json'
    if hashlib.sha256(case_file.read_bytes()).hexdigest() != frozen['cli_cases_sha256']:
        raise ValueError('Frozen CLI cases changed')
    for relative, expected in frozen['source_tree_sha256'].items():
        if hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() != expected:
            raise ValueError('Evaluated source changed: ' + relative)
    cases = json.loads(case_file.read_text())
    results = []
    for case in cases:
        # Input/output files contain JSON only; no source path is opened by workflow.py.
        with tempfile.TemporaryDirectory(prefix='framewright-studio-case-') as directory:
            source = Path(directory) / 'spec.json'
            source.write_text(json.dumps(case['spec']))
            command = [sys.executable, str(ROOT / 'skills/video-production-router/scripts/workflow.py'), str(source)]
            run = subprocess.run(command, text=True, capture_output=True, timeout=20)
        expect, failures = case['expected'], []
        report = json.loads(run.stdout) if run.returncode == 0 else None
        if 'error' in expect:
            if run.returncode == 0 or expect['error'] not in run.stderr:
                failures.append('Expected explicit rejection: ' + expect['error'])
        elif run.returncode:
            failures.append('Unexpected CLI rejection')
        else:
            plan = report['route_plan']
            actual = {'status': plan['status'],
                      'publication_blocked': bool(report['publication_blockers']),
                      'production_blocked': bool(report['production_blockers'])}
            for key in actual:
                if key in expect and actual[key] != expect[key]:
                    failures.append(f'{key}: expected {expect[key]!r}, got {actual[key]!r}')
            tools = {t for b in plan['blocks'] for t in b['tools']}
            if not set(expect.get('tools', [])).issubset(tools):
                failures.append('Missing expected tools: ' + str(set(expect['tools']) - tools))
            unmet = {f for b in plan['blocks'] for f in b['unmet']}
            if not set(expect.get('unmet', [])).issubset(unmet):
                failures.append('Missing expected unmet requirements')
            if expect.get('music_use') and plan['music']['intended_use'] != expect['music_use']:
                failures.append('Music did not inherit whole-film purpose')
            if report['execution_authorized'] or report['publication_authorized'] or plan['execution'] != 'not_started':
                failures.append('Unexpected execution/publication grant')
            if any(c['evidence'] != 'tested' for b in plan['blocks'] for c in b['coverage']):
                failures.append('Untested capability entered tested-only workflow')
            if any(x['file'] is not None or x['qa'] != 'not_run' for x in report['outputs'].values()):
                failures.append('Invented output or verified QA')
        results.append({'id':case['id'], 'passed':not failures, 'failures':failures,
                        'exit_code':run.returncode, 'report':report, 'stderr':run.stderr})
    return {'scope':'deterministic_cli_only', 'source_commit':frozen['source_commit'],
            'cases':len(results), 'passed':sum(r['passed'] for r in results), 'results':results}


def verify_retained(packet):
    """Check retained bytes/capture, not the correctness of controller grades."""
    from cli_capture import assess
    pins = json.loads((packet / 'evidence-hashes.json').read_text())
    for relative, digest in pins.items():
        path = (packet / relative).resolve()
        if not path.is_relative_to(packet.resolve()) or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError('Retained evidence drift: ' + relative)
    cases = json.loads((packet / 'cases.json').read_text())
    frozen = json.loads((packet / 'freeze.json').read_text())
    inputs = {row['id']:row for row in json.loads((packet / 'inputs.json').read_text())}
    expected_router = {'router/' + str(Path(p).relative_to('skills/video-production-router')):digest
                       for p,digest in frozen['source_tree_sha256'].items()
                       if not p.endswith('/references/scenarios.json')}
    for case in cases:
        base = packet / 'evidence' / case['id']
        execution = json.loads((base / 'execution.json').read_text())
        raw = (base / 'events.jsonl').read_text()
        capture = assess(raw, execution['exit_code'], bool((base / 'answer.txt').read_text().strip()),
                         execution['files_before'] == execution['files_after'])
        if not capture['ready_for_grading'] or capture['events_sha256'] != execution['events_sha256']:
            raise ValueError('Incomplete or changed capture: ' + case['id'])
        row = inputs[case['id']]
        expected = {**expected_router, **{name:hashlib.sha256(value.encode()).hexdigest() for name,value in row['fixtures'].items()}}
        if execution['files_before'] != expected or hashlib.sha256(row['prompt'].encode()).hexdigest() != frozen['prompt_sha256'][case['id']]:
            raise ValueError('Mixed source,fixtures or prompt: ' + case['id'])
    print(f'PASS: retained hashes/source/fixtures and{len(cases)} complete captures; manual semantic grades not independently validated')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('packet', type=Path)
    p.add_argument('--output', type=Path)
    p.add_argument('--verify-retained', action='store_true', help='Verify saved evidence only; no actor calls or CLI replay')
    args = p.parse_args()
    try:
        if args.verify_retained:
            verify_retained(args.packet)
            return
        result = check(args.packet)
        encoded = json.dumps(result, indent=2) + '\n'
        if args.output:
            if args.output.exists():
                raise ValueError('Refuse to overwrite retained results')
            args.output.write_text(encoded)
        print(json.dumps({k:v for k,v in result.items() if k!='results'}))
        for row in result['results']:
            print(row['id'] + ': ' + ('PASS' if row['passed'] else 'FAIL ' + '; '.join(row['failures'])))
        if result['passed'] != result['cases']:
            raise SystemExit(1)
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        p.error(str(exc))


if __name__ == '__main__':
    main()
