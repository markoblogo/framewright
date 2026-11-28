# PixelFX — lighthouse switch-on, two palettes

27 November 2026. Existing PIXELFX-01 bounded trial executed; owner preference pending.

Pinned patch-gg/pixelfx revision 5294518ce7c72e48b6100a744596e0acf57f2826.
Unmodified native collect-burst, core painter, lights and RNG run inside an authored
absolute-time scene wrapper. Seed37; replay at120Hz;320x180 effect enlarged6x
nearest-neighbour over an original1920x1080 lighthouse illustration.
A amber and B mint/cyan share geometry, seed, placement and timing.

Each8.000s/240frames/30fps/1920x1080, zero audio. Lamp warms at1.7s;
burst begins2s, active for native1.35s; beam gently sweeps afterwards.
Three exports fully decode, with no unintended black interval.41 active colour
alpha masks match across palettes. Repeated/backwards samples and fresh-page
raster match. Separate normal colour plus additive light matches native composite
at2.2s on three backgrounds (#102b3b,#eeeeee,#746f68), max error0.
Combined RGBA sheet is approximate for glow on dark backgrounds; use separate
colour/light sheets for accurate composition. Six sheets and metadata retained.
Operator inspected both palette samples: visible accent around lamp, clear title.
This is one native effect, not qualification of the full library, upstream export
CLI, engine importers or arbitrary backgrounds/times.

Initial mixed SVG/two-canvas/CSS composition had repeated screenshot differences
although native buffers and SVG matched exactly. Two animation-frame waits alone
did not fix it. One high-resolution composition canvas with a local transparent
SVG foreground fixed sampled repeatability; serialized foreground initialisation
also timed out during diagnosis, cause unestablished. Failures retained separately.

Preparation began23:13:11UTC26November, with deadline23:33:11UTC. Work disconnected
and was reconnected during preparation; clock was not reset. First stable checked
amber sample23:32:45.887UTC:19m34.887s. Cyan rendering followed using the same
prepared route; both movies were not completed within20min. Capture/check194.578s;
composition and packaging additional. No paid requests, new models, app/npm install
or browser download. Existing Chrome, Playwright and FFmpeg; all files on Work.

MIT source and derivative notices retained, including SpriteFusion/HugoDuprez and
HollowCrown/rehan-remade notices. No upstream gallery font or demo art used.
Editorial-graphics ranking reviewed and unchanged: specific accent only, no default
provider promotion. Owner adoption is not inferred from technical success.

Retained package: productions/pixelfx-trial-2026-11-27, with native pin/notices,
scene and source artwork, render/compose recipes, sprites, QA and three masters.
README.md and MOTION.md describe replay. Standard fixed Framewright page/check
baseline reused; no automatic browser opening. Local review is not publication.
