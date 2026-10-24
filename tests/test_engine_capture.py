"""Capture planning is offline; actual browser tests are opt-in."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
CLI=ROOT/'skills/video-production-router/scripts/engine_capture.py'
class CaptureTest(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
 def cli(self,config,*args,ok=True):
  c=self.root/'capture.json';c.write_text(json.dumps(config));p=subprocess.run([sys.executable,str(CLI),str(c),*map(str,args)],capture_output=True,text=True);self.assertEqual(p.returncode==0,ok,p.stderr);return p
 def test_plan_is_offline_and_requires_explicit_audio_and_bounded_loop(self):
  c={'url':'https://example.test/scene','adapter':'contract','canvas':'canvas','width':640,'height':360,'duration_seconds':4,'fps':24,'audio':'none','repeat':3}
  view=json.loads(self.cli(c).stdout);self.assertEqual(view['execution'],'not_started');self.assertEqual(view['output_seconds'],12)
  self.assertFalse((self.root/'capture').exists())
  for changes in ({'audio':'auto'},{'repeat':0},{'duration_seconds':float('nan')},{'url':'file:///etc/passwd'},{'width':True},{'width':641},{'browser_args':['--user-data-dir=/private/profile']},{'script':'alert(1)'}):self.cli({**c,**changes},ok=False)

 def test_execute_requires_existing_runtimes_without_creating_output(self):
  c={'url':'https://example.test','adapter':'contract','canvas':'canvas','duration_seconds':2,'audio':'none'}
  self.cli(c,'--execute','--output',self.root/'capture','--browser',self.root/'absent-browser','--puppeteer-module',self.root/'absent-module',ok=False)
  self.assertFalse((self.root/'capture').exists())
 @unittest.skipUnless(__import__('shutil').which('ffmpeg'),'ffmpeg unavailable')
 def test_loop_qa_measures_encoded_motion_and_rejects_static_capture(self):
  import runpy,shutil
  m=runpy.run_path(str(CLI));ffmpeg=shutil.which('ffmpeg');still=self.root/'still.mp4';moving=self.root/'moving.mp4'
  for output,source in [(still,'color=c=black:s=128x72:r=16:d=1'),(moving,'testsrc2=s=128x72:r=16:d=1')]:
   subprocess.run([ffmpeg,'-v','error','-f','lavfi','-i',source,'-c:v','libx264','-pix_fmt','yuv420p',str(output)],check=True,capture_output=True)
  with self.assertRaisesRegex(ValueError,'no measured motion'):m['seam_report'](still,ffmpeg,16,'none',True)
  self.assertTrue(m['seam_report'](moving,ffmpeg,16,'none',True)['motion_detected'])
 def test_hook_must_be_a_retained_exact_local_revision(self):
  import hashlib
  hook=self.root/'hook.js';hook.write_text('window.captureTest=true;')
  c={'url':'https://example.test','adapter':'contract','canvas':'canvas','duration_seconds':2,'audio':'none','hook':'hook.js','hook_sha256':hashlib.sha256(hook.read_bytes()).hexdigest()}
  self.cli(c);hook.write_text('changed');self.cli(c,ok=False)
 @unittest.skipUnless(__import__('os').environ.get('FRAMEWRIGHT_BROWSER') and __import__('os').environ.get('FRAMEWRIGHT_PUPPETEER'),'explicit local browser paths not supplied')
 def test_real_browser_audio_controls_and_repeated_encoded_cycle(self):
  import functools,http.server,threading,os
  handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT/'tests/fixtures/engine-capture'))
  server=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
  self.addCleanup(server.server_close);self.addCleanup(server.shutdown)
  c={'url':'http://127.0.0.1:'+str(server.server_port)+'/','adapter':'contract','canvas':'canvas','duration_seconds':2,'audio':'game','width':640,'height':360,'repeat':3}
  out=self.root/'capture';self.cli(c,'--execute','--output',out,'--browser',os.environ['FRAMEWRIGHT_BROWSER'],'--puppeteer-module',os.environ['FRAMEWRIGHT_PUPPETEER'])
  r=json.loads((out/'capture-report.json').read_text());self.assertEqual(r['full_decode'],'pass');self.assertGreater(r['output_seconds'],5.9);self.assertLess(r['output_seconds'],6.5);self.assertEqual(r['browser']['audio']['rms']['muted'],0);self.assertEqual(r['loop']['visual_seam'],'pass')
