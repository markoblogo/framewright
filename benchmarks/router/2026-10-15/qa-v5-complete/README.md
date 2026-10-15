# Stem phase QA and content-aware grading — protocol v5

**Model rubric:70/70. Evidence-complete cases:62/70. Blind controls:46/46.** Focus cases:
stems-rebuild PASS, watercolor-loop PASS, upgrade-history-rights PASS.
Separate replay of the two **unchanged old disputed answers:2/2**. No rendering,
provider/account/spending actions, media publication, tag, version bump or release.

This is known-case development/regression, not an unseen test or general reliability
claim. The previous [67/70](../qa-v4-complete/README.md), its grades and original
[13/18 first-exposure](../transfer-2/README.md) remain unchanged. No adjusted old score.

## Three fixes

| Finding | Layer | What changed / retained boundary |
| --- | --- | --- |
| Stem mix lacks explicit phase/cancellation QA | Router music and handoff guides | Inspect relative alignment, polarity/phase and stereo/mono sum for cancellation; compare recombination against approved master at matched level. Do not assume perfect nulling, zero phase difference or automatic corrective authority. Inspect WAV and encoded AV independently. |
| Readability penalty on artwork with no text | Case criterion and protocol | Plan decoded seam, crop/framing and artwork clarity. Text legibility is required when text/labels are proposed; no-text artwork does not need imaginary caption QA. |
| Suno native-card status penalised for missing a word | Case criterion and protocol | Accept equivalent technical-export/rights distinction. Retain native-card possibility, unverified actual access/inspection and separate commercial clearance; no requirement for the literal label documented. |

[Exact two criterion changes](criteria-changes.json) · [versioned protocol](protocol.txt).
The stem criterion itself was not relaxed. Calibration negatives still fail when
phase QA is omitted, proposed titles lack legibility QA, or a rights restriction is
misrepresented as technical failure. Prior40 controls remain, including source-read,
consent, output-specific QA and rights boundaries; six new controls cover these fixes.

## Frozen sequence

1. Freeze all70 known requests, authority envelopes, criteria, repaired decision
   source, complete shared fact corpus, protocol and grader configuration **before**
   actors. The source commit and exact hashes are in [freeze.json](freeze.json).
2. Freshly grade46 opaque/permuted controls in isolated contexts, gold hidden. Compare
   exact PASS/FAIL expectations; all46 match before actor launch.
3. Run all70 actors once on that source in ephemeral read-only contexts with source
   fixtures only. Withhold scenarios/criteria/gold; apps/plugins/web/multi-agent off,
   user config/rules ignored, host skills disabled. Before/after hashes retain all files.
4. Grade complete six-case batches in separate same-family contexts using full actor
   prompts, source facts, inventories and every attempted action. Frozen shared decision
   text is fact context, not proof that an actor read it; matching completed reads are
   still needed. The controller reviews every actual attempt and semantic tool-role fit.
5. Replay the two old disputed answers unchanged under v5: [input](comparison-replay-inputs.json),
   [grades](comparison-replay-grades.json), [provenance](comparison-replay-provenance.json).
   Both pass; this separate replay is not part of the70-case actor score.

No favourable same-source actor retries or manual grade changes. [Focus/remaining
findings](findings.json) retain every strict miss if present; qualification status remains
evaluated_with_gaps. No successful components or correct tools compensate for omitted checks.

## Trace completeness — retained technical gap

Final exhaustive integrity checking found eight cases with a started read lacking
its terminal event before turn.completed. These are CLI trace gaps, not replacements
for model rubric grades. No unsafe command was observed, but outcomes are unrecorded:

- explicit-paid-no-authority: item_6
- unverified-qa-note: item_2
- execution-request-handoff: item_2
- screenshots-explicit-flute: item_2
- three-style-blocks: item_2
- locked-score-frames: item_2
- commercial-free-song: item_2
- storyboard-single-shot-skip: item_2

The three requested fixes have complete traces. Other reads completed and model
criteria passed; the missing calls remain attempts, not evidence of access. Preserve
all raw stream hashes and every event. No completion is synthesized, no affected
actor is retried and no favourable score is stitched across attempts.

Model grades stay70/70. Complete-evidence counting stays62/70 and current scope
remains evaluated_with_gaps. The validator accepts an exact explicit missing-event
declaration **only as a failed/INSUFFICIENT_EVIDENCE case**. Unannotated omissions
still error; a declaration cannot qualify a case. New regression tests enforce both.
No renderer or service test is inferred from this record.

## Inspect / reproduce

[Manifest](manifest.json) · [cases](cases.json) · [exact inputs](inputs.json) ·
[answers/attempts](results.json) · [grades](grades.json) · [summary](summary.json) ·
[source snapshot](source-snapshot.zip) · [shared fact corpus](decision-sources.json) ·
[calibration](calibration/manifest.json).

Extract the snapshot into each workspace as router/, withholding references/scenarios.json.
Restore only that case's supplied fixtures and exact prompt from inputs.json. Use
actor-runner.py with Codex CLI0.162.0-alpha.17.2, gpt-6.1-sol medium, and a separate
FRAMEWRIGHT_EVAL_CODEX_HOME with your own authentication outside Git. Model runs need
the operator's authority. Current source hashes and snapshots support shallow clones.

For grading, copy protocol.txt as GRADE-PROTOCOL.md, restore calibration batches from
calibration/input.json (six records each), and copy the same decision-sources.json
into grade-input/. Use grader-runner.py; keep gold hidden and compare all46 control
verdicts before actors. Prepare actor batches with scripts/prepare_router_grading.py;
its shared corpus must match calibration byte-for-byte. Record all attempts. A
sandbox-blocked action still counts; a catalogue read is not completed media QA.

Run python3 -m unittest discover -s tests -q,
python3 scripts/check_router_evaluation.py --root benchmarks/router --qualification router-qualification.json,
and python3 scripts/validate.py for code/evidence integrity, not a new model run.

## Limits

Known cases and same-family actors/graders are not third-party certification or an
estimate of unseen reliability. No real stems were decoded, phase measured, render
performed, service integration promoted or execution permissions qualified. Those
checks remain future production QA. Token/worker totals exclude calibration/grading;
monetary cost is NOT_AVAILABLE. Machine-local diagnostic/citation paths are minimised
with original hashes; full raw streams remain on Work. VERSION stays0.1.1.
