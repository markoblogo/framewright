# PROD-01 — read-only completion diagnosis

Implemented 28 October 2026 using the existing project journal, task dependencies,
file pins, observation projections and production composition. No second tracker,
database, external service, media production or automatic task completion.

`project.py blockers PROJECT.json` provides a bounded readable explanation;
`--json` provides all rows and provenance. `brief` shows status/count. Sources include
history indices, receipts and their original pins, current target hash, dependent
tasks and existing scene/material/variant mapping. Unmapped observations and optional
tasks remain followups. A missing required receipt is visible even when someone
manually marked the check done. Empty project scope is not declared finished.

The retained [synthetic example](../../examples/project-blockers/diagnosis.md) shows
an owner-deferred input and a pending listening check. It is a generated software
fixture, not a real customer production or evidence of media quality.

## Internal acceptance coverage

Public CLI tests create original text fixtures and check:

- Absent output; retained output awaiting listening; task and dependent-work mapping.
- Latest rejection supersedes earlier acceptance; replacement of a receipt dependency
  exposes stale evidence and reopens dependent work through existing lifecycle logic.
- Owner waits remain intact; every diagnosis leaves checkpoint bytes unchanged.
- Manually done check without receipt remains unresolved; all declared required
  checks satisfied yields no recorded blockers, without publication authority.
- Empty project scope, unmapped deferred decision, and scene/material/variant context.

No ASR, rendering, listening, visual understanding or audience effect is claimed.
Read-only usefulness on a selected real production remains to assess. The command
does not infer missing dependencies, owners, rights or approvals from conversation.
It reports the current declared scope, not an independent audit of every film need.

Verification: `python3 -m unittest discover -s tests -p test_project_blockers.py -q`.
Related project/lifecycle/summary checks passed 36 tests (including the eight new
diagnosis cases), working-brief checks passed six, and executor checks passed ten.
The final affected-task refinement was rechecked with all eight diagnosis cases.
Repository validation and whitespace checks passed. These are software checks, not
media/model evaluation. [Usage and boundaries](../../skills/video-production-router/references/project-insights.md).
