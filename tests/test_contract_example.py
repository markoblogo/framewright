"""Exercise provenance guards without a voice runtime or model download."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import Mock

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / 'examples/remotion-contract-execution'
spec = importlib.util.spec_from_file_location('contract_voice', EXAMPLE / 'synthesize.py')
voice = importlib.util.module_from_spec(spec)
spec.loader.exec_module(voice)


class ContractVoiceTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name) / 'example'
        self.base.mkdir()
        self.shared = Path(self.temp.name) / 'shared'
        self.model = self.shared / 'models/Supertonic-3'
        self.model.mkdir(parents=True)
        self.payloads = {'model.onnx': b'model', 'config.json': b'config', 'F1.json': b'style'}
        self.manifest = {'revision': 'pinned', 'files': []}
        for name, data in self.payloads.items():
            (self.model / name).write_bytes(data)
            self.manifest['files'].append({'file': name, 'sha256': hashlib.sha256(data).hexdigest()})
        (self.base / 'model-manifest.json').write_text(json.dumps(self.manifest))

    def test_self_consistent_external_manifest_cannot_replace_committed_pin(self):
        (self.model / 'config.json').write_bytes(b'new config')
        altered = json.loads(json.dumps(self.manifest))
        altered['revision'] = 'unqualified'
        altered['files'][1]['sha256'] = hashlib.sha256(b'new config').hexdigest()
        (self.shared / 'model-manifest.json').write_text(json.dumps(altered))
        with self.assertRaisesRegex(ValueError, 'config.json'):
            voice.main(self.base, self.shared)
        self.assertFalse((self.base / 'audio').exists())

    def test_external_manifest_not_needed_for_verified_weights(self):
        pinned, root = voice.verify_model(self.shared, self.base / 'model-manifest.json')
        self.assertEqual(pinned['revision'], 'pinned')
        self.assertEqual(root, self.model)

    def test_changed_style_rejected(self):
        (self.model / 'F1.json').write_bytes(b'other voice')
        with self.assertRaisesRegex(ValueError, 'F1.json'):
            voice.main(self.base, self.shared)

    def test_existing_wav_is_regenerated_for_current_inputs(self):
        target = self.base / 'opening.wav'
        target.write_bytes(b'stale')
        tts = Mock()
        tts.synthesize.return_value = ('fresh waveform', 1)
        tts.save_audio.side_effect = lambda wave, path: Path(path).write_text(wave)
        set_seed = Mock()
        voice.generate_line(tts, 'new style', 'new text', target, 42, set_seed)
        self.assertEqual(target.read_text(), 'fresh waveform')
        set_seed.assert_called_once_with(42)
        self.assertEqual(tts.synthesize.call_args.kwargs['text'], 'new text')
        self.assertEqual(tts.synthesize.call_args.kwargs['voice_style'], 'new style')
        self.assertEqual(tts.synthesize.call_args.kwargs['lang'], 'en')
        tts.save_audio.assert_called_once_with('fresh waveform', str(target))

    def test_generated_paths_ignored_but_pins_and_source_not_ignored(self):
        for name in ['cache/hf/file', 'guides/model-manifest.json', 'audio/voice-lines.json',
                     'Contract-Execution-EN.srt', 'Contract-Execution-YouTube.png',
                     'Contract-Execution-YouTube.jpg', 'public/cover.jpeg']:
            with self.subTest(name=name):
                self.assertEqual(subprocess.run(['git', 'check-ignore', '--no-index', '-q',
                                                str(EXAMPLE / name)], cwd=ROOT).returncode, 0)
        for name in ['model-manifest.json', 'package.json', 'tsconfig.json', 'src/index.tsx']:
            with self.subTest(name=name):
                self.assertEqual(subprocess.run(['git', 'check-ignore', '--no-index', '-q',
                                                str(EXAMPLE / name)], cwd=ROOT).returncode, 1)

    def test_failed_rerun_cannot_leave_valid_old_metadata(self):
        audio = self.base / 'audio'
        audio.mkdir()
        for name in ['voice-lines.json', 'voice-lines-timed.json']:
            (audio / name).write_text('old complete metadata')
        voice.invalidate_previous_run(self.base)
        tts = Mock()
        tts.synthesize.side_effect = RuntimeError('failed synthesis')
        with self.assertRaises(RuntimeError):
            voice.generate_line(tts, 'F1', 'new text', audio / 'opening.wav', 42, Mock())
        self.assertFalse((audio / 'voice-lines.json').exists())
        self.assertFalse((audio / 'voice-lines-timed.json').exists())

    def test_clipped_raw_speech_rejected(self):
        voice.reject_clipping(0)
        with self.assertRaisesRegex(ValueError, 'Clipped raw speech'):
            voice.reject_clipping(1)

    def test_probe_does_not_publish_full_assembly_metadata(self):
        (self.base / 'audio').mkdir()
        rows = [{'id': voice.LINES[0][0], 'text': voice.LINES[0][1], 'start': voice.LINES[0][2]}]
        voice.publish_metadata(self.base, rows, True)
        self.assertTrue((self.base / 'audio/probe-lines.json').exists())
        self.assertFalse((self.base / 'audio/voice-lines.json').exists())
        with self.assertRaisesRegex(ValueError, 'Incomplete'):
            voice.validate_rows(rows, voice.LINES)
        full = [{'id': n, 'text': t, 'start': s} for n,t,s in voice.LINES]
        voice.validate_rows(full, voice.LINES)
