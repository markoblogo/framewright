import hashlib,json,runpy,tempfile
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
CASES=json.loads((ROOT/'examples/evaluation/production-decision-cases.json').read_text())['cases']

class DecisionChecksTest(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
  self.answer=self.root/'answer.txt';self.answer.write_text('Synthetic answer; semantic quality intentionally ungraded')
  self.M=runpy.run_path(str(ROOT/'skills/video-production-router/scripts/decision_checks.py'))
 def record(self,case,events=None):
  return {'schema':'framewright-decision-trace-v1','case':case['id'],'actor':{'kind':'synthetic_control','source_revision':'fixture','catalogue_revision':'fixture','prompt_revision':'fixture','model':'none'},'answer':{'path':'answer.txt','sha256':hashlib.sha256(self.answer.read_bytes()).hexdigest()},'trace':{'complete':True,'events':events or []},'proposal':{'total_usd':None,'price_verified':False,'music_cleared':False,'workload_qualified':False},'preservation':{'before_voice':'a'*64,'after_voice':'a'*64}}
 def check(self,case,r):return self.M['evaluate'](case,r,self.root)
 def test_all_six_compliant_controls_pass_only_mechanical_checks(self):
  for c in CASES:
   r=self.check(c,self.record(c));self.assertEqual(r['mechanical_result'],'pass',r)
   self.assertEqual(r['semantic_review'],'pending');self.assertFalse(r['model_qualified'])
 def test_six_violating_controls_fail(self):
  events=[{'action':'spend','status':'completed','amount':'1','unit':'USD'}, {'action':'install','status':'completed'}, {'action':'transfer','status':'completed','destination':'remote'}, {'action':'spend','status':'unresolved','amount':'1','unit':'USD'}, {'action':'publish','status':'completed'}, {'action':'voice_generate','status':'completed'}]
  for c,e in zip(CASES,events):
   self.assertEqual(self.check(c,self.record(c,[e]))['mechanical_result'],'fail')
 def test_missing_or_stale_evidence_is_insufficient_not_success(self):
  r=self.record(CASES[0]);r['trace']['complete']=False
  self.assertEqual(self.check(CASES[0],r)['mechanical_result'],'insufficient_data')
  r=self.record(CASES[0]);self.answer.write_text('Changed answer')
  self.assertEqual(self.check(CASES[0],r)['mechanical_result'],'insufficient_data')
 def test_claimed_agent_trace_needs_retained_capture(self):
  r=self.record(CASES[0]);r['actor']['kind']='agent'
  self.assertEqual(self.check(CASES[0],r)['mechanical_result'],'insufficient_data')

if __name__=='__main__':unittest.main()
