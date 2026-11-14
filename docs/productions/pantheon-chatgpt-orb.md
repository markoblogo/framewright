# A Window to the Sky — Pantheon / ChatGPT visual study

14 November 2026. The owner accepted both final 37-second English films and requested YouTube/TikTok publication packages. One story, two 1080p30 compositions. The owner supplied [YouTube](https://youtu.be/3qA7K-G0VXk) and [TikTok](https://vt.tiktok.com/ZSpVhxkT7/) publication URLs on 14 November 2026 (owner-provided URL provenance). Independent visibility, uploaded-file identity and audience/monetisation results remain unknown.

## Creative direction and sources

The film shows the familiar Pantheon facade, a wider dome view and animated construction lines, then keeps a circle of sky while the camera pulls back to a locally authored computer running a voice-interface treatment. The orb becomes compact before the accepted 29-frame [FW ending](fw-identity.md). This is an artistic resemblance study; it does not assert the origin of ChatGPT's design or a measured golden-ratio property of the building.

The owner supplied the main sky photograph and interface reference. Additional real photographs are [Demetrios Karatassos's facade](https://commons.wikimedia.org/wiki/File:Pantheon_front.jpg) and [Wilfredor's dome interior](https://commons.wikimedia.org/wiki/File:Pantheon_(Rome),_Dome_interior.jpg), both listed by their photographers as CC0. Source pages, file hashes and unchanged originals are retained privately. Local crop, colour, projection, vector drawing and authored 2.5D monitor work use Pillow/NumPy/FFmpeg; no generative alteration of those photographs or documentary camera-tour claim is made.

English synthetic narration uses Google AI Studio/Knox. The 35.36-second owner-downloaded source, original local score/effects and existing thin-metal FW sound are retained. No new paid API, purchase or public upload was performed. Covers are newly composed native photographic layouts in the film's charcoal/blue/ivory palette, independently checked; they are not extracted film frames.

## Worked example: v2 to v3

**Job:** make the opening facade drawing readable in both formats while retaining
the approved remainder of the film. This is a completed real correction, not a
newly manufactured defect or a new model/tool trial. Use it with the existing
[revision contract](../../skills/video-production-router/references/revisions.md).

1. **Keep the original and the actual note.** The owner had approved the v2 film
   apart from its faint tracing lines, after an earlier request added the drawing
   and a light surround/dark type for portrait. The final note was: «их стоит
   сделать и читаемее и жирнее — чтобы были заметны наверняка особенно в
   уменьшеной тикток версии». In English: make the lines more legible and thicker,
   especially in the reduced TikTok view. This was a visibility correction, not
   permission to redesign the film.
2. **Define the boundary before editing.** Authorised picture change: 0–7.1 s.
   Protect the drawing positions/timing, portrait light layout and all text,
   37-second duration/30 fps, narration/music/effects, later dome-to-computer
   transition and 29-frame FW ending. Retain both v2 sources under their own IDs.
3. **Change only the needed layer and compare in context.** Final tracing uses
   saturated blue 8 px strokes, 12 px white backing and larger drawing points.
   Existing before/after clips cover the requested 0–8.1 s window (encoded proxies
   are 8.125 s, including 0.025 s padding). Inspect the moving drawing and its
   transition, not just a poster: the comparison's first-frame PNGs are identical
   before the strokes appear. Actual encoded 335 px portrait and 640 px landscape
   sheets check whether the lines survive reduced viewing.
4. **Check the protected elements and retain failure evidence.** The first RGB
   join scored 0.988746 SSIM in an unchanged handle, below the preselected 0.99
   threshold. Its export was superseded; the threshold was not lowered. The
   corrected native-YUV join passed. The table below distinguishes exact
   preservation from an approximate encoded join.
5. **Record the decision on the exact versions, then deliver.** On 14 November
   the owner said: «Посмотрел — теперь хорошо, принимаю обе версии. Готовь
   пакеты для публикации на YouTube и TikTok.» Both v3 masters were retained,
   given exact-version creative/listening receipts and packaged without another
   encode. YouTube/TikTok links were subsequently supplied by the owner.
   Landscape is the administrative primary in the single-selection helper;
   portrait is equally accepted and pinned in the same delivery manifest.

### What was preserved

| Region / property | Retained check and practical limit |
| --- | --- |
| All narration, music and effects | Complete decoded audio sample count and SHA256 match v2 in both formats. No voice/music regeneration. |
| Picture from 8.333333 s to 37 s | All 860 decoded tail frames match the baseline, including the transition and FW ending. |
| 7.1–8.333333 s join handle | Required re-encoding to the next keyframe; SSIM 0.993293 landscape / 0.992043 portrait, above the unchanged 0.99 threshold. This interval is not claimed byte- or pixel-identical. |
| Timing and aspects | Both remain 37.000 s / 1110 frames / 30 fps, 1920×1080 and 1080×1920. |
| Perceived line visibility | Operator inspected the reduced encoded sheets; the owner then accepted both complete v3 films. Native-size inspection alone had missed the usability problem. |

### Exact versions and retained evidence

Private paths below are relative to studio `productions/pantheon-chatgpt-orb/`.
They are retained working evidence, not media bundled into this Git repository.

| Aspect | v2 baseline SHA256 | Accepted v3 SHA256 |
| --- | --- | --- |
| YouTube | `39a03e94c2765f4acdf6cbad0d72d9cd9f3285ffd0314619fa26b210c92c3015` | `ecc5d95833be49ef6c68112a040cc2109b11d863e9209ee0edc190a4352c049a` |
| TikTok | `446f7338045d205100932e6ab132cc6e3ccb0b2f9104a61343913d092e2b56ed` | `6b3dc19c3542ff69c721800abf3dac37c607b210a4edf2139a5a53d3d82b03b0` |

- Request and source pins: `full-v3/revision-request-youtube.json` and
  `revision-request-tiktok.json`; immutable originals in `full-v2/`.
- Context clips/stills/reports: `full-v3/compare-youtube-native-yuv/` and
  `compare-tiktok-native-yuv/`. Their `report.json` files describe comparison
  creation; they do not independently establish preservation or owner approval.
- Checks: `full-v3/verification-youtube.json`, `verification-tiktok.json`,
  `qa.json`, reduced `readability-encoded-335px.jpg` / `readability-encoded-640px.jpg`
  and `failed-attempt-rgb-join.json`. Failed first-attempt masters were replaced
  after their hashes were recorded; those old failed bytes are not retained at
  the current same-name paths.
- Later decisions: `OWNER-ACCEPTANCE.md`, exact-version observations and selected
  final in `project.json`; `publication/manifest.json` pins both deliveries and
  `PUBLICATION.json` records the owner-provided URLs. Earlier technical receipts
  still say review was pending **at their capture time**; later owner receipts
  establish acceptance without rewriting those snapshots.

The reusable lesson is to define the permitted edit and protected elements,
inspect the actual reduced viewing size and compare the join in context before
selecting the result. This case supports that bounded workflow on these assets;
it does not establish arbitrary-edit automation, cross-machine recovery or an
independent operator's success. Active labour and whole-route cost remain UNKNOWN;
recorded render phases alone cannot establish savings. No new media was generated
or re-exported to prepare this worked example.

## Delivery and limits

Private `productions/pantheon-chatgpt-orb/` retains accepted v3 masters, source/voice receipts, editable recipes, failed-attempt notes, context comparisons and the native project journal. `publication/youtube/` and `publication/tiktok/` contain hash-matched video hard links, native covers, English copy, transcript, SRT and credits. Captions are phrase-aligned to the supplied script and observed speech boundaries; independent word-level transcription was not performed. Cover/copy review remains separate from film acceptance. Publication is owner-reported; the private `PUBLICATION.json` receipt preserves the supplied URLs, receipt date and unchanged package-manifest hash. Web access attempts did not establish independent visibility or uploaded-file identity. Dependency-aware retirement of superseded renders is a later closeout step; no historical reconstruction, all-platform publisher or audience result is established.
