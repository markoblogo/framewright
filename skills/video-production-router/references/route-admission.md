# Selected route → local execution admission

[Bounded trial](../../../docs/experiments/route-admission.md). This bridge binds one
explicit local action to a selected stage in an actual intake comparison. It is
not a whole-recipe renderer or paid-provider dispatcher. Existing manual executor
commands remain available; a **bound** task cannot skip its admission by omitting
an extra flag. Selection, admission, production, quality and publication stay distinct.

## Reproducible original-fixture example

Python3 and trusted installed FFmpeg/ffprobe are required; nothing auto-installs.
Choose a new private folder outside the repository:

```sh
python3 examples/admission/prepare_demo.py /tmp/fw-route-demo
python3 skills/video-production-router/scripts/admission.py check /tmp/fw-route-demo/project.json --step inspect
python3 skills/video-production-router/scripts/executor.py /tmp/fw-route-demo/project.json --step inspect --source input:source --output report
python3 skills/video-production-router/scripts/executor.py /tmp/fw-route-demo/project.json --step inspect --source input:source --output report --execute
```

Preparation generates one second of original silence and a fictional free-only
profile/brief, compares existing catalogue recipes, retains the comparison and
requirements, then binds `local-media-review` to the selected FFmpeg finishing
stage. Preparation does not run the media worker. The check command is read-only;
it runs fixed local version queries and a bounded source metadata probe. It is
not consent to execute. `--execute` rechecks actual conditions under the normal
project/host locks, then persists admission evidence and a durable execution intent.

Successful output remains **review_pending**. The script does not approve a film,
transcribe, install software, query accounts, send media, spend or publish.
This synthetic example is not the product's full first-film onboarding proof.

## Binding an existing project

Declare a task and compatible unoccupied output, retain the actual route-comparison
JSON and the environment requirement manifest as project outputs, and retain the
actual source. Write an explicit selection using
[the example](../../../examples/admission/selection.json):

```sh
python3 skills/video-production-router/scripts/admission.py select PROJECT.json SELECTION.json --output NEW-BOUND-SELECTION.json
```

All task/source/output/tool/arguments are explicit, with a worker timeout1–180s,
positive output byte allowance, an optional declared available-RAM requirement and
an exact-decimal provider-fee maximum/unit. Unknown required RAM blocks admission;
null or zero means unconstrained, **not measured sufficient**. Existing environment
manifest checks retain total-RAM/disk/OS/architecture/program/model/manual semantics.
No threshold or model-fit claim is invented from the host's current footprint.

The selection is retained as a separate artifact and bound to that task in the same
project with an integrity hash. It pins the comparison, source and requirements,
plus implementation/cost-classification fingerprints. No existing selection, output
or approval is overwritten. A changed source, requirement, contract, action,
parameter or adapter implementation requires a newly reviewed task/selection.
Do not repin the contract alone to circumvent the binding. New-task selection still
needs explicit execution; no old approval is inherited.

## Checks and current scope

- The route and stage must actually exist in the retained intake comparison. Only
  the known local FFmpeg adapter currently maps to `local-media-review` or
  `review-clip`. A HyperFrames, remote generation or other stage is not silently
  substituted. Other route stages remain unexecuted/unqualified.
- Task/dependencies/waits, exact retained bytes and invocation match must hold.
  Fresh fixed local version probes, declared environment checks, source rights and
  current available memory/disk observations are separate evidence. Actual timed
  media and a selected video interval are checked by a10s local-only metadata probe.
- Cost admission currently requires **known zero local software provider fee** in
  the same unit. Unknown fees stay null and block; positive/unknown provider charges
  have no dispatcher. The project cost ledger is included as context, without
  treating another unsettled operation as this free action's charge. No currency
  conversion, prepaid-credit inference, automatic reservation or real billing cap.
- Expected output identity/kind/format is explicit in the retained contract.
  JSON source binding/schema or fixed MP4 proxy format/interval and maximum bytes
  are checked before retention. Worker timeout stops its owned process group.
  Byte allowance is a **postcondition**, not a filesystem quota; declared disk
  requirements must cover temporary intermediates and actual peak space. The fresh
  disk floor is checked on both the project volume and the actual runtime temporary
  volume. A full system temporary volume can block work even with a free external
  project disk. Set an explicit permitted TMPDIR before launching when appropriate;
  the helper never moves/deletes user files or changes system settings. Preflight
  queries are separately bounded, outside worker time. Available RAM is a snapshot,
  not a hard memory cap or a render/model performance guarantee.
- Admission history is not a successful creative/technical film review. A worker
  failure keeps the expected output unretained and records a failed attempt;
  ambiguous interruption retains recovery requirements. A produced output is
  not overwritten or automatically rerun. Viewing/listening/final choice still
  use the existing exact-revision journal.

Future adapters need their own executable/format/resource/rights/cost contracts and
trials. Paid/external actions additionally need authority, reservations, provider
job identity/reconciliation and ambiguity handling. This implementation does not
supply a transport sandbox, remote idempotency or a general generation scheduler.

Relative model paths preserve the retained manifest directory; output disk checks
still use the project volume. Inspection/proxy workers inherit the host lock and
a process-group deadline, including when the executor itself exits abruptly.
