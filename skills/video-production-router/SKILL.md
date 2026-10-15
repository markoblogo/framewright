---
name: video-production-router
description: Choose a tested video-production workflow for software promos, book trailers, music-driven videos, or announcements, and record new production experiments. Use when planning a video or comparing video tools; not for ordinary image generation or YouTube copy alone.
---

# Video production router

Select a method before committing to a toolchain. This skill selects and records;
it does not replace rendering skills or confer permission to publish.

1. Use the brief's product, available assets, audience/language, format, narration,
   cost/account constraints and intended deliverables. Ask only for missing facts
   that materially affect the choice. For a production plan or execution blocked
   by missing support/evidence, request the unresolved choice or propose a bounded
   future test with pass conditions; naming a prerequisite alone does not resolve it.
   For comparison-only feasibility, a supported negative answer and its limits can
   be complete: do not require relaxing constraints or an unsolicited experiment.
   Preserve the user's explicit tool choice.
2. For requests with style/effect requirements or multiple scenes, read
   [selection guidance](references/selection.md). Decompose into blocks and picture,
   text, voice, sound and finishing layers. Consult [the tool matrix](references/tool-matrix.md)
   and only relevant profiles in `references/tools.json`. The optional offline
   `scripts/plan.py BRIEF.json` shortlists tools; it never executes the plan. Distinguish
   tested, documented, failed and unknown features; preserve cost/language/format limits.
   For a new multi-shot video without a useful shot plan, read the
   [storyboard adapter](references/storyboard.md) and establish its shot/continuity
   handoff before production. Skip it for comparison, finishing, recuts or a single
   shot; it is a preparation layer, not a renderer or permission to generate clips.
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

Prefer Brag full for a short software launch; prefer the local narrated montage
recipe for existing book imagery with speech. Brag itself also supports voice:
our silent Brag tests do not establish a product limitation. Anatomy is a visual
prototype option, not a validated physics or finished sound workflow here. Do not
choose it just because a video contains an object. Historical reconstruction and
new AI-video services require bounded tests, not an invented capability claim.

For camera travel and focus around an existing React interface, consider the
tested `live-react-scene` Flute recipe. An explicit Flute request overrides the
default renderer choice; load its installed guide. Its browser-host success does
not prove full Electron or arbitrary React support. Keep the ordinary app and
production bundle outside the demonstration. Scope capture-style overrides to the
development host so genuine components retain their ordinary app styling.

For authored React motion graphics with a controllable frame timeline, native
audio and stills, consider `authored-react-film` (Remotion). Distinguish it from
camera treatment of existing app UI. Keep its own licence and observed browser
workaround visible; a successful pilot does not prove every rendering mode. If a
native still is a requested deliverable, plan its own inspection alongside the
encoded picture/audio rather than substituting an extracted or pre-existing frame.

For a miniature world with purposeful object action and camera travel, consider
`staged-3d-scene`: an authored Three.js scene inside Hyperframes, not Anatomy.
Use `three-scene` with `staged-3d`, `object-3d`, `object-motion` or `camera-travel`
requirements, or miniature/low-poly style. Do not infer it from a book cover alone.
The tested 20s 1080p30 pilot has grain loading, truck delivery, quote convergence
and a genuine-cover book reveal. Keep geometry/staging work explicit. Read its
[recipe](references/recipes.md#staged-3d-scene); other formats, physics, new assets
and cross-tool seams need their own checks. Kokoro and FFmpeg are separate layers.

When the chosen tool misses a requested deliverable, compose the smallest useful
chain rather than drop the deliverable or replace the whole workflow. Read
[tool chains](references/tool-chains.md) for handoff checks and tested combinations.
A successful component does not prove the combined chain; preserve the original
export, check the final file and record each tool's contribution and limitations.

For a new candidate, record its source/version, task, inputs, side effects/cost,
test, failure modes and evidence before promotion. In a full checkout, use
`docs/experiments.md` and `templates/experiment.md`. If installed standalone, retain
these fields in the active project's own experiment record instead. Keep large
artifacts outside Git. Never weaken QA thresholds to rescue an effect. Record the failed attempt;
propose revision/removal, and obtain acceptance before dropping a requested effect.

Routing behaviour scenarios are in [scenarios.json](references/scenarios.json).
They are specifications, not evidence of an independent model evaluation.
