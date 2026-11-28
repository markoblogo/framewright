# Production plan and resource budgets

Owner-selected business function,27November2026. This is the first local slice of Framewright production operations(M4/R09),not a software release,a paid dispatcher or another project database.

[27November agency direction](agency-operating-model.md) extends this foundation toward relationship/commitment records,communication and multi-product work. [Relationship/commitment and correspondence tracking](studio-relationships.md) is now implemented as optional fields in the same pinned input and derived reports. Token-level economics remains a later slice. Owner policy:correspondence control only;the owner composes/sends elsewhere;no sending,deletion or archiving from Framewright.

## One existing checkpoint

Use one ordinary schema-v2 `project.json` as the studio operations checkpoint. Retain a `studio-management` JSON input through `project.py retain`;its revision/hash is checked before reporting or reserving. It contains service terms,distinct credit pools and a small business work list. Each film/game keeps its existing production project;the work row links that checkpoint. Scene tasks,review waits and accepted artifacts remain authoritative there.

`studio.py PROJECT.json` joins the pinned management input with the existing append-only `costs.py` ledger. It reports separate opening observations,confirmed topups,settled costs,pending exposure,forecast remainder,recorded budget remainder and proposed/authorized planning allocations. No currency/credit conversion or cross-service grand total. A forecast is not a fresh provider balance. Unconfirmed renewals are conditions,not funding. One central account ledger prevents independent films from each treating the same account balance as their own;tag every attempt with its work ID/model and record it once. Do not copy an account debit as another charge into each film ledger.

```sh
python3 skills/video-production-router/scripts/studio.py /absolute/studio/project.json
python3 skills/video-production-router/scripts/studio.py /absolute/studio/project.json --html /absolute/studio/review.html
python3 skills/video-production-router/scripts/studio.py /absolute/studio/project.json --check-unit vendor:pool:batch --amount 9 --model 'Model A'
python3 skills/video-production-router/scripts/studio.py /absolute/studio/project.json --reserve /absolute/attempt-reservation.json --model 'Model A'
```

The reserve file is an existing COST-01 reserve event:known decimal amount,distinct operation-attempt,supplier,unit,category,basis,provenance;tag the work/model. Set a cost limit with `costs.py` before reserving. The wrapper checks the pool/model,known funding,expiry and remaining local cap under the existing project lock,then appends the ordinary cost event. Duplicate identical events are no-ops;changed attempts need a new operation. `--at` is for read-only planning,not reservations. Local admission is not permission to buy or submit a provider job and cannot enforce charges made outside this route.

Record usage,ambiguity,settlement/refund and exposure release through existing `costs.py`;never free an ambiguous attempt on a timeout. Keep supplier receipts and successful/failed-job reports as retained inputs/artifacts in the same checkpoint,with explicit outcome tags and publication references. Settlement requires a receipt;usage is not settlement. Reconcile provider balance/receipt before repeating a generation. A failed image can still have a charge;refunds are recorded only when observed.

## Resource record

Each service has a stable ID,name,terms/sources and pools. Each pool has its own ID/unit,opening balance(decimal string or null),observed_at(timezone timestamp),expires_on(date or null),eligible_models(names,`["*"]` for unrestricted or null for unknown),provenance and renewal conditions. Optional confirmed/conditional grants contain amount,observed_at,status;only confirmed nonfuture grants affect a forecast. A topup with different expiry creates a new pool/batch,not a guessed extension of old credits. Preserve past input versions/receipts before replacing the pinned profile. Do not add a fresh provider balance on top of opening funding:reconcile the ledger first.

Unknown balance,eligibility or expiry blocks a new reservation. Explicitly verified nonexpiring pools may use `nonexpiring:true`;absence never means unlimited lifetime. Date-only expiry conservatively stops new reservations at the start of the displayed expiry day;retain exact account text/timezone separately if precision matters. Monthly,daily,purchased,promotional and model-specific credits are distinct where their terms differ. Keep a current quote with exact model,resolution,length,audio,count and observation date;discount quotes are estimates until actual debit is observed. No universal credits-per-video assumption.

## Business priorities

Work categories:client,partner,own_production,editorial,own_research. Client/partner work comes first;within its class use explicit priority1–5,then committed deadline and internal target. Work carries a next step,blockers,status and optional linked production checkpoint/budget. No date is invented when a partner has not committed one. A target is not a deadline. Blocked/paused work remains visible;it is never promoted just because its date passes. At most five business work rows may be active. Queued work is not started automatically.

Planning allocations state `proposed` or `authorized`;they are not provider reservations. Over-allocation is visible. Actual caps/reserves remain separate. An optional idea cannot displace a client promise because its credits expire sooner. Among equally useful tasks,prefer expiring resources;do not spend merely to exhaust them. This first slice does not automatically optimize a schedule,measure labour capacity,pull account balances or enforce partner obligations. Use ordinary explicit edits and retain the new input revision.

## First live use —27November

Private checkpoint: `/Volumes/Work/Work/FramewrightStudio/records/studio-management/project.json`.

- Zopia: general and model-specific pools, displayed expiry and bounded review ceilings were retained privately. Opening funding, proposed allocations and actual use are separate; tentative allocations for other projects are not agreed budgets or reservations. No generation had run at setup.
- PlayMCP: observed balance, play count and time-block earnings are retained in the private resource record. Full production ROI and future rates/eligibility remain unverified. Two walking games and partner learning games are candidates, not automatically started productions.
- Flow: subscription/access owner-reported,tier/balance/next refresh unknown. [Official Google help](https://support.google.com/flow/answer/16526234?hl=en) distinguishes monthly,daily and purchased credits. Do not infer a1000credit tier or calendar-month expiry. No generation or purchase.

Active business work:Zopia review and this function. Zopia is targeted for27November afternoon;Tulvo card-choice game is an optional same-day slot after that review,without a Tulvo obligation. Plaud waits for the device;partner distribution of games is a hypothesis,not guaranteed reach. Radar remains paused through29November;Quixote frozen. No new automation,partner message,release or spending promise.

## Daily/monthly free quotas and today’s options

Optional pool `refresh` records cadence(daily/monthly/weekly/rolling/one_time/unknown),amount(decimal or null),rollover(yes/no/unknown),next_reset_at(timezone timestamp or null) and source basis. The public allowance is never added to the current opening balance automatically. After a known reset boundary the cached balance requires a fresh observation before a new reservation,even if the old pool was nonexpiring. Keep advertised entitlement,observed remainder and uncertain accumulation separate. Paid topups/auto-reload are not enabled.

A service can retain exact current configuration quotes. `today_options` lists local budgeted attempt counts separately per eligible pool,without adding alternative pools together. This is financial fit,not guaranteed model availability,success or permission to generate;time-bound discounts,actual debit pool and provider access still require checks. No count is invented for an unknown quote,balance,expiry or reset.

Initial free quota inventory includes Flow daily and monthly pools and already-used Hugging Face/ZeroGPU GPU-time pool. [Hugging Face docs](https://huggingface.co/docs/hub/spaces-zerogpu) describe daily quota by tier and a24hour reset after first use;GPU seconds and model output seconds are not interchangeable. The26November LongCat success and FastFrames quota rejection remain historical;they do not prove today’s available quota. Specific account balance/reset reads remain outstanding.
