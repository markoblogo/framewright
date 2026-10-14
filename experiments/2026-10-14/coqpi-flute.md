# CoqPi / Flute — scoped React UI export

Question: can Flute produce a useful promo from a real, previously untested ABVX
React application? Owner selected CoqPi. The local source branch is
`experiment/flute-coqpi` ([CoqPi draft PR #8](https://github.com/markoblogo/CoqPi/pull/8),
commit `83bd7ac`). The run used its actual components, synthetic demo inputs,
and restored host style scopes. It did not use real recordings, credentials or
live AI generation. No Electron main/preload or production service was changed.

## Source and licence evidence

- Flute source inspected: `4ab8c4a310ed051db9990e5a10a35fbcf2080cb1`;
  [MIT licence at that revision](https://github.com/webprodigies-org/flute/blob/4ab8c4a310ed051db9990e5a10a35fbcf2080cb1/LICENSE), copyright 2026 Web Prodigies.
  Installed package `@webprodigies/flute` 0.1.2 also declares `MIT` in its package.json.
  The inspected source revision is not asserted to be the package's build revision.
- CoqPi source baseline: `848fbdb89a7b99054f430429fd4f0a2bdc22bcfb`;
  [MIT licence at that revision](https://github.com/markoblogo/CoqPi/blob/848fbdb89a7b99054f430429fd4f0a2bdc22bcfb/LICENSE).
  Licence files and package metadata were checked locally during review remediation.
  Framewright's own licence does not replace these upstream notices or grant media rights.

## Criteria retained before rendering

The pilot workspace's original `BRIEF.md` retains these pre-execution conditions:
20–25 seconds, horizontal 1080p, genuine React components/styles with labelled
synthetic inputs; deterministic seekable camera/focus; no console/runtime failures
in the scene; no external requests; validate MP4 duration, dimensions and frame
count; inspect final frames. Install the published Flute package in an isolated
branch on Work, keep the normal app separate, and record failures and scope.
The brief allowed an original instrumental as a separately identified finishing
step and did not request narration. It excluded live microphone/provider activity,
personal data, production changes and public uploads. Its no-external-requests
condition concerns scene execution, not authorised package/browser downloads.

These criteria concern this browser-renderer pilot. Packaged Electron support,
physical optics, universal React support and audience performance were explicitly
outside scope. The production-bundle marker guard and stream-hash comparison were
additional verification added during execution, not predeclared acceptance gates.
The technical checks below do not substitute for owner artistic/audio acceptance.

## Execution and results

The official portable React setup and installed authoring guide were used. A
typed dev-only host connects the existing renderer to the shared Flute studio.
One JSON timeline drives camera/focus and actual Surface transforms. Actual
component source files are unchanged; promotional framing is separate.

Native export passed: 23s, 1920×1080, 30fps, 690 frames. Final version adds original
instrumental music with AAC; encoded video stream is unchanged. Five output frames
were inspected without studio controls. Full listening/aesthetic acceptance is
still for the owner. The agent did not upload the video. The owner subsequently
supplied [the YouTube publication](https://youtu.be/rqKXx_Z5AR0); it is retained as
a user-provided reference, not a byte-verified copy of the local export.

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
