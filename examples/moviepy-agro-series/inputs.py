"""Verify archived auxiliary input pins before any media decoder opens them."""
import hashlib
import json
from pathlib import Path


def verified_input(identity, root, manifest=None):
    pins = Path(manifest) if manifest else Path(__file__).with_name('auxiliary-inputs.json')
    row = json.loads(pins.read_text())[identity]
    source = Path(root) / row['local_output']
    if not source.is_file():
        raise ValueError(f'Missing source: {identity}')
    if hashlib.sha256(source.read_bytes()).hexdigest() != row['sha256']:
        raise ValueError(f'Changed source: {identity}')
    return source
