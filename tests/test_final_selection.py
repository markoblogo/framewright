"""A final selection never erases unrelated waits or revives stale approval."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
CLI=Path(__file__).resolve().parents[1]/'skills/video-production-router/scripts/project.py'
class FinalSelectionTest(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.p=self.root/'project.json'
  self.cli('create',self.p,'--goal','Film','--note','Test')
  self.f=self.root/'film.txt';self.f.write_text('fixture')
  self.cli('asset',self.p,'film','--kind','video');self.cli('retain',self.p,'film',self.f)
 def cli(self,*args,ok=True):
  p=subprocess.run([sys.executable,str(CLI),*map(str,args)],capture_output=True,text=True)
  self.assertEqual(p.returncode==0,ok,p.stderr);return p
 def approve(self):
  for kind,result in [('technical','pass'),('listening','accepted'),('creative','accepted')]:
   self.cli('observe',self.p,'output:film','--kind',kind,'--result',result,'--actor','owner','--provenance','owner_report','--note','Recorded review')
 def select(self,**kw):return self.cli('select-final',self.p,'output:film','--actor','owner','--note','Explicit choice',**kw)
 def brief(self):return json.loads(self.cli('brief',self.p,'--json').stdout)
 def test_selected_delivery_precedes_old_wait_without_cancelling_it(self):
  self.cli('task',self.p,'old','--label','Old pilot','--waiting-for','owner','--note','Review old pilot')
  self.approve();self.select();before=self.p.read_bytes();v=self.brief()
  self.assertEqual(v['selected_delivery']['state'],'accepted_recorded');self.assertEqual(v['selected_delivery']['subject'],'output:film')
  self.assertEqual(v['counts']['waiting'],1);self.assertEqual(v['proposed_next']['kind'],'selected_delivery_recorded')
  self.assertEqual(v['completion']['status'],'recorded_blockers');self.assertEqual(before,self.p.read_bytes())
 def test_unreviewed_selection_does_not_write(self):
  before=self.p.read_bytes();self.select(ok=False);self.assertEqual(before,self.p.read_bytes())
 def test_changed_bytes_invalidate_selection_without_reviving_old_final(self):
  self.approve();self.select();self.f.write_text('changed')
  v=self.brief();self.assertEqual(v['selected_delivery']['state'],'needs_review');self.assertEqual(v['proposed_next']['kind'],'file_review')
 def test_new_rejection_invalidates_selection(self):
  self.approve();self.select();self.cli('observe',self.p,'output:film','--kind','creative','--result','rejected','--actor','owner','--provenance','owner_report','--note','Changed decision')
  v=self.brief();self.assertEqual(v['selected_delivery']['state'],'needs_review');self.assertEqual(v['proposed_next']['kind'],'evidence_review')
 def test_later_unreviewed_final_never_falls_back_to_earlier_choice(self):
  self.approve();self.select();g=self.root/'second.txt';g.write_text('second')
  self.cli('asset',self.p,'second','--kind','video');self.cli('retain',self.p,'second',g)
  self.cli('observe',self.p,'output:second','--kind','decision','--topic','final-selection','--result','accepted','--actor','owner','--provenance','owner_report','--note','New selection')
  v=self.brief();self.assertEqual(v['selected_delivery']['subject'],'output:second');self.assertEqual(v['selected_delivery']['state'],'needs_review')
 def test_drifted_dependency_of_review_blocks_selection(self):
  q=self.root/'qa.txt';q.write_text('report');self.cli('asset',self.p,'qa','--kind','report');self.cli('retain',self.p,'qa',q)
  self.approve();self.cli('observe',self.p,'output:film','--kind','technical','--result','pass','--actor','operator','--provenance','supplied_report','--note','Bound report','--depends-on','output:qa')
  q.write_text('changed report');self.select(ok=False)
 def test_final_selection_cannot_accept_still_or_project(self):
  self.approve();self.cli('select-final',self.p,'project','--actor','owner','--note','No file',ok=False)
 def test_selected_final_does_not_hide_an_unrelated_file_problem(self):
  self.approve();self.select();q=self.root/'other.txt';q.write_text('other');self.cli('retain',self.p,'other',q,'--input');q.unlink()
  v=self.brief();self.assertEqual(v['selected_delivery']['state'],'accepted_recorded');self.assertEqual(v['proposed_next']['kind'],'file_review')
 def test_selected_final_keeps_a_new_ready_task_as_the_next_proposal(self):
  self.approve();self.select()
  self.cli('task',self.p,'prepare-kit','--label','Prepare accepted film kit','--note','New authorised follow-up')
  before=self.p.read_bytes();v=self.brief()
  self.assertEqual(v['selected_delivery']['state'],'accepted_recorded')
  self.assertEqual(v['proposed_next']['kind'],'ready_task')
  self.assertEqual(v['proposed_next']['task'],'prepare-kit')
  self.assertEqual(v['execution'],'not_started');self.assertEqual(before,self.p.read_bytes())
 def test_fresh_process_handoff_exposes_exact_retained_file_and_reviews(self):
  self.approve();self.select();before=self.p.read_bytes()
  result=subprocess.run([sys.executable,'-I',str(CLI),'brief',str(self.p),'--json','--limit','1'],cwd=tempfile.gettempdir(),capture_output=True,text=True)
  self.assertEqual(result.returncode,0,result.stderr);v=json.loads(result.stdout)
  selected=v['selected_delivery'];pin=selected['retained_file']
  self.assertEqual((self.p.parent/pin['path']).resolve(),self.f.resolve())
  self.assertEqual(pin['bytes'],len(self.f.read_bytes()))
  self.assertEqual(pin['sha256'],selected['sha256'])
  self.assertEqual(set(selected['reviews']),{'technical','listening','creative'})
  self.assertTrue(all(selected['reviews'].values()))
  self.assertEqual(v['execution'],'not_started');self.assertEqual(before,self.p.read_bytes())
 def test_selected_review_scope_is_visible_even_with_small_brief_limit(self):
  self.approve()
  self.cli('observe',self.p,'output:film','--kind','technical','--result','pass','--actor','operator','--provenance','operator_observation','--note','Technical check only; commercial narration rights not cleared')
  self.select();text=self.cli('brief',self.p,'--limit','1').stdout
  self.assertIn('Selected-version recorded reviews',text)
  self.assertIn('commercial narration rights not cleared',text)
  self.assertIn('Task constraints',text)
 def test_pending_provider_rights_remain_visible_without_revoking_picture_acceptance(self):
  self.approve();self.select()
  self.cli('observe',self.p,'output:film','--kind','provider','--topic','commercial-use','--result','pending','--actor','operator','--provenance','supplied_report','--note','Commercial narration permission is unresolved')
  before=self.p.read_bytes();v=self.brief()
  self.assertEqual(v['selected_delivery']['state'],'accepted_recorded')
  record=v['selected_delivery']['other_observations'][0]
  self.assertEqual(record['kind'],'provider');self.assertEqual(record['result'],'pending')
  text=self.cli('brief',self.p,'--limit','1').stdout
  self.assertIn('Commercial narration permission is unresolved',text)
  self.assertIn('not clearance',text);self.assertEqual(before,self.p.read_bytes())
