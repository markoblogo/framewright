# SOURCE-01: several sources → story proposal → remaining work

28 October 2026. Owner authorised retrieval, an edit proposal and identification
of missing material. This tests the proposal stage, not final film production.

## Inputs and evidence

One coherent MN7R source set:114s horizontal review,36s portrait Reels,9s standalone
3D intro and the text-bearing thumbnail. Total timed media:159s. Main/Reels/cover
and editorial captions matched the retained original production pins; the older
main ASR receipt also matches that source. Source files and the original checkpoint
remained unchanged. No fresh recognition, model download, cloud call or spending.

Speech evidence:30 existing editorial caption cues and5 raw ASR segments from the
separate Reels trial. Visual evidence:four currently viewed frames (intro4s,main12s
and38s,Reels16s), plus the original cover. These samples do not verify full motion,
complete UI actions, listening or comprehensive privacy coverage.

## Retrieval and selection

Existing `source_search.py` indexed all4 files and evidence sidecars. Nine authored
requests gave7 queries with candidates and2 without. This is an integration trial,
not a blind model benchmark.

| Query | Candidate |
| --- | --- |
| `OFFERS MATCH EXECUTION`, observations | Intro4.000–4.033s |
| `offer execution`, transcript | Reels0–3.92s |
| `Monitor brings`, transcript | Main9.86–13.92s;Reels4.68–13.10s |
| `Execution teams`, transcript | Main36.88–39.06s |
| `focused light layout`, transcript | Main67.82–72.62s;Reels13.86–20.30s |
| `Explore Monitor Online`, transcript | Reels28.96–31.40s |
| `MN7R commodity brokerage`, observations | Cover, no invented time |
| `saved order confirmation`, observations | Not found in supplied annotations |
| `customer testimonial`, any | Not found in supplied annotations |

The agent selected a43s horizontal feature summary. Every chosen range references
a returned source/cue and matching source hash, with explicit contextual handles.
The ordinary cut map checks actual media bounds, not editorial correctness.

| New timeline | Source selection | Purpose |
| --- | --- | --- |
| 0–2.50s | Intro3–5.50s | Connected workflow stages |
| 2.50–6.90s | Reels0–4.40s | Spoken premise |
| 6.90–20.00s | Main9.20–22.30s | Workspace and offer information |
| 20.00–30.50s | Main32.70–43.20s | Execution after agreement |
| 30.50–37.70s | Reels13.50–20.70s | Layouts and analytics |
| 37.70–40.64s | Reels28.96–31.90s | Existing spoken CTA |
| 40.64–42.64s | Cover reference, adaptation pending | Website closing card |

Three video sources provide6 passages,40.64s in the validated cut map. The planned
2s still card is outside that cut-only map;42.64s is a proposal, not an encoded file.
The page plays original ranges and displays the cover reference. It does not
implement final reframing, mixing or frame-accurate joins.

## Find / adapt / create

No new capture or generation is needed for this concept. Required adaptations:

1. Fit portrait passages into16:9 deliberately or replace them with available
   horizontal footage; preserve text and recheck readability/privacy.
2. Reconcile silent intro, music-backed main film and voice-only Reels. Existing
   audio is available; mix, listening and sound strategy remain unresolved.
3. Adapt the cover into a closing card with `mn7r.com`; it is not already an end card.

Two conditional gaps are separate: a tutorial would need a verified create/save
action; customer-results claims would need cleared testimony. Neither is required
or claimed in this feature summary. First search/review other captures if those
goals are selected. An annotation miss is not proof of absence from the library.

## Outcome and reusable procedure

**Proposal-stage integration exercised; owner agreed to the order.** Existing
search/cut-map helpers suffice. Added software regressions cover multiple sources
with identical local cue IDs and rejection when an unmatched source changes.
These synthetic integrity tests are separate from creative/perceptual evaluation.

Reusable process: coherent goal/explicit source set → pinned evidence → queries,
including honest misses → source/cue selections and context handles → ordinary
edit map → required adaptations versus conditional new-material requests → review.
Keep those decisions in the existing journal/composition plan. Missing annotations
must not automatically trigger generation.

Private index, results, proposal, map, gaps, review page, source-preservation records
and isolated journal stay in `source-multicut-20261028`, outside Git. Full listening,
motion, join meaning, final privacy/readability, encoded QA, rights and publication
remain separate. StoryToolkitAI runtime remains untested.
[ASR follow-up](source-asr-mn7r.md) · [Workflow](../../skills/video-production-router/references/editing.md).

## Authorised draft assembly

The owner then requested actual portrait adaptation, audio mixing and join checks.
An internal1920×1080/30fps draft was assembled sequentially with existing FFmpeg8.0.1,
Pillow and installed Arial. No new inference, upload or paid service. The accepted
42.64s plan quantises to1279frames/42.633333s: only the last2.94s video selection
rounds down by6.667ms. The planned2s closing card is now actually included.

Portrait passages keep the complete original picture in a576×1024 right inset;
original English headings and website occupy the left. No hidden crop or stretch.
The existing cover supplies the closing artwork with a new address overlay and
final350ms fade. New graphics are original local layouts; no font is redistributed.

Existing clean voice stems replace mixed-source audio. The already corrected
Monitor pronunciation is retained. Each selected voice is normalised, with8ms
edge fades in retained margins. The existing original score runs continuously,
ducked7dB during voice. No new TTS or source-separation inference. Clean voice versus
the corresponding original encoded ranges gave numeric best lag0ms in a±10ms
screen and correlation0.9943–0.99998; this is a timing screen, not listening or
perceptual sync approval. Mono/stereo RMS ratio0.99997 showed no material numeric
cancellation in this mix. Per-source/whole-project hashes remained unchanged.

The first encode exposed inherited empty/fading source backgrounds at some joins,
despite passing black-interval detection. Sampled before/after frames caught this.
The corrected v2 holds the first visible portrait frame for400ms and the offer
scene's visible boundary frames for500ms/700ms. These picture-only holds are
recorded separately from the straight source map; no cut-order, total-timing or
voice displacement is implied. The repaired encoded audio stream hashes identically
to v1. Preserve this limitation: an edit map alone cannot describe the later holds.

The retained10 speech cues lie wholly inside their selected source ranges;25
unselected cues remain listed as omissions, not approved semantic deletions. Six
short join previews come from the actual adapted/mixed encode, rather than from
unadapted originals. Full decode, exact format/duration and loudness/peak inspection
are recorded per version. Both v1 and the corrected v2 passed full decode and
measured−17.25LUFS/−3.45dBTP; v2 retains its own report and6 decoded join previews.
The corrected contact sheet removes the sampled empty backgrounds. This inspection
is sampled; motion, full
listening, join meaning, complete privacy coverage and owner film review remain
separate. A failed verification-path attempt is retained before the corrected v2
verification run; it is not classified as a media defect or passed check.

**Owner acceptance,28 October:** the owner replied “принято” after delivery of
draftv2 and the actual-encode join page. Creative/pacing and mixed-sound acceptance
are recorded with `owner_report` provenance against that exact file revision.
The scoped source-first trial is complete through an accepted internal draft.
This supersedes the draft-review waits above; it is not independent operator
listening/motion/privacy validation or permission to publish. No publication ran.
