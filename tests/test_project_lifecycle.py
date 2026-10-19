"""Local production memory through the public CLI; no real media or network."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / 'skills/video-production-router/scripts/project.py'

class LifecycleTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.project = self.root / 'project.json'

    def cli(self, *args, ok=True):
        p = subprocess.run([sys.executable, str(CLI), *map(str, args)], capture_output=True, text=True)
        self.assertEqual(p.returncode == 0, ok, p.stderr)
        return p

    def data(self):
        return json.loads(self.project.read_text())

    def status(self):
        return json.loads(self.cli('resume', self.project, '--json').stdout)

    def test_repinned_receipt_dependency_reopens_linked_check_and_delivery(self):
        self.cli('create',self.project,'--goal','Dependent QA','--note','Synthetic fixture')
        files={}
        for name in ['source','final']:
            f=self.root/(name+'.txt');f.write_text('first '+name);files[name]=f
            self.cli('asset',self.project,name,'--kind','video-export')
            self.cli('retain',self.project,name,f)
        self.cli('task',self.project,'author','--label','Author final','--requires','final')
        self.cli('task',self.project,'check-final','--label','Check final','--requires','final',
                 '--after','author','--check-kind','technical')
        self.cli('task',self.project,'delivery','--label','Deliver','--after','check-final')
        self.observe('output:final','technical','pass','--depends-on','output:source')
        for step in ['author','check-final','delivery']:
            self.cli('mark',self.project,step,'--state','done','--evidence','Fixture check')
        self.assertTrue(self.status()['technical_handoff_recorded'])
        files['source'].write_text('replacement source')
        self.cli('retain',self.project,'source',files['source'],'--replace')
        result=self.status();states={step['id']:step['state'] for step in self.data()['steps']}
        self.assertEqual(states['author'],'done')
        self.assertEqual(states['check-final'],'planned')
        self.assertEqual(states['delivery'],'planned')
        self.assertFalse(result['technical_handoff_recorded'])
        self.assertIn('check-final',result['evidence_blockers'])
        self.cli('mark',self.project,'check-final','--state','done','--evidence','No recheck',ok=False)
        self.observe('output:final','technical','pass','--depends-on','output:source')
        for step in ['check-final','delivery']:
            self.cli('mark',self.project,step,'--state','done','--evidence','Rechecked fixture')
        self.assertTrue(self.status()['technical_handoff_recorded'])

    def test_removal_cannot_be_attached_to_unpublished_replacement_bytes(self):
        self.cli('create',self.project,'--goal','Publication history','--note','Fixture')
        self.cli('asset',self.project,'film','--kind','video-export')
        f=self.root/'film.txt';f.write_text('revision one')
        self.cli('retain',self.project,'film',f)
        self.observe('output:film','publication','published','--url','https://example.test/film','--visibility','unlisted')
        f.write_text('revision two');self.cli('retain',self.project,'film',f,'--replace')
        before=self.project.read_bytes()
        self.observe('output:film','publication','removed','--url','https://example.test/film',ok=False)
        self.assertEqual(before,self.project.read_bytes())
        self.observe('output:film','publication','published','--url','https://example.test/film','--visibility','unlisted')
        self.observe('output:film','publication','removed','--url','https://example.test/film')
        self.assertEqual(self.status()['observations']['effective'][0]['result'],'removed')

    def test_routing_blockers_are_not_external_waits(self):
        brief=self.root/'brief.json';brief.write_text(json.dumps({'blocks':[{'id':'a','input':'book-art','language':'uk','preferred_voice':'mlx-audio','deliverables':['narration']}]}))
        self.cli('init',brief,self.project)
        result=self.status()
        self.assertTrue(result['blocked'])
        self.assertEqual(result['waiting'],{})

    def test_old_project_read_is_unchanged_and_explicit_migration_preserves_original(self):
        brief = self.root / 'brief.json'
        brief.write_text(json.dumps({'blocks': [{'id': 'intro', 'input': 'brand'}]}))
        self.cli('init', brief, self.project)
        old = self.data()
        old['schema_version'] = 1
        for name in ['project', 'journal', 'journal_sha256']:
            old.pop(name, None)
        self.project.write_text(json.dumps(old))
        before = self.project.read_bytes()
        self.status()
        self.assertEqual(before, self.project.read_bytes())
        self.cli('migrate', self.project)
        self.assertEqual(self.data()['schema_version'], 2)
        self.assertEqual(before, Path(str(self.project) + '.v1.bak').read_bytes())
        self.assertEqual(old['plan'], self.data()['plan'])
        self.cli('describe', self.project, '--goal', 'Finish the book virtual set', '--note', 'Owner selected subject')
        self.assertEqual(self.status()['project']['goal'], 'Finish the book virtual set')
        before = self.project.read_bytes()
        self.cli('migrate', self.project)
        self.assertEqual(before, self.project.read_bytes())

    def observe(self, subject, kind, result, *extra, ok=True):
        return self.cli('observe', self.project, subject, '--kind', kind, '--result', result,
                        '--actor', 'owner', '--provenance', 'owner_report',
                        '--note', 'Scoped fixture observation', *extra, ok=ok)

    def test_revision_replacement_reopens_only_relevant_decisions_and_preserves_rejection(self):
        self.cli('create', self.project, '--goal', 'Book set, no production', '--note', 'Manual project')
        art = self.root / 'art.txt'; art.write_text('accepted art')
        voice = self.root / 'voice.txt'; voice.write_text('rejected voice')
        for name, path in [('art', art), ('voice', voice)]:
            self.cli('asset', self.project, name, '--kind', 'reference')
            self.cli('retain', self.project, name, path)
        self.observe('output:art', 'creative', 'accepted')
        self.observe('output:voice', 'listening', 'rejected')
        self.cli('task', self.project, 'owner-recording', '--label', 'Wait for owner TP recording',
                 '--waiting-for', 'owner', '--note', 'Deferred during SSI work')
        self.cli('task', self.project, 'assemble', '--label', 'Assemble later', '--after', 'owner-recording')
        result = self.status()
        self.assertEqual(result['ready'], [])
        self.assertEqual(result['waiting']['owner-recording']['party'], 'owner')
        self.assertEqual([x['result'] for x in result['observations']['effective']], ['accepted','rejected'])
        voice.write_text('new recording')
        changed = self.status()
        self.assertEqual(len(changed['observations']['stale']), 1)
        self.cli('retain', self.project, 'voice', voice, '--replace')
        result = self.status()
        self.assertEqual(result['observations']['effective'][0]['result'], 'accepted')
        self.assertEqual(result['observations']['stale'][0]['result'], 'rejected')
        self.assertEqual(len(self.data()['journal']), 2)
        self.assertEqual(self.data()['plan']['mode'], 'manual_production')
        before = self.project.read_bytes(); self.status()
        self.assertEqual(before, self.project.read_bytes())

    def test_publication_removal_does_not_erase_technical_result_or_approve_provider(self):
        self.cli('create', self.project, '--goal', 'Verification demo', '--note', 'Fixture only')
        self.cli('asset', self.project, 'film', '--kind', 'video-export')
        f = self.root / 'film.txt';f.write_text('not real media')
        self.cli('retain', self.project, 'film', f)
        self.observe('output:film', 'technical', 'pass')
        self.observe('output:film', 'publication', 'published', '--url', 'https://example.test/video', '--visibility', 'unlisted')
        self.observe('output:film', 'decision', 'deferred', '--topic', 'remove-after-provider-decision')
        self.observe('output:film', 'publication', 'removed', '--url', 'https://example.test/video')
        r = self.status()
        self.assertEqual([x['result'] for x in r['observations']['effective']], ['pass','deferred','removed'])
        self.assertFalse(r['technical_handoff_recorded'])
        self.assertFalse(any(x['kind']=='provider' for x in self.data()['journal']))
        self.assertEqual(len(self.data()['journal']), 4)
        before=self.project.read_bytes()
        self.observe('output:film', 'technical', 'accepted', ok=False)
        self.observe('output:missing', 'technical', 'pass', ok=False)
        self.observe('project', 'technical', 'pass', ok=False)
        self.assertEqual(before,self.project.read_bytes())

    def test_failed_receipt_reopens_qa_not_authoring_and_cannot_be_marked_done(self):
        self.cli('create', self.project, '--goal', 'Scoped local QA', '--note', 'Fixture')
        self.cli('asset', self.project, 'voice', '--kind', 'narration')
        f=self.root/'voice.txt';f.write_text('synthetic fixture')
        self.cli('retain', self.project, 'voice', f)
        self.cli('task', self.project, 'author', '--label', 'Author voice', '--requires', 'voice')
        self.cli('task', self.project, 'listen', '--label', 'Listen', '--after', 'author',
                 '--requires', 'voice', '--check-kind', 'listening')
        self.cli('task', self.project, 'deliver', '--label', 'Deliver', '--after', 'listen')
        for step in ['author','listen','deliver']:
            self.cli('mark', self.project, step, '--state', 'done', '--evidence', 'Manual fixture check')
        self.observe('output:voice','listening','rejected')
        r=self.status()
        self.assertIn('author',r['recorded_done'])
        self.assertNotIn('listen',r['recorded_done'])
        self.assertNotIn('deliver',r['recorded_done'])
        self.assertNotIn('listen',r['ready'])
        self.cli('mark',self.project,'listen','--state','done','--evidence','ignore rejection',ok=False)
        self.observe('output:voice','listening','accepted')
        self.assertIn('listen',self.status()['ready'])
        self.assertNotIn('listen',self.status()['recorded_done'])

    def test_receipt_dependencies_and_integrity_are_checked_without_rewriting_history(self):
        self.cli('create',self.project,'--goal','Dependency check','--note','Fixture')
        for name in ['source','mix']:
            f=self.root/(name+'.txt');f.write_text(name)
            self.cli('asset',self.project,name,'--kind','reference')
            self.cli('retain',self.project,name,f)
        self.observe('output:mix','technical','pass','--depends-on','output:source')
        (self.root/'source.txt').write_text('new source')
        self.assertEqual(len(self.status()['observations']['stale']),1)
        before=self.project.read_bytes()
        self.observe('output:mix','technical','pass','--depends-on','output:source',ok=False)
        self.assertEqual(before,self.project.read_bytes())
        data=self.data();data['journal'][0]['result']='fail';self.project.write_text(json.dumps(data))
        before=self.project.read_bytes();self.cli('resume',self.project,ok=False)
        self.assertEqual(before,self.project.read_bytes())

    def test_project_decision_changes_are_historical_and_unknown_observation_time_is_not_invented(self):
        self.cli('create',self.project,'--goal','Original goal','--note','Original context')
        self.observe('project','decision','accepted','--topic','concept')
        row=self.data()['journal'][0]
        self.assertIsNone(row['observed_at'])
        self.assertTrue(row['recorded_at'])
        self.cli('describe',self.project,'--goal','New goal','--note','Scope changed')
        self.assertEqual(len(self.status()['observations']['stale']),1)
        self.assertEqual(self.status()['observations']['effective'],[])
        before=self.project.read_bytes()
        self.observe('project','decision','accepted',ok=False)
        self.observe('project','decision','accepted','--topic','concept','--observed-at','2026-10-18T12:00:00',ok=False)
        self.cli('task',self.project,'cycle','--label','Invalid dependency','--after','cycle',ok=False)
        self.assertEqual(before,self.project.read_bytes())
        logged=json.loads(self.cli('journal',self.project,'--json').stdout)
        self.assertEqual(logged['observations'][0]['result'],'accepted')

    def test_pending_receipt_preserves_explicit_owner_wait(self):
        self.cli('create',self.project,'--goal','Wait for review','--note','Fixture')
        self.cli('asset',self.project,'art','--kind','still-export')
        f=self.root/'art.txt';f.write_text('fixture')
        self.cli('retain',self.project,'art',f)
        self.cli('task',self.project,'owner-art','--label','Owner art review',
                 '--requires','art','--check-kind','creative','--waiting-for','owner','--note','Not yet reviewed')
        self.observe('output:art','creative','pending')
        self.assertEqual(self.status()['waiting']['owner-art']['party'],'owner')
        self.assertNotIn('owner-art',self.status()['ready'])

    def test_invalid_topic_cannot_leave_an_unreadable_checkpoint(self):
        self.cli('create',self.project,'--goal','Safe writes','--note','Fixture')
        self.cli('asset',self.project,'art','--kind','reference')
        f=self.root/'art.txt';f.write_text('fixture')
        self.cli('retain',self.project,'art',f)
        before=self.project.read_bytes()
        self.observe('output:art','creative','accepted','--topic','   ',ok=False)
        self.assertEqual(before,self.project.read_bytes())
        self.status()
