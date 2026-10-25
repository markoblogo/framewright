---
name: video-production-router
description: Plan video production scene by scene and layer by layer using evidence-aware tool choices, reusable workflows and output checks; record new production experiments. Use when planning a video or comparing video tools; not for ordinary image generation or YouTube copy alone.
---

# Video production router

Select a method before committing to a toolchain. For arsenal discovery,filters
and compatible proposed chains,read [search](references/arsenal-search.md) and use
`scripts/search.py`;keep evidence/rights limits and explicit choices visible.
Search/comparison alone never authorises execution. This skill selects and records;
it does not replace rendering skills or confer permission to publish.

For recuts, sourced insight stories, hybrid films or private music libraries, read
[shared studio intake](references/studio-workflows.md). Reuse one source/claim/EDL
contract; `workflow.py` adds experimental confirmation/delivery gates to the existing
checkpoint, not a new production route. `library.py` only scans an explicitly chosen
local folder. No actual source/track is needed for conditional planning. Origin is
separate from video/audio rights; remove unknown source audio when required and
block publication until retained rights are resolved. Never infer a reuse grant from
Telegram/X availability. New combinations remain unqualified until a bounded trial.

For recorded speech, multiple takes or screencast recuts, read the optional
[editing module](references/editing.md): source inspection, cut-only time maps,
subtitle/overlay retiming and playable join-review packs. It uses the existing
project and selected assembler; generated review media do not approve content.
For repeated company/deck styling, read [brand profiles](references/branding.md): freeze selected assets/tokens, export the same profile, and check each rendered variant. Profiles do not inherit film approval.
For a concrete correction, read [revisions](references/revisions.md). For an accepted
film becoming a series, read [template contracts](references/templates.md). Both
reuse the journal; rendering and per-variant approval remain separate.

1. Use the brief's product, available assets, audience/language, format, narration,
   cost/account constraints and intended deliverables. Ask only for missing facts
   that materially affect the choice. For a production plan or execution blocked
   by missing support/evidence, request the unresolved choice or propose a bounded
   future test with pass conditions; naming a prerequisite alone does not resolve it.
   For comparison-only feasibility, a supported negative answer and its limits can
   be complete: do not require relaxing constraints or an unsolicited experiment.
   Preserve the user's explicit tool choice.
2. For requests with style/effect requirements or multiple scenes, read
   [selection guidance](references/selection.md). For Russian or English camera/edit
   terms, use the [24-technique glossary](references/video-terms.md). Preserve exact
   technique requirements; a generic camera/export feature does not prove dolly zoom,
   rack focus or audio split edits. When a creative reference is requested, use the
   [reference-selection workflow](references/creative-references.md) before production. Decompose into blocks and picture,
   text, voice, sound and finishing layers. Consult [the tool matrix](references/tool-matrix.md)
   and only relevant profiles in `references/tools.json`. The optional offline
   `scripts/plan.py BRIEF.json` shortlists tools; it never executes the plan. Add `--format markdown` for a
   readable production packet: timeline, capability evidence, intended files and
   common per-output QA. Every checkbox remains planned/blocked; source kinds and
   suggested filenames are not inspected/delivered artifacts. The packet supplements,
   rather than replaces, the full handoff and renderer-specific contract.
   For work spanning sessions, use [production checkpoints](references/projects.md):
   freeze the accepted brief/plan, register actual files and record manual states.
   Resume inspects pins and remaining work; it never executes or marks QA passed. Distinguish
   tested, documented, failed and unknown features; preserve cost/language/format limits.
   For a new multi-shot video without a useful shot plan, read the
   [storyboard adapter](references/storyboard.md) and establish its shot/continuity
   handoff before production. Skip it for comparison, finishing, recuts or a single
   shot; it is a preparation layer, not a renderer or permission to generate clips.
   For short story-led book/project promos, use the optional
   [narrative-promo module](references/narrative-promos.md) for causal beats,
   reference roles and event-linked sound; it does not change the selected renderer.
   Then read [the catalogue](references/catalog.json), then only the matching section
   of [the recipes](references/recipes.md). Recommend a default with one sentence
   of evidence and relevant limits. If the user only asks to compare, stop there.
   For music or songs, read [music workflows](references/music-workflows.md): choose
   brief-first, video-first or music-first; keep singing separate from TTS, and
   classify native video before reuse. The optional `scripts/music.py MUSIC.json`
   or `music` object in a picture brief records independent source/rights/account
   gates. It does not generate or download music. Cloud music profiles are documented,
   not publicly tested; private probes do not change that qualification.
3. Follow the selected renderer's instructions. Verify its installed API, licence
   eligibility and pinned package version before execution. For Hyperframes-backed routes,
   load the installed `hyperframes` entry skill and relevant composition/audio/media
   guidance. For `live-react-scene` or another explicitly selected renderer, load
   that tool's installed guide directly; Hyperframes is not a prerequisite. If the
   selected route lacks instructions or dependencies, inspect its upstream docs
   and report the gap without silently installing tools. Preserve the requested
   format rather than applying today's horizontal 1080p examples to every job.
   Renderer-specific preflight belongs in the handoff, including blocked checks:
   Flute: genuine components, explicitly scoped capture-style overrides, synthetic
   inputs, production exclusion and the recorded snapshot failure. Remotion: pin
   package versions, check installed API/official skills and licence eligibility,
   retain downloaded-browser failure plus workaround, and inspect native stills
   separately from encoded picture/audio when stills are requested.
4. Work from verified product facts and authorised assets. In a prompt-only task,
   state an absent asset as a prerequisite inside the prompt (“use the approved
   logo once supplied”); do not imply it is available or inspected, or add intake.
   When shortening existing
   material, preserve factual claims and reading order unless the user requests a
   substantive rewrite. Measure generated speech
   before finalising cuts. Keep deterministic seekable picture timing and sound cues
   on a common timeline. Inspect the encoded final file, not just an intermediate mix.
5. For production planning, implementation/execution or finishing, read the [QA/handoff contract](references/handoff.md).
   Explicitly compare proposed copy with its named source, and identify whether
   each thumbnail is reused, newly rendered natively or extracted from video.
   If the current chain already meets deliverables, finish outstanding QA and
   hand over the result without adding tools or experiments. No more tools does not
   mean QA is complete; retain any checks blocked by missing files or authority.
   Before finalising a plan, check each requested output against its own handoff
   row and retain every named check, explicitly planned/blocked where necessary.
   Apply output-specific transparency and effect-specific temporal checks from that contract.
   Keep thumbnail QA separate from MP4 QA; preserving an image as-is does not
   replace inspecting its existing crop. Do not silently omit checklist items.
   For a plan-only request, name the intended output artifacts and the remaining
   QA/delivery steps; missing media blocks verification, not listing those steps.
   Deliver the export, thumbnail, subtitles/copy if requested, and honest QA status.
   Distinguish automated checks, human listening, user acceptance and public upload.
   Ask before external publication or a paid/account-authorisation step unless
   already authorised. Honour stop signals and do not extend a successful test into
   adjacent experiments without request.

For scoped default routes, voice preferences and renderer-specific limits, read
[route choices](references/selection.md#scoped-route-choices). These remain
separate from capability coverage and execution authority.

Before a new candidate or repeat trial, inspect [the review ledger](references/review-ledger.json).
Search by tool ID/upstream and read only relevant records. After every review or
trial, update the ledger and documentation, including rejected or blocked/no-run
outcomes. Retain negative, rights-blocked and deferred decisions as well as successes; name
the changed version, terms, requirement or unresolved feature before repeating work.
For a new candidate, record its source/version, task, inputs, side effects/cost,
test, failure modes and evidence before promotion. In a full checkout, use
`docs/experiments.md` and `templates/experiment.md`. If installed standalone, retain
these fields in the active project's own experiment record instead. Keep large
artifacts outside Git. Never weaken QA thresholds to rescue an effect. Record the failed attempt;
propose revision/removal, and obtain acceptance before dropping a requested effect.

Routing behaviour scenarios are in [scenarios.json](references/scenarios.json).
They are specifications, not evidence of an independent model evaluation.

For continuing production, use [project memory](references/projects.md): resume
an existing checkpoint before planning another one. Schema-2 observations bind
technical QA, listening, creative decisions and publication to retained revisions.
Keep explicit owner waits and rejected/stale receipts visible; never infer
acceptance from a filename or completion from an observation. Manual projects
cover existing game/virtual-set work without fabricating a router-qualified plan.

For script/capture/edit coordination and reuse, use the same project's
[composition and local kit](references/production.md). Bind real material versions,
keep main/Short cuts distinct, and expose missing footage/rights/narration.
A collected kit is a local handoff; never infer publication authority from it.

Before promising audio/image/video evaluation or asking an operator to record, use
[media review and recording rehearsal](references/media-review.md). For a unified file report and project import, read
[media-review reports](references/media-review-reports.md). Check actual
session input support; level measurement/ASR/frame sampling never substitute for
listening, motion or sync review. The local `capture_check.py` reads short clips;
cloud/local multimodal candidates need separate bounded qualification and authority.

For current project documentation and Trends/Radar follow-up, use
[derived status and content outcomes](references/project-insights.md). Project a
selected safe public summary instead of copying private checkpoint notes. Record
retrospective ideas honestly; missing views/retention/revenue remain unknown.
For an already controllable canvas scene, use the [local capture adapter](references/engine-capture.md).
Validate offline first, then execute only with authority for that scene and local
browser. Preserve seam warnings and separate technical, listening and creative checks.
