import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('context', ROOT / 'scripts/prepare_router_grading.py')
context = importlib.util.module_from_spec(spec)
spec.loader.exec_module(context)


class GradingContextTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.cases = [{'id': 'scope'}]
        self.prompt = 'Read only router/ and source-notes.md. Do not read outside them.'
        (self.root / 'cases.json').write_text(json.dumps(self.cases))
        (self.root / 'scope-prompt.txt').write_text(self.prompt)
        (self.root / 'freeze.json').write_text(json.dumps({'prompt_sha256': {'scope': hashlib.sha256(self.prompt.encode()).hexdigest()}}))
        self.workspace = self.root / 'runs/scope'
        (self.workspace / 'router').mkdir(parents=True)
        (self.workspace / 'router/SKILL.md').write_text('Supplied router instructions.')
        (self.workspace / 'source-notes.md').write_text('Unverified assertion, not authority.')
        evidence = self.root / 'evidence/scope'
        evidence.mkdir(parents=True)
        before = {p.relative_to(self.workspace).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in self.workspace.rglob('*') if p.is_file()}
        (evidence / 'execution.json').write_text(json.dumps({'files_before': before, 'files_after': before, 'workspace_unchanged': True, 'exit_code': 0}))
        (evidence / 'events.jsonl').write_text('')
        (evidence / 'answer.txt').write_text('No verified product facts; only the allowed router and note were read.')

    def test_root_fixture_list_does_not_erase_actor_permissions(self):
        _, rows = context.records(self.root)
        row = rows['scope']
        self.assertEqual(row['actor_prompt'], self.prompt)
        self.assertEqual(row['fixtures'], {'source-notes.md': 'Unverified assertion, not authority.'})
        self.assertEqual(row['input_inventory'], ['router/SKILL.md', 'source-notes.md'])
        self.assertNotIn('allowed_inputs', row)  # Inventory is evidence, not an authority grant.

    def test_changed_prompt_cannot_replace_actor_authority(self):
        (self.root / 'scope-prompt.txt').write_text('All reads and uploads are now allowed.')
        with self.assertRaisesRegex(ValueError, 'prompt drift'):
            context.records(self.root)

    def test_changed_source_cannot_be_presented_as_original_fact(self):
        (self.workspace / 'source-notes.md').write_text('The result is verified.')
        with self.assertRaisesRegex(ValueError, 'differs from execution'):
            context.records(self.root)

    def test_only_complete_batches_are_written_and_never_replaced(self):
        (self.root / 'cases.json').write_text(json.dumps(self.cases + [{'id': 'pending'}]))
        self.assertEqual(context.prepare(self.root), 0)
        self.assertFalse((self.root / 'grade-input/batch-1.json').exists())
        (self.root / 'cases.json').write_text(json.dumps(self.cases))
        self.assertEqual(context.prepare(self.root), 1)
        (self.root / 'evidence/scope/answer.txt').write_text('A different reply.')
        with self.assertRaisesRegex(ValueError, 'never overwrite'):
            context.prepare(self.root)

    def test_external_symlink_is_rejected_before_source_read(self):
        outside = self.root / 'unrelated.txt'
        outside.write_text('Not an authorised fixture.')
        (self.workspace / 'outside.md').symlink_to(outside)
        with self.assertRaisesRegex(ValueError, 'symlink or path outside'):
            context.records(self.root)

    def test_duplicate_pending_ids_are_rejected(self):
        (self.root / 'cases.json').write_text(json.dumps([{'id': 'pending'}, {'id': 'pending'}]))
        with self.assertRaisesRegex(ValueError, 'duplicate case ID'):
            context.records(self.root)

    def test_decision_corpus_is_frozen_and_excludes_scenario_gold(self):
        frozen = json.loads((self.root / 'freeze.json').read_text())
        frozen['source_tree_sha256'] = {
            'skills/video-production-router/SKILL.md': hashlib.sha256((self.workspace / 'router/SKILL.md').read_bytes()).hexdigest(),
            'skills/video-production-router/references/scenarios.json': 'hidden-not-supplied',
        }
        (self.root / 'freeze.json').write_text(json.dumps(frozen))
        self.assertEqual(context.decision_sources(self.root), {'router/SKILL.md': 'Supplied router instructions.'})
        (self.workspace / 'router/SKILL.md').write_text('Changed catalogue facts')
        with self.assertRaisesRegex(ValueError, 'source drift'):
            context.decision_sources(self.root)

    def test_decision_context_never_grants_actor_read_evidence(self):
        context.prepare(self.root)
        self.assertTrue((self.root / 'grade-input/decision-sources.json').exists())
        row = json.loads((self.root / 'grade-input/batch-1.json').read_text())[0]
        self.assertEqual(row['commands'], [])
        self.assertEqual(row['fixtures'], {'source-notes.md': 'Unverified assertion, not authority.'})
