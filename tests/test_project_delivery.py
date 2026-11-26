"""A fresh process reopens the explicitly retained, approved delivery."""
import hashlib
import json
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import unittest
import urllib.request

CLI = Path(__file__).resolve().parents[1] / 'skills/video-production-router/scripts/project.py'


class ProjectDeliveryTest(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.root = Path(scratch.name).resolve()
        self.project = self.root / 'project.json'
        self.folder = self.root / 'publication'
        self.folder.mkdir()
        self.manifest = self.folder / 'delivery.json'
        self.video = self.folder / 'film.mp4'
        self.video.write_bytes(b'synthetic video bytes')
        self.captions = self.folder / 'film.srt'
        self.captions.write_text('Example caption')
        self.page = self.folder / 'review.html'
        self.page.write_text('<h1>Fixture delivery</h1>')
        self.manifest.write_text(json.dumps({
            'schema_version': 1, 'state': 'final', 'title': 'Fixture', 'revision': 'v2',
            'variants': [{'platform': 'youtube', 'files': {'video': self.video.name, 'subtitles': self.captions.name},
                          'publication': {'description': 'Example description'}}],
            'note': 'Fixture package',
        }))
        self.receipt = self.folder / 'delivery-receipt.json'
        self.receipt.write_text(json.dumps({
            'schema_version': 1, 'state': 'final',
            'manifest_sha256': self.hash(self.manifest), 'page_sha256': self.hash(self.page),
            'files': [{'platform': 'youtube', 'role': role, 'path': file.name,
                       'bytes': file.stat().st_size, 'sha256': self.hash(file)}
                      for role, file in [('video', self.video), ('subtitles', self.captions)]],
        }))
        self.cli('create', self.project, '--goal', 'Fixture', '--note', 'Delivery recovery')
        self.cli('asset', self.project, 'master', '--kind', 'video')
        self.cli('retain', self.project, 'master', self.video)
        self.cli('task', self.project, 'field-test', '--label', 'Field test', '--waiting-for', 'owner', '--note', 'Outdoor feedback')

    @staticmethod
    def hash(file):
        return hashlib.sha256(file.read_bytes()).hexdigest()

    def cli(self, *args, ok=True):
        result = subprocess.run([sys.executable, str(CLI), *map(str, args)],
                                cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode == 0, ok, result.stderr)
        return result

    def approve(self):
        for kind, result in [('technical', 'pass'), ('creative', 'accepted')]:
            self.cli('observe', self.project, 'output:master', '--kind', kind,
                     '--result', result, '--actor', 'owner', '--provenance', 'owner_report', '--note', 'Fixture evidence')

    def attach(self, ok=True):
        return self.cli('attach-delivery', self.project, 'episode', self.manifest, '--video', 'master', ok=ok)

    def brief(self):
        return json.loads(self.cli('brief', self.project, '--json').stdout)

    def test_fresh_session_recovery_preserves_owner_wait(self):
        self.assertEqual(self.brief()['review_deliveries'], [])
        self.approve()
        self.attach()
        before = self.project.read_bytes()
        brief = self.brief()
        package, = brief['review_deliveries']
        self.assertEqual(package['state'], 'available')
        self.assertEqual(package['revision'], 'v2')
        self.assertEqual(package['publication_copy'], ['youtube'])
        self.assertEqual(package['page'], str(self.page))
        self.assertEqual({a['role'] for a in package['files']}, {'video', 'subtitles'})
        self.assertEqual(brief['proposed_next']['kind'], 'waiting')
        self.assertEqual(brief['waiting'][0]['task'], 'field-test')
        self.assertEqual(self.project.read_bytes(), before)
        with socket.socket() as candidate:
            candidate.bind(('127.0.0.1', 0))
            port = candidate.getsockname()[1]
        launch = [*package['open_command'], '--port', str(port)]
        with subprocess.Popen(launch, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd='/') as server:
            try:
                self.assertIn(str(port), server.stdout.readline())
                request = urllib.request.Request(f'http://127.0.0.1:{port}/film.mp4', headers={'Range': 'bytes=2-6'})
                with urllib.request.urlopen(request, timeout=3) as response:
                    self.assertEqual(response.status, 206)
                    self.assertEqual(response.read(), self.video.read_bytes()[2:7])
            finally:
                server.terminate()
                server.wait(timeout=3)
        self.assertEqual(self.project.read_bytes(), before)

    def test_unapproved_or_changed_package_cannot_open(self):
        self.attach(ok=False)
        self.approve()
        self.attach()
        receipt = json.loads(self.receipt.read_text())
        receipt['browser_check'] = {'state': 'passed'}
        self.receipt.write_text(json.dumps(receipt))
        self.assertEqual(self.brief()['review_deliveries'][0]['state'], 'available')
        self.captions.write_text('Changed after review')
        receipt['files'][1].update(bytes=self.captions.stat().st_size, sha256=self.hash(self.captions))
        self.receipt.write_text(json.dumps(receipt))
        entry = self.brief()['review_deliveries'][0]
        self.assertEqual(entry['state'], 'needs_review')
        self.assertNotIn('open_command', entry)
        self.cli('open-delivery', self.project, 'episode', ok=False)

    def set_package_state(self, state):
        manifest = json.loads(self.manifest.read_text())
        manifest['state'] = state
        self.manifest.write_text(json.dumps(manifest))
        receipt = json.loads(self.receipt.read_text())
        receipt.update(state=state, manifest_sha256=self.hash(self.manifest))
        self.receipt.write_text(json.dumps(receipt))

    def test_rejected_package_cannot_be_attached(self):
        self.approve()
        self.set_package_state('rejected')
        self.attach(ok=False)

    def test_legacy_rejected_package_binding_cannot_reopen(self):
        self.approve()
        self.attach()
        self.set_package_state('rejected')
        # Older clients could explicitly attach this rejected manifest. Model
        # their consistent binding so only the state guard prevents reopening.
        data = json.loads(self.project.read_text())
        data['review_deliveries']['episode']['manifest_sha256'] = self.hash(self.manifest)
        self.project.write_text(json.dumps(data))
        entry, = self.brief()['review_deliveries']
        self.assertEqual(entry['state'], 'needs_review')
        self.assertNotIn('open_command', entry)
        self.cli('open-delivery', self.project, 'episode', ok=False)

    def test_review_package_with_approved_master_remains_available(self):
        self.approve()
        self.set_package_state('review')
        self.attach()
        self.assertEqual(self.brief()['review_deliveries'][0]['state'], 'available')

    def test_rejected_master_cannot_reopen_previous_delivery(self):
        self.approve()
        self.attach()
        self.cli('observe', self.project, 'output:master', '--kind', 'creative', '--result', 'rejected',
                 '--actor', 'owner', '--provenance', 'owner_report', '--note', 'Revision required')
        self.assertEqual(self.brief()['review_deliveries'][0]['state'], 'needs_review')
        self.cli('open-delivery', self.project, 'episode', ok=False)
