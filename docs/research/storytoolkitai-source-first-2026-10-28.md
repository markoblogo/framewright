# StoryToolkitAI and source-first story assembly — 28 October 2026

Status: documentation reviewed; active bounded method/runtime candidate. No install,
model download or StoryToolkitAI runtime tested. [SOURCE-01 partial method trial](../experiments/source-first-playmcp.md)
now demonstrates local lexical retrieval over existing editorial subtitles and
assistant-supplied sampled visual observations. A [separate MN7R follow-up](../experiments/source-asr-mn7r.md)
ran existing local mlx-whisper and imported raw results; recognition errors caused
one expected-query miss. Neither trial qualifies semantic video indexing or the
StoryToolkitAI runtime.

## Official findings

[StoryToolkitAI](https://github.com/octimot/StoryToolkitAI) describes local speech
transcription, video indexing/search and a story editor with EDL/XML/Fountain exports.
It supports local or external LLM assistants and works independently of an editor.
The [installation guide](https://github.com/octimot/StoryToolkitAI/blob/main/INSTALLATION.md)
reports Mac M1 environments and Python 3.11; Resolve API integration explicitly
requires **Resolve Studio 18+**, not Free. These are upstream statements, not our
host qualification. Standalone releases may lag source features. The
[feature guide](https://github.com/octimot/StoryToolkitAI/blob/main/FEATURES.md)
warns that some references may be outdated. Verify the exact build/feature before use.

The repository identifies GPL-3.0. Models/dependencies, input rights and any code
integration need separate checks. Local operation has no hosted transcription fee
according to the README, but time, storage, hardware and model downloads remain.
External assistants have their own costs/terms. The README reports startup update
checks and selected external assistant/context transfers; do not equate a local
workflow with verified network silence. No private media is uploaded by this research.

## Recommended Framewright behaviour

First inspect the owner's authorised sources and retained catalogue before proposing
new generation. For each story need, distinguish:

| Action | Meaning | Required evidence |
| --- | --- | --- |
| Find / reuse | A suitable existing interval or still may cover the need | Exact material revision, interval and content observation |
| Adapt | Existing material needs crop, trim, cleanup, overlays or other processing | Retained source, change specification and review of the derived result |
| Create | Coverage is genuinely absent, or the owner explicitly requests new material | Missing-coverage reason and an authorised capture/generation route |

Searching is not proof of suitability. Absence from a transcript/index is not proof
that an event is absent from a video. Keep machine suggestions, operator observations
and approved selections separate; captions, OCR and visual similarity are different
evidence channels. ASR cannot establish that a screen action actually occurred.

Extend the existing [source-editing workflow](../../skills/video-production-router/references/editing.md)
and [material/scene composition](../../skills/video-production-router/references/production.md).
They already support source pins, explicit observations/transcripts, in/out ranges,
selection reasons, edit maps and retimed cues. The missing layer is searchable,
revision-bound content evidence and a source-backed story proposal, not another
project database or mandatory StoryToolkitAI/Resolve installation.

## SOURCE-01 — priority bounded trial on supplied material

Use one owner-authorised folder: a short screen recording, a short spoken take and
several images. Keep initial video/audio total around 2–5 minutes and run stages
sequentially on the Mac. Prefer existing local tools/model files; check disk/RAM and
obtain normal authorisation before installing/downloading a new model or app.

1. Inventory explicit files only; preserve originals, register material IDs/hash pins,
   duration/streams and provenance/rights. No unattended disk-wide search.
2. Retain a timestamped ASR transcript and visual observations with method/model,
   version, source hash and confidence/uncertainty. Human-corrected text must retain
   the original and correction provenance. Start with supplied annotations if the
   available ASR/vision route is unqualified; mark unperformed work explicitly.
3. Search three concrete story needs: an actually spoken phrase, a visible UI action,
   and one deliberately absent/unsupported request. Return material IDs, exact ranges
   or still IDs, supporting observations and reasons; allow “not found / not verified”.
4. Propose a 30–45s structure from those sources, tagging each beat find/adapt/create.
   Show exact candidate fragments, intended story role and remaining missing shots.
   No fabricated dialogue or claim inferred merely from a file name/transcript.
5. After the owner's selection, use the existing edit map for a local rough assembly.
   An EDL/XML or later OTIO handoff is a separate adapter check; no compatibility
   promise or automatic overwrite of the production journal.

Pass boundaries: manually verify returned content and bounds; make sure the absent
query remains unresolved; replace a source and demonstrate stale transcript/index
and selection handling. Check VFR/stream offsets and avoid trimming away qualifying
words. Retain search misses, corrections, effort and final viewing/listening separately.
Index coverage, retrieval relevance, editorial usefulness and final quality are
different outcomes. A readable index is not successful video understanding.

### Optional StoryToolkitAI runtime comparison

On a fitting authorised production, compare the same small source pack using the
exact chosen StoryToolkitAI build in standalone mode. Confirm import, timing, one
search, missing-file relink and one usable export. Only test local features first;
do not require paid Resolve or a cloud LLM. Compare effort, resource footprint,
retrieval quality and edit-map fidelity against current tools; preserve failures.
No upstream code or model assets are copied into Framewright.

## Relationship to current plans

Prefer SOURCE-01 before complex character generation on the next source-rich brief;
this is a planning priority, not permission to restart paused productions. Existing
owner-selected work stays authoritative. SOURCE-01 supplies concrete materials to
PREVIS-01 where staging is needed, PROD-01 records unmet coverage/review, and OTIO-01
can later export the accepted concrete cut. Generation remains available for actual
gaps and deliberate creative choices.
