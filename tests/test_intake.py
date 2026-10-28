"""Producer intake: local preferences, incomplete briefs and evidence-bounded options."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
CLI=ROOT/'skills/video-production-router/scripts/intake.py'
CATALOG=ROOT/'skills/video-production-router/references/provider-terms-pilot.json'


class IntakeTest(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);self.root=Path(t.name)
        self.profile=self.root/'profile.json';self.brief=self.root/'brief.json';self.routes=self.root/'routes.json'
        self.call('init',self.profile)
        self.brief.write_text(json.dumps({'idea':'A promo for my book'}))
        self.routes.write_text(json.dumps({'routes':[
            {'id':'local','label':'Local draft','cost_kind':'free_local','cost':0,'currency':'USD','evidence':'tested_scoped'},
            {'id':'quota','label':'Daily quota','cost_kind':'free_quota','cost':None,'currency':'credits','evidence':'unknown'},
            {'id':'paid','label':'Paid generation','cost_kind':'paid','cost':None,'currency':'USD','evidence':'documented'}]}))

    def call(self,*args,ok=True):
        p=subprocess.run([sys.executable,str(CLI),*map(str,args)],capture_output=True,text=True)
        self.assertEqual(p.returncode==0,ok,p.stderr);return p

    def propose(self):
        return json.loads(self.call('propose',self.profile,self.brief,self.routes).stdout)

    def test_defaults_to_two_options_and_asks_only_missing_information(self):
        result=self.propose()
        self.assertEqual([r['id'] for r in result['routes']],['local','quota','paid'])
        self.assertTrue(result['questions']);self.assertEqual(result['routes'][1]['cost'],None)
        self.assertEqual(result['execution'],'not_authorized')
        self.assertNotIn('idea',result['questions'])

    def test_free_only_preference_persists_and_hides_paid(self):
        self.call('preference',self.profile,'--options','free-only')
        self.assertEqual([r['id'] for r in self.propose()['routes']],['local','quota'])
        self.assertEqual(json.loads(self.profile.read_text())['options'],'free-only')
        self.assertNotIn('budget',self.propose()['questions'])

    def test_declared_entitlements_are_private_and_unverified(self):
        result=json.loads(self.call('subscription',self.profile,'example-service','--status','available').stdout)
        self.assertEqual(result['basis'],'user_declared_not_verified')
        self.assertEqual(json.loads(self.profile.read_text())['subscriptions']['example-service'],'available')
        self.assertNotIn('subscriptions',self.propose())

    def test_unknown_and_inconsistent_cost_never_become_free(self):
        self.routes.write_text(json.dumps({'routes':[{'id':'bad','label':'Unknown','cost_kind':'free_local',
           'cost':None,'currency':'USD','evidence':'unknown'}]}))
        self.call('propose',self.profile,self.brief,self.routes,ok=False)

    def test_init_does_not_overwrite_existing_profile(self):
        before=self.profile.read_bytes();self.call('init',self.profile,ok=False)
        self.assertEqual(before,self.profile.read_bytes())
        self.assertEqual(os.stat(self.profile).st_mode & 0o077,0)

    def test_catalogue_enriches_only_selected_provider_with_dated_unverified_terms(self):
        self.routes.write_text(json.dumps({'routes':[{'id':'v','label':'Video','cost_kind':'free_quota',
            'cost':None,'currency':'credits','evidence':'documented','provider_id':'pixverse'}]}))
        self.call('subscription',self.profile,'pixverse','--status','available')
        result=json.loads(self.call('propose',self.profile,self.brief,self.routes,'--catalog',CATALOG).stdout)
        row=result['routes'][0]
        self.assertEqual(row['provider_terms']['quota']['recurring_credits'],30)
        self.assertEqual(row['terms_status'],'historical_recheck_required')
        self.assertEqual(row['account_declaration'],'available')
        self.assertEqual(row['account_access'],'user_declared_not_verified')
        self.assertIsNone(row['cost']);self.assertEqual(row['rights'],'unknown')
        self.assertEqual(result['execution'],'not_authorized')

    def test_catalogue_does_not_turn_one_time_credits_into_a_refill(self):
        rows=json.loads((ROOT/'examples/intake/provider-routes.json').read_text())
        self.routes.write_text(json.dumps(rows))
        self.call('preference',self.profile,'--options','free-only')
        result=json.loads(self.call('propose',self.profile,self.brief,self.routes,'--catalog',CATALOG).stdout)
        runway=next(r for r in result['routes'] if r['provider_id']=='runway')
        self.assertEqual(runway['provider_terms']['quota']['interval'],'none')
        self.assertEqual(runway['provider_terms']['quota']['recurring_credits'],0)

    def test_catalogue_rejects_unknown_or_mismatched_provider(self):
        route={'id':'v','label':'Video','cost_kind':'paid','cost':None,'currency':'USD',
               'evidence':'documented','provider_id':'pixverse'}
        self.routes.write_text(json.dumps({'routes':[route]}))
        self.call('propose',self.profile,self.brief,self.routes,'--catalog',CATALOG,ok=False)
        route['provider_id']='not-in-catalogue'
        self.routes.write_text(json.dumps({'routes':[route]}))
        self.call('propose',self.profile,self.brief,self.routes,'--catalog',CATALOG,ok=False)

    def test_task_discovery_preserves_component_and_provider_evidence(self):
        self.call('preference',self.profile,'--options','free-only')
        result=json.loads(self.call('recommend',self.profile,self.brief,'--task','video').stdout)
        rows={r['id']:r for r in result['candidates']}
        self.assertEqual(rows['ffmpeg']['evidence'],'tested')
        self.assertEqual(rows['pixverse']['evidence'],'unknown')
        self.assertEqual(rows['pixverse']['provider_terms']['observed_on'],'2026-10-27')
        self.assertEqual(rows['runway']['provider_terms']['quota']['interval'],'none')
        self.assertNotIn('meshy',rows)
        self.assertTrue(result['excluded_unclassified_cost'])
        self.assertEqual(result['execution'],'not_authorized')

    def test_task_discovery_does_not_invent_free_options(self):
        self.call('preference',self.profile,'--options','free-only')
        result=json.loads(self.call('recommend',self.profile,self.brief,'--task','narration').stdout)
        self.assertTrue(result['candidates'])
        self.assertTrue(all(r['cost_kind']=='free_local' for r in result['candidates']))
        self.assertGreater(result['excluded_unclassified_cost'],0)
        self.call('recommend',self.profile,self.brief,'--task','nonexistent',ok=False)

    def test_both_options_retains_unknown_cost_candidates(self):
        result=json.loads(self.call('recommend',self.profile,self.brief,'--task','narration').stdout)
        self.assertTrue(result['candidates'])
        self.assertTrue(any(r['cost_kind']=='free_local' for r in result['candidates']))
        self.assertTrue(all(r['cost'] is None for r in result['candidates']))

if __name__=='__main__':unittest.main()
