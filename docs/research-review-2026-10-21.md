# Creative tools and owner-voice research — 2026-10-21

Primary-source review for Pocket OS, later fiction/world footage and reusable narration.
No tool installation, model download, account access, voice upload, generation or paid
call was performed. All twelve additions are **candidate** records, not tested routes.
Priorities below are editorial recommendations, not upstream performance claims.
[Queue](experiment-queue.md) · [Media review](../skills/video-production-router/references/media-review.md).

## Start with the nearest production need

1. Pocket OS: compare one short TerminalTextEffects title with an ASCII-treated
   Three.js object. Keep actual device and Mac UI captures readable and identifiable.
2. Owner voice: assess local Qwen3-TTS Base resources, then one short clone comparison;
   keep Chatterbox/OpenVoice as alternatives and ElevenLabs as an optional cloud baseline.
3. Media review: run a separate known-defect video pilot before relying on an automatic
   quality reviewer. ASR, scene cuts and technical measurements are already scoped tools;
   continuous semantic/temporal video assessment remains untested.
4. Add Blender or postprocessing only when a storyboard needs a specific shot/effect.
   Motion Canvas, Chafa and agg are optional helpers, not mandatory new dependencies.

## ASCII, animation and effects shortlist

| Candidate / primary source | Useful scope | Terms and integration limits | First bounded trial |
| --- | --- | --- | --- |
| [TerminalTextEffects](https://github.com/ChrisBuilds/terminaltexteffects) | Animated terminal typography, decrypt/build transitions; Python iterators yield text frames | MIT; no native MP4 export assumed. Needs fixed font/grid/fps and retained frame sequence | 5–8s Pocket OS title; seed randomness where available; replay frames at fixed times and check encoded legibility |
| [Three.js AsciiEffect](https://threejs.org/docs/pages/AsciiEffect.html) | Turn a 3D object/camera view into ASCII | MIT Three.js/addon notices; outputs a DOM element rather than the original canvas. Pin matching core/addon versions. Existing Three.js qualification does not qualify this effect | Same 5–8s object/camera move with and without ASCII; verify actual capture surface, glyph scale and seek/replay |
| [Chafa](https://github.com/hpjansson/chafa) | Authorised device photos/images converted into terminal art | LGPLv3+ library and CLI; default Unicode/terminal protocols are not necessarily ASCII. Verify strict character-set/output flags before use | One owner image, fixed text dimensions and font; inspect silhouette and export path. Use only if image-to-ASCII is needed |
| [agg](https://docs.asciinema.org/manual/agg/usage/) | Retained terminal cast to GIF, useful for authentic CLI demonstrations | GPLv3+; source cast capture tool has separate terms. Speed/idle caps can retime footage; GIF is not an MP4 master or physical-device recording | One short local cast, explicit timing/font/geometry, then existing video assembly; no public cast upload |
| [Blender](https://github.com/blender/blender) | Device diagrams, animated cameras, lights and later virtual-set shots | GPLv3 application with file-specific notices; imported models/fonts/media need separate rights. Headless workflow and Mac render cost still need a trial | One original simple 5s device silhouette/camera shot; label illustrative geometry and preserve real UI footage |
| [pmndrs/postprocessing](https://github.com/pmndrs/postprocessing) | Bloom, noise, scanlines, glitch; documented GPU ASCIIEffect is another candidate approach | Zlib plus retained original MIT notices; requires compatible Three.js. Colour/tone-mapping and effect time must be explicit | One 5s restrained CRT treatment, clean reference alongside it; verify readability and replay. Compare GPU ASCII only if DOM route fails or costs too much |
| [Motion Canvas](https://motion-canvas.io/docs/plugins/) | Scripted explanations, diagrams, timeline-led product animation | MIT core; Node/Vite/browser editor and exporter integration. FFmpeg exporter documented; unattended CLI rendering not established here | One 6–8s concept diagram only when existing renderer does not cover it; inspect export/replay before integration |
| [DeepFilterNet](https://github.com/Rikorose/DeepFilterNet) | Speech noise suppression before editing or clone preparation | Code dual MIT/Apache-2.0; exact selected pretrained-weight terms remain unresolved in this review. Mac support documented, local runtime untested. Not a pronunciation repair or listening model | Only for a genuinely noisy 10s owner sample, after weight terms/resource check; original/processed listening comparison, consonants and delay preserved |

ASCII is an illustrative layer, not permission to invent Pocket OS functions. Obtain
real Cardputer and Mac footage through the existing intake. Avoid making every screen
an effect demonstration. A frame-producing library still needs timeline and encoded QA.

## Clone the owner's voice for repeatable narration

| Candidate | What was verified in primary documentation | First use and remaining questions |
| --- | --- | --- |
| [Qwen3-TTS Base 0.6B](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-Base) | Reference-audio cloning; Apache-2.0 model card. EN/RU/FR among ten documented languages; Ukrainian and Toki Pona absent | First local candidate. Exact runtime/model revision, storage and peak memory must fit this Mac. CUDA quickstart is not Apple Silicon qualification. Base is the clone model; CustomVoice is a separate preset-voice scope |
| [Chatterbox Turbo](https://huggingface.co/ResembleAI/chatterbox-turbo) | English 350M reference-voice TTS; MIT model card; laugh/chuckle tags. [Code](https://github.com/resemble-ai/chatterbox) MIT | Alternative for expressive English narration. Mac speed/quality unmeasured; retain built-in watermark. Other Chatterbox models/languages are separate tests |
| [OpenVoice V2](https://github.com/myshell-ai/OpenVoice) | Authors identify V1/V2 as MIT, including commercial use; V2 lists EN/ES/FR/ZH/JA/KO | Tone-colour conversion with base TTS, not a single standalone text-to-clone model. Check exact base voice/converter weights and their terms; multi-stage quality/cost makes it a second-line local candidate |
| [ElevenLabs Instant Voice Cloning](https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/instant-voice-cloning) | Cloud clone workflow; [API](https://elevenlabs.io/docs/api-reference/voices/ivc/create) returns a voice ID. Guidance recommends about 1–2min clear consistent audio | Optional cloud comparator. Account, eligible feature/model, price and storage/data settings uninspected. Specific voice files/destination and budget must be agreed before upload. [Commercial use](https://help.elevenlabs.io/hc/en-us/articles/13313564601361-Can-I-publish-the-content-I-generate-on-the-platform) needs eligible paid generation; free and Beta output excluded from commercial production under reviewed terms |

The previous live narration recordings are possible source material, not a selected
clone reference or cloud-upload grant. Choose a clean, consistent passage with an
accurate transcript. Retain the untouched take. Do not use aggressive cleanup by default:
it can alter voice texture. No claim that a short reference guarantees likeness,
fixes the owner's accent, or validates a new language.

Suggested first fixture: a clean owner reference plus 8–12s of new English narration
containing Pocket OS, Cardputer, ordinary sentences and a number. Compare generated
and live readings at matched listening level. Record owner ratings for identity,
naturalness, pronunciation and delivery; also omissions/repetitions, elapsed synthesis,
peak resources, duration, clipping and sync. ASR can flag words, not approve likeness
or pronunciation. Stop after one corrected retry if the result remains unsuitable.
No cloning or benchmark is started by this plan.

If accepted, a future reusable **voice profile** should retain private reference hash,
consent/use scope, exact engine/model/terms, language, settings and approved example.
Scene text → cached narration WAV → timing/alignment → music mix → reviewed output.
Cache invalidation must include script, voice reference, model and settings. A saved
profile is a proposal for later development, not a newly implemented product feature.

## Understanding and assessing media: current boundary

Existing evidence: FFmpeg/ffprobe measures files; agent image inputs support review
of actually shown frames; PySceneDetect recovered four authored hard cuts in one
pilot; mlx-whisper has correction-dependent clean-English transcription/timing trials.
None proves general video semantics, continuous motion, lip sync or creative quality.
[Gemini audio/video](https://ai.google.dev/gemini-api/docs/video-understanding),
[Qwen3-Omni](https://github.com/QwenLM/Qwen3-Omni) and
[Claude Video](https://github.com/bradautomates/claude-video) remain untested candidates.

Proposed first video test: a non-private 10–15s original control with known actions,
plus separately labelled freeze/black interval, missing action, displaced sound and
an ambiguous valid cut. Ask timestamped findings and uncertainty; compare against
labels and human playback, including false positives. Record actual bytes/modality,
covered intervals, sampling and reviewer version. Frame-sheet analysis qualifies
only sampled visual findings; it cannot pass a continuous-video/audio test. Gemini
needs destination/account/budget approval; local Qwen needs resource preflight.
Keep model findings separate from technical QA and owner acceptance.

## Filtered or deferred

- [F5-TTS](https://github.com/SWivid/F5-TTS): MIT code, but reviewed default pretrained
  weights are CC-BY-NC. Exclude those weights from monetised YouTube narration unless
  a separately licensed model/grant is selected; this is a rights gate, not a failed test.
- [Natron](https://github.com/NatronGitHub/Natron): GPL-2.0 compositor, possible future
  masking/keying task. Defer because a concrete compositing gap and native Apple
  Silicon route are not established; avoid another full editor during Pocket OS intake.
- Existing tested Supertonic/MLX-Audio, Three.js and assembly routes remain usable
  within retained scopes. New voice models, cloning and effects do not inherit them.
- World creation remains a separate owner-selected Marble-first intake. This research
  does not start a world-provider generation or resume paused SSI production.

## Discovery and evidence

The twelve candidates have review-ledger/facet records, without automatic planner
profiles. They are visible with `--evidence any`; tested/default documented searches
must not silently promote them. Candidate style tags are not indexed by the current
style filter: use a query or explicit tool ID. Examples:

```sh
python3 skills/video-production-router/scripts/search.py --query ascii --evidence any
python3 skills/video-production-router/scripts/search.py --task narration --tool qwen3-tts --language en --evidence any
python3 skills/video-production-router/scripts/search.py --task media-review --evidence any
```

Retained GitHub source revisions inspected for this review follow. These are research
pins, not installed/tested versions. Model-weight revisions must be pinned separately
before an actual download; live hosted-service docs describe the review date only.

| Source | Inspected revision |
| --- | --- |
| [ChrisBuilds/terminaltexteffects](https://github.com/ChrisBuilds/terminaltexteffects/tree/b75a7baefe89a25d22754bcefb7d5caae8809477) | `b75a7baefe89a25d22754bcefb7d5caae8809477` |
| [NatronGitHub/Natron](https://github.com/NatronGitHub/Natron/tree/3763d805d7d277d10af10025ae41af677682b3e6) | `3763d805d7d277d10af10025ae41af677682b3e6` |
| [QwenLM/Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS/tree/022e286b98fbec7e1e916cb940cdf532cd9f488e) | `022e286b98fbec7e1e916cb940cdf532cd9f488e` |
| [Rikorose/DeepFilterNet](https://github.com/Rikorose/DeepFilterNet/tree/d375b2d8309e0935d165700c91da9de862a99c31) | `d375b2d8309e0935d165700c91da9de862a99c31` |
| [SWivid/F5-TTS](https://github.com/SWivid/F5-TTS/tree/2f866649b779881af8bd644e76b9a6d95053da29) | `2f866649b779881af8bd644e76b9a6d95053da29` |
| [asciinema/agg](https://github.com/asciinema/agg/tree/aae34b012382536c8c01c753e4b609424642a06d) | `aae34b012382536c8c01c753e4b609424642a06d` |
| [blender/blender](https://github.com/blender/blender/tree/2858241a2b1fa67e173d4af6b3ff4f7fbd5a9ec2) | `2858241a2b1fa67e173d4af6b3ff4f7fbd5a9ec2` |
| [hpjansson/chafa](https://github.com/hpjansson/chafa/tree/413b76e4ddefc3875b5220c68a328651f235d3ae) | `413b76e4ddefc3875b5220c68a328651f235d3ae` |
| [motion-canvas/motion-canvas](https://github.com/motion-canvas/motion-canvas/tree/7b91435c301d530351dcf5ebb91dd139c002e405) | `7b91435c301d530351dcf5ebb91dd139c002e405` |
| [mrdoob/three.js](https://github.com/mrdoob/three.js/tree/560f66427a4c3012e621fc9c6c1ec80b76a906ab) | `560f66427a4c3012e621fc9c6c1ec80b76a906ab` |
| [myshell-ai/OpenVoice](https://github.com/myshell-ai/OpenVoice/tree/74a1d147b17a8c3092dd5430504bd83ef6c7eb23) | `74a1d147b17a8c3092dd5430504bd83ef6c7eb23` |
| [pmndrs/postprocessing](https://github.com/pmndrs/postprocessing/tree/9cf03cff26615636a564d8bfddf765edb8917441) | `9cf03cff26615636a564d8bfddf765edb8917441` |
| [resemble-ai/chatterbox](https://github.com/resemble-ai/chatterbox/tree/5de7a54aa4e5e2baadb0182dde554908b48b85c2) | `5de7a54aa4e5e2baadb0182dde554908b48b85c2` |

No new export, release, model-quality evaluation or audience outcome is claimed.
