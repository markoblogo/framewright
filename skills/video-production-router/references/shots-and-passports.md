# Saved shots and continuity passports

Use the existing schema-2 project and journal. `shots.py` is an optional, bounded
local Blender executor; it does not make the router a general rendering service.
`passports.py` prepares versioned artistic definitions for later production.
[Internal Blender evidence](../../../docs/experiments/blender-shot-replay.md) ·
[Runnable fixture](../../../examples/blender-stage/README.md) ·
[Draft passports](../../../examples/passports/README.md).

## One retained shot, one controlled edit

Retain the trusted `.blend`, any external resources and optional audio as ordinary
project inputs. A shot specification contains `id`, `version`, `scene` subject,
`resources` subjects, `canvas` (width/height/fps), `frames` (start/end), `engine`,
`settings`, `audio` and `bindings`. The fixture builder supplies a complete example.

Settings contain a named camera and its local position/Euler rotation/lens, named
existing object/actions and named area lights with energy/color/location/size.
Geometry, materials, world, light orientation, camera constraints and color management
come from the pinned scene. This version supports Cycles CPU only, fixed samples/seed,
two threads and no denoising. It is not an arbitrary Python-command manifest.

```sh
python3 skills/video-production-router/scripts/shots.py prepare local/project.json local/shot-spec.json --output local/shot-v1.json --actor operator
python3 skills/video-production-router/scripts/shots.py render local/project.json output:shot:stage:v1 --attempt preview --start 12 --end 24 --output local/preview
python3 skills/video-production-router/scripts/shots.py render local/project.json output:shot:stage:v1 --attempt preview --start 12 --end 24 --output local/preview --execute --blender /trusted/Blender
python3 skills/video-production-router/scripts/shots.py patch local/project.json output:shot:stage:v1 --parameter settings.lights.Key.energy --value 1400 --version v2 --output local/shot-v2.json --actor operator
python3 skills/video-production-router/scripts/shots.py render local/project.json output:shot:stage:v2 --attempt correction --start 12 --end 24 --output local/correction --execute --blender /trusted/Blender
```

The first render command is a dry run: no renderer/output directory/project update.
Execution requires an explicit trusted executable and `--execute`; use a fresh folder
and attempt ID. A patch can change only one declared camera/action/light/audio
control. It retains the parent and before/after values; the original is preserved.
The manifest and fixed worker hash are pinned. Source drift or a changed worker
requires review and a new shot version. This is not a privilege/security sandbox;
use trusted scene/resources and executable, with normal OS resource permissions.

Public frame intervals are **zero-based, end-exclusive**; Blender frame = public
frame + 1. Supported fps: 12,24,25,30,50,60. Each call is capped at240 frames and
300 million pixels; it is a short-preview/range adapter, not a whole-film scheduler.
Rendering a subrange restores the same absolute action frames, not a restarted action.

Sound comes only from `audio: {subject, gain_db, offset_seconds}`, or `null` for
intentional silence. `offset_seconds` selects the source window; it is not a delayed
start cue. The source is resampled to48kHz stereo PCM16, cut at absolute sample
positions and padded to the exact range length before AAC encoding. Embedded scene
sound is not mixed. PCM hashes/clock checks do not prove listening quality.

Outputs retain MP4, job/state JSON, PCM WAV when present and a render receipt in
the project. Receipts include source-frame RGB MD5 values, measured elapsed time,
Blender version, state, decode/frame-count/dimension/audio-policy checks and pins.
PNG intermediates and logs stay in the attempt folder; PNGs are not individually
registered artifacts. Recheck their bytes before later reuse. Failed attempts retain
logs and `FAILED.txt`; there is no overwrite or automatic cleanup.

Compare baseline/candidate through [trials.py](trials-and-readiness.md), using the
same range, sources and declared criteria. For an editorial correction, retain the
[revision request](revisions.md) and review neighboring seconds as well; render a
larger range when context is needed. Comparison evidence and owner acceptance remain
separate. Never mark a tool production-qualified from a successful command alone.

## Explicit support boundary

The tested fixture is a simple saved action, two camera setups, area lights and
procedural materials, same Blender build/machine. Arbitrary rigs, facial motion,
parented/constrained cameras, NLA blending, cross-platform pixel equality and GPU
determinism have not been qualified. Physics, particles and geometry-node modifiers
are rejected until a separate baked-state adapter exists. External image/sound/font/
library/movie resources must be packed or explicitly retained. Unknown dependencies,
add-ons, drivers, simulation caches and complex production scenes need their own audit;
`--disable-autoexec` alone is not proof of a safe or fully deterministic file.

## Versioned character and environment definitions

Passports are ordinary `entity-passport` artifacts. Each version freezes references,
dimensions in metres, material descriptions/source subjects and continuity constraints.
Characters add proportions, clothing (explicitly say none if applicable), palette,
required/optional rig and named action source subjects. Environments add layout,
lighting intent and spatial anchors. Null/empty draft fields stay unresolved.

```sh
python3 skills/video-production-router/scripts/passports.py create local/project.json local/hero-spec.json --output local/hero-v1.json --actor operator
python3 skills/video-production-router/scripts/passports.py status local/project.json output:passport:hero:v1 --json
python3 skills/video-production-router/scripts/passports.py uses local/project.json output:passport:hero:v1 --json
```

Only after actual owner review, record a `creative` / `accepted` observation with
`owner_report` provenance and topic `passport-review` through `project.py observe`.
Incomplete definitions remain incomplete even if an observation says accepted.
Changing a pinned reference stales the passport. A new version may `--supersedes`
the previous subject, but does not inherit its approval or rewrite existing shots.

Each applicable shot explicitly binds an exact version, for example:
`bindings: [{"passport":"output:passport:hero:v1","object":"Actor"}]`.
An environment can use `object:null` for a whole-scene binding. Execution is blocked
when any declared passport is incomplete, unapproved, rejected or stale. Bindings
are optional for an abstract technical fixture, not a way to claim character continuity.
Select bindings for every recurring character/environment in a real production.

This checks documents, retained versions and manual decisions. It does **not** verify
rendered identity, proportions, costume, rig deformation or rights automatically.
Rights/source admission remain independent. Prepare the Good Dog hero and sets with
the owner during real production; the supplied drafts define no approved canon.
