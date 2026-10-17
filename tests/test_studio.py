"""Offline studio boundaries; generated PCM fixtures, no owner media or models."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import copy
import runpy
import shutil
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'skills/video-production-router/scripts'


class StudioTests(unittest.TestCase):
    def test_last_probe_exhausting_scan_budget_does_not_return_partial_index(self):
        api = runpy.run_path(str(SCRIPTS / 'library.py'))
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            (folder / 'sample.wav').write_bytes(b'synthetic probe fixture')
            args = SimpleNamespace(max_files=10, wall_seconds=1, max_file_mb=1,
                                   ffprobe='ffprobe', ffmpeg='ffmpeg', analyze_seconds=0)
            with patch('time.monotonic', side_effect=[0, 0, 0, 2]), patch('subprocess.run', side_effect=[
                    subprocess.TimeoutExpired('ffprobe', 1), SimpleNamespace(stdout='test version\n')]):
                with self.assertRaisesRegex(ValueError, 'budget reached'):
                    api['scan'](folder, {'tracks': []}, args)

    def example(self, scenario='repackaging'):
        return json.loads((ROOT / f'examples/workflows/{scenario}.json').read_text())

    def test_all_three_scenarios_share_gates_and_checkpoint_outputs(self):
        for scenario in ['repackaging', 'insight', 'hybrid']:
            with self.subTest(scenario=scenario):
                source = ROOT / f'examples/workflows/{scenario}.json'
                r = subprocess.run([sys.executable, str(SCRIPTS / 'workflow.py'), str(source), '--format', 'brief'],
                                   capture_output=True, text=True)
                self.assertEqual(r.returncode, 0, r.stderr)
                brief = json.loads(r.stdout)
                project = runpy.run_path(str(SCRIPTS / 'project.py'))['initial'](brief)
                steps = {s['id']: s for s in project['steps']}
                self.assertIn('production-review', steps['scene:1']['depends_on'])
                self.assertEqual(steps['publication']['state'], 'blocked')
                self.assertIn('production:provenance', project['artifacts'])
                self.assertIsNone(project['artifacts']['production:thumbnail']['file'])
                self.assertIn('qa:delivery-materials', steps['delivery']['depends_on'])
                self.assertEqual(project['plan']['minimum_evidence'], 'tested')
                self.assertFalse(project['plan']['production']['execution_authorized'])

    def test_source_rights_and_claim_validation(self):
        assess = runpy.run_path(str(SCRIPTS / 'workflow.py'))['assess']
        original = self.example('hybrid')
        self.assertTrue(assess(original)['publication_blockers'])
        keep = copy.deepcopy(original); keep['sources'][0]['audio_policy'] = 'keep'
        self.assertTrue(any(':audio:' in x for x in assess(keep)['publication_blockers']))
        denied = copy.deepcopy(original); denied['sources'][0]['video_rights'] = {'status': 'denied'}
        self.assertTrue(any('denied' in x for x in assess(denied)['publication_blockers']))
        for change in [lambda s: s['sources'].append(s['sources'][0]),
                       lambda s: s['claims'][0].update(source='absent'),
                       lambda s: s['edits'][0].update(out_seconds=-1),
                       lambda s: s['limits'].update(wall_minutes=float('nan')),
                       lambda s: s['sources'][0].update(video_rights={'status': 'granted'})]:
            bad = copy.deepcopy(original); change(bad)
            with self.assertRaises(ValueError): assess(bad)

    def test_unqualified_features_and_frozen_fact_gate_cannot_be_overridden(self):
        spec = self.example('insight')
        spec['brief']['blocks'][0]['deliverables'] = ['song-generation']
        brief = spec['brief']; brief['production'] = {k:v for k,v in spec.items() if k!='brief'}
        api = runpy.run_path(str(SCRIPTS / 'project.py'))
        data = api['initial'](brief)
        self.assertIn('song-generation', data['plan']['blocks'][0]['unmet'])
        self.assertNotIn('suno', data['plan']['blocks'][0]['tools'])
        with self.assertRaisesRegex(ValueError, 'unmet'):
            api['mark'](data, Path('/tmp'), 'production-review', 'done', 'override')

    def test_declared_timeline_budget_is_a_gate_and_legacy_briefs_are_unchanged(self):
        planner = runpy.run_path(str(SCRIPTS / 'plan.py'))['plan']
        registry = json.loads((SCRIPTS.parent / 'references/tools.json').read_text())
        spec = self.example()
        brief = spec['brief']
        before = planner(brief, registry)
        self.assertNotIn('production', before)
        brief['production'] = {k:v for k,v in spec.items() if k != 'brief'}
        brief['production']['limits']['max_output_seconds'] = 10
        result = planner(brief, registry)
        self.assertTrue(any('complete timeline' in x for x in result['production']['production_blockers']))
        del brief['production']
        self.assertEqual(planner(brief, registry), before)

    def test_independent_music_account_and_rights_gates_survive_workflow(self):
        planner = runpy.run_path(str(SCRIPTS / 'plan.py'))['plan']
        registry = json.loads((SCRIPTS.parent / 'references/tools.json').read_text())
        spec = self.example()
        brief = spec['brief']; brief['production'] = {k:v for k,v in spec.items() if k != 'brief'}
        brief['music'] = {'direction':'video-first','mode':'instrumental','provider':'suno','video_source':'uninspected.mp4'}
        result = planner(brief, registry)['production']
        self.assertTrue(any('credits' in x for x in result['production_blockers']))
        self.assertTrue(any('music usage' in x for x in result['publication_blockers']))

    @unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'), 'optional local FFmpeg integration')
    def test_audio_analysis_and_budget_failure_preserve_previous_catalogue(self):
        import wave
        import struct
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); folder = root / 'music'; folder.mkdir()
            with wave.open(str(folder / 'tone.wav'), 'wb') as w:
                w.setparams((1, 2, 8000, 0, 'NONE', 'not compressed'))
                w.writeframes(struct.pack('<h', 1000) * 8000)
            index = root / 'music.json'
            cli = [sys.executable, str(SCRIPTS / 'library.py')]
            first = subprocess.run(cli + ['scan', str(folder), str(index), '--analyze-seconds', '1'], capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            row = json.loads(index.read_text())['tracks'][0]
            self.assertAlmostEqual(row['loudness']['mean_dbfs'], -30.3, delta=0.2)
            self.assertEqual(row['loudness']['window_seconds'], 1)
            previous = index.read_bytes()
            limited = subprocess.run(cli + ['scan', str(folder), str(index), '--max-files', '0'], capture_output=True)
            self.assertNotEqual(limited.returncode, 0)
            self.assertEqual(index.read_bytes(), previous)

    def test_private_catalogue_cannot_be_written_among_public_source(self):
        private_path = runpy.run_path(str(SCRIPTS / 'library.py'))['private_path']
        with self.assertRaisesRegex(ValueError, 'Private catalogue'):
            private_path(ROOT / 'accidental-private-index.json')

    def test_denied_retained_media_blocks_execution_but_removed_audio_does_not(self):
        assess = runpy.run_path(str(SCRIPTS / 'workflow.py'))['assess']
        spec = self.example()
        spec['sources'][0]['audio_rights'] = {'status': 'denied'}
        self.assertFalse(any('use denied' in x for x in assess(spec)['production_blockers']))
        spec['sources'][0]['audio_policy'] = 'keep'
        self.assertTrue(any('use denied' in x for x in assess(spec)['production_blockers']))

    @unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'), 'optional local FFmpeg integration')
    def test_local_music_index_unknown_rights_annotation_and_changed_file(self):
        import wave
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            audio = root / 'music'; audio.mkdir()
            song = audio / 'own.wav'
            with wave.open(str(song), 'wb') as w:
                w.setparams((1, 2, 8000, 0, 'NONE', 'not compressed'))
                w.writeframes(b'\x00\x00' * 8000)
            index = root / 'index.json'
            def cli(*args, ok=True):
                r = subprocess.run([sys.executable, str(SCRIPTS / 'library.py'), *map(str, args)], capture_output=True, text=True)
                self.assertEqual(r.returncode == 0, ok, r.stderr)
                return json.loads(r.stdout) if ok else r
            cli('scan', audio, index)
            track = json.loads(index.read_text())['tracks'][0]
            self.assertAlmostEqual(track['duration_seconds'], 1)
            self.assertIsNone(track['bpm'])
            self.assertEqual(cli('find', index, '--use', 'commercial')['tracks'], [])
            cli('annotate', index, track['id'], '--mood', 'calm', '--bpm', '90',
                '--rights', 'granted', '--evidence', 'Owner confirms original composition and recording')
            self.assertEqual(len(cli('find', index, '--use', 'commercial', '--mood', 'calm')['tracks']), 1)
            song.write_bytes(b'changed')
            self.assertEqual(cli('find', index, '--use', 'commercial')['tracks'], [])
            self.assertTrue(cli('find', index)['file_problems'])

    def test_unknown_source_audio_can_be_removed_without_granting_video_rights(self):
        import runpy
        assess = runpy.run_path(str(SCRIPTS / 'workflow.py'))['assess']
        spec = {'scenario': 'repackaging', 'sources': [
            {'id': 'clip', 'kind': 'video', 'origin': 'owner-supplied local reference',
             'video_rights': {'status': 'unknown'}, 'audio_policy': 'remove'}],
            'limits': {'wall_minutes': 20, 'max_input_seconds': 60, 'max_output_seconds': 15,
                       'max_work_mb': 200, 'max_download_mb': 0, 'paid_calls': 0},
            'acceptance': ['No old audio; intelligible speech and readable first screen'],
            'edits': [{'source': 'clip', 'in_seconds': 0, 'out_seconds': 4, 'reason': 'owner-selected opening'}]}
        result = assess(spec)
        self.assertTrue(result['publication_blockers'])
        self.assertFalse(any('clip:audio' in x for x in result['publication_blockers']))
        self.assertFalse(result['execution_authorized'])
        self.assertEqual(result['qualification'], 'experimental_planning_only')


if __name__ == '__main__':
    unittest.main()
