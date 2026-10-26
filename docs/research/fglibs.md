# FGLibs: effect discovery and queued video trials

Reviewed 2026-10-26. Owner requested retention in the experiment queue after a
read-only catalogue/upstream review. No installation, MCP connection, code execution,
render, account grant or paid call occurred. All four entries remain untested.

## Discovery source

[F*cking Good Libraries](https://fglibs.com/) is a curated catalogue of libraries,
components and skills, searchable by a desired result. Its public connection dialog
advertises `https://fglibs.com/mcp`. Treat it as a source-finding aid, not a video
renderer or evidence that a listed effect is production-ready. MCP tool schemas,
authentication, limits, pricing and search quality have not been tested.

Before writing a custom effect: describe the intended shot, inspect a small shortlist,
follow the upstream source, check version/dependencies/media rights, then propose a
bounded capture trial. Keep the selected source and reason in the production journal.
Do not bulk-copy the catalogue or install its candidates automatically.

Proposed discovery test: compare three non-sensitive synthetic requests (photo reveal,
paper unfolding and animated report chart) against manual catalogue inspection.
Record relevant results, valid upstream links and missing/incorrect capability claims.
Read available MCP schemas before any later authorised connection; searches should
not contain private briefs/assets. Success means useful, traceable candidates;
runtime rendering remains a separate test.

## Selected tools and techniques

| Candidate / primary source | Intended use and first trial | Pass boundary |
| --- | --- | --- |
| [Emerging Images](https://github.com/akella/CodropsEmergingImages) | P1: shader-based image emergence for photo-series cinema or book art. One authorised image, two reveal variants, 6–8s at 1080p. | Repeatable absolute-time capture including out-of-order seeks; no unwanted image/calligraphy distortion, black frames or transition seams; inspect encoded output and owner preference. |
| [Paper Crumple](https://github.com/item-develop/paper-crumple-demo) | P2: crumpled paper unfolds into a book, letter or story card. One original paper design, 6–8s with a readable final hold. | Baked VAT playback and camera reproducible at specified times; no geometry clipping or texture loss; final text readable. Interactive physics must be frozen, seeded or baked before deterministic capture. |
| [EvilCharts](https://github.com/legions-developer/evilcharts) | P2, need-led: animated data charts for report/explainer films. One synthetic dataset, 8–10s with an animation followed by a two-second reading hold. | Values/units match input; stable labels at mobile size, repeatable seek/export, no hover/cursor dependency. Do not change accepted SSI templates or resume its production for this trial. |

Upstream repository pages identify MIT for all three codebases. This does not clear
all bundled images, fonts or dependencies. Emerging Images credits generated demo
images; use our cleared input instead. Paper Crumple documents a Houdini Vellum
simulation baked as vertex animation textures, decoded in Three.js with cannon-es
physics; supplied playback does not prove local Houdini authoring. EvilCharts uses
React/Next.js, shadcn and Recharts; UI animation does not prove frame-exact export.

Repository branches were inspected without pinning immutable revisions. Before any
runtime trial, retain the exact commit, licence texts, selected dependencies/assets,
local resource needs and capture route. Do not vendor upstream code or demo media.
Use the existing renderer/capture workflow where compatible; no new automatic planner
provider, sound capability or natural talking-face qualification is implied.

## Reuse after a successful trial

Retain an original thin scene wrapper with explicit time, image/data inputs, effect
parameters and an end hold. Record export checks, visual acceptance, source attribution
and limitations independently. Promote only the demonstrated effect/format; keep the
catalogue's discovery result separate from the chosen tool's production evidence.

[Queue](../experiment-queue.md) · [Tool inventory](../tool-research.md) ·
[Decision ledger](../../skills/video-production-router/references/review-ledger.json).
