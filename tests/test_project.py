"""Production checkpoint behavior through the standalone CLI; synthetic files only."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / 'skills/video-production-router/scripts/project.py'

class ProjectTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.brief = self.root / 'brief.json'
        self.project = self.root / 'project.json'
        self.brief.write_text(json.dumps({'blocks':[{'id':'intro','input':'brand','duration_seconds':3}]}))

    def run_cli(self, *args, ok=True):
        p = subprocess.run([sys.executable,str(CLI),*map(str,args)],capture_output=True,text=True)
        self.assertEqual(p.returncode == 0, ok, p.stderr)
        return p

    def load(self):
        return json.loads(self.project.read_text())

    def create(self):
        self.run_cli('init',self.brief,self.project)

    def preflight(self):
        for step in ['source-review','preflight']:
            self.run_cli('mark',self.project,step,'--state','done','--evidence','Operator reviewed fixture; not a real media test')

    def output(self):
        f=self.root/'picture.bin';f.write_bytes(b'fixture output; not a video')
        self.run_cli('retain',self.project,'scene:1:video-export',f)
        return f

    def test_init_freezes_plan_without_execution_and_refuses_overwrite(self):
        self.create(); data=self.load(); before=self.project.read_bytes()
        self.assertEqual(data['plan']['execution'],'not_started')
        self.assertEqual(data['steps'][0]['state'],'planned')
        self.run_cli('init',self.brief,self.project,ok=False)
        self.assertEqual(before,self.project.read_bytes())

    def test_resume_preserves_progress_and_leaves_qa_unverified(self):
        self.create();self.preflight();self.output()
        self.run_cli('mark',self.project,'scene:1','--state','done','--evidence','Operator authored fixture')
        before=self.project.read_bytes()
        status=json.loads(self.run_cli('resume',self.project,'--json').stdout)
        self.assertIn('qa:scene:1:video-export',status['ready'])
        self.assertEqual(before,self.project.read_bytes())
        qa=next(s for s in self.load()['steps'] if s['id']=='qa:scene:1:video-export')
        self.assertEqual(qa['state'],'planned')
        self.assertEqual(self.load()['artifacts']['scene:1:video-export']['file']['inspection'],'not_decoded_by_project_cli')

    def test_cannot_finish_before_dependencies_files_or_evidence(self):
        self.create()
        self.run_cli('mark',self.project,'scene:1','--state','done','--evidence','not ready',ok=False)
        self.preflight()
        self.run_cli('mark',self.project,'scene:1','--state','done','--evidence','no file',ok=False)
        self.output()
        self.run_cli('mark',self.project,'scene:1','--state','done',ok=False)

    def test_changed_input_blocks_resume_and_explicit_repin_invalidates_progress(self):
        self.create();source=self.root/'source.txt';source.write_text('old')
        self.run_cli('retain',self.project,'source',source,'--input')
        self.preflight();self.output()
        self.run_cli('mark',self.project,'scene:1','--state','done','--evidence','authored')
        source.write_text('new')
        status=json.loads(self.run_cli('status',self.project,'--json').stdout)
        self.assertEqual(status['ready'],[])
        self.assertIn('input:source',status['file_problems'])
        self.run_cli('mark',self.project,'qa:scene:1:video-export','--state','done','--evidence','stale',ok=False)
        self.run_cli('retain',self.project,'source',source,'--input',ok=False)
        self.run_cli('retain',self.project,'source',source,'--input','--replace')
        self.assertTrue(all(s['state']!='done' for s in self.load()['steps']))
        self.assertGreater(len(self.load()['history']),3)

    def test_missing_output_and_replacement_invalidate_assembly(self):
        self.create();self.preflight();f=self.output()
        self.run_cli('mark',self.project,'scene:1','--state','done','--evidence','authored')
        f.unlink()
        self.assertIn('output:scene:1:video-export',json.loads(self.run_cli('status',self.project,'--json').stdout)['file_problems'])
        f.write_bytes(b'different output')
        self.run_cli('retain',self.project,'scene:1:video-export',f,'--replace')
        self.assertEqual(next(s for s in self.load()['steps'] if s['id']=='scene:1')['state'],'planned')

    def test_still_only_and_blocked_plans_do_not_invent_video_or_override_unmet(self):
        self.brief.write_text(json.dumps({'blocks':[{'id':'cover','input':'book-art','deliverables':['still-export']}]}))
        self.create()
        self.assertNotIn('assembly',[s['id'] for s in self.load()['steps']])
        other=self.root/'blocked.json'
        self.brief.write_text(json.dumps({'blocks':[{'id':'a','input':'book-art','language':'uk','preferred_voice':'mlx-audio','deliverables':['narration']}]}))
        self.run_cli('init',self.brief,other)
        self.run_cli('mark',other,'scene:1','--state','done','--evidence','cannot override',ok=False)

    def test_manifest_recovers_from_abandoned_temp_and_rejects_corruption(self):
        self.create();(self.root/'.abandoned.tmp').write_text('partial')
        self.run_cli('status',self.project)
        data=self.load();data['plan']['status']='tampered'
        self.project.write_text(json.dumps(data))
        before=self.project.read_bytes()
        self.run_cli('status',self.project,ok=False)
        self.assertEqual(before,self.project.read_bytes())

    def test_interrupted_atomic_write_keeps_previous_complete_checkpoint(self):
        self.create();before=self.project.read_bytes()
        import runpy
        from unittest.mock import patch
        module=runpy.run_path(str(CLI))
        data=self.load();data['history'].append({'action':'unfinished'})
        with patch('os.replace',side_effect=OSError('synthetic interrupted write')):
            with self.assertRaises(OSError):module['save'](self.project,data)
        self.assertEqual(before,self.project.read_bytes())
        self.run_cli('status',self.project)

    def test_another_writer_is_rejected_without_losing_checkpoint(self):
        import fcntl
        self.create();before=self.project.read_bytes()
        with Path(str(self.project)+'.lock').open('a') as stream:
            fcntl.flock(stream,fcntl.LOCK_EX|fcntl.LOCK_NB)
            p=self.run_cli('mark',self.project,'preflight','--state','blocked','--evidence','fixture',ok=False)
            self.assertIn('Another writer',p.stderr)
        self.assertEqual(before,self.project.read_bytes())

    def test_delivery_waits_for_final_listening_and_publication_is_separate(self):
        self.create();self.preflight();self.output()
        for step in ['scene:1','qa:scene:1:video-export']:
            self.run_cli('mark',self.project,step,'--state','done','--evidence','Synthetic operator record only')
        final=self.root/'final.bin';final.write_bytes(b'synthetic final')
        self.run_cli('retain',self.project,'final-video',final)
        for step in ['assembly','qa:final-video']:
            self.run_cli('mark',self.project,step,'--state','done','--evidence','Synthetic operator record only')
        self.run_cli('mark',self.project,'delivery','--state','done','--evidence','too early',ok=False)
        self.run_cli('mark',self.project,'listen:final-video','--state','done','--evidence','Synthetic silence check record; no media test')
        self.run_cli('mark',self.project,'delivery','--state','done','--evidence','Synthetic handoff record')
        status=json.loads(self.run_cli('resume',self.project,'--json').stdout)
        self.assertTrue(status['technical_handoff_recorded'])
        self.assertIn('publication',status['ready'])
        self.assertNotIn('publication',status['recorded_done'])

    def test_lock_is_released_when_writer_process_is_killed(self):
        self.create()
        code="import fcntl,sys; f=open(sys.argv[1],'a'); fcntl.flock(f,fcntl.LOCK_EX); print('locked',flush=True); sys.stdin.read()"
        child=subprocess.Popen([sys.executable,'-c',code,str(self.project)+'.lock'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        try:
            self.assertEqual(child.stdout.readline().strip(),'locked')
            child.kill();child.communicate(timeout=3)
            self.run_cli('mark',self.project,'preflight','--state','blocked','--evidence','Resumed after synthetic writer termination')
        finally:
            if child.poll() is None:child.kill();child.communicate(timeout=3)
