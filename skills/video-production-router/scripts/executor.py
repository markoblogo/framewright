#!/usr/bin/env python3
"""Execute one explicitly authorised local media inspection or review clip."""
import argparse
import fcntl
import json
import math
import os
from pathlib import Path
import runpy
import signal
import shutil
import subprocess
import sys
import tempfile
import uuid

BASE = Path(__file__).resolve().parent
P = runpy.run_path(str(BASE / 'project.py'))
R = runpy.run_path(str(BASE / 'revisions.py'))
RESOURCES = runpy.run_path(str(BASE / 'resources.py'))
STATE = runpy.run_path(str(BASE / 'executor_state.py'))
ADMISSION = runpy.run_path(str(BASE / 'admission.py'))


def run(args):
    if args.observe_resources and args.tool == 'revision-comparison':
        raise ValueError('Owned worker sampling currently supports inspection and review-clip only')
    if args.tool == 'revision-comparison':
        if (not args.request or not math.isfinite(args.context) or not 0.1 <= args.context <= 5 or
                (args.after_start is None) != (args.after_end is None)):
            raise ValueError('Comparison needs a retained request, context 0.1–5s and both after bounds or neither')
        if args.after_start is not None and (not math.isfinite(args.after_start) or
                not math.isfinite(args.after_end) or args.after_start < 0 or args.after_end <= args.after_start):
            raise ValueError('After bounds must be finite and increasing')
    elif args.request or args.after_start is not None or args.after_end is not None:
        raise ValueError('Request and after bounds apply only to revision-comparison')
    if args.tool == 'review-clip':
        if (args.start is None or args.end is None or
                not all(math.isfinite(n) for n in (args.start, args.end, args.context)) or
                args.start < 0 or args.end <= args.start or not 0.1 <= args.context <= 5 or
                args.end - args.start + 2 * args.context > 30):
            raise ValueError('Use a finite positive interval, 0.1–5s context and at most 30s total')
    elif args.start is not None or args.end is not None:
        raise ValueError('Interval arguments apply only to review-clip')
    project = args.project.resolve(strict=True)
    with P['locked'](project):
        data = P['load'](project)
        if args.tool in {'review-clip', 'revision-comparison'} and data['schema_version'] != 2:
            raise ValueError('Migrate this project before creating a source-bound review output')
        state = P['summary'](data, project.parent)
        if args.step not in state['ready']:
            raise ValueError('Step is not ready; inspect project status and resolve its blockers')
        step = next(s for s in data['steps'] if s['id'] == args.step)
        if args.output not in step['required_outputs']:
            raise ValueError('Output must be required by the selected step')
        expected = {'local-media-review': 'review-report', 'review-clip': 'review-preview',
                    'revision-comparison': 'revision-comparison'}[args.tool]
        if data['artifacts'][args.output]['kind'] != expected:
            raise ValueError(args.tool + ' requires output kind ' + expected)
        if data['artifacts'][args.output]['file'] is not None:
            raise ValueError('Output already retained; review it before another run')
        kind, sep, identity = args.source.partition(':')
        if not sep or kind not in {'input', 'output'}:
            raise ValueError('Source must name a retained input:ID or output:ID')
        item = data['inputs'].get(identity) if kind == 'input' else data['artifacts'].get(identity, {}).get('file')
        if not item:
            raise ValueError('Source has not been retained')
        source = (project.parent / item['path']).resolve(strict=True)
        if args.tool == 'revision-comparison':
            request_pin = P['JOURNAL']['pin'](data, args.request)
            request_path = (project.parent / request_pin['path']).resolve(strict=True)
            request = R['checked_record'](data, project, request_path, 'framewright-revision-request-v1')
            if request['subject'] != args.request:
                raise ValueError('Request subject does not match its retained identity')
            if request['baseline_subject'] == args.source:
                raise ValueError('Retain corrected media under a distinct identity')
        if not args.execute:
            return {'step': args.step, 'tool': args.tool, 'source': args.source,
                    'output': args.output, 'state': 'preview_only', 'execution_started': False,
                    'admission': 'required_on_execute' if args.step in data.get('execution_routes',{}) else 'legacy_unbound_action'}
        # All cooperating executor invocations share one host lock. No queue or background worker.
        lockpath = STATE['host_lock_path']()
        flags = os.O_CREAT | os.O_RDWR | getattr(os, 'O_NOFOLLOW', 0)
        fd = os.open(lockpath, flags, 0o600)
        with os.fdopen(fd, 'a') as lock:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as exc:
                raise ValueError('Another Framewright executor is running') from exc
            gate=ADMISSION['check'](data,project,args.step,P,args)
            if gate is not None:
                P['event'](data,'execution_admission_checked',step=args.step,report=gate)
                P['save'](project,data)
                if gate['result']!='admitted_local_action':
                    raise ValueError('Route admission blocked: '+'; '.join(gate['blockers']))
            pins={args.source:item}
            if gate is not None:
                pins.update(gate['pins']);pins[gate['selection_subject']]=gate['selection_pin']
            if args.request:
                # Include the revision request's own pinned dependencies, not only its filename.
                pins.update({k:P['JOURNAL']['pin'](data,k) for k in request['pins']})
                pins[args.request]=request_pin
            payload={key:getattr(args,key) for key in ['tool','output','start','end','context','request','after_start','after_end','observe_resources']}
            if gate is not None:payload['admission']={'subject':gate['selection_subject'],'limits':gate['limits']}
            attempt=STATE['begin'](data,args.step,payload,pins,P,args.retry_of)
            P['save'](project,data) # durable intent before dispatch; a crash keeps outcome unresolved
            if args.tool == 'revision-comparison':
                folder = project.parent / ('executor-comparison-' + uuid.uuid4().hex)
                try:
                    report = R['comparison'](data, project, request_path, args.source, folder,
                                             args.context, args.after_start, args.after_end)
                    if P['file_problems'](data, project.parent):
                        raise ValueError('A retained file changed during comparison')
                    P['retain'](data, project.parent, args.output, folder / 'report.json', False, False)
                    P['JOURNAL']['append'](data, 'output:' + args.output, 'decision', 'proposed',
                                           'framewright', 'administrative_change',
                                           'Comparison prepared; viewing, listening and preservation checks pending',
                                           'executor-revision-comparison', [*report['pins'], report['subject']])
                    P['event'](data, 'executor_run', step=args.step, tool=args.tool, source=args.source,
                               source_pin=item, request=args.request, output=args.output,
                               comparison=report['subject'], result='retained_review_pending')
                    STATE['finish'](data,attempt,'produced',P,output=args.output,output_pin=P['JOURNAL']['pin'](data,'output:'+args.output))
                    P['save'](project, data)
                except (OSError, ValueError, KeyError, TypeError, AttributeError, subprocess.SubprocessError) as exc:
                    # Discard unsaved in-memory registrations on failure, keep any files for inspection.
                    original = P['load'](project)
                    P['event'](original, 'executor_run', step=args.step, tool=args.tool,
                               source=args.source, request=args.request, result='failed', reason=str(exc)[:500])
                    if next(r for r in STATE['attempts'](original) if r['attempt']==attempt)['state']=='unresolved':
                        STATE['finish'](original,attempt,'failed',P,reason=str(exc)[:500])
                    P['save'](project, original)
                    raise ValueError('Comparison failed; failure recorded in project history') from exc
                return {'step': args.step, 'tool': args.tool, 'output': args.output,
                        'file': str(folder / 'report.json'), 'review': str(folder / 'review.md'),
                        'comparison_subject': report['subject'], 'state': 'review_pending',
                        'execution_started': True}
            resources = {'host': RESOURCES['snapshot']([project.parent])} if args.observe_resources else None
            sampler = None
            try:
                with tempfile.TemporaryDirectory(prefix='.executor-', dir=project.parent) as temporary:
                    temp_output = Path(temporary) / 'preview.mp4'
                    seconds = gate['limits']['worker_seconds'] if gate else 180
                    arguments = [str(source)] if args.tool == 'local-media-review' else [
                        str(source), str(temp_output), str(args.start), str(args.end), str(args.context)]
                    command = [sys.executable, str(BASE / 'executor_worker.py'), str(fd),
                               str(seconds), args.tool, *arguments]
                    child = subprocess.Popen(command,
                                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                             start_new_session=True, pass_fds=(fd,))
                    if args.observe_resources:
                        sampler = RESOURCES['OwnedSampler'](child.pid).start()
                    try:
                        stdout, stderr = child.communicate(timeout=gate['limits']['worker_seconds'] if gate else 180)
                    except BaseException:
                        # Termination, Ctrl-C and timeouts must not leave a detached worker.
                        try: os.killpg(child.pid, signal.SIGKILL)
                        except ProcessLookupError: pass
                        child.communicate()
                        raise
                    finally:
                        if sampler: resources['worker'] = sampler.finish()
                    if child.returncode:
                        raise ValueError('Media inspection failed: ' + stderr[-300:])
                    if gate and args.tool=='local-media-review' and len(stdout.encode())>gate['limits']['max_output_bytes']:
                        raise ValueError('Inspection report exceeds selected output limit')
                    if gate and args.tool=='review-clip' and temp_output.stat().st_size>gate['limits']['max_output_bytes']:
                        raise ValueError('Review clip exceeds selected output limit')
                    report = json.loads(stdout)
                    if args.tool == 'local-media-review':
                        P['MEDIA']['validate'](report,item)
                    if P['file_problems'](data, project.parent):
                        raise ValueError('Retained files changed during inspection; result not registered')
                    output = project.parent / ('executor-review-' + uuid.uuid4().hex +
                                               ('.json' if args.tool == 'local-media-review' else '.mp4'))
                    if args.tool == 'local-media-review':
                        with output.open('x', encoding='utf-8') as stream:
                            json.dump(report, stream, ensure_ascii=False, indent=2, allow_nan=False); stream.write('\n')
                    else:
                        with temp_output.open('rb') as source_stream, output.open('xb') as target_stream:
                            try:
                                shutil.copyfileobj(source_stream, target_stream, 1024 * 1024)
                            except OSError:
                                output.unlink(missing_ok=True)
                                raise
                    if P['file_problems'](data, project.parent):
                        output.unlink(missing_ok=True)
                        raise ValueError('Retained files changed while saving; result not registered')
                    if gate and output.stat().st_size>gate['limits']['max_output_bytes']:
                        raise ValueError('Written result exceeds selected output limit; file kept unretained for inspection')
                    if gate:ADMISSION['validate_output'](gate,output,report)
                    P['retain'](data, project.parent, args.output, output, False, False)
                    if args.tool == 'review-clip':
                        P['JOURNAL']['append'](data, 'output:' + args.output, 'decision', 'proposed',
                                               'framewright', 'administrative_change',
                                               'Review proxy created; playback and creative review pending',
                                               'executor-review-clip', [args.source])
                    P['event'](data, 'executor_run', step=args.step, tool=args.tool, source=args.source,
                               source_pin=item, output=args.output, result='retained_review_pending',
                               admission=gate, resources=resources, details=report if args.tool == 'review-clip' else {'scope': 'technical report'})
                    STATE['finish'](data,attempt,'produced',P,output=args.output,output_pin=P['JOURNAL']['pin'](data,'output:'+args.output))
                    P['save'](project, data)
            except (OSError, ValueError, subprocess.SubprocessError) as exc:
                data=P['load'](project) # discard uncommitted in-memory output registrations
                if next(r for r in STATE['attempts'](data) if r['attempt']==attempt)['state']=='unresolved':
                    STATE['finish'](data,attempt,'failed',P,reason=str(exc)[:500])
                P['event'](data, 'executor_run', step=args.step, tool=args.tool,
                           source=args.source, result='failed', resources=resources, reason=str(exc)[:500])
                P['save'](project, data)
                raise ValueError('Inspection failed; failure recorded in project history') from exc
    result = {'step': args.step, 'tool': args.tool, 'output': args.output,
              'file': str(output), 'state': 'review_pending', 'execution_started': True}
    if gate is not None: result['admission'] = gate
    if resources is not None: result['resources'] = resources
    if args.tool == 'review-clip': result.update(report)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path); parser.add_argument('--step', required=True)
    parser.add_argument('--source', required=True); parser.add_argument('--output', required=True)
    parser.add_argument('--tool', choices=['local-media-review', 'review-clip', 'revision-comparison'], default='local-media-review')
    parser.add_argument('--start', type=float); parser.add_argument('--end', type=float)
    parser.add_argument('--context', type=float, default=1.0)
    parser.add_argument('--request', help='Retained output: revision request subject')
    parser.add_argument('--after-start', type=float); parser.add_argument('--after-end', type=float)
    parser.add_argument('--retry-of', help='Explicit retry of last reconciled failed/not-submitted attempt; same request only')
    parser.add_argument('--observe-resources', action='store_true', help='Optional owned-worker sampling; no auto-install or host-fit claim')
    parser.add_argument('--execute', action='store_true', help='Explicitly run this one local inspection')
    args = parser.parse_args()
    def interrupted(signum, _frame):
        raise ValueError('Execution interrupted by signal ' + str(signum))
    for signum in (signal.SIGTERM, signal.SIGHUP, signal.SIGINT):
        signal.signal(signum, interrupted)
    try:
        print(json.dumps(run(args), indent=2))
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(2, str(exc) + '\n')


if __name__ == '__main__': main()
