# OTIO-01: accepted source-first draft → portable editorial handoff

28 October 2026. Owner authorised export of the existing accepted MN7R draft.
**Scoped export passed. The same-day Kdenlive follow-up below also passes native
import/edit/re-export/render; broader editor interoperability remains untested.**
[Sanitized receipt](../../experiments/2026-10-28/evidence/otio-mn7r.json).
No new film, inference, cloud media transfer, paid call or public upload.

## Actual handoff

Official OpenTimelineIO **0.18.1**, Python3.12, isolated macOS arm64 environment.
The1.2MB official wheel was checked against PyPI SHA-256 before local installation;
OTIO is optional, not a default project dependency. The new `otio_export.py` helper
consumes an explicit pinned edit specification. It does not infer edits from chat,
render a film, install packages or export every production composition automatically.

The accepted42.633333s draft becomes1279frames at30fps: seven video clips, five
voice clips with two explicit boundary gaps, and one music clip. Nine retained
media files travel beside `Monitor.otio` using relative URL-escaped references.
A file manifest and Russian instructions accompany the private unarchived folder.
No credentials, absolute workstation paths or incidental journal notes enter OTIO.

Existing picture intermediates preserve the accepted portrait adaptation, typography,
source-boundary holds and fades. Existing normalization/ducking/fades are baked into
audio. These features are explicitly declared, not represented as editable OTIO FX.
Voice and music remain separate tracks. The bed is the accepted PCM mix minus its
existing clean voice, not model-based separation; sample-for-sample recombination
matches the accepted mix. This is specific to the retained audio, not a general
source-separation method or a guarantee of every editor's gain/pan behaviour.

## Verification and failures

- Official-library string/file round trips preserve IDs, order, source ranges,
  timeline positions, gaps, duration, relative URLs and material hashes.
- All1279 decoded picture frame hashes from the order read from actual OTIO match
  the accepted draft. This is baked-media sequence parity, not an external editor
  render or calibrated-colour test.
- DJV3.7.5 natively opened the OTIO. Actual inspected captures at frames330,990,1240
  show the offers table, adapted portrait insert and closing card. Relative media
  resolve correctly. Initial command capture was black with a null `View/Frame`
  error; a fixed-zoom/centre capture manifest succeeded. Both attempts are retained.
- Deliberately missing and replaced media are rejected without an output timeline.
  Nine focused software tests pass with OTIO; without it, seven pass and two native
  integration cases skip. These are software checks, separate from pixel inspection.
- An initial boundary failure came from rounded format duration:42.633333×30 is
  below1279. Exact sample/frame clocks now determine bounds; a regression retains
  the2046400/48000sample-clock case. No timing threshold was relaxed.

At the initial exporter-only checkpoint, complete native playback, listening,
perceptual sync and full-editor re-edit/render were **not tested**. The same-day
Kdenlive follow-up below closes the first editor gate; Resolve/Premiere remain
untested. DJV is a review player.
The exporter receipt keeps generic `editor_import` and `render_parity` untested;
this trial's picture and stem checks are separate scoped evidence. No new creative
approval of a re-edited version or permission to publish is inferred.

## Reusable procedure / next gate

Retain the accepted edit → explicitly bake unsupported features → copy permitted
media into one folder → record exact cuts/gaps and hashes → native export/readback
→ reject changed/missing files → inspect actual consumer pixels and sound → retain
results in the same journal. [Helper contract](../../skills/video-production-router/references/otio-export.md).
The initial next gate was a full-editor re-edit/render with audio/relink checks.
The owner separately authorised that follow-up, documented below; the original
export request alone did not require a large editor installation. Broader rates, transitions, native title effects,
external edit re-import and bidirectional journal synchronization remain out of scope.

[Source-first draft](source-multicut-mn7r.md) · [Official OTIO format guidance](https://opentimelineio.readthedocs.io/en/latest/tutorials/otio-file-format-specification.html).

## Same-day follow-up: actual Kdenlive import, edit and render

**The first full-editor handoff now passed in this bounded scope.**
[Native editor receipt](../../experiments/2026-10-28/evidence/otio-kdenlive.json).
Kdenlive26.08.2/rev.d4e87e4 arm64, MLT7.43.0, official download checksum verified;
application copied to external storage. No paid service or media upload. OTIO0.18.1
inspected exports; the editor's bundled OTIO version was not measured.

Native File → OpenTimelineIO Import resolved all nine media files and selected
1080p30 from the footage. Saved native-before.kdenlive and native-before.otio.
Their13 picture/audio clip references, order, source ranges and positions match
our original timeline exactly; overall duration remains1279frames. The editor
omits the trailing empty voice gap: semantic silence remains, but identical gap
objects/metadata are not claimed.

In the native Project Monitor, set the zone0–14 inclusive and extracted it on all
unlocked tracks. Saved native-after.kdenlive and native-after.otio. Result1264frames:
first picture in15/duration60; music starts at source15; later picture/speech clips
move earlier15frames together. Every resulting clip range/position matches the
explicit expected edit. The accepted original film and all handoff file hashes
remain unchanged. This is a technical test copy, not a new approved production.

Native Render to File produced H264/AAC,1920×1080/30fps,42.133333s,48kHz stereo,
with two encoder threads and parallel processing disabled. Full decoded comparison
covers1264frames: mean SSIM0.997979, minimum0.989947 versus the accepted film with
its first15frames removed. Lossy re-encoding means pixel identity is not expected.
Numeric8kHz mono audio screening gives best lag0ms within±10ms, correlation0.999931,
RMS ratio0.998961. Native timeline screenshot and six encoded samples were actually
inspected, including both sides of the first join. This is not focused full listening,
perceptual AV-sync approval or calibrated-colour qualification.

### Interchange and operating limits learned

- Kdenlive exports absolute media URLs and drops Framewright's custom metadata/clip
  IDs. Raw native exports are retained. A separate path-only repack copies verified
  media into a portable folder and changes only ExternalReference URLs; its receipt
  binds native/portable revisions. Journal identities and approvals remain external
  and authoritative. Never silently transfer acceptance through an editor re-export.
- CUA returned `Invalid app` even after the owner saw the window. Owner explicitly
  authorised AppleScript/macOS UI control for Kdenlive only. Native AXRaise/focus was
  needed before keyboard confirmation. Owner reported saving during one OTIO dialog;
  this does not qualify unattended GUI operation.
- `--setup-report` normally writes component JSON then exits. That diagnostic mode
  does not prove interactive startup failure. Official command options were inspected.
- Early SSIM runs had78/45 partial rows and nonmonotonic comparator clocks. Explicit
  ordinal frame clocks and disabled input filter reinitialisation yielded all1264
  rows without DTS warnings. Failed harness logs remain private; do not interpret
  partial statistics as a native-render defect or use this setting for arbitrary
  changing-resolution sources.

The first full-editor gate is satisfied for these straight cuts/baked intermediates.
Other editors, arbitrary rates/effects, native editable typography, full listening,
custom-ID preservation and bidirectional journal editing remain separate trials.
The original exporter remains optional. No new public video, release or export-registry
row is created. [Native editor documentation](https://docs.kdenlive.org/en/user_interface/menu/file_menu.html).

## Safe return follow-up: OTIO-02

Same-day bounded software implementation and real-source test.
[Sanitized receipt](../../experiments/2026-10-28/evidence/otio-return.json).
The new optional `otio_return.py` compares a supplied baseline export/spec against
an actual returned OTIO, then explicitly stages a separate candidate in the same
journal. It does not replace scene intent, the original film or its approvals.

Native-before.otio correctly reports no timeline change despite dropped metadata
and implicit trailing voice silence. The separately packaged native-after cut
reports1279→1264frames at30fps,−15frames. Nine returned media files match retained
source hashes. Picture/music absolute mappings change across0–1279; voice mapping
changes across60–1219. These are absolute before/after coordinates: deleting the
intro shifts later clips, rather than recreating their media. Opaque metadata
is different and remains untrusted as approval or rendered-effect evidence.

The existing native-after MP4 is supplied explicitly. Its format/extent matches
1264frames,1080p30; that association alone is not proof of picture/audio conformance.
The actual project receives new candidate aliases, pinned source dependencies,
a packet and three pending checks: technical, listening and creative. All prior
journal entries, every old step and artifact pin remained identical. The old
accepted film is still accepted under its old identity. The returned candidate
has no inherited acceptance or publication permission. Existing actual Kdenlive
QA remains separate evidence; it was not automatically converted into approval
of this newly staged branch.

Fourteen new tests cover the common-rate comparison, identity/gap handling,
source/range/effect/URL guards, report drift/forgery, duplicate IDs, preserved waits
and candidate-check reopening after a source receipt is repinned. Together with
nine exporter cases,23 native-environment tests pass. Without optional OTIO,
two interval-algebra cases pass and12 native cases skip explicitly. Software
checks are not a model, visual or listening benchmark. Tests were developed from
an initial failing inspect case and then a failing stage case before implementation.

No new render, paid/model call, upload, release or production publication. Remaining
scope: deliberate mapping for renamed/additional tracks/new material, richer
editor effects and rates, rendered-content review, explicit final selection and
any later composition adaptation. Do not claim automatic full project synchronization.

## Review and explicit final choice

28 October 2026. [Sanitized final-review receipt](../../experiments/2026-10-28/evidence/otio-final-review.json).
The owner requested the returned version's checks and explicit final choice.
A local comparison page presented accepted A (1279frames/42.633333s) and returned
B (1264frames/42.133333s), with start, narration and ending controls. Only the
first15frames are removed; picture, voice and music move together. No new render,
cloud transfer, paid/model call or publication was needed.

The current B hash was verified against its retained revision and the actual
native-render receipt. Exact editor ranges/order, full1264-frame picture/audio
decode evidence, numeric picture/audio conformance and six encoded samples were
reviewed. A fresh full-file loudness measurement reports input−17.25LUFS,
true peak−3.45dBTP, LRA5.80LU. The measurement writes to a null output and does not
normalise/change B. Numerical mono timing correlation is not perceptual sync
judgment; samples are not continuous viewing or calibrated-colour qualification.

The owner was explicitly asked to watch B in full with sound and answered:
“B —42.13s; image and sound accepted” (translated from Russian). Separate
version-bound listening and creative receipts record that owner report, rather
than converting prior A acceptance or numeric QA into listening. All three
candidate review tasks are done; the checkpoint reports no file drift, pending
review gates or recorded blockers. That is not an independent audience result.

A separate retained final-selection receipt and `final-cut` journal decision
select the exact B revision. All prior artifact pins, A and its old acceptance
remain intact. This completes the internal source-first/OTIO film trial; it does
not replace the already published MN7R overview, publish a new film, import a
new scene composition or implement a generic editor/journal synchronization layer.

Reusable closeout: inspect returned mappings → stage a new candidate → verify
current rendered bytes/content and sound → obtain its own owner review → record
the selected exact revision and keep the prior version. Replacing a dependency
requires a fresh review through the existing journal dependency checks.
