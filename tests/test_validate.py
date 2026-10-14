import base64
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import shutil
import subprocess
import sys
import unittest

spec = importlib.util.spec_from_file_location('validator', Path(__file__).resolve().parents[1] / 'scripts/validate.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class ArtifactValidationTest(unittest.TestCase):
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
        (self.root / 'schemas').mkdir()
        shutil.copy2(Path(__file__).resolve().parents[1] / 'schemas/outputs.schema.json', self.root / 'schemas/outputs.schema.json')
        self.record = {'id': 'fixture', 'route': 'fixture', 'evidence': 'evidence.txt', 'qa_scope': 'fixture'}
        for key, name, data in [(None, 'final.mp4', b'final'), ('native_export', 'native.mp4', b'native')]:
            (self.root / name).write_bytes(data)
            artifact = {'local_output': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
            if key:
                self.record[key] = artifact
            else:
                self.record.update(artifact)
        png = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aZ1sAAAAASUVORK5CYII=')
        (self.root / 'thumbnail.png').write_bytes(png)
        self.record['thumbnail'] = {'local_output': 'thumbnail.png', 'bytes': len(png), 'sha256': hashlib.sha256(png).hexdigest(), 'format': 'png', 'width': 1, 'height': 1}
        self.save()

    def save(self):
        self.outputs.write_text(json.dumps([self.record]))

    def check(self, local=True):
        with contextlib.redirect_stdout(io.StringIO()):
            validator.validate(self.root, self.root if local else None)

    def test_dependency_readme_is_not_project_documentation(self):
        dependency = self.root / 'node_modules/fixture'
        dependency.mkdir(parents=True)
        (dependency / 'README.md').write_text('[upstream-only link](missing.md)')
        self.check()

    def test_broken_project_readme_still_rejected(self):
        (self.root / 'README.md').write_text('[broken](missing.md)')
        with self.assertRaisesRegex(validator.ValidationError, 'Broken link'):
            self.check()

    def test_valid_native_export_passes(self):
        self.check()

    def test_missing_native_export_rejected(self):
        (self.root / 'native.mp4').unlink()
        with self.assertRaisesRegex(validator.ValidationError, "Missing artifact"):
            self.check()

    def test_native_size_drift_rejected(self):
        (self.root / 'native.mp4').write_bytes(b'short')
        with self.assertRaisesRegex(validator.ValidationError, 'Size drift'):
            self.check()

    def test_same_size_native_corruption_rejected(self):
        (self.root / 'native.mp4').write_bytes(b'broken')
        with self.assertRaisesRegex(validator.ValidationError, 'Hash drift'):
            self.check()

    def test_final_export_corruption_still_rejected(self):
        (self.root / 'final.mp4').write_bytes(b'wrong')
        with self.assertRaisesRegex(validator.ValidationError, 'Hash drift'):
            self.check()

    def test_missing_thumbnail_rejected(self):
        (self.root / 'thumbnail.png').unlink()
        with self.assertRaisesRegex(validator.ValidationError, "Missing artifact"):
            self.check()

    def test_same_size_thumbnail_corruption_rejected(self):
        p = self.root / 'thumbnail.png'
        data = p.read_bytes()
        p.write_bytes(data[:-1] + bytes([data[-1] ^ 1]))
        with self.assertRaisesRegex(validator.ValidationError, 'Hash drift'):
            self.check()

    def test_thumbnail_size_drift_rejected(self):
        (self.root / 'thumbnail.png').write_bytes(b'wrong')
        with self.assertRaisesRegex(validator.ValidationError, 'Size drift'):
            self.check()

    def test_thumbnail_dimension_drift_rejected(self):
        self.record['thumbnail']['width'] = 2
        self.save()
        with self.assertRaisesRegex(validator.ValidationError, 'Dimension drift'):
            self.check()

    def test_non_png_thumbnail_rejected_even_with_matching_hash(self):
        data = b'X' * 32
        (self.root / 'thumbnail.png').write_bytes(data)
        self.record['thumbnail']['bytes'] = len(data)
        self.record['thumbnail']['sha256'] = hashlib.sha256(data).hexdigest()
        self.save()
        with self.assertRaisesRegex(validator.ValidationError, 'Invalid PNG header'):
            self.check()

    def test_thumbnail_metadata_rejected_without_files(self):
        for field, value in [('width', 0), ('height', '1080'), ('sha256', 'invalid'), ('local_output', '../escape.png')]:
            with self.subTest(field=field):
                old = self.record['thumbnail'][field]
                self.record['thumbnail'][field] = value
                self.save()
                with self.assertRaises(validator.ValidationError):
                    self.check(local=False)
                self.record['thumbnail'][field] = old

    def test_native_metadata_rejected_without_local_files(self):
        for field, value in [('sha256', 'invalid'), ('bytes', 0), ('local_output', '../escape.mp4')]:
            with self.subTest(field=field):
                original = self.record['native_export'][field]
                self.record['native_export'][field] = value
                self.save()
                with self.assertRaises(validator.ValidationError):
                    self.check(local=False)
                self.record['native_export'][field] = original



    def test_next_date_is_discovered_without_code_changes(self):
        target = self.root / 'experiments/2027-01-01/outputs.json'
        target.parent.mkdir()
        self.outputs.rename(target)
        self.check()

    def test_duplicate_across_dates_rejected(self):
        target = self.root / 'experiments/2027-01-01/outputs.json'
        target.parent.mkdir()
        target.write_text(self.outputs.read_text())
        with self.assertRaisesRegex(validator.ValidationError, 'Duplicate experiment'):
            self.check()

    def test_evidence_markers_are_data_driven(self):
        self.record['evidence_checks'] = ['Fixture evidence']
        self.save()
        self.check()
        self.record['evidence_checks'] = ['unrecorded claim']
        self.save()
        with self.assertRaisesRegex(validator.ValidationError, 'Missing evidence marker'):
            self.check()

    def test_optimized_python_still_rejects_invalid_artifact(self):
        script = Path(validator.__file__)
        command = 'import runpy; v=runpy.run_path(' + repr(str(script)) + '); v["validate_artifact"]({"bytes":0,"sha256":"bad","local_output":"x"})'
        result = subprocess.run([sys.executable, '-O', '-c', command], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('ValidationError', result.stderr)

    def test_schema_rejects_missing_required_field(self):
        del self.record['sha256']
        self.save()
        with self.assertRaisesRegex(validator.ValidationError, 'missing sha256'):
            self.check(local=False)

    def test_new_schema_assertion_keyword_fails_closed(self):
        with self.assertRaisesRegex(validator.ValidationError, 'unsupported schema keywords'):
            validator.check_schema({}, {'additionalProperties': False}, {}, 'fixture')


if __name__ == '__main__':
    unittest.main()
