# Framewright / Remotion source example

Our authored 30-second 1080p30 film. Five independently registered scenes,
frame-driven motion, existing Framewright cover and original synthesized music.
No upstream skill code or media is bundled here. Package versions and lockfile
come from the tested isolated workspace; this copied example has not been installed
on a clean machine. Keep its dependencies and caches outside the system disk.

Requirements: compatible Node (pilot used Node 24), npm, Python 3.11+, FFmpeg,
and an available Chromium for Remotion. Read Remotion's own licence; this example's
presence does not relicense the renderer. The pilot used 4.0.535.

```sh
npm ci
python3 prepare-assets.py
npm run lint
npm run dev -- --port 5190
```

Open Framewright in Studio. The source uses no wall clock, random state or CSS
timeline animations. Music is generated locally from sine oscillators, normalized
with FFmpeg and rendered through Remotion's Audio component.

```sh
npx remotion still src/index.ts Framewright outputs/Framewright-Remotion-thumbnail.png --frame=60
npx remotion render src/index.ts Framewright outputs/Framewright-Remotion-1080p.mp4 --codec=h264 --crf=18 --concurrency=2
python3 verify-output.py
```

In the pilot, downloaded Headless Shell twice failed to connect within 25 seconds.
The successful render/still used a previously working Chromium through the supported
`--browser-executable=/absolute/path/to/chrome-headless-shell` option together with `--timeout=120000` on both commands. The first existing-browser
attempt also hit the default root-loading timeout; both failed logs were retained.
Select a compatible local browser; do not hardcode the pilot operator's machine path.
No upstream package was patched and no security checks were disabled to make this work.

The template's complete audit reports 10 high findings in its dev lint dependency
chain; `npm audit --omit=dev` reported zero in the tested runtime tree. Both remain
separate facts. Do not deploy Studio or describe the full install as vulnerability-free.

See [the pilot record](../../experiments/2026-10-14/framewright-remotion.md).
