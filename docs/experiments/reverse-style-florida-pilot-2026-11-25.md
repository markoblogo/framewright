# REVERSE-STYLE-01 — Florida vs Man motion-strip probe

25 November 2026. Owner requested a horizontal game review pilot from two
provided recordings and a queued tool. [Game](https://floridavsman.app/):
website direct fetch unavailable, owner capture provides actual evidence.
First 35s of gameplay capture included unrelated pages, excluded. Site hero
and native title/gameplay, delivery notification, rain and score screen
are actual selected footage; score 6,520 visible. No claim of independent play.
20s 1920×1080 30fps, original arcade-inspired side panels and procedural
chiptune, no voice in pilot. Sampled game-recording audio silent, not a claim
that game itself has no sound. Owner review pending.

## Bounded upstream test

[reverse-video](https://github.com/kelano86/reverse-video), MIT, commit
`793b80352dea379579c949b8f194da1cd01f863d`. Actual upstream `strips.py` and
`common.py` downloaded/pinned and inspected; local Python with numpy 2.4.1,
Pillow 12.0.0, FFmpeg; no models, accounts or global installation. No full
measure/listen/OCR/transcript/style.json execution. Six specified 0.8s windows
at 30fps, including five known edit cuts and one gameplay-only interval.

| Window start | Known authored cut | Reported peak |
| --- | --- | --- |
| 2.70s | 3.0s | f9 / 3.0s |
| 5.20s | 5.5s | f9 / 5.5s |
| 8.70s | 9.0s | f9 / 9.0s |
| 12.20s | 12.5s | f9 / 12.5s |
| 15.70s | 16.0s | f9 / 16.0s |
| 10.00s | none | f23 / 10.767s |

All five provided boundary windows peak at the exact known frame. The
non-cut gameplay window also reports motion, demonstrating that frame
change is not an automatic semantic event or edit detector. Several hard
cuts were described as multi-frame changes/easing due to native activity
around the cut; use the strip itself and recipe, not easing label as truth.
Focused QA utility useful for checking nominated transitions; complete
reverse-style research remains open, including narrated known fixture,
full measures/OCR/audio and dependency/model licence checks.

Private package `productions/florida-vs-man/pilot-v1/`: `make-pilot.py`,
`pilot-receipt.json`, `reverse-video-source/` (upstream code kept outside Git),
`reverse-trial/strip-results.txt` and six image strips.
Pilot master SHA256 `9f8e183d36211aab632a6f378401f00544e23bb2a9bffb8f6f0f986533e56de4`.

Owner accepted the 20s gameplay pilot and requested English YouTube and full-screen TikTok versions. [Full review](../productions/florida-vs-man.md) prepared; full-film acceptance pending. This is pilot creative feedback, not a separate verdict on tool correctness.

Owner subsequently accepted both full game-review cuts. The bounded motion-strip result stays unchanged; full reverse-style pipeline remains open.
