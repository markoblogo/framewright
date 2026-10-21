"""Public media report and project import behavior; local synthetic fixtures only."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import wave

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'skills/video-production-router/scripts'

class MediaReviewTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.source=self.root/'voice.wav'
        with wave.open(str(self.source),'wb') as stream:
            stream.setnchannels(1);stream.setsampwidth(2);stream.setframerate(8000)
            stream.writeframes(b'\x00\x10'*8000)
        self.project=self.root/'project.json'

    def cli(self,script,*args,ok=True):
        p=subprocess.run([sys.executable,str(BASE/script),*map(str,args)],capture_output=True,text=True)
        self.assertEqual(p.returncode==0,ok,p.stderr)
        return p

    def report(self,observations=None):
        if not shutil.which('ffmpeg') or not shutil.which('ffprobe'):self.skipTest('Existing FFmpeg/ffprobe required')
        args=[self.source]
        if observations is not None:
            p=self.root/'observations.json';p.write_text(json.dumps(observations));args+=['--observations',p]
        return json.loads(self.cli('media_review.py',*args).stdout)

    def observation(self,method='audio',kind='listening',result='accepted',coverage=None):
        return {'source_sha256':hashlib.sha256(self.source.read_bytes()).hexdigest(),'reviews':[
            {'kind':kind,'actor':'fixture-reviewer','reviewer_version':'human-fixture',
             'provenance':'operator_observation','method':method,'coverage_type':'continuous',
             'coverage':[[0,1]] if coverage is None else coverage,'result':result,'findings':[]}]}

    def test_local_measurements_leave_perceptual_checks_pending_and_source_untouched(self):
        before=self.source.read_bytes();r=self.report()
        self.assertEqual(r['source']['sha256'],hashlib.sha256(before).hexdigest())
        self.assertEqual(r['technical']['decode']['result'],'pass')
        self.assertEqual(r['summary']['results']['listening'],'pending')
        self.assertIn('content',r['summary']['unresolved'])
        self.assertFalse(r['publication_authorized']);self.assertEqual(self.source.read_bytes(),before)
        self.assertEqual(r['technical']['calibration']['perceptual_review'],'not_performed')

    def test_partial_listening_and_transcript_never_approve_full_audio(self):
        r=self.report(self.observation(coverage=[[0,.3]]))
        self.assertEqual(r['summary']['results']['listening'],'pending')
        p=self.root/'bad.json';p.write_text(json.dumps(self.observation(method='transcript')))
        self.cli('media_review.py',self.source,'--observations',p,ok=False)

    def test_stale_observation_hash_is_rejected(self):
        obs=self.observation();obs['source_sha256']='0'*64
        p=self.root/'bad.json';p.write_text(json.dumps(obs))
        self.cli('media_review.py',self.source,'--observations',p,ok=False)

    def test_review_findings_are_visible_and_markup_is_literal(self):
        obs=self.observation(result='rejected');obs['reviews'][0]['findings']=[
            {'start':.1,'end':.2,'severity':'error','note':'![remote](https://example.test/pixel)',
             'action':'Record the line again','reshoot':True}]
        r=self.report(obs)
        self.assertEqual(r['summary']['results']['listening'],'rejected')
        self.assertEqual(len(r['summary']['reshoot']),1)
        rp=self.root/'report.json';rp.write_text(json.dumps(r))
        rendered=self.cli('media_review.py','--read',rp,'--format','markdown').stdout
        self.assertNotIn('![remote](',rendered)
        self.assertIn('Record the line again',rendered)

    def setup_project(self,r):
        report=self.root/'report.json';report.write_text(json.dumps(r))
        self.cli('project.py','create',self.project,'--goal','Fixture','--note','Synthetic only')
        self.cli('project.py','asset',self.project,'voice','--kind','audio')
        self.cli('project.py','retain',self.project,'voice',self.source)
        self.cli('project.py','retain',self.project,'review',report,'--input')
        self.cli('project.py','task',self.project,'listen','--label','Listen','--requires','voice','--check-kind','listening')
        return report

    def test_import_is_bound_to_source_and_report_and_never_finishes_tasks(self):
        r=self.report(self.observation());report=self.setup_project(r)
        self.cli('project.py','review',self.project,'output:voice','--report','input:review','--actor','fixture-operator')
        d=json.loads(self.project.read_text());self.assertEqual(d['steps'][0]['state'],'planned')
        receipts=d['journal'];self.assertEqual(len(receipts),3)
        self.assertTrue(all('input:review' in row['pins'] and 'output:voice' in row['pins'] for row in receipts))
        self.assertTrue(all(row['provenance']=='supplied_report' for row in receipts))
        self.cli('project.py','mark',self.project,'listen','--state','done','--evidence','Operator record')
        report.write_text(report.read_text()+'\n')
        self.cli('project.py','retain',self.project,'review',report,'--input','--replace')
        d=json.loads(self.project.read_text());self.assertEqual(d['steps'][0]['state'],'planned')
        self.assertTrue(json.loads(self.cli('project.py','status',self.project,'--json').stdout)['observations']['stale'])

    def test_import_rejects_wrong_media_and_tampered_summary_without_project_changes(self):
        r=self.report();report=self.setup_project(r)
        for change in ['hash','summary']:
            bad=copy.deepcopy(r)
            if change=='hash':bad['source']['sha256']='0'*64
            else:bad['summary']['results']['listening']='accepted'
            report.write_text(json.dumps(bad));self.cli('project.py','retain',self.project,'review',report,'--input','--replace')
            before=self.project.read_bytes()
            self.cli('project.py','review',self.project,'output:voice','--report','input:review','--actor','fixture',ok=False)
            self.assertEqual(self.project.read_bytes(),before)

    def test_video_frames_cannot_approve_motion_or_sync(self):
        if not shutil.which('ffmpeg'):self.skipTest('Existing FFmpeg required')
        video=self.root/'fixture.mp4'
        subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=black:s=64x64:r=10:d=1',
                        '-c:v','mpeg4',str(video)],check=True,capture_output=True)
        self.source=video;obs=self.observation(method='frames',kind='visual')
        obs['reviews'][0]['coverage_type']='sampled'
        r=self.report(obs);self.assertEqual(r['summary']['results']['visual'],'pending')
        self.assertIn('motion',r['summary']['unresolved']);self.assertNotIn('listening',r['summary']['results'])
        obs['reviews'][0]['kind']='motion';p=self.root/'bad.json';p.write_text(json.dumps(obs))
        self.cli('media_review.py',video,'--observations',p,ok=False)

    def test_accepted_review_cannot_request_reshoot_or_claim_unseen_timestamp(self):
        for reshoot,result,start in [(True,'accepted',.1),(False,'rejected',.8)]:
            obs=self.observation(result=result,coverage=[[0,.4]])
            obs['reviews'][0]['findings']=[{'start':start,'end':start+.1,'severity':'warning',
                'note':'Fixture finding','action':'Repeat fixture take','reshoot':reshoot}]
            p=self.root/'bad.json';p.write_text(json.dumps(obs))
            self.cli('media_review.py',self.source,'--observations',p,ok=False)

    def test_nonfinite_saved_report_is_rejected(self):
        r=self.report();r['technical']['calibration']['duration_seconds']=float('inf')
        p=self.root/'bad.json';p.write_text(json.dumps(r))
        self.cli('media_review.py','--read',p,ok=False)

    def test_report_size_limit_is_checked_before_parsing(self):
        p=self.root/'huge.json'
        with p.open('wb') as stream:stream.truncate(8*1024*1024+1)
        failure=self.cli('media_review.py','--read',p,ok=False)
        self.assertIn('8 MiB',failure.stderr)

    def test_decoder_failure_stays_failed_in_report_and_project_receipt(self):
        import os
        if not shutil.which('ffprobe'):self.skipTest('Existing ffprobe required')
        fake=self.root/'bin';fake.mkdir();decoder=fake/'ffmpeg'
        decoder.write_text('#!'+sys.executable+'\nimport sys\nsys.stderr.write("fixture broken frame")\nsys.exit(1)\n');decoder.chmod(0o700)
        env={**os.environ,'PATH':str(fake)+os.pathsep+os.environ.get('PATH','')}
        p=subprocess.run([sys.executable,str(BASE/'media_review.py'),str(self.source)],capture_output=True,text=True,env=env)
        self.assertEqual(p.returncode,0,p.stderr);r=json.loads(p.stdout)
        self.assertEqual(r['technical']['result'],'fail');self.assertIn('technical',r['summary']['unresolved'])
        self.setup_project(r)
        self.cli('project.py','review',self.project,'output:voice','--report','input:review','--actor','fixture')
        d=json.loads(self.project.read_text());self.assertTrue(any(x['kind']=='technical' and x['result']=='fail' for x in d['journal']))

    def test_source_size_cap_is_checked_before_external_tools(self):
        large=self.root/'too-large.wav'
        with large.open('wb') as stream:stream.truncate(1024*1024*1024+1)
        p=self.cli('media_review.py',large,ok=False)
        self.assertIn('1 GiB',p.stderr)

    def test_long_audio_keeps_calibration_unperformed_but_records_full_decode(self):
        with wave.open(str(self.source),'wb') as stream:
            stream.setnchannels(1);stream.setsampwidth(2);stream.setframerate(8000)
            stream.writeframes(b'\x00\x10'*(8000*61))
        r=self.report()
        self.assertEqual(r['technical']['result'],'pass')
        self.assertEqual(r['technical']['calibration_status'],'outside_short_capture_limits')
        self.assertIsNone(r['technical']['calibration'])
        # Final progress timestamps vary across FFmpeg versions: the Linux
        # runner reports 60.928s for this 61s WAV. Keep a bounded tolerance.
        self.assertAlmostEqual(r['technical']['decode']['decoded_seconds'],61,delta=.25)
        self.assertEqual(r['technical']['streams'][0]['sample_rate'],'8000')

    def test_success_exit_without_decode_progress_never_passes(self):
        import os
        if not shutil.which('ffprobe'):self.skipTest('Existing ffprobe required')
        fake=self.root/'bin';fake.mkdir();decoder=fake/'ffmpeg'
        decoder.write_text('#!'+sys.executable+'\n');decoder.chmod(0o700)
        p=subprocess.run([sys.executable,str(BASE/'media_review.py'),str(self.source)],capture_output=True,text=True,
                         env={**os.environ,'PATH':str(fake)+os.pathsep+os.environ.get('PATH','')})
        self.assertEqual(p.returncode,0,p.stderr)
        self.assertEqual(json.loads(p.stdout)['technical']['result'],'fail')

    def test_output_report_repin_reopens_check_and_dependant(self):
        r=self.report(self.observation());report=self.setup_project(r)
        self.cli('project.py','asset',self.project,'review-output','--kind','text')
        self.cli('project.py','retain',self.project,'review-output',report)
        self.cli('project.py','review',self.project,'output:voice','--report','output:review-output','--actor','fixture')
        self.cli('project.py','task',self.project,'delivery','--label','Deliver','--after','listen')
        for step in ['listen','delivery']:
            self.cli('project.py','mark',self.project,step,'--state','done','--evidence','Fixture operator record')
        r['generated_at']='2026-10-21T20:00:00+00:00';report.write_text(json.dumps(r))
        self.cli('project.py','retain',self.project,'review-output',report,'--replace')
        d=json.loads(self.project.read_text());self.assertTrue(all(x['state']=='planned' for x in d['steps']))

if __name__=='__main__':unittest.main()
