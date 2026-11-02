# Storage and regular sanitation

Owner policy, 1 November 2026. Applies to Framewright work on this Mac.

## One external home

Canonical studio root: `/Volumes/Work/Work/FramewrightStudio`.

| Directory | Purpose |
| --- | --- |
| `repository/` | Framewright source and committed documentation |
| `productions/PROJECT/` | One film's final package, reusable sources and recipe |
| `tools/` | Retained portable applications and necessary reusable runtimes |
| `records/` | Compact research, reviews, release evidence and maintenance records |
| `workspace/` | Migrated legacy chat workspace; old internal entry contains shortcuts only |
| `incoming/` | Temporary incoming media, cleared after import |
| `scratch/` | Rebuildable render/test output, cleared after acceptance |

No new studio folders in the external volume root or internal Downloads/Desktop/
Documents. `/Volumes/Work/framewright` and `/Volumes/Work/framewright-local-tools`
may remain compatibility symlinks; their data lives under the studio root.
The Codex internal workspace root must remain a real directory: the executor
rejects symlinked writable roots. Keep only small entry instructions and child
shortcuts there, with no media or runtime copies. Do not weaken sandbox settings
to replace this entry directory with a symlink.
Other projects, books, personal archives, system files and AI model stores are
outside the studio cleanup scope. Do not reorganize them as incidental cleanup.

## Keep the result and the knowledge

At production closeout keep one accepted master per requested aspect/language,
the selected cover, metadata/subtitles, rights/provenance, decision and failure
notes, and the final editable recipe/scene with indispensable source assets.
Check the selected recipe's input references before classifying frames or assets
as cache. Retiring historical frame sources is an explicit availability decision;
it must not be described as preserving a fully rebuildable historical production.
Keep expensive-to-recreate source clips only when needed for reuse or correction.
Published YouTube copies do not replace the local accepted master.

Remove superseded full-film exports, intermediate cuts, per-frame render caches,
failed previews, duplicate delivery ZIPs when their verified contents are kept,
redundant source copies and downloaded installers after successful installation.
Do not keep every historical binary merely because a document mentioned it;
record that it was retired and retain its historical hash/QA/decision if useful.
Never call a removed version still locally available or reproducible.

An ongoing correction may temporarily keep the accepted original and one candidate.
After the decision keep the selected result; retain extra evidence only for a
specific unresolved issue. Paused productions and reusable provider originals
need an explicit retention decision, not an automatic age-based purge.

## Internal disk is temporary

Prefer external storage for all media, downloads, test environments and model
weights. Do not create a fresh virtual environment or download weights per film
when a shared, versioned external runtime is appropriate.

Use the internal disk only for a selected speed-sensitive temporary job. Declare
its exact scratch directory, estimated size and deletion point first. Start with
at least 20 GiB free, or defer/choose an external route; stop new heavyweight jobs
below 10 GiB. Do not consume the remaining system/swap reserve to finish a render.
Space-reclaiming maintenance itself does not require that starting reserve.

Move files sequentially: copy a small batch, compare SHA-256 and byte counts,
then remove that exact internal source. If verification fails, keep the source.
Avoid filling Trash with gigabytes of already verified generated duplicates.
Do not follow symlinks into unrelated folders. Record old/new paths and deletions.
While a large model download is active, prefer same-volume renames and small
rate-limited transfers; do not start a second large download or renderer.

## Software and cadence

Keep a small tested working set. Remove failed, rarely used or deferred trial
applications and their installers; retain version, outcome, reinstall URL and
known limitations in the tool catalogue. Removal is not a negative quality verdict.
Do not remove shared tools, an active runtime, Codex/browser state, credentials,
or model stores as a routine cache purge.

Run a short sanitation pass after an accepted/published film, before a release,
before any large install/model download, and weekly when actively producing.
This is a checklist in the work loop, not a newly scheduled background deletion.
Check both disks, identify the exact owned targets, finish the current operation,
prune intermediates, verify any transfers and report free space. Never schedule
blind recursive deletion. New ambiguous targets require clarification.

## Maintenance evidence

The private `records/storage-2026-11-01/` directory contains the move map,
before/deletion inventories, verified transfer receipts and final free-space
snapshot. Existing historical evidence remains historical; current availability
must be checked at the new canonical location.

[First sanitation report and exceptions](storage-maintenance-2026-11-01.md).
