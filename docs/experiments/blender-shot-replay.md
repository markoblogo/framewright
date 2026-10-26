# Reproducible Blender shot and continuity preparation

26 October2026. Owner authorised an internal Blender test and future-production
passport preparation. No public upload, production film, commit/push or release.
[Sanitised receipt](../../experiments/2026-10-26/evidence/blender-shot-replay.json) ·
[Fixture source](../../examples/blender-stage/README.md) ·
[Commands and boundaries](../../skills/video-production-router/references/shots-and-passports.md).

## Actual run

Downloaded the official Blender4.5.15 LTS ARM64 distribution, verified its published
SHA256 and retained a portable app outside Git. Build5afeabba6097. Existing FFmpeg
and Python were reused; no add-on, model, external creative asset or paid service.
Original geometry/materials, saved action and quiet two-tone audio form a3s fixture.
Renders use Cycles CPU,480×270,12fps,8samples and seed7 on this Mac only.

| Check | Observed result |
| --- | --- |
| Reload saved scene, render twice |36/36 source RGB frames equal |
| Independently render absolute frames12–23 |12/12 equal to corresponding full-shot frames |
| Change Key energy700→1400, rerender only that range |12/12 frames change; camera/action state preserved |
| Switch camera setup, reuse saved scene/action |Second view differs; source scene remains unchanged |
| PCM repeat, subrange clock, light/camera edits |Byte-equal repeated PCM; subrange matches exact source sample window; image edits preserve PCM |
| MP4 decode, frame count, dimensions, audio stream policy |Pass for all five attempts |
| Source scene, WAV and original shot card |Unchanged hashes |

Measured wall times: first full56.97s, repeated full40.74s, subrange14.71s,
light edit14.63s, alternate view15.72s. These tiny-fixture observations are not a
speed guarantee or measured production saving. Provider charges0; electricity,
machine time and operator labour were not costed.

The first restricted-process launch crashed in Metal backend initialization before
Python/scene loading. Retained the failure; the same verified executable succeeded
with normal native graphics-system access. CPU rendering still requires Blender's
native startup environment. This is not a claim that every Mac/process runner works.

Sampled actual decoded source images from base, light edit and alternate view show
the intended sphere/arch and visual changes. Low samples/resolution are deliberately
grainy; no cinematic quality, full playback/listening approval or natural rig motion
is established. RGB equality concerns source PNG pixels, not lossy MP4 pixel identity.

## Existing workbench integration

An actual source-pinned A/B card compares the base and changed-light subranges, with
render/probe evidence, declared prerequisites and measured processing time. Both MP4s
were copied into a local comparison pack. Status is `ready_for_owner_review`, with
no fabricated owner acceptance and no automatic provider admission. Environment
readiness is scoped to this original fixture, not general asset-rights clearance.
All media, app files and editable scenes remain private outside Git.

## Passport preparation

`passports.py` retains immutable character/environment versions and source references
in the existing project journal. `shots.py` pins exact bindings, blocks unresolved or
unapproved definitions and lists affected shots. New versions do not inherit approval
or silently rebind earlier shots. [Draft forms](../../examples/passports/README.md)
cover scale, appearance, materials, rig/actions, layout and constraints. Synthetic
tests exercise reference drift and version boundaries; no actual Good Dog character
or setting has been selected or approved. Automatic image identity checks are absent.

This is an internal technical fixture, **not another counted final video export**.
Next useful validation is one real approved recurring asset/shot with adjacent-second
review. Arbitrary rigs, simulation, facial motion, GPU/cross-build equality and complex
external dependencies remain untested. Jake Denham's unavailable reference project
stays watch-only; its code, .max support and claimed speedup were not tested/copied.

## Offline verification and final preparation

Full local suite:359 tests, zero failures, one skip. After the final fractional-source-
offset clock correction, all seven focused shot tests passed, including exact integer
sample deltas at half-sample offsets. Passport tests cover environment anchors, latest
pending/rejected review, source drift and immutable versions. Dotted Blender object
names (.001) are supported by one-control edits.

After refreshing only the unqualified current-source inventory,25 qualification and
18 evidence regressions passed. Router/storyboard historical evidence integrity,
documentation/links, generated reference and standalone helper/package smoke passed.
Historical model results stay unchanged; current source is `not_evaluated_current_source`.
No model call or release was performed.

Both draft passports were also retained in the actual private fixture project and
reported `incomplete`, as intended. They supply no production canon or approval.
