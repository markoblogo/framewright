"""Derived status through the public CLI; no media or network."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
CLI=ROOT/'skills/video-production-router/scripts/project.py'
class SummaryTest(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.p=self.root/'project.json'
  self.cli('create',self.p,'--goal','PRIVATE_GOAL','--note','PRIVATE_NOTE')
  self.f=self.root/'PRIVATE_FILE.txt';self.f.write_text('first')
  self.cli('asset',self.p,'film','--kind','video');self.cli('retain',self.p,'film',self.f)
 def cli(self,*args,ok=True):
  p=subprocess.run([sys.executable,str(CLI),*map(str,args)],capture_output=True,text=True);self.assertEqual(p.returncode==0,ok,p.stderr);return p
 def observe(self,kind,result,*args):
  self.cli('observe',self.p,'output:film','--kind',kind,'--result',result,'--actor','PRIVATE_ACTOR','--provenance','owner_report','--note','PRIVATE_NOTE',*args)
 def test_current_summary_does_not_resurrect_approval_after_file_drift(self):
  self.observe('creative','accepted');self.observe('publication','published','--url','https://example.test/video?secret=HIDDEN','--visibility','unknown')
  before=self.p.read_bytes();self.f.write_text('changed')
  view=json.loads(self.cli('summary',self.p,'--json').stdout)
  row=view['files'][0];self.assertEqual(row['state'],'changed');self.assertTrue(row['observations'][0]['stale']);self.assertEqual(before,self.p.read_bytes())
 def test_public_projection_is_allowlisted_and_drift_check_does_not_write(self):
  self.observe('creative','accepted');self.observe('creative','rejected')
  self.observe('publication','published','--url','https://example.test/video?secret=HIDDEN','--visibility','unknown')
  self.cli('summary',self.p,'--public','--json',ok=False)
  args=['summary',self.p,'--public','--title','Approved public title','--include','output:film','--json']
  text=self.cli(*args).stdout
  for private in ('PRIVATE','HIDDEN','example.test','actor'):self.assertNotIn(private,text)
  view=json.loads(text);self.assertEqual([r['result'] for r in view['files'][0]['observations']],['rejected','published'])
  out=self.root/'STATUS.json';self.cli(*args,'--output',out)
  self.cli(*args,'--output',out,'--check')
  self.f.unlink();before=out.read_bytes();self.cli(*args,'--output',out,'--check',ok=False);self.assertEqual(before,out.read_bytes())
  for protected in (self.p,self.f):self.cli(*args,'--output',protected,'--replace',ok=False)
 def test_public_url_strips_query_and_missing_file_stales_publication(self):
  self.observe('publication','published','--url','https://example.test/video?secret=HIDDEN#private','--visibility','public')
  self.f.unlink()
  v=json.loads(self.cli('summary',self.p,'--public','--title','Public','--include','output:film','--json').stdout)
  row=v['files'][0];self.assertEqual(row['state'],'missing');self.assertTrue(row['observations'][0]['stale']);self.assertEqual(row['observations'][0]['url'],'https://example.test/video')
 def test_unreadable_file_is_unavailable_not_changed_or_missing(self):
  self.f.chmod(0)
  try:
   if __import__('os').access(self.f,__import__('os').R_OK):self.skipTest('Runtime can read mode-000 files')
   v=json.loads(self.cli('summary',self.p,'--json').stdout)
   self.assertEqual(v['files'][0]['state'],'unavailable')
  finally:self.f.chmod(0o600)
 def test_public_youtube_watch_url_keeps_video_identity_only(self):
  self.observe('publication','published','--url','https://www.youtube.com/watch?v=ABCDEFGHIJK&secret=HIDDEN#PRIVATE','--visibility','public')
  v=json.loads(self.cli('summary',self.p,'--public','--title','Public','--include','output:film','--json').stdout)
  self.assertEqual(v['files'][0]['observations'][0]['url'],'https://www.youtube.com/watch?v=ABCDEFGHIJK')
 def test_local_summary_includes_latest_project_approval_without_public_leak(self):
  for result in ['accepted','rejected']:
   self.cli('observe',self.p,'project','--kind','decision','--topic','PRIVATE_DIRECTION','--result',result,'--actor','owner','--provenance','owner_report','--note','PRIVATE_NOTE')
  local=json.loads(self.cli('summary',self.p,'--json').stdout)
  self.assertEqual([r['result'] for r in local['project_decisions']],['rejected'])
  public=json.loads(self.cli('summary',self.p,'--public','--title','Public','--include','output:film','--json').stdout)
  self.assertEqual(public['project_decisions'],[])
