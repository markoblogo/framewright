"""Archived source/media protections, with no synthesis or decoding."""
import json
from pathlib import Path
import runpy
import subprocess
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]

class ReviewGuardsTest(unittest.TestCase):
    def test_openscreen_builder_rejects_same_ids_with_replaced_text_or_timing(self):
        voice = runpy.run_path(str(ROOT / 'examples/openscreen-ami-books/synthesize.py'))['voice']
        rows = [{'id':n,'text':t,'start':s} for n,t,s in voice.LINES]
        voice.validate_rows(rows, voice.LINES)
        for field,value in [('text','replacement'),('start',999)]:
            bad = json.loads(json.dumps(rows));bad[0][field]=value
            with patch.dict(sys.modules, {'synthesize':SimpleNamespace(voice=voice),
                                          'numpy':SimpleNamespace(), 'soundfile':SimpleNamespace()}):
                with patch.object(Path,'read_text',return_value=json.dumps(bad)):
                    with self.assertRaisesRegex(ValueError,'mismatched narration'):
                        runpy.run_path(str(ROOT / 'examples/openscreen-ami-books/build-audio.py'))

    def test_compilation_generated_images_ignored_but_input_pins_tracked(self):
        base = 'examples/moviepy-agro-series/'
        for file in ['Agro-Library-YouTube.png','Agro-Library-YouTube.jpg','Thumbnail-reduced.png']:
            self.assertEqual(subprocess.run(['git','check-ignore','--no-index','-q',base+file],cwd=ROOT).returncode,0)
        self.assertEqual(subprocess.run(['git','check-ignore','--no-index','-q',base+'auxiliary-inputs.json'],cwd=ROOT).returncode,1)

    def test_local_checkpoint_paths_are_ignored(self):
        for name in ['local/my-film/project.json','.framewright/project.json','.framewright/project.json.lock']:
            self.assertEqual(subprocess.run(['git','check-ignore','--no-index','-q',name],cwd=ROOT).returncode,0)
