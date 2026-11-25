# Video Shot Breakdown follow-up — Radar 17 Copilot Connectors

25 November 2026. Owner authorised a 12-second horizontal silent pilot only. [GitHub Changelog, 18 Nov](https://github.blog/changelog/2026-11-18-connect-supabase-box-calendly-and-more-to-copilot/) confirms eight additional GitHub-verified MCP connectors in public preview. Connect, read and write are an original synthetic permission metaphor, not an observed Copilot approval sequence. No accounts linked, permissions granted, production data touched, or external tool actions executed.

## Pilot and exact comparison

Original cardboard isometric diorama: projected extruded geometry, kraft/plum/lime, moving connector halves, read-copy movement through a door with the original retained, and an edit moving through a permitted-write doorway to change the original. Local Pillow/FFmpeg recipe; not an externally generated scene or product UI. Opening and closing stages corrected locally for label separation and result hold. Owner subsequently confirmed the three states were clear and the style acceptable but not a personal favourite; requested two geometry corrections and livelier full-film pacing. See [full film case](../productions/copilot-connectors.md).

Selected private pilot: `productions/radar-17-copilot-connectors-2026-11-25/review/copilot-connectors-pilot-v3.mp4`, 12.000 s, 1280×720, 30fps, 360 H.264 frames, no audio; SHA-256 `89d619f6e65f7ece140f872db50d08d0443b926e73f9aa77829c818f3c98b5d5`. Known authored cuts at 4s and 8s per edit/storyboard.json. Six representative frames inspected; full decode in package builder.

Reused local upstream Video Shot Breakdown at MIT commit `f8efbc6ff93eaaf21942917dc243249f350175af`, isolated Python 3.12.8/Pillow 13/openpyxl 3.1.5, FFmpeg. No paid calls or new dependency installed.

| Condition | Observed output against reference |
|---|---|
| Default scene threshold .32 | Exit 1 at candidate-image extraction (FFmpeg returned 234), 12 time-sampled references retained, no candidates file. Both expected cuts were below the threshold. |
| Tuned .04 | Exit 0. Candidate boundaries exactly 4.000 and 8.000, no extra candidates on this input. 2/2 known cuts. |

Threshold was informed by v2 scene-score diagnostics (.089547 and .055180 at authored boundaries, next-highest .013689); the final v3 check is on the same designed scene family, not an independent generalization trial. A low threshold is not universally suitable. The default failure is not an empty successful report. Shot names/interpretations remain authored; extraction does not infer meaning.

Raw upstream learning workbook reopened with 4 sheets, 3 shots, 3 embedded keyframes (3/7/11s from actual tuned-run samples), SHA-256 `0e37925a1bc07fa3e5ddbb0a34a37fe8e9a2e2f7a73ea8fa3ad1d7b7689a3abf`. An annotated copy adds an English Boundary comparison sheet, three rows and proportionally fitted 240×135 thumbnails preserving 16:9. Reopened with 5 sheets, 3 comparison images and exact cut cells; SHA-256 `27447d2334a7dc46735e3e4ef42ffcc9d883de487a3b2ab73333df37c286c92a`. Raw workbook Chinese headings and original fixed distorted thumbnails remain unchanged. No replication workbook. Human review of workbook legibility pending.

Retained private evidence: edit/render-pilot.py, edit/storyboard.json, sources/source-note.md, evidence/pilot-contact.jpg; evidence/shot-breakdown/{032,004} outputs and logs, comparison.json, raw analysis and workbook receipt; review/delivery.json and XLSX. No pilot publication. Owner reviewed pilot and authorised full-film production with corrections; the shot-analysis workbook has no separate owner evaluation. Full candidate and acceptance wait are recorded in the linked production.
