# PixelFX and a Codex production recipe

Status31October2026: primary-source review; active bounded candidate, not installed
or rendered. PIXELFX-01 maps to M4/R05 (reusable motion) and Good Dog R07.
No production acceptance or compatibility benchmark follows from this assessment.

## Sources and fit

- [PixelFX](https://github.com/patch-gg/pixelfx): code-driven pixel effects, browser
  integration and sprite-sheet export. Repository metadata and README disagree on
  the effect count; do not use that count as a capability gate.
- [Package prerequisites](https://github.com/patch-gg/pixelfx/blob/main/package.json):
  Node18+, ES modules; FFmpeg is optional for previews in the upstream skill.
- [Notices](https://github.com/patch-gg/pixelfx/blob/main/NOTICE.md): MIT code with
  attributed Sprite Fusion and Hollow Crown contributions. The gallery's Patch
  Pixel font has separate terms: exclude it from the first test. Preserve the exact
  checkout revision, LICENSE and applicable notices outside this repository.
- [Sprite Fusion method](https://www.spritefusion.com/blog/how-to-make-good-pixel-art-effects-with-claude):
  iterative visual selection; the article explicitly includes Codex. This is a
  useful working method, not a guarantee that a prompt yields finished animation.

Useful film roles: small event accents, transitions between visual modes, or an
intentional short pixel-art passage. It is not an image-to-video generator or a
replacement for continuous character acting.

## Codex adaptation: one selected effect, one reviewable output

This is an original Framewright recipe, not a copied or installed upstream skill.
Do not run Claude marketplace commands. Use the existing production journal and
local capture/edit path; PixelFX remains an optional external dependency.

1. Write the shot purpose, placement and protected elements before touching code.
   Good Dog's first candidate is a reward impulse at the schematic REWARD node,
   or a transition into the accepted ASCII view. Keep canonical Pictiq glyphs,
   accepted barks, source characters and approved timing unchanged.
2. Inspect a pinned external checkout and the selected effect/tool imports before
   running them. Start with an existing pickup or transition effect. Use an
   isolated folder; do not vendor upstream code or install a global plugin.
3. Make two contrasting treatments sequentially on this Mac: restrained amber
   pickup versus cyan scan. Proposed delivery:2s,24fps,320×180 working grid,
   nearest-neighbour4× upscale to1280×720. Avoid arbitrary scaling/blur. Review
   motion at final size and thumbnail size, not just a contact sheet.
4. Save seed, palette, effect ID, revision, duration, grid, placement and export
   settings. Reconstruct from time zero for repeated seeks when simulation state
   is involved; compare repeated frames rather than assuming determinism.
5. Export a transparent sprite sheet/PNG sequence when appropriate. Check alpha
   over dark, light and target backgrounds; inspect baked glow and first/last
   frames. The ordinary H.264 preview is not the transparency master. Integrate
   only after checking the actual export contract. Preserve colour and glow
   separately if the target composite requires it.

Reusable request for Codex:

> Prepare two sequential2-second pixel-art treatments for the reward event in the
> Good Dog schematic. Use a pinned PixelFX effect in an isolated workspace. Keep
> all canonical artwork, Pictiq and accepted audio unchanged. Save reproducible
> settings, full-speed previews and a contact sheet. Show the strongest treatment
> with neighbouring footage. Record technical checks separately from my approval.

## PIXELFX-01 acceptance and stop conditions

One effect → one parameter revision → repeat export → target composite. Compare
readability, timing, reproducibility, alpha/glow, seams and render cost. Save both
versions and owner choice. Stop on clipping, accidental character replacement,
font-rights uncertainty, excessive flicker or resource pressure. No new cloud
credits, GPU models or background batch rendering. Installation and first render
remain queued; the current conveyor correction takes priority.
