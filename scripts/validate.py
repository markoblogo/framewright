#!/usr/bin/env python3
"""Validate retained records; never launches a model, renderer or network call."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import os
import struct


def validate_artifact(artifact, local_root=None):
    assert isinstance(artifact, dict), 'Artifact must be an object'
    assert re.fullmatch(r'[0-9a-f]{64}', artifact['sha256'])
    assert type(artifact['bytes']) is int and artifact['bytes'] > 0
    output = Path(artifact['local_output'])
    assert artifact['local_output'] and not output.is_absolute() and '..' not in output.parts
    if local_root:
        media = local_root / output
        assert media.resolve().is_relative_to(local_root.resolve()), f'Artifact outside local root: {media}'
        assert media.stat().st_size == artifact['bytes'], f'Size drift: {media}'
        with media.open('rb') as stream:
            digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        assert digest == artifact['sha256'], f'Hash drift: {media}'


def markdown_files(root):
    for directory, folders, files in os.walk(root):
        folders[:] = [f for f in folders if f not in {'.git', 'node_modules', '.venv', '__pycache__'}]
        for name in files:
            if name.endswith('.md'):
                yield Path(directory) / name


def validate(root, local_root=None):
    refs = root / 'skills/video-production-router/references'
    catalog = json.loads((refs / 'catalog.json').read_text())
    outputs = json.loads((root / 'experiments/2026-10-14/outputs.json').read_text())
    scenarios = json.loads((refs / 'scenarios.json').read_text())
    assert catalog['schema_version'] == 1
    assert catalog['router_validation'] == 'structural_only', 'Model evidence required before promotion'
    assert scenarios['validation'] == 'structural_only'
    methods = {m['id']: m for m in catalog['methods']}
    records = {r['id']: r for r in outputs}
    assert len(methods) == len(catalog['methods']), 'Duplicate method'
    assert len(records) == len(outputs), 'Duplicate experiment'
    assert len({c['id'] for c in scenarios['cases']}) == len(scenarios['cases'])
    for method in methods.values():
        assert method['status'] in ('candidate', 'prototype', 'tested_for_scope')
        assert method['tested_scope'] and method['not_tested']
        assert (refs / method['recipe'].split('#')[0]).is_file()
        if method['status'] == 'tested_for_scope':
            assert method['experiments'], 'Tested scope needs an experiment'
        for cid in method['experiments']:
            assert records[cid]['route'] == method['id'], 'Mismatched evidence route'
    for record in records.values():
        assert record['route'] in methods
        validate_artifact(record, local_root)
        if 'native_export' in record:
            validate_artifact(record['native_export'], local_root)
        if 'thumbnail' in record:
            thumbnail = record['thumbnail']
            validate_artifact(thumbnail, local_root)
            assert thumbnail['format'] == 'png', 'Only PNG thumbnail dimensions are supported'
            assert all(type(thumbnail[k]) is int and thumbnail[k] > 0 for k in ('width', 'height'))
            if local_root:
                image = local_root / thumbnail['local_output']
                with image.open('rb') as stream:
                    header = stream.read(24)
                assert len(header) == 24 and header[:8] == b'\x89PNG\r\n\x1a\n' and header[12:16] == b'IHDR', 'Invalid PNG header'
                assert struct.unpack('>II', header[16:24]) == (thumbnail['width'], thumbnail['height']), f'Dimension drift: {image}'
        evidence = root / record['evidence']
        assert evidence.resolve().is_relative_to(root.resolve())
        assert evidence.is_file()
        text = evidence.read_text()
        assert '/Users/' not in text and '/Volumes/' not in text
        if record['qa_scope'] == 'encoded audio':
            assert 'PASSED: 0 failed, 0 warnings' in text, record['id']
        if record['id'] == 'anatomy-prototype':
            assert 'FAILED' in text and '22 audibility failures' in text
    for case in scenarios['cases']:
        assert case['request'] and case['required'] and case['forbidden']
        assert case['expected_method'] is None or case['expected_method'] in methods
    # Check local Markdown destinations, including heading fragments.
    for doc in markdown_files(root):
        for target in re.findall(r'\]\(([^)]+)\)', doc.read_text()):
            if '://' in target:
                continue
            path, _, anchor = target.partition('#')
            destination = doc.parent / path if path else doc
            assert destination.is_file(), f'Broken link: {doc}: {target}'
            if anchor:
                headings = re.findall(r'^#+ (.+)$', destination.read_text(), re.M)
                slugs = {re.sub(r'[^\w -]', '', h.lower()).replace(' ', '-') for h in headings}
                assert anchor in slugs, f'Broken heading: {doc}: {target}'
    print(f'PASS: {len(methods)} methods, {len(records)} outputs, {len(scenarios["cases"])} scenario specifications; local links intact.')
    print('Router evaluation: structural_only; no model or video experiment was run.')
    if local_root:
        print('All recorded local artifacts match sizes and SHA-256 (finals, native exports and thumbnails); recorded PNG dimensions match.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--local-root', type=Path, help='Optional local media base (e.g. /Volumes/Work)')
    args = parser.parse_args()
    validate(Path(__file__).resolve().parents[1], args.local_root)
