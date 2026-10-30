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

- The route and stage must actually exist in the retained intake comparison. The local FFmpeg adapter maps to `local-media-review` or
  `review-clip`; the selected Blender picture stage maps to `saved-blender-shot`. A HyperFrames, remote generation or other stage is not silently
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
still use the project volume. Inspection/proxy/saved-shot workers inherit the host lock and
a process-group deadline, including when the executor itself exits abruptly.

## Saved Blender shot (R01)

`intake.py routes` includes `local-saved-shot`, a proposal for an existing prepared
scene. Select its `picture` stage with tool `saved-blender-shot`, a retained
`output:shot:ID:VERSION` source, and a declared `shot-preview` output. A saved-shot
execution always requires a bound selection; there is no legacy unbound bypass.
Scene creation, the rest of the recipe and final acceptance are separate work.

Use the same selection fields as above. `arguments.start/end` are **zero-based,
end-exclusive integer frames** for this adapter, not seconds. `context` remains1
and is unused; revision-request/after bounds must be null. Keep the range within the
saved shot, at most240frames/300million pixels, and worker time at most180seconds.
Split larger production work into explicitly selected bounded tasks.

Prerequisites declare `blender`, `ffmpeg`, `ffprobe`; expose the trusted installed
Blender as `blender` on PATH (or the standard macOS application location). Selection
pins resolved executable paths and hashes, the shot card, scene, resources, audio,
passport references and adapter implementation. Preflight rechecks passport status,
frame bounds, resource drift, environment, rights and zero local provider fees.
The worker rechecks executables and the existing saved-shot renderer checks inputs.
This is for trusted local scenes; it is not a sandbox for untrusted blend files,
add-ons, linked dependencies or executables, nor a hash of the entire OS/runtime.

The full render folder is kept: PNGs, job/state, logs, PCM where applicable, MP4 and
receipt. For this adapter `max_output_bytes` covers **the entire folder**, checked
during rendering and before retention. Sampling is not a hard filesystem quota: an
in-flight write can overshoot. The worker group shares the existing deadline/host
lock; failures retain diagnostics without registering the expected output. A crash
with uncertain outcome requires reconciliation before an explicit retry.

Parent-side checks decode the MP4 and verify H264, dimensions, fps, frame count,
audio presence, duration, byte allowance and receipt/source/output pins. Successful
files and the receipt are retained under new identities; artistic/listening checks
remain pending. The executor does not mark the task accepted or publish it.

Reproduce the original internal test with an installed trusted Blender (no install,
network or account access):

```sh
python3 examples/blender-stage/run_executor_probe.py --output /tmp/fw-r01 --blender /path/to/Blender
# Add --execute only to run four short sequential renders of an original fixture.
```

See [R01 evidence](../../../docs/experiments/r01-saved-shot-executor.md).
