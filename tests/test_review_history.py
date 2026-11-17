"""An explicit accepted replacement moves old review waits to history,not done."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
CLI=Path(__file__).resolve().parents[1]/'skills/video-production-router/scripts/project.py'

class ReviewHistoryTest(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
  self.root=Path(self.tmp.name);self.p=self.root/'project.json'
  self.cli('create',self.p,'--goal','Accepted revised film','--note','Fixture')
  for ident in ['old','new','portrait']:
   f=self.root/(ident+'.txt');f.write_text(ident)
   self.cli('asset',self.p,ident,'--kind','video');self.cli('retain',self.p,ident,f)
  self.cli('task',self.p,'first-review','--label','Review original','--requires','old','--check-kind','creative','--waiting-for','owner','--note','Original review requested')
  self.observe('old','creative','pending')
  self.cli('task',self.p,'replacement-review','--label','Review revised pair','--requires','new','--requires','portrait','--check-kind','creative')
  for ident in ['new','portrait']:
   for kind,result in [('technical','pass'),('listening','accepted'),('creative','accepted')]:self.observe(ident,kind,result)
  self.cli('mark',self.p,'replacement-review','--state','done','--evidence','Owner accepted revised pair')
  self.cli('select-final',self.p,'output:new','--actor','operator','--note','Chosen accepted revision')
 def cli(self,*args,ok=True):
  r=subprocess.run([sys.executable,str(CLI),*map(str,args)],capture_output=True,text=True)
  self.assertEqual(r.returncode==0,ok,r.stderr);return r
 def observe(self,ident,kind,result):
  self.cli('observe',self.p,'output:'+ident,'--kind',kind,'--result',result,'--actor','owner','--provenance','owner_report','--note','Fixture review')
 def brief(self):return json.loads(self.cli('brief',self.p,'--json').stdout)
 def supersede(self,**kw):return self.cli('supersede-review',self.p,'first-review','--with-task','replacement-review','--actor','operator','--note','Owner requested old wait be historical',**kw)
 def test_explicit_replacement_preserves_history_and_protects_unrelated_wait(self):
  self.cli('task',self.p,'rights','--label','Rights decision','--waiting-for','owner','--note','Still required')
  before=json.loads(self.p.read_text());self.supersede();saved=json.loads(self.p.read_text());raw=self.p.read_bytes();v=self.brief()
  self.assertEqual(before['steps'],saved['steps']);self.assertEqual(saved['journal'][:len(before['journal'])],before['journal'])
  self.assertEqual([r['task'] for r in v['waiting']],['rights']);self.assertFalse(v['needs_recheck'])
  self.assertEqual(v['historical_reviews'][0]['task'],'first-review');self.assertEqual(v['historical_checks'][0]['subject'],'output:old')
  self.assertEqual(v['selected_delivery']['state'],'accepted_recorded');self.assertEqual(raw,self.p.read_bytes())
  diagnosis=json.loads(self.cli('blockers',self.p,'--json').stdout)
  self.assertFalse(any(r['task']=='first-review' for r in diagnosis['blockers']))
  self.assertTrue(any(r['task']=='first-review' for r in diagnosis['historical']))
  status=self.cli('status',self.p).stdout;self.assertIn('first-review -> replacement-review',status);self.assertIn('current tasks',status);self.assertIn('Selected final: output:new / accepted_recorded',status);self.assertIn('Historical review observation:',status)
 def test_no_automatic_history_from_final_selection_alone(self):
  before=self.p.read_bytes();v=self.brief()
  self.assertEqual(v['waiting'][0]['task'],'first-review');self.assertFalse(v['historical_reviews'])
  self.assertEqual(before,self.p.read_bytes())
 def test_unreviewed_replacement_is_refused_without_writing(self):
  self.cli('mark',self.p,'replacement-review','--state','planned')
  before=self.p.read_bytes();self.supersede(ok=False);self.assertEqual(before,self.p.read_bytes())
 def test_secondary_aspect_drift_restores_old_wait_without_writes(self):
  self.supersede();(self.root/'portrait.txt').write_text('changed')
  before=self.p.read_bytes();v=self.brief()
  self.assertFalse(v['historical_reviews']);self.assertEqual(v['waiting'][0]['task'],'first-review')
  self.assertTrue(v['file_changes']);self.assertEqual(v['proposed_next']['kind'],'file_review');self.assertEqual(before,self.p.read_bytes())
 def test_new_rejection_restores_old_wait(self):
  self.supersede();self.observe('new','creative','rejected');v=self.brief()
  self.assertFalse(v['historical_reviews']);self.assertTrue(any(r['task']=='first-review' for r in v['waiting']))
  self.assertEqual(v['selected_delivery']['state'],'needs_review')
 def test_shared_subject_check_stays_current_and_dependencies_do_not_advance(self):
  self.cli('task',self.p,'independent-review','--label','Still review original','--requires','old','--check-kind','creative','--waiting-for','partner','--note','Separate partner decision')
  self.cli('task',self.p,'dependent','--label','Needs old review done','--after','first-review')
  self.supersede();v=self.brief()
  self.assertEqual(v['waiting'][0]['task'],'independent-review');self.assertTrue(v['needs_recheck'])
  self.assertFalse(any(r['id']=='dependent' for r in v['ready_tasks']))
 def test_fresh_process_keeps_exact_final_and_readable_history(self):
  self.supersede();before=self.p.read_bytes()
  r=subprocess.run([sys.executable,'-I',str(CLI),'brief',str(self.p)],cwd=tempfile.gettempdir(),capture_output=True,text=True)
  self.assertEqual(r.returncode,0,r.stderr);self.assertIn('Historical replaced reviews',r.stdout)
  self.assertIn('first-review replaced by replacement-review',r.stdout);self.assertIn('Selected final: output:new / accepted_recorded',r.stdout)
  self.assertEqual(before,self.p.read_bytes())
 def test_explicit_reopening_restores_wait(self):
  self.supersede();self.cli('mark',self.p,'first-review','--state','blocked','--evidence','Owner reopened original review')
  v=self.brief();self.assertFalse(v['historical_reviews'])
  self.assertEqual(v['waiting'][0]['reason'],'Owner reopened original review')
 def test_context_change_requires_explicit_reconfirmation(self):
  self.supersede();self.cli('describe',self.p,'--goal','Accepted revised film','--note','Changed scope')
  v=self.brief();self.assertFalse(v['historical_reviews']);self.assertTrue(v['waiting'])
  self.supersede();self.assertFalse(self.brief()['waiting'])
 def test_narrower_replacement_cannot_retire_a_pair_review(self):
  self.cli('task',self.p,'pair-review','--label','Review original pair','--requires','old','--requires','portrait','--check-kind','creative','--waiting-for','owner','--note','Pair required')
  self.cli('task',self.p,'single-review','--label','One accepted output','--requires','new','--check-kind','creative')
  self.cli('mark',self.p,'single-review','--state','done','--evidence','Accepted single output')
  before=self.p.read_bytes()
  self.cli('supersede-review',self.p,'pair-review','--with-task','single-review','--actor','operator','--note','Try incomplete coverage',ok=False)
  self.assertEqual(before,self.p.read_bytes())
 def test_historical_review_cannot_be_marked_done_using_replacement_approval(self):
  self.supersede();before=self.p.read_bytes()
  self.cli('mark',self.p,'first-review','--state','done','--evidence','Try to reuse replacement approval',ok=False)
  self.assertEqual(before,self.p.read_bytes())
