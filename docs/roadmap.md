# Framewright roadmap

Updated5November2026; source version0.8.0 / REL-C published per retained
[release audit](release-audit-0.8.0.md). The Radar → Radar → French book cycle is
complete in its stated scope. Owner authorised dependency-aware closeout and a
documentation PR; no release, merge or new production. See the
[current slice](next-cycle.md) and [5November closeout](#5-november--post-rel-c-cycle-completed-documentation-closeout).
Earlier dated entries below are history; they do not restart completed work.
This is the primary **priority and milestone map**. It connects product work,
production and experiments; it does not start them or authorize spending/publication.
The owner requested a stable roadmap that absorbs new ideas without replacing the
direction each time. The ordering below is the proposed working sequence, adjustable
by an explicit owner decision. No new film is selected by this document.

## Direction and strategic outcomes

**A personal video-production studio led by an agent:** understand the intended
result, propose feasible ways to make it, carry the chosen project through production,
review and delivery, and reuse what was learned. Framewright remains one implementation
of portable production methods, not a requirement for applying them.

| Outcome | What should change for the user | Evidence of progress |
| --- | --- | --- |
| A useful production proposal | Choose a creative approach suited to the idea, sources, machine, time and budget | A person can choose without editing JSON or knowing tool names; assumptions and gaps remain visible |
| A recoverable production | Continue after a pause; correct a scene without losing accepted work | Exact-version inputs, outputs and decisions; successful interruption/recovery and bounded correction |
| Better repeat production | Reuse design, sources, voices, characters and decisions for a new episode | Comparable second production, measured operator effort and documented reuse; no assumed savings |
| An arsenal that solves problems | New tools improve a specific weak point | Bounded comparison against the existing method, feature/version/host scope and retained failures |
| Transferable knowledge | Another operator can use the methods and contribute experience | Reproduction, external handoff, worked cases with and without Framewright; book-readiness evidence |

## Foundation and dated release evidence

The [27–28 October capability review](product-progress-2026-10-27-28.md) and
[PR corrections](experiments/pr46-review.md) establish a bounded foundation:
profile-aware route proposals, local inspection/proxy admission, durable execution
intents, source-first editing, a real OTIO/Kdenlive return with owner acceptance,
cost evidence and offline decision assertions. These are **implemented or tested
within their stated scope**, not a fully autonomous studio.

Still unproven: a whole admitted production route, reliable time/cost forecasting,
paid-provider enforcement/reconciliation, general semantic video assessment,
independent-user success, measured labour savings and recurring character continuity.
R01 now connects the saved Blender shot to admission and sequential execution,
with an original local fixture and failure controls; see [evidence](experiments/r01-saved-shot-executor.md).
Published films demonstrate concrete work, not those broader claims.

**Current REL-B assessment, 1 November:** bounded repeat/reuse and scoped R05
comparison evidence complete; [release preparation is recommended](rel-b-readiness-2026-11-01.md).
DOC-ENTRY-01, final local checks and independent review now pass; see
[local review](rel-b-local-review-2026-11-01.md). PR50/merged-main CI pass; owner has now authorised0.7.0 release preparation and
publication. [Frozen publication audit](release-audit-0.7.0.md) separates candidate
checks from actual canonical tag/asset verification. This does not establish labour savings or whole-route automation.

## Milestones and exit evidence

Milestones are outcomes, not release dates. A release is a separate owner decision.
Status is evidence-based: planned → active → partial/blocked → verified in stated
scope. A blocked experiment does not block unrelated approved production.

| Milestone | Current state | Exit evidence and dependencies |
| --- | --- | --- |
| **M1 — One understandable entrance** | Partial beyond the bounded case: R02 proposal retained for owner-selected Last Seed; forecasts/independent-client use unproven | A real brief becomes a short approved concept, source/gap list and 1–3 genuinely feasible offers. Each explains creative result, prerequisites, human effort, cost/time basis, uncertainty, fallback and cheapest useful pilot. Persist free-only choice; distinguish declared access from checked access. Exercise RV02 and the existing decision contracts. |
| **M2 — One complete recoverable route** | Bounded operator-led loop evidenced in REL-A; full automation unproven | On one selected route, pilot → review → production → technical/listening/creative checks → targeted correction → accepted local delivery. Resume in a new session without re-explaining retained decisions. Manual steps are explicit. Bind a saved-shot renderer first; record failure/recovery and preservation checks. Depends on a usable M1 offer, not a new UI application. |
| **M3 — A repeatable second production** | Bounded REL-B repeat/alternate-format evidence complete; general savings unproven | A comparable second episode and one alternate format reuse accepted design/materials with their own reviews. Exercise short/long/missing-optional template controls. Measure active work, setup, render/wait, context recovery and avoidable rework separately under RV01. Depends on an accepted baseline from M2 or a suitable existing film. |
| **M4 — Controlled expansion that improves a route** | Partial: catalogue/workbench and many scoped trials exist | One observed production weakness → bounded candidate comparison → exact feature qualification or rejection → repeat on another suitable production. Preserve a proven fallback. Extend cost/resource/platform coverage in small sourced batches. Can accompany M1–M3; does not require testing the whole queue. |
| **M5 — A coherent short fiction** | Verified bounded internal scope; release publication checked separately | No Further Claims: accepted linked chase, completed131.25s fiction, local corrections, sound and two aspects. [REL-C matrix](rel-c-readiness-2026-11-04.md) separates manual/owner review from independent recovery. No rig, general contact, automated whole-route or audience claim. |
| **M6 — Transfer and independent use** | Partial: SSI reports approved private delivery; unattended cycle unproven; book base drafted | Another operator completes or resumes a bounded route from the handoff; record setup/support needs and unknowns. SSI reports three owner-approved videos delivered privately on1November; independent full listening and unattended future generation still need their own evidence. BOOK-01 remains its existing separate gate: cleared, reproducible cases and a useful sample chapter with/without Framewright. Optional community packets follow explicit opt-in and review; no telemetry or mandatory sharing. |

M1 and M2 are the immediate product focus; M3 demonstrates the practical benefit.
M4 supports those milestones continuously but with bounded trials. M5 is the creative
destination, not a reason to rush character tooling. M6 draws on completed work.

## Release checkpoints

Releases follow capability milestones, not a weekly schedule, tool count or each
merged PR. These are **readiness gates**, not instructions to publish. On reaching
one, report the evidence and outstanding limitations to the owner and propose a
release; wait for the owner's release decision. Do not automatically tag, upload
packages or create a GitHub release. No version number/date is assigned in advance.

| Gate | Earliest meaningful release scope | Required evidence |
| --- | --- | --- |
| **REL-A — A usable production loop** | M1 + M2, primarily R01–R03 | Readable selected offer, bounded execution, real pilot/film, one targeted correction, fresh-session recovery and accepted local delivery. Updated examples/docs, green relevant checks and resolved review findings. R01 or R02 alone does not reach this gate. |
| **REL-B — Repeat production and reuse** | M3 + a relevant M4 repeat, primarily R04–R05 | Second comparable production and alternate format, tested template boundaries, observed reuse/effort and a scoped candidate confirmed on another suitable case. Bundle related improvements rather than releasing after each tool test. |
| **REL-C — Coherent character production** | M5, primarily R07 plus needed R06 adapters | Accepted interaction/continuity pilot and completed coherent fiction; versioned hero/set, readable contact/action, correction/recovery and documented limits. A successful rig or single render is insufficient. |
| **REL-D — Transferable operation** | M6 when there is a distinct usable product increment | Another operator's reproducible route/handoff, support/setup evidence and portable instructions. May join REL-B/C if achieved together; book-readiness alone is not a software release. |

At each gate check the actual diff since the latest release, compatibility/migration
notes, evidence links, README, package validation and review. Merge/push and a release
remain distinct actions. A serious regression may justify a separate patch release,
but still requires an explicit owner decision. Research-only additions and internal
probes normally accumulate between gates. The owner authorized the 30October experimental consolidation release. That
[historical audit](release-audit-2026-10-30.md) kept recovery/Eevee evidence partial.
The [1November REL-A assessment](release-readiness-2026-11-01.md) now finds the
bounded operator-led production evidence assembled. [Final local checks/review](final-local-review-2026-11-01.md) now pass; remote CI and an owner release decision remain separate. Manual stages are explicit and allowed;
whole-film automation is not an additional release requirement.

**1November recovery update:** [new-agent Good Dog recovery](experiments/session-recovery-2026-11-01.md) verified selected-file/review/constraint restoration without chat history. This closes the bounded recovery block on that case. A subsequent bounded Eevee production-scene/admission test now passes (see block2 below); whole-film/final-quality and remaining REL-A evidence still need assessment. No release triggered.

## Tactical work: now, next, later

IDs below are roadmap slices; existing SOURCE/ROUTE/RV/BOOK identifiers retain their
original meaning. One substantive implementation or production task is active at a
time on this Mac; related documentation can be updated during waits.

| Horizon / ID | Concrete task | Completion check | Maps to |
| --- | --- | --- | --- |
| **Verified internal scope · R01** | Bind the existing saved-shot Blender adapter to selected-route admission and sequential execution; reuse scene pins, controls and review helpers | Passed original Blender fixture: repeated render, exact subrange and light-only change; automated drift, timeout/interruption and output-contract controls. [Results](experiments/r01-saved-shot-executor.md). Full production route and creative acceptance remain R03. | M2, ROUTE-01 |
| **Verified internal scope · R02** | Join existing intake/profile/source-gap/proposal outputs into one readable producer brief, including why a scene exists | Passed retained free-only/broader brief replay, source-index evidence/gaps, project waits/drift and preference/constraint checks. [Results](experiments/r02-producer-brief.md). Owner-selected Last Seed retains the R02 proposal; no invented costs or forced three-option count. | M1, RV02 |
| **Film accepted; bounded follow-ups verified · R03; final release review pending** | The Last Seed: owner accepted48.5s v4 picture and sound | [Recovery record](experiments/last-seed-recovery.md): local final copy matches accepted v4; title/description/tags/cover prepared. Native mixed-quality limits retained. Fresh-process recovery checked file pins and selected final bytes; stale historical waits remain visible. Independent-session recovery is now evidenced separately on Good Dog; a short Last Seed Eevee executor trial now passes; historical full-film rendering remains manual. Publication owner-reported; see the1November REL-A assessment. | M1–M2, RV01, RV03 |
| **Bounded evidence complete · R04 / REL-B** | Comparable repeat film and alternate format on the accepted One Artist, Two Cities base | [REL-B protocol](experiments/rel-b-repeat-protocol.md): both aspects owner-accepted; bounded caption controls and explicit long-copy timing follow-up pass, independent read-only continuation and result review retained. Private design remains proposed, baseline labour unknown. [Release-preparation assessment](rel-b-readiness-2026-11-01.md). | M3, RV01 |
| **Bounded repeat complete · R05** | Test one missing capability exposed by R03/R04 | Existing-method baseline, one candidate, same inputs and explicit accept/reject criterion; record negative results and whether a second production confirms them. | M4 |
| **Verified internal scope · DOC-ENTRY-01** | Simplify documentation entry points after the REL-B result | Three paths and compact current summary implemented; history archived with rebased links. Independent internal cold-reader walkthrough and link checks passed; [evidence](rel-b-local-review-2026-11-01.md). No external-user success claimed. | M6, RV02 |
| **Later · R06** | Broaden admission to another needed local adapter or one pinned ComfyUI workflow | Concrete scene need, available host/model/rights, failure path and retained output. Do not bulk-install nodes or rewrite orchestration. | M2/M4, COMFY-01 |
| **Production case closed · R07** | Good Dog v8 accepted and owner-reported published; [closeout and follow-ups](experiments/good-dog-closeout.md) | Retained133s film, corrections and limits; next-film two-shot continuity/voice tests remain open. No general rig/identity, rights or M5 completion inferred. | M5, GD-NEXT-01/02, PREVIS-01 |
| **First film accepted/published; later repeat · AZUR-GUIDE-01** | [Develop the guide-film style through varied guides](experiments/azur-guide-first-film.md) | First film owner-reported on YouTube; guide embed owner-reported complete. Next guide after several other productions: approve donor media before assembly, then pilot and dual-format review. Universal template not yet qualified. | M3/M6, R04, R09 |
| **Later staged handoff · AZUR-AUTO-01** | Transfer a proven guide/event template to AzurMenton for source-triggered production and distribution | [Staged plan](experiments/azur-guide-first-film.md#future-automation--staged-owner-direction): first qualify style/tools and formats; later receiving-project generation, YouTube upload/embed and dedicated Instagram/TikTok publishing with per-platform verification and duplicate protection. No current account creation or publishing task. | M3/M6 |
| **First TikTok publication owner-reported · TIKTOK-01 / SOCIAL-01** | [Social-media packaging and author/animation channel](social-media/README.md) | No Further Claims [TikTok](https://vt.tiktok.com/ZSpN7wfkP/) supplied4November; separate cover upload worked per owner. Region/monetisation are not launch blockers per owner. Next: measured learning; assess TikTok suitability at every new YouTube brief and adapt selected films natively. No reach/revenue claim or automatic publication. Instagram remains later discussion. | M4/M5/M6, R07/R09 |
| **Production closed · LIT-FILM-01; later · LIT-FILM-02–04** | No Further Claims Chapter1 incident,131.25s,16:9 and9:16 | [Method and limits](methods/coherent-manga-production.md); [REL-C assessment](rel-c-readiness-2026-11-04.md). Earlier No Giant Eagle deferred; other books remain [later](book-adaptation-slate.md). Same-case cold resume passed; owner authorised REL-C release, then plan discussion. | M5/R07/R09 |
| **Later · R08** | Add provider/quota execution only when a selected production needs it | Current terms/account evidence, retry reserve, per-operation authority, ambiguous-charge recovery and no duplicate submission; local cost ledger alone is insufficient. | M2/M4, COST-01/STATE-01 |
| **Ongoing closeout · R09** | Convert useful outcomes into reusable methods, case studies, post material and book coverage | Update exact evidence, existing queue/registry, chapter gap and next action. Retain with/without Framewright instructions; do not claim reader reproduction before it happens. | M6, BOOK-01 |

R01 and R02 are complete within their internal test scopes. R03 now has an
owner-accepted48.5s Last Seed film and reported publication; full-route execution remains unproven. Independent new-agent recovery is now evidenced on Good Dog. The roadmap
itself grants no execution authority. Owner-requested films may supply R03/R04 evidence
when they fit; otherwise use a separately selected original story designed for the
needed tests. Do not make filler films merely to close tasks.

### Existing tests to draw on, not a second queue

| Existing work | Where it fits next | Unclosed question |
| --- | --- | --- |
| [Source/ASR retrieval](experiments/source-asr-mn7r.md) and [multi-source editing](experiments/source-multicut-mn7r.md) | R02/R03, source-rich review or promo | Does retrieval find the needed moments despite recognition errors, and does it reduce manual preparation? |
| [PREVIS-01](research/storyboarder-previsualization-2026-10-28.md) and [saved shots/passports](../skills/video-production-router/references/shots-and-passports.md) | R01/R03/R07, original story | Does cheap staging reveal continuity/action defects before final rendering, and does a changed shot preserve the approved hero/set? |
| [DJV review](experiments/djv-review.md) and [media assessment trials](experiments/gemini-media-review.md) | R03/R04, actual final-master comparison | Can observations be tied reliably to exact frames/versions? Human viewing/listening remains necessary; automated perception is not established. |
| [Last Delivery](experiments/last-delivery.md) and [Tripo research](research/tripo-rigging-animation.md) | R05/R07, only for a concrete character weakness | Ground contact, prop interaction, expression and scene continuity; a paid-access blocker stays blocked under current free-only testing policy. |
| [Template/brand methods](../skills/video-production-router/references/templates.md), SSI handoff and RV01–RV03 | R03/R04/R09 | Can a new episode, correction and fresh session preserve design and reduce avoidable work, with independently reviewed output? |

[RECON-01 real-space reconstruction](research/reality-capture-2026-10-28.md) is a
new M4/R05 candidate capability with potential M5/R07 reuse: capture a location,
retain a scene and revise its camera move. Access/export/compute gates remain open;
no candidate displaces R01/R02 or becomes a tested route from this research.

At equal urgency, prefer resolving an active delivery blocker, then a reusable
capability gap, then stronger evidence for an existing method. Novelty alone has no
priority. Scope a test only when its expected learning justifies setup, resource and
review cost; otherwise keep the candidate in reserve.

## Intake rule for every new idea, tool or production order

1. **Classify and link.** Record the need and map it to an M milestone and an existing
   task/experiment ID before adding a new one. New tool: put research in the existing
   reference catalogue and queue, with dated sources and exact tested/unknown scope.
   New order: create/update its production brief and journal, not another roadmap.
2. **Choose disposition.** Active when it solves the current blocker and fits the
   environment; next when it helps the next milestone; reserve when useful only on a
   different OS/budget; paused when an owner/dependency blocks it; reject with reason
   when redundant or unsuitable. Being listed never means installed or qualified.
3. **Choose one learning objective.** For a commissioned/owner-requested film, first
   protect its creative result and delivery. Default to one main test and at most one
   small supporting check, with an existing-method fallback and a stop bound. A
   laboratory-led film may test more only if they form one coherent route and the
   owner selects that scope. No unrelated installations mid-production.
4. **Keep the active priority stable.** A new link does not interrupt current work.
   A fixed deadline, correctness problem or explicit owner reprioritization may do so;
   record what is displaced, why, its resume point and any lost/stale evidence.
5. **Close the loop.** Record outcome, versions, inputs/outputs, checks, human decision,
   measured cost/time and unknowns in existing evidence. Update milestone progress and
   propose the single next useful action. Promotion is scoped and reviewable.

Use this compact planning card in the relevant task/experiment document:

```text
ID / milestone / linked production:
Need and viewer-facing outcome:
Current evidence and missing capability:
Status / priority / dependency / next action:
Candidate and existing-method fallback:
Bound: duration, resources, cost, retries, stop condition:
Acceptance check and evidence location:
Owner decision / change to current order / resumption point:
Result, limits and reusable lesson:
```

The agent prepares and records; the owner selects creative routes, changes priorities
and accepts results. Existing authorization carries forward; this planning process
must not create repetitive permission questions for already authorized work.

## Production opportunities and protected waits

- **SSI:** v2.1 template owner-accepted; three new films reported prepared, not sent/published. Keep receiving-project ownership. Await partner/publication reports and the configured8November autonomous run outcome; do not duplicate its scheduler or infer autonomous success from configuration. Repeat-output evidence supports M3/M6 within this supplied scope.
- **Pocket OS:** paused until explicit resumption and device material. It can later
  exercise source-first editing, capture assistance and ASCII, not trigger them now.
- **Good Dog / later book series:** M5 destination; unique hero, continuity and
  multi-shot staging before a long film or 3–5 minute episodes. CoqPi and other promos
  remain opportunities, not silently selected productions.
- **Original publishable experiments:** choose a real hook, development and ending
  around R03–R05 needs. Default English where appropriate; retain project-specific
  languages. A technical demo is insufficient if the brief calls for a finished film.
- **Existing productions:** reuse authorized sources for internal controls when enough;
  record public URLs separately from acceptance, rights and audience measurements.

## Operating policy and measures

Free/open-source and macOS first for this owner; one heavy job at a time. A portable
catalogue can retain Windows/Linux/paid candidates without presenting them as locally
available. Persist each user's visibility preferences. Existing subscriptions are
separate from new spending. Free quota may justify a slow route, but cadence, actual
balance, rights and retries require current evidence. No fixed delivery promise from
advertised clip length or old credits.

At each milestone closeout record: active operator time, setup/wait/render time,
context recovery and repeated explanations, reused versus regenerated material,
requested versus avoidable corrections, costs/unknown exposure and delivery blockers.
Compare equivalent work before claiming savings. Track views/retention/revenue only
when actually supplied or retrieved, with comparable age and date windows; channel
performance is not a substitute for production evidence.

One production document/journal connects goal → scene purpose → shot/layer → retained
source → task → result → version-bound review. Add missing links to this model instead
of a second database. Editorial, directing, art, technical and sound expertise should
produce decisions/checks with inputs and outputs, not require a permanent agent swarm.

## How the existing documents fit

| Document | Responsibility |
| --- | --- |
| This roadmap | Strategy, milestone exits, priority and intake/change rules |
| [Next cycle](next-cycle.md) | Current production status, waits and dated progress; historical ordering yields to this roadmap and later owner decisions |
| [Producer-agency detail](producer-agency-roadmap.md) | Profile/catalogue/route/quota/community design and acceptance examples |
| [Experiment queue](experiment-queue.md), [tool research](tool-research.md) | Candidate details and historical scoped tests; queue position alone is not priority |
| [Post-release validation](post-release-validation.md) | RV01–RV03 measurement protocols, reused rather than renamed |
| [Book coverage](book/coverage.md), [BOOK-01](book-milestone.md), [editorial](editorial/README.md) | Portable cases, remaining examples and blog drafts; independent readiness/publication gates |

Update this map when a milestone changes, an owner reprioritizes, or a new capability
changes the feasible route. Routine tool details belong in the queue/evidence, not
another strategic rewrite. Review the next action after each completed task; do not
start a new recurring automation just to maintain the roadmap.

## Perplexity review: adopted, adjusted, deferred

Input: owner-supplied `FW.txt`, reviewed 28 October 2026; SHA-256
`6d06d20b61703d635269fbceb8801ce7c0134184392d557501b841d9986b2d8c`.
This is external advice, not executable instructions or verified repository state.
No private attachment or copied bulk prose is added to the repository.

**Adopt:** producer conversation; creative alternatives with tradeoffs; representative
risky pilot; scene purpose linked to source/task/review; human-readable state;
specialist decision checklists; separation of studio delivery and bounded laboratory
work; second-episode evidence rather than catalogue size as a success measure.

**Adjust to current evidence:** the review's descriptions of absent execution and
budget foundations partly predate PR #46. Local actions, recovery, admission and a
decimal ledger now exist, but full route execution and external budget enforcement
do not. Reuse these foundations. Offer one to three real alternatives, never insist
on three or show paid options against free-only preference. Route selection is not
spending or publication approval.

**Defer:** autonomous broad tool discovery, a new studio UI/platform, a new production
database, permanent multi-agent departments, unrestricted paid dispatch and automatic
community sync. Revisit only for a measured need in an active milestone. This plan
requires no new subscription, installation, model call, film or release.

## Newly assessed tools: adoption without priority drift

[30October adoption plan](research/agent-video-toolkits-2026-10-30.md):
FFMPEG-OPS-01 is a bounded local-adapter candidate; OM-BOARD-01 and OM-CORPUS-01
start from architectural reference and separate external trials;
VIDEO-SKILL-DISCOVERY-01 is discovery only. All support R05/R09, with source
retrieval linked to R02 and journal visibility to M2. No bulk installation.

After this consolidation, selected-delivery visibility and independent Good Dog recovery were verified on1November. Next: actual production-render admission; then the remaining R04 reuse/R05 confirmation evidence. Good Dog R07 production closeout is recorded separately.

## Historical follow-up after0.5.0

R03 recovery visibility: [selected-final implementation and isolated-process evidence](experiments/selected-final-recovery.md). Other waits remain explicit; [new-agent recovery](experiments/session-recovery-2026-11-01.md) now passes on Good Dog, while human-operator portability and whole-route evidence remain open. R04 selected production: **One Artist, Two Cities**, an English comparative Pokras Lampas art film using retained authorised sources, plus an alternate portrait edit. Measure scripted stage times and material reuse; baseline operator effort is unknown. One fitting R05 source-operation test uses ffmpeg-skill before any adapter promotion. Pocket OS remains paused.

R04 delivery: [33.208s comparative film and portrait adaptation](experiments/two-cities-reuse.md), owner review pending. Reuse controls and scripted stage timing are recorded; no measured labour saving or independent production qualification. R05 [first ffmpeg-skill trial](experiments/ffmpeg-skill-operations.md) is partial: cut/join and individual extraction succeeded; a timed-sheet failure prevents wider promotion.

30October owner accepted both R04 versions; [exact acceptance](experiments/two-cities-reuse.md). R07 now has the supplied original story and a [bounded pilot proposal](experiments/good-dog-preproduction.md). Canonical character/look and episode selection remain open. R06 is conditional on the selected pilot exposing an actual unsupported execution need; do not install another engine in advance.

Good Dog visual preparation:27supplied trilogy illustrations indexed; cover-dog and industrial-set draft passports bind exact references. Scale/rig/anchors and final look remain unresolved. [Source/visual boundary](experiments/good-dog-preproduction.md).

### R07 production case closed1November2026

[Good Dog closeout](experiments/good-dog-closeout.md): accepted133s v8 and owner-reported publication complete this bounded production case. Hybrid I2V/world/local-insert editing and targeted corrections are evidenced; whole M5, rig/identity automation, commercial clearance and full cloud-executor integration are not. Prioritise two-shot continuity and a publication-eligible expressive voice on the next selected film; then motivated physical contact, DJV and export regression tests. New finds retain their separate queue status.

PixelFX intake31October: [PIXELFX-01](research/pixelfx-codex-2026-10-31.md)
adds an optional pixel-effects trial to M4/R05 with motivated Good Dog R07 reuse.
It was not executed in Good Dog; trial only when a later scene needs pixel effects. No release follows automatically.

**1November block2:** [admitted Eevee trial](experiments/admitted-eevee-render-2026-11-01.md) passes on the saved Last Seed pilot scene-v4: bounded repeat/light edit, native interruption and explicit retry, with outputs review_pending. This supersedes the earlier statement that no Eevee action is admitted; it does not convert the historical manual film into a fully admitted production. REL-A needs a remaining-evidence assessment before a release decision. No release/commit/push performed.

**1November REL-A assessment:** [evidence matrix and remaining actions](release-readiness-2026-11-01.md). Blocks1/2 remain closed in scope. No new film or full-queue test is required for this release; consolidate the complete candidate, run final checks and review it before requesting a release decision. No commit/push/release authorised by this assessment.

**1November final local closeout:** [510-test full check and local review](final-local-review-2026-11-01.md) pass with18explicit skips. Caption overflow and stale catalogue fixtures corrected. Local REL-A readiness is evidenced; no new code-independent approval, remote CI, commit/push or release is implied. Next: authorised PR/CI and release decision, not another production/tool trial.

**1November release preparation:** merged-main CI on5a98bd6 passed. [0.6.0 REL-A candidate](release-audit-2026-11-01.md) is prepared locally; version/notes/package work does not itself publish a tag or release. No new functional gate or tool trial is added.

### 2 November intake — parameterized scenes and visible handoffs

[Unreal AI / Grok City assessment](research/unreal-ai-grok-city-2026-11-02.md):
PARAM-SHOT-01 extends R01/PREVIS-01 for a suitable REL-C shot; first use Blender
and verify it adds new evidence. UE-AI-01 remains deferred under M4/R05 and
conditional R06. Grok City's task ownership and human-decision queue extend
OM-BOARD-01 rather than creating another orchestrator. Grok Bot itself is a
reference with account/cost unknowns. No new production or test is started.

### 2 November lesson intake — motion guidance and bounded video edits

[Video-generation challenges](research/video-generation-challenges-2026-11-02.md)
adds conditional MOTION-GUIDE-01 and V2V-PRESERVE-01 under R05/R06/R07, using
local previz and an existing eligible provider only when a selected scene needs it.
Accepted-output yield enriches COST-01/R04; shot contracts and human decisions
extend existing controls. This is research, not a whole-route implementation,
new spending authority or a change to protected waits.

### 2 November closeout and next fiction selection

Storage/TokenEconomizer PR52 merged separately; [research closeout](research/intake-closeout-2026-11-02.md)
retains the new finds without starting their tests or triggering a release.
Owner selected LIT-FILM-01 / No Further Claims for REL-C planning; [episode/style/source
proposal](productions/no-further-claims-proposal.md) accepted by owner; production follows the short training block.
Then agree donor images, then two linked shots with both16:9/9:16 coverage.
No full film, account action or publication starts from this planning record.

### Pre-film training decision — 2 November 2026

[Разбор записок, платформ и трёх тренировок](research/continuity-motion-intake-2026-11-02.md) extends M4/R05–R06 and M5/R07 without a new release gate.
Owner approved the book proposal but requested analysis and several short training
films first. TRAIN-01/02/03 are proposed; select story/style/donors before execution.
Keep silent causality, bounded correction, meaningful resume and operator/machine
time separate. Heavy GPU candidates stay reserves; no whole-queue prerequisite.

Owner subsequently proposed [four training topics](productions/training-slate-2026-11-02.md)
in place of hypothetical TRAIN-01/02/03: scientific article visualization, animated
posters, surreal photo media art and practical airport routing. Recommended order
is provisional; use bounded new-feature tests with reusable evidence, then book film.


### Training-to-fiction checkpoint —3November2026

[Four accepted trainings](methods/training-to-fiction-2026-11-03.md) now supply bounded
R05/R06 lessons, not general tool qualification. Consolidate the documentation in
existing PR53; no release. Then prepare the owner-selected No Giant Eagle
100–120s montage/English text for16:9 and9:16, before exact donor/pilot review.
R06-MASK-01, R06-VOICE-01 and R07-PAIR-01 stay limited to useful next-production
questions. REL-C remains open until coherent fiction/interaction and recovery evidence.

### 4November — current character-production closeout

[No Further Claims method](methods/coherent-manga-production.md) consolidates the selected film. [REL-C matrix](rel-c-readiness-2026-11-04.md) now records bounded same-case cold resume PASS. PR53 merged after review/CI; the owner subsequently authorised the REL-C release. Earlier No Giant Eagle/preparation next steps above are historical and superseded.

### 4November — REL-C release decision

Same-case recovery PASS and independent additions review APPROVE; PR53 merged and
main CI passed. Earlier OPEN recovery/PR53-next-step notes above are historical.
Publish the authorised0.8.0 bounded methods release after release-PR/package checks.
Then wait for owner discussion; this does not start REL-D, another film or queued tools.


### 5 November — post-REL-C cycle completed; documentation closeout

[Owner-confirmed slate](productions/post-rel-c-slate-2026-11-05.md): both Radar films
(living-muscle robots and InfraDev) and the French illustrated book film
[Trois paquets](productions/harbour-three-parcels.md) are accepted and their publication
URLs owner-reported. The book film has YouTube16:9/TikTok9:16 packages and a book-page
embed. [French puzzle recipe](methods/french-illustrated-puzzle.md) preserves voices,
balloons, logic/reveal boundaries, corrections and known motion/source limits.

Owner authorised dependency-aware cleanup and a consolidated documentation/research
PR, without a release. YT-RADAR-01 maps to R04/R09/RV01; LIT-FILM-05 to M5/R07/R09.
Neither scoped repeat closes REL-D/M6 independent transfer or general mask/acting
qualification. New tool intake remains proposed; no queue-wide testing.
RUN-AUDIO-01 awaits the owner's concept without a fixed slot. Next film remains
unselected; refresh the existing Radar slate before any proposal. No scheduler,
account change, new production or release follows from this closeout.


### YT-RADAR-EXCHANGE-01 — local manual control,5November2026

[Thin exchange adapters](methods/radar-exchange.md) now link two existing films to
retained Radar ideas and return pinned publication receipts. Duplicate/recovery
checks passed locally; the existing InfraDev intake remains unchanged. Analytics
for both videos are pending in the retained acquisition. Opt-in normal-cycle hooks are implemented under the owner follow-up; their first
actual scheduled outcome, new prospective production and mature feedback remain open; REL-D is not closed.
No separate release is required for this development slice.
