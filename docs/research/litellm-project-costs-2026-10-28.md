# LiteLLM and project-wide cost evidence — 28 October 2026

Status update: the [local COST-01 ledger](../experiments/studio-foundations.md)
is implemented with synthetic controls, exact-decimal events, reservations and
reconciliation. LiteLLM itself remains research-only and untested. No proxy/database,
account/key setup, model call, real spend importer or paid-dispatch enforcement.
The proposal below retains broader future scope; use the linked contract for current
commands and limitations.

## Official findings

[Spend tracking](https://docs.litellm.ai/docs/proxy/cost_tracking) describes calculated
model spend by keys, users and teams and recommends reconciling discrepancies with
provider billing and updating price data. A proxy calculation is not a settled bill.
[Tag budgets](https://docs.litellm.ai/docs/proxy/tag_budgets) describe categories,
maximum USD budget and reset periods, with Postgres as a prerequisite. Check the
selected version/edition for availability; examples in spend-tracking documentation
mark some tag usage as enterprise. Do not promise the entire feature set is free.

The [repository licence](https://github.com/BerriAI/litellm/blob/main/LICENSE)
distinguishes MIT content from separately licensed `enterprise/` content. Model and
provider terms, optional hosted services and infrastructure remain separate. Installing
the client/proxy does not grant account access, credentials or permission to spend.
Calls outside the selected gateway are outside its observed coverage.

## Recommended architecture

Use LiteLLM, if justified, as a source of **model-operation usage/cost evidence**.
The project journal owns the overall budget and records non-model costs as well.
Reuse existing project/task/output identities and the experiment workbench's explicit
amount/currency/unknown conventions. The workbench already records trial costs;
the missing scope is project-wide categories, reservations and reconciliation.

Suggested categories: model inference, image/video/audio generation, cloud compute,
stock/licensed assets, subscriptions, manual purchases, and separately estimated
operator effort. Keep software fee, cash paid, allocated subscription share and labour
estimates distinct. A provider's prepaid credit consumption is a usage unit, not an
automatic USD expense at an invented rate. Free quotas have limits despite no new
payment; local software fees do not include labour/hardware/energy by implication.

### COST-01 — proposed journal contract

[Draft event template](../../examples/costs/cost-event-template.json) is a planning
artifact, not a new accepted project schema or working importer. Records should bind:

- Project, task, output revision, logical operation and actual attempt; provider/model
  or other supplier; category and unique source event/receipt identifiers.
- Approved cap and scope, estimated cost/basis, reserved exposure, observed usage,
  calculated provider charge and reconciled billed amount as separate evidence.
- Amount/unit/currency, price-map revision or quote source, event/observed timestamps,
  applicable period/reset time zone, provenance and completeness state.
- Retries, failures, cache/discount details where known, adjustments/refunds and
  unresolved outcomes. Missing usage/charge remains unknown, never zero.

Use exact decimal money representation and preserve original currency/credit units.
No cross-currency/unit total without an explicit dated conversion/allocation basis.
Separate lifetime project cap from provider rolling/periodic limits. Budget reset
is not authority to increase a project's remaining spend. Subscription allocation
must not also count the entire original purchase as a second project charge.

Multiple tags on the same request are dimensions, not separate charges. Deduplicate
repeated imports/webhooks by source receipt/charge identity. Link the gateway and
provider records for the same operation instead of summing them twice. Corrections
append reconciliation/adjustment events without erasing the original estimate.
Do not log API keys, private prompt bodies or unnecessary billing/customer details.

### Admission and failure handling

Before an authorised costly operation, reserve a conservative known exposure for
the planned attempt, including permitted retries. Unknown maximum exposure requires
a decision, a bounded alternative or a stop; an average cost is not a hard cap.
On completion reconcile the reservation with observed usage/charge. On an ambiguous
timeout retain unresolved exposure until the operation is reconciled; never release
it as zero and blindly resubmit. Apply [STATE-01](langgraph-state-and-approvals-2026-10-28.md)
operation identity/recovery rules and [COMFY-01](comfyui-workflow-executor-2026-10-28.md)
for any non-model generation jobs.

Do not claim absolute overspend prevention from after-the-fact usage logs. Gateway
coverage, in-flight requests, retry policy, price accuracy, database consistency and
other adapters must be tested. Project admission checks supplement provider limits;
an approved budget is still distinct from authority to execute a particular action.
This research does not implement reservations or provide an enforced financial cap.

## First internal trial

1. Map current trial cost records into a proposed project view without mutating
   originals. Use synthetic receipts and already authorised existing evidence only.
2. Exercise one model calculation, one non-model expense, an unknown charge, duplicate
   import, two tags on one request, retry, late settlement and a refund/adjustment.
3. Verify separate authorised/estimated/reserved/observed/reconciled amounts, mixed
   currencies/credits, and unresolved exposure after a simulated crash. Test a budget
   refusal without sending a paid request. Scope the mock result honestly.
4. Only if beneficial, test a pinned LiteLLM adapter with a supported local/mock route
   or saved spend export. Verify exact feature/edition/storage requirements before
   setup; no paid proxy/enterprise plan or provider call is needed for the first trial.

Pass: no unknown-to-zero conversion, duplicate accounting or fabricated bill; source
receipts remain traceable, credits/currencies stay comparable only with evidence, and
simulated ambiguous operations remain unresolved. Synthetic results do not establish
real provider billing/enforcement. Reconcile a real authorised production later.

## Priority and relationship to offers

Prefer a small local cost record first; adding a permanent proxy/Postgres service is
conditional on a real multi-provider need. Intake route comparisons may eventually
show estimated vs observed costs with coverage and uncertainty; their current null
totals remain unchanged. EVAL-01 can test budget reasoning, while the executor/adapters
must enforce actual admission rules independently of model promises.
