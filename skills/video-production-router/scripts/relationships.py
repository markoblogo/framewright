"""Linked agency records over the existing pinned studio-management profile.
Read-only projections: no mail transport, scheduler or second project store.
"""
from datetime import date, datetime
from hashlib import sha256
from html import escape
from pathlib import Path
from urllib.parse import urlsplit

ROLES = {"client", "partner", "provider"}
REL_STATES = {"active", "past", "prospect", "unknown"}
COMMITMENT_STATES = {"internal_plan", "proposed", "agreed", "fulfilled", "cancelled"}
MESSAGE_STATES = {"draft", "approved", "sent", "received", "owner_reported"}


def required_text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(label + " must be nonempty text")


def records(profile, key):
    rows = profile.get(key, [])
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        raise ValueError(key + " must be a list of records")
    ids = set()
    for row in rows:
        required_text(row.get("id"), key + " ID")
        if row["id"] in ids:
            raise ValueError("Duplicate " + key + " ID")
        ids.add(row["id"])
    return rows


def evidence(record):
    if not isinstance(record, dict):
        raise ValueError("Evidence needs a retained input reference")
    required_text(record.get("input_id"), "Evidence input ID")
    required_text(record.get("note"), "Evidence note")
    if record.get("basis") not in {"receipt", "retained_record", "owner_report"}:
        raise ValueError("Unknown evidence basis")


def moment(value):
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError("Communication timestamp needs timezone")
    return parsed


def validate(profile):
    relationships = records(profile, "relationships")
    commitments = records(profile, "commitments")
    messages = records(profile, "communications")
    work = {row["id"]: row for row in profile["work"]}
    relations = {row["id"]: row for row in relationships}
    promises = {row["id"]: row for row in commitments}
    mail = {row["id"]: row for row in messages}
    for row in relationships:
        required_text(row.get("name"), "Relationship name")
        required_text(row.get("responsible"), "Responsible person")
        roles = row.get("roles")
        if not isinstance(roles, list) or not roles or any(x not in ROLES for x in roles):
            raise ValueError("Relationship roles must be client/partner/provider")
        if row.get("status") not in REL_STATES:
            raise ValueError("Unknown relationship status")
        linked = row.get("work_ids")
        if not isinstance(linked, list) or any(x not in work for x in linked) or len(set(linked)) != len(linked):
            raise ValueError("Relationship must reference distinct existing work IDs")
        evidence(row.get("evidence"))
        if not isinstance(row.get("contacts", []), list):
            raise ValueError("Contacts must be a list")
        for contact in row.get("contacts", []):
            if not isinstance(contact, dict):
                raise ValueError("Contact must be a record")
            required_text(contact.get("channel"), "Contact channel")
            for field in ("name", "address"):
                if contact.get(field) is not None:
                    required_text(contact[field], "Contact " + field)
        questions = row.get("open_questions", [])
        if not isinstance(questions, list) or any(not isinstance(x, str) or not x.strip() for x in questions):
            raise ValueError("Open questions must be text")

    def linked(row, require_work):
        if row.get("relationship_id") not in relations:
            raise ValueError("Unknown relationship reference")
        work_id = row.get("work_id")
        if require_work or work_id is not None:
            if work_id not in work or work_id not in relations[row["relationship_id"]]["work_ids"]:
                raise ValueError("Record must reference work linked to its relationship")
        evidence(row.get("evidence"))

    for row in commitments:
        linked(row, True)
        required_text(row.get("title"), "Commitment title")
        if row.get("state") not in COMMITMENT_STATES or row.get("owed_by") not in {"studio", "counterparty", "unknown"}:
            raise ValueError("Unknown commitment state/responsibility")
        deliverables = row.get("deliverables")
        if not isinstance(deliverables, list) or not deliverables or any(not isinstance(x, str) or not x.strip() for x in deliverables):
            raise ValueError("Explicit commitment deliverables required")
        if row.get("deadline"):
            if row["state"] not in {"agreed", "fulfilled", "cancelled"}:
                raise ValueError("Internal/proposed work dates belong in the work target, not a committed deadline")
            date.fromisoformat(row["deadline"])
            evidence(row.get("deadline_evidence"))
        if row["state"] in {"agreed", "fulfilled"}:
            evidence(row.get("agreement_evidence"))
        if row["state"] == "fulfilled":
            evidence(row.get("completion_evidence"))

    for row in messages:
        linked(row, False)
        required_text(row.get("summary"), "Communication summary")
        required_text(row.get("channel"), "Communication channel")
        if row.get("state") not in MESSAGE_STATES or row.get("direction") not in {"inbound", "outbound"}:
            raise ValueError("Unknown communication state/direction")
        if row.get("occurred_at"):
            moment(row["occurred_at"])
        if row["state"] in {"sent", "received"}:
            if not row.get("occurred_at") or row["evidence"]["basis"] != "receipt":
                raise ValueError("Sent/received communication needs dated receipt evidence")
            if row["direction"] != ("outbound" if row["state"] == "sent" else "inbound"):
                raise ValueError("Communication state contradicts direction")
        if row["state"] in {"draft", "approved"} and row["direction"] != "outbound":
            raise ValueError("Only outbound messages can be drafts")
        if row["state"] == "approved":
            evidence(row.get("approval_evidence"))
        for flag in ("expects_reply", "needs_response"):
            if row.get(flag) is not None and type(row[flag]) is not bool:
                raise ValueError(flag + " must be boolean")
        if row.get("follow_up_on"):
            date.fromisoformat(row["follow_up_on"])
        if row.get("url"):
            parsed = urlsplit(row["url"])
            if parsed.scheme != "https" or not parsed.netloc:
                raise ValueError("Communication URL must use HTTPS")
        promise = row.get("commitment_id")
        if promise is not None and (promise not in promises or
                promises[promise]["relationship_id"] != row["relationship_id"] or
                row.get("work_id") != promises[promise]["work_id"]):
            raise ValueError("Communication commitment reference mismatch")
        reply = row.get("reply_to")
        if reply is not None:
            original = mail.get(reply)
            if not original or original["id"] == row["id"] or row["direction"] == original["direction"]:
                raise ValueError("Reply must reference the opposite direction")
            if original["relationship_id"] != row["relationship_id"] or original.get("work_id") != row.get("work_id"):
                raise ValueError("Reply relationship/work mismatch")
            expected = "sent" if original["direction"] == "outbound" else "received"
            if original["state"] not in {expected, "owner_reported"}:
                raise ValueError("Draft/approved messages cannot have received replies")
            if row.get("occurred_at") and original.get("occurred_at") and moment(row["occurred_at"]) < moment(original["occurred_at"]):
                raise ValueError("Reply cannot predate its original")


def report(data, profile, now, root):
    validate(profile)
    issues = {}
    cache = {}
    def source(item):
        if item is None:
            return None
        input_id = item["input_id"]
        if input_id not in cache:
            pin = data["inputs"].get(input_id)
            status = "not_retained"
            if pin:
                if root is None:
                    status = "not_checked"
                else:
                    path = (Path(root) / pin["path"]).resolve()
                    try:
                        raw = path.read_bytes()
                        status = "available" if len(raw) == pin["bytes"] and sha256(raw).hexdigest() == pin["sha256"] else "changed"
                    except OSError:
                        status = "missing"
            cache[input_id] = status
            if status != "available":
                issues[input_id] = {"input_id": input_id, "state": status}
        return {**item, "state": cache[input_id]}

    def project_link(row):
        path = row.get("project_file")
        if not path:
            return {"path": None, "state": "not_recorded"}
        if root is None:
            return {"path": path, "state": "not_checked"}
        resolved = (Path(root) / path).resolve()
        return {"path": str(resolved), "state": "available" if resolved.is_file() else "missing"}

    result = []
    for relation in profile.get("relationships", []):
        work = [{**w, "project_link": project_link(w)}
                for w in profile["work"] if w["id"] in relation["work_ids"]]
        promises = []
        for row in profile.get("commitments", []):
            if row["relationship_id"] != relation["id"]:
                continue
            deadline = row.get("deadline")
            closed = row["state"] in {"fulfilled", "cancelled"}
            date_state = "closed" if closed else "not_committed" if not deadline else "overdue" if date.fromisoformat(deadline) < now.date() else "due_today" if date.fromisoformat(deadline) == now.date() else "upcoming"
            projected = {**row, "evidence": source(row["evidence"]), "date_status": date_state}
            for field in ("agreement_evidence", "completion_evidence", "deadline_evidence"):
                if field in row:
                    projected[field] = source(row[field])
            promises.append(projected)
        communications = []
        for row in profile.get("communications", []):
            if row["relationship_id"] != relation["id"]:
                continue
            projected = {**row, "evidence": source(row["evidence"]), "reply_status": "not_requested", "response_status": "not_requested"}
            replies = [m for m in profile.get("communications", []) if m.get("reply_to") == row["id"]]
            if row["direction"] == "inbound" and row.get("needs_response"):
                states = {m["state"] for m in replies}
                projected["response_status"] = "responded" if "sent" in states else "response_owner_reported" if "owner_reported" in states else "response_approved" if "approved" in states else "draft_prepared" if "draft" in states else "needs_our_reply"
            if row["state"] in {"sent", "owner_reported"} and row["direction"] == "outbound" and row.get("expects_reply"):
                replies = [m for m in profile.get("communications", []) if m.get("reply_to") == row["id"]]
                projected["reply_status"] = "reply_received" if any(m["state"] == "received" for m in replies) else "reply_owner_reported" if replies else "awaiting_reply"
                if projected["reply_status"] == "awaiting_reply" and row.get("follow_up_on") and date.fromisoformat(row["follow_up_on"]) <= now.date():
                    projected["reply_status"] = "follow_up_due"
            if projected["evidence"]["state"] != "available" or any(source(m["evidence"])["state"] != "available" for m in profile.get("communications", []) if m.get("reply_to") == row["id"]):
                projected["reply_status"] = "needs_source_recheck"
                projected["response_status"] = "needs_source_recheck"
            if "approval_evidence" in row:
                projected["approval_evidence"] = source(row["approval_evidence"])
            communications.append(projected)
        communications.sort(key=lambda x: (moment(x["occurred_at"]).timestamp() if x.get("occurred_at") else float("-inf"), x["id"]))
        result.append({**relation, "evidence": source(relation["evidence"]), "work": work,
                       "commitments": promises, "communications": communications,
                       "latest_communication": communications[-1] if communications else None})
    attention = []
    for row in result:
        for mail in row["communications"]:
            if mail["reply_status"] in {"awaiting_reply", "follow_up_due", "needs_source_recheck"} or mail["response_status"] in {"needs_our_reply", "draft_prepared", "response_approved", "needs_source_recheck"}:
                attention.append({"relationship_id": row["id"], "message_id": mail["id"],
                                  "reply_status": mail["reply_status"], "response_status": mail["response_status"],
                                  "follow_up_on": mail.get("follow_up_on"), "url": mail.get("url")})
    return {"relationships": result, "correspondence_observed_at": profile.get("correspondence_observed_at"), "relationship_evidence_issues": list(issues.values()),
            "correspondence_attention": attention,
            "communication_policy": {"mode": "observe_only", "can_send": False,
                                     "can_delete": False, "can_archive": False,
                                     "owner_sends_in": "another thread", "reminders": "read_only_due_flags_no_scheduler"}}


def html(rows):
    def text(value):
        return escape(str(value if value is not None else "Unknown"))
    parts = ['<h2>Clients, partners and commitments</h2><p class="note">Observation only:the owner writes/sends in another thread. Linked to the existing work plan;internal plans are not partner promises. Mail receipts are dated observations,not live sync.</p>']
    for row in rows:
        parts.append('<article><h3>' + text(row["name"]) + '</h3><p>' + text(", ".join(row["roles"])) + ' · ' + text(row["status"]) + ' · Responsible: ' + text(row["responsible"]) + '</p>')
        for contact in row.get("contacts", []):
            parts.append('<p>Contact: ' + text(contact.get("name")) + ' · ' + text(contact.get("address")) + ' · ' + text(contact["channel"]) + '</p>')
        if row.get("gmail_label"):
            parts.append('<p>Gmail: ' + text(row["gmail_label"]) + '</p>')
        parts.append('<p class="note">Source: ' + text(row["evidence"]["input_id"]) + ' · ' + text(row["evidence"]["basis"]) + ' · ' + text(row["evidence"]["state"]) + '</p>')
        for promise in row["commitments"]:
            parts.append('<p><strong>' + text(promise["title"]) + '</strong> · ' + text(promise["state"]) + ' · owed by ' + text(promise["owed_by"]) + '<br>' + text("; ".join(promise["deliverables"])) + '<br>Committed deadline: ' + text(promise.get("deadline")) + ' · ' + text(promise["date_status"]) + '</p>')
        for work in row["work"]:
            parts.append('<p><strong>' + text(work["title"]) + '</strong> · ' + text(work["status"]) + '<br>Next: ' + text(work["next_step"]) + '<br>Internal target: ' + text(work.get("target_date")) + ('<br>Waiting: ' + text("; ".join(work["blockers"])) if work["blockers"] else '') + '<br>Project: ' + text(work["project_link"]["path"]) + ' · ' + text(work["project_link"]["state"]) + '</p>')
        if row.get("next_action"):
            parts.append('<p><strong>Relationship next step:</strong> ' + text(row["next_action"]) + '</p>')
        for question in row.get("open_questions", []):
            parts.append('<p class="wait">Open: ' + text(question) + '</p>')
        if row["communications"]:
            parts.append('<details><summary>Correspondence · ' + str(len(row["communications"])) + '</summary>')
            for mail in reversed(row["communications"]):
                link = '<a href="' + text(mail["url"]) + '">' + text(mail["summary"]) + '</a>' if mail.get("url") else text(mail["summary"])
                parts.append('<p>' + text(mail.get("occurred_at")) + ' · ' + text(mail["direction"]) + ' · ' + text(mail["state"]) + '<br>' + link + '<br>' + text(mail["reply_status"]) + ' · ' + text(mail["response_status"]) + ' · source ' + text(mail["evidence"]["state"]) + '</p>')
            parts.append('</details>')
        parts.append('</article>')
    return "".join(parts)
