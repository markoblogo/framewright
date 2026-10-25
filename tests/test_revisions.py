"""Revision requests share the existing project journal; synthetic recordings only."""
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

@unittest.skipUnless(shutil.which('ffprobe') and shutil.which('ffmpeg'),'Existing FFmpeg required')
class RevisionTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.project=self.root/'project.json'
        self.cli('project.py','create',self.project,'--goal','Fixture','--note','Synthetic only')
        for name,level in [('before',4096),('after',8192)]:
            path=self.root/(name+'.wav')
            with wave.open(str(path),'wb') as f:
                f.setparams((1,2,8000,0,'NONE','uncompressed'));f.writeframes(level.to_bytes(2,'little',signed=True)*8000*3)
            self.cli('project.py','asset',self.project,name,'--kind','audio')
            self.cli('project.py','retain',self.project,name,path)
        self.spec=self.root/'change.json'
        self.spec.write_text(json.dumps({'id':'sound-fix','start':1,'end':1.4,'defect':'Quiet phrase',
                                         'desired':'Raise this phrase','preserve':['Timing','Other phrases']}))
        self.request=self.root/'request.json'

    def cli(self,script,*args,ok=True):
        r=subprocess.run([sys.executable,str(BASE/script),*map(str,args)],capture_output=True,text=True,timeout=30)
        self.assertEqual(r.returncode==0,ok,r.stderr)
        return r

    def request_it(self):
        self.cli('revisions.py','request',self.project,'output:before',self.spec,'--output',self.request)
        return json.loads(self.request.read_text())

    def test_request_records_defect_preservation_and_pinned_decision_without_changing_media_approval(self):
        before=self.project.read_bytes();req=self.request_it();data=json.loads(self.project.read_text())
        self.assertEqual(req['change']['preserve'],['Timing','Other phrases'])
        self.assertEqual(req['baseline']['sha256'],data['artifacts']['before']['file']['sha256'])
        self.assertEqual(data['journal'][-1]['result'],'proposed')
        self.assertIn('output:before',data['journal'][-1]['pins'])
        self.assertFalse(any(x['kind']=='creative' for x in data['journal']))
        saved=self.project.read_bytes()
        self.cli('revisions.py','request',self.project,'output:before',self.spec,'--output',self.root/'duplicate.json',ok=False)
        self.assertEqual(saved,self.project.read_bytes())

    def compare_it(self):
        self.request_it();folder=self.root/'comparison'
        self.cli('revisions.py','compare',self.project,self.request,'--after','output:after','--output',folder,'--context','.5')
        return folder,json.loads((folder/'report.json').read_text())

    def test_comparison_has_both_contexts_and_preservation_review_is_required(self):
        folder,report=self.compare_it()
        self.assertEqual(report['before']['start'],.5)
        self.assertEqual(report['after']['end'],1.9)
        self.assertEqual(report['result'],'pending')
        for name in ['before.wav','after.wav','review.md']:
            self.assertTrue((folder/name).exists())
        state=self.project.read_bytes();checks=self.root/'checks.json'
        checks.write_text(json.dumps({'change':{'result':'pass','note':'Fixture check'},'preserve':[]}))
        self.cli('revisions.py','review',self.project,folder/'report.json','--checks',checks,
                 '--result','accepted','--actor','fixture-editor','--provenance','operator_observation',ok=False)
        self.assertEqual(state,self.project.read_bytes())
        checks.write_text(json.dumps({'change':{'result':'pass','note':'Fixture change'},'preserve':[
            {'requirement':s,'result':'pass','note':'Synthetic verification only'} for s in ['Timing','Other phrases']]}))
        self.cli('revisions.py','review',self.project,folder/'report.json','--checks',checks,
                 '--result','accepted','--actor','fixture-editor','--provenance','operator_observation')
        data=json.loads(self.project.read_text());row=data['journal'][-1]
        self.assertEqual(row['result'],'accepted');self.assertEqual(row['kind'],'decision')
        self.assertIn(report['subject'],row['pins']);self.assertIn('output:after',row['pins'])
        self.assertFalse(any(r['kind']=='creative' for r in data['journal']))
        # Replacing after makes the acceptance stale, without resurrecting old receipts.
        self.cli('project.py','retain',self.project,'after',self.root/'before.wav','--replace')
        status=json.loads(self.cli('project.py','status',self.project,'--json').stdout)
        self.assertTrue(any(x['id']==row['id'] for x in status['observations']['stale']))

    def test_changed_baseline_or_comparison_file_blocks_review(self):
        folder,report=self.compare_it();checks=self.root/'checks.json'
        checks.write_text(json.dumps({'change':{'result':'pass','note':'Changed'},'preserve':[
            {'requirement':s,'result':'pass','note':'Kept'} for s in ['Timing','Other phrases']]}))
        (folder/'after.wav').write_bytes(b'changed')
        before=self.project.read_bytes()
        self.cli('revisions.py','review',self.project,folder/'report.json','--checks',checks,
                 '--result','accepted','--actor','editor','--provenance','operator_observation',ok=False)
        self.assertEqual(before,self.project.read_bytes())

    def test_timing_change_requires_explicit_after_range_and_new_names(self):
        self.request_it();before=self.project.read_bytes()
        self.cli('revisions.py','compare',self.project,self.request,'--after','output:after',
                 '--after-start','2.8','--after-end','4','--output',self.root/'bad',ok=False)
        self.assertEqual(before,self.project.read_bytes());self.assertFalse((self.root/'bad').exists())
        self.cli('project.py','retain',self.project,'before',self.root/'after.wav','--replace')
        self.cli('revisions.py','compare',self.project,self.request,'--after','output:after','--output',self.root/'bad',ok=False)

    def test_video_comparison_has_real_frames_and_older_attempt_cannot_be_accepted(self):
        for name,color in [('before','red'),('after','blue')]:
            f=self.root/(name+'.mp4')
            subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i',f'color={color}:s=96x64:r=24:d=3',
                            '-c:v','libx264','-threads','1',str(f)],check=True,capture_output=True)
            self.cli('project.py','retain',self.project,name,f,'--replace')
        self.request_it();folder=self.root/'video-compare'
        self.cli('revisions.py','compare',self.project,self.request,'--after','output:after','--output',folder)
        for name in ['before.png','after.png','before.mp4','after.mp4']:
            self.assertTrue((folder/name).is_file())
        import hashlib
        self.assertNotEqual(hashlib.sha256((folder/'before.png').read_bytes()).hexdigest(),hashlib.sha256((folder/'after.png').read_bytes()).hexdigest())
        self.cli('revisions.py','compare',self.project,self.request,'--after','output:after','--output',self.root/'new-compare')
        checks=self.root/'checks.json';checks.write_text(json.dumps({'change':{'result':'pass','note':'Fixture'},'preserve':[
            {'requirement':s,'result':'pass','note':'Fixture'} for s in ['Timing','Other phrases']]}))
        self.cli('revisions.py','review',self.project,folder/'report.json','--checks',checks,
                 '--result','accepted','--actor','fixture','--provenance','operator_observation',ok=False)

    def test_preview_change_after_acceptance_makes_the_receipt_stale(self):
        folder,report=self.compare_it();checks=self.root/'checks.json'
        checks.write_text(json.dumps({'change':{'result':'pass','note':'Fixture'},'preserve':[
            {'requirement':s,'result':'pass','note':'Fixture'} for s in ['Timing','Other phrases']]}))
        self.cli('revisions.py','review',self.project,folder/'report.json','--checks',checks,
                 '--result','accepted','--actor','fixture','--provenance','operator_observation')
        receipt=json.loads(self.project.read_text())['journal'][-1]['id']
        (folder/'after.wav').write_bytes(b'changed preview')
        status=json.loads(self.cli('project.py','status',self.project,'--json').stdout)
        self.assertTrue(any(r['id']==receipt for r in status['observations']['stale']))
