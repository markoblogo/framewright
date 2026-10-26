# DJV: A/B frame notes and portable sessions

26 October 2026. Owner-selected real trial: two retained Nantes green-line exports,
1920×1080, 24fps, 100s. DJV 3.7.5 arm64; official release source pinned to
`4d90982b4085adf4d150f1bf0b0b4a5490b023d5`. **Partial success with gaps; keep candidate
status and repeat on the next one or two authorised productions.** This is neither
a new film nor an owner approval of v2. [Sanitized receipt](../../experiments/2026-10-26/evidence/djv-green-line-review.json).

## Observed

A=v2/B=v1 visibly compared at frame72 (3s). The facade edges in v2 are more defined;
one orange source-bound outline isolates the area. Three notes retain defect,
desired change and preservation requirements: frame72, range216–347 inclusive
(9–14.5s exclusive), frame612 (25.5s). The latter two are control observations,
not evidence of defects in the film. Notes/drawing were authored as session JSON,
then loaded and saved by native DJV; no mouse-drawing test is claimed.

Native save/reopen/relocation preserved the A/B setting, source identity, notes,
drawing and custom Framewright section. Resaved absolute paths resolve to the
relocated media directory, confirming relative links. Next-frame72→73 and
next-marker72→216 matched their anchors; the drawing was absent at frame73.
Original exports and review copies remained byte-identical. A thin bridge retains
the session, structured notes and report in the existing production journal,
with receipts pinned to both exports. It does not create another approval store.

## Gaps retained

- Startup screenshots and later H.264 native captures can be black although time,
  metadata and exit status are valid. Explicit fixed zoom fixes some captures,
  not all. Inspect actual pixels; metadata is insufficient.
- Local diagnostic 0–30s FFV1 RGB/PCM copies show the map at frame240, but frame612
  remains black in DJV. Independent FFmpeg extraction at612 is nonblack and
  labelled. That extraction does not count as a DJV pass. The root cause is unknown;
  neither H.264 alone nor a universal FFV1 workaround is established.
- Positional CLI `.djvr` reopening works. Some native Open-dialog attempts could
  not select a saved session; broad GUI reopening remains unqualified.
- Full continuous playback, focused listening, perceptual AV sync, calibrated
  colour, audio/image-only review and autonomous semantic review were not tested.

No paid service, upload, new install, publication or film alteration occurred.
Private media, session machine paths, logs and downloaded upstream source stay
outside Git. This record adds no row to the video-export registry.

## Follow-up agreed by owner

Repeat on the next one or two productions: actual A/B first/middle/last frames,
adjacent-frame navigation, a played/listened passage, save/reopen/relocation,
anchor/source integrity and explicit owner review. Keep failures; promote only
repeatedly demonstrated scope. [Reusable procedure](../../skills/video-production-router/references/djv-review.md).
