# Optional OTIO editorial handoff

Use for an explicitly authorised external-reference cut export. The accepted film,
creative scene intent and approvals remain in the existing project. OTIO describes
an edit; it is not a renderer or a media-embedded final movie. No automatic install,
cloud call, spending or publication. [Actual bounded trial](../../../docs/experiments/otio-mn7r-handoff.md).

## Requirements and command

Official `opentimelineio` is optional; tested0.18.1/Python3.12/macOS arm64 in a
separate environment. Check installed version and actual target-editor support.
Use the chosen environment's Python, with existing FFprobe available:

```sh
python skills/video-production-router/scripts/otio_export.py package/export-spec.json \
  --output package/Monitor.otio --receipt package/export-receipt.json
```

Both outputs must be new files; the `.otio` stays beside the spec/media package.
There is no automatic conversion from `project.py` or the seconds-based cut map.
Prepare exact frame ranges from the actual retained assembly, including later fixes.

```json
{
  "schema": "framewright-otio-export-v1",
  "name": "Approved cut",
  "project_id": "project-id",
  "variant_id": "main",
  "rate": 30,
  "duration_frames": 90,
  "declared_baked_features": ["Typography and reframing baked into picture"],
  "media": [{"id": "shot", "path": "media/shot.mp4", "sha256": "REPLACE_WITH_ACTUAL_SHA256"}],
  "tracks": [{"id": "Picture", "kind": "video", "items": [
    {"id": "shot-1", "type": "clip", "media": "shot", "in_frames": 0, "duration_frames": 90}
  ]}]
}
```

Audio uses `kind: audio`; a gap has `id`, `type: gap`, `duration_frames` only.
Every track must cover the declared duration, using explicit leading/trailing gaps.
A clip needs an existing requested stream and explicit zero-based source range.

## Bounded profile and checks

First profile: common integer CFR1–120, frame-valued in/duration, straight cuts,
multiple audio/video tracks and explicit gaps. Source video must match the timeline
rate and start at zero; bake VFR/mismatched rates first. Exact frame/sample clock
bounds are required; rounded container duration is insufficient. Media must resolve
inside the package, match retained hashes, and use relative references; remote,
absolute, traversal and escaping symlink paths are rejected. Unknown fields/effects
are rejected. Unsupported titles, retiming, automation and transitions must be
explicitly declared as baked media, never silently dropped.

Native library readback checks structure, clip IDs/order, positions/ranges, gaps,
URLs and revision metadata. Receipt pins the spec, output and media. It does not
claim editor import, render parity, listening or publication. Retain spec, OTIO,
receipt, media manifest and actual consumer checks with the existing project CLI;
do not copy private media/logs into Git or approve by file existence.

Keep the whole package together when moving it. Manually inspect target-editor
relinking, first/middle/last pictures, joins, sound, timing and any render. A player
opening three frames is narrower evidence than full editing-application support.
No external editor changes overwrite the journal automatically.

## Tested full-editor consumer: Kdenlive26.08.2

[Actual MN7R trial](../../../docs/experiments/otio-mn7r-handoff.md#same-day-follow-up-actual-kdenlive-import-edit-and-render)
opened the native timeline, saved a project, extracted15frames on all unlocked
tracks, re-exported OTIO and rendered a full MP4 with two encoder threads.
Source/changed cut timing and numeric encoded picture/audio checks passed.

Preserve raw native exports separately. This editor drops Framewright metadata/IDs,
converts URLs to absolute paths and omits trailing voice silence as an explicit gap.
A portable derivative may change only verified media URLs and retain its own receipt;
revalidate media hashes/ranges before mapping it to the existing journal. Do not
inherit approval or overwrite the journal from exported metadata. Baked effects
remain baked. Kdenlive support is scoped to the tested straight-cut profile.

Prefer one heavy job at a time. `--setup-report` is a diagnostic that exits normally;
it does not leave the GUI open. UI control needed an explicitly authorised AppleScript
fallback and one owner-assisted save; unattended execution is unqualified. Focused
listening and other editor interoperability require their own checks. The
[MN7R review follow-up](../../../docs/experiments/otio-mn7r-handoff.md#review-and-explicit-final-choice)
records explicit owner listening/creative acceptance and final selection for B;
that acceptance is not inherited by another edit.

## Safe return from an external editor

`otio_return.py` uses the same optional native library and existing project journal.
**Inspect is read-only; stage is a separate explicit action.** No editor, render,
model, installation, network call or publication runs. [Actual return trial](../../../docs/experiments/otio-mn7r-handoff.md#safe-return-follow-up-otio-02).

```sh
python skills/video-production-router/scripts/otio_return.py inspect local/export/export-spec.json \
  --baseline local/export/film.otio --after local/editor/film.otio \
  --output local/return-report.json

python skills/video-production-router/scripts/otio_return.py stage local/project.json local/return-report.json \
  --id editor-v1 --spec-subject output:otio-spec --baseline-subject output:otio \
  --after-subject output:editor-otio --render-subject output:editor-film \
  --output local/return-packet.json
```

Before staging, explicitly declare/retain the spec, baseline, returned OTIO and
rendered candidate through `project.py`. All four must match the report/current
pins; the render subject is mandatory. Stage redoes the inspection, checks render
format/extent and retains new aliases, all actual referenced media and a packet.
It adds three pending review tasks in the existing journal, bound to the new
candidate and its dependencies. Original outputs, observations, waits and accepted
work are preserved. Retaining a new candidate never selects it as the final film.
Normal `project.py observe`/`mark` records subsequent actual reviews. Dependency
replacement makes those receipts stale; nothing copies technical/creative,
listening, rights or publication approval from a previous artifact.

The report compares exact piecewise source-to-timeline mappings by verified media
hash, frame position and source range. Editor clip IDs and approval-looking metadata
are not trusted. Missing trailing audio gaps count as implicit silence. Reports
include the duration delta and affected absolute timeline intervals per track;
an intro cut can shift subsequent mappings across the whole remaining timeline.
Changed source content is distinct from changed timeline positioning. An unchanged
OTIO cut is not proof that an associated rendered file looks/sounds unchanged.

First profile: common integer CFR1–120,flat clips/gaps,at most one picture track,
unchanged unique track-name/kind mapping. Source ranges must be explicit integral
frames inside actual retained media. The baseline must match its export spec.
Known media can be rearranged or replaced by another known hash; new/changed hashes
need separate curation. Reject effects/retiming,nested cuts/transitions,remote refs,
escaping symlinks,ambiguous hashes,nonzero timecode and unmapped tracks. Local paths
must resolve inside the explicit export/return folders. Opaque metadata is digested,
not interpreted as conformance evidence. Review the rendered result separately.

Reports and packet IDs require new names. Staging uses the project lock and one
journal save; validation failures are tested not to mutate the project. A filesystem
failure after packet writing can leave an unregistered packet; that file is not a
completed intake/approval, and a retry needs a fresh path. No automatic overwrite,
composition rewrite, final-version switch or bidirectional approval synchronization.

Returned Track/Stack composition source ranges are rejected in this bounded profile;
flatten them into explicit child-clip ranges before comparison. They are not ignored.
