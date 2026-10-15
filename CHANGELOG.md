# Changelog

## Unreleased

Add local production checkpoints with frozen brief/plan/packet,file pins,manual
step states,dependency invalidation and read-only resume/status. Atomic writes
and exclusive macOS/Linux locking preserve the last complete checkpoint;no render,
decode,installation or upload is performed.

Backfill PySceneDetect from retained Burgers evidence as an existing-video analysis
companion. Escape brief Markdown images/links,validate OpenScreen narration against
the pinned script/timing,ignore generated compilation thumbnails,and require the
retained local Remotion executable in its archive. No new release/model/media run.

## 0.2.0 — 2026-10-16 — experimental

- Add `plan.py BRIEF.json --format markdown`: a readable production packet with
  scene timing, selected tools/evidence, intended files, unmet requirements and
  separate planned video/still/voice QA. Default JSON and routing ranking stay unchanged.
- Close the six-book + landing + compilation stage. Preserve technical results,
  owner feedback, supplied publication URLs and failed/deferred attempts separately.
- Record scoped Three.js, ManimGX, voice, OpenScreen and MoviePy workflows; the last
  two remain manual recipes rather than automatic planner providers. The registry
  has sixteen profiles,including preparation,voices and documented music providers.
- Retain chain-wide evidence ranking, explicit voice/language choices, low-quality
  Piper fallback exclusion and independent music planning/source/rights gates.
- Condense README and move provider-specific agent guidance to on-demand selection
  references. Correct stale qualification prose; preserve historical packets/scores.
- Enforce original compilation music/thumbnail pins; fix archived environment and
  FFmpeg commands. No new rendering or provider/model calls for this release.

Current source remains `not_evaluated_current_source`. Historical v5 is70/70 rubric,
62/70 complete evidence;separate CLI recovery8/8 and original first-exposure13/18
remain distinct. Details:[evaluation](docs/router-evaluation.md),
[stage audit and deferred constraint validation](docs/product-audit-2026-10-15.md).

## 0.1.1 — 2026-10-14 — experimental

Fix planner dependence on requirement ordering: canonical traversal and repeated
resolution allow finishing tools to consume an export supplied later in the plan.
Rank primary tools by all requested capabilities, including deliverables, then prefer
local evidence before style/default tie-breaks. A tested native still no longer
requires an unnecessary video-and-extract route. Still-only delivery omits global
video assembly. Explicit tool choices remain fixed.
Regression cases and requirement permutations cover both review findings.

## 0.1.0 — 2026-10-14 — experimental

First public methods/skills release: six scoped routes, eight retained exports and
an eight-tool capability inventory. Includes Brag/Hyperframes software promos,
local EN/FR book montage, teaser, Anatomy prototype, Flute React camera scenes
and Remotion authored graphics. Known failed audio/snapshot paths remain visible.

New: block/layer planning by inputs, style, effects, language, paid availability and
frame timing; standalone offline JSON planner; generated source-backed capability
matrix; open Remotion reference route with prompt, pinned commands and QA contract.

Integrity checks now use explicit errors, discover experiment folders across dates,
and separate output schema and record-specific evidence markers. Native exports and
PNG thumbnails retain independent integrity checks. CI tests the library without
launching models/renderers. Router package contains no media, runtimes or weights.

Router status remains **structural_only**. Planner regression tests are not an
independent model evaluation. Reference sources are public; clean-machine re-render
after the lint dependency repair, measured time/cost and new mixed-chain execution
are not claimed. The next experiment is agent behaviour against the frozen scenarios.
