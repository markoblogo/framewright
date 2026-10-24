# SSI website Reels: real pages, stationary captions

Produced 22 October 2026. Two local 15-second, 1080×1920p30 H.264/AAC exports for
Instagram Reels: Ukrainian and its requested English counterpart, no narration. Owner accepted the Studio preview
and later reported partner acceptance and a request for an otherwise identical
English version. The owner later reported English partner acceptance and supplied its Instagram URL; Ukrainian publication and all audience results remain unconfirmed.
[Artifact record](../../experiments/2026-10-22/outputs.json) ·
[Sanitised technical evidence](../../experiments/2026-10-22/evidence/ssi-site-reels.json).

## Brief and edit

Partner phone recordings were visual references only; their audio was not reused.
Large captions hold still while real Ukrainian site pages scroll beneath them.
The copy was compared with the public pages: prices, comparative analytics, index
explanation and market context. Recorded values are dated site content, not a new
market recommendation or a claim that the index itself is AI-generated.

| Time | Actual source page | Fixed caption |
| --- | --- | --- |
| 0–3s | [Home](https://spike.1d3x.com/uk) | ЦІНИ АГРОРИНКУ УКРАЇНИ |
| 3–7s | [Analytics](https://spike.1d3x.com/uk/analytics) | ДИНАМІКА ТА ПОРІВНЯННЯ ЦІН |
| 7–10s | [About](https://spike.1d3x.com/uk/about) | ЩО ЦЕ І ЯК ЦЕ ПРАЦЮЄ |
| 10–12.5s | [Context](https://spike.1d3x.com/uk/media-hub) | НОВИНИ Й КОНТЕКСТ РИНКУ |
| 12.5–15s | Home reprise | РИНОК — ПЕРЕД ОЧИМА; spike.1d3x.com |

## Capture and assembly

HyperFrames 0.8.185, existing Chromium/Playwright and FFmpeg; no paid APIs, model
calls or new model downloads. The fresh HyperFrames skill pack retired the former
specialised launch workflow; this job followed the current entry skill/references.
A native capture with `--skip-vision` supplied source/brand inspection and omitted
one small asset at its size floor; it did not supply live scroll video.

Playwright recording initially placed small page content inside a gray canvas.
That take was rejected after contact-sheet inspection. The successful route used
540×960 CSS pages at DPR2, capturing actual 1080×1920 browser frames at successive
scroll positions. Smooth scrolling was disabled only for deterministic capture;
screenshot animations were suppressed. This is authored scroll timing, not a claim
of unchanged real-time website animation or interaction speed.

Overlapping per-scene videos then produced native extraction warnings at seams.
The revision uses one continuous 15-second background stream, four 200ms
FFmpeg `smoothleft` transitions at 3/7/10/12.5s, and separate fixed caption layers.
A retained registry `transitions-push` example informed the transition direction;
its full showcase was not used or qualified. No upstream source is redistributed.

The original clean SSI D instrumental and previously admitted CC0 Freesound
whoosh were reused, with four transition cues. Exact attribution is retained in
the evidence. This is reuse of the tested Openverse acquisition workflow, not a
new API or automatic semantic sound-placement test. Local font files, captures,
phone references, music and full production projects stay private.

## Verification and limits

- Full encoded decode: 450 frames, 15.000s, no errors.
- Lint/runtime/layout/contrast/craft: zero errors and warnings; craft sampled 120
  times. The dedicated motion checker was disabled; no blanket motion score.
- Encoded contact sheet and preview phone/beat sheets/all four seams inspected.
  Five within-shot comparisons found caption differences 0.001–0.083 versus
  moving-background differences 22.768–39.531 on a 0–255 grayscale scale.
- Encoded audio: −17.32 LUFS, −1.51 dBTP, LRA2.0 LU; mono versus stereo RMS
  −0.008dB. Measurements do not replace listening; no independent listening pass.
- Owner preview acceptance and partner acceptance (owner report) are separate
  from technical QA, public publication and audience effectiveness.

The local production checkpoint retains file revisions, preview acceptance and
encoded technical evidence. It does not grant publication authority. No separate
cover, subtitle file or publication copy was requested or delivered.

## Partner decision and next version

The owner reports partners accepted the Ukrainian Reels and requested the same
edit with English site pages and English captions. The English counterpart is now
delivered locally and its preview accepted by the owner. The owner subsequently
reported English partner acceptance; its exact acceptance date is not established.

The English version recaptures actual `/en`, `/en/analytics`, `/en/about` and
`/en/media-hub` pages with the same scroll positions/durations, transition timing
and caption geometry. Captions: UKRAINE’S AGRI MARKET PRICES; PRICE TRENDS AND
COMPARISONS; WHAT IT IS / HOW IT WORKS; NEWS AND MARKET CONTEXT; THE MARKET —
AT A GLANCE. The CTA domain is unchanged. All five caption styles are identical
to the Ukrainian source. Both files are15s1080×1920p30; decoded PCM is byte-identical.
English encoded full decode, contact-sheet review and five hold/motion comparisons
passed; native phone/beat/four-seam review and HyperFrames checks are clean.
English output is13,569,392bytes; −17.32LUFS/−1.51dBTP. These are separate artifact
checks, not a new tool qualification.
[English evidence](../../experiments/2026-10-22/evidence/ssi-site-reels-en.json).

The [six weekly-report demos](ssi-logistics-illustrated.md) were **not accepted**
by partners and await a separate specification. Their detailed objections remain
unknown. That workstream stays paused; it neither rejects this Reels nor revokes
the earlier scoped Openverse SFX qualification.

## English publication link — owner report recorded 24 October 2026

[English SSI website Reels on Instagram](https://www.instagram.com/reel/DezcjZ0tXuz/).
The owner supplied this URL and previously reported partner acceptance. The local
production journal binds the publication observation to the retained English master.
Independent web fetching returned a cache miss; exact upload time, public visibility,
uploaded-byte identity and audience metrics are unknown. This does not resume the
paused weekly-report workstream or establish publication of the Ukrainian version.
