# Arsenal gaps and bounded additions — 26 October 2026

Owner requested a review of retained/tested tools and queued candidates, web research,
and retention of useful additions. **Research and queue work only:** no installations,
model downloads, scene builds, accounts, uploads, speech generation or renders.
No release, commit or push requested by this task.

## What the current arsenal covers

The registry and review ledger were inspected alongside the existing queue and
retained micro-lesson, forest-compositing and rigged-dog cases. Status is scoped:
supported features, used components, owner preference and runtime candidates are
different forms of evidence; none certifies a whole product or arbitrary pipeline.

- Assembly, typography, timelines, encoded delivery and selected 3D camera/action
  workflows have retained evidence: FFmpeg, HyperFrames, Remotion, Three.js and
  scoped capture methods. Do not add another generic renderer without a gap.
- Local speech, transcription/OCR, selected music/sound workflows and manually
  admitted Openverse SFX have retained scoped evidence. Recognition does not prove
  listening quality or pronunciation; procedural mixing does not qualify a DAW.
- Existing world plates, source-preserving photo staging and a dog rig have actual
  productions. Arbitrary tracked-camera integration, retargeting and long character
  continuity are not established by those films.
- The micro-lesson's photographic mouths were accepted with jerky/artificial
  facial motion. This is a known follow-up, not a natural-avatar success.
- Worlds, voice cloning, rigging, keying, ASCII, charts and design already have
  queued alternatives. New world generators or voice providers are lower-value
  additions than closing the following handoff/control gaps.

[Micro-lesson limitation](../experiments/framewright-micro-lesson.md#owner-acceptance-and-next-facial-animation-trial)
· [Forest composition](../experiments/marble-compositing.md)
· [Rigged-dog production](../experiments/little-light.md).

## Priority and first trial

Priorities below rank this batch; existing owner production order, Pocket OS pause,
resource/rights gates and current tests stay unchanged. Choose a concrete production
subject before execution. Candidates remain discoverable only as untested records.

| Order | Candidate / missing step | Bounded trial and evidence |
| --- | --- | --- |
| P1 | Rhubarb Lip Sync: editable speech-to-mouth cues | 8–12s cleared English speech + authored stylised mouth shapes; raw cues versus smoothed transitions, separate eyes/head; check consonants, rests, chatter and sync |
| P1, after queued Blender stage | Blender tracking + Cycles shadow catcher: camera/ground integration | 5–8s real textured moving-camera plate; insert one simple object, solve camera, match floor/scale and contact shadow; inspect start/middle/end and full playback |
| P1, humanoid prerequisite | Rokoko Blender retargeter: reuse motion across rigs | 5–8s cleared existing humanoid animation → different cleared humanoid rig → baked action → two views → save/reopen/export; inspect contact, root travel, joints and cleanup effort |
| P2, launch-route gate | SAM 2: video masks without green screen | 5–8s cleared clip with motion and brief occlusion → prompted mask propagation → corrected masks → three backgrounds; inspect ID drift, edges, flicker and correction time |
| P2, with next composite | OpenColorIO / Blender color handoff: consistent layers | sRGB plate + linear CG + neutral/color patch; pin input/working/view/output transforms → composite → SDR encode → second-player check; detect double transforms/range errors |
| P2, evaluation/need gate | REAPER + ReaScript: editable sound production | 15–20s, one voice, one ambience, three existing cleared effects; create cue markers/ducking/fades/stems → revise one cue → reopen/render; compare existing FFmpeg method |

## Rhubarb Lip Sync

[Official repository](https://github.com/DanielSWolf/rhubarb-lip-sync)
documents Windows/macOS/Linux CLI, WAV/Ogg input, script hints and timestamped
mouth-shape export including JSON. [Licence](https://github.com/DanielSWolf/rhubarb-lip-sync/blob/master/LICENSE.md)
is MIT with separately listed dependencies; source speech/art rights remain separate.
Confirm exact release/architecture and dependencies on our Apple Silicon Mac.

This targets stylised/editable lip sync, not photoreal facial synthesis. Mouth cues
alone do not animate eyes, brows or head and cannot certify realistic photographic
presenters. Compare the retained timing-only baseline on an original stylised face;
keep smoothing authored and inspect closures, silences and delay against audio.
Record the cue mapping and changes; good timing does not imply natural expression.

## Blender tracking and contact integration

[Tracking documentation](https://docs.blender.org/manual/id/dev/movie_clip/tracking/introduction.html)
covers camera/object solving, planar tracking, scene orientation and tracked masks.
[Cycles features](https://www.blender.org/features/rendering/) include shadow catchers,
holdouts and render passes. These are new scopes of the existing Blender candidate,
not another renderer or a claim about the installed version.

Start with real footage of static textured geometry, visible parallax and a simple
floor. Retain lens assumptions, tracks, solve diagnostics, scale, plate and camera.
Check visual stability, foot/object contact and occlusion, not only a small solve
error. Poor solve/manual repair is a valid result. Do not infer reliable camera
reconstruction from drifting generated video; native world cameras are preferable
when available. Pin actual Blender/Cycles version and independent source rights.

## Rokoko Blender retargeting

[Official plugin](https://github.com/Rokoko/rokoko-studio-live-blender) documents
source/target armatures, bone mapping, pose alignment, scale and retargeting.
Scope the first trial to existing local humanoid actions; Studio streaming, capture,
cloud services and paid plan entitlements are independent and not required assumptions.
[Installation guide](https://support.rokoko.com/hc/en-us/articles/4410463492241-How-to-install-the-Blender-plugin)
and [plans](https://www.rokoko.com/pricing) require separate checks for the chosen route.

Important source conflict: README's MIT badge conflicts with the actual
[LICENSE.md](https://github.com/Rokoko/rokoko-studio-live-blender/blob/master/LICENSE.md),
which contains LGPLv3. Do not treat the badge as a permissive grant. Pin source and
review applicable terms before installation/distribution; do not copy plugin code
into Framewright. Rig, animation and service rights remain independent.

Check plugin/current Blender compatibility and whether the selected local-retarget
path needs login before proceeding. Retain mapping, reference poses and root options.
Use the later Tripo humanoid export if qualified, or independently cleared rigs.
Do not count retargeting as animation generation, foot-lock correction or dog gait
support. A humanoid pass does not qualify quadrupeds or facial motion.

## SAM 2 video masks

[Meta repository](https://github.com/facebookresearch/sam2) documents prompted
image/video segmentation; [installation](https://github.com/facebookresearch/sam2/blob/main/INSTALL.md)
primarily specifies Linux/PyTorch/CUDA. Skipping the optional CUDA postprocessor
does not establish fast/correct Mac inference. Apple Silicon video runtime, model
size/memory and processing speed remain unresolved before any weight download.
Model checkpoints/code are Apache-2.0; demo fonts and third-party components have
separate terms. No model or demo installed/accessed in this review.

Segmentation masks are not automatically production alpha mattes for fur, hair,
transparent material or motion blur. Distinguish binary/soft mask values from true
opacity; record occlusion/identity failures and manual fixes. Compare ordinary
manual masks on a few retained reference frames and inspect all frames on light,
dark and intended backgrounds. Native-alpha renders need no segmentation pass.
Do not silently substitute a hosted paid service if a local route is blocked.

## OpenColorIO and scene-to-encode color

[OpenColorIO](https://github.com/AcademySoftwareFoundation/OpenColorIO) is a
BSD-3-Clause color framework with ACES support, not automatic artistic grading.
[Blender 5.0 documentation](https://developer.blender.org/docs/release_notes/5.0/color_management/)
describes working spaces and ACES view options; actual installed-version support
must be checked. Configuration files/LUTs and other applications retain their terms.

First pin a simple SDR delivery path with explicit inputs, no automatic migration
to HDR/ACES. Keep AgX/ACES choices intentional; prevent a display transform baked
twice into a plate/CG composite. Check neutral patches, highlight clipping, alpha
edges and encoded range/transfer tags; retain config/version and view settings.
Cross-player comparison is not monitor calibration or identical display proof.
Color management does not itself match direction of light, shadows or art style.

## REAPER and ReaScript

[ReaScript](https://www.reaper.fm/sdk/reascript/reascript.php) supports API/action
automation, including embedded Lua/EEL. [Download](https://www.reaper.fm/download.php)
lists Universal Intel/ARM64 macOS and a fully functional 60-day evaluation.
[Purchase terms](https://www.reaper.fm/purchase.php) distinguish discounted and
commercial licences; no perpetual-free assumption or purchase is made. Existing
installation/licence/evaluation eligibility has not been inspected.

Use a local editable project with markers, separate stems and retained mix settings;
no new plugins or downloaded sound libraries needed for the first comparison.
After one timing/level revision, check speech intelligibility, cue sync, tails,
loudness/true peak and clipping plus owner listening. Compare revision effort with
our existing FFmpeg pipeline; adopt only if editable mixing adds concrete value.
Do not expand this into a second video editor or autonomous publishing workflow.

## Remaining needs and scope limits

Photoreal facial performance and stable quadruped locomotion remain open after these
additions; neither Rhubarb nor a humanoid retargeter solves them. Use the already
queued Tripo/dog and video-guided-rig follow-ups for separate evidence, not promotion
by association. Long-form character/world continuity and real video-review judgement
also need production tests; more provider names do not close those gaps.

Re-use existing project/material/rights/decision/receipt records for all trials.
Retain exact source/asset/tool versions, resource/time/cost, failed results and
manual effort; owner preference separate from technical QA. No entries added to
automatic executable tools.json; no upstream code/media/weights copied into Git.

### Inventory snapshot before additions

Review ledger: 93 records, including tools, methods and components; not a tested-tool count.

```json
{
  "candidate": 39,
  "component_used": 3,
  "deferred": 12,
  "owner_accepted_scoped_voice": 1,
  "partial": 3,
  "prototype": 1,
  "reference_only": 7,
  "retained_profile": 7,
  "rights_blocked": 3,
  "runtime_incomplete_resource_guard": 1,
  "supported_scoped": 13,
  "tested_scoped": 3
}
```

Feature registry: 17 profiles; it overlaps the ledger and must not be added to its
count. Raw dispositions preserve different evidence scopes, not a single confidence
score. This snapshot is dated; use current search for production selection.

[Queue](../experiment-queue.md) · [Inventory](../tool-research.md).
