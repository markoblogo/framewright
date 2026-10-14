# Framewright / Remotion — authored identity film

Owner selected Remotion and its official skills, with Framewright itself as the
subject. This is a 30-second English motion-graphics introduction, not a recording
of an app or a one-click text-to-video result. Existing original cover plus our
authored React scene source and original local instrumental; no generated narration.

## Sources and licence

Installed remotion, @remotion/cli, @remotion/media and @remotion/transitions:
4.0.535. React 19.2.3, TypeScript 5.9.3, Node 24. The installed package's LICENSE.md
was read and retained locally: Remotion's own Free/Company licence (free eligibility
includes individuals and companies up to three employees), not MIT. Check current
[terms](https://github.com/remotion-dev/remotion/blob/v4.0.535/LICENSE.md) for reuse.
No paid service/account was used. Original Framewright code remains under this
repository's licence; no upstream runtime or skill is redistributed here.

Official skills mirror inspected at [7ba4dcf8ebe1626b00baa41e1f2478113719b60b](https://github.com/remotion-dev/skills/tree/7ba4dcf8ebe1626b00baa41e1f2478113719b60b):
creation, video layout, markup, composition/scene structure, interactivity, audio
and render instructions. The standalone skills mirror had no separate licence file
or package licence declaration; retain upstream provenance and do not treat it as
MIT or copy it into this repo. This is an agent authoring test, not an independent
evaluation of those skills' behaviour across models or unseen tasks.

## Predeclared criteria and execution

The original local BRIEF.md was written before composition authoring: 30s,
1920x1080 at 30fps, pinned official runtime/skills, deterministic frame motion,
no CSS timeline animations or Date/random dependence, local cover, original
instrumental, native still, encoded metadata/audio checks, representative-frame
and transition inspection, lint/types pass, readable safe margins. No composition
remote assets, accounts, providers, production changes or public upload. Source
and outputs remain on Work. Tool dependency/browser downloads are separate from
the composition's local asset scope.

Official create-video scaffold → Studio opened before authoring → five separate
React scene files/registrations → frame-driven sequencing and Audio → native still
and MP4 → FFprobe/FFmpeg QA. English copy describes task selection, complementary
tools and retained methods/evidence. It does not invent an automated service.
See [our source and commands](../../examples/remotion-framewright/README.md).

## Failure and workaround

Two native still attempts with the newly downloaded Headless Shell timed out
connecting after 25000ms. An isolated --version process also stalled. Root cause
was not established; cold disk/launch timing is a hypothesis, not a finding.
The supported --browser-executable flag pointed at an already working local
Chromium 152.0.7977.30. An initial attempt with that browser also timed out loading the root component;
the documented --timeout=120000 option allowed loading to complete. Native still
and full render then succeeded without
patching Remotion or disabling safeguards. This pilot therefore qualifies the
explicit-browser route, not an unconditional default-browser installation.

A later still with the downloaded Chromium 157.0.8080.0 also succeeded after
warm-up with --timeout=120000. This does not erase the initial failures or prove
their root cause. Full-film qualification uses the explicit Chromium 152 route.

The scaffold audit retained 10 high findings in its dev lint chain; the runtime
audit with --omit=dev returned zero. Lint/type success does not dismiss advisories.
Studio was used locally and is not published as a hosted service.

## Result and qualification

Native H264 MP4 with stereo AAC, 30 seconds, 1920x1080, 30fps, 900 frames.
Native still succeeded. Representative encoded frames and transitions inspected;
audio metrics retained in [evidence](evidence/framewright-remotion.txt). No claim
of human listening, owner aesthetic acceptance, public upload or audience result.
Final file size/hash in outputs.json; thumbnail and delivery manifest retained
locally. A copied source example is retained here but clean-machine reproduction
has not been tested. The copied example passed lint/types and asset preparation
using the existing dependency tree; its regenerated score matched the pilot score
hash. Published TSX was formatted without changing the authored scene behaviour.
System font/browser/platform changes may change rendered pixels.

Use for deliberately authored motion graphics and reusable frame timelines. Flute
remains the tested route around existing React components; Brag remains the quick
software-introduction starting point. Different briefs/tool preparation prevent
a fair speed, quality or cost comparison. Voice/captions, cloud, vertical variants,
universal browser support and automatic capture remain untested. Router stays
structural_only; no new independent model evaluation was run.
