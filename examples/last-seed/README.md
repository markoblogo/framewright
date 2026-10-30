# The Last Seed — original pilot

R03 production pilot, authorised for 6–8 seconds only. The selected construction
is 180 frames at 24 fps: seed → drop → first sprout. It is stylised animation,
not a botanical simulation or footage of real germination. No full film or public
upload is authorised by these scripts. [Experiment and status](../../docs/experiments/last-seed-pilot.md).

## Source and replay

Keep generated files in a new private directory outside Git. Use an existing
Blender 4.5 installation, Python 3, FFmpeg and ffprobe. Run heavy jobs sequentially.
The scene has original geometry/materials, baked transforms and no external models,
textures, caches, Geometry Nodes or physics simulations. The audio is original
local synthesis with explicit event times; Tone.js has not been tested here.

1. Invoke Blender in background/factory-startup/disable-autoexec mode with
   `--python create_scene.py -- NEW_DIRECTORY`. Use absolute script paths. This
   saves the scene, motion checkpoints and a **Cycles** shot specification.
2. Run `python3 prepare.py NEW_DIRECTORY --blender ABSOLUTE_BLENDER_BINARY` once.
   It creates the journal, free-only brief/proposal, retained sources and a pending
   owner-review task. It prepares work; it does not start rendering.
3. The initial scene exercised the existing Cycles executor with
   `python3 render_range.py NEW_DIRECTORY --name board --start 170 --end 171 --execute`.
   Its public range is zero-based/end-exclusive; the rendered Blender frame is 171.
   The later owner contact correction adds shape-key/material animation and is
   exercised only through the manual fallback; do not infer its executor support.
   Limits and the selected route still apply. This pilot found Cycles too slow
   for its full preview on the available Mac.
4. The **manual Eevee fallback** loads the saved scene in Blender and invokes
   `render_eevee.py -- NEW_OUTPUT_DIRECTORY FRAME_LIST`, with Blender frame numbers
   1–180, comma-separated. For control stills use `25,68,171`; for the full pilot,
   explicitly supply all 180 frames in order. It writes 1280×720 PNGs and a report.
   This is not an admitted executor action. Do not represent it as supported by
   R01, change the existing Cycles contract, or run it alongside another heavy job.
5. `python3 finish_pilot.py PRIVATE_DIRECTORY --frames RENDER_DIRECTORY_NAME`
   checks every frame hash, assembles the MP4 with the original WAV, measures format
   and duration, and fully decodes it. Viewing/listening and owner acceptance stay
   pending. Scripts refuse to overwrite an existing scene, project or final output.

Retain revised scene/script copies under new identities before resuming. The
recorded run preserves v1/v2 failures and the v3 correction; a fresh replay of the
current builder starts with the corrected design and will not recreate those
historical faults. No absolute workstation paths or generated media belong in Git.

## What this pilot can establish

- Whether the action reads clearly and looks worth developing into a film.
- Baked growth and event-timed sound in an original, editable scene.
- Actual rendering cost and the boundary between admitted and manual work.

It does not establish scientific growth, fluid physics, artistic continuity across
a full film, three-option PREVIS-01, Tone.js, DJV review or release readiness.

## Full-film storyboard (proposed)

[Eight-shot plan](../../docs/experiments/last-seed-storyboard.md) and
`storyboard-v1.json` describe60s/1440frames. `production-v1.json` is an existing
project composition: one retained pilot source, seven unproduced picture materials
and empty final-delivery slots. Its `output:pilot-v5` reference requires the existing
private pilot project; it is not a standalone runnable render specification.

## Wide set and light tests

[Staging experiment](../../docs/experiments/last-seed-staging-tests.md) uses
`stage_tests.py` in Blender with a pinned pilot-v5 scene and a new output directory.
Modes `wide` and `dawn` produce72frames/3s at720p24fps; `--controls` limits rendering
to frames1,36,72. These are explicit manual Eevee tests, intentionally silent,
with separate retained scenes/reports and pending owner review.

## Full-film rough edit

[Draft experiment](../../docs/experiments/last-seed-rough-cut.md) uses
`film_shots.py`: Blender invocation `--python SCRIPT -- RETAINED_WIDE_SCENE NEW_DIR`
renders seven new shots at960×540/12fps/8samples; `--controls` limits each to three
frames. It loads a fresh copy of the same source for each shot and refuses output
overwrite. `assemble_draft.py PRIVATE_DIR --frames RENDER_NAME --name NEW_DRAFT_NAME`
uses existing FFmpeg and Pillow, creates original sound/title overlays, copies the
accepted pilot and checks the60s draft. The example requires the existing private
pilot sources; it is not a standalone media bundle or admitted worker. No install,
provider or publication is performed.

## Grain/hardware/pace revision

`seed_design.py` creates the original pointed textured hull and curved irrigation
with a valve. `film_shots.py` now uses the40s edit and supports `--only S03` for
an isolated shot correction. `assemble_draft.py` uses the revised7.5s pilot file
`pilot-grain-v1.mp4` in the private project, large contrast-backed captions and
optional `--patch PATCH_DIRECTORY` for retained corrected-shot sources. Historical
60s scripts/output versions remain private; current source is the revised40s
workflow. Neither rendering nor a numeric pass transfers creative acceptance.
