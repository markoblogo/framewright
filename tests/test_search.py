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
        for identity in ['awwwards-mcp','odyssey-world-models','genjutsu']:
            with self.subTest(tool=identity):
                rows=self.search('--tool',identity,'--evidence','any')['results']
                self.assertEqual([r['id'] for r in rows],[identity])
                self.assertFalse(rows[0]['eligible_for_feature_planning'])
                self.assertFalse(rows[0]['rights']['asset_clearance'])
                self.assertEqual(self.search('--tool',identity,'--evidence','tested')['results'],[])

    def test_openverse_sfx_is_tested_without_qualifying_music_or_asset_rights(self):
        for task in ['audio','acquisition']:
            with self.subTest(task=task):
                rows=self.search('--tool','openverse','--task',task,'--evidence','tested')['results']
                self.assertEqual([row['id'] for row in rows],['openverse'])
                row=rows[0]
                self.assertEqual(row['evidence'],'tested')
                self.assertEqual(row['disposition'],'tested_scoped')
                self.assertFalse(row['eligible_for_feature_planning'])
                self.assertFalse(row['rights']['asset_clearance'])
                self.assertFalse(row['rights']['publication_authorized'])
        self.assertEqual(self.search('--tool','openverse','--task','music','--evidence','tested')['results'],[])

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
        self.assertIn('supertonic3',ids)
        self.assertNotIn('piper',ids)
        self.assertNotIn('kokoro',ids)
        self.assertEqual(r['execution'],'not_started')
        row=next(x for x in r['results'] if x['id']=='supertonic3')
        self.assertEqual(row['rights']['status'],'conditional_review_required')
        self.assertFalse(row['rights']['asset_clearance'])

    def test_style_matches_picture_without_filtering_out_ukrainian_voice(self):
        r=self.search('--task','video','--input','book-art','--style','paper-cut',
                      '--feature','paper-cut-regroup','--feature','narration','--feature','still-export',
                      '--language','uk','--rights','commercial','--evidence','tested','--combinations')
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
        p=subprocess.run([sys.executable,str(CLI),'--task','narration','--language','uk','--format','markdown'],capture_output=True,text=True,check=True)
        self.assertIn(r'conditional\_review\_required',p.stdout)
        self.assertNotIn('"id": "kokoro"',p.stdout)
        self.assertLess(len(p.stdout),12000)
        r=self.search('--tool','kokoro','--task','narration','--language','uk','--explain')
        self.assertTrue(r['excluded'])
        self.assertTrue(any('speech language' in reason for row in r['excluded'] if row['id']=='kokoro' for reason in row['reasons']))

    def test_retained_example_matches_current_cli_and_video_analysis_is_composable(self):
        flags=['--task','video','--input','book-art','--style','paper-cut','--feature','paper-cut-regroup',
               '--feature','narration','--feature','still-export','--language','uk','--rights','commercial',
               '--evidence','tested','--combinations','--format','markdown']
        p=subprocess.run([sys.executable,str(CLI),*flags],capture_output=True,text=True,check=True)
        self.assertEqual(p.stdout,(ROOT/'examples/plans/arsenal-search-paper-uk.md').read_text())
        r=self.search('--task','video','--input','video','--feature','hard-cut-detection','--evidence','tested','--combinations')
        self.assertEqual(set(r['combinations'][0]['tools']),{'ffmpeg','pyscenedetect'})
