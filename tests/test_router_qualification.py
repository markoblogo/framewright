import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
import zipfile

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('evidence', REPO / 'scripts/check_router_evaluation.py')
evidence = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evidence)


class QualificationGateTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.packet = self.root / 'packet'
        shutil.copytree(REPO / 'benchmarks/router/2026-10-14/qa-v4', self.packet)
        # Reconstruct evaluated sources without Git or any historical object.
        with zipfile.ZipFile(self.packet / 'source-snapshot.zip') as archive:
            for name in archive.namelist():
                target = self.root / 'skills' / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(archive.read(name))
        self.record = {'schema_version': 1, 'status': 'model_checked_planning_scope', 'scope': 'synthetic_read_only_planning', 'packet': 'packet', 'case_ids': [x['id'] for x in json.loads((self.packet / 'cases.json').read_text())], 'model': 'gpt-6.1-sol', 'reasoning_effort': 'medium'}
        self.path = self.root / 'router-qualification.json'
        self.save()

    def save(self):
        self.path.write_text(json.dumps(self.record))

    def test_complete_qualification_needs_no_git_history(self):
        result = evidence.check_qualification(self.root, self.path)
        self.assertEqual(result['cases'], 30)
        self.assertEqual(result['status'], 'model_checked_planning_scope')

    def rehash_calibration(self, *names):
        cal = self.packet / 'calibration'
        p = cal / 'manifest.json'
        manifest = json.loads(p.read_text())
        for name in names:
            manifest['files'][name] = hashlib.sha256((cal / name).read_bytes()).hexdigest()
        p.write_text(json.dumps(manifest))
        parent = self.packet / 'manifest.json'
        main = json.loads(parent.read_text())
        main['calibration_manifest_sha256'] = hashlib.sha256(p.read_bytes()).hexdigest()
        parent.write_text(json.dumps(main))

    def test_unblinded_controls_cannot_promote(self):
        p = self.packet / 'calibration/manifest.json'
        manifest = json.loads(p.read_text())
        manifest['blind_ids'] = False
        p.write_text(json.dumps(manifest))
        self.rehash_calibration()
        with self.assertRaisesRegex(ValueError, 'blind'):
            evidence.check_qualification(self.root, self.path)

    def test_rewriting_gold_and_grade_together_cannot_change_frozen_control(self):
        cal = self.packet / 'calibration'
        p = cal / 'gold.json'
        gold = json.loads(p.read_text())
        identity = next(x for x, row in gold.items() if not row['expected_pass'])
        gold[identity]['expected_pass'] = True
        p.write_text(json.dumps(gold))
        p = cal / 'grades.json'
        grades = json.loads(p.read_text())
        row = next(x for x in grades['cases'] if x['id'] == identity)
        row[gold[identity]['group']][0]['verdict'] = 'PASS'
        p.write_text(json.dumps(grades))
        self.rehash_calibration('gold.json', 'grades.json')
        with self.assertRaisesRegex(ValueError, 'Frozen calibration gold'):
            evidence.check_qualification(self.root, self.path)

    def inject_actor_file(self, path):
        p = self.packet / 'results.json'
        rows = json.loads(p.read_text())
        for key in ('files_before', 'files_after'):
            rows[0]['execution'][key][path] = hashlib.sha256(b'contaminated input').hexdigest()
        p.write_text(json.dumps(rows))
        manifest_path = self.packet / 'manifest.json'
        manifest = json.loads(manifest_path.read_text())
        manifest['files']['results.json'] = hashlib.sha256(p.read_bytes()).hexdigest()
        manifest_path.write_text(json.dumps(manifest))

    def test_hidden_gold_cannot_enter_actor_workspace(self):
        self.inject_actor_file('router/references/scenarios.json')
        with self.assertRaisesRegex(ValueError, 'Hidden gold|actor router file set'):
            evidence.check_qualification(self.root, self.path)

    def test_extra_router_file_cannot_enter_actor_workspace(self):
        self.inject_actor_file('router/extra-context.md')
        with self.assertRaisesRegex(ValueError, 'actor router file set'):
            evidence.check_qualification(self.root, self.path)

    def test_retained_failed_complete_run_cannot_promote(self):
        shutil.rmtree(self.packet)
        shutil.copytree(REPO / 'benchmarks/router/2026-10-14/qa-v3', self.packet)
        self.record['case_ids'] = [x['id'] for x in json.loads((self.packet / 'cases.json').read_text())]
        self.save()
        self.assertEqual(evidence.check_packet(self.packet), {'cases': 30, 'passed': 29})
        with self.assertRaisesRegex(ValueError, 'Incomplete behavioural qualification'):
            evidence.check_qualification(self.root, self.path)

    def test_gap_status_cannot_hide_a_complete_pass(self):
        self.record['status'] = 'evaluated_with_gaps'
        self.save()
        with self.assertRaisesRegex(ValueError, 'Gap status needs'):
            evidence.check_qualification(self.root, self.path)

    def test_current_sources_can_retain_a_failed_evaluation_without_promotion(self):
        shutil.rmtree(self.packet)
        shutil.copytree(REPO / 'benchmarks/router/2026-10-14/qa-v3', self.packet)
        shutil.rmtree(self.root / 'skills')
        with zipfile.ZipFile(self.packet / 'source-snapshot.zip') as archive:
            archive.extractall(self.root / 'skills')
        self.record['status'] = 'evaluated_with_gaps'
        self.record['case_ids'] = [x['id'] for x in json.loads((self.packet / 'cases.json').read_text())]
        self.save()
        result = evidence.check_qualification(self.root, self.path)
        self.assertEqual(result['status'], 'evaluated_with_gaps')
        self.assertEqual((result['passed'], result['cases']), (29, 30))

    def test_v3_cannot_reuse_legacy_calibration(self):
        p = self.packet / 'freeze.json'
        data = json.loads(p.read_text())
        data['protocol_version'] = 3
        p.write_text(json.dumps(data))
        manifest_path = self.packet / 'manifest.json'
        manifest = json.loads(manifest_path.read_text())
        manifest['files']['freeze.json'] = hashlib.sha256(p.read_bytes()).hexdigest()
        manifest_path.write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, 'v3 needs fresh'):
            evidence.check_qualification(self.root, self.path)

    def test_partial_case_set_cannot_promote(self):
        self.record['case_ids'] = self.record['case_ids'][:8]
        self.save()
        with self.assertRaisesRegex(ValueError, 'case set'):
            evidence.check_qualification(self.root, self.path)

    def test_source_drift_invalidates_current_scope(self):
        p = self.root / 'skills/video-production-router/SKILL.md'
        p.write_text(p.read_text() + '\nChanged routing instructions.\n')
        with self.assertRaisesRegex(ValueError, 'Current source drift'):
            evidence.check_qualification(self.root, self.path)

    def test_unfrozen_routing_file_invalidates_current_scope(self):
        p = self.root / 'skills/video-production-router/references/new-rules.md'
        p.write_text('Different routing rules.')
        with self.assertRaisesRegex(ValueError, 'Current source set'):
            evidence.check_qualification(self.root, self.path)

    def test_rehashed_fixture_change_still_breaks_execution_record(self):
        p = self.packet / 'inputs.json'
        data = json.loads(p.read_text())
        data[0]['fixtures']['product.md'] += 'Invented product claim.'
        p.write_text(json.dumps(data))
        manifest_path = self.packet / 'manifest.json'
        manifest = json.loads(manifest_path.read_text())
        manifest['files']['inputs.json'] = hashlib.sha256(p.read_bytes()).hexdigest()
        manifest_path.write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, 'Fixture hash mismatch'):
            evidence.check_qualification(self.root, self.path)

    def test_rehashed_prompt_change_still_breaks_freeze(self):
        p = self.packet / 'inputs.json'
        data = json.loads(p.read_text())
        data[0]['prompt'] += '\nAltered prompt.'
        p.write_text(json.dumps(data))
        manifest_path = self.packet / 'manifest.json'
        manifest = json.loads(manifest_path.read_text())
        manifest['files']['inputs.json'] = hashlib.sha256(p.read_bytes()).hexdigest()
        manifest_path.write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, 'Prompt hash mismatch'):
            evidence.check_qualification(self.root, self.path)
