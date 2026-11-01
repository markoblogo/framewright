"""English-copy preflight: layout fit cannot stand in for reading time."""
from pathlib import Path
import json, subprocess, sys, tempfile, unittest
ROOT=Path(__file__).resolve().parents[1]
TOOL=ROOT/'examples/production-reuse/caption_timing.py'
class CaptionTimingTest(unittest.TestCase):
 def check_plan(self,shots):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'plan.json';p.write_text(json.dumps({'shots':shots}))
   r=subprocess.run([sys.executable,str(TOOL),str(p)],capture_output=True,text=True)
   return r,json.loads(r.stdout) if r.stdout else {}
 def test_long_copy_is_flagged_and_short_copy_preserved(self):
  shots=[{'duration':3,'title':'ART','subtitle':''}, {'duration':3,'title':'Long international headline with numbers and details. '*2,'subtitle':'A separate subtitle also needs reading time'}]
  original=json.dumps(shots)
  r,d=self.check_plan(shots)
  self.assertEqual(r.returncode,2,r.stderr)
  self.assertEqual(d['shots'][0]['status'],'pass')
  self.assertEqual(d['shots'][1]['status'],'too_short')
  self.assertGreater(d['shots'][1]['minimum_seconds'],3)
  self.assertEqual(json.dumps(shots),original)
 def test_unbroken_copy_and_subtitle_are_timed_without_clamping(self):
  r,d=self.check_plan([{'duration':3,'title':'X'*96,'subtitle':'Y'*64}])
  self.assertEqual(r.returncode,2,r.stderr)
  self.assertGreater(d['shots'][0]['minimum_seconds'],10)
  r2,d2=self.check_plan([{'duration':d['shots'][0]['minimum_seconds'],'title':'X'*96,'subtitle':'Y'*64}])
  self.assertEqual(r2.returncode,0,r2.stderr)
  self.assertEqual(d2['shots'][0]['status'],'pass')
 def test_invalid_duration_rejected(self):
  for duration in [True,-1,0,float('nan'),float('inf')]:
   with self.subTest(duration=duration):
    r,_=self.check_plan([{'duration':duration,'title':'ART'}])
    self.assertEqual(r.returncode,1)
 def test_opt_in_render_guard_precedes_output_and_media_access(self):
  try:import PIL
  except ImportError:self.skipTest('Optional Pillow absent')
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'plan.json';out=Path(tmp)/'output'
   p.write_text(json.dumps({'shots':[{'duration':3,'title':'X'*96,'subtitle':'Y'*64,'file':'missing.png','kind':'photo'}]}))
   r=subprocess.run([sys.executable,str(ROOT/'examples/production-reuse/render.py'),str(p),str(out),'--aspect','16x9','--enforce-caption-timing'],capture_output=True,text=True)
   self.assertNotEqual(r.returncode,0)
   self.assertIn('Caption reading time',r.stderr)
   self.assertFalse(out.exists())
