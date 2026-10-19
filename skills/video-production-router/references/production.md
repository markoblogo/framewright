# Scenes, reusable materials and local publication kits

This is a schema-2 project extension, not a renderer/editor or publishing API.
One saved project holds the original plan, tasks, decisions, material catalogue,
scene script, independent cuts and delivery mappings. No extra database or service.

## Start with a plan-only example

From the checkout, after explicitly creating the local directory:

```sh
mkdir -p local/review
python3 skills/video-production-router/scripts/project.py create local/review/project.json --goal 'Review with a main video and Short' --note 'Planning only'
python3 skills/video-production-router/scripts/project.py compose local/review/project.json examples/production/review-main-short.json
python3 skills/video-production-router/scripts/project.py board local/review/project.json
python3 skills/video-production-router/scripts/project.py board local/review/project.json --json
```

The example has no real sources, permissions, recordings or final files; it stays
incomplete. Schema-1 projects need the existing explicit backed-up migration first.
The same composition shape supports service reviews, game stories and book promos;
this does not qualify an untested engine or verify a service's claims.

## One composition, several independent cuts

A JSON specification contains `schema_version: 1` and these lists:

| List | Required fields / purpose |
| --- | --- |
| `materials` | `id`, `kind`, `subject`, `origin`, `rights`; optionally tags, declared duration, parent IDs, capture mode and disclosure |
| `scenes` | `id`, `tell`, `show`, material IDs, narration `{text, material}`, `missing`; optional claims `{text, material}` |
| `variants` | `id`, `kind`, canvas `{width,height,fps}`, ordered edits, music ID or null, related task IDs and five delivery slots |

A material kind is `video`, `audio`, `image`, `text` or `project`. `subject` is an
existing `input:ID` / `output:ID`, or null for a planned material. Declare/retain
actual files through the existing project CLI; composing never finds, copies or
produces source media. Pending subjects are not inferred from filenames.

Narration IDs must refer to audio; music is separate. Each scene states the script
point, visual demonstration, sources, intended speech and missing work. Claims
reference their demonstration/source material, or remain explicitly unresolved.
A reference is not a semantic fact-check or proof that the described action worked.

Each variant has kind `main`, `short` or `other`; set actual intended dimensions.
An edit names a scene and picture material (or null), positive duration and an
explicit framing instruction. Video source ranges use `source_in` / `source_out`;
both bounds and a declared material duration are needed for bounded planning.
Only normal-speed ranges are supported. Durations are declarations, not decoded
measurements. Optional per-edit narration gives the Short its own text/audio.

Cuts reuse catalogue IDs without duplicating footage. Their order, ranges, framing,
narration and final outputs remain separate. Portrait framing is a manual decision,
not automatic tracking or proof that all important action fits. Use explicit
`capture_mode` and disclosure for scripted gameplay; a generated performance or
terminal fixture must not be described as real gameplay.

`delivery` maps `video`, `thumbnail`, `subtitles`, `title`, `description` to material
IDs (or null while missing). Final materials also have origin/rights and declared
parents; their local files use their own pins. Fixed delivery kinds are video,
image, then three text materials. Final duration, when declared, must agree with
the cut within one intended frame. Final format still needs actual technical QA.

## Rights, lineage and revisions

`rights` contains status (`unknown`, `owner_authorized`, `licensed`, `restricted`),
a basis note, allowed uses (`main`, `short`, `other`, `cover`, `copy`), attribution
text and unresolved restrictions. These are scoped operator records, not licence
verification or publication authority. Cleared statuses require a basis.

`derived_from` lists parent material IDs. Parent rights and missing/changed files
propagate into every use; a licensed child cannot silently clear an unknown parent.
Cycles, unknown IDs, invalid ranges, nonfinite/bool durations and unsupported keys
are rejected before the project is written. This strictness covers this extension,
not the separately deferred general brief/resource-constraint contract.

The composition binds the current file revisions. Replacement bytes require
explicit retaining, then `compose PROJECT SPEC --replace` after reviewing the
catalogue, rights and cuts. The previous composition stays in history. Pending
sources/finals becoming available also require explicit rebinding. Repeating an
identical composition is a no-op; an unrelated unused catalogue addition does not
invalidate a cut's footprint.

Changing a cut/its material footprint reopens final-video technical conformance,
even if the encoded bytes are unchanged. The journal records an administrative
pending receipt, not a failed decode or a new QA result. Recheck the actual final
against the revised cut before recording a pass. Positive receipts never execute
work or complete tasks automatically. Rejections/pending/stale source checks also
remain blockers; source approval does not substitute for final-file checks.

## Collect a local kit

```sh
python3 skills/video-production-router/scripts/project.py bundle local/review/project.json short --output local/review/short-kit --draft
```

Without `--draft`, unresolved checks prevent export. A draft can collect available
unchanged finals with an incomplete report; it never manufactures missing files.
No raw/source media is copied merely because it is in the catalogue.

Required current manual checks on each final revision:

| Slot | Checks |
| --- | --- |
| video | technical pass, accepted listening (or intentional silence), creative acceptance |
| thumbnail | technical pass, creative acceptance |
| subtitles | technical pass |
| title / description | creative acceptance |

These are check categories, not automatic evaluation of every handoff criterion.
Use the [full QA contract](handoff.md) for actual decoding, timing, readability,
pronunciation, subtitle accuracy and source-claim review. A generic/scoped receipt
cannot legitimately stand for inspections its operator did not perform.

The kit contains only mapped final files, `manifest.json` with hashes/provenance
and `CHECKS.md` with missing materials, rights, checks, cuts and open project work.
Only tasks explicitly attached to the variant block its handoff; other remaining
project work is disclosed. All five slots are required in this increment.

Copies are hashed against retained bytes; text must be nonempty UTF-8. Extension
checks are structural, not codec/pixel/subtitle-syntax verification. The command
does not call a decoder, model, network service or uploader. A complete local
handoff means recorded scoped checks, never `publication_authorized`.

Choose a new destination; existing directories are never overwritten. Preparation
happens privately before exclusive destination creation. The manifest is moved
last as the completion marker; an interrupted final move may leave an incomplete
directory for inspection. Project bytes and task/observation history are unchanged
by board/bundle commands. Kits/reports contain private context and are local review
artifacts, not material automatically cleared for public sharing.

Before a local kit can be complete, title, description and subtitle files must
contain non-whitespace UTF-8 text. This checks text presence/encoding, not its
meaning or subtitle timing. Changing only external cover/copy/subtitle mappings
or attached task metadata does not reopen video conformance; actual cut, picture,
audio or final-video changes do. Other delivery checks still apply independently.
