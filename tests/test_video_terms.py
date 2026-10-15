import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/video-production-router'
spec = importlib.util.spec_from_file_location('terms', SKILL / 'scripts/terms.py')
terms = importlib.util.module_from_spec(spec)
spec.loader.exec_module(terms)
spec = importlib.util.spec_from_file_location('planner', SKILL / 'scripts/plan.py')
planner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(planner)


class VideoVocabularyTest(unittest.TestCase):
    def test_all_24_ru_en_names_resolve_without_collision(self):
        rows = json.loads((SKILL / 'references/video-terms.json').read_text())['terms']
        self.assertEqual(len(rows), 24)
        self.assertEqual(len({x['id'] for x in rows}), 24)
        for row in rows:
            self.assertEqual(terms.normalize_effects([row['ru'], row['en']]), [row['id']])

    def test_distinct_moves_and_audio_edits_stay_distinct(self):
        self.assertEqual(terms.normalize_effects(['Наезд', 'Зум', 'Вертикальная панорама', 'Кран вверх', 'J-склейка', 'L-склейка']),
                         ['dolly-in', 'zoom-in', 'tilt', 'crane-up', 'j-cut', 'l-cut'])
        self.assertEqual(terms.normalize_effects(['Облёт', 'ORBIT', 'долли—зум']), ['orbit', 'dolly-zoom'])

    def test_unknown_and_existing_features_are_preserved(self):
        self.assertEqual(terms.normalize_effects(['camera-travel', 'not-a-known-effect']), ['camera-travel', 'not-a-known-effect'])
        for value in ['pan', [None], ['']]:
            with self.assertRaises(ValueError):
                terms.normalize_effects(value)

    def test_vocabulary_does_not_promote_unknown_technique(self):
        registry = json.loads((SKILL / 'references/tools.json').read_text())
        p = planner.plan({'blocks': [{'id': 'x', 'input': 'object', 'effects': ['Долли-зум', 'Перевод фокуса', 'J-склейка']}]}, registry)
        self.assertEqual(p['status'], 'blocked')
        self.assertEqual(p['blocks'][0]['unmet'], ['dolly-zoom', 'rack-focus', 'j-cut'])
        self.assertEqual(p['execution'], 'not_started')

    def test_ledger_covers_owner_inventory_and_revisit_conditions(self):
        ledger = json.loads((SKILL / 'references/review-ledger.json').read_text())
        rows = ledger['tools']
        self.assertEqual(len(rows), len({x['id'] for x in rows}))
        self.assertTrue({'hyperframes','ffmpeg','auto-editor','openscreen','yt-dlp','puppeteer','manimgx','anatomy','gsap','three-js','sound-layer','librosa','mlx-audio','pyannote','mlx-whisper','parakeet-mlx','claude-video','prompt-motion'} <= {x['id'] for x in rows})
        for row in rows:
            self.assertTrue(row['scope_and_findings'] and row['licence_note'] and row['next_trial_or_retest_condition'])
            for evidence in row['evidence']:
                self.assertTrue((ROOT / evidence).is_file(), evidence)
        anatomy = next(x for x in rows if x['id'] == 'anatomy')
        self.assertIn('failed', anatomy['scope_and_findings'])
        self.assertEqual(next(x for x in rows if x['id']=='prompt-motion')['disposition'], 'reference_only')
