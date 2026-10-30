# The Last Seed — R03 pilot

28 October 2026. Owner selected **The Last Seed** and authorised a 6–8-second
pilot: seed, drop, first sprout. Full production and publication remain separate.
[Replayable original source](../../examples/last-seed/README.md).

## Brief and production decision

7.5 seconds, horizontal 16:9, 24 fps; original greenhouse macro with a locked
camera, dry soil, warm seed, cooler background and green growth. The seed arrives,
a drop lands beside it, the soil darkens, and two leaves unfold. Growth is a
stylised compression of time. There is no narration; original quiet synthesis and
timed seed/water cues support the action. No provider calls, subscriptions or new
installations are needed; zero provider charges excludes labour and hardware.

The private project retains its free-only profile, R02 proposal, route comparison,
environment requirements, sources, shot versions, execution receipts and explicit
owner-review wait. The approval recorded at intake is **permission to make the
pilot**, not approval of its unseen picture or sound.

## What happened

| Trial | Observation | Consequence |
| --- | --- | --- |
| Restricted Blender launch | Metal initialisation crashed before the scene script ran | Scoped local retry outside that restriction succeeded; not a scene success on the first attempt |
| First admitted Cycles control | A rim mesh and area light shared a name; worker rejected the wrong object type | Preserve failure/source; rename light to `BackLight`, retain scene v2 |
| Second admitted Cycles control | Frame 171 rendered; worker technical checks passed; adapter took 30.96s, frame rendering 26.76s | Genuine bounded executor evidence, but expensive for a full 180-frame preview |
| Visual inspection of the control | Segmented stem looked striped; pale leaves, tight framing and grain | Scene v3 uses a continuous curve stem, revised framing/material/light; previous sources remain retained |
| Eevee control stills | Corrected stem and framing are visible; final control frame rendered in about 2.42s | Select manual Eevee for the pilot preview; this is a route gap, not a passed R01 Eevee adapter |

The full Eevee render is deliberately separate from the Cycles admission contract.
It keeps a report of source hash, frame hashes, camera/object positions and elapsed
time. A manual fallback must not silently inherit another engine's qualification.
The next executor improvement, if justified by this production, is a bounded Eevee
adapter with the same timeout, recovery, source and output controls.

## Checks and acceptance

The pilot preparation preserves 180 baked motion samples and explicit sound cues:
seed contact near 0.97s; nozzle cue 1.2s; water impact 2.833s; growth harmonic 3.5s.
These authored timings do not prove perceptual synchronisation.
[Measured evidence](../../experiments/2026-10-28/evidence/last-seed-pilot.json):
the 180-frame Eevee render completed in **387.36s**; assembly and technical checks
took **3.13s**. The MP4 passed 1280×720, 24 fps, 7.5s, 48kHz stereo, frame-count,
retained-frame-hash and full-decode checks. Encoded audio sample peak is −14.0 dBFS,
mean −37.3 dBFS; this is intentionally quiet but listening remains necessary.

Frames 25, 68 and 171 were rendered both as sparse controls in a fresh Blender
process and within the full sequential run. Their **decoded RGB pixels matched
exactly** (FFmpeg PSNR infinite), while PNG file hashes differed. This is a bounded
three-frame reproducibility result, not proof of every frame or all Eevee scenes.
Human viewing/listening and pilot acceptance remain pending. The local review
page and an identical downloadable MP4 were prepared; nothing was uploaded.

The private checkpoint preserves the original failed control as blocked/superseded,
marks the successful v2 technical control done, and binds separate pending creative
and listening tasks to pilot v3. It must not automatically retry the historical
failure. The script sources parse; repository documentation/link validation and
whitespace checks passed. These are not model evaluations or full-suite claims.

There are no accepted character/environment passports yet. The original scene is
a retained working design, not a proven continuity contract across multiple shots.
Tone.js, three-option PREVIS-01 and DJV are not promoted by this pilot. No new tool
is labelled production-qualified on the basis of its name or a successful still.

## Next decision and release boundary

### Owner revision: contact with soil and water

The owner liked the shell opening, sprout and sound, and requested two corrections
within the **same 7.5 seconds**: settle the seed into a dent with a brief soil/dust
reaction; land water on the seed and show it running into the soil. Preserve the
existing opening and growth timing. Feedback is retained against pilot v3; it is
not final acceptance of the next revision.

The revised source adds baked seed settling, a shape-key soil depression with a
displaced rim, small ballistic soil grains, surface runoff beads and an animated
wet-shell reflection. The wet patch/ripple follow runoff later; the original
water-contact audio cue remains at 2.833s and the accepted soundtrack is reused.
This is authored contact staging, not validated fluid/soil physics. An initial
local patch was superseded by a full soil surface so the original flat mesh could
not fill the depression. Revisions and control frames remain private and retained.

The manual Eevee path continues to apply; the shape-key/material animation is
not claimed as qualified by the bounded Cycles executor.

Owner explicitly accepted corrected pilot v5 on 28 October 2026 after viewing
review-v2 ("ок принимается"). The creative receipt and contact-review task are
accepted/done in the private journal. The pilot retains 180 frames/7.5s/720p24fps;
full decode passed and decoded audio matches v3 exactly. Five authored growth
checkpoints match the original. Manual Eevee rendering took374.92s.

Use this accepted pilot as the visual reference for the full-film storyboard.
Approval covers this delivered pilot; the full film remains a subsequent stage.
R03 still needs complete production, one scoped correction, a fresh-session
continuation and an accepted local delivery/publication kit. **REL-A is not reached**
by this pilot. No release, public upload or Git publication is part of this task.

## Full-film planning follow-up

The owner authorised storyboard preparation after accepting the pilot.
[Proposed60-second storyboard](last-seed-storyboard.md) uses8shots and reuses
the accepted pilot at18–25.5s. A native production composition is retained in
the same private journal; seven new picture sources/final delivery remain missing.
Schematics are planning diagrams, not rendered staging tests or owner acceptance.
