"""Public checkpoint/CLI behaviours for linked agency records; fictional data only."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills/video-production-router/scripts"


class StudioRelationshipsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.project = self.root / "project.json"
        self.profile = self.root / "management.json"
        self.source = self.root / "correspondence.json"
        self.source.write_text('{"kind":"fictional test receipt"}')
        self.cli("project.py", "create", self.project, "--goal", "Example studio", "--note", "No network")
        self.cli("project.py", "retain", self.project, "mail-receipt", self.source, "--input")
        self.evidence = {"input_id": "mail-receipt", "basis": "receipt", "note": "Fictional Gmail read-back"}
        self.data = {
            "schema_version": 1, "services": [],
            "work": [{"id": "review", "title": "Example review", "category": "partner",
                      "priority": 1, "status": "waiting", "deadline": None,
                      "target_date": "2026-11-26", "next_step": "Wait for device",
                      "blockers": ["Device not delivered"], "budgets": []}],
            "relationships": [{"id": "partner", "name": "Example Partner", "roles": ["partner"],
                               "status": "active", "responsible": "owner", "work_ids": ["review"],
                               "contacts": [{"name": "Example Contact", "channel": "email",
                                             "address": "contact@example.test"}],
                               "evidence": self.evidence, "open_questions": ["Arrival date unknown"]}],
            "commitments": [{"id": "review-agreement", "relationship_id": "partner", "work_id": "review",
                             "title": "One honest review", "state": "agreed", "owed_by": "studio",
                             "deliverables": ["One landscape video"], "deadline": None,
                             "evidence": self.evidence, "agreement_evidence": self.evidence}],
            "communications": [{"id": "ask", "relationship_id": "partner", "work_id": "review",
                                "commitment_id": "review-agreement", "direction": "outbound",
                                "state": "sent", "channel": "email", "occurred_at": "2026-11-27T10:00:00+00:00",
                                "summary": "Asked for arrival estimate", "evidence": self.evidence,
                                "expects_reply": True, "follow_up_on": None,
                                "url": "https://mail.google.com/mail/u/0/#all/fictional"}]
        }
        self.pin()

    def cli(self, script, *args, ok=True):
        result = subprocess.run([sys.executable, str(SCRIPTS / script), *map(str, args)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode == 0, ok, result.stderr)
        return result

    def pin(self):
        self.profile.write_text(json.dumps(self.data))
        self.cli("project.py", "retain", self.project, "studio-management", self.profile,
                 "--input", "--replace")

    def view(self, *args):
        return json.loads(self.cli("studio.py", self.project, "--at",
                                   "2026-11-27T12:00:00+00:00", *args).stdout)

    def test_fresh_process_recovers_relationship_obligation_and_wait_without_writing(self):
        before = self.project.read_bytes()
        view = self.view()
        row = view["relationships"][0]
        self.assertEqual(row["id"], "partner")
        self.assertEqual(row["work"][0]["next_step"], "Wait for device")
        self.assertEqual(row["work"][0]["blockers"], ["Device not delivered"])
        self.assertIsNone(row["commitments"][0]["deadline"])
        self.assertEqual(row["commitments"][0]["date_status"], "not_committed")
        self.assertEqual(row["communications"][0]["reply_status"], "awaiting_reply")
        self.assertEqual(row["evidence"]["state"], "available")
        self.assertFalse(view["execution_authorized"])
        self.assertEqual(before, self.project.read_bytes())


    def test_normal_project_brief_exposes_same_relationships_and_readonly_recovery(self):
        before = self.project.read_bytes()
        brief = json.loads(self.cli("project.py", "brief", self.project, "--json").stdout)
        self.assertEqual(brief["studio_management"]["relationships"][0]["id"], "partner")
        self.assertIn("Example Partner", self.cli("project.py", "brief", self.project).stdout)
        self.assertEqual(before, self.project.read_bytes())
        self.source.write_text("changed receipt")
        view = self.view()
        self.assertEqual(view["relationship_evidence_issues"][0]["state"], "changed")
        self.assertEqual(view["relationships"][0]["communications"][0]["reply_status"], "needs_source_recheck")
        self.assertEqual(before, self.project.read_bytes())

    def test_drafts_and_owner_reports_cannot_be_promoted_to_verified_mail(self):
        mail = self.data["communications"][0]
        mail["state"] = "draft"
        self.pin()
        self.assertEqual(self.view()["relationships"][0]["communications"][0]["reply_status"], "not_requested")
        mail["state"] = "sent"
        mail["evidence"] = {**self.evidence, "basis": "owner_report"}
        self.pin()
        self.cli("studio.py", self.project, ok=False)
        mail["state"] = "owner_reported"
        self.pin()
        self.assertEqual(self.view()["relationships"][0]["communications"][0]["state"], "owner_reported")

    def test_reference_and_agreement_guards(self):
        original = copy.deepcopy(self.data)
        mutations = [
            lambda: self.data["relationships"][0]["work_ids"].append("missing"),
            lambda: self.data["relationships"].append(copy.deepcopy(self.data["relationships"][0])),
            lambda: self.data["commitments"][0].pop("agreement_evidence"),
            lambda: self.data["commitments"][0].update(state="fulfilled"),
            lambda: self.data["communications"][0].update(commitment_id="missing"),
            lambda: self.data["communications"][0].update(url="javascript:alert(1)"),
        ]
        for change in mutations:
            self.data = copy.deepcopy(original)
            change()
            self.pin()
            self.cli("studio.py", self.project, ok=False)

    def test_reply_clears_only_the_matching_outbound_request(self):
        sent = self.data["communications"][0]
        reply = {**copy.deepcopy(sent), "id": "answer", "direction": "inbound", "state": "received",
                 "occurred_at": "2026-11-27T11:00:00+00:00", "summary": "Will check",
                 "reply_to": "ask", "expects_reply": False}
        self.data["communications"].append(reply)
        self.pin()
        messages = self.view()["relationships"][0]["communications"]
        self.assertEqual(messages[0]["reply_status"], "reply_received")
        self.data["communications"][0]["state"] = "draft"
        self.pin()
        self.cli("studio.py", self.project, ok=False)

    def test_internal_targets_never_become_overdue_partner_obligations(self):
        promise = self.data["commitments"][0]
        promise["state"] = "internal_plan"
        self.pin()
        self.assertEqual(self.view()["relationships"][0]["commitments"][0]["date_status"], "not_committed")
        promise.update(state="agreed", deadline="2026-11-26", deadline_evidence=self.evidence)
        self.pin()
        self.assertEqual(self.view()["relationships"][0]["commitments"][0]["date_status"], "overdue")
        promise.update(state="fulfilled", completion_evidence=self.evidence)
        self.pin()
        self.assertEqual(self.view()["relationships"][0]["commitments"][0]["date_status"], "closed")

    def test_relationship_filter_and_html_are_private_readonly_projections(self):
        self.data["relationships"][0]["name"] = "<script>bad()</script>"
        self.pin()
        destination = self.root / "review.html"
        view = self.view("--relationship", "partner", "--html", destination)
        self.assertEqual(len(view["relationships"]), 1)
        self.assertIn("&lt;script&gt;bad()", destination.read_text())
        self.assertNotIn("<script>bad()", destination.read_text())
        self.cli("studio.py", self.project, "--relationship", "missing", ok=False)
        self.cli("studio.py", self.project, "--html", self.profile, ok=False)

    def test_profile_replacement_uses_existing_pin_history_and_preserves_costs(self):
        old = self.project.read_bytes()
        old_data = json.loads(old)
        previous = json.loads(self.cli("project.py", "brief", self.project, "--json").stdout)
        self.data["work"][0]["next_step"] = "Inspect arrived device"
        version = self.root / "management-v2.json"
        version.write_text(json.dumps(self.data))
        self.cli("project.py", "retain", self.project, "studio-management", version, "--input", "--replace")
        current = json.loads(self.project.read_text())
        self.assertEqual(current.get("costs"), old_data.get("costs"))
        self.assertGreater(len(current["history"]), len(old_data["history"]))
        self.assertEqual(previous["studio_management"]["relationships"][0]["work"][0]["next_step"], "Wait for device")
        self.assertEqual(self.view()["relationships"][0]["work"][0]["next_step"], "Inspect arrived device")
        self.assertEqual(json.loads(self.profile.read_text())["work"][0]["next_step"], "Wait for device")



    def test_client_role_and_public_summary_do_not_leak_private_contact_details(self):
        self.data['relationships'][0]['roles'] = ['client', 'partner']
        self.pin()
        self.assertEqual(self.view()['relationships'][0]['roles'], ['client', 'partner'])
        self.cli('project.py', 'asset', self.project, 'film', '--kind', 'video')
        public = self.cli('project.py', 'summary', self.project, '--public', '--title', 'Public result', '--include', 'output:film', '--json').stdout
        self.assertNotIn('contact@example.test', public)
        self.assertNotIn('Asked for arrival estimate', public)
        self.assertNotIn('mail.google.com', public)

    def test_legacy_budget_profile_without_relationships_still_opens(self):
        for key in ['relationships', 'commitments', 'communications']:
            self.data.pop(key)
        self.pin()
        self.assertEqual(self.view()['relationships'], [])
        self.assertEqual(self.view()['plan']['waiting'][0]['next_step'], 'Wait for device')

    def test_missing_profile_in_brief_is_a_recovery_issue_not_a_crash(self):
        self.profile.unlink()
        brief = json.loads(self.cli('project.py', 'brief', self.project, '--json').stdout)
        self.assertEqual(brief['studio_management']['state'], 'needs_recheck')


    def test_inbound_request_stays_open_until_actual_outbound_response(self):
        incoming = self.data['communications'][0]
        incoming.update(direction='inbound', state='received', needs_response=True, expects_reply=False)
        self.pin()
        self.assertEqual(self.view()['relationships'][0]['communications'][0]['response_status'], 'needs_our_reply')
        reply = {**copy.deepcopy(incoming), 'id': 'our-answer', 'direction': 'outbound',
                 'state': 'draft', 'summary': 'Draft rates', 'reply_to': 'ask',
                 'occurred_at': '2026-11-27T11:00:00+00:00', 'needs_response': False}
        self.data['communications'].append(reply)
        self.pin()
        self.assertEqual(self.view()['relationships'][0]['communications'][0]['response_status'], 'draft_prepared')
        reply['state'] = 'sent'
        self.pin()
        self.assertEqual(self.view()['relationships'][0]['communications'][0]['response_status'], 'responded')


    def test_due_flag_is_only_an_observation_and_never_sending_authority(self):
        self.data['communications'][0]['follow_up_on'] = '2026-11-27'
        self.pin()
        view = self.view()
        self.assertEqual(view['correspondence_attention'][0]['reply_status'], 'follow_up_due')
        self.assertFalse(view['communication_policy']['can_send'])
        self.assertFalse(view['communication_policy']['can_delete'])
        self.assertFalse(view['communication_policy']['can_archive'])
        self.assertEqual(view['communication_policy']['owner_sends_in'], 'another thread')


    def test_html_export_cannot_overwrite_a_linked_production_checkpoint(self):
        linked = self.root / "linked-production.json"
        linked.write_text('{"preserve":"original"}')
        self.data["work"][0]["project_file"] = str(linked)
        self.pin()
        original = linked.read_bytes()
        self.cli("studio.py", self.project, "--html", linked, ok=False)
        self.assertEqual(linked.read_bytes(), original)



    def test_single_relationship_filter_also_limits_correspondence_attention(self):
        other = copy.deepcopy(self.data['relationships'][0])
        other.update(id='other', name='Other partner', work_ids=[])
        self.data['relationships'].append(other)
        mail = copy.deepcopy(self.data['communications'][0])
        mail.update(id='other-mail', relationship_id='other', work_id=None)
        mail.pop('commitment_id')
        self.data['communications'].append(mail)
        self.pin()
        view = self.view('--relationship', 'partner')
        self.assertEqual([x['relationship_id'] for x in view['correspondence_attention']], ['partner'])

if __name__ == "__main__":
    unittest.main()
