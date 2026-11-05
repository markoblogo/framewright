import json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'skills/video-production-router/scripts'))
import radar_auto as A
class AutoCheckpointTest(unittest.TestCase):
    def test_default_checkpoint_is_disabled(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'project.json';p.write_text('{}')
            self.assertEqual(A.checkpoint(p)['result'],'disabled')
            self.assertEqual(sorted(x.name for x in p.parent.iterdir()),['project.json'])
    def test_missing_exchange_does_not_break_saved_project_or_create_fallback(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);p=root/'project.json';p.write_text('{}');missing=root/'unmounted'/'exchange'
            (root/'radar-auto.json').write_text(json.dumps({'version':1,'enabled':True,'exchange_root':str(missing)}))
            self.assertEqual(A.checkpoint(p)['result'],'pending');self.assertFalse(missing.exists());self.assertEqual(p.read_text(),'{}')

class RealCheckpointTest(unittest.TestCase):
    from test_radar_exchange import StudioWorkflowTest as _Fixture
    setUp=_Fixture.setUp
    select=_Fixture.select
    def test_linked_checkpoint_publishes_stable_status_without_touching_project(self):
        self.select();before=self.project.read_bytes();A.enable(self.project,self.exchange)
        one=A.checkpoint(self.project);two=A.checkpoint(self.project)
        self.assertEqual(one['result'],'synced');self.assertEqual(one['message_id'],two['message_id']);self.assertEqual(self.project.read_bytes(),before)
    def test_saved_cli_checkpoint_triggers_enabled_exchange(self):
        import subprocess
        self.select();A.enable(self.project,self.exchange)
        result=subprocess.run([sys.executable,str(Path(A.__file__).parent/'project.py'),'describe',str(self.project),'--goal','Changed fixture','--note','test'],text=True,capture_output=True)
        self.assertEqual(result.returncode,0,result.stderr);self.assertIn('Radar exchange: synced',result.stdout)

    def test_malformed_optional_config_cannot_fail_saved_checkpoint(self):
        import subprocess
        self.select();(self.project.parent/'radar-auto.json').write_text('[]')
        result=subprocess.run([sys.executable,str(Path(A.__file__).parent/'project.py'),'describe',str(self.project),'--goal','Saved despite optional config','--note','test'],text=True,capture_output=True)
        self.assertEqual(result.returncode,0,result.stderr);self.assertIn('Saved checkpoint:',result.stdout);self.assertIn('pending',result.stdout)
        self.assertEqual(json.loads(self.project.read_text())['project']['goal'],'Saved despite optional config')
