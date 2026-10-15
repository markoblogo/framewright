#!/usr/bin/env python3
"""Normalize exact cinematography terms; never infer tool capability or execute."""
import argparse
import json
from pathlib import Path
import re
import unicodedata


def key(text):
    text = unicodedata.normalize('NFKC', text).casefold().replace('ё', 'е')
    return re.sub(r'[\s_\-–—]+', ' ', text).strip()


def aliases():
    data = json.loads((Path(__file__).resolve().parents[1] / 'references/video-terms.json').read_text())
    result = {}
    for term in data['terms']:
        for name in [term['id'], term['ru'], term['en'], *term['aliases']]:
            normalized = key(name)
            if normalized in result and result[normalized] != term['id']:
                raise ValueError('Conflicting technique alias: ' + name)
            result[normalized] = term['id']
    return result


def normalize_effects(effects):
    if not isinstance(effects, list) or any(not isinstance(x, str) or not x.strip() for x in effects):
        raise ValueError('effects must be nonempty strings in a list')
    mapping = aliases()
    return list(dict.fromkeys(mapping.get(key(x), x) for x in effects))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('terms', nargs='+')
    print(json.dumps(normalize_effects(parser.parse_args().terms), ensure_ascii=False))
