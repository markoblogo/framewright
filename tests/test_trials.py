import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

BASE=Path(__file__).resolve().parents[1]/'skills/video-production-router/scripts'


class TrialsTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.project=self.root/'project.json'
        self.cli('project.py','create',self.project,'--goal','Synthetic trial','--note','No media production')
        for ident in ['source','log-a','log-b']:
            path=self.root/(ident+'.txt');path.write_text('Synthetic '+ident)
            self.cli('project.py','retain',self.project,ident,path,'--input')
        for ident in ['baseline','candidate']:
            path=self.root/(ident+'.txt');path.write_text('Synthetic output '+ident)
            self.cli('project.py','asset',self.project,ident,'--kind','text')
            self.cli('project.py','retain',self.project,ident,path)
        self.spec={'id':'mouth-test','tool':'rhubarb-lip-sync','capability':'editable mouth timing',
            'question':'Can the candidate preserve rests without excess switching?',
            'sources':['input:source'],
            'baseline':{'method':'Authored timing','settings':{'fps':24}},
            'candidate':{'method':'Rhubarb cues','settings':{'fps':24}},
            'criteria':[{'id':'rests','kind':'technical','description':'Mouth closed in pauses'},
                        {'id':'natural','kind':'creative','description':'No distracting mouth chatter'}],
            'limits':{'max_cost':0,'currency':'USD','max_seconds':60}}
        self.spec_path=self.root/'spec.json';self.spec_path.write_text(json.dumps(self.spec))
        self.card=self.root/'trial.json';self.subject='output:trial:mouth-test'

    def cli(self,script,*args,ok=True):
        r=subprocess.run([sys.executable,str(BASE/script),*map(str,args)],capture_output=True,text=True,timeout=30)
        self.assertEqual(r.returncode==0,ok,r.stderr);return r

    def plan(self):
        return self.cli('trials.py','plan',self.project,self.spec_path,'--output',self.card,'--actor','fixture')

    def results(self,ident='attempt-1',cost=0):
        r={'id':ident}
        for arm,log in [('baseline','log-a'),('candidate','log-b')]:
            r[arm]={'output':'output:'+arm,'sources':['input:source'],'environment':None,
                    'elapsed_seconds':10,'cost':{'amount':cost,'currency':'USD'},
                    'checks':{c['id']:{'result':'pass','note':'Synthetic supplied observation',
                              'evidence':['input:'+log]} for c in self.spec['criteria']}}
        return r

    def retain_results(self,r,ident='run-report'):
        path=self.root/(ident+'.json');path.write_text(json.dumps(r))
        self.cli('project.py','retain',self.project,ident,path,'--input');return 'input:'+ident

    def compare(self,result_subject,folder='comparison',ok=True):
        return self.cli('trials.py','compare',self.project,self.subject,result_subject,
                        '--output',self.root/folder,'--actor','fixture','--provenance','supplied_report',ok=ok)

    def test_plan_reuses_journal_and_comparison_has_real_pins_and_no_approval(self):
        self.plan();card=json.loads(self.card.read_text())
        self.assertEqual(card['pins']['input:source']['bytes'],len('Synthetic source'))
        self.assertFalse(card['execution_authorized'])
        results=self.retain_results(self.results());self.compare(results)
        report=json.loads((self.root/'comparison/comparison.json').read_text())
        self.assertIn('input:run-report',report['pins'])
        self.assertIn('output:baseline',report['pins']);self.assertIn('output:candidate',report['pins'])
        self.assertEqual(report['qualification'],'not_promoted')
        self.assertTrue((self.root/'comparison/review.html').is_file())
        self.assertTrue((self.root/'comparison/comparison.md').is_file())
        current=json.loads(self.project.read_text())
        self.assertTrue(any(x['topic']=='trial:mouth-test' for x in current['journal']))
        state=json.loads(self.cli('trials.py','status',self.project,self.subject,'--json').stdout)
        self.assertIn('environment', ' '.join(state['blockers']).lower())
        self.assertFalse(state['eligible_for_manual_scoped_update'])

    def test_changed_or_replaced_source_never_resurrects_old_trial(self):
        self.plan();r=self.retain_results(self.results());self.compare(r)
        source=self.root/'source.txt';source.write_text('Changed fixture source')
        state=json.loads(self.cli('trials.py','status',self.project,self.subject,'--json').stdout)
        self.assertEqual(state['state'],'stale')
        before=self.project.read_bytes()
        self.compare(r,'bad-comparison',ok=False)
        self.assertFalse((self.root/'bad-comparison').exists());self.assertEqual(before,self.project.read_bytes())
        self.cli('project.py','retain',self.project,'source',source,'--input','--replace')
        state=json.loads(self.cli('trials.py','status',self.project,self.subject,'--json').stdout)
        self.assertEqual(state['state'],'stale');self.assertFalse(state['eligible_for_manual_scoped_update'])

    def environment(self):
        payload={'id':'synthetic-environment','platforms':[],'architectures':[],
                 'min_memory_gib':0,'min_free_disk_gib':0,'programs':[],'models':[],
                 'manual_checks':[],'rights':{'status':'allowed','basis':'Synthetic fixture only'},
                 'cost':{'status':'free_local','amount':0,'currency':'USD','basis':'Fixture has no provider calls'}}
        manifest=self.root/'environment-manifest.json';manifest.write_text(json.dumps(payload))
        path=self.root/'environment.json'
        self.cli('environment.py',manifest,'--output',path)
        self.cli('project.py','retain',self.project,'environment',path,'--input')
        return 'input:environment'

    def test_baseline_failure_does_not_disqualify_passed_candidate_but_owner_review_is_required(self):
        self.plan();env=self.environment();r=self.results()
        for row in [r['baseline'],r['candidate']]:row['environment']=env
        r['baseline']['checks']['rests']['result']='fail'
        source=self.retain_results(r);self.compare(source)
        state=lambda:json.loads(self.cli('trials.py','status',self.project,self.subject,'--json').stdout)
        self.assertEqual(state()['state'],'ready_for_owner_review')
        self.assertFalse(state()['eligible_for_manual_scoped_update'])
        report=json.loads((self.root/'comparison/comparison.json').read_text())['subject']
        self.cli('project.py','observe',self.project,report,'--kind','creative','--result','accepted',
                 '--actor','fixture-owner','--provenance','owner_report','--topic','trial-review','--note','Synthetic acceptance')
        final=state();self.assertTrue(final['eligible_for_manual_scoped_update'])
        self.assertEqual(final['proposed_scope']['capability'],self.spec['capability'])
        self.assertEqual(final['qualification'],'not_promoted')
        self.cli('project.py','observe',self.project,report,'--kind','creative','--result','pending',
                 '--actor','fixture-owner','--provenance','owner_report','--topic','trial-review','--note','Reopen fixture review')
        self.assertFalse(state()['eligible_for_manual_scoped_update'])

    def test_budget_unknown_zero_and_failed_candidate_are_not_silently_promoted(self):
        self.plan();env=self.environment()
        for n,change in enumerate(['over-budget','unknown','failure','currency']):
            r=self.results('attempt-'+str(n))
            for row in [r['baseline'],r['candidate']]:row['environment']=env
            if change=='over-budget':r['candidate']['cost']['amount']=1
            elif change=='unknown':r['candidate']['cost']['amount']=None
            elif change=='failure':r['candidate']['checks']['rests']['result']='fail'
            else:r['candidate']['cost']={'amount':100,'currency':'EUR'}
            source=self.retain_results(r,'report-'+str(n));self.compare(source,'compare-'+str(n))
            state=json.loads(self.cli('trials.py','status',self.project,self.subject,'--json').stdout)
            self.assertEqual(state['state'],'needs_review');self.assertFalse(state['eligible_for_manual_scoped_update'])
            report=json.loads((self.root/('compare-'+str(n))/'comparison.json').read_text())
            self.assertEqual(report['arms']['baseline']['cost']['amount'],0)
            if change=='unknown':self.assertIsNone(report['arms']['candidate']['cost']['amount'])
            if change=='currency':self.assertFalse(any('total cost' in b for b in state['blockers']))

    def test_mismatched_sources_nan_missing_evidence_and_duplicate_attempt_do_not_mutate_project(self):
        self.plan()
        for n,change in enumerate(['source','nan','evidence']):
            r=self.results('bad-'+str(n))
            if change=='source':r['candidate']['sources']=['input:log-a']
            elif change=='nan':r['candidate']['elapsed_seconds']=float('nan')
            else:r['candidate']['checks']['rests']['evidence']=[]
            source=self.retain_results(r,'bad-report-'+str(n));before=self.project.read_bytes()
            self.compare(source,'bad-'+str(n),ok=False)
            self.assertFalse((self.root/('bad-'+str(n))).exists());self.assertEqual(before,self.project.read_bytes())
        r=self.retain_results(self.results());self.compare(r)
        before=self.project.read_bytes();self.compare(r,'duplicate',ok=False)
        self.assertEqual(before,self.project.read_bytes());self.assertFalse((self.root/'duplicate').exists())

    def test_review_pack_escapes_notes_and_copied_media_changes_stale_the_result(self):
        self.plan();r=self.results();r['candidate']['checks']['natural']['note']='<script>alert(1)</script>'
        result=self.retain_results(r);self.compare(result)
        html=(self.root/'comparison/review.html').read_text()
        self.assertNotIn('<script>',html);self.assertIn('&lt;script&gt;',html)
        (self.root/'comparison/candidate.txt').write_text('Changed copy')
        state=json.loads(self.cli('trials.py','status',self.project,self.subject,'--json').stdout)
        self.assertEqual(state['state'],'stale')


if __name__=='__main__':unittest.main()
