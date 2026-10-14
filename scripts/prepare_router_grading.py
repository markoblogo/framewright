#!/usr/bin/env python3
"""Prepare complete immutable grading batches, retaining actor scope and facts."""
import argparse
import hashlib
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def records(root):
    root = Path(root)
    cases = json.loads((root / 'cases.json').read_text())
    frozen = json.loads((root / 'freeze.json').read_text())
    result = {}
    seen = set()
    for case in cases:
        identity = case['id']
        require(isinstance(identity, str) and identity not in {'.', '..'} and Path(identity).name == identity and identity not in seen, 'Unsafe or duplicate case ID')
        seen.add(identity)
        evidence = root / 'evidence' / identity
        if not (evidence / 'execution.json').exists():
            continue
        execution = json.loads((evidence / 'execution.json').read_text())
        workspace = root / 'runs' / identity
        before = execution['files_before']
        require(before == execution['files_after'] and execution['workspace_unchanged'], f'{identity}: changed fixture')
        paths = [p for p in sorted(workspace.rglob('*')) if p.is_file()]
        require(all(not p.is_symlink() and p.resolve().is_relative_to(workspace.resolve()) for p in paths), f'{identity}: symlink or path outside fixture')
        actual = {p.relative_to(workspace).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
        require(actual == before, f'{identity}: current fixture differs from execution snapshot')
        prompt = (root / (identity + '-prompt.txt')).read_text()
        require(hashlib.sha256(prompt.encode()).hexdigest() == frozen['prompt_sha256'][identity], f'{identity}: actor prompt drift')
        fixtures = {name: (workspace / name).read_text() for name in before if not name.startswith('router/')}
        events = [json.loads(line) for line in (evidence / 'events.jsonl').read_text().splitlines() if line.strip()]
        commands = [{'event': e['type'], 'item': {k: v for k, v in e['item'].items() if k != 'aggregated_output'}} for e in events if e.get('item', {}).get('type') == 'command_execution']
        other = [e for e in events if e.get('item', {}).get('type') not in {None, 'command_execution', 'agent_message', 'reasoning'}]
        result[identity] = {'case': case, 'actor_prompt': prompt, 'input_inventory': sorted(before), 'fixtures': fixtures,
                            'execution': {k: v for k, v in execution.items() if k not in {'files_before', 'files_after'}},
                            'answer': (evidence / 'answer.txt').read_text(), 'commands': commands, 'other_tool_events': other}
    return cases, result


def decision_sources(root):
    """Frozen shared decision text is fact context, not evidence of an actor read."""
    root = Path(root)
    frozen = json.loads((root / 'freeze.json').read_text())
    cases = json.loads((root / 'cases.json').read_text())
    result = {}
    for source, digest in frozen.get('source_tree_sha256', {}).items():
        path = Path(source)
        require(path.parts[:2] == ('skills', 'video-production-router') and '..' not in path.parts,
                'Unsafe frozen decision source')
        relative = path.relative_to('skills/video-production-router')
        if str(relative) == 'references/scenarios.json':
            continue  # Withheld rubric must not enter the fact corpus.
        supplied = root / 'runs' / cases[0]['id'] / 'router' / relative
        require(supplied.is_file() and not supplied.is_symlink() and supplied.resolve().is_relative_to((root / 'runs' / cases[0]['id']).resolve()), 'Missing, symlinked or outside decision source')
        require(hashlib.sha256(supplied.read_bytes()).hexdigest() == digest, 'Frozen decision source drift')
        result['router/' + relative.as_posix()] = supplied.read_text()
    return result


def prepare(root, batch_size=6):
    root = Path(root)
    require(type(batch_size) is int and batch_size > 0, 'Batch size must be positive')
    cases, ready = records(root)
    output = root / 'grade-input'
    output.mkdir(exist_ok=True)
    shared = json.dumps(decision_sources(root), indent=2) + '\n'
    path = output / 'decision-sources.json'
    if path.exists():
        require(path.read_text() == shared, 'Retained decision source context changed')
    else:
        with path.open('x') as stream:
            stream.write(shared)
    count = 0
    for start in range(0, len(cases), batch_size):
        expected = cases[start:start + batch_size]
        if not all(c['id'] in ready for c in expected):
            continue
        text = json.dumps([ready[c['id']] for c in expected], indent=2) + '\n'
        path = output / f'batch-{start // batch_size + 1}.json'
        if path.exists():
            require(path.read_text() == text, 'Retained grading input changed; archive the old attempt, never overwrite it')
        else:
            with path.open('x') as stream:
                stream.write(text)
        count += len(expected)
    return count


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    args = parser.parse_args()
    print(f'{prepare(args.root)} records in complete immutable batches')
