"""Route comparisons must retain missing capabilities, cost and access boundaries."""
import json
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'skills/video-production-router/scripts'
INTAKE=runpy.run_path(str(BASE/'intake.py'))
ROUTES=runpy.run_path(str(BASE/'intake_routes.py'))


class RouteComparisonTest(unittest.TestCase):
    def compare(self,options='free-only',**updates):
        brief={'idea':'An English book promo','language':'en','duration_seconds':30,
               'format':'16:9','visual_source':'supplied','source_rights':'owner','deadline':'flexible'}
        brief.update(updates)
        p={'schema':'framewright-intake-v1','options':options,'subscriptions':{},'sharing':'off'}
        return ROUTES['compare'](p,brief,INTAKE['recommend'])

    def test_equal_stages_and_scoped_evidence_do_not_qualify_chain(self):
        r=self.compare()
        self.assertTrue(r['routes'])
        for row in r['routes']:
            self.assertEqual([s['role'] for s in row['stages']],['picture','narration','finishing'])
            self.assertEqual(row['execution'],'not_authorized')
            self.assertIsNone(row['cost']['total_project_cost'])
            self.assertIsNone(row['time_estimate'])
            self.assertIn('integration_check',row['qualification'])
        local=r['routes'][0]
        self.assertEqual(local['cost']['provider_fee'],0)
        self.assertEqual(local['stages'][1]['required_capabilities'],{'narration':'tested'})

    def test_quota_route_remains_unpriced_and_needs_trial(self):
        row=next(r for r in self.compare()['routes'] if r['id']=='quota-generation')
        self.assertEqual(row['coverage'],'gaps_require_resolution')
        self.assertIsNone(row['cost']['provider_fee'])
        self.assertEqual(row['stages'][0]['candidate']['terms_status'],'historical_recheck_required')

    def test_conditional_eligibility_hidden_by_free_only(self):
        self.assertNotIn('conditional-authoring',[r['id'] for r in self.compare()['routes']])
        row=next(r for r in self.compare('both')['routes'] if r['id']=='conditional-authoring')
        self.assertIsNone(row['cost']['provider_fee'])
        self.assertIn('Licence eligibility and provider fee quote',row['unknown_conditions'])

    def test_declared_available_subscription_does_not_waive_licence_eligibility(self):
        p={'schema':'framewright-intake-v1','options':'free-only','subscriptions':{'remotion':'available'},'sharing':'off'}
        r=ROUTES['compare'](p,{'idea':'Promo','language':'en'},INTAKE['recommend'])
        self.assertNotIn('conditional-authoring',[x['id'] for x in r['routes']])
        p['options']='both'
        r=ROUTES['compare'](p,{'idea':'Promo','language':'en'},INTAKE['recommend'])
        row=next(x for x in r['routes'] if x['id']=='conditional-authoring')
        self.assertIsNone(row['cost']['provider_fee'])

    def test_unsupported_language_and_explicit_voice_are_never_substituted(self):
        for kwargs in [{'language':'xx'},{'preferred_voice':'not-indexed'}]:
            for r in self.compare(**kwargs)['routes']:
                self.assertIsNone(r['stages'][1]['tool'])
                self.assertIn('narration: no compatible candidate',r['gaps'])
                self.assertIsNone(r['cost']['provider_fee'])

    def test_documented_language_is_not_promoted_to_tested(self):
        for r in self.compare(language='ja',preferred_voice='kokoro')['routes']:
            self.assertEqual(r['stages'][1]['required_capabilities']['narration'],'documented')

    def test_generation_need_and_optional_narration(self):
        result=self.compare(visual_source='generate',narration=False)
        local=result['routes'][0]
        self.assertIn('Source generation is not covered by this supplied-media recipe',local['gaps'])
        self.assertEqual([s['role'] for s in local['stages']],['picture','finishing'])
        with self.assertRaises(ValueError):self.compare(narration='false')
        with self.assertRaises(ValueError):self.compare(visual_source='invented')

    def test_markdown_keeps_unresolved_conditions(self):
        r=self.compare(language='xx')
        text=ROUTES['markdown'](r)
        self.assertIn('UNRESOLVED',text)
        self.assertIn('total cost remain unknown',text)
        self.assertIn('required capability needs a trial',text)

    def test_declared_unavailable_provider_blocks_route(self):
        p={'schema':'framewright-intake-v1','options':'free-only','subscriptions':{'pixverse':'unavailable'},'sharing':'off'}
        r=ROUTES['compare'](p,{'idea':'Promo','language':'en'},INTAKE['recommend'])
        quota=next(x for x in r['routes'] if x['id']=='quota-generation')
        self.assertIn('Selected provider is declared unavailable',quota['gaps'])

    def test_cli_matches_retained_comparison(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'profile.json'
            p.write_text(json.dumps({'schema':'framewright-intake-v1','options':'both','sharing':'off','subscriptions':{}}))
            proc=subprocess.run([sys.executable,str(BASE/'intake.py'),'routes',str(p),
                str(ROOT/'examples/intake/comparison-brief.json'),'--format','markdown'],capture_output=True,text=True)
            self.assertEqual(proc.returncode,0,proc.stderr)
            self.assertEqual(proc.stdout,(ROOT/'examples/intake/route-comparison.md').read_text()+'\n')


if __name__=='__main__':unittest.main()
