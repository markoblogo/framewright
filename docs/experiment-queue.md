# Proposed experiment queue

Updated 2026-10-14. This is a prioritised backlog, not a schedule or permission to
install, spend credits, upload assets or run autonomous jobs. Use authorised ABVX
products or distributable demo assets. Declare success criteria before each run;
retain failures, costs and human review separately. No new release is planned for
this batch of research. [Source comparison](related-work.md).

| Order | Experiment / why next | Bounded input and success gate | Resources / stop boundary |
| --- | --- | --- | --- |
| 0 | **Router transfer evaluation** — check unseen requests beyond the retained planning suite | The [v3 development run](router-evaluation.md) passes 52/52 with 22/22 fresh controls; earlier first-exposure 9/12 remains historical. Freeze another genuinely unseen set before extending scope; assess tool choice, explicit preferences, evidence, budget and comparison-only stopping; retain decisions and tool traces | Approve a model/runtime budget; no real infrastructure or public uploads. Do not extend current planning qualification to unseen or privileged scopes without matching evidence |
| 1 | **librosa + PySceneDetect** — music/video cue sheets in both directions | One authorised 10–15 s audio excerpt and one fixed clip; compare detected onset/beat and cut candidates with manual annotations, declare tolerance before running; produce JSON cue sheet + edited microclip | Isolated local environment on Work; no model download initially. Distinguish beat errors from useful cut detection; record timing/memory and false positives |
| 2 | **WhisperX lyric alignment** — readable song words at the right time | One 10 s English sung excerpt with known original lyrics; compare word timestamps and omissions against listening; export reviewed captions | Review exact ASR/alignment model licences and sizes first; no diarisation or voice cloning needed. Do not equate speech alignment with singing success |
| 3 | **ACE-Step 1.5** — bounded local alternative to cloud music | After hardware preflight, one short instrumental and, if feasible, one original-lyric excerpt; compare intelligibility, cadence, control and real render time | Record Mac backend, free memory/storage and weight terms before download; agree model-size ceiling. Stop if the machine cannot support it; no advertised CUDA speed claims |
| 4 | **ViMax storyboard/checkpoint pilot** — test continuity and resumability | Two shots for one authorised product; approve references/animatic, interrupt one stage, resume without regenerating accepted shots; record actual calls/cost | Inspect provider requirements and set an explicit generation cap first. Borrow the stage contract even if execution is unsuitable; do not enable an unattended paid pipeline |

## Conditional / deferred

**Shipvideo / LaunchVideo** ([source](https://github.com/diggerhq/shipvideo)) is a
new research candidate, not installed or tested here. README describes URL/prompt
→ HTML → OpenComputer Chromium/FFmpeg. It requires cloud runtime/account review;
its current scene restrictions exclude audio, embedded video and external images.
Inspect the exact code/licence, cost controls and source-fact checks before a
future bounded comparison with Brag/Hyperframes. No cloud deployment is authorised
by adding this bookmark.

**Editly** is worth a small comparison only when the existing FFmpeg/Remotion
assembly contract has a concrete missing function. Test that it preserves locked
music duration and sync before adding another assembler.

**LTX-2** stays deferred until exact model licensing, hardware and download budget
are resolved. Joint audio/video is interesting but not a reason to fill Work with
large unqualified weights.

**Flow Music / Suno** remain documented music providers. Private account probes
are deliberately excluded from public experiment records and qualification. Future
public tests need separately authorised, redistributable inputs/evidence. Evaluate
generation, approved download, native-video class, quality and use rights as separate
checks. An account limitation does not make the entire service technically unavailable.

## Graduation rule

Research → candidate → bounded trial → retained evidence → narrowly qualified
capability. Failed, unknown and documented functions remain separate. A library's
output does not prove the router chooses it correctly; a successful private test
does not grant public sharing or qualify a new chain. Do not start the next queue
item automatically when the current one finishes.
