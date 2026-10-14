#!/usr/bin/env python3
"""Package only this project's router; smoke-test it outside the checkout."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def build(root, output):
    version = (root / 'VERSION').read_text().strip()
    output = output.resolve()
    if output.is_relative_to(root.resolve()):
        raise ValueError('Release output must be outside the checkout')
    output.mkdir(parents=True, exist_ok=True)
    skill = root / 'skills/video-production-router'
    files = [skill / 'SKILL.md']
    for folder, suffixes in [('references', {'.json', '.md'}), ('scripts', {'.py'})]:
        files.extend(p for p in (skill / folder).iterdir() if p.is_file() and p.suffix in suffixes)
    if any(p.is_symlink() for p in files):
        raise ValueError('Do not package symlinked source')
    archive = output / f'framewright-router-{version}.zip'
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for p in sorted(files):
            z.write(p, 'video-production-router/' + p.relative_to(skill).as_posix())
        z.write(root / 'LICENSE', 'video-production-router/LICENSE')
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (output / 'SHA256SUMS').write_text(f'{digest}  {archive.name}\n')
    # The installed skill must work without the repository or its private media.
    with tempfile.TemporaryDirectory() as directory:
        target = Path(directory)
        with zipfile.ZipFile(archive) as z:
            z.extractall(target)
        brief = target / 'brief.json'
        brief.write_text(json.dumps({'blocks': [{'id': 'ui', 'input': 'react-ui', 'deliverables': ['video-export', 'still-export']}]}))
        run = subprocess.run([sys.executable, str(target / 'video-production-router/scripts/plan.py'), str(brief)], check=True, capture_output=True, text=True)
        plan = json.loads(run.stdout)
        if plan['blocks'][0]['tools'] != ['flute', 'ffmpeg'] or plan['execution'] != 'not_started':
            raise ValueError('Standalone routing smoke check failed')
    print(f'PASS: standalone package {archive.name}; SHA-256 {digest}')
    return archive


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    build(ROOT, args.output)
