# Internal saved-shot replay probe

Original local fixture: amber sphere with a saved three-second action, simple arch,
two camera setups, two area lights and a quiet original two-tone WAV. No downloaded
models, generative provider or production footage. Only scripts belong in Git.
[Method and results](../../docs/experiments/blender-shot-replay.md) ·
[Shot/passport contract](../../skills/video-production-router/references/shots-and-passports.md).

Prerequisites: Python3.11+, FFmpeg/ffprobe and an explicitly selected trusted
Blender4.5-compatible executable. Actual test: Blender4.5.15 LTS, macOS ARM64,
Cycles CPU,480×270,12fps,8samples,seed7. Normal graphics-system access was required;
restricted-process startup crashed before scene loading. No global install is needed.

From the repository root, choose a new private folder with an existing parent:

```sh
python3 examples/blender-stage/run_probe.py --output /tmp/new-blender-probe --blender /trusted/Blender
python3 examples/blender-stage/run_probe.py --output /tmp/new-blender-probe --blender /trusted/Blender --execute
```

The first command only describes the test. The second builds/saves the original
scene and WAV, retains a schema-2 project and renders five attempts: full shot twice,
matching subrange, one energy patch and another camera setup. Each loads the saved
scene in a fresh Blender process. Use `--resume` only to inspect/continue this exact
fixture after interruption; existing reports/dependencies are rechecked. Partial or
failed attempts are not silently overwritten. A completed receipt is preserved;
use a new folder for another full run.

Checks compare source RGB frames, actual scene state, source hashes and sample-aligned
PCM, then inspect encoded shape/streams/full decode. `probe-receipt-v2.json` records
measured runtimes and exact scope. This is a tiny technical test, not a beauty render,
benchmark of arbitrary scenes or proof of natural character animation. PNGs/logs stay
private and are not individually registered. Creative/listening acceptance and actual
production passports remain separate; no automatic catalogue promotion/publication.
