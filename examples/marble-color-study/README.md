# Locked forest plate + independent actor — author-project example

Original authored scene, deterministic picture recorder and42s video-first sound script from [The Same Forest](../../docs/experiments/marble-compositing.md). The published film uses a retained Marble plate and a separate procedural Three.js character. This is an **asset-dependent 2.5D example**, not the clean-machine [reference film](../../docs/first-video.md), a provider connector or a world-mesh importer.

## Supply assets and runtimes first

No source assets, models, installed browser, vendor code or account data are bundled. This directory expects:

- `assets/forest-plate.png`: an authorised1920×1080 forest plate. The original used an inspected3s frame of the native fixed-camera Ultra export. Crop in `scene.js` is `[420,100,1320,742.5]`; a different image requires restaging.
- `assets/three.module.js` and `assets/three.core.js`: legally supplied Three.js ES modules, revision186 in the retained job. Exact npm patch version was not retained. Preserve the upstream MIT notices.
- `sound/source-music.mp3`: at least58s of authorised music; original retained source was benpm’s “Ambient Piano Music #4”, CC BY4.0, https://freesound.org/people/benpm/sounds/320603 .
- `sound/source-ambience.mp3`: at least50s of authorised ambience; original source was felix.blume’s “Night close to a river, crickets and frogs, bird sometimes.”, CC0, https://freesound.org/people/felix.blume/sounds/466955 .
- Python3 with an existing NumPy installation, FFmpeg/ffprobe, Node, an existing `puppeteer-core` installation and Chrome. No script installs dependencies or downloads a browser.

MIT covers the original code, **not** Marble outputs, third-party recordings, vendor libraries or provider rights. Free-generation output commercial permission is not established by this example or its public film link. Keep credits and disclose adaptations to the retained recordings.

## Local execution

Work from a fresh copy with your authorised inputs. Serve this directory locally:

```sh
python3 -m http.server 8874 --bind 127.0.0.1
```

In another terminal, set `FRAMEWRIGHT_CHROME` to your existing Chrome executable. Optionally set `FRAMEWRIGHT_PUPPETEER_MODULE` to an existing module path and `FRAMEWRIGHT_FFMPEG` to an existing FFmpeg binary; defaults use installed module/PATH resolution. `FRAMEWRIGHT_SCENE_URL` defaults to local port8874 and accepts loopback hosts only.

```sh
node render.cjs /path/to/new-empty-output-directory
mkdir -p final/sound
python3 build-sound.py
```

The recorder refuses an existing output directory and uses a fresh browser profile; it does not attach an owner browser/account. It records1260 JPEG94 frames into a silent42s1080p30 H.264 `film.mp4`, a native thumbnail and sample frames. The browser is closed after recording. The sound builder writes score/effect/premix WAVs and cue/phase measurements into `final/sound`; it **replaces those scratch mix files** on repeat execution. No mastering, muxing or publication is hidden in this command.

Master the whole premix as one piece, then explicitly mux with the silent picture and inspect the final encoded audio/video. The case retains the actual final QA; the generic wrappers here are sanitised derivatives, syntax-checked but not a clean-machine replay. Asset replacement, environment portability and exact cross-GPU pixels are unqualified. Do not claim wrapper execution from a syntax check.

## Preserved production mechanics

- 42s absolute-time scene with title, cold → warm → warning curves, walking/stop/turn/lantern action and end card. It exports `renderAt(t)` and `FramewrightCapture`.
- Native three-state cover from the same scene; in-scene captions suppressed during cover capture.
- Both stems start at sample 0,48kHz,2016000 samples; common headroom gain preserves their relative mix.
- Explicit 48kHz resample **before** rate-based octave/time treatment avoids the44.1kHz assumption found in the earlier full mix.
- Full decode/frame count, final-AAC/master alignment, stem recombination, mono-sum, encoded image/caption and full/reduced cover checks belong to finishing. Meter checks never substitute for listening.

This is a single-shot colour/sound study with a simple actor and an old soft environment. No moving-camera/depth/occlusion or multi-shot character continuity qualification is implied.

The `publication/` directory retains the English text draft, optional descriptive SRT and verbatim recording credits. These are plain files, not an archive or proof of live Studio settings.
