# IngeTrazo: editable sets for video

Reviewed 2026-10-26; owner requested retention and a queued test. Status:
**documentation-reviewed candidate**, not installed, connected or render-tested.
No accounts, paid calls, model downloads or production assets were used.

## Sources and documented scope

- [Official site](https://ingetrazo.com/en/): architecture/engineering 3D modeler;
  macOS Apple Silicon build, materials, real terrain and component library.
- [Upstream repository](https://github.com/ingelibre/ingetrazo): GPL-3.0-or-later,
  eye-level walkthrough, glTF/GLB export and Python extension system. Project remains
  0.x; file format and plugin API may evolve. No immutable revision was pinned in
  this read-only review; pin exact release/commit and licences before the trial.
- [AI/MCP manual](https://ingetrazo-docs.pages.dev/ia/): local bridge, Python actions,
  model queries, actual viewport screenshots and undo/redo. Codex is listed as a
  compatible client; our macOS/Codex connection has not been tested. The bridge is
  documented as loopback-only, with one client at a time. Python execution is an
  execution capability, not a read-only integration.
- [Scenes manual](https://ingetrazo-docs.pages.dev/modelado/organizacion/): named views
  retain camera, layer visibility, style, section and sun state. Saved views do not
  establish a timed animation/capture API.
- [Import/export manual](https://ingetrazo-docs.pages.dev/importar-exportar/): native
  editable documents and interchange formats. Inspect actual exported materials,
  units, orientation and hierarchy rather than assuming round-trip fidelity.

## Intended Framewright role

Create reusable rooms, streets, buildings and props as editable filming sets for
book promos or fiction. Proposed handoff: IngeTrazo model → GLB → existing Three.js
scene/capture workflow → encoded review clip. This is a proposed integration, not a
qualified route. Native character animation, timeline/video export, photorealism,
camera transfer and performance are unverified. No new automatic planner provider.

## P2 bounded trial: one room, one camera move

1. Before installing/connecting, inspect the exact Mac build, dependencies and MCP
   launch path; agree the bounded trial and local execution scope. The site describes
   unsigned builds: do not silently weaken OS protections. Existing local rendering
   dependencies should be reused where possible; no new paid provider is required
   by this proposed workflow.
2. Use only a simple original room with a door and window, specified dimensions and
   two materials. Create it through the bridge, query group names/bounds, inspect a
   viewport image and verify one reversible correction. Save/reopen the native file.
3. Export GLB and inspect it in the existing Three.js workflow. Compare dimensions,
   axis orientation, door/window openings, normals, materials and hierarchy against
   the source. Record any lost cameras/styles rather than recreating them silently.
4. Author a deterministic 10-second 1920×1080 camera pass in the receiving renderer.
   Check repeated and out-of-order seeks, camera clipping, encoded decode and visual
   continuity. Owner viewing is required for creative acceptance; technical checks
   alone do not qualify the tool or wider fiction workflow.

Retain exact versions, source/native/export revisions, captures, resource use,
failures and user review. Pass means the one-room author→edit→save→export→capture
chain works with usable fidelity. Broader sets, terrains and character integration
remain separate trials. Do not start Good Dog production from this queue entry.

## Rights and reuse

Code licence and media rights are separate. The site identifies mixed CC0, CC BY and
Free Art License items from Sweet Home 3D; check each chosen item and attribution
before use. Start with original geometry/materials instead of importing the whole
library. Map/terrain data also have independent terms. Keep third-party assets and
upstream code outside Git; retain source/licence notes and an original thin export
adapter only after a successful trial. No claim of blanket commercial clearance.

[Queue](../experiment-queue.md) · [Tool inventory](../tool-research.md) ·
[Decision ledger](../../skills/video-production-router/references/review-ledger.json).
