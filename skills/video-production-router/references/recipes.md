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

Tested once: Framewright identity film, 30s/1080p30/900 frames, five scenes, local
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
