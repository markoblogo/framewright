# PlayCanvas: controlled scenes first, Snapchat later

Reviewed 2026-10-26. Owner selected an **active candidate for a bounded local trial**.
This is retention in the queue, not immediate installation, account access, paid
usage or publication authority. No runtime, Editor MCP or Snapchat trial has run.

## Three separate stages

1. **First: local scene and capture, 15–20 seconds.** One cleared character, one
   visible action, a controlled camera and sound. Pin the engine/dependencies and
   assets; retain an original local project. Add explicit reset/seed/time controls
   rather than assuming real-time playback is reproducible. Reuse our capture adapter
   if compatible; inspect the actual encoded result. Compare repeated and out-of-order
   time samples, character contact/motion, camera, sound cues and picture/audio sync.
   Full decode and viewing/listening remain separate from source checks. Obtain owner
   review and record effort, local resources and limitations against the existing
   Three.js workflow on matched output scope; no assumed quality/speed advantage.
2. **Then, only if useful: Editor MCP.** Pin server and Editor versions. Review the
   exact account/project/visibility/plan and access scope before connecting; a private
   hosted project needs a paid plan according to current documentation. Read-only
   inspection must identify the intended project first. Create a checkpoint, change
   one light/material while preserving character/camera/timing, and verify both Editor
   and running scene. The bridge edits live project state and can perform destructive
   operations; do not infer broad account or destructive-action authority from a
   capture trial. Local Engine success does not qualify Editor MCP.
3. **Separate future experiment: Snapchat publication.** No upload or game submission
   now. Later choose a suitable small portrait game, review creator/asset/SDK terms,
   check the then-current beta requirements, package and test separately. Publication,
   moderation, audience response and monetization require their own evidence and
   authority. Desktop SDK stubs are not proof of real Snapchat API behavior.

## Documented capabilities and sources

- [Announcement](https://blog.playcanvas.com/snapchat-now-supports-playcanvas-games/)
  describes Web Lenses and two authoring routes: standalone Engine with a coding
  agent or hosted Editor through MCP. This review did not run its starter/installer.
- [Engine](https://developer.playcanvas.com/user-manual/engine/) is MIT-licensed,
  browser-based WebGPU/WebGL2 with cameras, animation, physics, sound and glTF.
  Engine code rights do not clear demo characters, textures or sound. No immutable
  revision was pinned in this review; retain one before execution.
- [Gaussian Splatting](https://developer.playcanvas.com/user-manual/gaussian-splatting/)
  is a possible later virtual-set route. No Marble export, relighting, character
  occlusion, collision or moving-camera fidelity was qualified. Do not silently
  expand the first local trial into a world-provider experiment.
- [Editor MCP](https://developer.playcanvas.com/user-manual/editor/mcp-server/)
  documents Codex setup, scene/asset/script edits, runtime inspection, input and
  checkpoints. A standalone Engine project does not require the hosted Editor.
- [Official agent skills](https://github.com/playcanvas/skills) are a documentation
  source, not installed or vendored here; skill availability is not runtime evidence.
- [Snap package requirements](https://developers.snap.com/web-lenses/requirements)
  currently state compressed ZIP ≤8 MB, root index.html ≤1 MB and relative paths.
  [Runtime](https://developers.snap.com/web-lenses/runtime-environment) is portrait
  9:16; [restrictions](https://developers.snap.com/web-lenses/capabilities)
  must be checked before later use. The announcement describes no ordinary network,
  camera or microphone access. These are Snapchat constraints, not Engine limits
  for our horizontal films. Platform details remain beta and can change.

## Evidence boundary

All three stages are untested. No automatic planner provider or tested capture
route was added. Keep native scene, camera/control script, final encoded artifact,
rights/provenance, technical QA and owner acceptance separately. Large assets,
downloaded upstream code, models and media remain outside Git. Passing one stage
does not qualify the others or justify publication/audience/monetization claims.

[Queue](../experiment-queue.md) · [Inventory](../tool-research.md).
