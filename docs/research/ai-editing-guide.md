# AI editing guide: integration decision

Reviewed 25 October 2026. Owner supplied *Вайб-монтаж с AI-агентами. Большой
практический гайд*, Точки над ИИ / AI Camp, dated 15 October 2026, 79 pages.
Text was extracted and example pages 13, 25, 33 and 72 were inspected visually.
Source filename: `Вайб-монтаж с ИИ.pdf`. SHA-256: `340420d7a80414040804358d5f7b5497c1365d447ef13080df632ee7437a20e2`.
The PDF remains outside the repository; no licence to redistribute the complete
publication was established. This module uses an original implementation and
paraphrased process, not copied upstream skill/code or the guide's prompt collection.

## Selected, authorised scope

Owner authorised items 1–3: inspect/choose source material; preserve source/output
time maps and retime cues; create bounded review clips around joins. Implemented
as `editing.py` plus the router's optional [editing module](../../skills/video-production-router/references/editing.md).
It extends existing project/material/journal and studio-workflow concepts.

The guide also discusses template extraction, revisions, cloud editors, TTS and
provider setup. Those are outside this implementation. Existing Remotion,
HyperFrames, FFmpeg and project evidence features are reused; no new provider or
third-party skill was installed. API/model names, commercial terms and commands in
the guide are dated assertions, not newly verified runtime integrations.

## Behaviour verification

`tests/test_editing.py` exercises the public CLI using local generated PCM and
FFV1/color/tone fixtures. It covers source hashes and no overwriting; absent content
review; cut intervals; reordered/repeated passages; removed/clipped cues; SRT guards;
overlay retiming; stale source/map rejection; audio-only joins; differently shaped
video with/without audio; playable exports, boundary picture/color and audio/silence.
No external ASR, natural speech or semantic judgement is evaluated by those tests.

A local FFmpeg8.0.1 run stalled on a short FFV1/PCM proxy with automatic filter
threading. The failed run and timeout were observed. The small-proxy route was
changed to bounded decoder/filter/encoder threading and bounded padding; a targeted repeated
reproduction completed. The test is a regression check, not a broad FFmpeg claim.

## Next production use

On the next owner-authorised footage-based production, choose one 30–60s excerpt
with a repeated take or pause. Supply corrected source-time transcript separately;
compare an actual edit with the original. Confirm word edges by listening, preserve
qualifications, inspect cut continuity and compare final subtitles to final audio.
Record measured setup/review effort and actual owner acceptance in that project's
journal. Do not reopen paused Pocket OS work merely to exercise this helper.

A non-frame-aligned synthetic review also exposed timestamp-based last-frame loss
and a one-frame picture/audio boundary offset. Frame-index sampling and a zero-based
CFR grid corrected them; regressions check the image immediately before/after the
reported cut. Source handles are trimmed before finite proxy padding. Review-proxy
padding is explicit and must not be confused with an edit to the final film.

## Local check result

Final targeted run: 9 public-CLI tests passed, including encoded audio and exact
before/after-cut color assertions at non-frame-aligned source times. Full offline
check: 320 tests passed (1 skipped), retained router/storyboard evidence integrity,
local documentation links, tool-matrix consistency and standalone package smoke
passed. No model calls or release publication. Synthetic normalized 0.75s proxy
was inspected as a four-frame sheet; waveform shows retained tone then declared
silence. Full natural-speech listening and editorial production remain unperformed.

## Revision and template extension

Owner subsequently authorised guide items 4–5 (pp.33,58,72): exact requests, context comparisons and preservation verification through the existing journal; accepted-film design contracts with independent typed content and three boundary cases. Original implementations are `revisions.py` and `templates.py`; no upstream code or prompt collection was copied. Rendering the comparison proxies is exercised with synthetic audio/video. Template checks validate data/layout selection; they do not qualify an actual renderer or typography.

## Closeout checks for items 4–5

Six revision CLI tests and five template CLI tests cover source-bound requests,
playable audio/video comparisons, per-requirement manual verification, stale media
and superseded attempts, current accepted baseline checks, fixed-style isolation,
short/long/missing-media packets and new media provenance. These synthetic tests
do not assert actual natural-speech editing or renderer typography quality.
The full offline check passed with 331 tests (1 skipped); the separate photo-series
camera suite passed 10 Node tests. Link/catalogue checks and temporary standalone
packaging passed. All recorded exports remain 33; fixture proxies are not productions.
No model/API calls, original-media uploads or new release were performed.
