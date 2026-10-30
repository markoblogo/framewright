# The Last Seed — rain recovery revision

30October2026. The owner explicitly resumed the selected story after the overnight
pause. This is a new local rough cut, not acceptance of the earlier rejected40s
film. [Checkpoint](last-seed-next-session.md), [history](last-seed-rough-cut.md).

## Story and causality

Dry cracked soil and exterior rain establish the mismatch: water exists outside
but cannot yet reach the plant. Retained cassette, reservoir, germination and
lamp-failure shots precede a roof drive that tries, jams, strains and finally
opens a vent. The final battery bar disappears only after the powered movement
finishes. The dead lamp slides away from the rain path. A control also exposed the empty
seed cassette above the leaves; it is moved aside in the water/recovery shots.
The earlier roof close-up is retained, so continuous cassette travel across the
join still needs a dedicated visual check before final production. Drops reach a leaf and
then soil; a visible damp patch grows. Morning light increases, the plant lifts
and develops a small new leaf pair. Camera rises along the plant and exits toward
the sky; title and picture fade into white. Old explanatory caption panels are
removed. Only the final title remains.

The48.5s working edit is: cracked ground2s; roof rain2s; cassette3s; reservoir3s;
retained germination7.5s; lamp fade4s; struggling roof7s; water5s; recovery7s;
upward ending8s. This duration is an editorial proposal, not an owner approval.
The earlier cassette/grain appearance remains retained; its final husk-colour
refinement is still open rather than claimed solved by new weather shots.

## Reusable implementation

- `examples/last-seed/recovery_design.py`: deterministic drought material, original
  roof vent/gear/battery rig, lamp retraction, authored rain/drop paths and growth.
- `examples/last-seed/recovery_shots.py`: loads a retained scene, freezes inherited
  animation, builds/bakes each named shot and saves sources plus frame hashes.
  `--controls` renders first/middle/last frames before full production.
- `examples/last-seed/assemble_recovery.py`: checks complete numbered sequences,
  retains source hashes, assembles the explicit edit and original event sound,
  checks output duration/frames/streams and full decode.

Use a new output directory for each revision. Heavy rendering is sequential,
with2 threads. Private immutable script copies accompany private scene/media
versions. No downloaded asset, paid generation or external music is introduced.
The new material is native960×540/12fps/8 Eevee samples; the review export is
720p24 through scaling/frame repetition. Retained germination is720p24. This is
an explicit manual Eevee example, not newly admitted executor support.

## Sound and limits

Original local synthesis provides restrained rain, room tone and harmonic bed.
Motor strain starts at21.5s, includes the jam, stops with the release click at
26.7s. Water impacts follow at29.37/30.62/31.87s; warmth grows during recovery.
The retained germination WAV is reused from10–17.5s with quiet rain mixed behind
it. No narration is added.

Cracks are procedural material/bump; rain, plant response and gears are authored
animation. This does not validate fluid dynamics, plant biology, refraction or a
mechanically simulated drive. Contact, framing, movement, sound quality and joins
require human review. Keep initial controls and any failed version for comparison. The first full
weather render was stopped after discovering the cassette obstruction; completed
valid ground/rain/roof shots are retained, while water/recovery/up shots come from
the corrected revision. This is scoped reuse, not acceptance of the stopped run.
R03 and REL-A remain open; no public upload or release is authorised here.

## Measured delivery

[Sanitized evidence](../../experiments/2026-10-28/evidence/last-seed-recovery-v3.json) records372 new selected frames,48.5s/1164 encoded frames,720p24,48kHz stereo and successful full decode. Source sequences were compared with retained frame hashes. PCM peak0.1953 leaves headroom; final sampled frame mean luminance249.98/255 supports the white-ending check. These checks do not establish perceptual smoothness or human listening/creative acceptance. The local review file, editable scenes, source copies, original sound and QA are retained privately.


## Owner corrections after v3 viewing

30October: the owner requested a visibly pitted/grooved almond/apricot-stone-like
seed surface; mechanical rather than electronic opening sounds; brighter and
more legible gears attached to a fixed support and connected to the window;
varied rain landing positions; and a more readable final title. The story and
48.5s working duration remain unchanged in the proposed correction.

The additional soundtrack request is explicit: loneliness/exhaustion early,
tentative hope at germination, oppressive suspense around the jam, then relief
and renewed hope. Original locally composed soft piano/bowed synthetic strings
are retained as a separate music stem from effects, with a section/event map.
This is authored synthesis, not a recorded orchestra or a model-generation test.

`surface_mechanics.py` adds shell material, a frame-supported backing plate,
bolts/axles, gear spokes and a crank/telescoping pushrod attached to the vent.
`polish_shots.py` patches retained scenes without resetting their action/camera
keys, provides first/middle/last controls, and saves new scene/frame hashes.
Three released drops have different timing, origins and destinations: right
leaf, left leaf and exposed soil. This is authored contact animation, not fluid
simulation or a validated real mechanical design.

Openverse returned a timeout for each of the two bounded searches. The fallback
used direct Freesound CC0 preview derivatives: [metal door creak by MathewHenry](https://freesound.org/people/MathewHenry/sounds/700705/)
and [creaky ratchet by cartoonrob](https://freesound.org/people/cartoonrob/sounds/588466/).
Private source HTML, downloaded-file hashes, licence links and credits are retained.
There was no Openverse result attribution field to copy; fallback credits are
explicit source/author records rather than invented verbatim Openverse text.
`score_recovery.py` mixes those recordings with retained pilot audio and original
music, keeping separate music/effects/mix PCM files. Human listening and creative
acceptance remain required after assembly. No new paid call or publication.


## Corrected v4 review delivery

[Correction evidence](../../experiments/2026-10-28/evidence/last-seed-polish-v4.json):
48.5s/1164 frames,720p24 encoded,48kHz stereo and full decode passed.588 selected
new frames cover the shell/mechanism/rain patches; a separate roof-only light
revision replaces the earlier roof pass. The germination action is rerendered at
native720p24; other new patches remain native540p12 roughs. No action/camera timing
approval is inherited merely because transforms were retained.

The final title is96px Georgia Bold, dark on a lightening sky, visible from45.1s
with the final0.6s fade included. A sampled encoded title frame was inspected.
Original score, effects and raw/master mixes are separate; rendered music/Foley
moods remain subject to owner listening. The encoded mix measured-19.30 LUFS and
-0.96dBTP, with no0dBFS clipping. This is a measured technical result, not a claim
of perceptual acceptance. Private review offers time-preserving v3/v4 switching.
The checkpoint retains a new technical receipt and separate creative/listening
review tasks. R03/REL-A, final quality/kit and publication remain open.


## Owner acceptance and publication kit

30October2026: owner replied “ок. принимается” to the displayed v4. Creative and
listening acceptance are recorded against that exact video revision. The local
final MP4 is a byte-identical copy, not a new unseen render. Its native mixed
resolution/frame-rate provenance stays explicit; no native-quality upgrade is
claimed. Prior rejected versions and their observations remain retained.

A local unarchived package contains the final MP4, an Imagegen cover based on the
retained plant frame with large “THE LAST SEED” lettering, English title,
description, tags and sound credits. The cover is a generated interpretation,
not an unchanged film still, and is proposed rather than separately owner-approved.
[Metadata example](../../examples/last-seed/youtube-package.md) is retained without
media or private paths. The cover/file hashes are kept in private delivery.json.
No YouTube upload, visibility or public URL is inferred from local delivery.

Fresh-session recovery and the unsupported manual Eevee/executor boundary remain
open for R03/REL-A. This acceptance does not automatically qualify a full route or
trigger a software release.

## Publication reported by owner

30October2026: owner supplied [The Last Seed on YouTube](https://youtu.be/ZQTORLBw9Zs). The URL is recorded against retained v4, following its explicit picture/sound acceptance and identical local delivery. This is owner-reported publication; the watch-page fetch returned a cache miss. Visibility, uploaded-byte identity, monetization and audience results remain unverified. Publication does not close the fresh-session/manual-executor gaps or trigger a release.
