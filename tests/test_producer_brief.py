"""Producer proposal public interface: planning facts never grant execution."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'skills/video-production-router/scripts'


class ProducerBriefTest(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup);self.root=Path(tmp.name).resolve()
        self.profile=self.root/'profile.json';self.brief=self.root/'brief.json'
        self.p={'schema':'framewright-intake-v1','options':'free-only','subscriptions':{},'sharing':'off'}
        self.b=json.loads((ROOT/'examples/intake/comparison-brief.json').read_text())

    def cli(self,*extra,ok=True):
        self.profile.write_text(json.dumps(self.p));self.brief.write_text(json.dumps(self.b))
        before={p:p.read_bytes() for p in (self.profile,self.brief)}
        r=subprocess.run([sys.executable,str(BASE/'intake.py'),'brief',str(self.profile),str(self.brief),*map(str,extra)],capture_output=True,text=True)
        self.assertEqual(r.returncode==0,ok,r.stderr)
        for p,raw in before.items():self.assertEqual(p.read_bytes(),raw)
        return r

    def test_retained_free_only_brief_is_one_readable_non_executing_offer(self):
        r=json.loads(self.cli().stdout)
        self.assertEqual(r['schema'],'framewright-producer-brief-v1')
        for key in ('task','materials','routes','constraints','next_step'):self.assertIn(key,r)
        self.assertEqual(r['task']['idea'],self.b['idea'])
        self.assertEqual(r['execution'],'not_authorized')
        self.assertEqual(r['network_calls'],0)
        self.assertGreater(len(r['routes']),0);self.assertLessEqual(len(r['routes']),3)
        self.assertEqual(r['routes'][0]['id'],'local-montage')
        self.assertNotIn('conditional-authoring',[x['id'] for x in r['routes']])
        self.assertEqual(r['materials']['status'],'declared_not_inspected')
        self.assertIn('source_index',r['materials']['missing'])
        for row in r['routes']:
            self.assertIsNone(row['time_estimate']);self.assertIsNone(row['cost']['total_project_cost'])
        md=self.cli('--format','markdown').stdout
        for heading in ('Task','Materials','Routes','Constraints','Next step'):self.assertIn(heading,md)
        self.assertIn('unknown',md.lower())
        self.assertIn('proposed',md.lower())

    def test_retained_markdown_examples_match_both_policy_views(self):
        for policy in ('free-only','both'):
            self.p['options']=policy
            self.assertEqual(self.cli('--format','markdown').stdout,
                (ROOT/'examples/intake'/('producer-brief-'+policy+'.md')).read_text())

    def test_missing_brief_details_require_clarification(self):
        self.b={'idea':'Book promo'}
        r=json.loads(self.cli().stdout)
        self.assertEqual(r['routes'],[])
        self.assertEqual(r['next_step']['kind'],'clarify_brief')
        self.assertIn('duration_seconds',r['questions'])

    def test_broader_policy_retains_conditional_cost_and_free_only_hides_it(self):
        self.p['options']='both'
        r=json.loads(self.cli().stdout)
        conditional=next(x for x in r['routes'] if x['id']=='conditional-authoring')
        self.assertIsNone(conditional['cost']['provider_fee'])
        self.assertIn('Licence eligibility', ' '.join(conditional['unknown_conditions']))

    def test_explicit_route_and_voice_are_not_silently_replaced(self):
        self.b.update(preferred_route='local-saved-shot',preferred_voice='not-indexed')
        r=json.loads(self.cli().stdout)
        self.assertEqual([x['id'] for x in r['routes']],['local-saved-shot'])
        self.assertIsNone(r['routes'][0]['stages'][1]['tool'])
        self.assertEqual(r['next_step']['kind'],'resolve_route_gaps')
        self.b['preferred_route']='conditional-authoring'
        r=json.loads(self.cli().stdout)
        self.assertEqual(r['routes'],[])
        self.assertEqual(r['next_step']['kind'],'resolve_route_gaps')
        self.b['preferred_route']='invented'
        self.cli(ok=False)

    def test_upload_restriction_and_declared_unavailable_block_generation(self):
        self.b.update(visual_source='generate',constraints={'allow_uploads':False})
        r=json.loads(self.cli().stdout)
        self.assertEqual(r['routes'],[])
        self.assertIn('upload',str(r['route_exclusions']).lower())
        self.b.pop('constraints');self.p['subscriptions']['pixverse']='unavailable'
        r=json.loads(self.cli().stdout)
        self.assertEqual(r['routes'],[])
        self.assertIn('unavailable',str(r['route_exclusions']))
        self.p['subscriptions']['pixverse']='available'
        r=json.loads(self.cli().stdout)
        row=r['routes'][0]
        self.assertIsNone(row['time_estimate'])
        self.assertEqual(row['stages'][0]['candidate']['access'],'user_declared_not_verified')

    def test_scene_purpose_is_declared_or_proposed_never_inferred_approval(self):
        self.b['scenes']=[{'id':'hook','purpose':'Show why the book matters','query':'cover'},
                          {'id':'proof','purpose':'Show a page example','query':'page'}]
        r=json.loads(self.cli().stdout)
        self.assertEqual(r['scenes'][0]['purpose'],self.b['scenes'][0]['purpose'])
        self.assertEqual(r['scenes'][0]['basis'],'declared')
        self.assertEqual(r['scenes'][0]['material_status'],'not_searched')
        self.b.pop('scenes')
        r=json.loads(self.cli().stdout)
        self.assertTrue(r['scenes']);self.assertTrue(all(x['basis']=='proposed' for x in r['scenes']))
        self.assertIn('scene_purposes',r['questions'])

    def test_forbidden_installation_is_not_treated_as_installed(self):
        self.b['constraints']={'allow_installation':False}
        r=json.loads(self.cli().stdout)
        self.assertIn('unknown',r['constraints']['machine'])
        self.assertTrue(all('Installation forbidden' in ' '.join(x['unknown_conditions']) for x in r['routes']))

    def test_invalid_inputs_fail_instead_of_looking_complete(self):
        for update in ({'duration_seconds':-2},{'duration_seconds':True},{'duration_seconds':float('nan')},
                       {'format':[]},{'scenes':[]},{'scenes':[{'id':'x','purpose':''}]},
                       {'constraints':{'allow_uploads':'false'}},{'constraints':{'ignored_rule':True}}):
            with self.subTest(update=update):
                old=self.b.copy();self.b.update(update);self.cli(ok=False);self.b=old

    def test_source_index_keeps_exact_evidence_and_marks_real_gaps(self):
        import runpy
        source=runpy.run_path(str(BASE/'source_search.py'))
        image=self.root/'cover.png';image.write_bytes(b'fixture; no image quality claim')
        spec=self.root/'sources.json'
        spec.write_text(json.dumps({'sources':[{'id':'cover','kind':'image','path':image.name,
            'evidence_sha256':source['E']['file_hash'](image),
            'observations':[{'id':'obs','text':'Book cover'}],
            'annotation_provenance':{'method':'manual','scope':'supplied observation'}}]}))
        index=self.root/'index.json';index.write_text(json.dumps(source['build'](spec)))
        self.b['scenes']=[{'id':'hook','purpose':'Introduce the book','query':'cover'},
                          {'id':'inside','purpose':'Read a sample','query':'page'}]
        r=json.loads(self.cli('--source-index',index).stdout)
        self.assertEqual(r['materials']['status'],'checked_file_revisions_only')
        self.assertEqual(r['scenes'][0]['candidates'][0]['source'],'cover')
        self.assertEqual(r['scenes'][0]['material_status'],'candidates_require_review')
        self.assertEqual(r['scenes'][1]['material_status'],'not_found_in_index')
        md=self.cli('--source-index',index,'--format','markdown').stdout
        self.assertIn('Read a sample',md);self.assertIn('not_found_in_index',md)
        self.assertIn('supplied observation',md)
        image.write_bytes(b'changed')
        self.cli('--source-index',index,ok=False)

    def test_project_wait_and_file_drift_survive_join_without_writes(self):
        project=self.root/'project.json'
        def project_cli(*args):
            r=subprocess.run([sys.executable,str(BASE/'project.py'),*map(str,args)],capture_output=True,text=True)
            self.assertEqual(r.returncode,0,r.stderr)
        project_cli('create',project,'--goal','Book promo','--note','Internal fixture')
        project_cli('asset',project,'cover','--kind','image')
        material=self.root/'cover.txt';material.write_text('first')
        project_cli('retain',project,'cover',material)
        project_cli('task',project,'pause','--label','Await owner','--waiting-for','owner','--note','Keep production paused')
        before=project.read_bytes()
        waiting=json.loads(self.cli('--project',project).stdout)
        self.assertEqual(waiting['next_step']['kind'],'waiting')
        self.assertEqual(waiting['project']['waiting'][0]['reason'],'Keep production paused')
        self.assertEqual(project.read_bytes(),before)
        material.write_text('changed')
        r=json.loads(self.cli('--project',project).stdout)
        self.assertEqual(r['next_step']['kind'],'file_review')
        self.assertEqual(r['project']['counts']['file_changes'],1)
        self.assertEqual(project.read_bytes(),before)


if __name__=='__main__':unittest.main()
