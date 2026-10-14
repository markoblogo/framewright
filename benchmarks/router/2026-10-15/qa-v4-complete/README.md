# Five transfer findings fixed; complete protocol-v4 regression — 2026-10-15

**Original five:5/5 pass. Strict complete result:67/70** — prior52 **52/52**,
last18 **15/18**. **40/40 blind grading controls** with complete source context.
Three remaining strict misses are retained below; current status is **evaluated_with_gaps**.
No render, provider/spending action, media publication, version bump, tag or release.

This is known-case development/regression, not an unseen test or causal improvement
score. The original [13/18 first-exposure packet](../transfer-2/README.md) and its
answers/criteria/grades remain unchanged. No manual verdict overrides or favourable
answers stitched across source revisions.

## The five corrections

| Retained finding | Correction | Final case |
| --- | --- | --- |
| PNG transparency QA omitted | Inspect each alpha-bearing output's decoded channels and light/dark composites; a WebM trial cannot cover PNG | transparent-overlay:PASS |
| Film-burn temporal QA omitted | Inspect flashes/flicker, transition boundaries and readability; agree intended artistic/comfort acceptance | data-noir:PASS |
| Effect-removal fallback ambiguous | Preserve original settings; removing/replacing a requested effect stays a proposal until accepted | vfx-composition-collision:PASS |
| Negative interactive-MP4 comparison penalised | A supported no-fit answer may stop; gate an alternative only when it is proposed for adoption | interactive-mp4:PASS |
| Negative stream-copy comparison penalised | No unsolicited relaxation tutorial; adopting transcoding or another deliverable remains conditional | copy-only-incompatible-streams:PASS |

[Exact two criterion changes](criteria-changes.json) and [protocolv4](protocol.txt)
were frozen before actors. Two **unchanged original answers** independently pass
regrading2/2 with those criteria: [inputs](comparison-replay-inputs.json),
[grades](comparison-replay-grades.json), [provenance](comparison-replay-provenance.json).
That replay is separate from the70-case score and does not rewrite old13/18.

## Additional diagnosis and retained history

The [first complete v4 run](../qa-v4-initial/README.md) scored **67/70** on source
028d9f4: last18 passed18/18; the older52 exposed one real QA omission and two
INSUFFICIENT_EVIDENCE grades. Source-master preservation was promised without an
explicit verification check. The final decision source adds original-hash, approved
working-input and decoded timing/content checks, without equating AAC bytes with WAV.

The two physics conclusions lacked text evidence **in the grader input**, not the
actor's reads. The context preparer now retains frozen shared decision text, checks
its hashes and withholds scenario gold. This corpus supports fact-checking, not
claims that the actor read it or performed media QA. Successful matching read events
remain required. The validator checks the corpus against the frozen source and
requires identical calibration/actor grading context for protocol-v4 qualification.

Two complete actor rounds are retained, each one answer per case on a distinct
frozen decision source. The final round first received incomplete-context grading;
all those [preliminary grades](preliminary-grades.json) are retained. We then supplied
the complete corpus, freshly calibrated40 controls, and **regraded all70 unchanged
final answers**, not a favourable subset. [Context history and run hashes](grading-context-history.json).
No criteria were relaxed for that context correction. One initial grader batch
also timed out before any answer; its retained interruption is disclosed in the
initial packet. No same-source actor retries.

## What remains — no adjusted green score

- **stems-rebuild:** no explicit phase/coherence/cancellation inspection, although
  alignment, sum/master comparison and listening are planned. A specific QA gap.
- **watercolor-loop:** the frozen rubric requires readability even though the answer
  proposes no text and plans artwork detail/framing checks. Applicability is disputed.
- **upgrade-history-rights:** the answer retains native song-card identity and
  separates availability from rights, but omits an explicit documented-capability
  label demanded by the criterion. The explicitness requirement is disputed.

[Adjudication](adjudication.json) separates these interpretations from exact grades.
All five original cases pass. All70 tool-role choices and observed action boundaries
pass controller review; that does not compensate for these three rubric misses.
Current qualification retains gaps. Future fixes need a new declared version/run;
these70 are now known. Do not generate favourable retries or change this score.

## Reproduce / integrity

[Manifest](manifest.json) · [cases](cases.json) · [exact inputs](inputs.json) ·
[answers and all attempts](results.json) · [grades](grades.json) · [summary](summary.json) ·
[source snapshot](source-snapshot.zip) · [shared grader sources](decision-sources.json) ·
[calibration](calibration/manifest.json).

Extract the source snapshot into each synthetic workspace as router/, excluding
references/scenarios.json, then restore that case's fixtures and exact prompt.
The source commit is in freeze.json; the snapshot also works in a shallow clone.
Use actor-runner.py with Codex CLI0.162.0-alpha.17.2, gpt-6.1-sol medium, fresh
read-only contexts, ignored user config/rules, apps/plugins/web/multi-agent off,
and host skills disabled. A dedicated FRAMEWRIGHT_EVAL_CODEX_HOME holds your own
authentication outside Git. These invocations need the operator's model authority.

For accepted grading, reconstruct six-case calibration batches from calibration/input.json;
copy protocol.txt to GRADE-PROTOCOL.md and decision-sources.json to grade-input/.
Keep gold hidden, run grader-runner.py and compare all40 exact control verdicts.
Prepare actor records with scripts/prepare_router_grading.py; copy the same shared
source corpus into grade-input and grade all complete batches in separate contexts.
Retain all attempts and independently inspect action scope. A blocked attempt still
counts; a source-text read never establishes media/rendering QA.

Repository checks: python3 -m unittest discover -s tests -q;
python3 scripts/check_router_evaluation.py --root benchmarks/router --qualification router-qualification.json;
python3 scripts/validate.py. These verify code/evidence, not a fresh model run.

## Limits

Same-family actors/graders and chosen known cases are not independent certification
or a reliability estimate. No runtime, media quality, production privileges or
provider integration was tested. Token/worker totals exclude calibration/grading
and are not billing; monetary cost is NOT_AVAILABLE. Local citation/diagnostic
paths are minimised with original hashes; full raw streams remain on Work.
