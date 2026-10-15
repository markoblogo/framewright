#!/usr/bin/env python3
"""Lossless JSONL intake and conservative readiness checks for CLI actors."""
import hashlib
import json


def parse_events(raw):
    events, errors = [], []
    for number, line in enumerate(raw.splitlines(), 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
            if not isinstance(event, dict) or not isinstance(event.get('type'), str):
                raise ValueError('expected an event object with a type')
            events.append(event)
        except (ValueError, TypeError) as exc:
            errors.append(f'line {number}: {exc}')
    return events, errors


def inspect_events(events):
    starts, ends, errors = {}, {}, []
    turns_started = turns_completed = 0
    for event in events:
        kind = event.get('type')
        if kind == 'turn.started':
            turns_started += 1
        if kind == 'turn.completed':
            turns_completed += 1
            if turns_started != 1:
                errors.append('turn completion without exactly one start')
        if kind in {'turn.failed', 'error'}:
            errors.append(f'CLI {kind}')
        item = event.get('item', {})
        if not isinstance(item, dict) or item.get('type') != 'command_execution':
            continue
        identity, command = item.get('id'), item.get('command')
        if not isinstance(identity, str) or not identity or not isinstance(command, str) or not command:
            errors.append('invalid command identity/text')
            continue
        if turns_started != 1 or turns_completed:
            errors.append(f'{identity}: command outside active turn')
        if kind == 'item.started':
            if identity in starts:
                errors.append(f'{identity}: duplicate start')
            starts[identity] = command
        elif kind == 'item.completed':
            if identity in ends or identity not in starts or starts[identity] != command:
                errors.append(f'{identity}: duplicate, unmatched or changed completion')
            if type(item.get('exit_code')) is not int or item.get('status') not in {'completed', 'failed'}:
                errors.append(f'{identity}: nonterminal completion')
            ends[identity] = command
        elif kind != 'item.updated':
            errors.append(f'{identity}: unexpected command event {kind}')
    missing = sorted(starts.keys() - ends.keys())
    if missing:
        errors.append('unfinished commands: ' + ', '.join(missing))
    if turns_started != 1 or turns_completed != 1:
        errors.append('expected one started and completed turn')
    return {'complete': not errors, 'errors': errors, 'unfinished_command_ids': missing,
            'commands_started': len(starts), 'commands_completed': len(ends)}


def assess(raw, exit_code, answer_present, workspace_unchanged):
    events, malformed = parse_events(raw)
    trace = inspect_events(events)
    ready = not malformed and trace['complete'] and exit_code == 0 and answer_present and workspace_unchanged
    return {'status': 'ready_for_grading' if ready else 'infrastructure_incomplete',
            'ready_for_grading': ready, 'trace': trace, 'parse_errors': malformed,
            'events_sha256': hashlib.sha256(raw.encode()).hexdigest()}


def codex_args(binary, model, effort, disabled_skills):
    settings = ['model_reasoning_effort=' + json.dumps(effort), 'allow_login_shell=false',
                'project_doc_max_bytes=0', 'web_search="disabled"', 'features.apps=false',
                'features.plugins=false', 'features.multi_agent=false',
                'features.skip_host_skill_discovery=true', 'shell_environment_policy.inherit="none"',
                'shell_environment_policy.set.PATH="/opt/homebrew/bin:/usr/bin:/bin"']
    settings.append('skills.config=[' + ','.join('{path=' + json.dumps(p) + ',enabled=false}' for p in sorted(disabled_skills)) + ']')
    args = [binary, 'exec', '--ignore-user-config', '--ignore-rules', '--ephemeral', '--skip-git-repo-check', '-m', model]
    for setting in settings:
        args += ['-c', setting]
    return args + ['-s', 'read-only', '--json']
