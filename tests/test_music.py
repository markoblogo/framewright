import copy
import importlib.util
import json
from pathlib import Path
import unittest
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('music', ROOT / 'skills/video-production-router/scripts/music.py')
music = importlib.util.module_from_spec(spec)
spec.loader.exec_module(music)
REGISTRY = json.loads((ROOT / 'skills/video-production-router/references/tools.json').read_text())


class MusicPlanTest(unittest.TestCase):
    def run_plan(self, **changes):
        brief = {'direction': 'brief-first', 'mode': 'instrumental', 'provider': 'suno', **changes}
        return music.plan_music(brief, copy.deepcopy(REGISTRY))

    def test_song_is_foreground_not_tts(self):
        p = self.run_plan(mode='song', lyrics='An original synthetic test line.', lyrics_authorized=True)
        self.assertEqual(p['audio_role'], 'foreground_song')
        self.assertEqual(p['execution'], 'not_started')

    def test_existing_audio_with_provider_visuals_still_has_account_gate(self):
        for visual in ['native-export', 'generated-scenes']:
            with self.subTest(visual=visual):
                p = self.run_plan(direction='music-first', mode='existing', provider='suno', audio_source='demo.wav', inputs_authorized=True, visual_source=visual)
                self.assertTrue(any('account model' in gate for gate in p['permission_gates']))

    def test_video_first_existing_audio_retains_both_sources(self):
        p = self.run_plan(direction='video-first', mode='existing', provider='existing', video_source='locked.mp4', audio_source='score.wav')
        self.assertEqual(p['sources'], {'video': 'locked.mp4', 'audio': 'score.wav'})
        self.assertEqual(p['timeline_owner'], 'locked_picture')

    def test_video_first_locks_picture(self):
        p = self.run_plan(direction='video-first', video_source='clip.mp4', cues=[{'time_seconds': 0, 'event': 'opening'}, {'time_seconds': 6, 'event': 'cut'}])
        self.assertEqual(p['timeline_owner'], 'locked_picture')

    def test_music_first_uses_existing_source_without_generation(self):
        p = self.run_plan(direction='music-first', mode='existing', provider='existing', audio_source='authorised.wav')
        self.assertEqual(p['timeline_owner'], 'locked_music')
        self.assertEqual(p['technical_status'], 'source_declared_not_decoded')
        self.assertFalse(any('account model' in g for g in p['permission_gates']))

    def test_noncommercial_is_supported_not_technical_failure(self):
        p = self.run_plan(intended_use='noncommercial', rights={'status': 'noncommercial_only', 'evidence': 'current terms and approved trial export'})
        self.assertEqual(p['usage_status'], 'noncommercial_compatible_with_record')
        self.assertEqual(p['technical_status'], 'documented_requires_account_check')

    def test_commercial_restriction_does_not_relabel_tool_unavailable(self):
        p = self.run_plan(intended_use='commercial', rights={'status': 'noncommercial_only', 'evidence': 'trial download receipt'})
        self.assertEqual(p['usage_status'], 'commercial_not_permitted_by_record')
        self.assertEqual(p['technical_status'], 'documented_requires_account_check')

    def test_unknown_rights_are_not_inferred_from_paid_provider(self):
        p = self.run_plan(intended_use='commercial', provider_plan='paid')
        self.assertEqual(p['usage_status'], 'rights_review_required')
        self.assertFalse(p['publication_authorized'])

    def test_native_song_card_is_separate_from_paid_generated_art(self):
        a = self.run_plan(visual_source='native-export')
        b = self.run_plan(visual_source='generated-scenes')
        self.assertEqual(a['native_visuals']['feature'], 'song-card-video')
        self.assertFalse(a['native_visuals']['requires_paid_feature'])
        self.assertEqual(b['native_visuals']['feature'], 'video-cover-art')
        self.assertTrue(b['native_visuals']['requires_paid_feature'])

    def test_flow_generated_scene_remains_documented(self):
        p = self.run_plan(provider='flow-music', visual_source='generated-scenes')
        self.assertEqual(p['native_visuals']['feature'], 'music-video-generation')
        self.assertEqual(p['native_visuals']['evidence'], 'documented')

    def test_missing_sources_lyrics_and_false_rights_claim_rejected(self):
        for args in [{'direction': 'video-first'}, {'direction': 'music-first', 'mode': 'existing'}, {'mode': 'song'}, {'rights': {'status': 'commercial_granted'}}]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                self.run_plan(**args)

    def test_existing_provider_cannot_generate_a_song(self):
        with self.assertRaisesRegex(ValueError, 'cannot generate'):
            self.run_plan(provider='existing', mode='song', lyrics='Original synthetic line')

    def test_music_plan_in_picture_brief_keeps_independent_gates(self):
        import runpy
        picture = runpy.run_path(str(ROOT / 'skills/video-production-router/scripts/plan.py'))['plan']
        result = picture({'blocks': [{'id': 'intro', 'input': 'brand'}], 'music': {'direction': 'video-first', 'video_source': 'local.mp4', 'provider': 'suno'}}, REGISTRY)
        self.assertEqual(result['status'], 'proposed')
        self.assertEqual(result['music']['timeline_owner'], 'locked_picture')
        self.assertTrue(result['music']['permission_gates'])
        self.assertFalse(result['music']['publication_authorized'])

    def test_standalone_cli_returns_json_and_rejects_invalid_input(self):
        with tempfile.TemporaryDirectory() as directory:
            brief = Path(directory) / 'music.json'
            brief.write_text(json.dumps({'direction': 'music-first', 'audio_source': 'demo.wav'}))
            command = [sys.executable, str(ROOT / 'skills/video-production-router/scripts/music.py'), str(brief)]
            run = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(json.loads(run.stdout)['execution'], 'not_started')
            brief.write_text('{}')
            run = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(run.returncode, 0)
            self.assertIn('music.direction', run.stderr)

    def test_invalid_cues_rejected(self):
        for cues in [[{'time_seconds': -1, 'event': 'cut'}], [{'time_seconds': 'NaN', 'event': 'cut'}], [{'time_seconds': 2, 'event': 'a'}, {'time_seconds': 1, 'event': 'b'}]]:
            with self.subTest(cues=cues), self.assertRaises(ValueError):
                self.run_plan(cues=cues)


if __name__ == '__main__':
    unittest.main()
