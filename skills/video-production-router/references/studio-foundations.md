# Resources, costs, recovery and decision assertions

Optional extensions of the existing project/checkpoint. No second production database,
provider proxy, actor/grader model, automatic installation, paid call or publication.
[Internal trial and limits](../../../docs/experiments/studio-foundations.md).

## RESOURCE-01: observe, do not infer fit

`environment.py MANIFEST.json --observe-resources` adds a dated host observation:
total/available RAM, swap when available and free space on the explicitly selected
manifest volume. Existing total-RAM requirements keep their original meaning.

`executor.py PROJECT.json ... --execute --observe-resources` attaches a bounded
sampler to that executor's inspection/review-clip worker. Optional `psutil` must
already be installed in the chosen Python environment; absence is reported and
never triggers installation. Revision-comparison sampling is deliberately unsupported.
Only the owned process and its children are requested; no unrelated command lines,
environment, open files or network connections are read. A denied child tree falls
back to root-only coverage and records the gap. Observations are saved in the
existing execution history and returned JSON, including failed-worker evidence.

Default interval0.25s, at most720 samples; shorter workers may have no sample.
PID plus creation time binds the root. First CPU readings are discarded. RSS is a
sampled sum which can double-count shared memory; CPU100% means one core. No
hard memory limit, automatic kill policy, GPU/model/codec/storage-speed qualification
or network-speed measurement follows. Paths/PIDs in local observations stay private.

## COST-01: separate limits, estimates, exposure and bills

Create an ordinary local synthetic project, then import one explicit event at a time:

```sh
python3 skills/video-production-router/scripts/project.py create /tmp/fw-cost-demo.json --goal 'Synthetic costs' --note 'No provider calls'
python3 skills/video-production-router/scripts/costs.py /tmp/fw-cost-demo.json --event examples/costs/controls/limit.json
python3 skills/video-production-router/scripts/costs.py /tmp/fw-cost-demo.json --event examples/costs/controls/reserve.json
python3 skills/video-production-router/scripts/costs.py /tmp/fw-cost-demo.json --event examples/costs/controls/unknown.json
python3 skills/video-production-router/scripts/costs.py /tmp/fw-cost-demo.json --event examples/costs/controls/settle.json
python3 skills/video-production-router/scripts/costs.py /tmp/fw-cost-demo.json
```

Events live in the same schema-v2 project, with integrity hash and history entries.
A supplied cap is a recorded declaration, not spend authority. Exact decimal strings,
explicit currency/credit unit, supplier/category, distinct operation-attempt ID,
nonempty basis and provenance are required. Optional `task` and `subject` bind an
existing task and exact retained revision; later binding changes need a new attempt.
Do not store credentials, prompts or customer/billing details in event text.

Kinds: `limit`, `estimate`, `reserve`, `usage`, `unknown`, `settle`, `adjust`, `release`.
Unknown amounts remain null. Reservation requires a known remaining recorded cap;
a repeated reservation needs a new attempt. Ambiguous outcomes retain exposure;
unknown exposure without a bounded reservation makes remaining budget unknown.
Releasing exposure requires an explicit evidence-based event; never infer it from
a timeout. A later charge reopens exposure. Real bills exceeding a cap are recorded
truthfully and flagged; recording an overspend is not permission for another one.

Settlement requires a supplier receipt. Reimport of the identical supplier/receipt
is a no-op; conflicting duplicate is rejected. Gateway usage and settlement for one
mapped operation are separate columns, not two charges. Tags are dimensions.
A corrected settlement is the latest bill amount for that operation; refunds and
other distinct adjustments append signed events with their own receipt identity.
An adjustment cannot refund more than the recorded charge. Map gateway/provider
identities explicitly before import; no automatic billing importer exists.

Reports group by unit. No FX/credit conversion, subscription allocation, rolling-quota
scheduler or grand total is invented. Estimate, reserve, usage and settlement columns
must not be added together. `project.py status --json` also includes the cost view.
This first slice refuses ledger reservations, but is **not wired to a paid dispatcher**
and does not enforce a provider's charges or stop calls made elsewhere. LiteLLM is
still an optional research candidate, not a dependency or tested integration.

## STATE-01: recover before repeating

The existing executor persists an intent before any admitted local worker or comparison
starts: task, request/settings digest and exact input pins. On success it records
produced output and its pin; on a known local failure it records failure. A process
interruption before durable completion leaves outcome unresolved. `status`, `brief`
and completion diagnosis surface it; that task is not ready for automatic execution.

```sh
python3 skills/video-production-router/scripts/executor_state.py PROJECT.json
python3 skills/video-production-router/scripts/executor_state.py PROJECT.json --reconcile ATTEMPT_ID --outcome not-submitted --evidence output:RECOVERY_REPORT
```

Reconciliation requires a separately retained current report and an explicit operator
statement (`failed`, `not-submitted`, `produced`). It is not independent verification
of an external effect. For produced output, retain the found file separately first.
Known failed/not-submitted work is not silently repeated: invoke the same executor
request with `--retry-of ATTEMPT_ID --execute`. Changed settings/pins require a newly
reviewed task, not reuse of the old retry identity. Normal project and host locks,
waits and required-output checks still apply. Preserve leftover files for inspection.

Produced is not accepted. The existing revision-bound technical/listening/creative
journal remains authoritative; input/output drift is visible. No review is cleared by
restart/reconciliation. This is local crash recovery, not distributed exactly-once,
provider idempotency, external-job reconciliation or automatic review/replanning.
LangGraph is not installed or adopted; external adapters need their own future trials.

## EVAL-01: assertions, not an agent score

```sh
python3 skills/video-production-router/scripts/decision_checks.py examples/evaluation/production-decision-cases.json examples/evaluation/controls/weak-host.json
```

The six existing contracts cover weak host/zero budget, forbidden installs, no egress,
uncertain prices/retries, uncleared music and a protected voice. Structured events
have explicit action/status; rejected/not-submitted actions are distinct from executed
or ambiguous ones. Retained answer hashes and complete mapped events are required.
Agent records additionally need a matching hashed raw JSON action capture. The helper
reports mechanical pass/fail/insufficient_data. Observed violations remain failures
when other evidence is missing; missing/incomplete traces never become success.

These checks read supplied records, not the real tool transport. An agent or fabricated
capture is not independently verified by a self-declared complete flag. Independent
capture provenance, proposal usefulness, rights reasoning, staging quality and language
need human/rubric review. Semantic status always stays pending and model qualification
false. Synthetic compliant/violating controls validate plumbing only; historical router
qualification and the six `not_run` actor contracts remain unchanged. Promptfoo is
still optional and untested; no model request or evaluation runs in ordinary CI.

The cooperating local POSIX executors share one per-user lock under `/tmp`,
independent of TMPDIR. Moving scratch files to another volume does not permit
a concurrent executor. This remains an advisory lock for these local commands,
not coordination with unrelated tools or remote machines.
