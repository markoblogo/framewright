"""Readable plans through the public CLI; no model, media or renderer."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / 'skills/video-production-router/scripts/plan.py'

class ProductionPacketTest(unittest.TestCase):
    def run_packet(self, brief):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'brief.json'
            source.write_text(json.dumps(brief))
            result = subprocess.run([sys.executable, str(CLI), str(source), '--format', 'markdown'], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def test_real_mixed_plan_has_timeline_evidence_outputs_and_unverified_checks(self):
        brief = json.loads((ROOT / 'examples/briefs/mixed-promo.json').read_text())
        packet = self.run_packet(brief)
        for text in ['# Production plan', '0–180', 'flute', 'kokoro', 'intro-still.png',
                     'planned', 'not_started', 'native', 'loudness', 'source claims', 'integration']:
            self.assertIn(text, packet)
        self.assertNotIn('verified: ', packet)

    def test_still_only_has_image_checks_and_no_final_video_or_audio_work(self):
        packet = self.run_packet({'minimum_evidence':'tested', 'blocks':[
            {'id':'cover','input':'book-art','deliverables':['still-export']}]})
        for text in ['cover-still.png', 'decoded format/dimensions and crop', 'reduced preview', 'unknown; timing']:
            self.assertIn(text, packet)
        self.assertNotIn('## Final assembly', packet)
        self.assertNotIn('final-video.mp4', packet)
        self.assertNotIn('loudness', packet)

    def test_unmet_voice_keeps_explicit_choice_and_no_fictional_wav(self):
        packet = self.run_packet({'blocks':[{'id':'voice','input':'book-art',
            'language':'uk','preferred_voice':'mlx-audio','deliverables':['narration']}]})
        self.assertIn('**blocked**', packet)
        self.assertIn('Explicit voice choice: mlx-audio', packet)
        self.assertIn('blocked: narration', packet)
        self.assertNotIn('-narration.wav', packet)
        self.assertNotIn('## Final assembly', packet)

    def test_music_gates_sources_and_visuals_survive_readable_view(self):
        packet = self.run_packet({'blocks':[{'id':'a','input':'brand'}], 'music':{
            'direction':'video-first','mode':'existing','provider':'suno',
            'video_source':'locked-video.mp4','audio_source':'owned-audio.wav',
            'visual_source':'generated-scenes'}})
        for text in ['locked-video.mp4', 'owned-audio.wav', 'permission_gates', 'credits', 'video-cover-art']:
            self.assertIn(text, packet)

    def test_untrusted_text_cannot_insert_extra_markdown_rows_or_html(self):
        packet = self.run_packet({'blocks':[{'id':'x|y\n<script>', 'input':'brand', 'style':'<img>|test'}]})
        self.assertNotIn('<script>', packet)
        self.assertNotIn('<img>', packet)
        self.assertIn('x\\|y &lt;script&gt;', packet)

    def test_extracted_still_names_its_video_prerequisite(self):
        packet = self.run_packet({'blocks':[{'id':'ui','input':'react-ui','preferred_tool':'flute',
                                              'deliverables':['still-export']}]})
        self.assertIn('extracted encoded frame', packet)
        self.assertIn('intermediate video', packet)
        self.assertNotIn('## Final assembly', packet)

    def test_default_json_and_committed_example_stay_in_sync(self):
        source = ROOT / 'examples/briefs/mixed-promo.json'
        result = subprocess.run([sys.executable, str(CLI), str(source)], text=True, capture_output=True, check=True)
        self.assertEqual(json.loads(result.stdout), json.loads((ROOT / 'examples/plans/mixed-promo.json').read_text()))
        self.assertEqual(self.run_packet(json.loads(source.read_text())), (ROOT / 'examples/plans/mixed-promo.md').read_text())
