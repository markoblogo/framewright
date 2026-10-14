# Your first Framewright film

One open reference project: the authored 30-second Framewright introduction.
This is a reproducible source route, not a universal installer. Real author-project
archives may use assets that are not redistributable; they are not prerequisites.

## Inputs and rights

Use only `examples/remotion-framewright/src`, its original score generator and
`assets/framewright-cover.png`. Framewright grants use of these repository materials
under its [MIT licence](../LICENSE); do not imply endorsement or impersonate the brand.
No book covers, customer data, API keys, voice service or external asset account is
needed. Remotion retains its own licence; review eligibility before running it.
The repository licence does not relicense the engine or its dependencies.

## Environment and exact route

Clone this repository at the v0.1.1 tag on a disk with space for Node/browser downloads.
Use Node 24 and npm, Python 3.11+, FFmpeg/ffprobe and a compatible local Chromium.
Remotion/CLI/media/transitions are pinned to 4.0.535; React/React DOM to 19.2.3.
The tested browser path used Chromium 152.0.7977.30; see the source example for the
connection failures and later warmed Chromium 157 still check. Other environments
need their own browser smoke test. No clean-machine re-render is claimed after the
subsequent dev-lint dependency repair.

From `examples/remotion-framewright`:

```sh
npm ci
python3 prepare-assets.py
npm run check
REMOTION_BROWSER='/absolute/path/to/chrome-headless-shell'
npx remotion still src/index.ts Framewright outputs/Framewright-Remotion-thumbnail.png --frame=60 --browser-executable="$REMOTION_BROWSER" --timeout=120000
npx remotion render src/index.ts Framewright outputs/Framewright-Remotion-1080p.mp4 --codec=h264 --crf=18 --concurrency=2 --browser-executable="$REMOTION_BROWSER" --timeout=120000
python3 verify-output.py
```

The browser path must be supplied; do not paste it literally. Dependency installation
uses the network. No paid API, login or upload is part of these commands. Downloads,
hardware, power and any Remotion licence obligation remain the operator's responsibility.

## Exact agent request

> Use Framewright's open Remotion reference project at examples/remotion-framewright.
> Reproduce its existing 30-second horizontal 1080p30 film and frame-60 PNG, keeping
> its pinned versions, original cover and synthesized score. Read its README first.
> Use my compatible Chromium path and the documented 120-second timeout. Check the
> full dependency audit, lint/types and encoded metadata; inspect representative
> frames/transitions and listen before calling artistic QA complete. Save all outputs
> locally. Do not add paid services, install unrelated tools or publish anything.
> If a requirement is missing, report it instead of silently changing renderer.

## Expected files and checks

`outputs/Framewright-Remotion-1080p.mp4`,
`outputs/Framewright-Remotion-thumbnail.png`, `outputs/ffprobe.json`;
asset preparation also creates local score WAVs and the working public cover.
Run the source example's verification: H264, 1920×1080, 30 fps, 900 frames,
30 seconds, stereo AAC and PNG 1920×1080. Reproduction outputs may have different
hashes across browser/encoder builds; historical hashes identify the retained pilot,
not a universal bit-identical target. Listen, inspect cuts/text, and retain new hashes.

## Time and cost of the recorded pilot

Elapsed wall time: **not retained**. Total production effort and per-run compute
cost: **not measured**. No paid/cloud service was used in the recorded pilot, but
that does not establish zero total cost or universal free licence eligibility.
For a new run record environment, install/render/QA times separately, package/browser
downloads and any actual licence charges. Do not infer speed from the 30-second runtime.

[Source example and known failures](../examples/remotion-framewright/README.md).
[Retained pilot](../experiments/2026-10-14/framewright-remotion.md).
[Public owner-supplied video](https://youtu.be/s3BBP698_r8).
