# Staged market miniature — authored source

Original scene code from the [Spot-Market pilot](../../experiments/2026-10-15/spot-market-3d-miniature.md).
This preserves staging, geometry and deterministic camera/action timing. It is an
asset-dependent author-project example, not the open clean-machine reference film.
Use [the reference film](../../docs/first-video.md) for that purpose.

## Dependencies and asset contract

The supplied HTML expects these operator-provided files under `assets/`:

- `three.module.js` and `three.core.js`: Three.js 0.186.1 ES modules (MIT).
- `gsap.min.js`: GSAP runtime used by Hyperframes; inspect its applicable terms.
- `display.ttf` and `serif.ttf`: legally available display/serif fonts. The pilot
  used local macOS Arial Narrow Bold and Georgia; they are not redistributed.
- `cover.png`: authorised uncropped400×590 cover. This pilot used owner-supplied
  artwork; do not assume the repository licence grants rights to that artwork.
- `final-mix.wav`:20s48kHz stereo mix with speech aligned to the retained timeline.

Node22.14, Hyperframes 0.8.161 and a working Chrome runtime were used. The pilot
reused its existing Hyperframes installation. `package.json` pins CLI invocations;
no clean-machine installation or arbitrary replacement assets were tested.

From this directory after satisfying the asset contract:

```sh
npm run check
npm run dev
npm run render
```

Render writes the MP4 to the parent directory. These commands mirror the tested
CLI operations; the newly added npm wrappers were not separately executed.
The paused20s GSAP timeline calls `renderAt(t)`; transforms derive from absolute
time, without a realtime animation loop. Repeated8s seeks matched pixel-for-pixel
in the same environment. Cross-GPU pixel identity is not claimed.

The route is `staged-3d-scene`, tool ID `three-scene`: authored Three.js,
not Anatomy. Production scope remains the single pilot; new routing rules have
deterministic regressions but no new full model qualification. Real
geometry/action does not imply physically validated grain or logistics simulation.
