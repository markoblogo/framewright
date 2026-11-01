# Start / continue / correct

Choose the task below. [Current priorities](next-cycle.md) track ongoing project work;
[roadmap](roadmap.md) governs priorities and release gates. Production records belong
in a private project folder; example files are demonstrations, not your live project.

## Start a film

Tell the agent the intended viewer/result, source material, language, aspect ratio,
length, deadline and budget/tool limits. Unknown answers stay visible; ask only
questions that change the production choice. A usable request can be:

> Make a40-second English guide from my photos and footage. YouTube16:9 first,
> free tools on my Mac, no publication. Show the proposed source clips before assembly.

1. Review existing sources and permissions; distinguish find/adapt/create.
2. Agree a short concept and feasible production route with gaps, tradeoffs,
   observed or unknown costs/time, and a small pilot. A provider listing is not access.
3. Create the private project checkpoint, retain inputs and decisions, then execute
   the authorised stage. Review pilot before expanding production.

[Production guide and setup](production-guide.md) ·
[Unified proposal](../skills/video-production-router/references/producer-brief.md) ·
[Project journal](../skills/video-production-router/references/projects.md).

For a harmless local demonstration, from the repository root:

```sh
python3 skills/video-production-router/scripts/plan.py examples/briefs/mixed-promo.json --format markdown
```

This prints a proposal, not a film. Actual tools/dependencies and authority are
checked for the selected route; no global prerequisite installation is implied.

## Continue a project

Give the agent the existing private `project.json` path. Start with:

```sh
python3 skills/video-production-router/scripts/project.py brief /absolute/private/project.json --json
python3 skills/video-production-router/scripts/project.py blockers /absolute/private/project.json --json
```

Read the selected exact final, current-version reviews, explicit waits and latest
checkpoint. Distinguish historical preparation text from later accepted receipts.
Changed sources/checks require reconciliation, not blind retry. A ready-task
suggestion is not execution authority. Resume only the authorised stage; preserve
accepted bytes and owner choices, including “internal only” and no-publication.
If a real answer is missing, report that gap while continuing independent work.

[Recovery procedure](../skills/video-production-router/references/projects.md) ·
[Selected-final recovery evidence](experiments/selected-final-recovery.md) ·
[Current release assessment](rel-b-readiness-2026-11-01.md).

## Correct a fragment

Record four things: **interval, defect, desired change, what to preserve**. Example:

> At12–14s the caption covers the subject. Move it above the subject; preserve
> the voice, music, scene duration and all other shots.

Retain the original under its own ID, make the edit in the selected tool, and retain
the correction under another ID. Do not replace the accepted final before review.
Create a before/after comparison with neighbouring seconds; inspect the actual
encoded files and sound. Record technical, listening and creative results against
that exact revision, then explicitly select a final if accepted.

[Request and compare commands](../skills/video-production-router/references/revisions.md) ·
[External-editor return](../skills/video-production-router/references/otio-export.md#safe-return-from-an-external-editor).
Caption geometry and reading time are different checks; [timing preflight](../examples/production-reuse/README.md)
is an English heuristic, not an automatic retime or approval.

## Shared boundaries

No new paid call, upload or public publication follows from an example, old approval
or a “ready” status. Keep platform/model/media rights, technical QA and owner review
separate. Reuse the existing journal/executor; don't create another scheduler or
approval database. [Experiments and limitations](experiments.md) · [Checks](checking-policy.md).
