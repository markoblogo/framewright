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
