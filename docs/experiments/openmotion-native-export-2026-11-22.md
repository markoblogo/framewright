# OpenMotion native export / The Backup Route

22 November 2026. One original silent 10-second editorial diagram at 960×540
and 30 fps. An amber signal stops at a broken link, retraces to the source and
reaches its destination via the green backup route. This was a local export
probe with no account, paid calls or publication.

The retained OpenMotion checkout at `fcbaa2b` (HyperFrames 0.9.7) created the
project, saved the new composition and queued native export against that saved
revision. A fresh isolated test workspace used already-installed Chrome and
local media tooling. The export reached `completed` in 154.4 seconds from
acceptance through verification, including renderer startup and final checks.
No external recipe or fallback renderer produced the MP4.

The native job receipt passed H.264/MP4, dimensions, 30 fps, 10-second duration,
absence of an audio track, full decode of 300 frames, and first/middle/last
seeks. Four sampled output frames show legible labels and the source, blocked
route, bypass and delivery beats. The renderer logged two non-blocking
resource notices and forced browser shutdown on close. The final output
passed verification after those diagnostics. The optional standalone
verification tool was unavailable on this MCP surface; the job's own retained
verification provided the checks.

On 23 November the owner confirmed that the rerouting sequence was clear
in the silent clip.

This closes native export feasibility for a single small landscape scene.
Repeatability, portrait export, audio, larger compositions and active
authoring time were not measured. Keep the existing scoped motion workflow
and its production ranking. The test does not supersede the two incomplete
landscape runs in the [earlier trial](openmotion-reuse-2026-11-17.md).

Private scene, revision, job receipt, renderer log and encoded output are under
`productions/openmotion-native-export-2026-11-22/`.
