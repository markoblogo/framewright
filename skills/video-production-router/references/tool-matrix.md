# Tool capability matrix

Generated from `tools.json`; reviewed 2026-10-16.

Scope: decision-relevant inventory, not an exhaustive API guarantee. Tested means
the stated local experiment only. Documented needs installed-version verification;
failed is a retained limitation; unknown is not a usable promise. Styles are
affordances and preferences, not renderer boundaries or comparative quality scores.

## Brag full

**Role:** orchestrator. **Inputs:** source-project, brand.

**Style directions:** default, polished, cinematic, deadpan, app-store, chaotic, yc-parody.
Seven documented tone presets shape story, rhythm and typography; default is playful/clean. Freeform tone overrides the presets. See the immutable tone reference in sources.brag-tones.

**Tested version/scope:** retained full-workflow snapshot

**Licence:** MIT; renderer/providers have separate terms

| Feature | Evidence | Scope / source |
| --- | --- | --- |
| `storyboard` | tested | Observed scope: asciitheme, ami [Source](https://github.com/latent-spaces/brag/blob/069432cac935ed1895859df201c31436c07fb74e/README.md) |
| `video-export` | tested | Observed scope: asciitheme, ami [Source](https://github.com/latent-spaces/brag/blob/069432cac935ed1895859df201c31436c07fb74e/README.md) |
| `typography` | tested | Observed scope: asciitheme, ami [Source](https://github.com/latent-spaces/brag/blob/069432cac935ed1895859df201c31436c07fb74e/README.md) |
| `narration` | documented | Upstream claim; not locally qualified [Source](https://github.com/latent-spaces/brag/blob/069432cac935ed1895859df201c31436c07fb74e/README.md) |
| `vertical-format` | documented | Upstream claim; not locally qualified [Source](https://github.com/latent-spaces/brag/blob/069432cac935ed1895859df201c31436c07fb74e/README.md) |
| `transitions` | documented | Upstream claim; not locally qualified [Source](https://github.com/latent-spaces/brag/blob/069432cac935ed1895859df201c31436c07fb74e/README.md) |

**Limits:** Full Hyperframes workflow was tested; brag-slim was not. Voice is documented, not exercised in our Brag runs.

## Hyperframes

**Role:** renderer. **Inputs:** source-project, brand, book-art, composition, video, object.

**Style directions:** editorial, montage, kinetic, minimal, playful.
HTML/CSS/SVG/Canvas plus seekable motion. The book-test editorial look was our direction, not an engine restriction.

**Tested version/scope:** 0.8.157 in retained pilots

**Licence:** Apache-2.0 for CLI; check current runtime, asset, cloud/provider terms

| Feature | Evidence | Scope / source |
| --- | --- | --- |
| `video-export` | tested | Observed scope: asciitheme, ami, jeanne-fr, good-dogs-en, good-dogs-teaser [Source](https://hyperframes.heygen.com/concepts/compositions) |
| `typography` | tested | Observed scope: asciitheme, ami, jeanne-fr, good-dogs-en, good-dogs-teaser [Source](https://hyperframes.heygen.com/concepts/compositions) |
| `image-pan-zoom` | tested | Observed scope: asciitheme, ami, jeanne-fr, good-dogs-en, good-dogs-teaser [Source](https://hyperframes.heygen.com/concepts/compositions) |
| `scene-timeline` | tested | Observed scope: asciitheme, ami, jeanne-fr, good-dogs-en, good-dogs-teaser [Source](https://hyperframes.heygen.com/concepts/compositions) |
| `transitions` | tested | Observed scope: asciitheme, ami, jeanne-fr, good-dogs-en, good-dogs-teaser [Source](https://hyperframes.heygen.com/concepts/compositions) |
| `still-export` | documented | Upstream claim; not locally qualified [Source](https://hyperframes.heygen.com/concepts/compositions) |
| `native-audio` | documented | Upstream claim; not locally qualified [Source](https://hyperframes.heygen.com/concepts/compositions) |
| `captions` | documented | Upstream claim; not locally qualified [Source](https://hyperframes.heygen.com/concepts/compositions) |
| `vertical-format` | documented | Upstream claim; not locally qualified [Source](https://hyperframes.heygen.com/concepts/compositions) |
| `svg-overlay` | documented | Upstream claim; not locally qualified [Source](https://hyperframes.heygen.com/concepts/compositions) |
| `shader-transitions` | documented | Upstream claim; not locally qualified [Source](https://hyperframes.heygen.com/packages/shader-transitions) |
| `color-grade` | documented | Upstream claim; not locally qualified [Source](https://hyperframes.heygen.com/reference/color-grading) |
| `speed-ramp` | documented | Upstream claim; not locally qualified [Source](https://hyperframes.heygen.com/reference/speed-ramps) |
| `ascii-treatment` | documented | Check current installed version, browser/capture requirements and effect-specific controls. [Source](https://hyperframes.heygen.com/reference/color-grading) |
| `pixelate` | documented | Check current installed version, browser/capture requirements and effect-specific controls. [Source](https://hyperframes.heygen.com/reference/color-grading) |
| `bloom` | documented | Check current installed version, browser/capture requirements and effect-specific controls. [Source](https://hyperframes.heygen.com/reference/color-grading) |
| `lut` | documented | Check current installed version, browser/capture requirements and effect-specific controls. [Source](https://hyperframes.heygen.com/reference/color-grading) |
| `wave-warp` | documented | Check current installed version, browser/capture requirements and effect-specific controls. [Source](https://hyperframes.heygen.com/guides/vfx-chain) |
| `displacement` | documented | Check current installed version, browser/capture requirements and effect-specific controls. [Source](https://hyperframes.heygen.com/guides/vfx-chain) |

**Limits:** New VFX, captions, vertical/4K/cloud paths were not validated by our horizontal pilots. Media and animation timing must share the seekable timeline. Current docs note conflicts between capturing VFX chains and page-side shader transitions; test the combined layer, do not assume independent effects compose safely.

## Flute

**Role:** renderer. **Inputs:** react-ui.

**Style directions:** cinematic-ui, spatial, minimal.
Camera travel, perspective, depth and selective focus around actual DOM panels; preserve host styles/providers. DOM blur is not ray-traced optics.

**Tested version/scope:** 0.1.2

**Licence:** MIT

| Feature | Evidence | Scope / source |
| --- | --- | --- |
| `video-export` | tested | Observed scope: coqpi-flute [Source](https://github.com/webprodigies-org/flute/blob/4ab8c4a310ed051db9990e5a10a35fbcf2080cb1/README.md) |
| `react-components` | tested | Observed scope: coqpi-flute [Source](https://github.com/webprodigies-org/flute/blob/4ab8c4a310ed051db9990e5a10a35fbcf2080cb1/README.md) |
| `camera-travel` | tested | Observed scope: coqpi-flute [Source](https://github.com/webprodigies-org/flute/blob/4ab8c4a310ed051db9990e5a10a35fbcf2080cb1/README.md) |
| `depth-of-field` | tested | Observed scope: coqpi-flute [Source](https://github.com/webprodigies-org/flute/blob/4ab8c4a310ed051db9990e5a10a35fbcf2080cb1/README.md) |
| `scene-timeline` | tested | Observed scope: coqpi-flute [Source](https://github.com/webprodigies-org/flute/blob/4ab8c4a310ed051db9990e5a10a35fbcf2080cb1/README.md) |
| `vertical-format` | documented | Upstream claim; not locally qualified [Source](https://github.com/webprodigies-org/flute/blob/4ab8c4a310ed051db9990e5a10a35fbcf2080cb1/README.md) |
| `still-export` | failed | Portable CoqPi adapter snapshot CLI failed; FFmpeg extracted the delivered thumbnail. [Source](https://github.com/webprodigies-org/flute/blob/4ab8c4a310ed051db9990e5a10a35fbcf2080cb1/README.md) |

**Limits:** Browser-host CoqPi success does not establish packaged Electron or arbitrary React support. Keep real data and IPC outside demo. No Flute audio workflow was tested.

## Remotion

**Role:** renderer. **Inputs:** brand, data, book-art, composition, react-ui, video, object.

**Style directions:** editorial, kinetic, minimal, data-motion, paper-cut, lcd-editorial.
React frame-driven graphics and programmable layout; typography, editorial montage, UI or 3D can be authored. Our restrained Framewright film is one art direction.

**Tested version/scope:** 4.0.535

**Licence:** Remotion Free/Company licence; individual/small-team eligibility and paid features need separate checking

| Feature | Evidence | Scope / source |
| --- | --- | --- |
| `video-export` | tested | Observed scope: framewright-remotion [Source](https://www.remotion.dev/docs/) |
| `still-export` | tested | Observed scope: framewright-remotion [Source](https://www.remotion.dev/docs/) |
| `native-audio` | tested | Observed scope: framewright-remotion [Source](https://www.remotion.dev/docs/) |
| `typography` | tested | Observed scope: framewright-remotion [Source](https://www.remotion.dev/docs/) |
| `scene-timeline` | tested | Observed scope: framewright-remotion [Source](https://www.remotion.dev/docs/) |
| `image-pan-zoom` | documented | Upstream claim; not locally qualified [Source](https://www.remotion.dev/docs/) |
| `data-driven` | documented | Upstream claim; not locally qualified [Source](https://www.remotion.dev/docs/) |
| `vertical-format` | documented | Upstream claim; not locally qualified [Source](https://www.remotion.dev/docs/) |
| `react-components` | documented | Upstream claim; not locally qualified [Source](https://www.remotion.dev/docs/) |
| `svg-overlay` | documented | Upstream claim; not locally qualified [Source](https://www.remotion.dev/docs/) |
| `transitions` | documented | Upstream claim; not locally qualified [Source](https://www.remotion.dev/docs/transitions/) |
| `book-flip` | documented | Upstream claim; not locally qualified [Source](https://www.remotion.dev/docs/transitions/) |
| `film-burn` | documented | Upstream claim; not locally qualified [Source](https://www.remotion.dev/docs/transitions/) |
| `zoom-blur` | documented | Upstream claim; not locally qualified [Source](https://www.remotion.dev/docs/transitions/) |
| `object-3d` | documented | Upstream claim; not locally qualified [Source](https://www.remotion.dev/docs/three) |
| `captions` | documented | Upstream claim; not locally qualified [Source](https://www.remotion.dev/docs/captions) |
| `cube-transition` | documented | Official transition list marks cube paid; not covered by this pilot. [Source](https://www.remotion.dev/docs/transitions/) |
| `wipe` | documented | Official transition presentation; not exercised in the Framewright film. [Source](https://www.remotion.dev/docs/transitions/) |
| `slide` | documented | Official transition presentation; not exercised in the Framewright film. [Source](https://www.remotion.dev/docs/transitions/) |
| `iris` | documented | Official transition presentation; not exercised in the Framewright film. [Source](https://www.remotion.dev/docs/transitions/) |
| `ripple` | documented | Official transition presentation; not exercised in the Framewright film. [Source](https://www.remotion.dev/docs/transitions/) |
| `crosswarp` | documented | Official transition presentation; not exercised in the Framewright film. [Source](https://www.remotion.dev/docs/transitions/) |
| `paper-cut-regroup` | tested | Authored90-kernel field→route→contract motion,paper truck/stamp/book reveal in24s1080p30 UK promo;not physics or automatic scene generation. Native pixel-repeat discrepancy retained. [Source](https://www.remotion.dev/docs/) |
| `lcd-terminal-motion` | tested | 24s1080p30 authored LCD housing,pixel grain,factor selectors,abstract conveyor and slat-to-cover reveal;encoded samples checked. No real quotes,service UI,geography,physics or strobe. [Source](https://www.remotion.dev/docs/) |

**Limits:** Explicit Chromium and 120s load allowance used for full film; cold default browser failed twice, later still passed. 3D/captions/extra transition packages are documented, not locally tested. Dev audit repair retained separately.

## Anatomy

**Role:** illustrator. **Inputs:** object.

**Style directions:** isometric, technical.
Dense crafted isometric objects, four-tone shaded SVG, optional integrated WebGL layers and beta 3D moving parts. Recognisable mechanical explanations, not generic slides.

**Tested version/scope:** e6600ffc4e8e6620eeb45bf49bcdbd5e4b84163f in prototype

**Licence:** MIT at the reviewed revision (sources.anatomy-licence); input assets retain their own rights.

| Feature | Evidence | Scope / source |
| --- | --- | --- |
| `isometric-svg` | tested | Observed scope: anatomy-prototype [Source](https://github.com/wheresryan22/anatomy/blob/e6600ffc4e8e6620eeb45bf49bcdbd5e4b84163f/README.md) |
| `object-motion` | tested | Observed scope: anatomy-prototype [Source](https://github.com/wheresryan22/anatomy/blob/e6600ffc4e8e6620eeb45bf49bcdbd5e4b84163f/README.md) |
| `svg-overlay` | documented | Upstream claim; not locally qualified [Source](https://github.com/wheresryan22/anatomy/blob/e6600ffc4e8e6620eeb45bf49bcdbd5e4b84163f/README.md) |
| `webgl-effects` | documented | Upstream claim; not locally qualified [Source](https://github.com/wheresryan22/anatomy/blob/e6600ffc4e8e6620eeb45bf49bcdbd5e4b84163f/README.md) |
| `object-3d` | documented | Upstream claim; not locally qualified [Source](https://github.com/wheresryan22/anatomy/blob/e6600ffc4e8e6620eeb45bf49bcdbd5e4b84163f/README.md) |
| `still-export` | documented | Upstream claim; not locally qualified [Source](https://github.com/wheresryan22/anatomy/blob/e6600ffc4e8e6620eeb45bf49bcdbd5e4b84163f/README.md) |
| `video-export` | unknown | No native MP4 exporter verified; a deterministic adapter and renderer are a separate chain. [Source](https://github.com/wheresryan22/anatomy/blob/e6600ffc4e8e6620eeb45bf49bcdbd5e4b84163f/README.md) |

**Limits:** Local visual prototype only; combined sound QA failed. Beta 3D is not a calibrated physics simulator. Historical accuracy remains unverified.

## Kokoro ONNX

**Role:** voice. **Inputs:** .

**Style directions:** narrated, measured.
Synthetic narration with selectable voice/speed; language and pronunciation choices shape performance. It does not write the story or render picture.

**Tested version/scope:** retained v1.0 ONNX voice/model files

**Licence:** Wrapper MIT; model Apache-2.0; inspect individual input/voice rights

| Feature | Evidence | Scope / source |
| --- | --- | --- |
| `narration` | tested | Observed scope: jeanne-fr, good-dogs-en [Source](https://github.com/thewh1teagle/kokoro-onnx/blob/3596b26764286a7de9d90c363e988d50578918e5/README.md) |

**Limits:** Local FR/EN tested; other documented languages require a voice/pronunciation and timing trial. No voice cloning tested.

## opus-sound-layer

**Role:** audio. **Inputs:** .

**Style directions:** cinematic, tactile.
Recorded sound effects, cue placement and measured final-file QA; sonic palette can be restrained or dramatic. Metrics do not replace listening.

**Tested version/scope:** 52ac266a24b7dfd3cd06a28c34d5af360a8d7586 in pilots

**Licence:** MIT code; upstream kit CC0 with credits; added sounds retain their own rights

| Feature | Evidence | Scope / source |
| --- | --- | --- |
| `audio-mix` | tested | Observed scope: jeanne-fr, good-dogs-en, good-dogs-teaser [Source](https://github.com/Bodila51/opus-sound-layer/blob/52ac266a24b7dfd3cd06a28c34d5af360a8d7586/README.md) |
| `audio-qa` | tested | Observed scope: jeanne-fr, good-dogs-en, good-dogs-teaser [Source](https://github.com/Bodila51/opus-sound-layer/blob/52ac266a24b7dfd3cd06a28c34d5af360a8d7586/README.md) |
| `ducking` | documented | Upstream claim; not locally qualified [Source](https://github.com/Bodila51/opus-sound-layer/blob/52ac266a24b7dfd3cd06a28c34d5af360a8d7586/README.md) |
| `sfx-library` | documented | Upstream claim; not locally qualified [Source](https://github.com/Bodila51/opus-sound-layer/blob/52ac266a24b7dfd3cd06a28c34d5af360a8d7586/README.md) |
| `peak-alignment` | documented | Upstream claim; not locally qualified [Source](https://github.com/Bodila51/opus-sound-layer/blob/52ac266a24b7dfd3cd06a28c34d5af360a8d7586/README.md) |
| `room-effect` | documented | Upstream claim; not locally qualified [Source](https://github.com/Bodila51/opus-sound-layer/blob/52ac266a24b7dfd3cd06a28c34d5af360a8d7586/README.md) |
| `normalization` | documented | Upstream claim; not locally qualified [Source](https://github.com/Bodila51/opus-sound-layer/blob/52ac266a24b7dfd3cd06a28c34d5af360a8d7586/README.md) |

**Limits:** Anatomy combined sound run failed (22 audibility failures); Good Dogs intermediate effects were removed after QA. Never lower thresholds to make an effect pass.

## FFmpeg

**Role:** finisher. **Inputs:** video.

**Style directions:** neutral.
Finishing/transcoding/filter primitives, not a project-specific visual direction. Combine with a renderer rather than add an unnecessary redesign.

**Tested version/scope:** local ffmpeg/ffprobe on PATH

**Licence:** Build-dependent LGPL/GPL and codec/asset conditions; verify the actual build

| Feature | Evidence | Scope / source |
| --- | --- | --- |
| `video-export` | tested | Observed scope: coqpi-flute, framewright-remotion, jeanne-fr, good-dogs-en [Source](https://ffmpeg.org/ffmpeg-filters.html) |
| `still-export` | tested | Observed scope: coqpi-flute, framewright-remotion, jeanne-fr, good-dogs-en [Source](https://ffmpeg.org/ffmpeg-filters.html) |
| `media-mux` | tested | Observed scope: coqpi-flute, framewright-remotion, jeanne-fr, good-dogs-en [Source](https://ffmpeg.org/ffmpeg-filters.html) |
| `normalization` | tested | Observed scope: coqpi-flute, framewright-remotion, jeanne-fr, good-dogs-en [Source](https://ffmpeg.org/ffmpeg-filters.html) |
| `concat` | documented | Upstream claim; not locally qualified [Source](https://ffmpeg.org/ffmpeg-filters.html) |
| `captions` | documented | Upstream claim; not locally qualified [Source](https://ffmpeg.org/ffmpeg-filters.html) |
| `transitions` | documented | Upstream claim; not locally qualified [Source](https://ffmpeg.org/ffmpeg-filters.html) |
| `image-pan-zoom` | documented | Upstream claim; not locally qualified [Source](https://ffmpeg.org/ffmpeg-filters.html) |
| `color-grade` | documented | Upstream claim; not locally qualified [Source](https://ffmpeg.org/ffmpeg-filters.html) |
| `speed-ramp` | documented | Upstream claim; not locally qualified [Source](https://ffmpeg.org/ffmpeg-filters.html) |

**Limits:** Stream copy is conditional on compatible containers/codecs; resizing, burning captions or frame-rate conversion requires re-encoding and final QA.

## Suno

**Role:** music-provider. **Inputs:** .

**Style directions:** electronic, cinematic, pop, song, instrumental.
Prompted genre/instrument/voice directions, not a fixed house style or verified coverage of every language. Singing is distinct from Kokoro narration.

**Tested version/scope:** No public qualification record; current account/model must be checked

**Licence:** Cloud service terms, not the repository MIT licence. Free/trial use can be personal and noncommercial; approved-download rights and account/song history require per-asset review. A noncommercial limitation is not a technical failure.

| Feature | Evidence | Scope / source |
| --- | --- | --- |
| `instrumental-generation` | documented | Instrumental creation and custom style controls are documented; current model/access can differ. [Source](https://help.suno.com/en/articles/2415873) |
| `song-generation` | documented | Custom original/licensed lyrics; actual singing, pronunciation and timings require listening. [Source](https://help.suno.com/en/articles/2415873) |
| `audio-download` | documented | Approved download workflow only. Formats and trial/download allocations are account-dependent. [Source](https://help.suno.com/en/articles/13926081) |
| `song-card-video` | documented | Video export is documented. Inspect whether the actual file is a lyric/song card or scene footage; MP4 is not proof of a narrative music video. [Source](https://help.suno.com/en/articles/13926081) |
| `video-cover-art` | documented | Image/video cover-art generation; release index states Pro/Premier availability. A cover loop is not a full multi-scene film. [Source](https://suno.com/release-notes/cover-art-improvements) |

**Limits:** Do not infer commercial clearance from a playable library item or current paid status alone. Retain current terms and permitted-download evidence. Use approved downloads; do not bypass limits or strip provenance/branding. Song-card export, generated video cover art, uploaded looping art and third-party full music videos are separate capabilities. Private test media and account details are not public experiment evidence.

## Google Flow Music

**Role:** music-provider. **Inputs:** .

**Style directions:** electronic, cinematic, song, instrumental, music-video.
Conversational Producer and compose controls describe music and visuals; specific style, timing and story adherence require a bounded trial. Google Flow Music is distinct from Google Flow filmmaking and Autodesk Flow Studio.

**Tested version/scope:** No public qualification record; live Lyria/Veo availability must be checked

**Licence:** Cloud service/Google terms. Plan benefits can include commercial use; do not infer a Free account grant from credits or a general product page. Input, music and visual rights require separate records.

| Feature | Evidence | Scope / source |
| --- | --- | --- |
| `instrumental-generation` | documented | Lyria music creation; requested duration/tempo is a prompt, not an exact delivery guarantee. [Source](https://www.flowmusic.app/?version=published) |
| `song-generation` | documented | Songs with dynamic vocals and lyrics are described; language/lyric alignment must be evaluated. [Source](https://www.flowmusic.app/?version=published) |
| `audio-download` | documented | MP3/WAV/M4A downloads listed; inspect the actual approved export. [Source](https://www.flowmusic.app/pricing?plan=monthly) |
| `music-video-generation` | documented | Veo-backed music videos are advertised; inspect account entitlement, clip length, credits, storyboard and final export. [Source](https://www.flowmusic.app/?version=published) |
| `song-card-video` | unknown | A video/download menu does not establish which picture treatment is produced. Classify an actual export first. [Source](https://www.flowmusic.app/pricing?plan=monthly) |
| `stem-export` | documented | Stem downloads listed; not qualified in the public catalogue. [Source](https://www.flowmusic.app/pricing?plan=monthly) |

**Limits:** Inspect actual account credits/model/plan before generation; no purchasing or upgrade authority is implied. Do not treat the Producer chat response as proof of generation, rights, export success or account entitlement. A music-driven generative scene needs deterministic finishing for exact typography, UI facts and reliable logos. Cloud uploads/outputs may be retained and reviewed under the privacy notice. Private microtests do not promote the public catalogue to tested_for_scope.

## AI Video Storyboard / Framewright adapter

**Role:** preproduction. **Inputs:** brief.

**Style directions:** cinematic, editorial, paper-collage, minimal.
Shared visual-language planning across shots; style labels are creative targets, not proof of a renderer effect. Framewright adapts the pattern to existing UI, artwork and authored graphics.

**Tested version/scope:** Upstream 93f8a6d6935858bc4acd7ff3bbea2411edf88caa: 3/4 strict Codex text-only cases after grading-context repair; missing explicit pre-render storyboard approval handoff retained. Original adapter addresses the handoff; its routing is checked separately. No rendered media tested.

**Licence:** MIT declared in upstream README and SKILL; no standalone LICENSE at inspected revision. Original Framewright adapter links upstream without vendoring its code/skill. Provider and asset rights remain separate.

| Feature | Evidence | Scope / source |
| --- | --- | --- |
| `shot-list` | documented | Text-only preproduction: coordinated shot purposes, timing and per-shot instructions; use references/storyboard.md, not picture-chain export. [Source](https://github.com/aicontentskills/ai-video-storyboard-skill/blob/93f8a6d6935858bc4acd7ff3bbea2411edf88caa/SKILL.md) |
| `visual-consistency-plan` | documented | Plan shared palette, lighting, lens/motion and recurring assets; no guarantee of generated visual continuity. [Source](https://github.com/aicontentskills/ai-video-storyboard-skill/blob/93f8a6d6935858bc4acd7ff3bbea2411edf88caa/SKILL.md) |
| `post-production-plan` | documented | Plan transitions, audio/caption roles, export targets and QA. Does not execute editing or export. [Source](https://github.com/aicontentskills/ai-video-storyboard-skill/blob/93f8a6d6935858bc4acd7ff3bbea2411edf88caa/SKILL.md) |

**Limits:** Not a renderer, image generator, audio generator or editor; never selected as a picture provider by plan.py. Upstream references directory is absent. Fixed five-second pacing, 1080p and synchronized-audio suffix are defaults that explicit user constraints override. Plan-only trials cannot qualify generated continuity, actual duration/sync, native export or provider costs.

## Authored Three.js scene + Hyperframes

**Role:** renderer. **Inputs:** object, book-art, brand.

**Style directions:** miniature-diorama, low-poly, staged-3d.
A miniature world with purposeful object action and camera travel. Owner found this pilot more interesting than the preceding basic montage; not a comparative quality benchmark.

**Tested version/scope:** Three.js0.186.1 inside Hyperframes0.8.161; Spot-Market20s1080p30 pilot

**Licence:** Original adapter and Three.js MIT; Hyperframes CLI Apache-2.0. Inspect GSAP, fonts, cover and model terms separately; no paid/cloud account used.

| Feature | Evidence | Scope / source |
| --- | --- | --- |
| `staged-3d` | tested | One authored low-poly grain/truck/port miniature; planned loading, delivery and quote-to-benchmark action. [Source](https://github.com/markoblogo/framewright/blob/7d8a326de3bd6e6bfb1fbd243155b6ad61b24952/experiments/2026-10-15/spot-market-3d-miniature.md) |
| `object-3d` | tested | Actual Three.js geometry and uncropped cover texture on a volumetric book; no arbitrary mesh generation. [Source](https://github.com/markoblogo/framewright/blob/7d8a326de3bd6e6bfb1fbd243155b6ad61b24952/experiments/2026-10-15/spot-market-3d-miniature.md) |
| `object-motion` | tested | 22 grain meshes, route-following truck and converging quote tickets; illustrative choreography, not calibrated physics. [Source](https://github.com/markoblogo/framewright/blob/7d8a326de3bd6e6bfb1fbd243155b6ad61b24952/experiments/2026-10-15/spot-market-3d-miniature.md) |
| `camera-travel` | tested | Deterministic establishing, loading closeup, truck tracking and closing-book camera poses; not ray-traced optics. [Source](https://github.com/markoblogo/framewright/blob/7d8a326de3bd6e6bfb1fbd243155b6ad61b24952/experiments/2026-10-15/spot-market-3d-miniature.md) |
| `scene-timeline` | tested | Absolute-time renderAt(t), paused GSAP timeline; repeated 8s seek matched state and pixels in the pilot environment. [Source](https://github.com/markoblogo/framewright/blob/7d8a326de3bd6e6bfb1fbd243155b6ad61b24952/experiments/2026-10-15/spot-market-3d-miniature.md) |
| `video-export` | tested | Hyperframes owns H2641080p30/600frames/20s native MP4; final AAC mix checked. Other durations/content need their own QA. [Source](https://github.com/markoblogo/framewright/blob/7d8a326de3bd6e6bfb1fbd243155b6ad61b24952/experiments/2026-10-15/spot-market-3d-miniature.md) |

**Limits:** Authored geometry and staging are required; a book cover is not an automatic 3D reconstruction. Only the20s horizontal1920x1080/30fps pilot is tested; other canvases/fps downgrade feature evidence. No calibrated physics, historical reconstruction, live market data, arbitrary imported models, native still, transparency, vertical export or cross-GPU reproducibility qualified. Hyperframes owns rendering; no unrelated Anatomy/Flute/Remotion execution is implied. Kokoro and FFmpeg supply voice/audio/encoded stills as separate layers. New multi-tool combinations require encoded integration QA. Technical QA and owner preference do not prove agent routing or audience performance.

## ManimGX + FFmpeg timing adapter

**Role:** renderer. **Inputs:** brand, data, book-art.

**Style directions:** technical-diagram, editorial-diagram.
Readable vector workflow/action/role diagrams. This pilot did not test 3D,scientific plots or aesthetic superiority.

**Tested version/scope:** ManimGX0.1.1 on Python3.14.5,FFmpeg normalisation;MN7R20s pilot

**Licence:** MIT engine;bundled fonts/x264/FFmpeg components retain their own terms. Owner cover not redistributed.

| Feature | Evidence | Scope / source |
| --- | --- | --- |
| `workflow-diagram` | tested | Scattered labelled cards align,connect and reveal roles/AI support;illustrative,no live data. [Source](https://github.com/markoblogo/framewright/blob/main/experiments/2026-10-15/mn7r-manim-mlx.md) |
| `scene-timeline` | tested | 20s absolute scene timeline;21native storyboard samples and encoded stages inspected. [Source](https://github.com/markoblogo/framewright/blob/main/experiments/2026-10-15/mn7r-manim-mlx.md) |
| `typography` | tested | Bundled sans-serif text and genuine cover import,layout checked. [Source](https://github.com/markoblogo/framewright/blob/main/experiments/2026-10-15/mn7r-manim-mlx.md) |
| `video-export` | tested | Qualified adapter includes mandatory FFmpeg CFR/timestamp normalisation and encoded QA;native VFR direct mux warned. [Source](https://github.com/markoblogo/framewright/blob/main/experiments/2026-10-15/mn7r-manim-mlx.md) |
| `native-mux-timing` | failed | Native VFR direct-mux Invalid DTS warnings;do not stream-copy this pilot without adaptation. [Source](https://github.com/markoblogo/framewright/blob/main/experiments/2026-10-15/mn7r-manim-mlx.md) |

**Limits:** FFmpeg timing adapter required for this qualified path;native standalone timestamp compatibility is not qualified. Only20s1080p30 2D workflow promo tested;3D/math plots,other formats,native still and unrelated data inputs need new scoped checks. Setup snapshot exceeded planned2GB before task-cache cleanup;no cold-install speed or general portability claim. Owner accepted basic infographic style;separate voice review and audience outcomes remain pending.

## MLX-Audio — scoped Kokoro English voice

**Role:** voice. **Inputs:** .

**Style directions:** narrated, neutral.
Tested am_michael English model/runtime only;not all MLX-Audio models or languages.

**Tested version/scope:** MLX-Audio0.5.9,Kokoro82M MLX weights,Python3.12.13,speed1.03;MN7R20s pilot

**Licence:** MIT library,Kokoro model Apache-2.0;exact voice/NLP/model terms separate,no cloning or paid service.

| Feature | Evidence | Scope / source |
| --- | --- | --- |
| `narration` | tested | Five local English phrases;18.15s speech,last end19.525s;no retiming. Listening pending. [Source](https://github.com/markoblogo/framewright/blob/main/experiments/2026-10-15/mn7r-manim-mlx.md) |

**Limits:** Ukrainian is unsupported by this tested profile;choose and review another exact model before that experiment. Local model-directory naming affects type detection;explicit English spaCy package setup required in this environment. Audio environment approximately1.2GB plus~327MB voice weights;first pipeline/phrase init68.649s,subsequent phrases0.966–1.618s;not a speed comparison. No singing,diarization,cloning,other voices/languages or arbitrary models qualified.

## Piper — Tetiana Ukrainian voice

**Role:** voice. **Inputs:** .

**Style directions:** narrated, neutral.
Exact Ukrainian female voice; one short promotional script,not singing or cloned identity.

**Tested version/scope:** Piper1.4.2,ONNXRuntime CPU,Python3.12.13;Tetiana model42be6e3f72a7c6042271236b94e48edffd1f0c63

**Licence:** GPL3 engine;exact voice card declaresApache2.0;dataset provenance linked by author,not independently audited;no engine/weights redistributed.

| Feature | Evidence | Scope / source |
| --- | --- | --- |
| `narration` | tested | Technical synthesis/integration tested:five Ukrainian lines in24s promo. Owner found this exact voice weak:unnecessary pauses,wrong stress and intonation. Technical tested status is not a voice-quality endorsement. [Source](https://github.com/OHF-Voice/piper1-gpl) |

**Limits:** Owner reports broken rhythm,unnecessary pauses,stress/intonation errors in this exact version. Retained as low-quality explicit fallback to Supertonic3;never silently substitute. Existing film unchanged;do not generalize to all Piper voices. No EN/FR,singing,voice cloning or arbitrary Piper voices qualified. ONNXRuntime emitted telemetry/cache-ID persistence warnings;no external voice API called;network traffic not independently audited. One script/voice integration,not general language quality;native Remotion raster repeat differed slightly and full-export browser workarounds were required.

## Supertonic3 — owner-recommended Ukrainian voice

**Role:** voice. **Inputs:** .

**Style directions:** narrated, neutral.
Local stockM1/F1;owner slight preferenceF1 after same-text Ukrainian probe. Naturalness is owner-assessed,not a universal quality score.

**Tested version/scope:** SDK1.3.1,ONNX CPU,Python3.12.13;model3cadd1ee6394adea1bd021217a0e650ede09a323

**Licence:** SDKMIT;weightsBigScienceOpenRAIL-M,including explicit machine-generated-content disclosure;no cloning or redistribution.

| Feature | Evidence | Scope / source |
| --- | --- | --- |
| `narration` | tested | M1/F1 short UK probes owner-accepted;defaultF1(slight subjective preference). First24s F1 video integration passed encoded checks,accepted intro reused,new title/CTA generated;final-film listening pending. Residual pause/stress errors known. [Source](https://huggingface.co/Supertone/supertonic-3) |

**Limits:** M1/F1 short-script probes and one24s F1 film integrated;longer/new scripts and other voices need QA. Final film owner listening remains pending. Owner reports residual pauses and2–3 stress errors;intonation good. F1 preference is slight and subjective. Other upstream-documented languages are not locally qualified by this profile. No singing,cloning or other stock voices tested. Model output requires explicit synthetic/AI-generated disclosure;licence restrictions still apply.

## PySceneDetect

**Role:** analysis. **Inputs:** video.

**Style directions:** .
Encoded hard-cut analysis;does not choose a visual style or create footage.

**Tested version/scope:** 0.7.2 with OpenCV5.0.0.93

**Licence:** BSD-3-Clause;OpenCV/build dependencies have separate terms

| Feature | Evidence | Scope / source |
| --- | --- | --- |
| `hard-cut-detection` | tested | 4/4 exact authored cuts in one15s1080p30 promo;not general scene understanding or semantic editing. [Source](https://www.scenedetect.com/docs/latest/api/detectors.html) |

**Limits:** Existing encoded video required;not a picture renderer. Only retained authored hard-cut fixture and same-input helper replay tested;fades,complex footage and blind generalisation unqualified.

## Source freshness

Immutable repository README links retain the reviewed revision. Live documentation
links describe upstream capability on the review date, not a test of the pilot
runtime. Refresh the registry before depending on a changed external contract.
