"""Synthetic video-control generation and grading; no model calls."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
CLI=ROOT/'skills/video-production-router/scripts/media_pilot.py'
MEDIA=ROOT/'skills/video-production-router/scripts/media_review.py'

class MediaPilotTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not shutil.which('ffmpeg') or not shutil.which('ffprobe'):raise unittest.SkipTest('Existing FFmpeg required')
        cls.temp=tempfile.TemporaryDirectory();cls.root=Path(cls.temp.name);cls.suite=cls.root/'suite'
        p=subprocess.run([sys.executable,str(CLI),'build',str(cls.suite),'--seed','17'],capture_output=True,text=True)
        if p.returncode:
            cls.temp.cleanup();raise AssertionError(p.stderr)
        cls.manifest=json.loads((cls.suite/'operator/suite.json').read_text())
        cls.gold=json.loads((cls.suite/'operator/gold.json').read_text())
        cls.template=json.loads((cls.suite/'reviewer/answers-template.json').read_text())

    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()

    def call(self,*args,ok=True):
        p=subprocess.run([sys.executable,str(CLI),*map(str,args)],capture_output=True,text=True)
        self.assertEqual(p.returncode==0,ok,p.stderr);return p

    def answers(self,perfect=False):
        a=copy.deepcopy(self.template);a['reviewer']={'actor':'synthetic-fixture','version':'test-v1','run_kind':'synthetic_control'}
        for case in a['cases']:
            case.update(method='audio_video',coverage_type='continuous',coverage=[[0,10]],sampled_fps=None)
            case['checks']={k:'pass' for k in case['checks']}
            if perfect:
                for event in self.gold[case['id']]['events']:
                    case['checks'][event['kind']]='fail'
                    case['findings'].append({'category':event['category'],'start':event['start'],'end':event['end'],'note':'Known synthetic fixture label'})
        return a

    def score(self,a):
        p=self.root/'answers.json';p.write_text(json.dumps(a))
        return json.loads(self.call('score',self.suite,p).stdout)

    def test_build_freezes_eight_encoded_controls_without_reviewer_labels(self):
        task=json.loads((self.suite/'reviewer/task.json').read_text())
        self.assertEqual(len(task['cases']),8);self.assertEqual(len(self.gold),8)
        self.assertEqual(len(list((self.suite/'reviewer').glob('*.mp4'))),8)
        self.assertTrue(all(set(c)=={'id','file','sha256','duration_seconds','width','height','fps'} for c in task['cases']))
        self.assertNotIn('expected',json.dumps(task));self.assertNotIn('\"events\"',json.dumps(task));self.assertNotIn('\"recipe\"',json.dumps(task))
        self.assertEqual(self.manifest['model_evaluation'],'not_performed')
        self.assertEqual(self.manifest['label_validation'],'authored_not_human_verified')
        before=(self.suite/'freeze.json').read_bytes();self.call('build',self.suite,ok=False)
        self.assertEqual(before,(self.suite/'freeze.json').read_bytes())
        self.call('verify',self.suite)

    def test_controls_use_browser_compatible_avc_and_aac(self):
        for case in self.manifest['cases']:
            path=self.suite/'reviewer'/case['file']
            probe=subprocess.run(['ffprobe','-v','error','-show_streams','-of','json',str(path)],capture_output=True,text=True,check=True)
            streams=json.loads(probe.stdout)['streams']
            video=next(s for s in streams if s['codec_type']=='video')
            audio=next(s for s in streams if s['codec_type']=='audio')
            self.assertEqual(video['codec_name'],'h264',case['id'])
            self.assertEqual(video['codec_tag_string'],'avc1')
            self.assertEqual(video['pix_fmt'],'yuv420p')
            self.assertEqual(audio['codec_name'],'aac')

    def test_encoded_perturbations_retain_the_authored_signals(self):
        qa=json.loads((self.suite/'operator/perturbation-qa.json').read_text())
        by_recipe={self.gold[k]['recipe']:v for k,v in qa['cases'].items()}
        self.assertTrue(all(abs(x-.65)<.05 for x in by_recipe['sync']['audio_minus_flash_seconds']))
        self.assertTrue(all(abs(x)<.05 for x in by_recipe['clean']['audio_minus_flash_seconds']))
        self.assertLess(by_recipe['freeze']['motion_pair_mae'],.05)
        self.assertGreater(by_recipe['clean']['motion_pair_mae'],.1)
        self.assertLess(by_recipe['black']['mid_luma_mean'],2)
        self.assertLess(by_recipe['tiny']['header_luma_range'],40)
        self.assertEqual(qa['semantic_label_validation'],'pending_human')

    def test_perfect_synthetic_answers_test_grader_without_qualifying_a_model(self):
        r=self.score(self.answers(True))
        self.assertEqual(r['counts']['true_positive'],6)
        self.assertEqual(r['counts']['false_positive'],0)
        self.assertEqual(r['counts']['false_negative'],0)
        self.assertEqual(r['counts']['unassessed_events'],0)
        self.assertEqual(r['model_evaluation'],'not_performed')
        self.assertEqual(r['qualification'],'diagnostic_only')

    def test_missing_action_matches_the_persistent_commanded_open_interval(self):
        for start,end in [(2,8),(3,8),(2,3)]:
            a=self.answers(True);row=next(c for c in a['cases'] if self.gold[c['id']]['recipe']=='missing')
            row['findings'][0].update(start=start,end=end)
            r=self.score(a)
            self.assertEqual(r['counts']['true_positive'],6)
            self.assertEqual(r['counts']['false_positive'],0)
            self.assertEqual(r['counts']['false_negative'],0)
        a=self.answers(True);row=next(c for c in a['cases'] if self.gold[c['id']]['recipe']=='missing')
        row['findings'][0].update(start=8,end=10)
        r=self.score(a)
        self.assertEqual(r['counts']['false_positive'],1);self.assertEqual(r['counts']['false_negative'],1)

    def test_all_green_fails_defect_cases_and_reports_missed_events(self):
        r=self.score(self.answers())
        self.assertEqual(r['counts']['false_negative'],6)
        self.assertEqual(r['counts']['false_pass_cases'],5)
        self.assertEqual(r['counts']['clean_correct_cases'],3)

    def test_false_alarm_on_clean_case_and_timing_mismatch_are_not_success(self):
        a=self.answers(True)
        clean=next(c for c in a['cases'] if not self.gold[c['id']]['events'])
        clean['checks']['motion']='fail';clean['findings']=[{'category':'freeze','start':4,'end':5,'note':'Deliberate false alarm'}]
        r=self.score(a);self.assertEqual(r['counts']['false_positive'],1);self.assertEqual(r['counts']['false_alarm_cases'],1)
        a=self.answers(True);c=next(c for c in a['cases'] if any(f['category']=='freeze' for f in c['findings']))
        c['findings'][0].update(start=0,end=1)
        r=self.score(a);self.assertEqual(r['counts']['false_negative'],1);self.assertEqual(r['counts']['false_positive'],1)

    def test_partial_and_sampled_inputs_stay_insufficient(self):
        a=self.answers()
        for c in a['cases']:c.update(method='frames',coverage_type='sampled',coverage=[[0,10]],sampled_fps=1)
        r=self.score(a)
        self.assertEqual(r['counts']['sufficient_cases'],0)
        self.assertEqual(r['counts']['false_pass_cases'],0)
        self.assertEqual(r['counts']['unassessed_events'],6)
        r=self.score(self.template);self.assertEqual(r['counts']['sufficient_cases'],0)

    def test_changed_media_or_gold_is_rejected_before_scoring(self):
        other=self.root/'tampered';shutil.copytree(self.suite,other)
        try:
            media=next((other/'reviewer').glob('*.mp4'));media.write_bytes(media.read_bytes()+b'changed')
            p=self.root/'answers.json';p.write_text(json.dumps(self.answers(True)))
            self.call('score',other,p,ok=False)
            shutil.rmtree(other);shutil.copytree(self.suite,other)
            (other/'operator/gold.json').write_text('{}')
            self.call('score',other,p,ok=False)
        finally:shutil.rmtree(other)

    def test_duplicate_or_stale_answers_do_not_grade(self):
        for mutation in ['duplicate','source','suite','timestamp']:
            a=self.answers(True)
            if mutation=='duplicate':a['cases'].append(copy.deepcopy(a['cases'][0]))
            if mutation=='source':a['cases'][0]['source_sha256']='0'*64
            if mutation=='suite':a['suite_sha256']='0'*64
            if mutation=='timestamp':
                c=next(c for c in a['cases'] if c['findings']);c['findings'][0]['start']=-1
            p=self.root/'bad.json';p.write_text(json.dumps(a));self.call('score',self.suite,p,ok=False)

    def test_unseen_second_event_is_unassessed_even_after_same_kind_rejection(self):
        a=self.answers(True)
        row=next(c for c in a['cases'] if any(f['category']=='av_sync' for f in c['findings']))
        row['coverage']=[[0,3]];row['findings']=row['findings'][:1]
        row['checks']={kind:'fail' if kind=='sync' else 'unknown' for kind in row['checks']}
        r=self.score(a)
        self.assertEqual(r['counts']['true_positive'],5)
        self.assertEqual(r['counts']['false_negative'],0)
        self.assertEqual(r['counts']['unassessed_events'],1)

    def test_spurious_audio_artifact_is_counted_as_false_alarm(self):
        a=self.answers(True);row=next(c for c in a['cases'] if not self.gold[c['id']]['events'])
        row['checks']['listening']='fail'
        row['findings']=[{'category':'audio_artifact','start':2,'end':2.15,'note':'Deliberate unsupported sound complaint'}]
        r=self.score(a);self.assertEqual(r['counts']['false_positive'],1);self.assertEqual(r['counts']['false_alarm_cases'],1)

    def test_duplicate_findings_cannot_double_count_a_detection(self):
        a=self.answers(True);row=next(c for c in a['cases'] if c['findings'])
        row['findings'].append(copy.deepcopy(row['findings'][0]))
        r=self.score(a);self.assertEqual(r['counts']['true_positive'],6);self.assertEqual(r['counts']['false_positive'],1)

    def test_reviewer_packet_rejects_unfrozen_extra_files(self):
        other=self.root/'extra-packet';shutil.copytree(self.suite,other)
        try:
            (other/'reviewer/gold-copy.json').write_text(json.dumps(self.gold))
            self.call('verify',other,ok=False)
        finally:shutil.rmtree(other)

    def test_exported_observations_are_accepted_by_unified_report(self):
        a=self.answers(True);p=self.root/'answers.json';p.write_text(json.dumps(a))
        case=next(c for c in a['cases'] if self.gold[c['id']]['events'])
        obs=json.loads(self.call('observations',self.suite,p,'--case',case['id']).stdout)
        op=self.root/'observations.json';op.write_text(json.dumps(obs))
        media=self.suite/'reviewer'/next(c['file'] for c in self.manifest['cases'] if c['id']==case['id'])
        run=subprocess.run([sys.executable,str(MEDIA),str(media),'--observations',str(op)],capture_output=True,text=True)
        self.assertEqual(run.returncode,0,run.stderr)
        result=json.loads(run.stdout);self.assertEqual(result['summary']['perceptual_result'],'rejected')
        self.assertFalse(result['publication_authorized'])

if __name__=='__main__':unittest.main()
