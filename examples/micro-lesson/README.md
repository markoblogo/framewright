# Asset-dependent two-host lesson source

Original Canvas composition from the120-second English Framewright lesson.
[Case](../../docs/experiments/framewright-micro-lesson.md) ·
[Procedure](../../skills/video-production-router/references/micro-lessons.md).

`scene.js` renders a deterministic frame through async `window.renderAt(seconds)`;
`window.sceneReady` is set only after source videos/stills are loaded. `getReport()`
returns the shot boundaries. `script.json` separates spoken turns/voices from the
visual source; `timeline.json` contains actual measured turn boundaries and file
hashes. These are original source/metadata, not copied Claudemy code.

Requires local cleared `assets/dog.mp4`, `book.mp4`, `game.mp4`,
`street-before.mp4`, `street-after.mp4`, plus `audio-envelope.json` derived from
actual PCM at60Hz. Those asset-dependent files, raw audio and model caches are
not distributed. The case receipt pins the actual private film and thumbnail.
Serve the folder locally, wait for readiness, then await renderAt at24fps and
capture the canvas. The actual trial used existing Chrome/Puppeteer and FFmpeg;
this source alone is not a turnkey installer or independently reproduced export.

For new material, update the script, factual source map, source rights, voice
measurements, media and shot mapping together. Do not inherit the original film's
technical or creative receipts. Graphic panels illustrate a workflow; they do not
impersonate an application UI. Keep visible credits for map-derived material.

Optional `index-v2.html` / `scene-v2.js` introduces two fictional photo presenters
for the first9seconds. It additionally needs private `assets/host-questioner-atlas.png`
and `assets/host-maker-atlas.png`, each a verified1536×1024 six-pose atlas. The
standalone `hosts-function.js` is the original inserted component for inspection;
the compiled composition in scene-v2 includes it. No generated portraits are
distributed here. Audio-envelope pose selection is not exact phoneme lip sync.
