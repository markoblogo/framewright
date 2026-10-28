# LangGraph: state, approval and recovery patterns — 28 October 2026

Status: documentation reviewed; orchestration-model reference and optional bounded
comparison candidate. No package installation, graph run, checkpoint migration,
LLM request, external operation or framework dependency added.

The same-day [STATE-01 local implementation](../experiments/studio-foundations.md)
now adds durable executor intent and explicit reconciliation/retry to the existing
project. No LangGraph dependency was needed. This does not close external-provider
recovery, distributed idempotency or the complete pilot/replanning comparison below.

## Official findings

[LangGraph repository](https://github.com/langchain-ai/langgraph) describes a low-level
framework for long-running stateful agents and identifies the core licence as MIT.
Core use is distinct from optional hosted products, model calls and their terms.
[Persistence documentation](https://docs.langchain.com/oss/python/langgraph/persistence)
distinguishes thread checkpoints from cross-thread stores. In-memory checkpoints
do not survive process restart; a recovery test needs actual durable storage.

[Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) pause for
external input and resume against the same thread identity. The interrupted node
restarts from its beginning: code preceding the interrupt runs again. Persisted
graph state therefore does not establish exactly-once external effects, operator
authentication, approval of changed inputs, or authority to spend/publish.

## Adopt the pattern before choosing the framework

Framewright already has pinned materials, task dependencies, effective observations,
explicit waits and a sequential allowlisted executor. Extend
[these existing mechanisms](../../skills/video-production-router/references/projects.md)
rather than moving their authority to a second graph database. An optional graph
checkpoint should reference project/task/revision identities and an event cursor;
the project journal remains authoritative for decisions and output acceptance.

Keep deterministic actions separate from model proposals. Save a model's proposed
route/settings as a versioned artifact; replay must not silently ask for a new answer
and treat it as the already reviewed decision. No LLM is needed for the first test.

## STATE-01 — one pilot/review/revision loop

Proposed state transition contract, not an implemented graph:

| Current state | Event and evidence | Next state / allowed action |
| --- | --- | --- |
| Pilot planned | Task ready, exact inputs/settings and execution scope authorised | Run one admitted local action |
| Pilot produced | Expected output retained and technical checks recorded | Await human review; produced is not accepted |
| Review pending | Human accepts that output revision | Eligible for the agreed production scope; further execution still uses normal authorisation checks |
| Review pending | Human requests a bounded change | Create revision task; rerun affected work only |
| Review pending | Human rejects the route | Revisit staging/route proposal; no silent provider substitution |
| Any reviewed state | A relevant input/output revision changes | Prior dependent approval becomes stale; reassess required checks |
| External action unresolved | Timeout, crash or missing acknowledgement | Needs reconciliation; no blind resubmission |

Represent who must decide, what artifact/version they review and the permissible
decision values explicitly. Unknown owner remains unknown. Preserve waiting party,
deferred decisions, task history and rejected versions. Resuming a program does not
clear a wait. Old graph checkpoints must not resurrect stale approvals, repeat
publication or undo later journal events. Re-read current pins and decisions before
performing an action. Pilot acceptance alone is not a general purchase/upload grant.

## External-operation boundary

Plan these safeguards in each relevant adapter; a graph checkpointer is not enough:

1. Persist an operation identity, project/task/revision, request digest, intended
   limits and authorised action before sending. A changed request needs a new
   identity and possibly a new decision. Retain attempts as well as logical actions.
2. If the provider supports an idempotency key, reuse the same key for the same
   logical operation and verify its documented lifetime/scope. A local key alone
   does not make a provider idempotent.
3. Record returned job/receipt IDs and terminal results. For an ambiguous send,
   query the provider by its supported identifiers where possible. Without evidence
   of whether the operation happened, stop for reconciliation/human decision.
4. Separate job submission, monitoring, output retention and technical/human review.
   An existing provider job must be resumed/inspected, not automatically recreated.
5. Use host/project locking and durable operation ownership to prevent concurrent
   duplicate submission. Handle orphaned locks/attempts explicitly after crashes;
   do not claim distributed exactly-once behaviour from a local lock or checkpoint.

Keep credentials and sensitive responses outside public records. Error types should
distinguish not submitted, provider rejected, known running, known failed, known
completed and unknown outcome. No automatic paid retry or publication on resume.
This complements [COMFY-01](comfyui-workflow-executor-2026-10-28.md), whose per-prompt
reconciliation and isolated cancellation requirements remain unchanged.

## Bounded comparison and adoption decision

First express the loop in the existing journal/executor using original local
fixtures and a fake external operation ledger. Test acceptance, revision, route
rejection, deferred review, source replacement, repeated resume, concurrent attempt,
and process restart before/after a fake provider accepts a submission. Inject the
unknown-outcome case; assert that no automatic second send or approval occurs.

Only if useful, compare the same fixtures with a minimal LangGraph implementation,
pinned version and local durable checkpointer in an isolated environment. No hosted
LangSmith, paid model, cloud account or production data is required. Do not introduce
parallel heavy jobs. A RAM-only demonstration cannot pass restart recovery.

Retain state/event traces, fake-operation counts, recovery behaviour, changed-input
handling, dependencies, resource footprint and operator effort. Prefer LangGraph
only if it improves the tested pause/recovery/branching behaviour enough to justify
added complexity without duplicating journal authority. Keeping the existing
executor after a successful comparison is a valid result. No migration is presumed.

## Relationship to queued work

PROD-01 exposes current blockers; STATE-01 specifies the permitted transitions and
recovery boundaries. SOURCE-01/PREVIS-01 provide source/staging decisions; COMFY-01
may later execute an admitted generative task. OTIO-01 remains the independent
concrete-cut handoff. This research does not reorder owner-authorised production.
