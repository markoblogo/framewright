import copy
import itertools
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('planner', ROOT / 'skills/video-production-router/scripts/plan.py')
planner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(planner)
REGISTRY = json.loads((ROOT / 'skills/video-production-router/references/tools.json').read_text())


class BlockPlannerTest(unittest.TestCase):
    def brief(self, **block):
        return {'blocks': [{'id': 'one', 'input': 'brand', **block}]}

    def run_plan(self, brief):
        return planner.plan(brief, copy.deepcopy(REGISTRY))

    def test_mn7r_diagram_keeps_explicit_mlx_voice_and_extracted_still(self):
        brief = self.brief(input='book-art', effects=['workflow-diagram'], preferred_voice='mlx-audio', deliverables=['video-export', 'narration', 'still-export'])
        brief['minimum_evidence'] = 'tested'
        p = self.run_plan(brief)
        b = p['blocks'][0]
        self.assertEqual(p['status'], 'proposed')
        self.assertEqual(b['primary_tool'], 'manimgx')
        self.assertEqual(set(b['tools']), {'manimgx', 'mlx-audio', 'ffmpeg'})
        self.assertEqual(next(x['tool'] for x in b['coverage'] if x['feature']=='narration'), 'mlx-audio')
        self.assertIn('timing', ' '.join(b['known_limits']['manimgx']))

    def test_explicit_english_mlx_profile_does_not_claim_ukrainian(self):
        p = self.run_plan(self.brief(input='book-art', effects=['workflow-diagram'], preferred_voice='mlx-audio', language='uk', deliverables=['video-export', 'narration']))
        self.assertIn('narration', p['blocks'][0]['unmet'])
        self.assertEqual(p['status'], 'blocked')
        self.assertNotIn('kokoro', p['blocks'][0]['tools'])

    def test_ukrainian_paper_scene_preserves_voice_and_picture(self):
        brief = self.brief(input='book-art', language='uk', style='paper-cut',
                           preferred_tool='remotion', preferred_voice='piper',
                           effects=['paper-cut-regroup'],
                           deliverables=['video-export', 'narration', 'still-export'])
        result = self.run_plan(brief)
        block = result['blocks'][0]
        self.assertEqual(result['status'], 'proposed')
        self.assertEqual(set(block['tools']), {'remotion', 'piper'})
        self.assertEqual(next(c['tool'] for c in block['coverage'] if c['feature'] == 'narration'), 'piper')

    def test_ukrainian_piper_does_not_claim_french_or_singing(self):
        french = self.run_plan(self.brief(input='book-art', language='fr', preferred_voice='piper', deliverables=['narration']))
        self.assertIn('narration', french['blocks'][0]['unmet'])
        song = self.run_plan(self.brief(input='book-art', language='uk', preferred_voice='piper', deliverables=['song-generation']))
        self.assertIn('song-generation', song['blocks'][0]['unmet'])

    def test_paper_effect_other_canvas_is_not_promoted(self):
        tool = copy.deepcopy(next(t for t in REGISTRY['tools'] if t['id'] == 'remotion'))
        feature = next(f for f in tool['features'] if f['id'] == 'paper-cut-regroup')
        feature['status'] = 'tested'
        feature['tested_canvases'] = [{'width': 1920, 'height': 1080, 'fps': 30}]
        cap = planner.capability(tool, 'paper-cut-regroup', 'uk', False,
                                 {'width': 1080, 'height': 1080, 'fps': 30})
        self.assertEqual(cap['evidence'], 'documented')
        self.assertEqual(planner.capability(tool, 'paper-cut-regroup', 'uk', False,
                         {'width': 1920, 'height': 1080, 'fps': 30})['evidence'], 'tested')

    def test_owner_rejected_voice_is_not_automatically_selected(self):
        result = self.run_plan(self.brief(input='book-art', language='uk',
                                         deliverables=['video-export', 'narration']))
        self.assertEqual(result['status'], 'proposed')
        self.assertIn('supertonic3', result['blocks'][0]['tools'])
        self.assertNotIn('piper', result['blocks'][0]['tools'])
        self.assertTrue(next(t for t in REGISTRY['tools'] if t['id'] == 'piper')['features'][0]['status'] == 'tested')

    def test_explicit_rejected_voice_keeps_quality_warning(self):
        result = self.run_plan(self.brief(input='book-art', language='uk',
                                         preferred_voice='piper', deliverables=['narration']))
        self.assertEqual(result['status'], 'proposed')
        self.assertIn('piper', result['blocks'][0]['tools'])
        self.assertIn('unnecessary pauses', ' '.join(result['blocks'][0]['known_limits']['piper']))

    def test_new_eligible_ukrainian_voice_can_replace_rejected_default(self):
        registry = copy.deepcopy(REGISTRY)
        registry['tools'] = [t for t in registry['tools'] if t['id'] != 'supertonic3']
        alternative = copy.deepcopy(next(t for t in registry['tools'] if t['id'] == 'piper'))
        alternative['id'] = 'fixture-uk-voice'
        alternative['default_narration_eligible'] = True
        registry['tools'].append(alternative)
        result = planner.plan(self.brief(input='book-art', language='uk',
                                         deliverables=['narration']), registry)
        self.assertEqual(result['status'], 'proposed')
        self.assertIn('fixture-uk-voice', result['blocks'][0]['tools'])
        self.assertNotIn('piper', result['blocks'][0]['tools'])

    def test_low_quality_fallback_is_not_silent_when_primary_missing(self):
        registry = copy.deepcopy(REGISTRY)
        registry['tools'] = [t for t in registry['tools'] if t['id'] != 'supertonic3']
        result = planner.plan(self.brief(input='book-art', language='uk', deliverables=['narration']), registry)
        self.assertEqual(result['status'], 'blocked')
        self.assertNotIn('piper', result['blocks'][0]['tools'])

    def test_lcd_uk_scene_selects_recommended_voice_and_actual_finisher(self):
        brief = self.brief(input='book-art', language='uk', preferred_tool='remotion',
                           style='lcd-editorial', effects=['lcd-terminal-motion'],
                           deliverables=['video-export', 'narration', 'media-mux', 'still-export'])
        brief['minimum_evidence'] = 'tested'
        result = self.run_plan(brief)
        self.assertEqual(result['status'], 'proposed')
        self.assertEqual(set(result['blocks'][0]['tools']), {'remotion', 'supertonic3', 'ffmpeg'})
        self.assertEqual(next(c['tool'] for c in result['blocks'][0]['coverage'] if c['feature']=='narration'), 'supertonic3')

    def test_invalid_preferred_voice_rejected(self):
        for tool in ['unknown', 'manimgx', []]:
            with self.subTest(tool=tool), self.assertRaisesRegex(ValueError, 'preferred_voice'):
                self.run_plan(self.brief(preferred_voice=tool))

    def test_staged_3d_selects_authored_adapter_and_local_voice(self):
        brief = self.brief(input='book-art', effects=['staged-3d', 'object-motion', 'camera-travel'], deliverables=['video-export', 'narration', 'still-export'])
        brief['minimum_evidence'] = 'tested'
        p = self.run_plan(brief)
        b = p['blocks'][0]
        self.assertEqual(p['status'], 'proposed')
        self.assertEqual(b['primary_tool'], 'three-scene')
        self.assertEqual(set(b['tools']), {'three-scene', 'kokoro', 'ffmpeg'})
        self.assertNotIn('anatomy', b['tools'])
        self.assertFalse(b['requires_feature_test'])

    def test_staged_3d_does_not_replace_plain_object_or_book(self):
        for kind in ['object', 'book-art', 'brand']:
            p = self.run_plan(self.brief(input=kind))
            self.assertNotIn('three-scene', p['blocks'][0]['tools'])

    def test_staged_3d_style_alone_is_an_explicit_activation(self):
        p = self.run_plan(self.brief(input='book-art', style='miniature-diorama'))
        self.assertEqual(p['blocks'][0]['primary_tool'], 'three-scene')
        self.assertTrue(p['blocks'][0]['style_match'])

    def test_staged_3d_does_not_claim_tested_60fps(self):
        brief = self.brief(input='object', preferred_tool='three-scene', effects=['staged-3d', 'object-motion'])
        brief['canvas'] = {'width': 1920, 'height': 1080, 'fps': 60}
        p = self.run_plan(brief)
        self.assertIn('staged-3d', p['blocks'][0]['requires_feature_test'])
        brief['minimum_evidence'] = 'tested'
        self.assertIn('staged-3d', self.run_plan(brief)['blocks'][0]['unmet'])

    def test_staged_3d_preserves_explicit_renderer(self):
        p = self.run_plan(self.brief(input='object', preferred_tool='anatomy', effects=['staged-3d']))
        self.assertEqual(p['blocks'][0]['primary_tool'], 'anatomy')
        self.assertIn('three-scene', p['blocks'][0]['tools'])
        self.assertIn('integration test', p['assembly']['qualification'])

    def test_staged_3d_unknown_physics_is_unmet(self):
        p = self.run_plan(self.brief(input='object', effects=['staged-3d', 'calibrated-physics']))
        self.assertEqual(p['status'], 'blocked')
        self.assertIn('calibrated-physics', p['blocks'][0]['unmet'])

    def test_staged_3d_other_canvas_needs_test(self):
        brief = self.brief(input='object', preferred_tool='three-scene', effects=['staged-3d'])
        brief['canvas'] = {'width': 1080, 'height': 1920, 'fps': 30}
        p = self.run_plan(brief)
        self.assertIn('staged-3d', p['blocks'][0]['requires_feature_test'])
        self.assertIn('vertical-format', p['blocks'][0]['requires_feature_test'])
        brief['minimum_evidence'] = 'tested'
        self.assertIn('staged-3d', self.run_plan(brief)['blocks'][0]['unmet'])

    def test_staged_3d_style_and_multiblock_combination(self):
        brief = {'minimum_evidence': 'tested', 'blocks': [
            {'id': 'object', 'input': 'object', 'style': 'miniature-diorama', 'effects': ['staged-3d'], 'duration_seconds': 5},
            {'id': 'ui', 'input': 'react-ui', 'preferred_tool': 'flute', 'duration_seconds': 5},
            {'id': 'title', 'input': 'brand', 'preferred_tool': 'remotion', 'duration_seconds': 5}]}
        p = self.run_plan(brief)
        self.assertEqual([b['primary_tool'] for b in p['blocks']], ['three-scene', 'flute', 'remotion'])
        self.assertTrue(p['blocks'][0]['style_match'])
        self.assertEqual(p['duration_frames'], 450)
        self.assertEqual(p['execution'], 'not_started')
        self.assertIn('integration test', p['assembly']['qualification'])

    def test_music_provider_cannot_bypass_independent_music_plan(self):
        for feature in ['song-generation', 'audio-download']:
            with self.subTest(feature=feature):
                p = self.run_plan(self.brief(effects=[feature]))
                self.assertEqual(p['status'], 'blocked')
                self.assertIsNone(p['music'])
                self.assertIn(feature, p['blocks'][0]['unmet'])
                self.assertFalse({'suno', 'flow-music'}.intersection(p['blocks'][0]['tools']))

    def test_storyboard_cannot_act_as_picture_provider(self):
        registry = copy.deepcopy(REGISTRY)
        registry['tools'].append({
            'id': 'preproduction-probe', 'role': 'preproduction', 'inputs': ['brand'],
            'styles': [], 'limitations': [],
            'features': [{'id': 'shot-list', 'status': 'documented', 'source': 'remotion', 'note': 'text only'}],
        })
        result = planner.plan(self.brief(deliverables=['shot-list']), registry)
        self.assertEqual(result['status'], 'blocked')
        self.assertIn('shot-list', result['blocks'][0]['unmet'])
        self.assertNotIn('preproduction-probe', result['blocks'][0]['tools'])

    def test_existing_ui_uses_flute_without_extra_renderer(self):
        p = self.run_plan(self.brief(input='react-ui', effects=['camera-travel', 'depth-of-field']))
        self.assertEqual(p['blocks'][0]['tools'], ['flute'])

    def test_native_still_does_not_add_finisher(self):
        p = self.run_plan(self.brief(preferred_tool='remotion', deliverables=['video-export', 'still-export']))
        self.assertEqual(p['blocks'][0]['tools'], ['remotion'])

    def test_flute_snapshot_failure_gets_real_finishing_fallback(self):
        b = self.brief(input='react-ui', preferred_tool='flute', deliverables=['video-export', 'still-export'])
        p = self.run_plan(b)
        self.assertEqual(p['blocks'][0]['tools'], ['flute', 'ffmpeg'])
        self.assertEqual(p['blocks'][0]['coverage'][-1]['tool'], 'ffmpeg')
        self.assertTrue(p['blocks'][0]['known_limits']['flute'])

    def test_voice_is_a_layer_not_a_new_picture_renderer(self):
        p = self.run_plan(self.brief(preferred_tool='remotion', deliverables=['video-export', 'narration'], language='fr'))
        self.assertEqual(p['blocks'][0]['tools'], ['remotion', 'kokoro'])
        self.assertEqual(p['qualification'], 'planning_only')

    def test_untested_language_is_not_promoted(self):
        b = self.brief(deliverables=['narration'], language='ja')
        b['minimum_evidence'] = 'tested'
        self.assertIn('narration', self.run_plan(b)['blocks'][0]['unmet'])
        b['minimum_evidence'] = 'documented'
        self.assertIn('narration', self.run_plan(b)['blocks'][0]['requires_feature_test'])

    def test_unknown_language_is_not_invented(self):
        p = self.run_plan(self.brief(deliverables=['narration'], language='unknown-language'))
        self.assertEqual(p['status'], 'blocked')

    def test_style_can_change_primary_without_becoming_a_hard_limit(self):
        b = self.brief(input='source-project', style='kinetic')
        p = self.run_plan(b)
        self.assertEqual(p['blocks'][0]['primary_tool'], 'hyperframes')
        b['blocks'][0]['preferred_tool'] = 'brag'
        self.assertEqual(self.run_plan(b)['blocks'][0]['primary_tool'], 'brag')

    def test_incompatible_explicit_choice_not_silently_replaced(self):
        p = self.run_plan(self.brief(preferred_tool='flute'))
        self.assertEqual(p['status'], 'blocked')
        self.assertEqual(p['blocks'][0]['primary_tool'], 'flute')
        self.assertEqual(p['blocks'][0]['tools'], [])

    def test_object_layer_can_come_from_another_tool(self):
        b = self.brief(preferred_tool='remotion', assets=['object'], effects=['isometric-svg', 'typography'])
        p = self.run_plan(b)
        self.assertEqual(p['blocks'][0]['tools'], ['remotion', 'anatomy'])

    def test_paid_effect_requires_explicit_planning_constraint(self):
        b = self.brief(preferred_tool='remotion', effects=['cube-transition'])
        self.assertEqual(self.run_plan(b)['status'], 'blocked')
        b['allow_paid'] = True
        p = self.run_plan(b)
        self.assertEqual(p['status'], 'proposed')
        self.assertEqual(p['execution'], 'not_started')

    def test_vertical_is_documented_not_locally_tested(self):
        b = self.brief()
        b.update(canvas={'width': 1080, 'height': 1920, 'fps': 30}, minimum_evidence='tested')
        self.assertIn('vertical-format', self.run_plan(b)['blocks'][0]['unmet'])

    def test_physics_accuracy_stays_unmet(self):
        p = self.run_plan(self.brief(input='object', effects=['physics-calibration']))
        self.assertIn('physics-calibration', p['blocks'][0]['unmet'])

    def test_multitool_blocks_and_explicit_overlap_have_one_timeline(self):
        b = {'canvas': {'width': 1920, 'height': 1080, 'fps': 30}, 'duration_seconds': 9,
             'blocks': [{'id': 'intro', 'input': 'brand', 'duration_seconds': 4},
                        {'id': 'ui', 'input': 'react-ui', 'duration_seconds': 6, 'overlap_frames': 30}]}
        p = self.run_plan(b)
        self.assertEqual([x['primary_tool'] for x in p['blocks']], ['remotion', 'flute'])
        self.assertEqual([x['start_frame'] for x in p['blocks']], [0, 90])
        self.assertEqual(p['duration_frames'], 270)
        self.assertIn('integration test', p['assembly']['qualification'])

    def test_missing_timing_stays_unknown(self):
        p = self.run_plan(self.brief())
        self.assertIsNone(p['duration_frames'])

    def test_invalid_duration_and_duplicate_ids_rejected(self):
        for b in [self.brief(duration_seconds=.01), {'blocks': [{'id':'x','input':'brand'}, {'id':'x','input':'react-ui'}]}, {'blocks':[]}]:
            with self.subTest(brief=b), self.assertRaises(ValueError):
                self.run_plan(b)



    def test_malformed_briefs_fail_with_clear_errors(self):
        for brief in [[], {'blocks': ['bad']}, {'blocks': [{'id': 'x', 'input': 'brand'}], 'canvas': 42}, self.brief(language=[]), self.brief(effects=[''])]:
            with self.subTest(brief=brief), self.assertRaises(ValueError):
                self.run_plan(brief)



    def test_requirement_order_does_not_block_finishing_dependencies(self):
        plans = []
        for deliverables in [['media-mux', 'video-export'], ['video-export', 'media-mux']]:
            plans.append(self.run_plan(self.brief(input='object', preferred_tool='anatomy', deliverables=deliverables)))
        for p in plans:
            self.assertEqual(p['status'], 'proposed')
            self.assertEqual(p['blocks'][0]['tools'], ['anatomy', 'hyperframes', 'ffmpeg'])
            self.assertEqual(p['blocks'][0]['unmet'], [])
        self.assertEqual(plans[0]['blocks'][0]['tools'], plans[1]['blocks'][0]['tools'])

    def test_still_only_prefers_direct_tested_export(self):
        brief = self.brief(input='book-art', deliverables=['still-export'])
        brief['minimum_evidence'] = 'tested'
        p = self.run_plan(brief)
        self.assertEqual(p['blocks'][0]['tools'], ['remotion'])
        self.assertEqual(p['blocks'][0]['coverage'][0]['tool'], 'remotion')



    def test_requirement_permutations_have_identical_tool_coverage(self):
        expected = None
        for items in itertools.permutations(['media-mux', 'video-export', 'still-export', 'narration']):
            p = self.run_plan(self.brief(input='object', preferred_tool='anatomy', deliverables=list(items)))
            block = p['blocks'][0]
            actual = (block['tools'], sorted((x['feature'], x['tool'], x['evidence']) for x in block['coverage']), sorted(block['unmet']))
            if expected is None:
                expected = actual
            self.assertEqual(actual, expected)

    def test_native_tested_still_beats_documented_default(self):
        p = self.run_plan(self.brief(input='book-art', deliverables=['still-export']))
        self.assertEqual(p['blocks'][0]['tools'], ['remotion'])



    def test_still_only_has_no_global_video_assembly(self):
        p = self.run_plan(self.brief(input='book-art', deliverables=['still-export']))
        self.assertIsNone(p['assembly']['tool'])
        self.assertIn('Still-only', p['assembly']['qualification'])



    def test_tested_fallback_beats_documented_native_still(self):
        p = self.run_plan(self.brief(input='source-project', deliverables=['still-export']))
        b = p['blocks'][0]
        self.assertEqual(b['tools'], ['brag', 'ffmpeg'])
        self.assertEqual(b['coverage'][0]['evidence'], 'tested')
        self.assertEqual(b['requires_feature_test'], [])



    def test_existing_documented_provider_cannot_hide_tested_alternative(self):
        p = self.run_plan(self.brief(effects=['normalization', 'audio-mix']))
        b = p['blocks'][0]
        self.assertEqual(b['requires_feature_test'], [])
        by_feature = {x['feature']: x for x in b['coverage']}
        self.assertEqual(by_feature['normalization']['tool'], 'ffmpeg')
        self.assertEqual(by_feature['audio-mix']['tool'], 'sound-layer')

    def test_cut_analysis_is_a_companion_for_existing_video_only(self):
        video = self.run_plan(self.brief(input='video', effects=['hard-cut-detection']))
        self.assertEqual(set(video['blocks'][0]['tools']), {'ffmpeg','pyscenedetect'})
        self.assertEqual(video['blocks'][0]['requires_feature_test'], [])
        art = self.run_plan(self.brief(input='book-art', effects=['hard-cut-detection']))
        self.assertIn('hard-cut-detection', art['blocks'][0]['unmet'])
        self.assertNotIn('pyscenedetect', art['blocks'][0]['tools'])


if __name__ == '__main__':
    unittest.main()
