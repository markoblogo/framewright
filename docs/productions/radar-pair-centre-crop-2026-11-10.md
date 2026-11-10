# CENTRE-CROP-01: selected Radar pair and frozen comparison

Closed10November2026 · full films accepted; publication owner-reported · R04/R05, M4/M5 repeat-production evidence.
The owner accepted the revised scripts/reference frames and both moving pilots, then authorised full films and publication packages. Two90second English films now have landscape/portrait exports and platform packages. Full films and covers are owner-accepted; the owner supplied both YouTube and TikTok publication URLs; no new account access, purchase or Radar schedule.

## Pair and source boundaries

| Film | Working English title | Route and question |
| --- | --- | --- |
| A | Copilot Says “Addressed”. Was the Bug Fixed? | Separate YouTube/TikTok compositions. A response to an AI review comment is not proof of a correct fix. |
| B | Final Cut + Pixelmator: Fix the Image Without Rebuilding the Edit | Independent creative-editing story: repair a still image and return it to the timeline. Warm coastal world;4K landscape with a self-contained central portrait crop. |

Both come from the received 9 November menu, packet
`0c791dacfcf2e9bb8833dd1c08afb5679d0a3f77af5cd0953bd159423ab68a33`.
A: `yt-20261109-copilot-comments-outcomes`; B:
`yt-20261109-apple-creator-roundtrip` after the owner clarification below. The initial B was `yt-20261109-copilot-review-provenance`; its preparation/association/history remain retained as rejected, not a completed Radar case. Novelty is provisional; audience/revenue unknown. Dependabot/APM stays reserve.

A uses the [official 5 November metrics update](https://github.blog/changelog/2026-11-05-usage-metrics-api-adds-code-review-details-and-addressed-rate/).
“Addressed” includes responding that a fix will arrive later; evaluation is on PR
merge day. Use a hypothetical comment and regression-test illustration, not our
own organisation metrics or a claim that uptake measures bug-fix correctness.
B uses the [official Apple27October announcement](https://www.apple.com/newsroom/2026/10/apple-creator-studio-adds-powerful-new-ai-features-and-even-more-creative-tools/), refreshed10November: open an image from Final Cut’s timeline in Pixelmator Pro and save it back without reimport. November availability is announced; no installation, purchase or hands-on app trial is claimed. Original coastal illustrations explain local image repair; this does not prove repair through moving video frames or measured savings.

### Owner clarification and preparation revision —10November

The owner rejected the initial pairing because both subjects and the review-lab imagery felt like one story. Required: two independently useful Radar stories with different images, possibly different palettes, but common tools/approach, similar planned complexity and duration. Two distinct YouTube/TikTok packages allow later observation of audience response as well as technical effort and owner quality. A remains the dark code-review lab; replacement B uses a warm coastal picture, lighthouse/boat, image layers and a filmstrip. English narration is210/214words. The original frozen private protocol is preserved; `shared/records/protocol-amendment-v2.json` records the clarification, revised pair and accounting boundaries before pilots.

## Matched creative and technical conditions

- English, target 90 seconds each (±3 s), 30 fps; same voice and similar narration load.
  Six story beats: two original 3D sequences, three moving illustrative UI sequences,
  one closing takeaway. Common renderer, modelling/animation approach, typography and sound scope. Topic-specific geometry, imagery and palettes are deliberately different; same planning budget is not assumed equal actual effort.
  No 90-second static screenshot; same packaging/covers/subtitles scope per film.
- Both YouTube masters 3840×2160. A gets a separate native 1080×1920 composition.
  B's 1080×1920 file comes only from the **approved encoded landscape master**:
  fixed 1215×2160 crop at x=1312, y=0, then proportional downsampling. This is 0.5 source
  pixel off exact centre. RGB crop prevents subsampled input from silently rounding
  the odd source width; actual export/encode QA is still required.
- B's side regions carry useful secondary illustration; no essential information
  lives there. Portrait critical-safe guide at 1080×1920: x=80–900, y=160–1580;
  primary text at least 42 px, short lines. Check against the actual phone UI.
  Each film keeps the same audio timeline across its two aspects.
- Intended common stack: Blender 4.5.15 LTS, Pillow 12.0.0, NumPy 2.4.1, FFmpeg 8.0.1,
  offline Supertonic-3 M1 English. Blender4.5.15LTS availability and four Eevee still renders were verified on10November. Voice and encoded-motion exports passed bounded local checks for this pair; owner full-film acceptance is recorded. Preserve the shared runtime and
  freeze codec/quality settings before either film; stop both if unavailable.
  No automatic install, paid fallback or tool novelty on only one side.
- Equal source quality for both.4K graphics do not make a low-resolution insert
  native 4K detail. Record source/upscale resolution and 4K render expense. This
  comparison does not measure the usual 1080p baseline against 4K. Omit the optional
  FW sting/watermark from both, keeping the identity-placement experiment separate.

## Measurements fixed before production

Actual records belong in each future project's existing journal/COST-01 receipts.
The private paired forms are capture/comparison aids, not a second production log.
Preparation records have begun; no comparative result is established. Missing values stay unknown, not zero.

| Measure | Capture and comparison |
| --- | --- |
| Active work | Research, script, storyboard, assets, landscape, format adaptation, animation, corrections, QA, packaging. Distinguish observed owner work, tool elapsed and estimated agent-active effort with its basis; never present unattended wall time as human labour. |
| Waiting and rendering | Render/export, provider queue and human-review waits separately. Preserve UTC boundaries and overlap; do not add overlapping elapsed times into total wall duration. |
| Money/resources | Receipt-backed amounts/currency and credits separately. Unpriced model, compute and subscription allocation stay unknown; no invented labour rate or credit-to-money exchange. |
| Setup and corrections | Shared generic infrastructure recorded once; show raw costs and50/50 allocation. Topic-specific models/design are film-specific. Preserve rejected B0 work as disclosed setup/rework overhead, with gross totals and sensitivity to its exclusion. B-specific centre-safe design and all failed attempts/rescues are B effort. Lock the common kit before film-specific work; changes benefit both or enter the deviation log. |
| Quality | Owner reviews encoded landscape and portrait on display/phone. Score readability/safe zones, framing/content retention, clarity, motion/composition/joins and sound/sync. Record exact file hashes and technical QA separately. |

Quality scale: 1 unusable, 2 major defects, 3 needs correction, 4 publishable, 5 strong.
Every category must reach 4 with no critical defect and separate owner acceptance.
Practical time-efficiency signal: B passes quality, format-related active effort
is at least 20% lower, and total active effort is no higher under the same setup
allocation. This threshold is a planning heuristic, not a statistical test.
Cost saving requires comparable actual cost evidence; unknowns prevent that claim.
A B-only portrait reflow, moved overlay or tracking crop fails the pure-crop route:
retain its failure and rescue cost, then report conditional use or inconclusive.

Different topics, order/learning, manual estimates and owner preferences remain
confounders. Do not infer universal savings or causally attribute audience results.
Normal owner script/reference-frame, pilot and whole-film approvals remain gates.
No general replacement of native portrait composition follows from this plan.

## Retention, Radar and next gate

Private source menu, selected cards, frozen protocol, blank capture forms,
selection receipt and hash manifest: studio `records/centre-crop-01-20261110/`.
The receipt binds menu/packet, assignments, merge/CI and untouched exchange state.
The frozen plan was not a registered Radar experiment or association. At the initial production entry official GitHub sources were refreshed and two associations were exported. After clarification the Apple source was refreshed and a distinct replacement-B association was exported; the prior B association remains historical/rejected preparation, not a completed film. No automatic hooks or parallel scheduler were enabled. Association is not a registered Radar performance experiment.

After accepted films and owner publication, send only YouTube URLs through the
existing exchange. TikTok stays separate. Existing 7/28 calendar reports must not be
relabeled as upload-age windows. Views/retention/revenue are descriptive, separate
from production efficiency. The third film uses actual retained excerpts and
measured results after the two cases; it is not started by this record.

## Preparation checkpoint —10November

Private production: studio `productions/copilot-review-ab-20261110/`. Active A script210words, replacement B214words; six beats each. Four active original2160-square Blender states, twelve4K landscape references and twelve1080×1920 portrait references are retained; original B sources remain separate rejected preparation. A portraits are independently composed; all six B portraits match the fixed RGB crop pixel-for-pixel. Static dimensions, text-safe bounds and50 local review references passed. These are not encoded-video, motion, listening or owner creative checks.

Existing native projects retain source/QA/manifest records and COST-01 events. Raw still-render times, shared setup, failed compositor/setup attempts and a B-specific safe-margin correction are recorded. Active effort and assistant/model/local-compute monetary costs remain unknown. No zero-total-cost or efficiency conclusion. Owner reviews encoded motion/audio and phone presentation later; no new public-evidence count at preparation stage.

## Publication observation and deliverables

Two films × two platform versions = four accepted exports and four platform packages grouped into two Radar cases. A uses independent aspect compositions; B uses the fixed centre crop. Each gets its own story-appropriate cover/copy/subtitles. Publish only after owner acceptance, by the owner; send onlyYouTubeURLs toRadar.

Compare available views, watch/retention/completion and engagement at matched elapsed publication ages within each platform; proposed24h/7d/28d snapshots require timestamps and available data, not a new schedule. Include YouTube impressions/CTR/revenue only when available. Preserve unknowns and existing calendar-report boundaries. Different topics, colours, packaging and upload conditions remain confounds: audience response is descriptive, not causal proof that crop or separate composition won.

## Full-film checkpoint —10November

Owner accepted both20second pilots with sound and authorised the full versions plus publication packages. Private `full-v1/review.html` provides four90second/2700frame films, four platform text pages, covers and English SRT/VTT. A portrait is independently composed; B portrait is a fixed1215×2160 RGB crop at x1312/y0 from the encoded3840×2160 landscape, proportionally reduced to1080×1920. No portrait reflow or tracking crop. AAC payloads match within each film's two aspects.

Blender4.5.15 Eevee sources render1440×1440;4K graphics are not native4K object detail. Common offlineSupertonic-3 M1, a shared original electronic score and matched SFX scope are retained; no provider credits or new purchase. New narration covers five paragraphs per film; the accepted pilot's opening speech is reused. Continuous closing action and soft joins avoid a single still being held for the film.

Preflight caught doubled child offsets in a test-gate hinge and a boat rig. Corrected only the affected sources, retaining the failed attempts and probe/render times. B's layer explanation uses three independently drawn semantic planes after a colour-mask approach produced duplicate fragments. A hard-edged close-up trial was removed before export. Corrected B hero1 was fully rerendered rather than silently replacing accepted pilot bytes. Technical decode, dimensions/fps/duration, faststart, audio payload, representative encoded crop and packaging/link checks are retained. Selected encoded frames and actual browser seeking are operator checks; full creative/listening acceptance is separately owner-reported.

Native project journals/COST-01 and the derived comparison sheet retain raw render/export/inference times, correction overhead and earlier rejectedB0 preparation. Human/agent active-authoring effort, assistant/model allocation and compute/subscription money are unknown. Do not substitute tool seconds for labour or infer a20% active-work saving. Generic infrastructure/QA remains raw once, with50/50 allocation only in later comparison. No winner, monetary saving or audience result is established.

Owner accepted both full films with sound and their covers10November. Numeric quality categories remain unscored, not inferred from binary acceptance. Publication links and owner visual assessment are recorded below. Closeout retained current editable dependencies and bounded future-film excerpts; see the dependency-checked sanitation record below. Film/aspect variants are not new trials. No merge or release is part of this closeout.

**Next gate:** the separately authorised future experiment film may use the retained excerpts and measured results; observe audience data later through the existing Radar cycle. The third experiment film remains future work and can use only measured results, with unknown labour/money left explicit.
[Current priorities](../next-cycle.md) · [Experiment queue](../experiment-queue.md).


## Owner publication and visual assessment — received10November2026

| Case | YouTube | TikTok |
| --- | --- | --- |
| A — Copilot addressed metrics; independent aspect compositions | [Published link](https://youtu.be/YH-_vrmMquQ) | [Published link](https://vt.tiktok.com/ZSpPYkS9F/) |
| B — Final Cut/Pixelmator; fixed centre crop | [Published link](https://youtu.be/NvAYxy-n4JI) | [Published link](https://vt.tiktok.com/ZSpPYuXmA/) |

These are owner-provided publication URLs bound to the accepted local masters. Receipt date is known; upload timestamps, independent visibility/remote-file identity and audience metrics were not checked. Two stories remain two cases; aspect variants are not additional films.

The owner considers both visual results good and explicitly accepts using either technique. This is a qualitative same-pair judgement, not invented numeric category scores or universal qualification. Keep both methods: independent portrait composition where framing must change, fixed crop where the landscape's central story remains self-contained and readable. Neither is declared a time/cost winner: active-authoring effort and monetary allocations remain unknown.

The two pre-existing prospective idea associations and published statuses were delivered through the existing local exchange. Radar applied each; exact re-delivery returned duplicate and acknowledgements returned toFramewright. Only the YouTube URLs are in Radar publication payloads; TikTok URLs stay in native studio journals. Original rejectedB0 checkpoint and all four accepted master hashes remain unchanged. Private receipts: studio `productions/copilot-review-ab-20261110/publication-20261110/{owner-publication,radar-delivery-receipt}.json`. No analytics acquisition, new hook/schedule or registered Radar experiment was created.


## Closeout and retained material —10November2026

The [two-route recipe](../methods/centre-safe-dual-format.md) records the shared
production chain, independent A compositions, exact encoded-master B crop, failure
recovery, transferable manual alternative and known limits. Raw receipts plus
`closeout/measurements-summary.json` preserve measured phase costs. Portrait export
was142.75tool seconds for A and40.47for B; landscape+portrait exports total390.61
and331.40respectively. Neither sum is authoring time or overall production saving.
Full-stage source rendering including failed attempts/probes was614.47/926.73tool
seconds, with pilot source renders291.74/219.67retained separately. Shared final
technical/package QA111.96seconds is recorded once. Unknowns remain unknown.

Retained four accepted masters and covers/copy/SRT/VTT, editable selected scenes,
static assets/font, helper scripts, raw/processed speech and score/SFX stems,
publication/ack evidence, contact sheets and twelve future-film excerpts with
source intervals/hashes. Bounded before/after rig images preserve failure evidence.
The third film itself has not been produced. Its archival excerpt encodes are
closeout maintenance, excluded from the original A/B export comparison.

Sanitation retired1,374exact files /1,908,234,989bytes, chiefly rejected/probe and B
pilot/benchmark PNG caches, unused backup scenes and crop-check images. Plan and
apply helper received independent read-only approval before deletion. No candidate
overlapped protected dependencies. All non-null registered/linked hashes remained
valid;1,752required current PNG paths and173local HTML references passed after
cleanup. Eighteen source-compositor samples matched before/after hashes. This is
selected-input preservation and sampled reconstruction, not a fresh full-film or
independent-user reproduction. The retired historical B pilot/failed/probe pixel
caches are no longer locally available; their master clips, editable sources and
historical receipts/hashes remain.

Private external receipts: `closeout/{cleanup-plan,cleanup-receipt,excerpts-manifest,
measurements-summary,review-round1-result}.json`. Existing project journals retain
the closeout record. No Transit/RUN/SSI sources were deleted. The public evidence
index adds two film stories and one executed comparison, reaching75films/46trials
in the documented set; Hungarian Transit remains a language variant of one case.
The source version remains0.8.0. This documentation/closeout requires no separate
release, schedule, analytics acquisition or routine FW branding decision.
