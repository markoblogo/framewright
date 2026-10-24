"""Hypothesis → exact master/upload → supplied outcome, through project CLI."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1];CLI=ROOT/'skills/video-production-router/scripts/project.py'
class ContentTest(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.p=self.root/'project.json'
  self.cli('create',self.p,'--goal','Pilot','--note','Private')
  self.source=self.root/'source.txt';self.source.write_text('Trends supplied by owner');self.cli('retain',self.p,'trends',self.source,'--input')
  self.cli('asset',self.p,'film','--kind','video')
 def cli(self,*args,ok=True):
  p=subprocess.run([sys.executable,str(CLI),*map(str,args)],capture_output=True,text=True);self.assertEqual(p.returncode==0,ok,p.stderr);return p
 def spec(self,name,value):
  p=self.root/(name+'.json');p.write_text(json.dumps(value));return p
 def hypothesis(self):
  return self.cli('hypothesis',self.p,self.spec('idea',{'id':'cash','statement':'Animated cash gap earns attention','audience':'Founders','format':'short','target':'output:film','source':{'kind':'youtube_trends','subject':'input:trends'}}),'--actor','owner','--provenance','owner_report')
 def test_hypothesis_preserves_unknown_outcomes_and_actual_declaration_timing(self):
  self.hypothesis();v=json.loads(self.cli('results',self.p,'--json').stdout)
  self.assertEqual(v['hypotheses'][0]['timing'],'before_retained_master');self.assertEqual(v['hypotheses'][0]['publications'],[])
  before=self.p.read_bytes();self.hypothesis();self.assertEqual(before,self.p.read_bytes())
 def publish(self):
  f=self.root/'master.txt';f.write_text('master');self.cli('retain',self.p,'film',f)
  self.cli('observe',self.p,'output:film','--kind','publication','--result','published','--url','https://example.test/short','--visibility','public','--actor','owner','--provenance','owner_report','--note','Owner supplied URL')
  self.pub=json.loads(self.p.read_text())['journal'][-1]['id']
  evidence=self.root/'analytics.txt';evidence.write_text('Owner supplied snapshot');self.cli('retain',self.p,'analytics',evidence,'--input')
 def outcome(self,spec,ok=True):
  return self.cli('outcome',self.p,self.spec('outcome',spec),'--actor','owner','--provenance','owner_report',ok=ok)
 def test_snapshots_keep_zero_distinct_from_unknown_and_allow_shorts_replays(self):
  self.hypothesis();self.publish()
  s={'id':'day2','hypothesis':'cash','publication':self.pub,'evidence':'input:analytics','as_of':'2026-10-24T12:00:00Z','published_at':'2026-10-22T12:00:00Z','window':'lifetime','metrics':{'views':0,'average_percentage_viewed':135,'estimated_revenue':0,'currency':'USD','monetization':'enabled'}}
  self.outcome(s)
  v=json.loads(self.cli('results',self.p,'--json','--compare-age-hours','48').stdout);p=v['hypotheses'][0]['publications'][0];m=p['snapshots'][0]['metrics']
  self.assertEqual(m['views'],0);self.assertIsNone(m['average_view_duration_seconds']);self.assertEqual(m['estimated_revenue'],0);self.assertEqual(p['selected_snapshot'],'day2')
  self.assertEqual(p['snapshots'][0]['age_hours'],48)
  before=self.p.read_bytes();self.outcome(s);self.assertEqual(before,self.p.read_bytes())
 def test_unknown_upload_age_is_excluded_and_changed_master_stales_snapshot(self):
  self.hypothesis();self.publish()
  spec={'id':'unknown-age','hypothesis':'cash','publication':self.pub,'evidence':'input:analytics','as_of':'2026-10-24T12:00:00Z','window':'lifetime','metrics':{}}
  self.outcome(spec)
  p=json.loads(self.cli('results',self.p,'--json','--compare-age-hours','48').stdout)['hypotheses'][0]['publications'][0]
  self.assertEqual(p['snapshots'][0]['comparison'],'upload_time_unknown');self.assertIsNone(p['snapshots'][0]['metrics']['estimated_revenue']);self.assertIsNone(p['selected_snapshot'])
  master=self.root/'master.txt';master.write_text('new cut');self.cli('retain',self.p,'film',master,'--replace')
  p=json.loads(self.cli('results',self.p,'--json').stdout)['hypotheses'][0]['publications'][0]
  self.assertTrue(p['snapshots'][0]['stale']);self.outcome({**spec,'id':'wrong-master'},ok=False)
 def test_outcome_rejects_bad_currency_time_and_metrics_without_mutation(self):
  self.hypothesis();self.publish()
  spec={'id':'bad','hypothesis':'cash','publication':self.pub,'evidence':'input:analytics','as_of':'2026-10-24T12:00:00Z','window':'lifetime','metrics':{}}
  cases=[{'metrics':{'views':True}},{'metrics':{'views':-1}},{'metrics':{'estimated_revenue':0}},{'as_of':'2026-10-24'},{'published_at':'2026-10-25T00:00:00Z'},{'metrics':{'rpm':float('nan'),'currency':'USD'}},{'publication':'e000001'}]
  before=self.p.read_bytes()
  for change in cases:self.outcome({**spec,**change},ok=False);self.assertEqual(before,self.p.read_bytes())
 def test_removed_upload_keeps_historical_snapshots_but_cannot_receive_new_ones(self):
  self.publish();self.hypothesis()
  self.assertEqual(json.loads(self.cli('results',self.p,'--json').stdout)['hypotheses'][0]['timing'],'retrospective')
  spec={'id':'historic','hypothesis':'cash','publication':self.pub,'evidence':'input:analytics','as_of':'2026-10-24T12:00:00Z','window':'unknown','metrics':{'views':22}}
  self.outcome(spec)
  self.cli('observe',self.p,'output:film','--kind','publication','--result','removed','--url','https://example.test/short','--actor','owner','--provenance','owner_report','--note','Removed')
  pubs=json.loads(self.cli('results',self.p,'--json').stdout)['hypotheses'][0]['publications']
  self.assertEqual(pubs[0]['publication_state'],'removed');self.assertEqual(pubs[0]['snapshots'][0]['metrics']['views'],22);self.outcome({**spec,'id':'after-removal'},ok=False)
 def test_append_preserves_different_windows_and_currencies_without_ranking(self):
  self.hypothesis();self.publish()
  base={'hypothesis':'cash','publication':self.pub,'evidence':'input:analytics','as_of':'2026-10-24T12:00:00Z','published_at':'2026-10-22T12:00:00Z','window':'lifetime'}
  self.outcome({**base,'id':'usd','metrics':{'views':100,'estimated_revenue':1,'currency':'USD'}})
  self.outcome({**base,'id':'eur','metrics':{'views':101,'estimated_revenue':2,'currency':'EUR'}})
  self.outcome({**base,'id':'period','window':'period','period_start':'2026-10-23T12:00:00Z','period_end':'2026-10-24T12:00:00Z','metrics':{'views':50}})
  v=json.loads(self.cli('results',self.p,'--json','--compare-age-hours','48').stdout)
  snaps=v['hypotheses'][0]['publications'][0]['snapshots'];self.assertEqual(len(snaps),3);self.assertEqual([s['metrics']['currency'] for s in snaps[:2]],['USD','EUR']);self.assertEqual(snaps[2]['comparison'],'window_not_lifetime')
  self.assertNotIn('winner',v);self.cli('results',self.p,'--compare-age-hours','nan',ok=False)
 def test_results_expose_revision_and_provenance_and_reject_conflicting_upload_time(self):
  self.hypothesis();self.publish()
  self.cli('observe',self.p,'project','--kind','decision','--topic','content-hypothesis:cash','--result','accepted','--actor','owner','--provenance','owner_report','--note','Owner accepted concept')
  spec={'id':'provenance','hypothesis':'cash','publication':self.pub,'evidence':'input:analytics','as_of':'2026-10-24T12:00:00Z','published_at':'2026-10-22T12:00:00Z','window':'lifetime','metrics':{'views':10}}
  self.outcome(spec)
  p=json.loads(self.cli('results',self.p,'--json').stdout)['hypotheses'][0]['publications'][0]
  self.assertEqual(len(p['master_sha256']),64);self.assertEqual(p['snapshots'][0]['provenance'],'owner_report');self.assertEqual(p['snapshots'][0]['evidence_subject'],'input:analytics')
  self.outcome({**spec,'id':'conflicting-age','published_at':'2026-10-23T12:00:00Z'},ok=False)
