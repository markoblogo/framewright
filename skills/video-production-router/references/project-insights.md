# Derived status and content outcomes

These commands extend the [same production checkpoint](projects.md). They do not
create a second lifecycle, edit the frozen plan, connect analytics or upload media.
Python standard library; file checks hash local bytes and can take time on large masters.

## Start a session with a working brief

Completion diagnosis uses the same records:

```sh
python3 skills/video-production-router/scripts/project.py blockers local/film/project.json
python3 skills/video-production-router/scripts/project.py blockers local/film/project.json --json
```

It reports required open work, dependencies, missing/changed files, linked absent,
pending/rejected/stale reviews, explicit waits and declared variant requirements.
Rows include task/subject, current hash, the exact receipt and its original dependency
pins when present, source history indices, affected downstream tasks and scene/material/
variant context where mapped. File problems block readiness globally in the existing
CLI; source dependencies absent from the journal are not inferred from media contents.

Optional tasks, unmapped observations and changed planning sources are followups,
not newly invented mandatory gates. A manually completed check without a matching
observation is explicitly reported as missing evidence. No-recorded-blockers does
not establish rights, creative approval, publication readiness or permission to run.
Empty projects report undefined completion scope. Output is local/private; raw notes,
actors and paths in retained pins must be reviewed before sharing.

The default text limits each section to five rows (`--limit 1..20`); counts and JSON
expose omissions. `brief` includes the completion status/count. This read-only command
does not mark tasks, remove waits, approve versions or write the checkpoint.
[Internal validation and example](../../../docs/experiments/completion-diagnosis.md).

```sh
python3 skills/video-production-router/scripts/project.py brief local/film/project.json
python3 skills/video-production-router/scripts/project.py brief local/film/project.json --json --limit 3
```

This is a short **local** view of the same resume/journal facts, not another log.
It shows the recorded goal, latest non-stale accepted decisions/creative observations,
current file problems, recent retained replacements, declared-but-unretained outputs,
unresolved/stale checks, explicit waits, recorded constraints and ready tasks. Technical passes
are not creative acceptance. An older acceptance never overrides a later rejection.
Each list shows up to three items by default; `--limit 1..10` and totals expose omissions.

Current problems are differences from retained bytes. Replacement history is labelled
historical: no previous-session baseline or creative impact is invented. An approved
file's new revision removes its old acceptance from the preserved-work list and
surfaces the stale check. Existing task dependencies determine readiness. Explicit
waits remain waits; the command cannot interpret a new task or permission from prose.

The next step is a deterministic **proposal, not execution authority**: inspect file
problems first, then blocking evidence, an already ready task, an explicit wait,
a recorded constraint or unresolved checks. Creative suggestions must be labelled by the agent separately
and recorded through the ordinary decision journal only when appropriate. The command
never renders, approves, replans or writes the checkpoint. Its private notes are not
safe public copy; use the allowlisted `summary --public` below for publication.

On the existing two-Shorts project, a fresh brief preserves both master revisions,
detects the changed retained review log, shows pending listening checks and
explicit owner waits, and does not invent new production or audience results. The
changed log is reported for inspection, not silently repinned or treated as a
changed video. This verifies derivation only; reduced owner effort still needs a
future authorised production/reuse trial.

## Generate current documentation

```sh
python3 skills/video-production-router/scripts/project.py summary local/film/project.json
python3 skills/video-production-router/scripts/project.py summary local/film/project.json --json
python3 skills/video-production-router/scripts/project.py summary local/film/project.json --public --title 'Film status' --include output:final-video --output local/film/STATUS.md
```

The projection combines retained hashes with the **latest** observation per
subject/kind/topic. Files are declared, current, missing, changed or unavailable (for example,
permission denied). Observations
bound to a changed file or dependency are marked stale; an earlier acceptance never
reappears. Absence of a receipt means unknown, not approval. Each upload has its own
publication topic. Owner-reported publication is not independently checked visibility
or proof that the uploaded bytes equal the local master.

The local form includes file paths and latest project-wide decisions by topic. Public mode requires a title and explicit
subject allowlist. It excludes goals/context, paths, actors, raw notes, history,
source dependency labels and analytics values. Only explicitly `public` publication
URLs are exposed. Query/fragment data is removed except a valid YouTube watch `v`
identifier; unknown/unlisted/private links stay hidden. Review the selected title,
IDs and public URLs before committing; the generator cannot infer confidentiality
from an identifier or a path inside a URL.

An existing output requires `--replace`. `--check --output STATUS.md` compares
against the current projection without rewriting the document. Checkpoints, lock
files, retained sources and symlink destinations cannot be overwritten by this
export. Output is stable for an unchanged journal and file state; it has no changing
wall-clock stamp. Run the command after new receipts or before a documentation
commit. It is not a background watcher and cannot refresh private-file status in CI
without those files. The [real Shorts snapshot](../../../docs/experiments/trends-project-summary.json)
shows the safe output, including intentionally hidden visibility-unknown links.

## Record the idea before production when possible

Declare the future output and retain the dated source (Trends screenshot, Radar
report or owner brief). Hypothesis JSON:

```json
{
  "id": "cash-gap-v1",
  "statement": "A visible profit/cash contradiction may improve early attention.",
  "audience": "Entrepreneurs",
  "format": "youtube_short",
  "target": "output:final-video",
  "source": {"kind": "youtube_trends", "subject": "input:trend-source"}
}
```

```sh
python3 skills/video-production-router/scripts/project.py hypothesis local/film/project.json local/film/idea.json --actor owner --provenance owner_report
```

Source kinds: `youtube_trends`, `youtube_radar`, `owner_idea`, `other`. A retained
source pins the evidence. A declared target is sufficient; it need not exist yet.
The command records a **proposed** decision, not owner approval. Exact repetition
is a no-op; changed hypotheses need new IDs. Timing is `before_retained_master` or
`retrospective` according to the actual checkpoint at recording time. It cannot
establish that no earlier external production occurred, and does not backdate a
hypothesis. For an already closed project, retain retrospective source notes as an
additional evidence artifact; adding a new production input conservatively reopens
existing production tasks under the normal checkpoint rules.

## Import manually supplied outcomes

First record the exact master publication, retain a separate analytics screenshot
or report, then supply an outcome JSON. `publication` is the journal receipt ID,
not a video title or inferred channel match:

```json
{
  "id": "cash-gap-48h",
  "hypothesis": "cash-gap-v1",
  "publication": "e000005",
  "evidence": "input:analytics-report",
  "as_of": "2026-10-26T12:00:00Z",
  "published_at": "2026-10-24T12:00:00Z",
  "window": "lifetime",
  "metrics": {
    "views": null,
    "average_view_duration_seconds": null,
    "average_percentage_viewed": null,
    "impressions_ctr_percent": null,
    "monetization": "unknown",
    "estimated_revenue": null,
    "rpm": null,
    "currency": null
  }
}
```

```sh
python3 skills/video-production-router/scripts/project.py outcome local/film/project.json local/film/outcome.json --actor owner --provenance owner_report
python3 skills/video-production-router/scripts/project.py results local/film/project.json --json --compare-age-hours 48 --age-tolerance-hours 6
```

Use actual values when supplied; omitted metrics become null. Real zero stays zero.
Views must be nonnegative integers, CTR is 0–100; average percentage viewed may
exceed 100 for replayed Shorts. Revenue/RPM, including zero, require an explicit
three-letter currency. Monetization is independently `unknown`, `enabled`,
`disabled`, `not_eligible` or `not_available`. Currencies are never converted or
added. Estimated revenue is reported evidence, not a payout or a forecast.

`as_of` requires a timezone. `published_at` is optional and must be the **actual
upload time**; journal recording time is never a substitute. Windows are `lifetime`,
`unknown`, or `period` with `period_start`/`period_end`. Comparable-age selection
uses only non-stale lifetime snapshots within tolerance and actual upload time.
It exposes exclusion reasons, chooses the nearest snapshot per upload and does
not rank ideas or claim causality. Different topics are not a controlled A/B test.

Reports expose master/source/report hashes and supplied provenance. Conflicting
actual upload times for one receipt are rejected; review the source and record a
corrected publication receipt before attaching corrected analytics.

Snapshots are append-only by ID. New observations preserve earlier windows and
values. Missing/replaced master, source or analytics bytes mark results stale;
removed/superseded publications keep their historical metrics but cannot receive
new snapshots. Importing metrics never completes technical/creative checks or
publishes anything. Reports contain private commercial data: keep them local.
The public summary exposes only receipt status, not analytics values.
