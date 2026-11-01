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
