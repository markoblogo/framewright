"""Selected-route admission through public local CLIs; no production or remote calls."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import wave

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'skills/video-production-router/scripts'

class RouteAdmissionTest(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
  self.root=Path(self.tmp.name);self.project=self.root/'project.json'
  self.call('project.py','create',self.project,'--goal','Synthetic route gate','--note','No film')
  self.source=self.root/'tone.wav'
  with wave.open(str(self.source),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(8000);f.writeframes(b'\0\0'*8000)
  self.call('project.py','retain',self.project,'source',self.source,'--input')
  self.call('project.py','asset',self.project,'report','--kind','review-report')
  self.call('project.py','task',self.project,'inspect','--label','Inspect existing source','--requires','report')
  profile=self.root/'profile.json';self.call('intake.py','init',profile)
  self.call('intake.py','preference',profile,'--options','free-only')
  brief=self.root/'brief.json';brief.write_text(json.dumps({'idea':'Use existing media','language':'en','duration_seconds':10,'format':'16:9','narration':False,'visual_source':'supplied','source_rights':'owner','deadline':'flexible'}))
  routes=self.call('intake.py','routes',profile,brief)
  self.retain('routes',routes.stdout,'route-comparison')
  self.env={'id':'local-review','platforms':[],'architectures':[],'min_memory_gib':0,'min_free_disk_gib':0,'programs':[{'name':'ffmpeg'},{'name':'ffprobe'}],'models':[],'manual_checks':[],'rights':{'status':'allowed','basis':'Original synthetic fixture,local inspection only'},'cost':{'status':'free_local','amount':0,'currency':'USD','basis':'Installed local software provider fee only'}}
  self.retain('requirements',json.dumps(self.env),'environment-manifest')
  self.spec={'id':'route-v1','route_subject':'output:routes','route_id':'local-montage','stage_role':'finishing','environment_subject':'output:requirements','step':'inspect','tool':'local-media-review','source':'input:source','output':'report','arguments':{'start':None,'end':None,'context':1.0,'request':None,'after_start':None,'after_end':None,'observe_resources':False},'limits':{'worker_seconds':30,'max_output_bytes':1048576,'min_available_memory_gib':None,'provider_fee_max':'0','unit':'USD'}}
 def call(self,script,*args,ok=True):
  r=subprocess.run([sys.executable,str(BASE/script),*map(str,args)],capture_output=True,text=True)
  self.assertEqual(r.returncode==0,ok,r.stderr);return r
 def retain(self,name,text,kind):
  p=self.root/(name+'.json');p.write_text(text)
  self.call('project.py','asset',self.project,name,'--kind',kind)
  self.call('project.py','retain',self.project,name,p)
 def select(self,ok=True):
  p=self.root/'selection.json';p.write_text(json.dumps(self.spec))
  return self.call('admission.py','select',self.project,p,'--output',self.root/'bound-selection.json',ok=ok)
 def run_executor(self,*extra,ok=True):
  return self.call('executor.py',self.project,'--step','inspect','--source','input:source','--output','report','--execute',*extra,ok=ok)
 def intents(self):return [e for e in json.loads(self.project.read_text())['history'] if e['action']=='executor_intent']
 def test_selected_route_is_checked_before_execution_and_result_stays_unaccepted(self):
  self.select();r=json.loads(self.run_executor().stdout)
  self.assertEqual(r['admission']['result'],'admitted_local_action')
  self.assertEqual(r['state'],'review_pending')
  d=json.loads(self.project.read_text());self.assertEqual(d['steps'][0]['state'],'planned')
  intent=self.intents()[0];self.assertIn('output:admission:route-v1',intent['pins'])
  self.assertEqual(len(self.intents()),1)
  repeat=json.loads(self.call('admission.py','check',self.project,'--step','inspect').stdout)
  self.assertEqual(repeat['result'],'blocked')

 def update_environment(self):
  path=self.root/'requirements.json';path.write_text(json.dumps(self.env))
  self.call('project.py','retain',self.project,'requirements',path,'--replace')
 def test_arguments_and_source_revision_drift_stop_before_dispatch(self):
  self.select();self.run_executor('--observe-resources',ok=False)
  self.assertFalse(self.intents())
  with self.source.open('ab') as f:f.write(b'changed revision')
  self.call('project.py','retain',self.project,'source',self.source,'--input','--replace')
  self.run_executor(ok=False);self.assertFalse(self.intents())
 def test_unmet_host_requirement_stops_before_worker(self):
  self.env['platforms']=['ImaginaryOS'];self.update_environment();self.select()
  report=json.loads(self.call('admission.py','check',self.project,'--step','inspect').stdout)
  self.assertEqual(report['result'],'blocked')
  self.run_executor(ok=False);self.assertFalse(self.intents())
 def test_unknown_cost_and_rights_do_not_become_free_or_allowed(self):
  self.env['cost']={'status':'unknown','amount':None,'currency':'USD','basis':'No quote'}
  self.env['rights']={'status':'unknown','basis':'Not assessed'}
  self.update_environment();self.select();self.run_executor(ok=False)
  self.assertFalse(self.intents())
  gate=next(e['report'] for e in reversed(json.loads(self.project.read_text())['history']) if e['action']=='execution_admission_checked')
  self.assertTrue(any('rights' in b for b in gate['blockers']))
  self.assertTrue(any('paid dispatcher' in b for b in gate['blockers']))
  self.assertIsNone(gate['evidence']['cost']['local_provider_fee'])
 def test_no_silent_substitution_for_other_route_stage(self):
  self.spec['route_id']='quota-generation';self.spec['stage_role']='picture'
  before=self.project.read_bytes();self.select(ok=False)
  self.assertEqual(before,self.project.read_bytes());self.assertFalse(self.intents())
  self.assertFalse((self.root/'bound-selection.json').exists())
 def test_expected_output_limit_rejects_produced_report_without_acceptance(self):
  self.spec['limits']['max_output_bytes']=1;self.select();self.run_executor(ok=False)
  data=json.loads(self.project.read_text())
  self.assertIsNone(data['artifacts']['report']['file']);self.assertEqual(data['steps'][0]['state'],'planned')
  self.assertEqual(len(self.intents()),1)
  self.assertEqual(next(e['state'] for e in reversed(data['history']) if e['action']=='executor_terminal'),'failed')
 def test_contract_repin_cannot_bypass_the_frozen_binding(self):
  self.select();path=self.root/'bound-selection.json';data=json.loads(path.read_text())
  data['selection']['limits']['max_output_bytes']=99;path.write_text(json.dumps(data))
  self.call('project.py','retain',self.project,'admission:route-v1',path,'--replace')
  self.run_executor(ok=False);self.assertFalse(self.intents())
 def test_changed_environment_and_unknown_available_memory_stop_before_dispatch(self):
  self.spec['limits']['min_available_memory_gib']=1000000
  self.select();self.run_executor(ok=False);self.assertFalse(self.intents())
 def test_wrong_output_contract_and_invalid_limits_do_not_select(self):
  before=self.project.read_bytes()
  self.spec['output']='not-required';self.select(ok=False)
  self.spec['output']='report';self.spec['limits']['provider_fee_max']='NaN';self.select(ok=False)
  self.assertEqual(before,self.project.read_bytes());self.assertFalse(self.intents())
 def test_video_review_route_preserves_selected_interval_and_checks_expected_file(self):
  video=self.root/'source.mp4'
  subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','testsrc=size=96x64:rate=24:duration=4','-threads','1','-c:v','libx264','-pix_fmt','yuv420p',str(video)],check=True)
  self.call('project.py','retain',self.project,'video',video,'--input')
  self.call('project.py','asset',self.project,'preview','--kind','review-preview')
  self.call('project.py','task',self.project,'clip','--label','Review source interval','--requires','preview')
  self.spec.update(step='clip',tool='review-clip',source='input:video',output='preview')
  self.spec['arguments'].update(start=1,end=2,context=.5)
  self.select()
  result=json.loads(self.call('executor.py',self.project,'--step','clip','--source','input:video','--output','preview','--tool','review-clip','--start','1','--end','2','--context','.5','--execute').stdout)
  self.assertEqual(result['interval'],{'start':.5,'end':2.5})
  self.assertEqual(result['admission']['expected_output']['format'],'mp4')
  self.assertEqual(result['state'],'review_pending')

 def test_public_preparation_example_creates_selected_unexecuted_project(self):
  folder=self.root/'prepared-example'
  result=subprocess.run([sys.executable,str(ROOT/'examples/admission/prepare_demo.py'),str(folder)],capture_output=True,text=True)
  self.assertEqual(result.returncode,0,result.stderr)
  data=json.loads((folder/'project.json').read_text())
  self.assertIn('inspect',data['execution_routes'])
  self.assertFalse(any(e['action']=='executor_intent' for e in data['history']))
  self.assertIsNone(data['artifacts']['report']['file'])

 def test_scratch_volume_failure_is_visible_even_when_working_volume_fits(self):
  import runpy
  from types import SimpleNamespace
  from unittest.mock import patch
  self.select()
  P=runpy.run_path(str(BASE/'project.py'));A=runpy.run_path(str(BASE/'admission.py'))
  data=P['load'](self.project)
  scratch=Path(tempfile.gettempdir())
  def disk_usage(path):return SimpleNamespace(free=0 if Path(path)==scratch else 4*2**30)
  with patch.object(A['check'].__globals__['shutil'],'disk_usage',side_effect=disk_usage):
   report=A['check'](data,self.project,'inspect',P)
  self.assertEqual(report['result'],'blocked')
  self.assertTrue(any('Scratch volume' in v for v in report['blockers']))
  self.assertFalse(self.intents())
