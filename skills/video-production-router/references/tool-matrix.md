# Tool capability matrix

Generated from `tools.json`; reviewed 2026-10-14.

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

**Style directions:** editorial, kinetic, minimal, data-motion.
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

## Source freshness

Immutable repository README links retain the reviewed revision. Live documentation
links describe upstream capability on the review date, not a test of the pilot
runtime. Refresh the registry before depending on a changed external contract.
