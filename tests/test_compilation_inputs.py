"""Source pins reject substitution before media decoding; no renderer needed."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / 'examples/moviepy-agro-series'

class CompilationInputsTest(unittest.TestCase):
    def test_changed_or_missing_auxiliary_source_rejected(self):
        spec = importlib.util.spec_from_file_location('compilation_inputs', EXAMPLE / 'inputs.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / 'stem.wav'
            source.write_bytes(b'qualified')
            pins = root / 'pins.json'
            pins.write_text(json.dumps({'music': {'local_output': 'stem.wav', 'sha256': hashlib.sha256(b'qualified').hexdigest()}}))
            self.assertEqual(module.verified_input('music', root, pins), source)
            source.write_bytes(b'replacement')
            with self.assertRaisesRegex(ValueError, 'music'):
                module.verified_input('music', root, pins)
            source.unlink()
            with self.assertRaisesRegex(ValueError, 'music'):
                module.verified_input('music', root, pins)
