# Recipes — tested 2026-10-14

## software-launch

Use for a short product introduction grounded in source code or a landing page.
Start from the full [Brag workflow](https://github.com/latent-spaces/brag), then
follow installed Hyperframes instructions. Check upstream requirements at use time.
The tested renderer was Hyperframes 0.8.157 with Node 24 and FFmpeg.

Inspect real product behaviour/assets; agree a single communication angle; prepare
the storyboard and composition; inspect representative frames and full playback;
render and inspect the final export. Deliver reusable copy/thumbnail as requested.
AsciiTheme used its real UI; AMI used current public branding and imagery.
Use source verification to avoid presenting a preview as a live operational feed.

Tested: 20-second AsciiTheme and 24-second AMI, horizontal 1080p/30fps, instrumental,
accepted by user. Full Brag supports optional narration, but that was not tested
here. Brag-slim and other model-specific dispatch paths were not tested.
User preferred this AsciiTheme presentation to the later retro-computer prototype.

## narrated-montage

Use for a book/product trailer built around existing authorised artwork. This is
a reusable method, not a packaged one-command generator. Do not recreate covers
or invent book excerpts, product capabilities, awards or testimonials.

1. Verify page facts, title/author/translator roles, artwork and CTA. Plan a few
   narrative beats, with the imagery's palette and typography guiding the treatment.
2. Use local [Kokoro ONNX](https://github.com/thewh1teagle/kokoro-onnx) if permitted
   and suitable for the requested language. Check its current voices/licences and
   available environment; use actual speech durations for the scene schedule.
3. Compose in Hyperframes with deterministic timing, restrained camera movement
   and readable type. Inspect cut boundaries; crossfades produced doubled text in
   our French test, so clean cuts worked better for that composition.
4. Mix voice, original/licensed music and only useful effects with
   [opus-sound-layer](https://github.com/Bodila51/opus-sound-layer). It supplies
   scripts and PROMPT.md; do not assume it is an installed root SKILL.md.
5. Run its encoded-file QA using unchanged thresholds, inspect/listen, and retain
   the log. Automated QA is not proof of natural pronunciation or marketing quality.

French test: ff_siwis, fr-fr, speed 0.86; approximately 28 seconds; no extra SFX.
English test: am_michael, en-us, speed 0.94; approximately 34 seconds. These voice
choices worked for these exports, not a universal language/voice recommendation.
Final audio was approximately -18 LUFS; music roughly 16–17 LU below speech.
These are measured results, not mandatory targets for every platform.

Good Dogs: page-turn effects failed audibility; replacement book-placement sounds
improved the result; the middle effect still failed and was removed. Two remaining
accents passed. Kenney recordings used here were CC0; a full sound library was not
tested. Do not turn this into a blanket licence claim for other libraries.
Visual/editor-structure advisory warnings are separate from the zero-warning
sound QA reports. Windows/Linux portability has not been tested.

## short-teaser

Use the established product/series composition for a short hook and CTA. The
six-second Good Dogs edit passed local audio QA; no audience A/B test was run.
Preserve the longer version as a separate deliverable. Shorts/vertical formats
need their own reframing and verification; horizontal success does not prove them.

## object-prototype

[Anatomy](https://github.com/wheresryan22/anatomy) already supports Codex. The test
adapted its bundled desk-computer example; it was not a newly authored 3D machine.
Replace wall-clock/random behaviour with deterministic seek(t), using one event
ledger for picture and audio. Test seeking out of order. Fix geometry issues with
the supplied line checker and inspect frames before adding many effects.

Five adapter tests and the visual checks passed. Combined encoded sound QA failed
with 22 audibility failures and 38 picture-motion warnings; global picture-motion
checks may not capture tiny key movements well. Do not declare the sound mix passed
or disable thresholds to compensate. The user stopped this direction, preferring
the earlier AsciiTheme promo. Historical-photo reconstruction, calibrated physics,
general 3D beta and agent swarms remain untested.

## live-react-scene

Use [Flute](https://github.com/webprodigies-org/flute) when the requested effect is
cinematic camera travel and focus around existing React DOM components. Honour an
explicit Flute choice; do not route it back to Hyperframes just because that is the
default renderer elsewhere. It is a different route from a narrated image montage.

Tested: Flute 0.1.2, React 19.2.7, Vite 6.4.3, Playwright 1.58.2, Node 24; CoqPi's
Electron-project renderer running in an isolated browser, not the packaged Electron
runtime. Requirements documented upstream: React DOM 18.2+/19, Node 22.12+, FFmpeg
and Chromium. Check current source/docs before a new installation.

1. Create a separate branch/checkout on the work disk. Inspect existing components,
   style scopes, providers and side effects. Use synthetic, visibly labelled inputs;
   do not load real app records merely to make the demonstration look populated.
2. Install the pinned dev dependency using the host package manager. Read FLUTE.md
   and the installed `flute guide --json`. For a custom/Electron renderer use its
   portable React adapter and an explicit compile-time development-only host.
3. Import real host components as Surface leaves. The JSON node transforms must
   also reach actual Surface props; metadata alone does not position the React tree.
   Preserve the required surrounding style/provider context. CoqPi needed scoped
   presentation spacing and existing prepare-layout styles; it was not zero-adaptation.
4. Use one studio/capture bridge and its canonical scene clock. Inspect close shots,
   intermediate camera positions and the closing view before a full export.
5. Export via the explicit loopback scene URL to a fresh project-relative MP4 filename.
   In this pnpm layout Playwright was available under Flute's optional dependencies
   but had no root CLI bin, so its installed cli.js downloaded Chromium to Work.
6. Check the encoded file, sample frames, original component provenance and the
   production build boundary. The CoqPi scene exported 23s/1080p30/690 frames.
   Optional original instrumental was added with FFmpeg; the H.264 stream hash
   stayed identical. Flute itself exported silent video.

Observed limitation: `flute snapshot` refused the portable React host with the
manual-preview instruction. Direct-URL video export worked. Extract a thumbnail
from the encoded export, record the limitation, and do not report the snapshot CLI
as passed. No Flute package code was patched for this test.

Native DOM depth-of-field approximates blur; it is not ray-traced bokeh or physics.
Full Electron, other hosts, narrator/audio workflows, arbitrary React compatibility
and audience impact remain untested. The new route does not promote the router
itself beyond structural_only. Do not change the host's production configuration
or install a global skill just to capture one scene.

## authored-react-film

Use Remotion when the task calls for authored, frame-driven React motion graphics,
editable scene timing and native picture/audio/still output. This is distinct from
Flute's camera around existing app components. Honour an explicit Remotion choice
and load its official creation, markup and rendering skills locally; Hyperframes
is not a prerequisite. Read the selected version's installed API before authoring.

First scoped test: Framewright identity film, 30s/1080p30/900 frames, five scenes, local
cover, original instrumental through @remotion/media, native PNG still. Follow
[the source example](https://github.com/markoblogo/framewright/tree/main/examples/remotion-framewright) in a full
Framewright checkout; when this skill is installed alone, use the upstream docs
and retain your own project source instead of assuming that example is present.

Start with criteria and verified copy, pin compatible @remotion packages together,
open Studio, use currentFrame/interpolate and measured timing. Avoid CSS animation,
Date/random-driven layouts or remote assets in a deterministic composition. Inspect
representative native frames and transitions; check actual encoded metadata and sound.
The native render/still used an explicit existing Chromium after the downloaded
Headless Shell twice timed out connecting. Use the supported --browser-executable
option and the supported --timeout=120000 loading allowance; retain failures and workaround, and do not patch the vendor package.

Remotion has its own Free/Company licence, not this repository's MIT licence.
The pilot qualifies only this local authored film, not all rendering paths, Studio
source-edit operations, voice/captions, vertical output or cloud rendering. The
original scaffold had 10 high dev lint findings. The retained example now removes
the braces chain through a scoped typescript-eslint update; full audit, lint and
types passed with zero vulnerabilities. The pilot environment remains historical.
No fair speed/quality comparison with Brag or Flute was conducted.

## staged-3d-scene

Choose for authored miniature/diorama scenes where objects act and the camera
explains a process. Tool ID `three-scene` means Three.js geometry/action authored
inside a Hyperframes composition; it does not mean Anatomy or a standalone engine.
Do not choose solely because a product has a cover or contains a pictured object.

Evidence: [Spot-Market 20s pilot](../../../experiments/2026-10-15/spot-market-3d-miniature.md)
and [authored source/asset contract](../../../examples/staged-market-scene/README.md).
Three.js 0.186.1 + Hyperframes 0.8.161,1920×1080/30fps;22 grain meshes, route-following
truck, converging quote tickets, absolute-time camera and genuine-cover book reveal.
Repeated seeking matched state/pixels in this environment. MP4/audio and extracted
PNG checked. Owner liked the 3D animation and narration; audience response unknown.

1. Plan actions, camera framing and reading holds. Obtain authorised assets and
   build simple geometry; cover art is not an automatic reconstruction source.
2. Follow Hyperframes instructions, verify WebGL/runtime/dependency licences and
   required assets. Derive all transforms from absolute timeline time, register a
   paused timeline and verify readiness before capture. No realtime-only loops.
3. Seek forward/back through action and inspect loading, object paths, camera,
   occlusion, title/CTA and closing hold. Deterministic animation is not physics.
4. Add Kokoro speech/original or authorised audio separately, measure duration,
   mix with FFmpeg or the selected master, then inspect the encoded MP4. Extracted
   thumbnails get independent crop/readability/dimensions/hash checks.
5. For mixed Flute/Remotion/other scenes, declare picture/colour/fps/frame boundaries,
   one audio/assembly owner and planned integration QA. Such seams were not tested
   by this single-scene pilot. Keep unavailable source/runtime checks blocked.

Known limits: no calibrated physics, arbitrary model import, automatic historical
reconstruction, live market values, vertical/alpha/native still or other fps/canvas
qualified. The profile downgrades evidence outside 1080p30; do not call a proposed
fallback tested. Preserve explicit tool choices, budget/account and publication
boundaries. No installer, paid service or media upload is implied.

## diagram-explainer

Use the `manimgx` profile for labelled workflow/process diagrams and intentional
card/line transformations. Tested path: ManimGX 0.1.1 → **FFmpeg CFR/timestamp
normalisation** → one audio master. It is not the authored Three.js miniature or
real UI capture. [MN7R experiment](../../../experiments/2026-10-15/mn7r-manim-mlx.md)
and [source](../../../examples/manimgx-mn7r/README.md) retain exact setup/limits.

Inspect native layout/storyboard first. Preserve the native VFR file, including
held-frame durations. The pilot had409 frames spanning20.033333s; that count alone
is not frame loss. Direct mux warned about DTS. The qualified route explicitly
uses `fps=30,setpts=PTS-STARTPTS`,600 output frames and re-encoding, then checks the
final 20s CFR picture/audio. Do not reset frame-number timestamps on deduplicated
VFR or stream-copy the native pilot without inspecting its timestamps.

For the new English audio layer, `mlx-audio` means only MLX-Audio 0.5.9 + local
Kokoro 82M/am_michael,speed1.03. Use a recognisable Kokoro model directory or explicit
supported configuration and install soundfile plus the correct English spaCy model
in its isolated environment before synthesis. Keep caches/models on Work. The
current voice profile supports **en only**; Ukrainian needs another verified exact
model and owner pronunciation review. No singing,diarization or cloning qualified.
`preferred_voice: "mlx-audio"` preserves an explicit voice runtime in offline plans;
unsupported languages remain unmet instead of silently changing the voice tool.

No known human preference or audience qualification for this film yet. Resource
setup exceeded the 2GB plan before task-only cache cleanup; retained runtimes/model
and new model downloads must be budgeted together. Reuse this environment instead
of repeating unchanged installation. New languages/formats/3D/math plots need
bounded follow-ups,not a general claim based on this 2D English promo.

### Ukrainian paper-route variation

For a narrative transformation from agricultural objects to a workflow,use the
authored-react-film route:Remotion4.0.535 authored SVG/React paper layers plus
local Piper1.4.2/Tetiana Ukrainian voice,then FFmpeg assembly.
[Experiment](../../../experiments/2026-10-15/agro-uk-paper-piper.md) and
[source example](../../../examples/remotion-agro-uk/README.md) retain the exact
24s1080p30 scope. `paper-cut-regroup` names authored kernel regrouping/route/truck/
contract action;it does not promise an automatic generator,real geography,3D or
physics. Owner listening found this exact Ukrainian voice weak:unnecessary pauses,wrong stress/intonation. Keep the existing clip;choose another tool for the next Ukrainian narration. Technical synthesis is not a quality recommendation. Keep unsupported
languages,singing and other voices outside the qualification.

Measure each voice WAV before cuts;retain locked timeline and separate stems.
Native silent MP4 is retained;final audio is added with FFmpeg. Inspect encoded
scene boundaries,object displacement,labels/cover and closing hold. Thumbnail is
an encoded20s frame,not a native-still claim. Chromium launch/root timeouts can
recur:retain failed logs and use a supported working executable,not disabled checks.
