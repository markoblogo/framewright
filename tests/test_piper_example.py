"""Guard the exact voice pair without installing Piper or running a model."""
import hashlib
import importlib.util
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('piper_example', ROOT / 'examples/remotion-agro-uk/synthesize.py')
example = importlib.util.module_from_spec(spec)
spec.loader.exec_module(example)


class PiperExampleTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        (self.base / 'models').mkdir()
        self.payloads = {'tetiana.onnx': b'test-model', 'tetiana.onnx.json': b'{"sample_rate":22050}'}
        for name, data in self.payloads.items():
            (self.base / 'models' / name).write_bytes(data)
        hashes = {name: hashlib.sha256(data).hexdigest() for name, data in self.payloads.items()}
        self.hash_patch = patch.object(example, 'MODEL_FILES', hashes)
        self.hash_patch.start()
        self.addCleanup(self.hash_patch.stop)
        self.load = Mock(side_effect=RuntimeError('verified loader reached'))
        self.modules = patch.dict('sys.modules', {
            'onnxruntime': SimpleNamespace(disable_telemetry_events=Mock()),
            'piper': SimpleNamespace(PiperVoice=SimpleNamespace(load=self.load), SynthesisConfig=Mock()),
        })
        self.modules.start()
        self.addCleanup(self.modules.stop)

    def test_changed_config_rejected_before_voice_load(self):
        (self.base / 'models/tetiana.onnx.json').write_bytes(b'{"sample_rate":44100}')
        with self.assertRaisesRegex(ValueError, 'tetiana.onnx.json'):
            example.main(self.base)
        self.load.assert_not_called()
        self.assertFalse((self.base / 'audio').exists())

    def test_changed_model_rejected_before_voice_load(self):
        (self.base / 'models/tetiana.onnx').write_bytes(b'different-model')
        with self.assertRaisesRegex(ValueError, 'tetiana.onnx'):
            example.main(self.base)
        self.load.assert_not_called()

    def test_verified_pair_is_passed_explicitly_to_loader(self):
        with self.assertRaisesRegex(RuntimeError, 'verified loader reached'):
            example.main(self.base)
        self.load.assert_called_once_with(str(self.base / 'models/tetiana.onnx'),
                                          config_path=str(self.base / 'models/tetiana.onnx.json'))
