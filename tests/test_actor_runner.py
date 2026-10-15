import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('actors', Path(__file__).resolve().parents[1] / 'scripts/run_router_actors.py')
actors = importlib.util.module_from_spec(spec)
spec.loader.exec_module(actors)


class ActorRunnerTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        (self.root / 'runs/a').mkdir(parents=True)
        (self.root / 'runs/a/product.md').write_text('Synthetic authorised input')
        (self.root / 'a-prompt.txt').write_text('Read product.md only')
        (self.root / 'freeze.json').write_text(json.dumps({'prompt_sha256': {
            'a': hashlib.sha256(b'Read product.md only').hexdigest()}, 'source_tree_sha256': {}}))
        self.args = argparse.Namespace(codex_home=self.root, timeout=1)

    def run_fake(self, body):
        return actors.run_case(self.root, {'id': 'a'}, self.args, [sys.executable, '-c', body])

    def test_complete_raw_bytes_retained_and_reserved_against_overwrite(self):
        body = 'import pathlib,sys; pathlib.Path(sys.argv[-2]).write_text("answer"); print(\'{"type":"turn.started"}\'); print(\'{"type":"turn.completed"}\')'
        self.assertEqual(self.run_fake(body)['status'], 'ready_for_grading')
        raw = (self.root / 'evidence/a/events.jsonl').read_bytes()
        record = json.loads((self.root / 'evidence/a/execution.json').read_text())
        self.assertEqual(record['events_sha256'], hashlib.sha256(raw).hexdigest())
        with self.assertRaises(FileExistsError):
            self.run_fake(body)
        self.assertEqual(raw, (self.root / 'evidence/a/events.jsonl').read_bytes())

    def test_truncation_is_retained_and_not_sent_to_grader(self):
        self.assertEqual(self.run_fake('print("{truncated")')['status'], 'infrastructure_incomplete')
        self.assertEqual((self.root / 'evidence/a/events.jsonl').read_text(), '{truncated\n')
        record = json.loads((self.root / 'evidence/a/execution.json').read_text())
        self.assertTrue(record['capture']['parse_errors'])

    def test_timeout_retains_failure(self):
        self.assertEqual(self.run_fake('import time; print("partial", flush=True); time.sleep(10)')['status'], 'infrastructure_incomplete')
        record = json.loads((self.root / 'evidence/a/execution.json').read_text())
        self.assertEqual(record['exit_code'], 124)
        self.assertEqual((self.root / 'evidence/a/events.jsonl').read_text(), 'partial\n')

    def test_source_drift_blocks_launch(self):
        (self.root / 'runs/a/router').mkdir()
        (self.root / 'runs/a/router/SKILL.md').write_text('Unexpected changed source')
        with self.assertRaisesRegex(ValueError, 'source drift'):
            self.run_fake('raise SystemExit("must not run")')
        self.assertFalse((self.root / 'evidence/a/events.jsonl').exists())
