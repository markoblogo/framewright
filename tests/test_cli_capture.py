import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('capture', Path(__file__).resolve().parents[1] / 'scripts/cli_capture.py')
capture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(capture)


def event(kind, identity='read', command='cat product.md', **fields):
    return {'type': kind, 'item': {'id': identity, 'type': 'command_execution', 'command': command, **fields}}


def stream(*items):
    return [{'type': 'thread.started'}, {'type': 'turn.started'}, *items, {'type': 'turn.completed'}]


class CaptureTest(unittest.TestCase):
    def test_turn_success_is_not_command_success(self):
        result = capture.inspect_events(stream(event('item.started')))
        self.assertFalse(result['complete'])
        self.assertTrue(result['turn_completed'])
        self.assertEqual(result['unfinished_command_ids'], ['read'])

    def test_parallel_commands_may_complete_out_of_order(self):
        events = stream(event('item.started', 'a'), event('item.started', 'b'),
                        event('item.completed', 'b', exit_code=0, status='completed'),
                        event('item.completed', 'a', exit_code=1, status='failed'))
        self.assertTrue(capture.inspect_events(events)['complete'])

    def test_invalid_lifecycle_is_not_evidence(self):
        good = [event('item.started'), event('item.completed', exit_code=0, status='completed')]
        variants = [good[1:], good + good[1:], [good[1], good[0]],
                    [good[0], event('item.completed', command='cat other', exit_code=0, status='completed')],
                    [good[0], event('item.completed', exit_code=None, status='in_progress')],
                    [good[0], event('item.completed', exit_code=True, status='completed')]]
        for items in variants:
            with self.subTest(items=items):
                self.assertFalse(capture.inspect_events(stream(*items))['complete'])

    def test_missing_turn_or_late_command_fails(self):
        self.assertFalse(capture.inspect_events(stream()[:-1])['complete'])
        self.assertFalse(capture.inspect_events(stream() + [event('item.started')])['complete'])

    def test_malformed_json_is_retained_as_error(self):
        events, errors = capture.parse_events('{"type":"turn.started"}\ntruncated\n[]\n')
        self.assertEqual(len(events), 1)
        self.assertEqual(len(errors), 2)

    def test_capture_does_not_promote_exit_zero_with_gaps(self):
        result = capture.assess('{"type":"turn.started"}\n', 0, True, True)
        self.assertFalse(result['ready_for_grading'])
        self.assertEqual(result['status'], 'infrastructure_incomplete')

    def test_no_login_is_part_of_runner_config(self):
        argv = capture.codex_args('codex', 'gpt-6.1-sol', 'medium', [])
        self.assertIn('allow_login_shell=false', argv)
        self.assertIn('read-only', argv)
