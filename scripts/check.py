#!/usr/bin/env python3
"""One offline check entry point; model work is separately budgeted, never automatic."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
MODEL_POLICY = {
    'docs': 'No model calls for prose, links or research-only additions.',
    'capture': 'At most eight affected cases once after deterministic capture tests; no full routing benchmark.',
    'router': 'Freeze affected boundary cases before calls; default ceiling eight. A broad qualification run needs its own declared scope.',
    'grader': 'Use frozen controls and unchanged-answer replay. No actor rerun unless actor source or requests also changed.',
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scope', choices=MODEL_POLICY, default='docs')
    parser.add_argument('--plan', action='store_true', help='Print checks and the model policy without running anything')
    args = parser.parse_args()
    checks = [
        ['-m', 'unittest', 'discover', '-s', 'tests', '-q'],
        ['scripts/check_router_evaluation.py', '--root', 'benchmarks/router', '--qualification', 'router-qualification.json'],
        ['scripts/check_router_evaluation.py', '--root', 'benchmarks/storyboard'],
        ['scripts/validate.py'], ['scripts/render_tool_reference.py', '--check'],
    ]
    print(json.dumps({'scope': args.scope, 'automatic_model_calls': 0,
                      'model_policy': MODEL_POLICY[args.scope], 'offline_checks': checks + [['scripts/build_release.py', '--output', '<temporary directory>']]}, indent=2), flush=True)
    if args.plan:
        return
    for command in checks:
        subprocess.run([sys.executable] + command, cwd=ROOT, check=True)
    # Package smoke only: no tag, upload or release, and no persistent repository output.
    with tempfile.TemporaryDirectory(prefix='framewright-package-check-') as output:
        subprocess.run([sys.executable, 'scripts/build_release.py', '--output', output], cwd=ROOT, check=True)


if __name__ == '__main__':
    main()
