# ComfyUI as a bounded workflow executor — 28 October 2026

Status: documentation reviewed; candidate adapter and workflow trial planned. No
installation, endpoint probe, model download, inference, custom-node install or
executor integration performed. This is not a qualified ComfyUI production route.

## Official basis

[ComfyUI documentation](https://docs.comfy.org/) describes a node-based interface
and inference engine. The [core repository](https://github.com/Comfy-Org/ComfyUI)
identifies GPL-3.0 and describes image/video/audio/3D graphs, local APIs and optional
paid partner nodes. Models, nodes, input assets and hosted services have separate
terms; free core software does not imply free or cleared workflow execution.

[System requirements](https://docs.comfy.org/installation/system_requirements)
includes Apple Silicon support using PyTorch/MPS. This is not proof that the
owner's Mac can run a specific graph. Requirements vary with model, precision,
resolution, frame count, batch size, offloading, disk/swap and dependency versions.
Recheck actual pinned build documentation; no universal minimum RAM/video claim.

[Server routes](https://docs.comfy.org/development/comfyui-server/comms_routes)
describe node inventory, statistics, prompt submission and per-prompt history.
[Messages](https://docs.comfy.org/development/comfyui-server/comms_messages) include
success, error and interruption events. A node `executed` message is not a complete
workflow-success receipt. A queued prompt is not a validated media output.

## Architectural role

Framewright chooses the production task, approved assets, budget, allowed process
and review conditions. ComfyUI runs one admitted graph. Reuse the existing
[trial/readiness contract](../../skills/video-production-router/references/trials-and-readiness.md),
project pins and [sequential executor](../../skills/video-production-router/references/projects.md).
Do not turn Framewright into a mandatory ComfyUI shell or build another scheduler.

Qualification unit: **workflow revision + model/node revisions + parameters + tested
environment + observed outputs**, never “ComfyUI works” for every modality.

## COMFY-01 — proposed card and adapter contract

[Draft workflow card](../../examples/comfyui/workflow-card-template.json) is a
non-executable planning template, not an implemented validator or runnable graph.
It records:

- Task, input/output contract, graph path/hash and permitted parameter overrides.
- Core/Python/PyTorch/backend versions; every model's revision/hash/terms and every
  custom node's source/revision/terms. First test uses built-in nodes only.
- Tested OS/architecture, memory/disk/backend evidence, settings, seed and observed
  elapsed time, peak-resource measurements or explicit unknowns, failures and limits.
- Actual run ID, source/output pins and separate technical and human review.
- Local/hosted boundary, provider/model/asset rights and execution authority.

Preflight must verify the exact approved graph and allowed node types/parameters,
matching model hashes, local server/build/backend, required nodes and sufficient
known resource margins. File presence or a reachable server alone is insufficient;
untested peak memory stays unknown. Reject changed/missing requirements before
submission. UI workflow JSON and API prompt JSON must not be confused.
No automatic custom-node install/update, model download, paid partner node or upload.
Cloud/remote execution is separately authorised, not a fallback for local failure.

On explicit execution, admit one prompt only and retain its ID before monitoring.
Record validation errors, runtime failure, timeout, interruption, disconnection and
ambiguous submission separately. An unknown submission outcome needs reconciliation
against the server, not a blind resubmit. Match status/history to the actual prompt,
then verify expected output paths, file hashes and media integrity. Progress or an
old cached file must not complete the task. Track cache use and actual seeds/settings;
seed alone does not promise byte-identical output across hardware/versions.

Use the existing host/project lock and a dedicated idle local worker for the first
test. Never clear another user's queue or blindly invoke a server-wide interrupt:
prove ownership/isolation before cancellation. After failure retain evidence and
partial files as unaccepted; stop for a decision. No automatic paid retry or silent
reduction of resolution, frames, model or quality to make a run fit.

### First bounded acceptance trial

1. Choose a concrete useful image workflow and exact model only after checking
   available local resources and terms; prefer already available approved weights.
   Keep one small still, batch one, modest resolution and a fixed runtime limit.
2. Reuse the trial/readiness machinery; implement one allowlisted adapter path with
   a preview of graph/inputs/settings before any authorised run.
3. Test missing model/changed graph, one normal output and controlled failure or
   cancellation. Exercise timeout/disconnected-submission handling with synthetic
   server responses before risking another real inference.
4. Inspect the output and retain resource/time measurements plus human review.
   Repeat the admitted graph with the same settings and document variation/cache use.

Pass: the exact graph completes with valid output and honest resource evidence;
failures stop cleanly without false completion, duplicate jobs or unrelated queue
changes. Only that bounded scope becomes eligible for catalogue promotion.
Video/audio/3D workflows each need separate cards and real tests. A lightweight
no-model server smoke check may validate plumbing only, not generative capability.

## Priority

SOURCE-01 reuse and PREVIS-01 cheap staging remain preferred when they meet the
brief. COMFY-01 supplies missing generative material for a selected production need.
Models and large downloads remain outside Git. Integration is planned; current
executor support remains limited to its existing allowlisted local actions.
