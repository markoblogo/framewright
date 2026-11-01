# Comparative art-film reuse example

Authored local FFmpeg/Pillow example, tested on macOS Apple Silicon. No vendor
source, photographs, footage, fonts, voice weights or media binaries are included.
[Case and limitations](../../docs/experiments/two-cities-reuse.md).

Private plan fields: `shots` (each: permitted file, kind photo/video, offset in
seconds, duration, English title and optional subtitle), `voice`, `score`, and
`reuse_scope`. Appearance lives in the pinned Python recipe; all changing content
lives in the plan/media. Requires installed FFmpeg/ffprobe, Python/Pillow and the
specified macOS font; it does not install dependencies or generate speech itself.

```sh
python3 render.py PRIVATE_PLAN.json NEW_OUTPUT --aspect 16x9
python3 render.py PRIVATE_PLAN.json NEW_OUTPUT --aspect 9x16
```

Each aspect gets a new directory. Two encoder threads, sequential shots, bounded
subprocess timeouts, stage progress, source hashes and full-decode report. Exact
frame counts, current output files and picture/listening still require checking.
This is an authored example, not an admitted executor adapter or publication tool.
No automatic overwrite, approval inheritance or paid/network call.

Caption bounds: titles wrap/reduce within three lines. An oversized unbroken
title or optional subtitle is rejected before writing its PNG; shorten the copy
instead of accepting clipping. [Regression closeout](../../docs/final-local-review-2026-11-01.md).

## Caption reading-time preflight (optional, English heuristic)

```sh
python3 caption_timing.py PRIVATE_PLAN.json > NEW_TIMING_REPORT.json
python3 render.py PRIVATE_PLAN.json NEW_OUTPUT --aspect 9x16 --enforce-caption-timing
```

The read-only preflight counts title **and** subtitle. Minimum seconds are the
maximum of 2s, words/2.5 and non-whitespace characters/15, plus0.4s for transitions,
rounded up to24fps (or the explicit preflight fps). These are conservative authored
English-copy assumptions, not measured reading ability or a cross-language rule.
No-text scenes require no caption hold. Negative/nonfinite durations are rejected.
The preflight returns2 for insufficient time,1 for invalid input,0 for a heuristic
pass. It does not inspect media, evaluate layout, assess speech or change the plan.

With the explicit render flag, insufficient time is rejected **before output
creation/media access**. Default rendering remains backward-compatible. Shorten
copy or author a new timing plan and recheck narration/music/source ranges; never
silently stretch an accepted film or assume global voice timestamps stay aligned.
A longer source clip still needs a valid range, and an image needs intentional
movement. A heuristic pass is not owner readability/listening acceptance.

REL-B controls: a96-character heading plus64-character subtitle fitted geometrically
but the3s test was too short; this policy recommends9.75s for that exact copy. Two
new long-copy controls rendered/decoded at9.75s in16:9/9:16. The old voice was
replaced with explicit local silence for these internal stress tests (score retained),
not misrepresented as narration of the test text. Existing accepted masters remain
unchanged. Preflight also flags one accepted-film caption4s vs4.4167s; this is an
advisory difference from owner acceptance, not grounds to reopen it automatically.
