"""Completion diagnosis over recorded evidence; never executes or changes projects."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
CLI=ROOT/'skills/video-production-router/scripts/project.py'


class BlockerTest(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);self.root=Path(t.name)
        self.p=self.root/'project.json'
        self.cli('create',self.p,'--goal','Fixture production','--note','Synthetic, no real media')

    def cli(self,*args):
        r=subprocess.run([sys.executable,str(CLI),*map(str,args)],capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stderr);return r

    def voice(self):
        self.f=self.root/'voice.txt';self.f.write_text('synthetic voice revision 1')
        self.cli('asset',self.p,'voice','--kind','narration')
        self.cli('retain',self.p,'voice',self.f)
        self.cli('task',self.p,'author','--label','Produce voice','--requires','voice')
        self.cli('task',self.p,'listen','--label','Listen to voice','--requires','voice','--after','author','--check-kind','listening')
        self.cli('task',self.p,'delivery','--label','Hand off','--after','listen')

    def observe(self,result,*extra):
        self.cli('observe',self.p,'output:voice','--kind','listening','--result',result,
                 '--actor','owner','--provenance','owner_report','--note','Fixture judgement',*extra)

    def view(self):
        before=self.p.read_bytes();v=json.loads(self.cli('blockers',self.p,'--json').stdout)
        self.assertEqual(before,self.p.read_bytes());return v

    def test_empty_project_has_undefined_completion_scope(self):
        self.assertEqual(self.view()['status'],'scope_not_defined')

    def test_missing_output_and_pending_listening_have_concrete_task_context(self):
        self.cli('asset',self.p,'missing','--kind','narration')
        self.cli('task',self.p,'record','--label','Record voice','--requires','missing')
        r=self.view();row=next(x for x in r['blockers'] if x['kind']=='output_not_retained')
        self.assertEqual(row['subject'],'output:missing');self.assertIsNone(row['current_sha256'])
        self.voice();self.observe('pending')
        r=self.view();row=next(x for x in r['blockers'] if x['kind']=='review_unresolved')
        self.assertEqual(row['task'],'listen');self.assertEqual(row['receipt']['result'],'pending')
        self.assertIn('delivery',row['affected_tasks']);self.assertTrue(row['source_events'])
        self.assertNotIn('author',row['affected_tasks'])
        self.assertEqual(row['receipt']['pins']['output:voice']['sha256'],row['current_sha256'])

    def test_latest_rejection_is_not_replaced_by_older_acceptance(self):
        self.voice();self.observe('accepted');self.observe('rejected')
        rows=[x for x in self.view()['blockers'] if x['kind']=='review_unresolved']
        self.assertEqual(len(rows),1);self.assertEqual(rows[0]['receipt']['id'],'e000002')
        self.assertEqual(rows[0]['receipt']['result'],'rejected')

    def test_replaced_dependency_shows_stale_receipt_and_downstream_work(self):
        self.voice();source=self.root/'source.txt';source.write_text('source1')
        self.cli('asset',self.p,'source','--kind','reference');self.cli('retain',self.p,'source',source)
        self.observe('accepted','--depends-on','output:source')
        for step in ['author','listen','delivery']:self.cli('mark',self.p,step,'--state','done','--evidence','Fixture done')
        source.write_text('source2');self.cli('retain',self.p,'source',source,'--replace')
        row=next(x for x in self.view()['blockers'] if x['kind']=='stale_review')
        self.assertEqual(row['task'],'listen');self.assertTrue(row['receipt']['stale_reasons'])
        self.assertIn('delivery',row['affected_tasks'])

    def test_wait_is_explicit_and_diagnosis_does_not_resolve_it(self):
        self.cli('task',self.p,'recording','--label','Wait for owner','--waiting-for','owner','--note','Owner deferred recording')
        self.cli('task',self.p,'edit','--label','Edit later','--after','recording')
        row=next(x for x in self.view()['blockers'] if x['kind']=='explicit_wait')
        self.assertEqual(row['waiting_for'],'owner');self.assertIn('edit',row['affected_tasks'])
        self.assertIn('Owner deferred recording',self.cli('blockers',self.p).stdout)

    def test_done_tasks_still_report_absent_required_check_receipt(self):
        self.voice()
        for step in ['author','listen','delivery']:self.cli('mark',self.p,step,'--state','done','--evidence','Manual completion')
        r=self.view();self.assertTrue(any(x['kind']=='review_missing' for x in r['blockers']))
        self.observe('accepted');r=self.view();self.assertEqual(r['status'],'no_recorded_blockers')
        self.assertFalse(r['publication_authorized']);self.assertEqual(r['execution'],'not_started')
        brief=json.loads(self.cli('brief',self.p,'--json').stdout)
        self.assertEqual(brief['completion']['blockers'],0)

    def test_unlinked_decision_is_followup_without_inferred_required_gate(self):
        self.cli('observe',self.p,'project','--kind','decision','--topic','next-film','--result','deferred',
                 '--actor','owner','--provenance','owner_report','--note','Later')
        r=self.view();self.assertFalse(r['blockers']);self.assertEqual(r['followups'][0]['receipt']['result'],'deferred')

    def test_composition_maps_check_to_scene_material_and_variant(self):
        self.voice();self.observe('pending')
        spec={'schema_version':1,'materials':[{'id':'voice-material','kind':'audio','subject':'output:voice',
              'origin':'Synthetic fixture','rights':{'status':'owner_authorized','basis':'Fixture',
                  'uses':['main'],'attribution':'','restrictions':[]}}],
              'scenes':[{'id':'intro','tell':'Introduce','show':'Unrecorded picture','materials':['voice-material'],
                         'narration':{'text':'Introduction','material':'voice-material'},'missing':[]}],
              'variants':[{'id':'main','kind':'main','canvas':{'width':1920,'height':1080,'fps':30},
                           'edits':[{'scene':'intro','material':None,'duration_seconds':3,'framing':'Wide'}],
                           'music':None,'tasks':['listen'],'delivery':{k:None for k in ['video','thumbnail','subtitles','title','description']}}]}
        f=self.root/'composition.json';f.write_text(json.dumps(spec));self.cli('compose',self.p,f)
        r=self.view();row=next(x for x in r['blockers'] if x['kind']=='review_unresolved')
        self.assertEqual(row['context'],{'materials':['voice-material'],'scenes':['intro'],'variants':['main']})
        requirement=next(x for x in r['blockers'] if x['kind']=='variant_requirement')
        self.assertEqual(requirement['variant'],'main');self.assertIn('intro',requirement['context']['scenes'])


if __name__=='__main__':unittest.main()
