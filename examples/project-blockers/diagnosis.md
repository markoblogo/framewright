# What prevents completion?

Fixture production

Status: recorded_blockers
Recorded blockers: 6; followups: 0

## Blockers

- explicit_wait / owner-recording: Owner deferred the recording
  Waiting for: owner
  Affected tasks: owner-recording
  Proposed action: Obtain the recorded input/decision; preserve the wait until explicitly resolved
- review_unresolved / listen: listening: pending
  Evidence: e000001 / pending
  Affected tasks: delivery, listen
  Proposed action: Inspect the exact revision/dependencies, perform the relevant review and record the outcome
- dependency / listen: Dependencies are not done
  Affected tasks: delivery, listen
  Proposed action: Resolve the listed dependencies first
- dependency / delivery: Dependencies are not done
  Affected tasks: delivery
  Proposed action: Resolve the listed dependencies first
- task_open / author: Task is not recorded done
  Affected tasks: author, delivery, listen
  Proposed action: Review the recorded task and its evidence before marking completion
- More: 1; use --json for all records.

## Followups

- None recorded

Derived local/private evidence only. No recorded blockers does not establish creative approval, rights clearance or publication readiness. Unmapped observations and optional tasks are followups.
