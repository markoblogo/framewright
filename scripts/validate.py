#!/usr/bin/env python3
"""Validate retained records; never launches a model, renderer or network call."""
import argparse
import hashlib
import json
from pathlib import Path
import re


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
        assert re.fullmatch(r'[0-9a-f]{64}', record['sha256'])
        assert record['bytes'] > 0
        evidence = root / record['evidence']
        assert evidence.resolve().is_relative_to(root.resolve())
        assert evidence.is_file()
        text = evidence.read_text()
        assert '/Users/' not in text and '/Volumes/' not in text
        if record['qa_scope'] == 'encoded audio':
            assert 'PASSED: 0 failed, 0 warnings' in text, record['id']
        if record['id'] == 'anatomy-prototype':
            assert 'FAILED' in text and '22 audibility failures' in text
        if local_root:
            media = local_root / record['local_output']
            assert media.stat().st_size == record['bytes'], f'Size drift: {media}'
            assert hashlib.file_digest(media.open('rb'), 'sha256').hexdigest() == record['sha256'], f'Hash drift: {media}'
    for case in scenarios['cases']:
        assert case['request'] and case['required'] and case['forbidden']
        assert case['expected_method'] is None or case['expected_method'] in methods
    # Check local Markdown destinations, including heading fragments.
    for doc in root.rglob('*.md'):
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
        print('All retained local video sizes and SHA-256 hashes match.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--local-root', type=Path, help='Optional local media base (e.g. /Volumes/Work)')
    args = parser.parse_args()
    validate(Path(__file__).resolve().parents[1], args.local_root)
