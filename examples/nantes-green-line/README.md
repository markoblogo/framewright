# Nantes-specific authored scene (asset-dependent)

Original Three.js scene and deterministic timeline event handler from the
[Nantes walking-film case](../../docs/experiments/nantes-green-line.md).
This is evidence and a filming starting point, not a self-contained renderer or
an exact reconstruction of Nantes. The package lock pins dependencies; upstream
code, GSAP, media, map datasets and generated images are not vendored.

## Input contract

Supply cleared local `assets/city.json` with projected-meter building footprints
(points, height, id), roads (points, kind), parks/waters (point rings), POIs
(id, ll, position, eyePosition) and `fullRoute` (all official longitude/latitude
line geometries). This source has Nantes-specific origin −1.55 / 47.218 and six
named stop models. Changing city requires a deliberate coordinate/model pass.
Supply cleared jardin/musee/cathedrale/chateau/lu PNGs, #view/#map canvases and
#title/#eyebrow/#small/#photo-label/#hud DOM nodes. Registration of the paused
100s `main` timeline occurs in the HTML after `window.__hf.buildReady.scene`.

Install pinned packages in an authorised local environment with install scripts
disabled, bundle scene.js with esbuild, and capture through HyperFrames. Do not
call arbitrary browser automation scripts. Render timing comes from `hf-seek`
absolute seconds; there is no requestAnimationFrame or wall-clock animation.

`check-route.py` is an offline coverage check. Its expected production folder has
research/official-full-route.geojson, film/assets/full-route.json,
film/assets/city.json and evidence/. It compares official geometries with both
film inputs and validates complete-map projection bounds. It does not fetch
sources, grant source rights or infer missing route branches. Raw sources are
not included. The same-instance replay diagnostic is private QA evidence, not a
claim of device-independent or encoded-audio determinism.
