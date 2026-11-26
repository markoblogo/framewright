"""Reopen a project delivery from its pinned page, assets and recorded reviews."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import runpy
import sys

BASE = Path(__file__).resolve().parent
DELIVERY = runpy.run_path(str(BASE / 'delivery.py'))
digest = DELIVERY['digest']


def local_file(root, relative):
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute() or '..' in Path(relative).parts:
        raise ValueError('Delivery paths must be relative and stay inside their directory')
    file = (root / relative).resolve(strict=True)
    if not file.is_relative_to(root) or not file.is_file():
        raise ValueError('Invalid or escaping delivery file: ' + relative)
    return file


def inspect(project_root, manifest_path):
    manifest = local_file(project_root, manifest_path)
    package = manifest.parent
    if package == project_root:
        raise ValueError('The delivery must have its own subdirectory')
    page = local_file(package, 'review.html')
    receipt_path = local_file(package, 'delivery-receipt.json')
    if page != package / 'review.html' or receipt_path != package / 'delivery-receipt.json':
        raise ValueError('Delivery page and receipt must be regular files in the package')
    receipt = json.loads(receipt_path.read_text())
    data = json.loads(manifest.read_text())
    manifest_sha, page_sha = digest(manifest), digest(page)
    if (data['schema_version'] != 1 or receipt['schema_version'] != 1 or
            receipt['state'] != data['state'] or receipt['manifest_sha256'] != manifest_sha or
            receipt['page_sha256'] != page_sha):
        raise ValueError('Delivery page or manifest differs from the delivery receipt')
    if data['state'] == 'rejected':
        raise ValueError('Rejected delivery package cannot be attached or reopened')

    advertised = Counter((v['platform'], role, path) for v in data['variants'] for role, path in v['files'].items())
    advertised.update(('common', 'extra', x['path']) for x in data.get('extras', []))
    if advertised != Counter((row['platform'], row['role'], row['path']) for row in receipt['files']):
        raise ValueError('Delivery manifest and receipt list different files')
    files = []
    for row in receipt['files']:
        asset = local_file(package, row['path'])
        if asset.stat().st_size != row['bytes'] or digest(asset) != row['sha256']:
            raise ValueError('Delivery file changed: ' + row['path'])
        files.append({**{key: row[key] for key in ('platform', 'role', 'bytes', 'sha256')}, 'path': str(asset)})

    # Browser QA may update the receipt without changing delivery content.
    pinned_files = sorted((row['platform'], row['role'], row['path'], row['bytes'], row['sha256'])
                          for row in receipt['files'])
    files_sha = hashlib.sha256(json.dumps(pinned_files).encode()).hexdigest()
    copy = [v['platform'] for v in data['variants'] if v.get('publication') or 'copy' in v['files']]
    return {'manifest_sha256': manifest_sha, 'page_sha256': page_sha, 'files_sha256': files_sha, 'title': data['title'],
            'revision': data['revision'], 'package_state': data['state'], 'page': str(page),
            'files': files, 'publication_copy': copy}


def check_masters(data, status, subjects, files):
    if not subjects or len(set(subjects)) != len(subjects):
        raise ValueError('Select each retained video output once')
    masters = Counter()
    for subject in subjects:
        pin = data['artifacts'][subject]['file']
        if pin is None or 'output:' + subject in status['file_problems']:
            raise ValueError('Selected master is missing or changed: ' + subject)
        for kind, expected in [('technical', 'pass'), ('creative', 'accepted')]:
            reviews = [r['result'] for r in status['observations']['effective']
                       if r['subject'] == 'output:' + subject and r['kind'] == kind]
            if not reviews or any(result != expected for result in reviews):
                raise ValueError(f'Current {kind} review required for {subject}')
        masters[pin['bytes'], pin['sha256']] += 1
    if masters != Counter((f['bytes'], f['sha256']) for f in files if f['role'] == 'video'):
        raise ValueError('Package videos are not the explicitly selected master revisions')


def attach(data, status, checkpoint, identity, manifest, subjects, replace):
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', identity):
        raise ValueError('Delivery ID must use lowercase letters, numbers or hyphens')
    root = checkpoint.parent
    relative = manifest.resolve(strict=True).relative_to(root).as_posix()
    package = inspect(root, relative)
    check_masters(data, status, subjects, package['files'])
    binding = {'manifest': relative, 'subjects': sorted(subjects),
               **{key: package[key] for key in ('manifest_sha256', 'page_sha256', 'files_sha256')}}
    deliveries = data.setdefault('review_deliveries', {})
    before = deliveries.get(identity)
    if before == binding:
        return False
    if before and not replace:
        raise ValueError('Existing delivery differs; inspect it and use --replace explicitly')
    deliveries[identity] = binding
    return True


def current(data, status, checkpoint, identity):
    binding = data.get('review_deliveries', {})[identity]
    project_root = checkpoint.parent
    info = inspect(project_root, binding['manifest'])
    if any(info[key] != binding[key] for key in ('manifest_sha256', 'page_sha256', 'files_sha256')):
        raise ValueError('Delivery revision changed; attach the intended package explicitly')
    check_masters(data, status, binding['subjects'], info['files'])
    return info


def views(data, status, checkpoint):
    entries = []
    for identity, binding in data.get('review_deliveries', {}).items():
        entry = {'id': identity, 'subjects': binding['subjects']}
        try:
            info = current(data, status, checkpoint, identity)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            entry.update(state='needs_review', reason=str(exc))
        else:
            entry.update(info, state='available',
                         open_command=[sys.executable, str(BASE / 'project.py'), 'open-delivery', str(checkpoint), identity])
        entries.append(entry)
    return entries
