# Studio foundation — helper qualification, not a film experiment

2026-10-17. Scope: conditional A/B/C intake and local audio catalogue only. Owner
explicitly deferred selecting footage and creating a music folder. No production,
models, runtime installation, paid calls or public media upload.

## Predeclared checks

- A/B/C share the existing planner and checkpoint; source rights, claim references,
  ordered intervals, finite limits and explicit owner review remain visible.
- Unknown source video and retained audio rights block publication independently;
  removing audio does not clear video. Denied retained sources block execution.
- Pending facts, unsupported features and music account/rights gates cannot be
  bypassed through the experimental workflow. Legacy briefs preserve behavior.
- Delivery requires separate intended artifacts and operator QA evidence; planned
  outputs are neither retained files nor independently verified media.
- Private catalogue: generated1sPCM only,actual FFprobe metadata and optional
  FFmpeg mean/sample-peak window,unknown rights excluded from commercial results,
  explicit annotations,changed-byte rejection,scan-limit failure preserves old index.
- Public checkout/standalone ZIP contain no owner audio,index,source paths or models.

## Observed

Tests live in [test_studio.py](../../tests/test_studio.py); fixtures are generated
in temporary directories and removed after tests. FFprobe/FFmpeg8.0.1 were already
installed; no binary download. PCM sample mean is checked against known amplitude;
this does not evaluate LUFS,real music,beat/mood detection or final mix quality.
The full offline check and extracted-package smoke are the reproduction gate:

Observed initial run:10 studio boundary/helper tests;208 full-suite tests passed in
6.818s unittest wall time. Integrity,links,generated matrix and extracted standalone
package smoke passed. This is test-run time,not a film-production or model benchmark.

PR publication preflight found a final-probe budget overrun could return a partial
index. A regression failed before the fix;scan now checks the deadline before
returning a persistable result. Follow-up:11 studio tests and209 full-suite tests
passed (7.592s unittest time),plus the same integrity/package checks. No media run.

```sh
python3 -m unittest discover -s tests -p test_studio.py -q
python3 scripts/check.py --scope router
```

No artifact is registered in outputs.json because no film was made. Full-suite
counts describe code/helper checks,not independent model routing evaluation.
Whole A/B/C production remains not_started. Runtime/memory/cost comparisons for
real workflows remain unknown;declared future caps are not measured performance.
No licence,tool,method or combined-chain production qualification was promoted.

See [audit and next experiments](../../docs/personal-studio.md) and
[operator guide](../../skills/video-production-router/references/studio-workflows.md).
