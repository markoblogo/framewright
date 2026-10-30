"""Saved-shot admission/worker integration; synthetic Blender stand-in, no model calls."""
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
import unittest
from unittest.mock import patch
import test_route_admission as admission_tests
BASE=admission_tests.BASE

class SavedShotExecutorTest(unittest.TestCase):
 call=admission_tests.RouteAdmissionTest.call
 retain=admission_tests.RouteAdmissionTest.retain
 select=admission_tests.RouteAdmissionTest.select
 intents=admission_tests.RouteAdmissionTest.intents
 def setUp(self):
  admission_tests.RouteAdmissionTest.setUp(self)
  self.bin=self.root/'bin';self.bin.mkdir()
  self.blender=self.bin/'blender'
  self.blender.write_text('#!'+sys.executable+'\n'+'''import json,sys,subprocess,time,os
from pathlib import Path
if '--version' in sys.argv: print('Blender 4.5.15');sys.exit()
job=json.loads(Path(sys.argv[-1]).read_text());out=Path(job['output']);spec=job['spec']
(out/'started').write_text(str(os.getpid()))
if (Path(job['scene']).parent/'hang').exists():
 for _ in range(1200): (out/'alive').touch();time.sleep(.05)
for frame in range(job['start']+1,job['end']+1):
 subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i',f"color=c=orange:s={spec['canvas']['width']}x{spec['canvas']['height']}",'-frames:v','1','-threads','1',str(out/f'frame_{frame:06d}.png')],check=True)
(out/'state.json').write_text(json.dumps({'states':[]}))
''')
  self.blender.chmod(0o700)
  self.addCleanup(patch.stopall);patch.dict(os.environ,PATH=str(self.bin)+os.pathsep+os.environ['PATH']).start()
  scene=self.root/'fixture.blend';scene.write_bytes(b'Synthetic worker fixture, not actual Blender media')
  self.call('project.py','retain',self.project,'scene',scene,'--input')
  shot={'id':'stage','version':'v1','scene':'input:scene','resources':[],
   'canvas':{'width':96,'height':64,'fps':12},'frames':{'start':0,'end':12},
   'engine':{'name':'CYCLES','device':'CPU','samples':4,'seed':7},
   'settings':{'camera':{'object':'Camera','location':[4,-6,3],'rotation_euler':[1,0,.5],'lens':45},
    'actions':{'Actor':'Glide'},'lights':{'Key':{'energy':500,'color':[1,.8,.6],'location':[0,-2,4],'size':3}}},'audio':{'subject':'input:source','gain_db':-6,'offset_seconds':0},'bindings':[]}
  path=self.root/'shot-spec.json';path.write_text(json.dumps(shot))
  self.call('shots.py','prepare',self.project,path,'--output',self.root/'shot.json','--actor','test')
  self.call('project.py','asset',self.project,'shot-preview','--kind','shot-preview')
  self.call('project.py','task',self.project,'render','--label','Render bounded shot','--requires','shot-preview')
  self.env['programs'].append({'name':'blender','minimum_version':'4.5'})
  p=self.root/'requirements.json';p.write_text(json.dumps(self.env));self.call('project.py','retain',self.project,'requirements',p,'--replace')
  self.spec.update(step='render',tool='saved-blender-shot',source='output:shot:stage:v1',output='shot-preview',route_id='local-saved-shot',stage_role='picture')
  self.spec['arguments'].update(start=0,end=3)
 def command(self):
  return [sys.executable,str(BASE/'executor.py'),str(self.project),'--step','render','--source',self.spec['source'],'--output','shot-preview','--tool','saved-blender-shot','--start','0','--end','3','--execute']
 def execute(self,ok=True):
  r=subprocess.run(self.command(),capture_output=True,text=True,timeout=40)
  self.assertEqual(r.returncode==0,ok,r.stderr);return r
 def test_render_retains_receipt_and_stays_review_pending(self):
  self.select();r=json.loads(self.execute().stdout)
  self.assertEqual(r['state'],'review_pending')
  import runpy,copy
  admission=runpy.run_path(str(BASE/'admission.py'));wrong=copy.deepcopy(r['admission'])
  wrong['evidence']['shot']['canvas']['width']+=2
  with self.assertRaisesRegex(ValueError,'picture differs'):
   admission['validate_output'](wrong,Path(r['file']),json.loads(Path(r['receipt']).read_text()))
  data=json.loads(self.project.read_text())
  self.assertTrue(Path(r['file']).is_file())
  receipt=json.loads(Path(r['receipt']).read_text())
  self.assertEqual(receipt['frames'],{'start':0,'end':3})
  self.assertEqual(receipt['creative_review'],'pending')
  self.assertEqual(receipt['audio']['frames'],12000)
  self.assertTrue(receipt['subject'][7:] in data['artifacts'])
  self.assertEqual(next(t for t in data['steps'] if t['id']=='render')['state'],'planned')
  self.assertIn('input:scene',self.intents()[0]['pins'])
  self.assertIn('input:source',self.intents()[0]['pins'])
  self.execute(ok=False);self.assertEqual(len(self.intents()),1)
 def test_intentional_silence_is_preserved(self):
  p=self.root/'shot-spec.json';spec=json.loads(p.read_text());spec.update(version='silent',audio=None);p.write_text(json.dumps(spec))
  self.call('shots.py','prepare',self.project,p,'--output',self.root/'silent.json','--actor','test')
  self.spec['source']='output:shot:stage:silent';self.select()
  r=json.loads(self.execute().stdout);receipt=json.loads(Path(r['receipt']).read_text())
  self.assertIsNone(receipt['audio']);self.assertEqual(receipt['listening_review'],'intentional_silence')
 def test_no_selection_never_dispatches(self):
  self.execute(ok=False);self.assertFalse(self.intents())
 def test_drift_and_binary_replacement_block_before_dispatch(self):
  self.select();self.blender.write_text(self.blender.read_text()+'\n# changed runtime\n')
  self.execute(ok=False);self.assertFalse(self.intents())
 def test_missing_scene_and_fractional_range_block(self):
  self.spec['arguments']['start']=.5;self.select(ok=False)
  self.spec['arguments']['start']=0;self.select()
  (self.root/'fixture.blend').unlink();self.execute(ok=False);self.assertFalse(self.intents())
 def test_small_bundle_limit_fails_without_accepting_output(self):
  self.spec['limits']['max_output_bytes']=1024;self.select();self.execute(ok=False)
  self.assertIsNone(json.loads(self.project.read_text())['artifacts']['shot-preview']['file'])
 def test_scene_repin_invalidates_selection(self):
  self.select();p=self.root/'fixture.blend';p.write_bytes(b'new scene')
  self.call('project.py','retain',self.project,'scene',p,'--input','--replace')
  self.execute(ok=False);self.assertFalse(self.intents())
 def test_timeout_keeps_failure_files_but_no_output(self):
  (self.root/'hang').touch();self.spec['limits']['worker_seconds']=2;self.select()
  self.execute(ok=False)
  data=json.loads(self.project.read_text());self.assertIsNone(data['artifacts']['shot-preview']['file'])
  self.assertTrue(list(self.root.glob('executor-shot-*/job.json')))
  self.assertEqual([e['state'] for e in data['history'] if e['action']=='executor_terminal'],['failed'])
 def test_interruption_kills_owned_blender_and_requires_explicit_retry(self):
  (self.root/'hang').touch();self.select()
  p=subprocess.Popen(self.command(),stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
  self.addCleanup(lambda:p.poll() is None and p.kill())
  marker=None
  for _ in range(200):
   marker=next(self.root.glob('executor-shot-*/started'),None)
   if marker:break
   if p.poll() is not None:break
   time.sleep(.05)
  self.assertIsNotNone(marker)
  child=int(marker.read_text());p.send_signal(signal.SIGTERM);p.communicate(timeout=10)
  alive=marker.with_name('alive');before=alive.stat().st_mtime_ns;time.sleep(.25)
  self.assertEqual(alive.stat().st_mtime_ns,before,'Owned Blender survived interruption')
  self.execute(ok=False);self.assertEqual(len(self.intents()),1)

if __name__=='__main__':unittest.main()
