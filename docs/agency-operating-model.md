# Framewright — creative agency operating direction

Owner direction, 27 November 2026. Extends the [existing studio vision](vision.md), [internal product scope](internal-studio-scope.md) and [production operations](studio-production-management.md). This is the selected development direction and a staged plan, not a claim that a complete agency system is implemented. The public site/README, active productions and account permissions are unchanged.

## Purpose and audience

Develop Framewright into a creative agency with agent-assisted operations: create audiovisual and interactive work, research production tools, manage resources and commitments, support its own media, and carry client/partner work from request through delivery and follow-up.

Keep the owner-led creative studio as the execution core. Agency scope adds accountable business operations around that core. It does not require a large staff, a general-purpose NLE, a new CRM service or an autonomous publisher.

Primary relationships:
- clients commissioning a defined creative result;
- platform/tool partners supporting production access or requesting demonstrations;
- audiences using Framewright's own films, games and worlds;
- creators/teams adapting its open methods.

A commissioned project, an editorial review and an internal experiment have different objectives and obligations even when they reuse the same material. Partner access is neither cash revenue nor a promise of favourable coverage. Own media can support discovery,portfolio and incoming requests as well as editorial learning;record actual enquiries separately from views or assumed leads.

## Five connected functions

| Function | Work included | Existing foundation | Remaining scope |
|---|---|---|---|
| **Creative production** | Films, shorts, images, sound, playable games, exploratory worlds and interactive demonstrations; coordinated packages where useful | Existing production checkpoints, review/correction/delivery and PlayMCP/world cases | Product-specific acceptance and maintenance; no universal game/world builder or engine independence demonstrated |
| **Research and tool selection** | Watch relevant products, assess stack/access/rights, compare a bounded approach, retain actual outcomes and apply useful results | Tool research, experiment queue, scoped arsenal and owner corrections | Link each new trial to an actual production risk or reusable gap; measure practical benefit rather than accumulate tools |
| **Resources and economics** | Provider terms, token/credit quotas, expiry, quotes, reservations, actual usage, refunds, planned work and operating effort | studio.py plus existing project/cost ledger, separate pools and priority work list | Token/cache metering, provider reconciliation and labour/project economics where observable; no automatic account pulls or complete margin reporting currently |
| **Clients, partners and communication** | Contacts, requests, scope, deliverables, deadlines, approvals, changes, correspondence, handover and follow-up | Pinned relationship/commitment records, correspondence history and due flags in the existing studio report and project brief | Repeated live reconciliation and one complete agency-project follow-up; no autonomous mail, contract enforcement or full CRM |
| **Own media and learning** | Channel plans, film/game release links, covers/copy/disclosures, distribution, dated analytics, useful reuse and observed outcomes | Existing social/publication packages, editorial cases and owner-reported links | Regular comparable follow-up and cross-project learning; no general automated publishing, revenue attribution or growth prediction |

Quality, recovery, source/rights evidence and owner acceptance run through all five functions. They are not a separate approval department or a substitute for creative judgement.

## One operational chain

Request/idea → relationship and objective → scoped brief and deliverables → feasible route and resource plan → production with useful bounded tests → review/correction → authorised delivery/publication → outcomes and follow-up.

Use existing work/project statuses; the chain above describes responsibilities, not a new parallel state machine. A relationship may have several projects; a project may have several products, experiments and publications. Link those records by stable IDs rather than copying their status or budget into several lists.

Every active item must answer:
1. Who needs the result, and what was actually promised?
2. What is the next action, its responsible person and any waiting dependency?
3. Which deadline is committed, and which date is only an internal target?
4. Which resources are available/authorised, and what is the actual or unknown cost?
5. Where is the current accepted work, delivery evidence and next follow-up?

Keep at most five active studio work items. Client/partner obligations retain first priority; queued work, expiring free credits and interesting tools do not silently displace a commitment.

## Extend current records, not parallel infrastructure

Keep production truth in each ordinary project checkpoint; shared resource truth remains in the studio management checkpoint and append-only cost journal. Extend the existing pinned management profile and project references for relationship/commitment views when that implementation slice is selected. Retain private contacts, terms, correspondence and analytics externally under the canonical studio; public method examples use fictional data.

Proposed additions below are **record requirements, not implemented schema fields**:

| Record | Minimum useful information |
|---|---|
| Relationship | Stable identity, client/partner role, owner/responsible person, contact/source references, terms and linked projects; private details remain private |
| Commitment | Who requested what, source/date, proposal/accepted scope,deliverables,committed deadline or unknown,internal target,dependencies,next action and required decision;agreed fee/resource exchange and payment conditions where applicable |
| Communication | Inbound/source or outbound draft, counterpart/channel, linked project/commitment, draft/approved/sent/replied evidence, sent time/receipt when observed and follow-up condition |
| Change | Requested change, origin, effect on time/resources/deliverables, accepted or pending scope and affected revision; do not silently expand the order |
| Outcome | Accepted delivery and links, actual cost/effort where measured, feedback, unresolved support and dated distribution/analytics observations |

For paid work,link the agreed quotation and any invoice/payment evidence without building a second accounting system. A proposal is not an order,an issued invoice is not a received payment,and a gifted credit pool is not a cash fee. Commercial documents and contractual acceptance require their applicable owner authority.

Owner clarification27November2026:Framewright controls correspondence and its implications for status,dates,priorities,budgets and follow-up. The owner composes and sends in another thread. Framewright does not compose/send replies,delete messages or archive threads. It can track drafts prepared elsewhere and surface due reminders;no scheduler is created. The initial Gmail Framewrite labels were explicitly authorised as organisation only. [Implemented first slice](studio-relationships.md).

## Resource accounting across providers

Track cash, input/output/cached tokens, generation credits, compute/GPU time and recurring allowances in their actual units. Token categories and whether cached usage is discounted depend on the provider's dated terms. Keep observed counters, estimates and unknowns separate. Never infer exact token usage or a cash debit from a model's reply or a character count.

Keep one attempt/operation ID from estimate/reservation to actual usage and settlement. Existing pools handle validity/renewal/eligibility; extend them rather than introduce another budget database. Record the project and purpose of an attempt, including paid failures, refunds and reuse. One asset reused in several products incurs its original charge once; allocation is analysis, not another provider debit.

Only compute a monetary estimate using an applicable known price/configuration/date. Do not sum unrelated credit units. Subscriptions, internal operator effort and project quotes need separate treatment; any allocation method must be stated. Actual business margin requires known revenue and relevant costs. Provider gifts, provisional replenishment, views and play time are not verified cash revenue. Games may earn observed production credits; record those as resource replenishment, not automatic profit.

Planning should show useful options within confirmed resources, not demand that expiring credits be spent. New purchases and paid jobs retain their existing authorisation rules.

## Games and worlds are first-class products

A game/world can be a deliverable, an editorial subject or a virtual set for a film. Declare which role applies. A package may pair a playable partner demo with a video explanation, but the game and video have separate acceptance and publication evidence.

For a playable product retain the selected build/URL, mechanics/capabilities, save/reset or persistence behaviour, source/asset rights, supported environment, known defects and handover/maintenance scope. For a world also identify capture/camera/export constraints and whether it is owned, remixed or only referenced. A saved room or working public link does not by itself establish a portable project or commercial reuse right.

Use the product-appropriate pilot: a short playable loop for a game, a navigable/captureable scene for a world, a landscape excerpt for a selected video. Do not force the video-first pilot rule onto a non-video product. Existing PlayMCP/Rooms/virtual-set evidence remains scoped to its tested route.

## Delivery plan and acceptance gates

These are ordered implementation slices under M1/M2/M3/M4 and R05/R09/SOCIAL-01; external handoff later uses M6/REL-D. No new experiment family, release deadline or active job is created by listing them.

| Order | Small implementation slice | Demonstration of completion |
|---|---|---|
| **1. Relationships and commitments** | Extend the existing studio checkpoint with a small linked view for two or three existing relationships: current ask, agreed deliverables, dates/waits, correspondence references and next action. Reconcile from retained sources; unknowns remain unknown. | A fresh session can recover who is owed what and the next permitted action without an owner recap. Drafts cannot become sent messages or promises merely by changing a view. Tests use fictional records. |
| **2. Per-project resource reconciliation** | Extend the current ledger/report only for resource types actually used. Connect estimates/reserves/actual usage and observed replenishments; include operator time if recorded. | On one real project, explain what was spent, what remains, which numbers are estimates and which resource pools can fund the next authorised step, without double-counting. Missing external meters are an explicit limit, not a blocker to local records. |
| **3. One agency workflow and follow-up** | Use an owner-selected existing partner/own project to join brief, production, useful test, communications, delivery/publication and one dated follow-up. Pair video and interactive output only where selected. | Recover the full chain, accepted result, actual commitments and resource observations. Observe a useful repeat/correction and actual outcomes; record missing analytics. Do not manufacture a new partner obligation to demonstrate the system. |

Current paid/generative production, partner waits and Radar/Quixote pauses remain as recorded in [current work](next-cycle.md). Slice1 is now [implemented in the existing checkpoint/report](studio-relationships.md),with a bounded live reconciliation of the selected correspondence. Other agency functions remain staged targets;this does not claim the complete agency system is implemented.

## Success and boundaries

Near-term evidence is practical: fewer lost obligations, recoverable projects, accurate resource exposure, clearer next actions, accepted outputs and useful repeated methods. Record active work/waiting time, substantial correction rounds, recurring defects, resource observations and dated audience/partner feedback where available. There is no measured general efficiency or profitability claim yet.

The public proposition can later present Framewright as an agency/studio when the offered service and evidence are concrete. This direction does not immediately rewrite the landing page, expand claims, change accounts, hire staff or authorise client communication. Nor does it promise every creative format, automated business management or fully autonomous operation.

Develop business capability alongside real production. Release scope should reflect a demonstrated small working function, not completion of this entire agency ambition.
