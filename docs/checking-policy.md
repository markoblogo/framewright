# Proportionate checks

Framewright is a methods library. Improving a document or adding a research candidate
must not trigger an expensive model benchmark or a media render. CI stays offline.

```sh
python3 scripts/check.py --scope docs --plan  # inspect the check plan; no work
python3 scripts/check.py --scope capture      # deterministic checks, no models/render
```

The same entry point is used by CI. It checks unit regressions, retained evidence,
links/catalogue, generated matrix and a temporary standalone-package smoke. Building
that temporary zip does not create or publish a release.

| Changed surface | Evidence needed before publication | Model work ceiling for a routine patch |
| --- | --- | --- |
| Prose, research queue, links | Offline checks and source review | 0 |
| CLI capture/infrastructure | Synthetic malformed/unfinished/timeout fixtures, then affected trace smoke | Up to 8 explicitly named actors, once each |
| Router selection or authority rules | Deterministic boundary regression and frozen affected actor requests | Up to 8 affected cases by default; broader claims need a separately scoped run |
| Grader/criteria | Negative and positive frozen controls; unchanged-answer replay | No new actors unless actor source/request changes |
| New production tool | Agreed product, inputs, budget and acceptance criteria | One bounded experiment; no automatic full router benchmark |

A ceiling is not a target. Stop once the relevant claim has evidence. These are
work-allocation rules, not claims that eight cases prove general reliability or
that a call ceiling fixes token billing. Runtime timeout is enforced per actor;
account price and final bill remain separately unavailable unless measured.

## Capture before grade

Use the reusable runner on a **prepared frozen fixture root** with `cases.json`,
`freeze.json`, `<id>-prompt.txt`, and `runs/<id>/router` plus declared fixture files.
The freeze names source and prompt SHA-256 hashes. Prepare an isolated Codex home
without inherited user/project rules and grants; keep authentication outside Git.

```sh
python3 scripts/run_router_actors.py /path/to/frozen-run --case CASE_ID
# Preview is the default. Execution is separately explicit:
python3 scripts/run_router_actors.py /path/to/frozen-run --case CASE_ID \
  --codex-home /path/to/isolated-codex-home --execute
python3 scripts/prepare_router_grading.py /path/to/frozen-run
```

Default: one worker, 240 seconds per actor, at most eight named cases, no retries.
Two workers are available explicitly. Raising the case cap is an explicit operator
choice, not an automatic response to a failure. Sources/prompts are checked before
launch; an existing attempt directory cannot be overwritten. Keep actor workspaces
separate from the evidence directory.

Login shells are disabled **only in the actor harness**, not in the user's terminal
or global Codex settings. Raw stdout/stderr, command/config, answer, before/after
file hashes, duration and readiness are retained per attempt. No malformed JSON
line is silently dropped. A completed answer/exit 0 is insufficient: each started
command needs one matching terminal event with an exit code, inside a complete
turn. Nonzero command exits remain visible for semantic review.

Incomplete capture is infrastructure evidence; block grading/public qualification
and retain the attempt. Do not manufacture completion events, infer success from a
later read, or retry until a favourable answer appears. A separately declared
technical follow-up retains the first attempt and does not turn known cases into
unseen tests. The checker is not a sandbox: use an isolated home and OS permissions
for execution, then review every attempted action before a behavioural claim.

## Preserve useful progress

Keep three distinct records: routing/semantic failures, grader disagreements, and
capture/runtime failures. Repair only the affected layer. Reuse unchanged valid
controls/evidence with exact provenance; do not relabel old answers as fresh results.
Do not combine a targeted follow-up with an earlier full run into a new full-run
score. Full qualification changes require their own frozen protocol and complete
evidence. A known limitation can remain documented while a new useful tool is
researched; it does not require another broad benchmark every turn.
