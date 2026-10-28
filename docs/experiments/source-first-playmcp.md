# SOURCE-01: retrieval and a proposed PlayMCP recut

28 October 2026. Owner authorised a trial using an already-created review. Existing
local PlayMCP sources were selected; no new capture, generation, ASR, model download,
cloud upload, final export or publication. The original production checkpoint was
byte-identical after the trial and source media were not edited.

## Source set and method

Five explicit sources: the 150s final review, a 12s sign-in capture, a 14s community
capture and two images (landing page/book cover). Total timed media: 176s. Final video
and subtitle hashes matched their retained original project pins. Existing 38 editorial
subtitle cues supplied speech text. The assistant visually inspected five extracted
frames and two original images. Those are sampled observations, not full-motion
review or fresh acoustic verification. No claim of automated video understanding.

New standard-library `source_search.py` reuses the existing media inspector and
hash-pins the source specification, media and evidence sidecars. Its retrieval is
lexical over supplied evidence, with channel/range/provenance kept on each result.
Changing a source, sidecar, source specification or retained index requires explicit
rebuilding/review. It does not run ASR/OCR/vision, interpret negation or rank semantic
quality. New files only; no overwrite or network operation.

## Observed queries

| Query | Result | What it establishes |
| --- | --- | --- |
| `connect PlayMCP`, transcript | Final review 21.1–24.9s | One existing editorial cue found, not new ASR/listening |
| `sign in phone number`, observations | Sign-in capture 3.000–3.033s | One inspected frame shows the form; successful authentication unverified |
| `multiplayer voice chat`, any | Not found in index | No supporting annotation; not proof of absence from the site/media |
| `successful login completed`, observations | Not found in index | No matching supplied evidence of completed action |

A private copy of the book-cover source was altered after indexing. Search refused
the stale source; the real original remained unchanged. Unit controls also cover
changed annotations/sidecars, modified index, bounds and still-image evidence.

One useful finding: the `web-challenge` filename suggested a narrower subject than
its inspected frame, which showed community game cards. Indexing from filenames
alone would misrepresent that evidence. The visual annotation reflects the frame.

## Proposed structure, accepted by owner

Original agent-authored proposal based on saved cues and inspected frames, using
the existing cut-only edit map:

| New timeline | Source range | Purpose |
| --- | --- | --- |
| 0–18.5s | Master 0–18.5s | Question and platform explanation |
| 18.5–29.8s | Master 37–48.3s | Agent code and creative tools |
| 29.8–34.3s | Master 61.8–66.8s | Community/challenge overview |

Existing picture, owner voice and music are retained together. No fresh speech or
generation is needed for this proposed 34.3s order. The local review page plays
source ranges sequentially; browser seeking is not an encoded edit or frame-accurate
export test. On 28 October the owner replied “принято” to this new proposal. Creative
acceptance is recorded against the proposal, edit map and review-page revisions in
the isolated project journal. Dedicated join listening and final encoded QA remain
unperformed; neither publication nor an extra export is authorised by this acceptance.

Missing work: reviewed login action if this becomes an authentication tutorial;
updated site facts/capture if it becomes a current review; join/semantic listening,
final CTA and delivery kit if a new publication is selected. Historical dated source
footage is not current provider availability or terms. No blanket music-rights clearance
or publication grant is established by reuse.

## Qualification and next use

Outcome: **partial method trial; proposal accepted by owner**. Local evidence
indexing, exact lexical hits, honest misses and stale-copy refusal were exercised.
Six focused software tests cover the new helper. Semantic retrieval, automatic
transcription/indexing, comprehensive visual/action interpretation, complete-cycle
edit quality, time savings and StoryToolkitAI runtime remain unqualified.

Private source plans, index/results, proposed edit map, review page, source-preservation
receipt and journal stay outside Git in `source-first-20261028`. This public report
records method/scope only. [Usage](../../skills/video-production-router/references/editing.md).
