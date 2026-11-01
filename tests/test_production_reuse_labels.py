"""Authored example: reject clipped copy instead of reporting safe_area=True."""
from pathlib import Path
import runpy
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
try:
 import PIL
except ImportError:
 PIL=None

@unittest.skipUnless(PIL is not None,'Optional Pillow is not installed')
class ReuseLabelTest(unittest.TestCase):
 def setUp(self):
  self.module=runpy.run_path(str(ROOT/'examples/production-reuse/render.py'))
  # Prefer a host font without introducing a bundled font/dependency.
  candidates=[self.module['FONT'],'/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf']
  font=next((p for p in candidates if Path(p).is_file()),None)
  if not font:self.skipTest('No available test font')
  self.label=self.module['label'];self.label.__globals__['FONT']=font
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
  self.out=Path(self.tmp.name)/'caption.png'
 def test_long_unbroken_title_and_subtitle_fail_before_output(self):
  for title,sub in [('ART','subtitle '*120),('W'*400,'')]:
   with self.subTest(title=title[:10],subtitle=bool(sub)),self.assertRaisesRegex(ValueError,'bound'):
    self.label(self.out,title,sub,1280,720)
   self.assertFalse(self.out.exists())
 def test_normal_and_optional_copy_fit_both_aspects(self):
  for w,h in [(1280,720),(720,1280)]:
   for sub in ['', 'POKRAS LAMPAS']:
    result=self.label(self.out,'ONE ARTIST TWO CITIES',sub,w,h)
    self.assertTrue(result['safe_area']);self.assertTrue(self.out.is_file())
