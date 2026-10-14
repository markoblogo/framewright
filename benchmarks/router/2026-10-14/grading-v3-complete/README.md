# Protocol v3 — full current-source planning check

**52/52 strict actor passes; 22/22 blind grader controls.**
[Diagnosis](../../../../docs/grading-v3.md) · [Report](../../../../docs/router-evaluation.md).

Original 46 user requests retained; three criterion revisions are explicit in
`rubric-changes.json`. Six boundary cases were added before the initial v3 run. One malformed
completed-comparison fixture was clarified before this run; fixture-changes.json
retains its exact before/after content and hashes. The prior isolated51/52 is
retained, with all 46 original cases passing. No criterion or request was relaxed.
The old 43/46 packet is unchanged; this is development/regression, not unseen
transfer or a causal improvement comparison. All answers/grades are from the
complete new run, with no favourable per-case retries or manual overrides.

To repeat, verify the manifest/source snapshot, extract the original router, and
create separate synthetic workspaces using only `inputs.json` fixtures and exact
prompts. Omit `router/references/scenarios.json`. Set FRAMEWRIGHT_EVAL_CODEX_HOME to a dedicated local CLI home using your own
authentication, without inherited user AGENTS/config/skills. The drivers explicitly
disable discovered host skills; the retained smoke lists four bundled native skills.
No credential values belong in the packet. Apply the recorded ephemeral
read-only CLI/model configuration from `freeze.json`, no apps/plugins/web, ignored
user config/rules and no renderer/accounts. Preserve every attempted/completed
command and full before/after file set. Grade in separate contexts with actual
fixture text, protocol.txt, exact case criteria and the matching grader config.

The exact actor/grader drivers are retained as actor-runner.py and grader-runner.py.
After materialising the workspaces/prompts and retaining execution logs, prepare
complete grading batches with the repository helper:

```sh
python3 scripts/prepare_router_grading.py /path/to/local-evaluation
```

It checks frozen prompts and complete unchanged file trees, preserves the actor
permission envelope and inventory, and refuses to overwrite different retained
inputs. Inventory never grants permission. Grade with the retained grader driver.

First grade all calibration/input.json batches with gold hidden, then compare
against calibration/gold.json. The retained 22 controls were freshly assessed in the preceding identical isolated
grader setup and reused unchanged here. All 22 opaque/permuted controls must classify
correctly: source proof, rights and stage distinctions include negative examples.
The source-bound v3 gate rejects old 12-control calibration. It also rejects
INSUFFICIENT_EVIDENCE as a successful negative-control rejection. A partial actor run
cannot promote the scope. Never overwrite an active output or turn a hypothetical
plan into completed media QA.

Only machine-local citation destinations may be made fixture-relative; affected
records retain original answer SHA-256. Full raw answers/CLI streams stay on Work.
No factual answer content or grade is rewritten. Source hashes do not depend on
historical Git objects. No render, account/provider action, release or media upload.
