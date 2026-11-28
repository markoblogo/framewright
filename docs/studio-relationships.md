# Clients, partners and commitments

Implemented first agency slice, 27 November 2026. Extends the existing [studio management checkpoint](studio-production-management.md), [project journal](../skills/video-production-router/references/projects.md) and [agency direction](agency-operating-model.md). It is not a second CRM, task system or mail client.

## Owner boundary: correspondence control only

Framewright observes correspondence and records its implications for status, dates, priorities, budgets, dependencies and next actions. The owner writes and sends messages in another thread. Framewright does not compose/send replies, delete mail or archive threads. Existing external correspondence is evidence to track, not instructions to execute.

The owner explicitly authorised the initial Gmail organisation: a parent label spelled **Framewrite**, with project/counterparty child labels. Existing messages received additive labels only. No mail was sent, deleted or archived. This authorisation does not create an ongoing Gmail filter or background process.

An explicit follow-up date can produce a due flag in the local report. This is not a scheduled notification or automatic follow-up email. No new automation was created.

## Existing checkpoint, extended input

The same pinned schema-v1 studio-management input now accepts optional:
- `relationships`: stable ID, name, client/partner/provider roles, active/past/prospect/unknown state, responsible person, contact metadata, existing work IDs, source evidence, open questions and relationship next action;
- `commitments`: linked relationship/work, deliverables, who owes the result, internal_plan/proposed/agreed/fulfilled/cancelled state and evidence;
- `communications`: linked relationship, optional existing work/commitment, direction, draft/approved/sent/received/owner_reported state, timestamp, source, original-mail link and explicit reply/response expectations;
- `correspondence_observed_at`: the assembled correspondence snapshot's dated observation, separate from the time the report is generated.

Older budget-only profiles still open. Production work, blockers, targets and project paths come from the existing work list, not copied relationship statuses. Account costs remain in the existing cost ledger and are not copied into each card. A prospect with no agreed work has an empty work-ID list; it is not automatically an active project.

Each source refers to an input retained through project.py. The report checks pinned bytes/hashes and shows missing/changed/unretained evidence. Available evidence means the retained snapshot is intact, not that Gmail was just refreshed or the source's business claims independently proved true.

## Agreements and replies

A proposed or internal production date is not a contractual deadline. A committed deadline needs its own source; internal/proposed work dates stay in the work target. Agreed work requires agreement evidence; fulfilled work also requires completion evidence. One partner may have a completed review and an unrelated internal prototype without the prototype becoming another partner promise.

Gmail Sent/received records require a dated receipt reference. Owner-reported correspondence remains labelled owner_reported. These are recorded observations, never sending permissions. Drafts and approved drafts do not count as actual responses.

Explicit opposite-direction reply links support:
- waiting for the partner, or follow-up due when a date was recorded;
- an inbound request needing our response;
- a draft prepared elsewhere, which does not close that request;
- a sent response or an owner-reported response, kept distinct;
- source drift needing recheck.

An automated credit email does not answer an earlier technical question merely because it comes from the same company. A thank-you can acknowledge delivery without accepting a new commercial proposal. Unknown reply dates and commercial terms remain unknown.

## Read and resume

Use the ordinary project brief; it now includes a compact private relationship view and the full-report command. Public project summaries retain their explicit subject selection and do not inherit private counterpart/contact data.

```sh
python3 skills/video-production-router/scripts/project.py brief /absolute/studio/project.json --json
python3 skills/video-production-router/scripts/studio.py /absolute/studio/project.json
python3 skills/video-production-router/scripts/studio.py /absolute/studio/project.json --relationship example-partner
python3 skills/video-production-router/scripts/studio.py /absolute/studio/project.json --html /absolute/studio/review.html
```

A relationship filter narrows cards and work; shared account budgets remain account-wide. Reading and exporting the report do not modify the checkpoint. Export cannot overwrite the checkpoint or retained files. The HTML is the existing private studio report with added relationship cards, contacts, source state, obligations, waits and collapsible original-mail links. Valid undated drafts and owner-reported records display an unknown date rather than preventing export.

## Refresh without parallel records

1. Read the relevant existing Gmail labels/threads through the connected account, including Sent when determining who owes a reply. Search remaining Inbox/Updates when the owner selects that scope. Do not assume an unanswered inbound message before checking outgoing replies.
2. Retain a small versioned private receipt: message/thread IDs, dates, relevant headers/excerpts, source links and observed business facts. Keep invitation secrets, shipping addresses and unrelated mail out of public docs. This is a working evidence snapshot, not a full Gmail backup.
3. Reconcile the same management profile. Keep proposed rates, accepted orders, fulfilled delivery, provider notices and actual funding separate. Record changed scope/dates from their sources; do not start a project or move a source production's acceptance merely to match an email.
4. Retain the new receipt/profile revisions with project.py. Preserve previous referenced files. Regenerate studio.py and the ordinary brief; inspect evidence issues, explicit waits and current next actions.

The initial live update used the existing checkpoint lock, retained new inputs and the replacement profile through the normal journal, preserved the earlier management file and checked that cost events were unchanged. No production checkpoints were rewritten.

## First live reconciliation

Private source of truth: records/studio-management/project.json under the canonical external studio. The pinned profile, report.json and review.html are in that same directory.

The owner expanded the bounded reconciliation from selected relationships to relevant incoming notices and existing correspondence. Exact counterpart/message counts, mailbox references, source excerpts, shipment information and account observations remain in the private checkpoint. This is not a completeness claim about all historical mail or all customers.

The reconciliation distinguishes agreed review scope from an unknown publication date or delivery wait; completed materials from prospective work; unanswered enquiries from drafts prepared elsewhere; and account notices from confirmed budget funding. No placeholder clients, accepted paid orders or promised renewals were invented.

## Verification and remaining scope

Public CLI tests cover fresh-process recovery, old-profile compatibility, referential/agreement guards, source drift, bidirectional replies, draft/non-sent boundaries, internal dates, due flags, owner-only communication policy, HTML escaping, output protection and public-summary privacy. Existing studio budget tests and project-summary tests are retained. A private live receipt records actual verification results.

This slice does not poll Gmail automatically, send reminders on a schedule, execute messages, enforce external agreements, produce invoices or book provider credits from notification emails. Those boundaries do not stop the agent updating the existing records during an authorised review. Broader resource reconciliation and a full repeated agency-project follow-up remain the next separate development slices.
