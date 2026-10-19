# Save and resume a production project

`project.py` stores a local brief, frozen plan, readable packet, file pins, manual
step states and history. `resume` shows where to continue; it never runs production.
Python standard library; checkpoint writes/locking are tested on macOS and Linux.
Windows, network filesystems and recovery after disk/filesystem failure are unqualified.

## Start once

From a checkout (or use the installed skill's script path):

```sh
mkdir -p local/my-film
python3 skills/video-production-router/scripts/project.py init examples/briefs/mixed-promo.json local/my-film/project.json
python3 skills/video-production-router/scripts/project.py packet local/my-film/project.json
python3 skills/video-production-router/scripts/project.py resume local/my-film/project.json
```

`init` refuses to overwrite. Source kinds are not actual files; register the files
you will use. Relative references are stored from the manifest directory; media is
not copied or committed. Keep project/media roots mounted in the same relationship.

```sh
python3 skills/video-production-router/scripts/project.py retain local/my-film/project.json approved-cover /absolute/path/to/approved-cover.png --input
```

Complete preflight/source review only after doing that work. Evidence is a manual
note/reference to observed work, not a generated proof. No tool is installed and
no licence, budget or permission is automatically validated.

```sh
python3 skills/video-production-router/scripts/project.py mark local/my-film/project.json source-review --state done --evidence 'Source claims and authorised input versions reviewed; see my source notes'
python3 skills/video-production-router/scripts/project.py mark local/my-film/project.json preflight --state blocked --evidence 'Selected runtime is unavailable; no installation authorised'
```

## Continue after stopping

```sh
python3 skills/video-production-router/scripts/project.py resume local/my-film/project.json
python3 skills/video-production-router/scripts/project.py status local/my-film/project.json --json
```

These read the saved checkpoint and hash registered files. They show ready steps,
missing/changed files, blocked work and output IDs. They never infer completion
from an existing filename, recalculate choices or run queued commands. Changed
planning sources produce a warning; the original plan stays frozen. Review it
before further production; use a new project for a changed brief/plan and preserve
the old checkpoint as evidence. This is not in-render-engine checkpointing.

After an independently authorised scene export, retain its real file using the
output ID from status. Hash registration records bytes, not a successful decode:

```sh
python3 skills/video-production-router/scripts/project.py retain local/my-film/project.json scene:1:video-export /absolute/path/to/scene.mp4
python3 skills/video-production-router/scripts/project.py mark local/my-film/project.json scene:1 --state done --evidence 'Authored/exported; native file retained; see production log'
```

A scene requires its declared outputs and completed source-review/preflight.
Its QA remains planned. For a scene requesting stills/voice too, retain those outputs
as well. Video assembly requires authored scenes and its own `final-video` file.
Separate output QA, human narration/final-master listening (or intentional-silence
confirmation),delivery,optional creative review
and publication records remain separate. `publication` stores an outcome only;
it grants no upload authority. No command uploads, generates or decodes media.

Use `mark ... --state blocked --evidence 'reason'` to record a pause; `planned`
reopens work. Changing a step invalidates downstream recorded completion. A frozen
unmet routing requirement cannot be overridden as done/planned: revise the brief
in a new project. Done always means operator-recorded, not independently verified.
Use the saved packet and [full handoff contract](handoff.md) for actual QA.

## Input changes and safe writes

Changed/missing pinned bytes block forward completion until reviewed. `retain`
refuses to replace a different existing pin without `--replace`. An accepted input
change reopens all steps; a replaced output reopens its authoring/QA and dependent
assembly/delivery/review steps. Old states and pins stay in history. Reattaching
identical bytes/path is a no-op. This is conservative dependency invalidation, not
semantic knowledge of which pixels or words changed.

Same-directory atomic replacement keeps the previous complete checkpoint on a
failed write. An exclusive OS lock rejects concurrent writers and is released on
process exit/crash; the harmless `.lock` file can remain. Do not edit the frozen
brief/plan/packet in place; their digests detect accidental drift. This is local
integrity bookkeeping, not signed attestation or a security boundary. Keep backups.

Manifests contain local paths and evidence notes: keep them in ignored `local/` or
`.framewright/`, review before sharing, and never include credentials. Cross-machine
runtime portability, media recovery and automatic production execution are not provided.

## Project memory and revision-bound observations (schema 2)

New `init` projects use schema 2. Old schema-1 projects remain readable without
modification. Upgrade explicitly: `project.py migrate local/my-film/project.json`.
The original bytes are saved as `project.json.v1.bak`; an existing backup is never
overwritten. Repeating migration on schema 2 is a no-op. If an interrupted migration
left only a backup, preserve/check it before recovery; never delete it blindly.

For a game, virtual set or existing production without a router brief, create a
manual project instead of inventing a qualified renderer or fake video plan:

```sh
python3 skills/video-production-router/scripts/project.py create local/my-film/project.json --goal 'Book virtual set and later films' --note 'Local alpha; production currently paused'
python3 skills/video-production-router/scripts/project.py asset local/my-film/project.json voice --kind narration
python3 skills/video-production-router/scripts/project.py retain local/my-film/project.json voice /absolute/path/to/voice.wav
python3 skills/video-production-router/scripts/project.py observe local/my-film/project.json output:voice --kind listening --result rejected --actor owner --provenance owner_report --note 'Owner rejected pronunciation; recording required'
python3 skills/video-production-router/scripts/project.py task local/my-film/project.json owner-recording --label 'Receive owner recording' --waiting-for owner --note 'Owner deferred recording'
```

`describe PROJECT --goal TEXT --note TEXT` updates purpose/context with history.
Manual projects share the same pins, tasks, atomic writes and journal, but their
`packet` explicitly has no tool plan. They do not qualify arbitrary game engines.
Declared assets may be pending; retaining a filename does not generate or approve it.

`task PROJECT ID --label TEXT` adds an explicit work item. `--after ID` and
`--requires OUTPUT_ID` repeat; dependencies/output declarations must already exist,
so the CLI cannot create a dependency cycle. `--waiting-for PARTY --note REASON`
records an explicit wait. Use `mark` to reopen or finish it after the actual work.
Receipt/file changes never silently remove explicit waits. Append a replacement
work item for a revised task; do not edit frozen routing requirements in place.
Use `--check-kind technical|listening|creative|provider|publication` with required
artifacts to connect a check task to its observations.

Observation subjects are `input:ID`, `output:ID`, or `project` for decisions only.
Files must be retained and match their pins before an observation can be recorded.
Kinds/results are separate:

| Kind | Results |
| --- | --- |
| technical | pass, fail, pending |
| listening / creative | accepted, rejected, pending |
| decision | accepted, rejected, deferred, proposed |
| publication | published, removed, pending |
| provider | approved, rejected, pending |

Every observation requires `--actor`, `--provenance` and `--note`. Provenance is
`owner_report`, `operator_observation`, `supplied_report` or `independent_check`;
`administrative_change` records CLI-generated pending checks without asserting QA.
Source labels are not actor authentication or verification performed by the CLI.
`--observed-at` accepts a timezone-aware ISO timestamp when actually known; otherwise
observation time stays unknown. Recording time is always retained separately.
Decisions require `--topic` so unrelated decisions cannot silently replace each other.
Project-wide decisions bind the current goal/context; artifact decisions bind bytes.

Use repeated `--depends-on input:ID` / `output:ID` to bind a receipt to relevant
source revisions as well as its target. Replacing narration does not invalidate an
unchanged image's creative receipt. A mix receipt depending on that narration
becomes stale. Input changes still conservatively reopen task completion as before;
observations are scoped separately. Dependencies are operator-declared, not inferred
from media, nested JSON references or semantic content. Register relevant sources.

The latest receipt per subject/kind/topic is effective only for matching files and
dependencies. Older/superseded/rejected/stale entries remain in the journal; an old
approval is never resurrected merely because the latest receipt is stale. Failed,
rejected, pending or stale evidence blocks a linked check; recording a failure also
reopens completed checks and their dependants, preserving authoring work. Accepted
receipts never complete tasks automatically. `resume --json` exposes current
observations, stale receipts, explicit waits, evidence blockers and labelled next
actions. `journal PROJECT --json` reads all observation and task history.

Publication observations require `--url`; `published` also requires explicit
`--visibility public|unlisted|private|unknown`. The URL is never fetched. Record the
source in provenance (e.g. owner-supplied link); no URL implies an upload grant or
provider approval. Record planned removal as a decision, not as `removed`. Actual
removal needs a prior publication entry; it does not erase technical receipts or
locally retained files. Different URLs remain separate publication histories.

The journal is append-only through this CLI, with an accidental-drift checksum.
It is not signed, tamper-proof or an authority/security boundary. Private context,
receipts and paths remain local; the CLI does not redact secrets for publication.
The frozen packet is the original planning handoff; `resume` is the current work
view. No command produces media, performs a check, downloads a model or publishes.


## Continue from script to delivery

[Production composition](production.md) adds a shared material catalogue, scene
script, separate main/Short edits and local delivery kit to the same project.
`compose` explicitly imports the current specification; `board`/`resume` expose
missing takes/narration, rights and output checks. `bundle` collects existing finals
and a review report, without completing tasks or uploading anything. Old projects
without a composition remain readable and keep their previous behaviour.

Publication removal requires a prior publication receipt for the same retained
file revision and URL. Keep older published versions as distinct retained
artifacts when replacing production files; a new file must not inherit an old
publication or removal. Routing blockers remain in `blocked`; only explicit
external parties/reasons appear in `waiting`.
