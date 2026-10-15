#!/usr/bin/env python3
"""Preview or run explicitly selected frozen actors, once, with strict CLI capture."""
import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import time
from cli_capture import assess, codex_args


def snapshot(root):
    paths = sorted(root.rglob('*'))
    if any(p.is_symlink() for p in paths):
        raise ValueError('Symlink in actor workspace')
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in paths if p.is_file()}


def run_case(root, case, args, base):
    identity = case['id']
    workspace, evidence = root / 'runs' / identity, root / 'evidence' / identity
    # Exclusive directory reserves the attempt. Never rerun or overwrite a failure.
    evidence.mkdir(parents=True, exist_ok=False)
    prompt = (root / (identity + '-prompt.txt')).read_text()
    freeze = json.loads((root / 'freeze.json').read_text())
    if hashlib.sha256(prompt.encode()).hexdigest() != freeze['prompt_sha256'][identity]:
        raise ValueError('Actor prompt drift: ' + identity)
    before = snapshot(workspace)
    expected = {str(Path(p).relative_to('skills/video-production-router')): digest
                for p, digest in freeze['source_tree_sha256'].items()
                if p != 'skills/video-production-router/references/scenarios.json'}
    actual = {p.removeprefix('router/'): digest for p, digest in before.items() if p.startswith('router/')}
    if actual != expected:
        raise ValueError('Actor source drift: ' + identity)
    command = base + ['-C', str(workspace), '-o', str(evidence / 'answer.txt'), '-']
    (evidence / 'command.json').write_text(json.dumps(command, indent=2) + '\n')
    env = {k: v for k, v in os.environ.items() if k in {'PATH', 'HOME', 'LANG', 'TMPDIR'}}
    env['CODEX_HOME'] = str(args.codex_home)
    start = time.monotonic()
    with (evidence / 'events.jsonl').open('xb') as out, (evidence / 'stderr.txt').open('xb') as err:
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=out, stderr=err,
                                   env=env, start_new_session=True)
        try:
            process.communicate(prompt.encode(), timeout=args.timeout)
            code = process.returncode
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait()
            code = 124
    after = snapshot(workspace)
    answer = evidence / 'answer.txt'
    raw = (evidence / 'events.jsonl').read_bytes()
    # Invalid UTF-8 remains in the raw artifact and fails; never silently discard it.
    try:
        capture = assess(raw.decode('utf-8'), code, answer.is_file() and bool(answer.read_text().strip()), before == after)
    except UnicodeError as exc:
        capture = {'ready_for_grading': False, 'status': 'infrastructure_incomplete', 'decode_error': str(exc)}
    result = {'id': identity, 'exit_code': code, 'duration_seconds': round(time.monotonic() - start, 2),
              'files_before': before, 'files_after': after, 'workspace_unchanged': before == after,
              'capture': capture, 'events_sha256': hashlib.sha256(raw).hexdigest(),
              'turn_completed': capture.get('trace', {}).get('complete', False),
              'answer_present': answer.is_file() and bool(answer.read_text().strip())}
    (evidence / 'execution.json').write_text(json.dumps(result, indent=2) + '\n')
    return {'id': identity, 'status': capture['status'], 'duration_seconds': result['duration_seconds']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    parser.add_argument('--case', action='append', required=True, help='Explicit frozen case ID; repeat to select')
    parser.add_argument('--execute', action='store_true', help='Default is a no-model preview')
    parser.add_argument('--jobs', type=int, choices=[1, 2], default=1)
    parser.add_argument('--max-cases', type=int, default=8)
    parser.add_argument('--timeout', type=int, default=240)
    parser.add_argument('--codex-home', type=Path)
    parser.add_argument('--model', default='gpt-6.1-sol')
    parser.add_argument('--effort', default='medium', choices=['low', 'medium', 'high'])
    args = parser.parse_args()
    cases = json.loads((args.root / 'cases.json').read_text())
    ids = [c['id'] for c in cases]
    if len(ids) != len(set(ids)) or len(args.case) != len(set(args.case)) or not set(args.case) <= set(ids):
        parser.error('Duplicate or unknown case IDs')
    if not all(isinstance(i, str) and Path(i).name == i and i not in {'.', '..'} for i in ids):
        parser.error('Unsafe case ID')
    if not 0 < len(args.case) <= args.max_cases or not 1 <= args.timeout <= 600:
        parser.error('Case budget or timeout exceeded')
    selected = [c for c in cases if c['id'] in args.case]
    print(json.dumps({'cases': [c['id'] for c in selected], 'model_calls': len(selected),
                      'jobs': args.jobs, 'timeout_seconds': args.timeout, 'execute': args.execute}), flush=True)
    if not args.execute:
        return
    if not args.codex_home or not args.codex_home.is_dir():
        parser.error('--codex-home must name a prepared isolated authentication/config home')
    disabled = set()
    for folder in [Path.home() / '.codex/skills', Path.home() / '.agents/skills']:
        if folder.exists():
            for path in folder.rglob('SKILL.md'):
                disabled.update([str(path), str(path.resolve())])
            for path in folder.iterdir():
                if (path / 'SKILL.md').is_file():
                    disabled.update([str(path / 'SKILL.md'), str((path / 'SKILL.md').resolve())])
    base = codex_args('codex', args.model, args.effort, disabled)
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(lambda case: run_case(args.root, case, args, base), selected))
    print(json.dumps(results, indent=2), flush=True)
    if any(r['status'] != 'ready_for_grading' for r in results):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
