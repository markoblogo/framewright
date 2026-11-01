# Reanimate — motion reconstruction and comparison candidate

Reviewed30October2026, documentation/source instructions only. Not installed or tested.

Primary sources: [repository/README](https://github.com/NiazMorshed2007/reanimate),
[workflow skill](https://github.com/NiazMorshed2007/reanimate/blob/main/skills/reanimate/SKILL.md).
Repository displays MIT. Model, reference-media and copied site assets have separate rights.

The toolkit captures a live site or supplied recording/GIF/Lottie, describes motion,
rebuilds it in the target code stack and compares reference/candidate frames.
It documents CSS/WAAPI tracking and optional Canvas/WebGL/WebGPU/Three.js traces,
virtual-clock capture, parameter curves, timing/easing and pixel comparisons.
These are author claims, not Framewright-verified capabilities. Matching pixels
is not evidence of narrative clarity, plausible anatomy or correct physical contact.

Documented prerequisites: Bun1.1+, macOS/Linux; Windows untested; first setup
fetches Chromium/static FFmpeg, about250MB. No toolkit API keys; agent/model use
can still incur the user's normal costs. Only Claude Code is reported tested;
Codex compatibility needs an actual trial. Login pages/YouTube/Loom need a supplied
recording; tracing does not grant rights to reuse extracted shaders/assets.

## REANIMATE-01 — active bounded candidate

Fit: R05/local motion QA and later R07/Good Dog browser-shot timing. Reuse existing
revision comparison/journal; do not replace the production executor or identity passports.
First trial: one original local3–5second scene with known camera/object keyframes;
record twice at the same viewport/fps/trigger, reconstruct one motion, then introduce
an80–120ms timing defect. Verify whether tracking/comparison detects that defect,
repeat capture is stable, and the diff sheet is useful to a human. Keep CPU/RAM/time
and setup downloads recorded; run sequentially on this Mac.

For the current Good Dog pilot it could later evaluate camera/foreground timing,
but is not an image-to-video generator, quadruped rig, motion capture solver or
proof that a static illustration can become convincing walking animation.
No setup or benchmark launched during this assessment.
