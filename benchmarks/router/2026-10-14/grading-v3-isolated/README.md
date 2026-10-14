# Isolated protocol-v3 run — 51/52

All46 original cases pass. One of the six added development fixtures is malformed:
`completed-comparison-v3` asks to compare two claims but never supplies their text.
The actor successfully reads the facts, correctly requests the missing claims,
and does not falsely claim the comparison was completed. The strict grader still
fails its completed-comparison criteria. This is a test-input ambiguity, not a
verified router defect; no model grade is manually overridden.

The [final complete rerun](../grading-v3-complete/README.md) clarifies just this
synthetic product fixture with explicit candidate claims before launching all 52
new actors. `fixture-changes.json` in that packet retains before/after text and
hashes. Original46 inputs, requests, criterion strings and router source stay fixed.
No favourable answers are stitched across these runs.

All22 blind controls are freshly graded under the isolated configuration and match
strict expected verdicts. The final run reuses that unchanged calibration with
identical protocol/core grader/model/host context. The four native system skills
shown in isolation-smoke.txt remain visible; the user-local catalog/config/AGENTS
do not. All actual attempts in this run remain inside authorised fixture paths
and allowed offline helpers. No renderer/provider/account/spend/upload occurred.

The exact source snapshot, prompts/fixtures, full answers, tool attempts/completions,
original-output hashes, model grades and CLI drivers are retained. Machine-local
citation/diagnostic paths are minimised with original hashes; raw streams remain on
Work. Earlier50/52 and49/52 records remain, and do not qualify this source as a full
pass. No unseen-transfer, production-permission, media-quality or release claim.
