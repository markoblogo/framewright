# Experiment workbench and local readiness

Two local helpers extend the existing [project journal](projects.md), not a second
project database. Python 3.11+ standard library; no model, renderer, installation,
account, upload or publication is invoked. All file writes require explicit paths.

## A complete offline example

From the repository, choose a new local directory with an existing parent:

```sh
python3 examples/trials/run_demo.py --output /tmp/framewright-trial-demo
```

The example creates original **text fixtures**, a project, an environment snapshot,
one experiment card and an A/B review folder. It measures whether a text marker
survives; it is not a media/tool-quality experiment. The intentionally bad baseline
does not disqualify the passing candidate. No owner approval is fabricated; status
stops at `ready_for_owner_review`. Files, measurements and source pins are inspectable.
[Example details](../../../examples/trials/README.md).

## Inspect the environment before attempting a method

```sh
python3 skills/video-production-router/scripts/environment.py local/requirements.json --output local/environment.json
python3 skills/video-production-router/scripts/environment.py local/requirements.json --probe-versions --probe-hardware --output local/environment-probed.json
```

Requirements JSON has `id`, `platforms`, `architectures`, `min_memory_gib`,
`min_free_disk_gib`, `programs`, `models`, `manual_checks`, `rights` and `cost`;
optional `backends` contains `cpu`, `cuda` or `metal`. Empty platform/architecture
lists mean unconstrained, not compatible with every model. Example:

```json
{
  "id": "local-speech-sample", "platforms": ["Darwin"], "architectures": ["arm64"],
  "min_memory_gib": 8, "min_free_disk_gib": 2, "backends": ["cpu"],
  "programs": [{"name": "python3", "minimum_version": "3.11"}],
  "models": [],
  "manual_checks": [{"id": "selected-export", "status": "unknown", "basis": "No export test yet"}],
  "rights": {"status": "unknown", "basis": "Exact build, assets and use not reviewed"},
  "cost": {"status": "unknown", "amount": null, "currency": "USD", "basis": "No current quote"}
}
```

Models are explicit `{id, path, sha256}` regular files; paths resolve relative to
the requirements file, hashes may be null. No directory scan/download/model import.
An existing nonempty file without a required hash passes presence only, not identity
or inference. RAM is total system memory, disk is free space on the requirements
file's volume; neither proves model fit or accounts for transient load/other volumes.

Without probe flags, the helper checks program discovery only; a required minimum
version stays unknown. Version queries are fixed for `python3`, `node`, `ffmpeg`,
`ffprobe`, `blender`, `rhubarb`; manifests cannot supply commands or arguments.
Blender can also be found at its standard `/Applications` executable. Explicit
hardware probing uses local driver/system queries, not a model. CUDA/Metal hardware
presence does not establish a compatible framework or successful inference. Record
that separate prerequisite under `manual_checks`; export is never inferred from
an installed executable. Only trusted installed programs should be probed.

Technical status is `ready`, `needs_preparation` or `unknown`, **relative to declared
requirements**. Rights (`unknown`, `allowed`, `restricted`) and cost (`unknown`,
`free_local`, `quoted`) remain supplied declarations with mandatory basis. Unknown
amount is null; local no-provider charge is zero, not a claim of zero electricity or
operator cost. Quotes are not paid usage or spending permission. `next_step` is a
proposal; `execution_authorized` is always false. Outputs are new files, never
overwrite a checkpoint, existing file or symlink. Snapshots are private, time-bound
evidence; do not publish local paths or treat them as a monitor of later changes.

## Define a bounded A/B question

Retain selected real sources and declare actual outputs through `project.py` first.
The experiment specification contains:

- `id`, `tool`, **bounded** `capability`, `question` and distinct retained `sources`;
- `baseline` / `candidate`: `method` and non-executable `settings` objects;
- distinct `criteria`: `id`, `kind` (`technical`, `listening`, `creative`), `description`;
- `limits`: `max_cost`, `currency`, `max_seconds` (unknown ceilings may be null).

```sh
python3 skills/video-production-router/scripts/trials.py plan local/project.json local/trial-spec.json --output local/trial.json --actor operator
```

This retains `output:trial:ID` and a proposed decision, pinning the exact source
revisions. A second plan with the same ID is refused. No run, approval, or source
lineage is inferred. State that a saved-case backfill is retrospective; do not
invent its historical environment, processing time or cost.

## Collect a comparison

An observations JSON contains a new attempt `id` plus `baseline` and `candidate`.
Each arm supplies retained `output`, the identical `sources` list, retained
`environment` report or null, actual `elapsed_seconds` or null, `cost` with amount
or null and explicit currency/unit, and a map of all criterion IDs to:
`{result: pass|fail|pending, note, evidence: [retained subjects]}`.
Pass/fail requires retained evidence. These are supplied checks, not automatic
semantic evaluation. Source-list equality is an attestation, not proof of derivation.

```sh
python3 skills/video-production-router/scripts/project.py retain local/project.json run-observations local/observations.json --input
python3 skills/video-production-router/scripts/trials.py compare local/project.json output:trial:ID input:run-observations --output local/comparison-001 --actor operator --provenance supplied_report
python3 skills/video-production-router/scripts/trials.py status local/project.json output:trial:ID --json
```

The new folder contains copied, hash-checked A/B artifacts, `review.html`, a readable
`comparison.md` and the pinned `comparison.json`. Native HTML image/audio/video
controls depend on the browser codec; non-media fixtures are download links. This
does not decode, transcode, synchronise or independently judge either artifact.
All copies/reports become ordinary project artifacts; the comparison decision binds
sources, outputs, evidence and environment. Existing files/folders are never replaced.
Large selected masters are copied; check space first or select existing short excerpts.
No server is started and nothing is publicly shared. Open the local review file,
or explicitly serve only the intended review folder on localhost if needed.

Failed candidate checks, pending checks, unknown actual time/cost, currency mismatch,
unready/unknown environment, unresolved rights/cost and exceeded summed arm limits
remain blockers. A snapshot older than 24 hours or over five minutes in the future
does not establish current readiness for admission; saved historical comparisons
remain viewable. Time totals are reported arm processing time, not measured end-to-end
production efficiency. Failed baseline checks remain visible but do not alone block
a passing candidate. No automatic currency conversion or unknown-to-zero conversion.

## Review and retain only the confirmed scope

```sh
python3 skills/video-production-router/scripts/project.py observe local/project.json output:trial-result:ID:ATTEMPT --kind creative --result accepted --actor owner --provenance owner_report --topic trial-review --note 'Actual owner decision and limitations'
python3 skills/video-production-router/scripts/trials.py status local/project.json output:trial:ID --json
```

Record that acceptance only after the actual decision; the demo does not run it.
When all gates pass, status proposes the exact tool/capability/evidence for **manual
scoped catalogue review**. It never edits tool qualification, tools.json, rights,
production approval or publishing state. A later pending/rejected owner review
overrides acceptance. A changed/repinned input, output, report or review copy stales
the attempt; old acceptance never returns. New attempts have new IDs, preserve old
files and require their own review. The latest attempt remains authoritative even
when it becomes stale.

This complements [precise revisions](revisions.md), [project summaries](project-insights.md)
and [arsenal search](arsenal-search.md). Structural and fixture tests qualify the
helper behaviour only; real method quality still needs its bounded production trial.
