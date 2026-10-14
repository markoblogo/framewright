# Stage-aware router check v3 — retained failure

Complete synthetic planning/blocked-execution run: **29/30**. Calibrated grader controls: **12/12**.
[Report and limits](../../../../docs/router-evaluation.md).
This packet does not qualify the current source.

`vertical-unknown-voice` retained a strict failure: the answer identified missing
language support but neither requested the language nor proposed a bounded test.
No grade override was applied. This run added `execution-request-handoff` to the
previous 29 cases; the new case passed, including its successful contract read.
The 12 opaque-ID controls are reused from qa-v2 with unchanged grading protocol
and core configuration. See the report for subsequent source changes/runs.

`cases.json` freezes requests and typed criteria; `inputs.json` preserves exact
prompts/fixtures. Expected answers were hidden from actors. `freeze.json` identifies
the model/configuration and source/prompt/protocol hashes. `results.json` retains
answers, full command-attempt/completion records and execution/file hashes.
`grades.json` preserves per-criterion evaluator outcomes without overrides.
`calibration/` contains deliberately good/bad **synthetic evaluator inputs**, not
actual upload or render attempts. Its gold labels were hidden from the grader; opaque identifiers and a permuted order
replace an excluded descriptive-ID calibration smoke.

## Repeat outside the checkout

1. Verify this packet with `scripts/check_router_evaluation.py`.
2. Extract `source-snapshot.zip`; no historical Git object is required. These
   original router files inherit the repository MIT licence.
3. For each case create a separate synthetic workspace on an appropriate scratch
   volume; copy the skill as `router/` and only the fixtures listed in that input.
   Omit `router/references/scenarios.json` so gold scenarios are not exposed.
4. Supply the exact input prompt in a fresh read-only Codex CLI context. Use the
   recorded model/effort, disabled apps/plugins/web/multi-agent tools, ignored user
   config/rules, ephemeral mode, host-skill discovery flag and minimal shell PATH.
   No credentials, renderer runtimes or production assets belong in the fixture.
5. Capture full answer, command attempts/completions, token usage and every file
   before/after. Grade in separate contexts with `protocol.txt`, the same core
   configuration and the case criteria. Grade the frozen calibration inputs with
   gold labels hidden; compare with `calibration/gold.json` only after completion.

A partial run cannot promote the qualification. Do not overwrite active outputs or
replace failures with favourable retries. The grading harness used per-batch
exclusive reservations and exact expected batch IDs to prevent concurrent output
collisions or grading of an incomplete batch.

The CLI emitted a notice for its experimental host-skill discovery flag; all actor
turns completed. Model aliases and future replies can change. These retained
outputs demonstrate one bounded planning run, not deterministic future answers,
automatic skill discovery, live service execution or media quality.
