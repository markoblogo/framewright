# Router behaviour evaluation

Completed bounded decision checks on 2026-10-14. The catalogue remains
`structural_only`: this experiment did not achieve a full qualification-suite pass
or establish unrestricted execution safety. [Retained packets and case-level grades](../benchmarks/router/2026-10-14/README.md).

## What was tested

The 17 existing scenarios plus six frozen boundary cases covered route selection,
explicit Anatomy/Flute/Remotion choices, comparison-only and stop requests, EN/FR,
unknown language/vertical constraints, mixed scene/layer plans, failed snapshot
fallback, free/noncommercial music, locked source references, visual-generation
credit gates and an untrusted source asking for credential access/publication.
A second full run added three held-out paraphrases. No account or provider call,
installation, renderer or public upload was part of these tests.

Each actor had a fresh synthetic read-only workspace and the supplied skill, without
expected answers. Model: gpt-6.1-sol, medium; CLI: 0.162.0-alpha.17.2. Separate
same-family evaluator contexts graded required/forbidden criteria; the controlling
agent also reviewed route choices and every command attempt. That is separate
context grading, not a claim of third-party independence or statistical robustness.

## Results and fixes

| Run | Scope | Strict rubric | Route/action review |
| --- | --- | --- | --- |
| First | 23 complete cases | 19/23 | Chosen routes matched; no out-of-envelope attempt |
| Second | 26 complete cases | 22/26 | Chosen routes matched; no out-of-envelope attempt |
| Final regression | 8 affected cases only | 6/8 | Chosen routes matched; no out-of-envelope attempt |

The first run exposed incomplete plans: preserve claim wording/reading order in a
short edit, keep Flute capture-style overrides scoped, finish existing QA/handoff,
and state Remotion API/version/native-still checks. The skill now carries these
handoff requirements and renderer-specific preflight. The final retest made scoped
styles, version pinning and API/browser prerequisites explicit, and the new short-cut
case retained output artifacts and reading-time feasibility.

Two final strict grades remained unsuccessful. One evaluator demanded completed QA
in an intentionally planning-only fixture despite the frozen rule accepting proposed
blocked checks. The other flagged non-explicit product-copy verification and a
conditional native-still check where the request referred to an existing thumbnail.
[Controller review](../benchmarks/router/2026-10-14/controller-review.json) explains
both without rewriting raw grades. Full checklist compliance is not established;
keep manual source-copy/asset/native-still preflight before real production.

## Limits

The envelope itself prohibited external actions and disabled relevant capabilities.
No forbidden attempt was observed, including in the source-injection case, but this
cannot certify behaviour with actual credentials, spending or production privileges.
Read-only planning does not prove a renderer, singing quality, account rights,
media sync or successful file delivery. The eight-case retest is not a full current-
revision suite; do not combine successful answers across revisions into a pass.

All fixture files, including unexpected additions, were rechecked after execution.
Packet hashes, exact case/criterion sets, command completion pairs and aggregate
counts are checked by `scripts/check_router_evaluation.py`. The checker verifies
record integrity, not semantic correctness or shell safety. Model/cost/token and
source details are retained per packet. A model alias is not a permanent model pin.

Next: clarify existing-thumbnail versus native-still requests, make source-copy
checks reliably explicit, and evaluate an independent unseen set with realistic
permission boundaries. Freeze criteria before running; preserve incomplete,
unsuccessful and ambiguous results. Do not start more renderers merely to obtain
a favourable routing score.
