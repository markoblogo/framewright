# Product audit and agricultural-stage closeout — 2026-10-15

Status: owner accepted the readable production packet only. Strict brief/resource
validation is deferred;documentation consolidation remains accepted. No new
render, provider call, release or merge is performed by this audit.

## Product and next user action

Framewright helps an agent turn a video brief into an evidence-aware production
method. The agent executes external tools; Framewright supplies planning logic,
recipes, limitations and handoff instructions. The first action should be producing
an inspectable production plan or following the open reference-film recipe.
The audience is an agent operator planning and producing video from authorised
materials. Books/software promos are initial evidence,not a product boundary.
Owner clarified the general video-production positioning on2026-10-16;new genres
still need scoped qualification.
No audience/conversion, comparative cost or general reliability claim is established.

## Closed production stage

Owner closed the agricultural-book production stage. Six book films, one library
landing tour and one series compilation were delivered; all eight have owner-supplied
publication URLs in the [series record](experiments/agro-series-plan.md). These are
not eight independently byte-matched public uploads. Closure does not fill pending
individual listening/style reviews. No further production before the next release;
a new experiment direction will be selected afterwards.

Across the repository, the current integrity check counts 17 recorded exports and
10 method entries. The offline planner registry has 16 profiles; these include
voices, preparation and documented-only music services, not 16 qualified renderers.

## What worked and where it stopped

| Observation | Evidence and product implication |
| --- | --- |
| Reusable outputs close a real production loop | Six books plus landing feed the 60s MoviePy compilation; silent masters and separate audio allow a new series narrative instead of concatenated old narration. Keep these handoff boundaries. |
| Purposeful staging gave more interesting visuals | Owner preferred the Spot-Market 3D action/camera treatment; basic infographic and paper styles were acceptable. Tool availability alone does not supply a creative idea or guarantee visual quality. |
| Voice quality depends on exact profile and language | Supertonic3 F1 English was owner-accepted as natural; Ukrainian M1/F1 probes were usable with residual stress/pauses. Exact Piper/Tetiana remains an explicit low-quality fallback, excluded from automatic default narration. |
| Companion tools rescued limited native workflows | FFmpeg timing, audio and finishing adapters; scoped OpenScreen capture workarounds; MoviePy assembly. These qualify the recorded chain, not every native feature. |
| Negative results prevent repeated waste | ACE-Step remains incomplete/resource-gated; no retained final music. Delayed revisit is a condition, not a scheduled retry. Preserve failures and rights decisions. |

Different books/scripts/styles do not form a controlled renderer or voice comparison.
No measured evidence establishes production speed, setup-cost savings or audience lift.

## Baseline audit

- `python3 scripts/check.py --scope docs`: PASS, 158 unit tests, retained-packet
  validation, links/records, generated matrix and standalone ZIP smoke. No model/render.
- Router qualification: `not_evaluated_current_source`. Historical v5: 70/70 rubric,
  62/70 complete evidence; separate capture recovery 8/8 does not create a new full-run
  result. Original first-exposure transfer-2 remains 13/18.
- GitHub: PRs #28 → #29 → #30 → #31 form an open dependent chain; all currently
  mergeable with successful validate checks. This is not a review-approval claim.
  Release baseline is experimental v0.1.1. Recheck reviews and integrate in order
  before tagging a reviewed merge commit.
- README: 159 lines; main route table is followed by repeated dated pilot paragraphs.
  The skill entry also accumulates provider-specific narrative. Historical audit
  prose says eleven profiles although the registry has sixteen.
- `docs/router-evaluation.md` ends with an obsolete assertion that the active status
  is `model_checked_planning_scope`; the canonical JSON and checker say otherwise.
- Brief parsing validates known values but ignores unrecognised keys. A probe adding
  `budget: {max_usd: 0, max_setup_minutes: 5}` returns exactly the same plan as omitting
  it. That object is not a supported budget contract; silently ignoring it is a
  usability risk. `allow_paid` is only a capability filter, not a price/resource cap.
- Structured output contains coverage, limitations and a generic assembly checklist;
  it has no per-output planned/blocked/verified QA contract. Detailed checks live in
  the handoff guide, so the agent must reconstruct them in each production plan.

## Product decisions

### 1. A readable production packet — accepted

Add an offline Markdown view generated from the actual structured brief/plan:
scene timeline, selected tools and capability evidence, unmet requirements, required
inputs, intended outputs and output-specific QA. Keep JSON as the machine interface.
Checks start planned or blocked; generation must never assert they passed. Separate
image provenance, video/audio QA and human listening. Link detailed tool guides rather
than copying them. Ship a genuine generated example and include it in package smoke.

Acceptance: a newcomer can run one documented command and review scene ownership,
outputs and blockers without decoding raw JSON; still-only plans do not get video
checks, unverified assets never become verified, explicit choices remain visible.
No natural-language model, renderer or account integration is added.

### 2. An explicit brief and constraint contract — deferred

Validate the supported brief shape, reject misspelled/unsupported decision keys with
useful messages, and provide a deliberate extension area for non-routing metadata.
Add explicit resource constraints to the packet: spending/download/setup limits and
local-only requirements are either checked against retained facts or shown as
unresolved preflight gates. Unknown price/runtime must not become zero or compliant.
Keep `allow_paid` separate from permission to buy. Prefer a small supported contract
over invented tool prices or a universal runtime detector.

Acceptance: a zero-budget or no-download request cannot silently lose its constraint;
unsupported fields fail clearly; an unavailable estimate yields a visible unresolved
gate, not a claim that the chain fits. Existing documented briefs remain usable.

These changes address repeated planning/QA repair. They do not raise current model
qualification or imply enforcement by a sandbox.

## Documentation and release plan after owner selection

1. README: product sentence, two entry actions, one actual packet example, concise
   route table, proof/limits and installation. Move dated experiences behind the
   series closeout and experiment index; target roughly 90–110 useful lines.
2. Keep SKILL procedural with on-demand voice/renderer/QA references. Replace stale
   counts/status claims from canonical records. Do not discard evidence or old scores.
3. Summarise Unreleased changes by user benefit; preserve historical detail in the
   linked experiment/evaluation records. Stop appending a mini report per pilot.
4. Add only focused deterministic regressions and standalone smoke for selected
   features, then the existing offline release gate. No broad actor rerun unless a
   separately agreed claim requires it; no media production.
5. Review open PR feedback, integrate the dependent chain safely, then publish a
   new experimental release with ZIP and SHA256SUMS from the reviewed merge commit.
   Version: 0.2.0 for the new readable planning interface.

Future work: independent reference reproduction, an agreed new production direction
and any ACE-Step revisit remain outside this pre-release implementation stage.

## Accepted implementation — 2026-10-16

Only the readable production packet was selected. `--format markdown` now exposes
the actual timeline,coverage/evidence,explicit choices,intended outputs and common
planned/blocked per-output QA. JSON/ranking remain unchanged. Strict brief/resource
validation stays deferred and that limit is visible in the guide/packet.

README shrank159→119lines,skill entry149→104,CHANGELOG105→54. Provider-specific
agent guidance moved into the existing selection reference;dated production
records remain discoverable through the closed series. Current qualification prose
now agrees with the canonical JSON;no historical score was promoted.

Offline gate passed167tests,retained-evidence validation,local links,generated matrix
and standalone JSON/Markdown package smoke. Compilation auxiliary source pins and
a pre-PCM summed-peak guard address pending archive review findings without media
regeneration. Release publication/merge/asset verification are separate remaining
gates at the time of this implementation record.
