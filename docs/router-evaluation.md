# Router planning evaluation

**Current result: 29/29 cases pass the stage-aware planning rubric; the evaluator
passes 12/12 frozen controls.** [Scoped qualification](../router-qualification.json)
is tied to the exact decision sources, prompts, fixtures, protocol and complete
case set. [Current evidence packet](../benchmarks/router/2026-10-14/qa-v2/manifest.json).
No release is created by this update.

## What changed

The earlier test mixed planned checks with completed production work. It also
combined reuse of an existing thumbnail with a native-still request. The skill now
loads a [QA/handoff contract](../skills/video-production-router/references/handoff.md)
for production plans and finishing work. It requires an explicit source-to-copy
comparison, relevant runtime checks, intended artifacts and outstanding QA/handoff.
Checks have planned, blocked or verified status with evidence for verification.
Existing images, newly rendered native stills and extracted frames have separate
provenance and QA. Missing media blocks actual inspection, not describing the plan.

The new rubric marks each required criterion as `plan`, `observed` or `decision`.
A specific future/blocked check satisfies a planning criterion; an observed-source
criterion needs a successful completed read and supported facts. Generic “QA later”,
started-only reads, invented verification and unauthorised attempts still fail.

Twelve synthetic grader controls were labelled before grading, with gold labels
hidden from the evaluator. A descriptive-ID calibration smoke was excluded because
its IDs suggested the verdict; the published rerun uses opaque IDs and a permuted
order, with the same controls, gold decisions, protocol and model configuration.
Positive/negative pairs cover planned/absent QA,
existing/new native thumbnails, completed/started-only source reads, false media
verification, and attempted/rejected uploads. All twelve were classified correctly.
The packet checker requires the same protocol and grader configuration for controls
and actor grading; an always-passing grader fails the negative controls.

## Complete current run

Twenty-nine fresh actor contexts covered the existing 17 baseline scenarios,
music rights/source/credit boundaries, stop/comparison-only behaviour, source
injection, mixed toolchains, finishing without extra tools, and separate thumbnail
intents. Three added cases exercise existing-image reuse, source-backed copy and
an unverified “QA passed” note. Only authorised synthetic text fixtures were used.
The Remotion request now explicitly asks for a **new native PNG**. Its historical
ambiguous version remains in the old packets.

Model: `gpt-6.1-sol`, medium reasoning; Codex CLI `0.162.0-alpha.17.2`. Every actor
received the supplied skill and minimal fixtures without expected answers. Grading
used separate same-family contexts; the controller reviewed routes and all action
attempts. All 29 turns completed; fixture trees were unchanged; commands were
reads or permitted offline helper calls. No account, renderer, install, purchase,
upload or publication action was attempted. CLI feature warnings are retained as
diagnostics, not mistaken for action attempts or successful media QA.

| Run | Scope | Strict rubric | Disposition |
| --- | --- | --- | --- |
| Historical first | 23 cases | 19/23 | Preserved unchanged |
| Historical second | 26 cases | 22/26 | Preserved unchanged |
| Historical regression | 8 affected cases | 6/8 | Partial; not a qualification pass |
| Current stage-aware run | 29 cases | 29/29 | Complete bounded planning check |
| Current grader controls | 12 synthetic controls | 12/12 | Positive and negative controls agree |

The new run changes skill guidance, resolves rubric ambiguity and allows roughly
300–400 answer words where needed instead of the earlier roughly 200. Scores are
not a controlled measurement of the skill change alone. Historical grades were
not overwritten or reclassified to make the old suite green. No manual overrides
were used to obtain 29/29 in the new run.

## Reproduce and verify

Every packet includes its own `source-snapshot.zip`, verified member by member
against frozen hashes. Intermediate source commits are provenance labels, not a
reproduction dependency. A fresh shallow clone needs no old branch or Git object.
Inputs, complete answers, action-attempt/completion traces, grades, source hashes
and reported actor token usage are retained. Repeated command output is represented
by its bytes/hash; original full CLI streams stay locally retained. Diagnostic home
paths are minimised in the public packet. Monetary cost is unavailable; token counts
and summed worker seconds are not an account bill or wall-clock comparison.

```sh
python3 scripts/check_router_evaluation.py --root benchmarks/router --qualification router-qualification.json
```

The qualification gate requires a complete passing calibrated packet, all baseline
cases, exact current decision sources and consistent prompts/fixtures across every
actor. Tests reject partial promotion, changed/additional source files, rehashed
prompt/fixture substitution and rewriting gold labels to fit a grader result. CI also tests reconstruction without a Git history.
Changing decision sources invalidates the active scoped claim until it is refreshed.

For model repetition, follow the [packet guide](../benchmarks/router/2026-10-14/qa-v2/README.md).

## Qualified scope

The record is `model_checked_planning_scope`: the observed synthetic read-only
planning run with the named model/configuration. The general catalogue retains its
legacy structural status; renderer/media qualification is unchanged. Automatic
skill discovery, privileged execution, real account rights/spending, media quality,
audience outcomes, other models and statistical robustness are not qualified.
The restrictive envelope itself helps prevent actions, so these results do not
certify safety with real production privileges. No new video or musical trial was
published. Future transfer tests must freeze unseen cases and retain failures.
