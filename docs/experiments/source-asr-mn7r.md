# SOURCE-01 follow-up: search raw local ASR on MN7R

28 October 2026. Owner authorised retrieval from a newly transcribed different
source. Selected the existing 36s English voice-only MN7R Reels film. Its hash
matched the original production's retained `reels` artifact. That checkpoint and
source bytes were preserved; no new film, upload, paid call or publication.

## Execution and source binding

Existing mlx-whisper 0.4.3 and retained tiny.en weights ran offline on this Mac:
English, temperature 0, word timestamps, no previous-text conditioning, complete
original video as input. No script/prompt was passed to recognition. Six queries
and their reference-script expectations were retained before the ASR run. The
reference script is not an independent acoustic transcript or ground truth.

Initial restricted-session import failed with `No Metal device available`.
The same installed environment succeeded with approved local GPU access; no
installation/model download/cloud fallback. One inference call took **20.022s**;
MLX peak allocation **308,803,674 bytes**, under the configured 1 GiB MLX limit.
These allocation counters are not total process RSS or a universal machine estimate.
Weights/config identities and raw-output hashes are retained in the private receipt.

`source_search.py import-whisper` adapts the raw five segments to the existing
source schema, preserving text/times and tagging it `local_asr_unverified`. It
checks source/raw-receipt hashes and original playback timing, validates ranges
with ffprobe, and pins the raw transcript/receipt sidecars. It makes no model call.
The receipt attests the operator's run; hashes detect drift, not authenticity.

## Retrieval results

| Query | Raw index result | Reference-script comparison |
| --- | --- | --- |
| `offers bids` | No hit | Expected present; ASR substituted `beads` for scripted `bids` |
| `focused Light layout` | 13.86–20.30s | Candidate covers the matching reference sentence |
| `Open analytics` | 13.86–20.30s | Same coarse segment; not a separately aligned action |
| `Monitor` | 4.68–13.10s; 28.96–31.40s | Product-name candidates found twice |
| `synthetic demo` | 20.92–28.96s | Candidate covers the reference phrase |
| `multiplayer voice chat` | No hit | Absent from the reference script; not proof of site-feature absence |

Thus **4/5 reference-present queries produced candidates**; the one reference-absent
query produced none. This is a tiny authored retrieval probe, not an ASR accuracy,
semantic-quality or independent model benchmark. After the miss, broader `offers`
returned two segments; it recovers a possible location but is ambiguous. It is
recorded as a separate follow-up query, not counted in the initial six.

Raw wording also differs at `AI supports stays review-belbel` and `public side`
versus the reference. No silent correction was made. Five segments replace manual
typing for initial retrieval, but no matched human-time baseline or speed-saving
claim was measured. Segment timings are candidates, not verified word/cut boundaries.

## Outcome and limits

**Partial success:** local raw ASR → revision-bound index → timestamped retrieval
works on this source, with an observed recognition-induced false miss. The local
review page offers original-source playback around the candidates, raw text,
reference expectations and missing-query controls. Independent listening, exact
word timing, pronunciation and any new montage remain unperformed/pending.
No current session audio-perception tool was used; text comparison is not listening.
Owner acceptance of an older film does not approve this transcript or a new cut.

Original Framewright importer tests cover text/provenance preservation, changed
source/raw rejection, missing model identity, unmapped timing and empty/invalid
segments. Existing lexical/staleness controls remain in force. No upstream
StoryToolkitAI runtime was installed or tested, and no general ASR promotion follows.

Private run, raw output, receipts, query fixtures/results, report/review page and
isolated journal remain in `source-asr-20261028`, outside Git. For a further real
edit, inspect candidate audio, retain any corrections separately and review joins.
[Importer contract](../../skills/video-production-router/references/editing.md).
