# Related work and useful design ideas

Research snapshot: 2026-10-14; bounded cue-analysis follow-up2026-10-15. These are upstream source/documentation comparisons,
not blanket benchmarks or endorsements; bounded follow-ups are linked separately. Licences below describe repository
code; weights, media and paid providers can carry separate conditions. Framewright
keeps a small selection/evidence layer instead of importing another complete stack.

| Project / inspected revision | Useful idea for Framewright | Boundary / next check |
| --- | --- | --- |
| [AI Video Storyboard](https://github.com/aicontentskills/ai-video-storyboard-skill/tree/93f8a6d6935858bc4acd7ff3bbea2411edf88caa), MIT declared in README/SKILL | Shared visual language plus coordinated shots, prompts and post-production notes | Raw text trial 3/4; missing references and fixed defaults documented. Original [Framewright adapter](storyboard-adapter.md) checked 4/4 as part of the integrated suite; no upstream skill vendored or media generated |
| [ViMax](https://github.com/HKUDS/ViMax/blob/fd4b72e7731be6e5f88486206d25ea59849b0285/readme.md), MIT | Story → storyboard → reference assets → shots; per-shot checkpoints and resumable work | Adopt inspectable stages and approval before paid motion; do not copy unbounded autonomous generation or assume provider access |
| [MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo/blob/c184fccd05621d7a654b6e6ea34102a0a0de0657/README.md), MIT | Explicit script/material/voice/subtitle/music stages and custom-audio override | Preserve asset provenance and owner audio; no automatic stock collection or bulk public publishing |
| [Editly](https://github.com/mifi/editly/blob/dc46674052eacd15ef6e0f563a58eb378b3804ad/README.md), MIT | Declarative clip/layer manifest, durations, transitions and audio tracks | Useful contract pattern; its default duration fitting can retime media, so locked picture/music needs an explicit preservation check |
| [librosa](https://github.com/librosa/librosa/blob/08e2c0a20d650fe00f10aaf3a1eaa9698ac19641/README.md), ISC | Onset, tempo and beat analysis to make music-first cue sheets | [Authored-reference trial](../experiments/2026-10-15/burgers-cue-analysis.md):3/3 accents within17ms. Manual-listening annotation remains pending; no downbeat qualification |
| [PySceneDetect](https://github.com/Breakthrough/PySceneDetect/blob/7cd1005e8349d8e913d0930fc1750363eb4ddc51/README.md), BSD-3-Clause | Detect picture cuts before choosing music for a fixed video | [Same trial](../experiments/2026-10-15/burgers-cue-analysis.md):4/4 exact hard cuts, no extras. Fades and story-beat judgement remain untested |
| [WhisperX](https://github.com/m-bain/whisperX/blob/771b4a14a9486f8fd5aef18ef49e35d639523dd3/README.md), BSD-2-Clause code | Word alignment as a candidate for lyric/subtitle cues | Speech performance does not establish singing accuracy; inspect individual model licences, particularly language aligners, and compare supplied lyrics by ear |
| [ACE-Step 1.5](https://github.com/ace-step/ACE-Step-1.5/blob/ca1e85fe9430179831e6bc6be790c332190a3866/README.md), MIT code | Local music/lyrics alternative with reproducible parameters | Preflight this machine's memory, model size, runtime and exact weight terms; advertised GPU speed is not a local result |
| [LTX-2](https://github.com/Lightricks/LTX-2/blob/be6d6d0a69d11a0a399c462ed92606692e5f8697/README.md), own licence review required | Joint audio/video generation as a possible hero-shot source | Defer large downloads and hardware commitments; no claim of Mac feasibility or MIT model rights |

## Patterns worth adopting

1. **Checkpoint each shot.** Persist input revisions, intended duration, provider,
   output hash, cost and approval. Regenerate a failed shot, not an accepted film.
2. **Approve before expensive motion.** Use a low-cost storyboard/animatic with a
   fixed audio version; agree shot count and credit ceiling before generation.
3. **Mix expensive and deterministic layers.** Use selected generated hero shots
   alongside typography, real product UI, book art and inexpensive transitions.
4. **Keep overrides visible.** Owner-supplied audio, explicit renderer choice and
   locked timings survive defaults. Unknown capability/rights remains unknown.
5. **Separate source assets from delivery.** Preserve originals and native exports;
   normalise only at the declared handoff, then check the encoded master.

These are attributed design proposals, not copied upstream code or imported skills.
The planner provides explicit choices and evidence states. The new textual
[storyboard contract](storyboard-adapter.md) adds proposed/approved plan status and
per-shot tool handoffs. A resumable shot-checkpoint engine and interactive approval
interface are **not implemented**; a text contract is not such a runtime.

## Creative workflow references

Third-party guides suggest locking the track, marking sections, reviewing a
storyboard, then generating only the shots that need motion:
[Renderforest](https://www.renderforest.com/blog/turn-suno-song-into-music-video),
[Pixo](https://pixo.video/blog/ai-music-video-guide), and
[SunoMV](https://suno.bi/en/blog/suno-storyboard-to-screen-workflow-2026).
SunoMV is an independent third party, not Suno. Treat pricing, performance and
comparisons in vendor guides as claims, not evidence. Do not adopt advice to remove
required watermarks. Use [the experiment queue](experiment-queue.md) to turn ideas
into bounded tests rather than expanding the supported-tool matrix prematurely.
