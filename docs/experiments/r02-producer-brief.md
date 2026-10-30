# R02 — one readable production proposal

28 October 2026. Internal offline CLI replay; no production, account call, upload,
paid generation or release. [Roadmap M1/R02](../roadmap.md) ·
[Contract](../../skills/video-production-router/references/producer-brief.md).

## Result

`intake.py brief` now combines the existing profile and route comparison with scene
purposes, source-index matches/gaps and optional version-bound project status.
The proposal separates declared intent, checked local file revisions, proposed
creative structure and unknown prerequisites. It never approves or starts work.

The same retained [book-promo brief](../../examples/intake/comparison-brief.json)
was replayed with two profile preferences:

| Preference | Proposal | Preserved uncertainty |
| --- | --- | --- |
| Free-only | Local supplied-media montage and local authored motion | Source index not supplied, scene purposes proposed, whole-route integration and machine fit unverified |
| Both | The same two plus conditional-licence authoring | Licence eligibility and fee unknown; no invented paid quote or turnaround estimate |

[Free-only readable result](../../examples/intake/producer-brief-free-only.md) ·
[Broader readable result](../../examples/intake/producer-brief-both.md).
These are retained planning examples, not new owner-approved productions.

## Automated checks

Public CLI checks cover the two exact Markdown replays; explicit route/voice
preferences; unavailable providers; upload and installation restrictions; missing or
invalid brief fields; declared versus proposed scene purposes; file-pinned lexical
source matches and missing matches; source drift; explicit project waits and changed
retained files; and unchanged profile, brief and project bytes. Tests use small
original fixtures; no rendering or external services are required.

Run the focused regression:

```sh
python3 -m unittest discover -s tests -p test_producer_brief.py -q
```

## Verification result

The focused R02 suite passed all 11 tests. The complete offline check on Python3.12
completed 492 tests in 288.733s, with one skipped test and no failures. Documentation
links, retained benchmark-packet integrity, generated tool-reference consistency and
a temporary standalone package build passed. The package smoke test created no tag,
upload or release. Historical model results remain unchanged; the current source is
still `not_evaluated_current_source`, not newly model-qualified.

## What this does not establish

No new model evaluation, semantic footage understanding, complete financial quote,
current subscription verification, measured labour saving or whole-route feasibility.
The catalogue remains partial. A prepared saved Blender shot requires explicit route
selection and the existing admission checks. Free-text journal decisions are retained
for human reconciliation, not interpreted as machine-enforceable creative constraints.

R02 is complete within this internal interface scope. M1 still needs an owner-selected
real proposal in R03; REL-A also needs the integrated film, targeted correction and
fresh-session recovery. This result alone does not trigger a release.
