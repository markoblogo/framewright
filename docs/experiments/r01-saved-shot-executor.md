# R01 — saved Blender shot through the sequential executor

28 October2026. Internal original-fixture test; no film, upload, paid call or release.
[Roadmap R01/M2](../roadmap.md) · [machine-readable evidence](../../experiments/2026-10-28/evidence/r01-saved-shot-executor.json)
· [reproduction](../../examples/blender-stage/run_executor_probe.py)
· [binding contract](../../skills/video-production-router/references/route-admission.md#saved-blender-shot-r01).

## What changed

The existing `shots.py` renderer now runs as `saved-blender-shot` inside the same
sequential executor used for inspections and review clips. A prepared Blender
picture stage is selected from an intake comparison. The frozen selection includes
its shot/resource/audio/passport pins, exact frame bounds, runtime executable
paths/hashes, environment and output limits. Unbound saved-shot dispatch is rejected.

The parent retains its project lock; the worker inherits the host exclusion lock
and independent process-group deadline. The worker never saves the project.
Parent-side output checks register the checked preview and associated shot receipt,
job/state and PCM under fresh identities. Viewing/listening/creative approval stays
pending; a generated file does not mark its task complete or permit publication.

## Observed real Blender result

Portable Blender4.5.15LTS, macOS Apple Silicon, Cycles CPU, two threads. Original
amber sphere/arch with named action, camera, two area lights and original tone.
480×270,12fps,8samples,seed7. Four sequential calls,18frames total:

| Run | Absolute public frames, end exclusive | Result | Renderer elapsed |
| --- | --- | --- | --- |
| Baseline |12–18|6decoded frames, correct format/audio, review pending|9.03s|
| Repeat |12–18|6/6RGB hashes and PCM match baseline|8.43s|
| Subrange |14–17|3/3RGB hashes and sample-aligned PCM match baseline segment|4.14s|
| Light edit |14–17|Key700→1400 changes3/3images; camera/action/PCM preserved|4.94s|

These durations are renderer measurements, excluding setup/admission, and are not
production forecasts. Inspected one rendered frame: original sphere and arch were
visible. This is technical proof of a bounded same-build adapter, not cinematic
quality, a human listening approval, character continuity or general hardware fit.
The first probe attempt stopped during fixture preparation because its launcher
expected JSON from a text-returning command; fixed the launcher and used a new
folder. The failed preparation was preserved; it did not dispatch a render.

## Failure and boundary controls

Automated public-CLI tests use a synthetic Blender stand-in, actual FFmpeg outputs
and the real worker/locks. They cover selection required, integer-frame bounds,
missing/repinned scenes, executable replacement, successful receipt retention,
intentional silence, wrong output dimensions, small bundle allowance, timeout,
SIGTERM cleanup and no implicit retry. Existing executor tests additionally cover
host exclusion after abrupt parent SIGKILL and its independent deadline. These are
process-control tests, not evidence that every native Blender failure is recovered.

A render's entire output folder is checked against the byte allowance, with a
sampling monitor during execution. It is not a filesystem quota or hard RAM limit;
one write may overshoot. Resource snapshots do not prove arbitrary scene fitness.
Use only trusted scenes/executables and explicitly retained dependencies. There is
no new scene generator, dependency installer, external dispatcher or complete-film
orchestrator. Existing saved-shot simulation/driver limitations still apply.

## Verification closeout

The broad native-environment run exercised481tests with1optional skip. It found two
fixture issues: the retained route comparison lacked the new Blender proposal, and
an in-process admission test mixed macOS `/var` and `/private/var` paths. Updated the
comparison and resolved the test root consistently; no integrity check was relaxed.
Repeated all13admission tests,10route-comparison tests and9saved-shot tests: all pass.
The remaining broad-run tests had already passed. No second full run was needed
for these fixture-only corrections.

Router/storyboard historical-packet integrity, local link/schema validation, generated
tool-reference check, standalone package smoke and `git diff --check` passed.
Historical model results remain historical; current source is **not model-evaluated**.
The package smoke used a temporary directory and removed its output; no release,
tag, remote push, publication or new model/provider calls were made.

## Next and release boundary

R01's internal acceptance scope is complete. R02 (one readable producer brief) is
next; R03 must still demonstrate an integrated film and fresh-session recovery.
REL-A requires the combined M1/M2 evidence, so this test alone does not trigger a
release. Announce a reached release gate and wait for the owner's decision.
