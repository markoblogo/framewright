# REVERSE-VIDEO-01 — local reverse-video fixture

25 November 2026. [Research](../research/reverse-video-2026-11-25.md). Three known 4s segments concatenated into one silent 1280×720 24 fps H.264 12s edit: owner-provided Blue Lagoon photo (digital push-in), 4s of studio's recorded browser-game review (source offset 111s, displaying rendered 3D content), then studio's code-rendered process animation. Authored boundaries 4.000s/frame 96 and 8.000s/frame 192. No new game play or footage upload. Private folder: `productions/reverse-video-2026-11-25` under canonical external studio. Fixture SHA-256 `2bb1229bac497a880dd77e16f513881114f7dff0cc2357136fa01e9360ac0e57`.

## Observed result

| Shot | Known production route | REA pixel-statistics inference | Boundary |
|---|---|---|---|
| 01 | Moving still photo | still image + pan/zoom, 86% | 0–4s correct |
| 02 | Screen recording of 3D browser game | 3D render, 57%; alternative code/template, 26% | 4–8s correct |
| 03 | Code-rendered motion | code/template render, 80% | 8–12s correct |

REA 2/2 cuts exactly, no extra cut in this fixture. Its inferred screen-capture production route is not identified correctly; content and capture method are distinct. Confidence percentages are the tool's own heuristic outputs, not calibrated probabilities. First shot's real vs generated provenance remains open in tool report. The initial FFmpeg scdet threshold 10 yielded only 8s; threshold 3 yielded 6.75, 7.916667 and 8s (missed 4s and introduced two false detections). This is one tested setting/input, not a broad ranking. REA emitted report.html, breakdown.json, shot frames/storyboard and VIDEO.md with inferred markers and questions. videomd 1.2.0 check accepted package conforming to VIDEO.md 1. Does not prove its semantic claims or original edit recovery.

## Reproducibility and limits

[REA source](https://github.com/JuneYaooo/rea-video) 0.1.0 commit `c11f1bd8fd3edd26a40e8f45be828be685417700`, isolated Python 3.12.8 environment on Mac; numpy 2.5.5, OpenCV-headless 4.14.0.94, Pillow 13.0.0, PyYAML 6.0.4, ONNX Runtime 1.32.0 and videomd 1.2.0. Source/venv in task-specific external scratch. The CLI ran decompose with --lang en --no-vlm --no-ocr --no-asr --no-speakers --no-packaging --no-moments --workers 2. Initial setup downloaded dependencies and the YuNet face ONNX model automatically (hash `8f2383e4dd3cfbb4553ea8718107fc0423210dc964f9f4280604804ed2552fa4`); no external inference or media transmission observed or requested. Silent input bypassed audio stem models. Run log reported 14.8s after initialization; not a timing benchmark. No paid purchase; local compute unpriced. No generation, automatic remake, system installation or cloud inference. Inspect each dependency/weights license before redistribution.

Retained REA output hashes: breakdown.json `f81ace849800fa913dca614a5362a67cd4ecc3c708a4ccb76f32df730298b8d3`; VIDEO.md `bba089ac58926f5295c4e12dbe676e4964d82166420149d10271259c5ecf7439`; report.html `9847679ecd27040c1d3b4ba6f5364a07871684c39b172aee3176745fba103fdc`; run log `e58fb37766a0f01645acbd227903df2d91e7e89effd8062e333ab4633e8ba2be`. Retained source clips, exact outputs and native report screenshots are private, not Git. No owner creative acceptance or audience evidence. Next test richer transitions and known live action/AI/capture provenance, human correction, audio and a verified boundary-only OTIO conversion; compare FrameLens on the same baseline.

26November follow-up: [VIDEO.md boundary-only OTIO and cold reopen](video-md-otio-reopen-2026-11-26.md) passed with the same unchanged fixture; all288comparison frames match. Current GUIeditor import unconfirmed; this does not validate REA production-route inferences or recover layers.

27November applied follow-up:[Slow Roads74s known edit](slow-roads-road-background-2026-11-27.md):8/9editorial cuts exact;nearest41s detection−267ms;extra native settings/fade boundaries. Known game footage mislabelled as live action/AI. Same bounded navigation use;audio/semantic route remains unqualified.
