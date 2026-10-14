#!/usr/bin/env python3
"""Generate the readable inventory from the same registry used by the planner."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFS = ROOT / 'skills/video-production-router/references'


def render(data):
    lines = ['# Tool capability matrix', '', 'Generated from `tools.json`; reviewed ' + data['reviewed'] + '.', '',
             'Scope: decision-relevant inventory, not an exhaustive API guarantee. Tested means',
             'the stated local experiment only. Documented needs installed-version verification;',
             'failed is a retained limitation; unknown is not a usable promise. Styles are',
             'affordances and preferences, not renderer boundaries or comparative quality scores.', '']
    for tool in data['tools']:
        lines += ['## ' + tool['name'], '', '**Role:** ' + tool['role'] + '. **Inputs:** ' + ', '.join(tool['inputs']) + '.', '',
                  '**Style directions:** ' + ', '.join(tool['styles']) + '.', tool['style_note'], '',
                  '**Tested version/scope:** ' + tool['tested_version'], '', '**Licence:** ' + tool['licence_note'], '',
                  '| Feature | Evidence | Scope / source |', '| --- | --- | --- |']
        for feature in tool['features']:
            url = data['sources'][feature['source']]['url']
            note = (feature['note'] or ('Observed scope: ' + ', '.join(feature['experiments']) if feature['experiments'] else 'Upstream claim; not locally qualified')).replace('|', '\\|').replace('\n', ' ')
            lines.append(f'| `{feature["id"]}` | {feature["status"]} | {note} [Source]({url}) |')
        lines += ['', '**Limits:** ' + ' '.join(tool['limitations']), '']
    lines += ['## Source freshness', '', 'Immutable repository README links retain the reviewed revision. Live documentation',
              'links describe upstream capability on the review date, not a test of the pilot',
              'runtime. Refresh the registry before depending on a changed external contract.', '']
    return '\n'.join(lines)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    expected = render(json.loads((REFS / 'tools.json').read_text()))
    target = REFS / 'tool-matrix.md'
    if args.check:
        if not target.is_file() or target.read_text() != expected:
            parser.exit(1, 'Tool matrix drift: run scripts/render_tool_reference.py\n')
        print('PASS: tool matrix matches registry')
    else:
        target.write_text(expected)
