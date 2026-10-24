"""A working brief derives facts and proposes a next step without editing the project."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1];CLI=ROOT/'skills/video-production-router/scripts/project.py'
class BriefTest(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.p=self.root/'project.json'
  self.cli('create',self.p,'--goal','English cut','--note','Private project')
  self.f=self.root/'master.txt';self.f.write_text('retained film');self.cli('asset',self.p,'film','--kind','video');self.cli('retain',self.p,'film',self.f)
 def cli(self,*args,ok=True):
  p=subprocess.run([sys.executable,str(CLI),*map(str,args)],capture_output=True,text=True);self.assertEqual(p.returncode==0,ok,p.stderr);return p
 def test_brief_preserves_accepted_work_and_distinguishes_next_proposal_from_authority(self):
  self.cli('observe',self.p,'output:film','--kind','creative','--result','accepted','--actor','owner','--provenance','owner_report','--note','Keep approved picture')
  self.cli('task',self.p,'sample','--label','Prepare short narration sample')
  self.cli('task',self.p,'names','--label','Confirm names','--waiting-for','owner','--note','Pronunciation of two names')
  before=self.p.read_bytes();v=json.loads(self.cli('brief',self.p,'--json').stdout)
  self.assertEqual(v['goal'],'English cut');self.assertEqual(v['accepted'][0]['note'],'Keep approved picture')
  self.assertEqual(v['waiting'][0]['party'],'owner');self.assertEqual(v['proposed_next']['kind'],'ready_task');self.assertEqual(v['proposed_next']['status'],'proposal_not_execution_authority');self.assertEqual(before,self.p.read_bytes())
 def test_changed_revision_overrides_ready_work_and_reopens_approval_for_review(self):
  self.cli('observe',self.p,'output:film','--kind','creative','--result','accepted','--actor','owner','--provenance','owner_report','--note','Picture accepted')
  self.cli('task',self.p,'render','--label','Render final')
  self.f.write_text('changed bytes')
  v=json.loads(self.cli('brief',self.p,'--json').stdout)
  self.assertEqual(v['accepted'],[]);self.assertEqual(v['file_changes'][0]['state'],'changed');self.assertEqual(v['proposed_next']['kind'],'file_review');self.assertEqual(v['ready_tasks'],[]);self.assertEqual(v['needs_recheck'][0]['reason'],'stale_revision')
 def test_explicit_wait_is_not_converted_to_ready_production(self):
  self.cli('task',self.p,'pause','--label','Production paused','--waiting-for','owner','--note','Await explicit resumption')
  before=self.p.read_bytes();v=json.loads(self.cli('brief',self.p,'--json').stdout)
  self.assertEqual(v['proposed_next']['kind'],'waiting');self.assertEqual(v['ready_tasks'],[]);self.assertEqual(before,self.p.read_bytes())
 def test_limits_are_visible_and_recorded_replacement_does_not_invent_a_session_diff(self):
  for n in range(3):
   self.cli('observe',self.p,'project','--kind','decision','--topic','direction-'+str(n),'--result','accepted','--actor','owner','--provenance','owner_report','--note','Keep direction '+str(n))
  self.f.write_text('replacement');self.cli('retain',self.p,'film',self.f,'--replace')
  v=json.loads(self.cli('brief',self.p,'--json','--limit','1').stdout)
  self.assertEqual(len(v['accepted']),1);self.assertEqual(v['counts']['accepted'],3);self.assertEqual(v['recent_revisions'][0]['subject'],'output:film');self.assertEqual(v['file_changes'],[])
  self.assertIn('showing 1',self.cli('brief',self.p,'--limit','1').stdout)
  self.cli('brief',self.p,'--limit','0',ok=False)
 def test_rejected_decision_does_not_reappear_as_accepted_work(self):
  for result in ['accepted','rejected']:
   self.cli('observe',self.p,'project','--kind','decision','--topic','look','--result',result,'--actor','owner','--provenance','owner_report','--note','Look '+result)
  self.assertEqual(json.loads(self.cli('brief',self.p,'--json').stdout)['accepted'],[])
 def test_blocked_constraint_is_visible_even_without_a_named_waiting_party(self):
  self.cli('task',self.p,'budget','--label','Generation budget')
  self.cli('mark',self.p,'budget','--state','blocked','--evidence','No paid generation authorised')
  v=json.loads(self.cli('brief',self.p,'--json').stdout)
  self.assertEqual(v['blockers'][0]['reason'],'No paid generation authorised');self.assertEqual(v['proposed_next']['kind'],'blocked')
