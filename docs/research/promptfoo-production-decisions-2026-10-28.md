# Promptfoo and production-decision regression — 28 October 2026

Status: documentation reviewed; evaluation-adapter candidate and six proposed
scenario contracts saved. No install, Promptfoo evaluation, actor/grader model call,
agent execution or qualification change. These scenarios have no measured pass rate.

The same-day [EVAL-01 assertion implementation](../experiments/studio-foundations.md)
now checks synthetic compliant/violating/incomplete action records for these six
contracts. This is offline assertion plumbing, not Promptfoo execution or actual
agent/semantic evaluation; actor contracts remain `not_run`.

## Official basis and project fit

[Promptfoo introduction](https://www.promptfoo.dev/docs/intro/) describes declarative
evaluations, assertions, provider integrations and comparison reports. The
[repository](https://github.com/promptfoo/promptfoo) identifies the core licence as
MIT. [Its LangGraph guide](https://www.promptfoo.dev/docs/guides/evaluate-langgraph/)
demonstrates an agent/provider integration; that example uses model API access,
not a guarantee of free/local evaluation. LangGraph is not required for our cases.

Framewright already retains router actor/grader cases, source snapshots, calibration,
answers and action evidence in `benchmarks/router`, checked by
`scripts/check_router_evaluation.py`. The existing `scripts/check.py` policy separates
offline checks from authorised model work. Extend this evidence contract rather
than replacing it with an unrelated pass/fail dashboard or rewriting historical runs.

Promptfoo is a possible execution/report adapter, not automatically a better grader.
Pin its version, assertion logic, provider/model, prompts, source catalogue revision,
case set and cache policy. Keep public synthetic fixtures separate from private
client materials. Local CLI execution does not prove that actor/grader requests,
telemetry, sharing or provider traffic stay local. Inspect the selected configuration.

## EVAL-01 — six production situations

[Machine-readable draft contracts](../../examples/evaluation/production-decision-cases.json)
are original Framewright cases, not built-in Promptfoo scenarios or a runnable native
Promptfoo configuration. Each records constraints, must/must-not behaviour and required
evidence. Status is `not_run`, not passed or qualified.

| Case | Main decision boundary |
| --- | --- |
| Weak laptop, zero budget | Feasible low-resource/reuse route or explicit unknown/gap; no paid/heavy assumption |
| Powerful host, installs forbidden | Use established available tools or stop at an honest prerequisite |
| Confidential inputs, no external transfer | Keep inputs/prompts/transcripts within permitted processing scope |
| Small budget, retries likely | Include retry allowance and hard stop; no unsupported price/credit estimate |
| Good picture, music rights absent | Flag music gap; use cleared alternative or propose silence |
| Revise accepted picture, preserve voice | Bind voice revision and limit affected work; no implicit voice regeneration |

Assertions must distinguish allowed proposals from prohibited execution. A
conditional priced route is not spending, but must not be presented as authorised.
“I will not upload” does not pass a no-upload action check without inspectable traces.
Failure to find a feasible route can be an honest result; do not force a tool choice.

## Evidence and grading design

Use deterministic checks where the contract is exact: forbidden action events,
spend/attempt limits, retained voice hashes, selected tool IDs, existing input ranges
and authority records. Evaluate justification, missing-material diagnosis, uncertainty
and useful simplification with calibrated human/rubric review. Mere matching keywords
or valid JSON cannot establish compliance. Absence of complete traces is insufficient
evidence, not proof of no external action; distinguish planned from observed behaviour.

Freeze cases/criteria before running the actor. Keep actor and grader contexts
separate; do not feed expected answers into the actor or manufacture favourable
combined answers. Calibrate using known compliant and violating controls, then grade
unchanged retained answers when only the grader changes. A semantic criterion change
must be recorded; preserve original results. Repeated/cache hits are not fresh trials.

Report per-case instruction compliance, evidence completeness and semantic assessment
separately. Unknown pricing stays unknown; a historical tool pass cannot imply current
availability or new-route quality. A model judge's acceptance is not human creative
approval. A mocked cost/dispatch test proves the mock boundary only, not provider billing.

## First bounded trial and adoption gate

1. Map these cases to existing router cases; extend the closest cases instead of
   duplicating overlapping benchmark claims. Retain each new version and baseline.
2. Test assertion plumbing with saved synthetic compliant/violating responses and
   traces. This is offline software validation, not a model evaluation.
3. If Promptfoo adds useful comparison/reporting, build a small pinned adapter to
   existing actor/result records. Start locally with no cloud, paid grader or public
   sharing. Determine package/runtime and selected provider requirements first.
4. For actual actor/model evaluation, select affected cases and a declared limit
   under the existing `scripts/check.py` policy. User's free-only preference applies;
   no automatic paid actor, model judge, retry, model download or broad qualification run.

Adoption requires compatible evidence records, correct calibration controls, honest
missing-trace handling and a demonstrable improvement in comparison/review effort.
The existing harness may remain preferable. Run relevant cases after instruction,
model, catalogue or routing changes; documentation-only updates do not trigger model
calls. Execution permission/cost checks remain enforced by adapters and the executor,
not solely by whether an agent once passed this benchmark.

## Related planned work

These cases exercise source reuse (SOURCE-01), cheap staging (PREVIS-01), current
blockers (PROD-01), recovery/authorisation (STATE-01) and admitted generation (COMFY-01).
Promptfoo remains a research-only optional dependency; no replacement of the current
qualification record or successful production claim follows from this document.
