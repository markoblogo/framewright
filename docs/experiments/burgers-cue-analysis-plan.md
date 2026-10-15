# Burgers, Lipstick & Underwear — proposed cue-analysis pilot

Execution update,2026-10-15: [completed pilot and retained limitations](../../experiments/2026-10-15/burgers-cue-analysis.md). The text below is the original pre-execution plan, preserved without relaxing its criteria.

Original status: owner selected the book and requested English narration. Planning only;
no tools installed, audio generated, media rendered or capability promoted.

Source: [book page](https://abvx.xyz/books/burgers-lipstick-underwear).
Owner supplied a promotional image locally; it is not copied into this repository.
The page describes everyday economic indicators and their interpretation. Avoid
invented sales, reviews, predictive accuracy or investment recommendations.

## Why these tools next

[librosa](https://github.com/librosa/librosa/releases/tag/1.0.0) supplies onset and
beat candidates; [PySceneDetect](https://github.com/Breakthrough/PySceneDetect/releases/tag/v0.7.2)
supplies picture-cut candidates. They complement the existing renderer/FFmpeg chain.
Neither makes a film, writes a soundtrack or judges whether an edit tells the story.
Upstream research checked 2026-10-15: librosa 1.0.0 (ISC), PySceneDetect 0.7.2
(BSD-3-Clause); recheck exact distribution/dependency terms before installation.
[Onsets](https://librosa.org/doc/1.0.0/auto_tutorials/01-intro/05-onsets.html)
are note/transient beginnings, not necessarily beats or downbeats.
[Detectors](https://www.scenedetect.com/docs/latest/cli.html) distinguish sharp cuts,
adaptive content changes and threshold fades; camera movement can cause false cuts.

## Proposed creative treatment

Horizontal 1920×1080, 30 fps, approximately 15 seconds. Editorial, tactile,
warm cream/black with restrained red accents, drawn from the supplied book image.
English narration, calm with a little dry humour; no finance-ad urgency.
The source promotional image is one flattened image, not layered artwork. Isolating
objects requires a reviewed crop or separately approved assets, not assumed 3D data.

| Proposed time | Picture / text | Narration |
| --- | --- | --- |
| 0–3 s | Burger detail, then lipstick detail; restrained reframing | “Burgers. Lipstick. Underwear.” |
| 3–6 s | Third detail; tidy indicator-like typography, no invented market values | “Strange clues to the economy.” |
| 6–9 s | Visual pause; question on screen | “But what do they really tell us?” |
| 9–12 s | Pull back to full supplied promotional image | “Discover the stories behind everyday indicators.” |
| 12–15 s | Readable book title and short ABVX destination | “Burgers, Lipstick & Underwear. Explore the book at ABVX.” |

This is proposed copy, not a quotation from the book. The 29-word narration must
be timed by listening before picture lock; extend duration if needed rather than
speeding speech or shortening the title hold automatically.

Music directions to choose before execution: (A) sparse brushed-percussion/bass
groove, (B) restrained piano/percussion editorial pulse, (C) minimal electronic
pulse. A is the initial recommendation: clear accents without masking narration.
Use an owner-approved track or authorised original audio. Record source, permitted
use, exact excerpt and hash; availability of a provider is not rights clearance.
Local Kokoro is a voice candidate from prior workflow, not a completed voice test
for this script. Confirm pronunciation, model/voice terms and local dependencies.

## Bounded test, after storyboard/music approval

1. Freeze music alone, voice alone and the picture edit separately. The analyzer
   should use the music stem, not mistake spoken consonants for musical accents.
   Annotate three intended musical accents by listening and three chosen hard cuts
   by frame inspection **before** detector output is viewed.
2. Run local analysis in an isolated Work environment. No model downloads or cloud
   calls are needed by these two analysis libraries. Installation/storage ceiling:
   1 GB and 10 minutes; stop and report if exceeded. No service subscription.
3. Retain JSON/CSV onset, beat and cut candidates, parameters, versions, inputs,
   wall time and false positives. One initial parameter set and at most one labelled
   adjustment; retain both. No silent threshold tuning to obtain a passing result.
4. Acceptance proposal: match each of three predeclared hard cuts within one decoded
   frame; match at least two of three audible target accents within 100 ms. Report
   precision/recall and individual deviations; do not use a three-point result to
   claim general accuracy. A failure is useful evidence, not a reason to repeat
   indefinitely. Beat estimation is exploratory, not an acceptance substitute.
5. Human review: voice is intelligible over music, title/CTA readable, no object crop
   misleading. Only after an authorised render, verify encoded video/audio streams,
   duration, sync, complete playback and hashes using the existing QA recipe.

Expected analysis outputs: `cue-sheet.json`, `cuts.csv`, `comparison.json`,
`environment.txt` and a short findings record. Final MP4, thumbnail and YouTube copy
are a later delivery stage, not outputs of the present no-render task.
