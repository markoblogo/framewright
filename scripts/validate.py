"""Validate retained records; never launches a model, renderer or network call."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import os
import struct


class ValidationError(ValueError):
    """Invalid retained data; remains active under python -O."""


def require(condition, message):
    if not condition:
        raise ValidationError(message)


def check_schema(value, rule, schema, path):
    """Evaluate this repository's deliberately small JSON Schema keyword subset.

    Fail closed on new assertion keywords; this is not a general JSON Schema engine.
    """
    known = {'$schema', '$defs', '$ref', 'title', 'description', 'type', 'required',
             'properties', 'items', 'minItems', 'minLength', 'minimum', 'pattern', 'const'}
    require(not set(rule) - known, f'{path}: unsupported schema keywords {set(rule) - known}')
    if '$ref' in rule:
        ref = rule['$ref']
        require(ref.startswith('#/$defs/'), f'{path}: only local definition references supported')
        check_schema(value, schema['$defs'][ref.split('/')[-1]], schema, path)
    if 'type' in rule:
        checks = {'object': lambda x: isinstance(x, dict), 'array': lambda x: isinstance(x, list),
                  'string': lambda x: isinstance(x, str), 'integer': lambda x: type(x) is int}
        require(rule['type'] in checks, f'{path}: unsupported schema type')
        require(checks[rule['type']](value), f'{path}: expected {rule["type"]}')
    if 'const' in rule:
        require(value == rule['const'], f'{path}: expected {rule["const"]!r}')
    if isinstance(value, dict):
        for key in rule.get('required', []):
            require(key in value, f'{path}: missing {key}')
        for key, child in rule.get('properties', {}).items():
            if key in value:
                check_schema(value[key], child, schema, f'{path}.{key}')
    if isinstance(value, list):
        require(len(value) >= rule.get('minItems', 0), f'{path}: too few items')
        if 'items' in rule:
            for i, child in enumerate(value):
                check_schema(child, rule['items'], schema, f'{path}[{i}]')
    if isinstance(value, str):
        require(len(value) >= rule.get('minLength', 0), f'{path}: empty string')
        if 'pattern' in rule:
            require(re.fullmatch(rule['pattern'], value), f'{path}: invalid format')
    if 'minimum' in rule:
        require(value >= rule['minimum'], f'{path}: below minimum {rule["minimum"]}')


def validate_artifact(artifact, local_root=None):
    require(isinstance(artifact, dict), 'Artifact must be an object')
    require(re.fullmatch('[0-9a-f]{64}', artifact['sha256']), 'Artifact SHA-256 must be 64 lowercase hex characters')
    require(type(artifact['bytes']) is int and artifact['bytes'] > 0, 'Artifact bytes must be a positive integer')
    output = Path(artifact['local_output'])
    require(artifact['local_output'] and (not output.is_absolute()) and ('..' not in output.parts), 'Artifact path must be nonempty, relative and contain no parent traversal')
    if local_root:
        media = local_root / output
        require(media.resolve().is_relative_to(local_root.resolve()), f'Artifact outside local root: {media}')
        require(media.is_file(), f'Missing artifact: {media}')
        require(media.stat().st_size == artifact['bytes'], f'Size drift: {media}')
        with media.open('rb') as stream:
            digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        require(digest == artifact['sha256'], f'Hash drift: {media}')

def markdown_files(root):
    for directory, folders, files in os.walk(root):
        folders[:] = [f for f in folders if f not in {'.git', 'node_modules', '.venv', '__pycache__'}]
        for name in files:
            if name.endswith('.md'):
                yield (Path(directory) / name)

def validate(root, local_root=None):
    refs = root / 'skills/video-production-router/references'
    catalog = json.loads((refs / 'catalog.json').read_text())
    schema = json.loads((root / 'schemas/outputs.schema.json').read_text())
    output_files = sorted((root / 'experiments').glob('*/outputs.json'))
    require(output_files, 'No experiment outputs.json found')
    outputs = []
    for path in output_files:
        batch = json.loads(path.read_text())
        check_schema(batch, schema, schema, str(path.relative_to(root)))
        outputs.extend(batch)
    scenarios = json.loads((refs / 'scenarios.json').read_text())
    require(catalog['schema_version'] == 1, 'Unsupported catalogue version')
    require(catalog['router_validation'] == 'structural_only', 'Model evidence required before promotion')
    require(scenarios['validation'] == 'structural_only', 'Scenario promotion requires independent model evidence')
    methods = {m['id']: m for m in catalog['methods']}
    records = {r['id']: r for r in outputs}
    require(len(methods) == len(catalog['methods']), 'Duplicate method')
    require(len(records) == len(outputs), 'Duplicate experiment')
    require(len({c['id'] for c in scenarios['cases']}) == len(scenarios['cases']), 'Duplicate scenario ID')
    for method in methods.values():
        require(method['status'] in ('candidate', 'prototype', 'tested_for_scope'), f'Unknown method status: {method["id"]}')
        require(method['tested_scope'] and method['not_tested'], f'Method needs scope and limits: {method["id"]}')
        require((refs / method['recipe'].split('#')[0]).is_file(), f'Missing recipe for {method["id"]}')
        if method['status'] == 'tested_for_scope':
            require(method['experiments'], 'Tested scope needs an experiment')
        for cid in method['experiments']:
            require(cid in records, f'Unknown experiment: {cid}')
            require(records[cid]['route'] == method['id'], 'Mismatched evidence route')
    for record in records.values():
        require(record['route'] in methods, f'Unknown route for {record["id"]}')
        validate_artifact(record, local_root)
        if 'native_export' in record:
            validate_artifact(record['native_export'], local_root)
        if 'thumbnail' in record:
            thumbnail = record['thumbnail']
            validate_artifact(thumbnail, local_root)
            require(thumbnail['format'] == 'png', 'Only PNG thumbnail dimensions are supported')
            require(all((type(thumbnail[k]) is int and thumbnail[k] > 0 for k in ('width', 'height'))), 'Thumbnail dimensions must be positive integers')
            if local_root:
                image = local_root / thumbnail['local_output']
                with image.open('rb') as stream:
                    header = stream.read(24)
                require(len(header) == 24 and header[:8] == b'\x89PNG\r\n\x1a\n' and (header[12:16] == b'IHDR'), 'Invalid PNG header')
                require(struct.unpack('>II', header[16:24]) == (thumbnail['width'], thumbnail['height']), f'Dimension drift: {image}')
        evidence = root / record['evidence']
        require(evidence.resolve().is_relative_to(root.resolve()), f'Evidence outside repository: {record["id"]}')
        require(evidence.is_file(), f'Missing evidence: {record["evidence"]}')
        text = evidence.read_text()
        require('/Users/' not in text and '/Volumes/' not in text, f'Machine-local path in public evidence: {record["id"]}')
        for marker in record.get('evidence_checks', []):
            require(marker in text, f'Missing evidence marker for {record["id"]}: {marker}')
    profile_path = refs / 'tools.json'
    if profile_path.is_file():
        registry = json.loads(profile_path.read_text())
        require(registry['schema_version'] == 1, 'Unsupported tool registry version')
        tools = registry['tools']
        require(len({t['id'] for t in tools}) == len(tools), 'Duplicate tool ID')
        for tool in tools:
            require(isinstance(tool['inputs'], list) and tool['tested_version'] and tool['licence_note'], f'Incomplete tool: {tool["id"]}')
            features = tool['features']
            require(len({f['id'] for f in features}) == len(features), f'Duplicate feature: {tool["id"]}')
            for feature in features:
                require(feature['status'] in {'tested', 'documented', 'failed', 'unknown'}, 'Unknown feature evidence state')
                require(feature['source'] in registry['sources'], 'Missing feature source')
                if feature['status'] == 'tested':
                    require(feature['experiments'], f'Tested feature lacks experiments: {tool["id"]}/{feature["id"]}')
                require(all(e in records for e in feature['experiments']), f'Unknown experiment in {tool["id"]}/{feature["id"]}')
        for source in registry['sources'].values():
            require(source['url'].startswith('https://') and re.fullmatch(r'\d{4}-\d{2}-\d{2}', source['reviewed']), 'Invalid upstream source')
    for case in scenarios['cases']:
        require(case['request'] and case['required'] and case['forbidden'], f'Incomplete scenario: {case["id"]}')
        require(case['expected_method'] is None or case['expected_method'] in methods, f'Unknown scenario route: {case["id"]}')
    for doc in markdown_files(root):
        for target in re.findall('\\]\\(([^)]+)\\)', doc.read_text()):
            if '://' in target:
                continue
            path, _, anchor = target.partition('#')
            destination = doc.parent / path if path else doc
            require(destination.is_file(), f'Broken link: {doc}: {target}')
            if anchor:
                headings = re.findall('^#+ (.+)$', destination.read_text(), re.M)
                slugs = {re.sub('[^\\w -]', '', h.lower()).replace(' ', '-') for h in headings}
                require(anchor in slugs, f'Broken heading: {doc}: {target}')
    print(f"PASS: {len(methods)} methods, {len(records)} outputs, {len(scenarios['cases'])} scenario specifications; local links intact.")
    print('Catalogue qualification: structural_only; this integrity check runs no model or renderer.')
    if local_root:
        print('All recorded local artifacts match sizes and SHA-256 (finals, native exports and thumbnails); recorded PNG dimensions match.')
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--local-root', type=Path, help='Optional local media base (e.g. /Volumes/Work)')
    args = parser.parse_args()
    try:
        validate(Path(__file__).resolve().parents[1], args.local_root)
    except (ValidationError, OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f'INVALID: {exc}\n')
