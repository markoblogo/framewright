"""Arsenal discovery through the public CLI, without tools/media/providers."""
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
CLI=ROOT/'skills/video-production-router/scripts/search.py'

class ArsenalSearchTest(unittest.TestCase):
    def search(self,*args,ok=True):
        p=subprocess.run([sys.executable,str(CLI),*args],capture_output=True,text=True)
        self.assertEqual(p.returncode==0,ok,p.stderr)
        return json.loads(p.stdout) if ok else p

    def test_ranked_profile_falls_back_when_primary_is_unavailable(self):
        result=self.search('--rank-profile','editorial-graphics','--unavailable','GiveMotion')
        self.assertEqual((result['primary'],result['fallback'],result['next_test']),
                         ('manim-community','openmotion',None))
        remaining=('--rank-profile','editorial-graphics','--unavailable','givemotion',
                   '--unavailable','manim-community','--unavailable','openmotion')
        self.assertIsNone(self.search(*remaining)['primary'])
        self.assertEqual(self.search(*remaining,'--include-fallbacks')['primary'],'minicharts')
        self.assertIn('Unavailable in this production',result['production'][0]['blocking_reasons'])
        self.assertNotIn('speed',result['production_score_axes'])
        self.assertIsNone(result['production'][0]['ratings']['speed'])

    def test_paid_trials_need_both_confirmation_and_paid_permission(self):
        args=('--rank-profile','editorial-graphics','--confirmed','premotio')
        self.assertIsNone(self.search(*args)['next_test'])
        self.assertEqual(self.search(*args,'--allow-paid')['next_test'],'premotio')
        self.assertIsNone(self.search('--rank-profile','editorial-graphics','--allow-paid')['next_test'])

    def test_reserve_and_rejected_routes_do_not_silently_take_over(self):
        args=('--rank-profile','local-english-narration','--unavailable','kokoro')
        self.assertIsNone(self.search(*args)['primary'])
        self.assertEqual(self.search(*args,'--include-fallbacks')['primary'],'supertonic3')
        args=('--rank-profile','portrait-adaptation','--unavailable','ffmpeg','--unavailable','filmcraft',
              '--confirmed','klap','--confirmed','opusclip','--allow-paid','--include-fallbacks')
        result=self.search(*args)
        self.assertIsNone(result['primary'])
        self.assertEqual({r['tool'] for r in result['excluded']},{'klap','opusclip'})
        self.assertEqual(self.search(*args,'--confirmed','inshot-android')['primary'],'inshot-android')

    def test_rankings_require_a_tested_application_and_a_valid_rating(self):
        import runpy
        ranking=runpy.run_path(str(CLI))['RANKING']
        facets=json.loads((ROOT/'skills/video-production-router/references/arsenal-facets.json').read_text())
        first=facets['rankings']['editorial-graphics']['entries'][0]
        first['ratings']['quality']=6
        with self.assertRaisesRegex(ValueError,'Invalid ranking ratings'):
            ranking['validate_rankings'](facets)
        first['ratings']['quality']=4
        del first['application']
        with self.assertRaisesRegex(ValueError,'requires usable tested application'):
            ranking['validate_rankings'](facets)

    def test_newspaper_application_and_owner_evidence_are_discoverable(self):
        rows=self.search('--query','газетный коллаж с цветными вставками','--evidence','tested')['results']
        self.assertEqual([r['id'] for r in rows],['genmotion'])
        row=rows[0];app=row['applications'][0]
        self.assertEqual(app['version'],'0.8.1')
        self.assertEqual(app['owner_evaluation']['status'],'accepted')
        self.assertEqual(app['technical']['status'],'passed')
        self.assertEqual(set(app['quality']),{'readability','motion','drawing_stability','artifacts','controllability'})
        self.assertTrue(app['examples'][0]['url'].endswith('h0ZTfFPKbcs'))
        self.assertFalse(row['eligible_for_feature_planning'])
        self.assertFalse(row['rights']['asset_clearance'])

    def test_new_style_technique_filters_and_distinct_manim(self):
        for tool,style,tech in [('genmotion','paper-collage','colour-footage-insert'),('manim-community','ascii','glyph-transform'),('givemotion','paper-ink','receipt-story')]:
            rows=self.search('--tool',tool,'--style',style,'--technique',tech,'--evidence','tested')['results']
            self.assertEqual([r['id'] for r in rows],[tool])
        self.assertEqual(self.search('--tool','manimgx','--style','ascii','--evidence','tested')['results'],[])
        self.assertEqual(self.search('--tool','genmotion','--feature','narration','--evidence','tested')['results'],[])

    def test_publication_does_not_create_owner_acceptance_or_a_comparison(self):
        applications=self.search('--tool','givemotion','--evidence','tested')['results'][0]['applications']
        app=next(row for row in applications if row['id']=='givemotion--vet402')
        self.assertEqual(app['owner_evaluation']['status'],'not_recorded')
        self.assertEqual(app['technical']['status'],'passed')
        self.assertTrue(app['examples'])
        self.assertTrue(all(a['comparison']=='not_compared'for a in app['alternatives']))

    def test_unknown_history_is_explicit_and_formats_do_not_promote_provider(self):
        app=self.search('--tool','manimgx','--evidence','tested')['results'][0]['applications'][0]
        self.assertTrue(all(q['status']=='not_assessed'for q in app['quality'].values()))
        r=self.search('--task','video','--input','composition','--tool','genmotion','--style','paper-collage','--evidence','tested','--combinations')
        self.assertEqual(r['combinations'],[])
        self.assertTrue(r['blocked_combinations'])

    def test_historical_ledger_summary_is_not_feature_specific_evidence(self):
        for tool,technique in [('hyperframes','native-audio'),('hyperframes','typography')]:
            self.assertEqual(self.search('--tool',tool,'--technique',technique,'--evidence','tested')['results'],[])
        apps=self.search('--tool','hyperframes','--evidence','tested')['results'][0]['applications']
        self.assertEqual(len(apps),1)
        self.assertEqual(apps[0]['id'],'hyperframes--retained-scope')
        self.assertNotIn('experiment_id',apps[0])
        self.assertEqual(apps[0]['techniques'],[])
        self.assertTrue(apps[0]['scope'].startswith('Tool-level'))

    def test_application_facets_must_match_one_scope(self):
        import runpy
        match=runpy.run_path(str(CLI))['application_matches']
        q={'task':'editing','style':'photo-collage','input':'video','technique':None,'evidence':'tested','text':''}
        app={'tasks':['editing'],'styles':['screencast-tour'],'inputs':['video'],'techniques':[],'evidence':'tested'}
        self.assertFalse(match(app,q))
        self.assertEqual(self.search('--tool','inshot-android','--task','editing','--style','photo-collage','--evidence','tested')['results'],[])

    def test_authored_compositions_do_not_claim_untested_media_import(self):
        for tool,style in [('manim-community','ascii'),('givemotion','paper-ink')]:
            for kind in ['image','video']:
                self.assertEqual(self.search('--tool',tool,'--task','video','--input',kind,'--style',style,'--evidence','tested')['results'],[])
            self.assertEqual([r['id']for r in self.search('--tool',tool,'--input','composition','--style',style,'--evidence','tested')['results']],[tool])

    def test_installed_discovery_needs_no_checkout_docs(self):
        import shutil,tempfile
        with tempfile.TemporaryDirectory()as tmp:
            target=Path(tmp)/'video-production-router'
            for folder in ['scripts','references']:
                shutil.copytree(ROOT/'skills/video-production-router'/folder,target/folder,ignore=shutil.ignore_patterns('__pycache__'))
            self.assertFalse((Path(tmp)/'docs').exists())
            p=subprocess.run([sys.executable,str(target/'scripts/search.py'),'--query','газетный коллаж с цветными вставками','--evidence','tested'],capture_output=True,text=True)
            self.assertEqual(p.returncode,0,p.stderr)
            self.assertEqual([r['id']for r in json.loads(p.stdout)['results']],['genmotion'])

    def test_repository_validation_still_rejects_missing_source(self):
        import runpy
        validate=runpy.run_path(str(CLI))['validate_applications']
        facets=json.loads((ROOT/'skills/video-production-router/references/arsenal-facets.json').read_text())
        facets['tools']['genmotion']['applications'][0]['sources']=['docs/nonexistent-application-source.md']
        validate(facets)  # Installed structural check keeps checkout-relative references.
        with self.assertRaisesRegex(ValueError,'Invalid application source'):validate(facets,source_root=ROOT)

    def test_rejected_and_failed_comparisons_stay_diagnostic(self):
        r=self.search('--tool','playmcp-veo31-fast','--evidence','any')['results'][0]
        a=r['applications'][0]
        self.assertEqual(a['technical']['status'],'passed')
        self.assertEqual(a['owner_evaluation']['status'],'rejected')
        self.assertEqual(self.search('--tool','playmcp-veo31-fast','--evidence','tested')['results'],[])
        a=self.search('--tool','chatgpt-native-gif','--evidence','any')['results'][0]['applications'][0]
        self.assertEqual(a['evidence'],'failed')
        self.assertEqual(a['technical']['status'],'failed')
        self.assertEqual(a['owner_evaluation']['status'],'not_recorded')

    def test_application_schema_rejects_missing_quality_and_duplicate_ids(self):
        import runpy,copy
        validate=runpy.run_path(str(CLI))['validate_applications']
        facets=json.loads((ROOT/'skills/video-production-router/references/arsenal-facets.json').read_text())
        a=facets['tools']['genmotion']['applications'][0]
        del a['quality']['motion']
        with self.assertRaisesRegex(ValueError,'quality axis'):validate(facets)
        facets=json.loads((ROOT/'skills/video-production-router/references/arsenal-facets.json').read_text())
        facets['tools']['genmotion']['applications'].append(copy.deepcopy(facets['tools']['genmotion']['applications'][0]))
        with self.assertRaisesRegex(ValueError,'Duplicate application'):validate(facets)

    def test_unindexed_world_candidate_does_not_match_explicit_input_modalities(self):
        rows=self.search('--task','video','--tool','odyssey-world-models','--evidence','any')['results']
        self.assertEqual([row['id'] for row in rows],['odyssey-world-models'])
        for kind in ['audio','image','video','book-art']:
            result=self.search('--task','video','--tool','odyssey-world-models','--input',kind,'--evidence','any','--explain')
            self.assertEqual(result['results'],[])
            self.assertTrue(any(row['id']=='odyssey-world-models' and
                'input kind does not match or is unindexed' in row['reasons'] for row in result['excluded']))

    def test_review_modalities_audio_and_image_are_reachable_filters(self):
        for modality in ['audio','image','video']:
            rows=self.search('--task','media-review','--input',modality,'--evidence','any')['results']
            self.assertIn('gemini-media-review',{row['id'] for row in rows})
            self.assertTrue(all(not row['eligible_for_feature_planning'] for row in rows))

    def test_latest_research_is_discoverable_without_tested_promotion(self):
        for identity in ['awwwards-mcp','genjutsu']:
            with self.subTest(tool=identity):
                rows=self.search('--tool',identity,'--evidence','any')['results']
                self.assertEqual([r['id'] for r in rows],[identity])
                self.assertFalse(rows[0]['eligible_for_feature_planning'])
                self.assertFalse(rows[0]['rights']['asset_clearance'])
                self.assertEqual(self.search('--tool',identity,'--evidence','tested')['results'],[])

    def test_odyssey_retained_component_is_not_structured_feature_or_rights_approval(self):
        rows=self.search('--tool','odyssey-world-models','--evidence','tested')['results']
        self.assertEqual([r['id'] for r in rows],['odyssey-world-models'])
        row=rows[0]
        self.assertEqual(row['disposition'],'component_used')
        self.assertFalse(row['eligible_for_feature_planning'])
        self.assertEqual(row['task_capabilities'],{})
        self.assertFalse(row['rights']['asset_clearance'])
        self.assertFalse(row['rights']['publication_authorized'])
        self.assertIn('docs/experiments/good-dog-closeout.md',row['reference'])

    def test_openverse_sfx_acquisition_does_not_qualify_audio_or_music_work(self):
        rows=self.search('--tool','openverse','--task','acquisition','--evidence','tested')['results']
        self.assertEqual([row['id'] for row in rows],['openverse'])
        row=rows[0]
        self.assertEqual(row['evidence'],'tested')
        self.assertEqual(row['disposition'],'tested_scoped')
        self.assertFalse(row['eligible_for_feature_planning'])
        self.assertFalse(row['rights']['asset_clearance'])
        self.assertFalse(row['rights']['publication_authorized'])
        for task in ['audio','music']:
            with self.subTest(task=task):
                self.assertEqual(self.search('--tool','openverse','--task',task,'--evidence','tested')['results'],[])

    def test_tesseract_conversion_is_discoverable_without_becoming_a_renderer(self):
        result = self.search('--task', 'editing', '--tool', 'tesseract-converter',
                             '--input', 'source-project', '--rights', 'commercial',
                             '--evidence', 'tested')
        self.assertEqual([r['id'] for r in result['results']], ['tesseract-converter'])
        row = result['results'][0]
        self.assertFalse(row['eligible_for_feature_planning'])
        self.assertFalse(row['rights']['asset_clearance'])
        self.assertTrue(row['rights']['classification_matches_retained_note'])
        self.assertIn('Native editor playback/export unverified', ' '.join(row['limits']))
        rendered = self.search('--task', 'video', '--tool', 'tesseract-converter',
                               '--feature', 'video-export', '--evidence', 'tested')
        self.assertEqual(rendered['results'], [])

    def test_ukrainian_voice_discovery_keeps_scope_and_excludes_low_quality_default(self):
        r=self.search('--task','narration','--language','uk','--evidence','tested','--rights','commercial')
        ids=[x['id'] for x in r['results']]
        self.assertNotIn('supertonic3',ids)
        self.assertIn('low-quality explicit fallback;enable --include-fallbacks to inspect',r['excluded_summary'])
        self.assertNotIn('piper',ids)
        self.assertNotIn('kokoro',ids)
        self.assertEqual(r['execution'],'not_started')
        explicit=self.search('--task','narration','--language','uk','--tool','supertonic3','--evidence','tested','--rights','commercial')
        row=next(x for x in explicit['results'] if x['id']=='supertonic3')
        self.assertEqual(row['rights']['status'],'conditional_review_required')
        self.assertFalse(row['rights']['asset_clearance'])

    def test_narrated_chain_requires_explicit_reserve_voice(self):
        r=self.search('--task','video','--input','book-art','--style','paper-cut',
                      '--feature','paper-cut-regroup','--feature','narration','--feature','still-export',
                      '--language','uk','--rights','commercial','--evidence','tested','--combinations')
        self.assertEqual(r['combinations'],[])
        self.assertTrue(any('narration' in c['unmet'] for c in r['blocked_combinations']))
        r=self.search('--task','video','--input','book-art','--style','paper-cut',
                      '--feature','paper-cut-regroup','--feature','narration','--feature','still-export',
                      '--language','uk','--rights','commercial','--evidence','tested','--combinations',
                      '--voice','supertonic3')
        self.assertTrue(r['combinations'])
        c=r['combinations'][0]
        self.assertEqual(c['primary'],'remotion')
        self.assertEqual(set(c['tools']),{'remotion','supertonic3'})
        self.assertEqual(c['qualification'],'proposed_chain_requires_integration_check')
        self.assertTrue(all(not p['asset_clearance'] for p in c['rights'].values()))

    def test_music_providers_never_fill_picture_chain_features(self):
        r=self.search('--task','video','--input','brand','--feature','song-generation','--combinations')
        self.assertEqual(r['combinations'],[])
        self.assertTrue(r['blocked_combinations'])
        for c in r['blocked_combinations']:
            self.assertNotIn('suno',c['tools'])
            self.assertNotIn('flow-music',c['tools'])
            self.assertIn('song-generation',c['unmet'])

    def test_noncommercial_restriction_is_visible_not_treated_as_technical_failure(self):
        public=self.search('--task','narration','--rights','commercial','--evidence','any')
        self.assertNotIn('mms-tts-ukr',[r['id'] for r in public['results']])
        private=self.search('--task','narration','--rights','noncommercial','--evidence','any','--limit','50')
        row=next(r for r in private['results'] if r['id']=='mms-tts-ukr')
        self.assertEqual(row['rights']['classification'],'noncommercial_only')
        self.assertEqual(row['evidence'],'unknown')
        self.assertFalse(row['eligible_for_feature_planning'])

    def test_manual_moviepy_is_discoverable_but_not_invented_as_planner_provider(self):
        r=self.search('--task','editing','--input','video','--evidence','tested')
        row=next(x for x in r['results'] if x['id']=='moviepy')
        self.assertEqual(row['mode'],'retained_manual_or_review_record')
        r=self.search('--task','editing','--input','video','--tool','moviepy','--combinations')
        self.assertEqual(r['combinations'],[])
        self.assertIn('explicit tool',r['blocked_combinations'][0]['unmet'][0])

    def test_failed_native_feature_is_diagnostic_only_not_supported(self):
        r=self.search('--task','video','--input','react-ui','--tool','flute','--feature','still-export','--evidence','any')
        self.assertEqual(r['results'][0]['evidence'],'failed')
        self.assertFalse(r['results'][0]['eligible_for_feature_planning'])
        good=self.search('--task','video','--input','react-ui','--tool','flute','--feature','still-export','--evidence','tested','--combinations')
        self.assertEqual(set(good['combinations'][0]['tools']),{'flute','ffmpeg'})

    def test_cloud_account_and_paid_feature_gates_are_not_waived(self):
        r=self.search('--task','song','--feature','video-cover-art')
        self.assertEqual(r['results'],[])
        r=self.search('--task','song','--feature','video-cover-art','--allow-paid','--rights','commercial')
        row=next(x for x in r['results'] if x['id']=='suno')
        self.assertTrue(row['requires_account_check'])
        self.assertFalse(row['rights']['publication_authorized'])
        self.assertEqual(row['rights']['status'],'conditional_review_required')
        lang=self.search('--task','song','--language','uk')
        self.assertEqual(lang['results'],[])

    def test_explicit_bad_voice_is_blocked_and_explicit_fallback_is_inspectable(self):
        r=self.search('--task','video','--input','book-art','--feature','narration','--voice','mlx-audio','--language','uk','--combinations')
        self.assertEqual(r['combinations'],[])
        self.assertTrue(all('narration' in x['unmet'] for x in r['blocked_combinations']))
        fallback=self.search('--task','narration','--language','uk','--tool','piper','--evidence','tested')
        self.assertEqual(fallback['results'][0]['id'],'piper')
        self.assertIn('weak',' '.join(fallback['results'][0]['limits']))

    def test_task_presets_activate_diagram_and_capability_order_does_not_change_chains(self):
        a=self.search('--task','diagram','--input','book-art','--combinations','--evidence','tested')
        self.assertIn('manimgx',a['combinations'][0]['tools'])
        flags=['--task','video','--input','object','--tool','anatomy','--combinations']
        a=self.search(*flags,'--feature','isometric-svg','--feature','media-mux')
        b=self.search(*flags,'--feature','media-mux','--feature','isometric-svg')
        self.assertEqual([c['tools'] for c in a['combinations']],[c['tools'] for c in b['combinations']])

    def test_filters_are_listed_and_unknown_or_incomplete_queries_fail_clearly(self):
        index=self.search('--list-filters')
        self.assertIn('paper-cut',index['styles'])
        self.assertIn('uk',index['speech_languages'])
        self.assertGreaterEqual(index['records'],39)
        for flags in [('--combinations',),('--task','fictional'),('--task','video','--language','uk'),('--tool','fictional')]:
            self.search(*flags,ok=False)

    def test_changed_license_note_invalidates_its_old_discovery_classification(self):
        import copy
        import runpy
        module=runpy.run_path(str(CLI))
        refs=ROOT/'skills/video-production-router/references'
        registry=json.loads((refs/'tools.json').read_text())
        ledger=json.loads((refs/'review-ledger.json').read_text())
        facets=json.loads((refs/'arsenal-facets.json').read_text())
        changed=copy.deepcopy(registry)
        next(t for t in changed['tools'] if t['id']=='supertonic3')['licence_note']='changed,unreviewed licence terms'
        row=module['inventory'](changed,ledger,facets)['supertonic3']
        policy=module['rights'](row,'commercial')
        self.assertFalse(policy['matches_filter'])
        self.assertFalse(policy['classification_matches_retained_note'])
        self.assertEqual(policy['classification'],'unknown')

    def test_input_and_evidence_filters_do_not_promote_unknown_manual_or_candidate_scope(self):
        r=self.search('--task','editing','--input','book-art','--evidence','tested')
        self.assertNotIn('moviepy',[x['id'] for x in r['results']])
        r=self.search('--task','transcription','--evidence','tested')
        self.assertEqual([x['id'] for x in r['results']], ['mlx-whisper'])
        self.assertFalse(r['results'][0]['eligible_for_feature_planning'])
        self.assertIn('No general ASR/lyric alignment qualification', ' '.join(r['results'][0]['limits']))
        for candidate in ['parakeet-mlx', 'whisperx', 'whisper']:
            self.assertEqual(self.search('--task', 'transcription', '--tool', candidate,
                                         '--evidence', 'tested')['results'], [])
        self.assertEqual(self.search('--task', 'transcription', '--language', 'uk',
                                     '--evidence', 'tested')['results'], [])
        candidates=self.search('--task','transcription','--evidence','any')
        self.assertEqual({x['id'] for x in candidates['results']},{'mlx-whisper','parakeet-mlx','whisperx','whisper'})
        self.assertTrue(all(not x['eligible_for_feature_planning'] for x in candidates['results']))

    def test_cross_format_evidence_is_not_promoted_and_unknown_style_has_no_match(self):
        r=self.search('--task','diagram','--input','book-art','--feature','workflow-diagram',
                      '--width','1080','--height','1920','--evidence','tested','--combinations')
        self.assertEqual(r['combinations'],[])
        r=self.search('--task','video','--style','not-indexed-style')
        self.assertEqual(r['results'],[])
        self.assertIn('style not indexed for this tool',r['excluded_summary'])

    def test_markdown_is_bounded_and_explicit_diagnostics_available(self):
        p=subprocess.run([sys.executable,str(CLI),'--task','narration','--language','uk','--tool','supertonic3','--format','markdown'],capture_output=True,text=True,check=True)
        self.assertIn(r'conditional\_review\_required',p.stdout)
        self.assertNotIn('"id": "kokoro"',p.stdout)
        self.assertLess(len(p.stdout),12000)
        r=self.search('--tool','kokoro','--task','narration','--language','uk','--explain')
        self.assertTrue(r['excluded'])
        self.assertTrue(any('speech language' in reason for row in r['excluded'] if row['id']=='kokoro' for reason in row['reasons']))

    def test_retained_example_matches_current_cli_and_video_analysis_is_composable(self):
        flags=['--task','video','--input','book-art','--style','paper-cut','--feature','paper-cut-regroup',
               '--feature','narration','--feature','still-export','--language','uk','--rights','commercial',
               '--evidence','tested','--combinations','--voice','supertonic3','--format','markdown']
        p=subprocess.run([sys.executable,str(CLI),*flags],capture_output=True,text=True,check=True)
        self.assertEqual(p.stdout,(ROOT/'examples/plans/arsenal-search-paper-uk.md').read_text())
        r=self.search('--task','video','--input','video','--feature','hard-cut-detection','--evidence','tested','--combinations')
        self.assertEqual(set(r['combinations'][0]['tools']),{'ffmpeg','pyscenedetect'})
