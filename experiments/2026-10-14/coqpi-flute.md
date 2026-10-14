# CoqPi / Flute — scoped React UI export

Question: can Flute produce a useful promo from a real, previously untested ABVX
React application? Owner selected CoqPi. The local source branch is
`experiment/flute-coqpi` ([CoqPi draft PR #8](https://github.com/markoblogo/CoqPi/pull/8),
commit `83bd7ac`). The run used its actual components, synthetic demo inputs,
and restored host style scopes. It did not use real recordings, credentials or
live AI generation. No Electron main/preload or production service was changed.

The official portable React setup and installed authoring guide were used. A
typed dev-only host connects the existing renderer to the shared Flute studio.
One JSON timeline drives camera/focus and actual Surface transforms. Actual
component source files are unchanged; promotional framing is separate.

Native export passed: 23s, 1920×1080, 30fps, 690 frames. Final version adds original
instrumental music with AAC; encoded video stream is unchanged. Five output frames
were inspected without studio controls. Full listening/aesthetic acceptance is
still for the owner; no video was uploaded publicly.

Flute snapshot CLI failed on this manual React adapter, while explicit-URL MP4
export succeeded. Thumbnail was extracted from the encoded video. Earlier setup
also found that pnpm did not expose the optional Playwright CLI at the root; its
installed CLI was used without patching Flute. Cold dependency setup was slower
than reusing the already-prepared earlier toolchain; no fair timing benchmark was run.

Validation: CoqPi check passed with 359 tests, no failures, two moderate advisory
findings below its high gate. Scene types passed. The production renderer build
contained no Flute/demo markers, and the guard rejected a deliberately injected
capture marker. Audio measured -19.3 LUFS with -8.6 dBFS true peak.

Use this route for deliberate spatial treatment of existing React UI. Brag remains
the starting point for a quick general software introduction; image montages and
local narration remain the book-trailer route. This pilot does not establish a
universal winner, full Electron support, physical optics, or audience performance.

Hashes/version details: outputs.json, entry coqpi-flute. Evidence: evidence/coqpi-flute.txt.
Local work: /Volumes/Work/flute-pilot-20261014. No upstream code, media masters,
model weights or dependency caches are bundled in Framewright.
