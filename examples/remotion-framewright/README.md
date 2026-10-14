# Framewright / Remotion source example

Our authored 30-second 1080p30 film. Five independently registered scenes,
frame-driven motion, existing Framewright cover and original synthesized music.
No upstream skill code or media is bundled here. Renderer pins come from the tested isolated workspace. The example
subsequently received a separate dependency installation and lint-chain repair;
clean-machine video rendering has not been repeated. Keep its dependencies and caches outside the system disk.

Requirements: compatible Node (pilot used Node 24), npm, Python 3.11+, FFmpeg,
and an available Chromium for Remotion. Read Remotion's own licence; this example's
presence does not relicense the renderer. The pilot used 4.0.535.

```sh
npm ci
python3 prepare-assets.py
npm run check
npm run dev -- --port 5190
```

Open Framewright in Studio. The source uses no wall clock, random state or CSS
timeline animations. Music is generated locally from sine oscillators, normalized
with FFmpeg and rendered through Remotion's Audio component.

Set `REMOTION_BROWSER` to a working local Chromium executable (pilot: Chromium
152.0.7977.30). This is the complete tested rendering configuration:

```sh
REMOTION_BROWSER='/absolute/path/to/chrome-headless-shell'
npx remotion still src/index.ts Framewright outputs/Framewright-Remotion-thumbnail.png --frame=60 --browser-executable="$REMOTION_BROWSER" --timeout=120000
npx remotion render src/index.ts Framewright outputs/Framewright-Remotion-1080p.mp4 --codec=h264 --crf=18 --concurrency=2 --browser-executable="$REMOTION_BROWSER" --timeout=120000
python3 verify-output.py
```

In the pilot, downloaded Headless Shell twice failed to connect within 25 seconds.
The successful render/still used a previously working Chromium through the supported
`--browser-executable=/absolute/path/to/chrome-headless-shell` option together with `--timeout=120000` on both commands. The first existing-browser
attempt also hit the default root-loading timeout; both failed logs were retained.
Select a compatible local browser; do not hardcode the pilot operator's machine path.
No upstream package was patched and no security checks were disabled to make this work.

## Dependency audit repair

The original scaffold had 10 high package findings from one advisory:
[GHSA-vfj7-8cjw-p6xm](https://github.com/advisories/GHSA-vfj7-8cjw-p6xm).
`@remotion/eslint-config-flat` 4.0.535 pinned typescript-eslint 8.21.0, which pulled
fast-glob → micromatch → braces. Braces had no published patched version.

The example scopes an override to that config's typescript-eslint dependency,
pinning 8.71.2. Its dependency tree removes braces. Remotion and all runtime
package versions stay unchanged. A separate local install, ESLint, TypeScript
and full npm audit passed: **0 vulnerabilities, including dev dependencies**.
`npm run check` retains lint/types and the full high-severity audit gate. Revisit
the override when upstream updates its pin; do not suppress the advisory or
remove lint to obtain a green result. Original pilot audit evidence is historical.

See [the pilot record](../../experiments/2026-10-14/framewright-remotion.md).
