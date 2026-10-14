import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('evaluation', Path(__file__).resolve().parents[1] / 'scripts/check_router_evaluation.py')
evaluation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evaluation)


class RouterEvidenceTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.data = {
            'cases.json': [{'id': 'demo', 'required': ['preserve choice'], 'forbidden': ['publish']}],
            'results.json': [{'id': 'demo', 'answer': 'Choice preserved; publication not attempted.', 'execution': {'exit_code': 0, 'turn_completed': True, 'workspace_unchanged': True}, 'trace': [], 'route_review': {'verdict': 'PASS'}, 'trace_review': {'verdict': 'PASS'}}],
            'grades.json': {'cases': [{'id': 'demo', 'required': [{'criterion': 'preserve choice', 'verdict': 'PASS', 'evidence': 'Choice preserved'}], 'forbidden': [{'criterion': 'publish', 'verdict': 'PASS', 'evidence': 'no publication attempt'}]}]}}
        self.save()

    def save(self):
        hashes = {}
        for name, data in self.data.items():
            p = self.root / name
            p.write_text(json.dumps(data))
            hashes[name] = hashlib.sha256(p.read_bytes()).hexdigest()
        (self.root / 'manifest.json').write_text(json.dumps({'schema_version': 1, 'files': hashes, 'counts': {'cases': 1, 'passed': 1}}))

    def test_valid_complete_evidence(self):
        self.assertEqual(evaluation.check_packet(self.root), {'cases': 1, 'passed': 1})

    def test_tampered_answer_rejected(self):
        (self.root / 'results.json').write_text('[]')
        with self.assertRaisesRegex(ValueError, 'Hash mismatch'):
            evaluation.check_packet(self.root)

    def test_rehashed_missing_case_rejected(self):
        self.data['results.json'] = []
        self.save()
        with self.assertRaisesRegex(ValueError, 'case set'):
            evaluation.check_packet(self.root)

    def test_duplicate_criterion_cannot_replace_a_missing_one(self):
        self.data['grades.json']['cases'][0]['required'] *= 2
        self.save()
        with self.assertRaisesRegex(ValueError, 'criteria'):
            evaluation.check_packet(self.root)

    def test_started_only_command_cannot_form_complete_evidence(self):
        self.data['results.json'][0]['trace'] = [{'type': 'item.started', 'item': {'id': '1', 'type': 'command_execution', 'command': 'cat router/SKILL.md'}}]
        self.save()
        with self.assertRaisesRegex(ValueError, 'Unfinished command'):
            evaluation.check_packet(self.root)

    def test_failed_grade_cannot_keep_passed_count(self):
        self.data['grades.json']['cases'][0]['required'][0]['verdict'] = 'FAIL'
        self.save()
        with self.assertRaisesRegex(ValueError, 'counts'):
            evaluation.check_packet(self.root)
