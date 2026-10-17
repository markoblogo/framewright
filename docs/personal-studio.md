# Personal studio: next production programme

2026-10-17. Framewright is an open-source personal AI production toolkit for the
owner's YouTube, ABVX and other films. Quality and saved operator time take priority
over a commercial editor product. The existing router and renderers remain the base.
Owner clarified: **infrastructure and conditional examples now; no real recut, music
folder, model installation or film production in this pass**. No new release.

## Audit → minimum extension

| Need | Already available / reuse | Actual gap / decision |
| --- | --- | --- |
| Video inspection | FFprobe metadata, full FFmpeg decode recipes; PySceneDetect scoped hard-cut analysis | Cut detection is not semantic understanding; new source still needs transcript and human context review |
| Montage / multiple visual sources | Delivered MoviePy/FFmpeg compilation, source-audio disabling, timed overlays/crossfades | Reuse manual recipe. MoviePy remains discoverable but not an automatic planner provider |
| New scenes / typography | Scoped Remotion, Hyperframes, Three.js, storyboard preparation | New styles/seams require a bounded integration test; no universal scene generator promised |
| Voice / sound | Supertonic EN/UK, scoped Kokoro EN/FR; sound-layer and FFmpeg | Final listening, stress, sync, loudness remain output-specific; voice licence/model pins still apply |
| Captions | Authored transcript/SRT in archives; FFmpeg captions documented | Accurate ASR and word alignment not qualified; investigate one local speech candidate when needed |
| Colour / audio treatment | FFmpeg documented colour filters; recorded mixes/normalization | No new aesthetic grade qualification; approve samples/scopes and inspect encoded output |
| Facts / source rights | Existing handoff prose and source pins | Add machine-readable source/claim/EDL intake; provenance ≠ reuse permission |
| Personal music | Existing-source music planning | Add private scan/annotations/search. No semantic mood model or automatic song selection |
| Deliveries / resume | Existing project pins/manual state, independent QA | Add required stems/copy/provenance/resources to experimental checkpoints |

Implemented foundation: [shared workflow + music catalogue guide](../skills/video-production-router/references/studio-workflows.md).
Three scenarios reuse **one source, claim, edit-decision and delivery contract**.
Hybrid combines recut sources and original-scene plans; it has no separate engine.
Existing briefs without `production` keep their selection/output behavior.
These workflows enforce tested component evidence, not tested whole-chain evidence.
Every new A/B/C chain still needs its own integration test and owner confirmation.

## Focused upstream review

Reviewed official sources on 2026-10-17, no installation or model calls. Exact
candidate decisions are retained in the [review ledger](../skills/video-production-router/references/review-ledger.json).
The two new research records have no capability profiles or production eligibility.

| Tool / source | Licence and resources | Decision and concrete future test |
| --- | --- | --- |
| [FFprobe](https://ffmpeg.org/ffprobe.html) / [FFmpeg legal](https://ffmpeg.org/legal.html) | Build-dependent LGPL/GPL; media/codec issues separate. Installed 8.0.1. Catalogue default: ≤100 files, ≤200MiB/file, 120s wall; optional ≤30s audio analysis/file | Reuse installed tools. Test private indexing on generated 1s PCM only; no owner archive scan. Production trim/loop/mix recipes remain unchanged |
| [MoviePy](https://zulko.github.io/moviepy/) | MIT code; FFmpeg/fonts/media separate. Upstream inspected `211e4b15f6ce4f34a6a9efbfff40590e43a68f77`; delivered archive uses 2.2.1 | Reuse existing montage recipe for A/C. Resource cost depends on frames/layers; proposed output 15s1080p30,500MiB work cap, not a measured performance claim |
| [PySceneDetect](https://www.scenedetect.com/docs/latest/) | BSD-3-Clause; upstream inspected `217cc8c65cfd58290cff8313327fb4d6098419d5` differs from retained tested version | Keep exact retained hard-cut scope; no install/upgrade. A: compare returned cut times with manual labels; dissolves/semantic importance unqualified |
| [Whisper](https://github.com/openai/whisper) | MIT code **and weights** per upstream; revision `86098128c0b4f24f0e2aa2994de830614b474227`. tiny/tiny.en table quotes ~1GB VRAM; CPU timing, download bytes and peak RAM unmeasured here | Candidate only for ASR gap. First consider existing MLX-Whisper/Parakeet candidates; choose one exact model,15s speech/known transcript,manual word/timestamp comparison. No default turbo download |
| [auto-editor](https://github.com/WyattBlue/auto-editor/blob/066e9b7fe2fe83e28e641d647f84b6dfbeaba69f/LICENSE) | Unlicense source; packaged dependencies/build separate. CPU/FFmpeg runtime; peak RAM/time unmeasured | Existing candidate, documentation refreshed. Only if an authorised60–90s source has pauses worth cutting; freeze protected phrases, review edit list and sync. Loudness/motion cuts do not choose truthful or interesting excerpts |
| [Diffusers](https://github.com/huggingface/diffusers) + [SDXL terms](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/blob/462165984030d82259a11f4367a4eed129e94a7b/LICENSE.md) | Apache-2.0 library; CreativeML Open RAIL++-M model with use/distribution restrictions, not unrestricted OSI terms. Metadata:6,938,078,334-byte main checkpoint; this excludes dependencies/caches. RAM/VRAM unmeasured | Deferred still-generation study, not video capability. Two approved storyboard illustrations,10min cap,exact model/device/storage budget first. Use existing authored graphics for B/C until justified |

Existing LTX-2, ACE-Step, ViMax and cloud-native-video limitations remain in their
prior records. No unchanged retry. Free software does not imply free compute or
cleared footage, voices, fonts, compositions, recordings or generated likenesses.

## Predeclared A/B/C experiments — not started

All examples are **placeholders**, not licensed footage or factual scripts.
No input has been chosen and no music folder is required now. Do not search/download
random Telegram/X footage to fill these examples. A source URL is not a reuse grant.

| Trial | Inputs / method | Pass criteria | Initial declared caps / stop |
| --- | --- | --- | --- |
| A — repackaging | Owner-authorised≤60s local clip; ordered human-selected excerpts; existing MoviePy/FFmpeg; replace/remove old audio; optional library music | Source context preserved; every excerpt has reason/time range; no retained original audio when removed; readable opening/captions/thumbnail; full final decode,sync/loudness and human listening; separate rights record | 15s1080p30 output,30min operator/runtime window,500MiB work,0 downloads/paid calls. Missing permissions/materials or cap reached → stop |
| B — insight → video | Owner-selected article, dated factual claim/locator table; original script/storyboard and scoped Remotion/voice/FFmpeg | Every factual statement reviewed against source; no unsupported inference; new scenes match script; same technical/delivery checks as A; distinguish article quotation and original visuals | Same caps; unknown source/claim or required untested capability → planning only. No new model needed for authored scenes |
| C — hybrid | Reuse A source/EDL plus B fact/scene contracts; one new authored scene, titles/voice and library track | Both source and new-scene contracts; old audio absent; loop/mix/transition checks across seams; full composite QA rather than component-pass inference | Same initial caps; freeze concrete EDL and exact new-scene duration before approval. No automatic cascade of regeneration |

These limits are **declared acceptance/stop conditions**, not enforced by a renderer
supervisor. Catalogue scanning has separate implemented subprocess/file/time bounds.
Any changed brief/caps needs owner review. Current scripts do not spend, install,
render, fetch articles, select interesting moments or upload anything.

## Evidence from this infrastructure pass

Retain deterministic tests in `tests/test_studio.py`: source/rights/claim/EDL
boundaries, unchanged legacy plan behavior, experimental checkpoint gates/deliveries,
private PCM catalogue/probe/annotations, denied/unknown rights and changed bytes.
Optional FFmpeg tests skip explicitly when absent; dependency-free planning tests
still run. These are **helper tests**, not three completed production experiments,
semantic ASR evaluation or independent model qualification.
[Retained helper-test scope and commands](../experiments/2026-10-17/studio-foundation.md).

When a real experiment is selected later, use `docs/experiments.md`: preserve exact
versions/commands, source pins, failures, time/storage/memory observations, final
artifact hashes, separate technical/human QA and publication provenance. Generated
MP4/stems/thumbnail remain outside Git. Planned files, retained files and verified
files are separate states; a file hash is not a media QA result.
