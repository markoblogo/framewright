# Framewright roadmap

Updated 30 October 2026, after [PR #46](https://github.com/markoblogo/framewright/pull/46)
merged. This is the primary **priority and milestone map**. It connects product work,
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

## Where we are

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

## Milestones and exit evidence

Milestones are outcomes, not release dates. A release is a separate owner decision.
Status is evidence-based: planned → active → partial/blocked → verified in stated
scope. A blocked experiment does not block unrelated approved production.

| Milestone | Current state | Exit evidence and dependencies |
| --- | --- | --- |
| **M1 — One understandable entrance** | Partial: unified R02 proposal verified internally; real owner selection remains | A real brief becomes a short approved concept, source/gap list and 1–3 genuinely feasible offers. Each explains creative result, prerequisites, human effort, cost/time basis, uncertainty, fallback and cheapest useful pilot. Persist free-only choice; distinguish declared access from checked access. Exercise RV02 and the existing decision contracts. |
| **M2 — One complete recoverable route** | Partial: individual local actions and saved-shot probe exist | On one selected route, pilot → review → production → technical/listening/creative checks → targeted correction → accepted local delivery. Resume in a new session without re-explaining retained decisions. Manual steps are explicit. Bind a saved-shot renderer first; record failure/recovery and preservation checks. Depends on a usable M1 offer, not a new UI application. |
| **M3 — A repeatable second production** | Partial: templates, branding, passports and SSI handoff exist | A comparable second episode and one alternate format reuse accepted design/materials with their own reviews. Exercise short/long/missing-optional template controls. Measure active work, setup, render/wait, context recovery and avoidable rework separately under RV01. Depends on an accepted baseline from M2 or a suitable existing film. |
| **M4 — Controlled expansion that improves a route** | Partial: catalogue/workbench and many scoped trials exist | One observed production weakness → bounded candidate comparison → exact feature qualification or rejection → repeat on another suitable production. Preserve a proven fallback. Extend cost/resource/platform coverage in small sourced batches. Can accompany M1–M3; does not require testing the whole queue. |
| **M5 — A coherent short fiction** | Preparation only | Before Good Dog's approximately three-minute adaptation, accept a two-shot interaction/continuity pilot with versioned hero/set, readable action, body/ground/prop contact and motivated sound. Then a coherent story, targeted correction and independent viewing/listening. Requires usable M2 execution/review and relevant M4 evidence; published dog/robot studies are preparation, not completion. |
| **M6 — Transfer and independent use** | Partial: SSI recipient integration reported; book base drafted | Another operator completes or resumes a bounded route from the handoff; record setup/support needs and unknowns. SSI's first actual scheduled delivery needs its own evidence. BOOK-01 remains its existing separate gate: cleared, reproducible cases and a useful sample chapter with/without Framewright. Optional community packets follow explicit opt-in and review; no telemetry or mandatory sharing. |

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
probes normally accumulate between gates. The owner authorized the 30October experimental consolidation release. REL-A remains
partial: fresh-process checks do not establish independent-session recovery or
complete admitted Eevee production. See the [release audit](release-audit-2026-10-30.md).

## Tactical work: now, next, later

IDs below are roadmap slices; existing SOURCE/ROUTE/RV/BOOK identifiers retain their
original meaning. One substantive implementation or production task is active at a
time on this Mac; related documentation can be updated during waits.

| Horizon / ID | Concrete task | Completion check | Maps to |
| --- | --- | --- | --- |
| **Verified internal scope · R01** | Bind the existing saved-shot Blender adapter to selected-route admission and sequential execution; reuse scene pins, controls and review helpers | Passed original Blender fixture: repeated render, exact subrange and light-only change; automated drift, timeout/interruption and output-contract controls. [Results](experiments/r01-saved-shot-executor.md). Full production route and creative acceptance remain R03. | M2, ROUTE-01 |
| **Verified internal scope · R02** | Join existing intake/profile/source-gap/proposal outputs into one readable producer brief, including why a scene exists | Passed retained free-only/broader brief replay, source-index evidence/gaps, project waits/drift and preference/constraint checks. [Results](experiments/r02-producer-brief.md). Real proposal selection remains R03; no invented costs or forced three-option count. | M1, RV02 |
| **Film accepted / publication reported · R03; recovery gate partial** | The Last Seed: owner accepted48.5s v4 picture and sound | [Recovery record](experiments/last-seed-recovery.md): local final copy matches accepted v4; title/description/tags/cover prepared. Native mixed-quality limits retained. Fresh-process recovery checked file pins and selected final bytes; stale historical waits remain visible. Independent-session recovery and manual Eevee/executor qualification remain open; publication owner-reported. | M1–M2, RV01, RV03 |
| **Next · R04** | Make a comparable second film or episode and alternate format on that accepted base | Review template edge cases; measure actual reuse and operator effort without counting first-time template development as recurring work. | M3, RV01 |
| **Next · R05** | Test one missing capability exposed by R03/R04 | Existing-method baseline, one candidate, same inputs and explicit accept/reject criterion; record negative results and whether a second production confirms them. | M4 |
| **Later · R06** | Broaden admission to another needed local adapter or one pinned ComfyUI workflow | Concrete scene need, available host/model/rights, failure path and retained output. Do not bulk-install nodes or rewrite orchestration. | M2/M4, COMFY-01 |
| **Later · R07** | Build the Good Dog continuity pilot from an owner-selected excerpt | Two coherent shots, actual travel/contact/interaction, stable hero and set, intelligible motivation; preserve a simpler staging fallback. | M5, PREVIS-01 |
| **Later · R08** | Add provider/quota execution only when a selected production needs it | Current terms/account evidence, retry reserve, per-operation authority, ambiguous-charge recovery and no duplicate submission; local cost ledger alone is insufficient. | M2/M4, COST-01/STATE-01 |
| **Ongoing closeout · R09** | Convert useful outcomes into reusable methods, case studies, post material and book coverage | Update exact evidence, existing queue/registry, chapter gap and next action. Retain with/without Framewright instructions; do not claim reader reproduction before it happens. | M6, BOOK-01 |

R01 and R02 are complete within their internal test scopes. R03 now has an
owner-accepted48.5s Last Seed film and reported publication; full-route execution
and independent recovery remain unproven. The roadmap
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

- **SSI:** keep receiving-project ownership. Await actual first scheduled run and
  fresh video/delivery assessment; do not duplicate its scheduler or declare success
  from deployment. Suitable evidence for M3/M6 if supplied.
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

After this consolidation: first resolve selected-delivery versus historical-wait
visibility and independently exercise recovery; then R04 measured reuse and one
R05 candidate on that production. Good Dog R07 follows a two-shot continuity pilot.
