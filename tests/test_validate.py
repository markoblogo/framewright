import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('validator', Path(__file__).resolve().parents[1] / 'scripts/validate.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class NativeExportValidationTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        refs = self.root / 'skills/video-production-router/references'
        refs.mkdir(parents=True)
        self.outputs = self.root / 'experiments/2026-10-14/outputs.json'
        self.outputs.parent.mkdir(parents=True)
        (self.root / 'evidence.txt').write_text('Fixture evidence')
        (refs / 'recipes.md').write_text('# Fixture')
        (refs / 'catalog.json').write_text(json.dumps({'schema_version': 1, 'router_validation': 'structural_only', 'methods': [{'id': 'fixture', 'status': 'tested_for_scope', 'tested_scope': 'fixture', 'not_tested': ['other inputs'], 'recipe': 'recipes.md', 'experiments': ['fixture']}]}))
        (refs / 'scenarios.json').write_text(json.dumps({'validation': 'structural_only', 'cases': []}))
        self.record = {'id': 'fixture', 'route': 'fixture', 'evidence': 'evidence.txt', 'qa_scope': 'fixture'}
        for key, name, data in [(None, 'final.mp4', b'final'), ('native_export', 'native.mp4', b'native')]:
            (self.root / name).write_bytes(data)
            artifact = {'local_output': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
            if key:
                self.record[key] = artifact
            else:
                self.record.update(artifact)
        self.save()

    def save(self):
        self.outputs.write_text(json.dumps([self.record]))

    def check(self, local=True):
        with contextlib.redirect_stdout(io.StringIO()):
            validator.validate(self.root, self.root if local else None)

    def test_valid_native_export_passes(self):
        self.check()

    def test_missing_native_export_rejected(self):
        (self.root / 'native.mp4').unlink()
        with self.assertRaises(FileNotFoundError):
            self.check()

    def test_native_size_drift_rejected(self):
        (self.root / 'native.mp4').write_bytes(b'short')
        with self.assertRaisesRegex(AssertionError, 'Size drift'):
            self.check()

    def test_same_size_native_corruption_rejected(self):
        (self.root / 'native.mp4').write_bytes(b'broken')
        with self.assertRaisesRegex(AssertionError, 'Hash drift'):
            self.check()

    def test_final_export_corruption_still_rejected(self):
        (self.root / 'final.mp4').write_bytes(b'wrong')
        with self.assertRaisesRegex(AssertionError, 'Hash drift'):
            self.check()

    def test_native_metadata_rejected_without_local_files(self):
        for field, value in [('sha256', 'invalid'), ('bytes', 0), ('local_output', '../escape.mp4')]:
            with self.subTest(field=field):
                original = self.record['native_export'][field]
                self.record['native_export'][field] = value
                self.save()
                with self.assertRaises(AssertionError):
                    self.check(local=False)
                self.record['native_export'][field] = original


if __name__ == '__main__':
    unittest.main()
