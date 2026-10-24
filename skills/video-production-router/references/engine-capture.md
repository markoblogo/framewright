# Reusable canvas capture adapter

`engine_capture.py` captures a scene in a fresh local browser, verifies controls
and optional source audio, then normalises/decodes the recorded canvas with FFmpeg.
It does not create worlds, install dependencies, use an authenticated profile,
change a hosted game, upload or spend provider credits. Page navigation still
contacts the explicitly selected URL. Capture and reuse need authorised assets.

Tested: an original controllable canvas fixture with generated oscillator audio,
and a short excerpt from the published Babylon/PlayMCP Möbius Walk. Other engines,
iframe/offscreen/WebGPU captures, protected assets, mobile capture and long real-time
reliability are unqualified. Rendering the browser canvas is different from
capturing DOM captions, HUD overlays or an entire desktop.

## Plan first

Save a config beside the project:

```json
{
  "url": "http://127.0.0.1:8871/",
  "adapter": "contract",
  "canvas": "canvas",
  "width": 1280,
  "height": 720,
  "duration_seconds": 4,
  "fps": 30,
  "audio": "game",
  "seek_seconds": 0,
  "bot": true,
  "expect_motion": true,
  "repeat": 3
}
```

```sh
python3 skills/video-production-router/scripts/engine_capture.py local/capture.json
```

Default is offline validation only. Execution requires explicit `--execute`, a
**new** output directory, an installed Chrome/Chromium binary and installed
`puppeteer-core` module path. It also needs Node, FFmpeg and ffprobe on PATH (or
`--node`, `--ffmpeg`, `--ffprobe`). No download or install fallback:

```sh
python3 skills/video-production-router/scripts/engine_capture.py local/capture.json --execute --output local/take-01 --browser /path/to/chrome --puppeteer-module /path/to/puppeteer-core
```

`adapter` is `playmcp` for a page exposing the native `PlayMCP` controller, or
`contract` for an original scene exposing `window.FramewrightCapture`. Both need:

- `state()` returning `{ready, t, playing, muted, bot}`;
- `play()`, `pause()`, `seek(seconds)`, `mute(boolean)`, `setBot(boolean)`;
- for contract game audio, `getAudioStream()` returning the actual post-mute output
  MediaStream; native PlayMCP instead provides `sinks()` output gain nodes.

State must reflect actual scene time, not just an unrelated timer. The runner waits
for readiness and verifies paused time, seek, bot and advancing resumed time. With
`audio: game`, it measures the actual capture bus unmuted/muted/restored and checks
the encoded audio is present/non-silent. `audio: none` intentionally records no
audio track; no listening or native audio test is then inferred.

## Cycles and recording hooks

A natural scene may already close at a chosen period. Otherwise an authorised
scene may expose `FramewrightCapture.setCaptureTime(seconds, period)` for a
filming-only canonical camera cycle. An optional local `hook` file can install that
bridge; its exact `hook_sha256` is mandatory. It executes page code with the page's
authority, so inspect it before approving capture. No JavaScript string from config,
service template or remotely downloaded code is automatically executed as a hook.
Native PlayMCP controls remain native even when the optional timing hook is used.

The scene owns period, motion and audiovisual continuity. The adapter cannot make
an arbitrary four-second walk into a seamless loop. Source capture is bounded to
1–300 seconds, 1–60 fps and 3840×2160 (even dimensions, at least two frames); repetition is 1–100, final length at most two
hours. Default browser arguments enable autoplay/background capture; sandboxing is
not disabled. Explicit `browser_args` are an operator choice and remain in the
private config/report. Profile, extension-loading and remote-debugging overrides
are refused so capture cannot silently attach a personal browser profile.

Outputs: raw `source.webm`, normalised `cycle.mp4`, repeated `capture.mp4`, end
screenshot, config, browser report and capture report with hashes. Source WebM may
omit container duration; encoded packet timestamps are the fallback. A failed run
keeps a failed report and partial outputs for diagnosis, not an accepted master.
Use a new take directory for retries.

All decoded luma frames are checked for motion and first/last-frame difference.
The numeric visual seam is pass/warn against adjacent-frame differences; source
blackness, composition, subtle glitches and artistic continuity still need viewing.
Audio checks measure RMS and boundary discontinuity relative to sampled adjacent
jumps. A numeric audio pass cannot establish a musically seamless loop: listen
across several joins. Seam warnings remain visible and do **not** block saving a
useful non-loop excerpt. A full final decode is separate from human acceptance.

Retain the master/report in the same [production project](projects.md), record
technical findings with their scope, and obtain creative/listening acceptance
separately. A completed capture report is not directly a unified `media_review.py`
report: inspect it, then record/import the appropriate separately qualified checks.
Disclose repeated/canonical footage when it materially changes the viewing promise.
See the [ambient recipe](../../../docs/workflows/ambient-game-video.md) and
[adapter trial](../../../docs/experiments/production-memory-adapters.md).

## Reproduce the open smoke test

The checkout has an original test fixture, not copied game code. Start
`python3 -m http.server 8871 --bind 127.0.0.1 --directory tests/fixtures/engine-capture`,
then use the config above with `duration_seconds: 2` (its natural two-second cycle).
Normal unit tests require no browser or provider. To run the opt-in real-browser
integration test, set `FRAMEWRIGHT_BROWSER` and `FRAMEWRIGHT_PUPPETEER` to those
installed paths and run `python3 -m unittest discover -s tests -p test_engine_capture.py -q`.
