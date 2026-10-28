# Editorial interchange and production accountability — 28 October 2026

Status: OTIO bounded export implemented and tested on the accepted MN7R draft;
[results](../experiments/otio-mn7r-handoff.md). A Kdenlive26.08.2 follow-up now
passes native import/edit/re-export/render, with metadata/ID loss and listening limits retained. Kitsu/Zou remains a model reference, without installation or integration.

## OTIO: accepted integration direction

[OpenTimelineIO](https://github.com/AcademySoftwareFoundation/OpenTimelineIO) is
an editorial interchange API. A native `.otio` describes ordered cuts, timing and
external media references. Its optional bundle formats are separate from this
first external-reference export. Licence reported by the repository: Apache-2.0.
Use the official Python library rather than a handwritten schema serializer.
See [adapters](https://opentimelineio.readthedocs.io/en/latest/tutorials/adapters.html)
and [format guidance](https://opentimelineio.readthedocs.io/en/latest/tutorials/otio-file-format-specification.html).

Preserve these boundaries:

1. Brief and creative decisions → scenes and production tasks → versioned materials.
2. A concrete cut binds those materials/ranges to timeline tracks and exact rates.
3. An OTIO adapter exports that cut; editor/build adapters consume it.

Framewright already separates scene `tell`/`show`, materials and variant edits in
[production compositions](../../skills/video-production-router/references/production.md).
Extend those entities; keep creative intent, approvals and rights in the journal.
Export namespaced metadata for project, scene, material and retained revision IDs.
Never export credentials or incidental private journal notes. Stable IDs/pins remain
authoritative even if an editor drops custom metadata. Unresolved media stays explicit.

### OTIO-01 — bounded export and editor check

First implementation: one variant, straight cuts, one video track, separate voice
and music tracks, gaps, external file references and exact source/timeline ranges.
Resolve the file from its retained revision, reject changed/missing sources, use
rate-aware frame arithmetic and record the export's input revision manifest.
Do not infer an audio range from text alone: require explicit timings or report
an unresolved track. Unsupported titles, effects, retiming and audio automation
must be reported or explicitly supplied as baked media, never silently dropped.

Internal trial: 20–30 seconds, three authorised fragments, narration and music.
Validate using the official library, reopen and compare clip IDs, order, in/out,
duration, gaps and track offsets. Then open in one available editor and inspect
media relinking, picture/sound synchronisation and duration. Choose/check that
editor's adapter/version before installation. Native round-trip success alone
does not establish editor interoperability or render parity. Include a deliberately
missing/replaced source and verify the diagnostic. Media stays outside Git.

Pass: exact tested timings/structure plus successful scoped editor opening and
human review, with unsupported features listed. Retain output pins, versions,
commands, observations and failure evidence. Bidirectional editing is a later scope;
external edits must never silently overwrite the production journal.

## Kitsu/Zou: model reference, optional future team integration

[Kitsu](https://github.com/cgwire/kitsu) is a collaboration platform;
[Zou](https://github.com/cgwire/zou) stores production entities, file metadata,
versioned previews and change events. [Current developer documentation](https://dev.kitsu.cloud/)
describes the Gazu Python SDK. The old gazu.cg-wire.com documentation flags itself
as unmaintained. Use current guides for any later integration.

[Task tracking](https://dev.kitsu.cloud/guides/task-tracking) distinguishes task
types (production steps) and task statuses (work states).
[Publishing/review](https://dev.kitsu.cloud/guides/publishing) is the separate
reference for result review. Our dual authoring/review-state design below is a
Framewright recommendation, not a claim of an identical upstream database schema.
Both Kitsu and Zou repositories identify AGPL-3.0. No upstream code is copied;
any later embedding, modification or distributed integration needs its own licence
assessment. A hosted API connection is not automatically cleared by this research.

Recommended mapping, using existing entities:

| Concept | Existing Framewright basis | Remaining work |
| --- | --- | --- |
| Production | Local project + brief | Reuse project identity |
| Shot / asset | Scene + material/passport | Explicit task-to-scene/material links where missing |
| Task / output version | Task + retained output pin | Keep production completion separate from review readiness |
| Review / decision | Revision-bound observations and topics | Show effective, rejected, pending and stale evidence clearly |
| History | Journal and task history | Explain the source event behind each blocker |
| Remaining work | `brief`, `resume --json`, production blockers | One concise evidence-based completion diagnosis |

### PROD-01 — completion diagnosis, extending the existing journal

Implementation update, 28 October: `project.py blockers` and a completion count in
`brief` now derive this view from existing records. [Internal validation](../experiments/completion-diagnosis.md)
covers absent/pending/rejected/stale evidence, waits and composition context. No new
task-scene storage links or Kitsu integration were introduced; context uses existing
declared mappings, and unmapped observations remain followups.

Proposed user question: “What currently prevents this film from being finished?”
Build the response from existing file problems, task dependencies, explicit waits,
variant requirements and effective observations, not conversation recall. Avoid a
second tracker/database or blanket status migration. Extend the existing brief/status
path; a convenience command can follow once its output contract is established.

Each blocker should identify project/variant, scene/material when mapped, task,
exact output revision, reason, source observation/event, waiting party if known,
affected dependants and next permitted action. Unknown ownership remains unknown.
Distinguish execution progress from review status: produced, ready for review,
accepted, changes requested, or stale are derived views, not automatic approval.
An existing wait cannot be cleared by a new render or a diagnostic command.

Internal acceptance cases: output absent; produced but listening pending; rejected
voice; approved version replaced; downstream mix stale after a source revision;
owner-deferred recording; all required checks satisfied. Rendering success must not
equal creative approval, publication or permission to proceed. Retain synthetic
fixtures and inspect an owner-selected real project read-only after unit checks.

## Sequence and integration gates

1. PROD-01: audit existing blocker coverage and add only missing links/explanations.
2. OTIO-01: build the bounded cut exporter and test one editor handoff sequentially.
3. Later, only for a concrete team-production need: evaluate optional Gazu/Zou API
   mapping, ownership, conflict handling, event cursors, privacy and licence conditions.

Kitsu/Zou is a reference reserve; no server setup or mandatory service dependency.
OTIO now has an optional common-CFR cut exporter, official0.18.1 readback and
three native DJV sample checks. The first full-editor re-edit/render gate passed
in Kdenlive26.08.2; other consumers, metadata preservation and listening remain separate.
The original trial proposal above is historical; actual source-specific scope and
failures are in the linked result. Source, installation, account and budget
boundaries remain per task; this record does not authorise new production.
