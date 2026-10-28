"""Bounded execution through the public CLI, using a local generated audio file."""
import json
import fcntl
import os
import signal
import time
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import wave

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'skills/video-production-router/scripts/project.py'
EXECUTOR = ROOT / 'skills/video-production-router/scripts/executor.py'


class ExecutorTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name); self.project = self.root / 'project.json'
        self.media = self.root / 'tone.wav'
        with wave.open(str(self.media), 'wb') as f:
            f.setnchannels(1); f.setsampwidth(2); f.setframerate(8000); f.writeframes(b'\0\0' * 8000)
        self.project_cli('create', self.project, '--goal', 'Local review', '--note', 'Synthetic')
        self.project_cli('retain', self.project, 'source', self.media, '--input')
        self.project_cli('asset', self.project, 'report', '--kind', 'review-report')
        self.project_cli('task', self.project, 'inspect', '--label', 'Inspect', '--requires', 'report')

    def call(self, script, *args, ok=True):
        p = subprocess.run([sys.executable, str(script), *map(str, args)], capture_output=True, text=True)
        self.assertEqual(p.returncode == 0, ok, p.stderr)
        return p

    def project_cli(self, *args, **kw): return self.call(PROJECT, *args, **kw)

    def run_executor(self, *extra, ok=True):
        return self.call(EXECUTOR, self.project, '--step', 'inspect', '--source', 'input:source',
                         '--output', 'report', *extra, ok=ok)

    def test_interrupted_intent_survives_restart_and_requires_explicit_reconciliation(self):
        import runpy
        P=runpy.run_path(str(PROJECT))
        S=runpy.run_path(str(EXECUTOR.with_name('executor_state.py')))
        data=P['load'](self.project)
        intent=S['begin'](data, 'inspect', {'tool':'local-media-review','output':'report','start':None,'end':None,'context':1.0,'request':None,'after_start':None,'after_end':None,'observe_resources':False},
                          {'input:source':data['inputs']['source']}, P)
        P['save'](self.project,data)
        status=json.loads(self.project_cli('status',self.project,'--json').stdout)
        self.assertNotIn('inspect',status['ready'])
        self.assertEqual(status['unresolved_attempts'][0]['attempt'],intent)
        self.run_executor('--execute',ok=False)
        proof=self.root/'recovery.txt';proof.write_text('Synthetic fixture: dispatch was never performed')
        self.project_cli('asset',self.project,'recovery','--kind','recovery-evidence')
        self.project_cli('retain',self.project,'recovery',proof)
        self.call(EXECUTOR.with_name('executor_state.py'),self.project,'--reconcile',intent,
                  '--outcome','not-submitted','--evidence','output:recovery')
        self.run_executor('--execute',ok=False) # explicit retry selection required
        self.run_executor('--execute','--retry-of',intent)
        data=P['load'](self.project)
        attempts=S['attempts'](data)
        self.assertEqual(len(attempts),2)
        self.assertEqual(attempts[-1]['state'],'produced')
        self.assertEqual(next(t for t in data['steps'] if t['id']=='inspect')['state'],'planned')

    def test_known_failure_requires_explicit_retry_and_changed_request_is_refused(self):
        self.project_cli('asset',self.project,'excerpt','--kind','review-preview')
        self.project_cli('task',self.project,'clip','--label','Clip','--requires','excerpt')
        args=[self.project,'--step','clip','--source','input:source','--output','excerpt','--tool','review-clip','--start','0','--end','0.5','--context','0.1','--execute']
        self.call(EXECUTOR,*args,ok=False) # audio source cannot satisfy video clip worker
        data=json.loads(self.project.read_text());attempt=next(e['attempt'] for e in data['history'] if e['action']=='executor_intent')
        before=self.project.read_bytes()
        self.call(EXECUTOR,*args,ok=False)
        self.assertEqual(before,self.project.read_bytes())
        changed=list(args);changed[changed.index('--end')+1]='0.6'
        self.call(EXECUTOR,*changed,'--retry-of',attempt,ok=False)
        self.assertEqual(before,self.project.read_bytes())
        self.call(EXECUTOR,*args,'--retry-of',attempt,ok=False) # admitted same attempt; still invalid input
        data=json.loads(self.project.read_text())
        self.assertEqual(sum(e['action']=='executor_intent' for e in data['history']),2)

    def test_resource_observation_is_opt_in_and_does_not_accept_output(self):
        result = json.loads(self.run_executor('--execute', '--observe-resources').stdout)
        self.assertIn(result['resources']['worker']['status'], ['observed','unavailable'])
        self.assertFalse(result['resources']['host']['workload_qualified'])
        self.assertEqual(result['state'], 'review_pending')
        data = json.loads(self.project.read_text())
        self.assertEqual(data['steps'][0]['state'], 'planned')
        event = next(e for e in reversed(data['history']) if e['action']=='executor_run')
        self.assertEqual(event['resources']['worker']['samples'], result['resources']['worker']['samples'])

    def test_preview_then_one_explicit_run_keeps_review_open(self):
        before = self.project.read_bytes()
        self.run_executor()
        self.assertEqual(before, self.project.read_bytes())
        self.run_executor('--execute')
        data = json.loads(self.project.read_text())
        self.assertIsNotNone(data['artifacts']['report']['file'])
        self.assertEqual(next(s for s in data['steps'] if s['id'] == 'inspect')['state'], 'planned')
        self.assertTrue((self.root / data['artifacts']['report']['file']['path']).is_file())
        self.run_executor('--execute', ok=False)

    def test_changed_source_or_unmet_dependency_blocks_execution(self):
        self.media.write_bytes(b'changed')
        before = self.project.read_bytes()
        self.run_executor('--execute', ok=False)
        self.assertEqual(before, self.project.read_bytes())

    def test_waiting_and_missing_dependencies_cannot_be_bypassed(self):
        self.project_cli('task', self.project, 'owner', '--label', 'Owner approval',
                         '--waiting-for', 'owner', '--note', 'Waiting for owner')
        self.project_cli('task', self.project, 'later', '--label', 'Later inspection',
                         '--after', 'owner', '--requires', 'report')
        before = self.project.read_bytes()
        self.call(EXECUTOR, self.project, '--step', 'later', '--source', 'input:source',
                  '--output', 'report', '--execute', ok=False)
        self.assertEqual(before, self.project.read_bytes())

    def test_unretained_or_unrelated_output_cannot_be_selected(self):
        self.project_cli('asset', self.project, 'other', '--kind', 'review-report')
        before = self.project.read_bytes()
        self.call(EXECUTOR, self.project, '--step', 'inspect', '--source', 'input:source',
                  '--output', 'other', '--execute', ok=False)
        self.assertEqual(before, self.project.read_bytes())

    def test_another_executor_holding_the_host_lock_blocks_execution(self):
        import runpy
        state = runpy.run_path(str(EXECUTOR.with_name('executor_state.py')))
        lock = state['host_lock_path']()
        with lock.open('a') as f:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            before = self.project.read_bytes()
            self.run_executor('--execute', ok=False)
            self.assertEqual(before, self.project.read_bytes())

    def test_host_lock_is_shared_across_different_scratch_directories(self):
        import runpy
        state = runpy.run_path(str(EXECUTOR.with_name('executor_state.py')))
        scratch = self.root / 'alternate-scratch'; scratch.mkdir()
        before = self.project.read_bytes()
        with state['host_lock_path']().open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            result = subprocess.run([sys.executable, str(EXECUTOR), str(self.project),
                '--step', 'inspect', '--source', 'input:source', '--output', 'report', '--execute'],
                env={**os.environ, 'TMPDIR': str(scratch), 'TMP': str(scratch), 'TEMP': str(scratch)},
                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Another Framewright executor is running', result.stderr)
        self.assertEqual(before, self.project.read_bytes())

    def interrupted_worker(self, signum):
        import runpy
        state = runpy.run_path(str(EXECUTOR.with_name('executor_state.py')))
        folder = self.root / 'tools'; folder.mkdir()
        marker = self.root / 'worker.json'
        fake = folder / 'ffmpeg'
        fake.write_text('#!' + sys.executable + '\nimport json,os,time\n'
                        'from pathlib import Path\n'
                        'Path(os.environ["FW_FIXTURE_PID"]).write_text(json.dumps({"pid":os.getpid(),"group":os.getpgrp()}))\n'
                        'for _ in range(400):\n Path(os.environ["FW_FIXTURE_PID"]).with_suffix(".alive").touch();time.sleep(.05)\n')
        fake.chmod(0o700)
        command = [sys.executable, str(EXECUTOR), str(self.project), '--step', 'inspect',
                   '--source', 'input:source', '--output', 'report', '--execute']
        parent = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            env={**os.environ, 'PATH':str(folder)+os.pathsep+os.environ['PATH'], 'FW_FIXTURE_PID':str(marker)})
        group = None
        try:
            deadline = time.monotonic()+15
            while not marker.exists() and time.monotonic()<deadline and parent.poll() is None:time.sleep(.05)
            self.assertTrue(marker.exists(), 'Owned fixture never reached inspection')
            row=json.loads(marker.read_text());group=row['group']
            parent.send_signal(signum);parent.wait(timeout=10)
            with state['host_lock_path']().open('a') as lock:
                if signum==signal.SIGKILL:
                    with self.assertRaises(BlockingIOError):fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
                else:
                    fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
                    alive=marker.with_suffix('.alive')
                    before=alive.stat().st_mtime_ns
                    time.sleep(.2)
                    self.assertEqual(alive.stat().st_mtime_ns,before,'Owned grandchild survived executor termination')
            data=json.loads(self.project.read_text())
            self.assertIsNone(data['artifacts']['report']['file'])
        finally:
            if group:
                try:os.killpg(group,signal.SIGKILL)
                except ProcessLookupError:pass
            if parent.poll() is None:parent.kill()
            parent.communicate(timeout=10)

    def test_sigterm_stops_owned_group_before_releasing_host_lock(self):
        self.interrupted_worker(signal.SIGTERM)

    def test_sigkill_keeps_host_lock_with_the_surviving_worker(self):
        self.interrupted_worker(signal.SIGKILL)

    def test_inherited_worker_deadline_survives_without_executor_supervision(self):
        import runpy
        state=runpy.run_path(str(EXECUTOR.with_name('executor_state.py')))
        launcher=self.root/'executor_worker.py'
        launcher.write_bytes(EXECUTOR.with_name('executor_worker.py').read_bytes())
        launcher.with_name('media_review.py').write_text('import time\ntime.sleep(20)\n')
        with state['host_lock_path']().open('a') as lock:
            fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
            worker=subprocess.Popen([sys.executable,str(launcher),str(lock.fileno()),'1','local-media-review'],
                pass_fds=(lock.fileno(),),start_new_session=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        try:
            worker.communicate(timeout=5)
            self.assertEqual(worker.returncode,-signal.SIGKILL)
            with state['host_lock_path']().open('a') as lock:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        finally:
            if worker.poll() is None:os.killpg(worker.pid,signal.SIGKILL)
            worker.communicate(timeout=5)

    def test_video_review_clip_is_bounded_and_requires_human_review(self):
        video = self.root / 'source.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i',
                        'testsrc=size=96x64:rate=24:duration=4', '-threads', '1',
                        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', str(video)], check=True)
        self.project_cli('retain', self.project, 'video', video, '--input')
        self.project_cli('asset', self.project, 'excerpt', '--kind', 'review-preview')
        self.project_cli('task', self.project, 'clip', '--label', 'Prepare review excerpt', '--requires', 'excerpt')
        args = [self.project, '--step', 'clip', '--source', 'input:video', '--output', 'excerpt',
                '--tool', 'review-clip', '--start', '1', '--end', '2', '--context', '0.5']
        before = self.project.read_bytes()
        self.call(EXECUTOR, *args)
        self.assertEqual(before, self.project.read_bytes())
        result = json.loads(self.call(EXECUTOR, *args, '--execute').stdout)
        self.assertEqual(result['state'], 'review_pending')
        self.assertEqual(result['interval'], {'start': 0.5, 'end': 2.5})
        output = Path(result['file']); self.assertTrue(output.is_file())
        duration = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries',
                          'format=duration', '-of', 'default=nw=1:nk=1', str(output)], text=True))
        self.assertAlmostEqual(duration, 2, delta=0.1)
        data = json.loads(self.project.read_text())
        self.assertEqual(next(s for s in data['steps'] if s['id'] == 'clip')['state'], 'planned')
        event = next(e for e in reversed(data['history']) if e['action'] == 'executor_run')
        self.assertEqual(event['source_pin']['sha256'], data['inputs']['video']['sha256'])
        self.call(EXECUTOR, *args, '--execute', ok=False)
        with video.open('ab') as f: f.write(b'changed revision')
        self.project_cli('retain', self.project, 'video', video, '--input', '--replace')
        state = json.loads(self.project_cli('status', self.project, '--json').stdout)
        self.assertTrue(any(r['subject'] == 'output:excerpt' for r in state['observations']['stale']))

    def test_clip_rejects_invalid_bounds_before_execution(self):
        self.project_cli('asset', self.project, 'excerpt', '--kind', 'review-preview')
        self.project_cli('task', self.project, 'clip', '--label', 'Clip', '--requires', 'excerpt')
        for start, end, context in [('3', '1', '1'), ('0', '3', '6'), ('0', 'nan', '1'), ('0', '29', '2')]:
            before = self.project.read_bytes()
            self.call(EXECUTOR, self.project, '--step', 'clip', '--source', 'input:source',
                      '--output', 'excerpt', '--tool', 'review-clip', '--start', start,
                      '--end', end, '--context', context, '--execute', ok=False)
            self.assertEqual(before, self.project.read_bytes())

    def test_invalid_source_records_failure_without_retaining_a_clip(self):
        self.project_cli('asset', self.project, 'excerpt', '--kind', 'review-preview')
        self.project_cli('task', self.project, 'clip', '--label', 'Clip', '--requires', 'excerpt')
        self.call(EXECUTOR, self.project, '--step', 'clip', '--source', 'input:source',
                  '--output', 'excerpt', '--tool', 'review-clip', '--start', '0',
                  '--end', '0.5', '--context', '0.1', '--execute', ok=False)
        data = json.loads(self.project.read_text())
        self.assertIsNone(data['artifacts']['excerpt']['file'])
        self.assertEqual(data['history'][-1]['result'], 'failed')

    def test_revision_comparison_uses_journal_and_stops_for_review(self):
        after = self.root / 'after.wav'
        with wave.open(str(after), 'wb') as f:
            f.setnchannels(1); f.setsampwidth(2); f.setframerate(8000); f.writeframes(b'\x01\x02' * 8000)
        self.project_cli('asset', self.project, 'after', '--kind', 'audio')
        self.project_cli('retain', self.project, 'after', after)
        spec = self.root / 'change.json'
        spec.write_text(json.dumps({'id':'fix', 'start':0.2, 'end':0.4, 'defect':'Noise',
                                    'desired':'Clean sound', 'preserve':['Timing']}))
        self.call(ROOT / 'skills/video-production-router/scripts/revisions.py', 'request', self.project,
                  'input:source', spec, '--output', self.root/'request.json')
        self.project_cli('asset', self.project, 'comparison', '--kind', 'revision-comparison')
        self.project_cli('task', self.project, 'compare', '--label', 'Compare versions', '--requires', 'comparison')
        args = [self.project, '--step', 'compare', '--source', 'output:after', '--output', 'comparison',
                '--tool', 'revision-comparison', '--request', 'output:revision:fix', '--context', '0.1']
        before = self.project.read_bytes()
        self.call(EXECUTOR, *args)
        self.assertEqual(before, self.project.read_bytes())
        result = json.loads(self.call(EXECUTOR, *args, '--execute').stdout)
        self.assertEqual(result['state'], 'review_pending')
        report = json.loads(Path(result['file']).read_text())
        self.assertEqual(report['result'], 'pending')
        self.assertTrue((Path(result['file']).parent/'before.wav').is_file())
        self.assertTrue((Path(result['file']).parent/'after.wav').is_file())
        data = json.loads(self.project.read_text())
        self.assertEqual(next(s for s in data['steps'] if s['id']=='compare')['state'], 'planned')
        self.assertEqual(data['artifacts']['comparison']['file']['sha256'],
                         data['artifacts'][report['subject'].removeprefix('output:')]['file']['sha256'])
        self.call(EXECUTOR, *args, '--execute', ok=False)
        with after.open('ab') as f: f.write(b'changed')
        self.project_cli('retain', self.project, 'after', after, '--replace')
        status = json.loads(self.project_cli('status', self.project, '--json').stdout)
        self.assertTrue(any(r['subject']=='output:comparison' for r in status['observations']['stale']))

    def test_comparison_rejects_unpaired_bounds_and_stale_request(self):
        self.project_cli('asset', self.project, 'comparison', '--kind', 'revision-comparison')
        self.project_cli('task', self.project, 'compare', '--label', 'Compare', '--requires', 'comparison')
        spec = self.root / 'change.json'
        spec.write_text(json.dumps({'id':'fix', 'start':0.2, 'end':0.4, 'defect':'Noise',
                                    'desired':'Clean sound', 'preserve':['Timing']}))
        self.call(ROOT / 'skills/video-production-router/scripts/revisions.py', 'request', self.project,
                  'input:source', spec, '--output', self.root/'request.json')
        args = [self.project, '--step', 'compare', '--source', 'input:source', '--output', 'comparison',
                '--tool', 'revision-comparison', '--request', 'output:revision:fix']
        before = self.project.read_bytes()
        self.call(EXECUTOR, *args, '--after-start', '0.2', '--execute', ok=False)
        self.assertEqual(before, self.project.read_bytes())
        self.media.write_bytes(b'changed')
        self.project_cli('retain', self.project, 'source', self.media, '--input', '--replace')
        before = self.project.read_bytes()
        self.call(EXECUTOR, *args, '--execute', ok=False)
        self.assertEqual(before, self.project.read_bytes())


if __name__ == '__main__': unittest.main()
