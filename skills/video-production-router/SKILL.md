---
name: video-production-router
description: Choose a tested video-production workflow for software promos, book trailers, or announcements, and record new production experiments. Use when planning a video or comparing video tools; not for ordinary image generation or YouTube copy alone.
---

# Video production router

Select a method before committing to a toolchain. This skill selects and records;
it does not replace rendering skills or confer permission to publish.

1. Use the brief's product, available assets, audience/language, format, narration,
   cost/account constraints and intended deliverables. Ask only for missing facts
   that materially affect the choice. Preserve the user's explicit tool choice.
2. For requests with style/effect requirements or multiple scenes, read
   [selection guidance](references/selection.md). Decompose into blocks and picture,
   text, voice, sound and finishing layers. Consult [the tool matrix](references/tool-matrix.md)
   and only relevant profiles in `references/tools.json`. The optional offline
   `scripts/plan.py BRIEF.json` shortlists tools; it never executes the plan. Distinguish
   tested, documented, failed and unknown features; preserve cost/language/format limits.
   Then read [the catalogue](references/catalog.json), then only the matching section
   of [the recipes](references/recipes.md). Recommend a default with one sentence
   of evidence and relevant limits. If the user only asks to compare, stop there.
3. Follow the selected renderer's instructions. For Hyperframes-backed routes,
   load the installed `hyperframes` entry skill and relevant composition/audio/media
   guidance. For `live-react-scene` or another explicitly selected renderer, load
   that tool's installed guide directly; Hyperframes is not a prerequisite. If the
   selected route lacks instructions or dependencies, inspect its upstream docs
   and report the gap without silently installing tools. Preserve the requested
   format rather than applying today's horizontal 1080p examples to every job.
4. Work from verified product facts and authorised assets. Measure generated speech
   before finalising cuts. Keep deterministic seekable picture timing and sound cues
   on a common timeline. Inspect the encoded final file, not just an intermediate mix.
5. Deliver the export, thumbnail, subtitles/copy if requested, and honest QA status.
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
production bundle outside the demonstration.

For authored React motion graphics with a controllable frame timeline, native
audio and stills, consider `authored-react-film` (Remotion). Distinguish it from
camera treatment of existing app UI. Keep its own licence and observed browser
workaround visible; a successful pilot does not prove every rendering mode.

When the chosen tool misses a requested deliverable, compose the smallest useful
chain rather than drop the deliverable or replace the whole workflow. Read
[tool chains](references/tool-chains.md) for handoff checks and tested combinations.
A successful component does not prove the combined chain; preserve the original
export, check the final file and record each tool's contribution and limitations.

For a new candidate, record its source/version, task, inputs, side effects/cost,
test, failure modes and evidence before promotion. In a full checkout, use
`docs/experiments.md` and `templates/experiment.md`. If installed standalone, retain
these fields in the active project's own experiment record instead. Keep large
artifacts outside Git. Never weaken QA thresholds to rescue an effect; revise or
remove the effect and record the failed attempt.

Routing behaviour scenarios are in [scenarios.json](references/scenarios.json).
They are specifications, not evidence of an independent model evaluation.
