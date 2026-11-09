# Premation — native export sync test and two-format explainer

Closed9November2026. Both99.3s English films were owner-accepted with sound and
owner-reported published: [YouTube](https://youtu.be/PhwCWcEe0LE) and
[TikTok](https://vt.tiktok.com/ZSpDa9LYn/). Only YouTube was sent to Radar; apply,
duplicate handling and returned acknowledgements were checked. Visibility,
uploaded-file identity, audience results and monetisation are separate observations.

## Repeatable test

Question: does embedded source audio remain aligned with matching picture events
after a native variable-speed export? Pin the exact app/build and media first.
This trial used official Premation1.1.1 arm64, one original12s source with six white
flashes and six embedded clicks, a normal-speed control and a10.5s retimed export.
The speed profile includes0.5× and2× sections with transitions.

1. Verify the unmodified source's six shared anchors before evaluating an editor.
2. Save a complete `.motion` bundle, including asset registry and embedded media
   blob. The initial minimal project produced an export but did not provide the
   required audio anchors; its failed measurement remains evidence, not a pass.
3. Export control and candidate with the same native CLI/build/settings. Retain
   commands, exit states, files and hashes before measuring.
4. Decode the actual exported video and audio independently. Detect every flash
   onset and click onset, match events and report missing events as failures or
   explicitly unmeasurable. Predeclared window: one30fps output frame,33.3ms.
5. In the corrected bundled control and ramp exports, all six events in each file
   stayed inside that window. Small computed audio offsets do not establish
   sub-frame visual accuracy: the picture measurement is quantised to30fps.

Private source of truth: external `productions/premation-sync-test/trial/` keeps
the original fixture, both self-contained bundles, original failed control export,
selected native exports, detection code, run logs and measurement receipts.
No native generation or benchmark was rerun during closeout.

## Repeatable film recipe

Use the real trial as the centre of the explanation, with independently authored
opening/ending inserts: original Blender clapper, violet/coral/cream design,
large labels, clear source/control/ramp comparison and a concise limitation ending.
Measure English voice takes first; use one frame-based beat timeline for speech,
picture and source clicks. Keep a quiet original score under speech. The explanatory
mix is not the unaltered audio used for the native synchronization measurement.

`full/build-film-rendered-v1.py` is the exact used assembly source;
`full/build-film.py` adds source-pipe draining for later reuse. Preserve both,
the final mix, beat voice stems/manifests, timeline, actual trial clips, original
clapper clips/scenes and source-frame input. Do not rerun over accepted filenames;
prepare a new version/work copy for a later correction. No exact future encoded-byte
identity is promised across tool/runtime changes.

Separate1920×1080 and1080×1920 graphic compositions were delivered. The clapper
source is720p; the actual Premation inserts are640×360 and visibly enlarged.
Native1080p graphic layout does not create detail missing in those sources.
The cover was a separate local composition from a clapper frame in the film palette.
English SRT/VTT use approximate measured-take timing, not forced alignment.

## Limits and reuse boundaries

- One synthetic clip, six sparse transients per export, one pinned CLI build/route.
  No qualification of arbitrary codecs, long programmes, complex audio, lip-sync,
  pitch quality, realtime preview or the editor's graphical speed-ramp controls.
- Original local visuals/sound and offline Supertonic3M1 speech; retained speech
  licence is separate from Premation's upstream software terms. No copied upstream
  source/binary is redistributed through this case document.
- Full-film acceptance belongs to these outputs. The package's older `pending`
  notes describe its preparation time; current state is in `production-status.json`
  and the owner-publication receipt. A URL does not establish uploaded-byte identity.

## Dependency-aware sanitation

Removed47 superseded local files:24,016,965 logical bytes (about22.9MiB). The two
pilot MP4s, pilot-only mix/take, unnormalised mixes, individual review stills,
cover-source extractions and automatic Blender backup were retired. Their hashes
and historical pilot pins are preserved in the private availability record.

Retained52 critical selected inputs and all accepted-master hashes. Full/package
MP4 names are hardlinks to the same underlying files; they were kept and never
counted as duplicate allocated-space savings. Selected native test exports,
failed setup evidence, full mix/stems, scenes, receipts and publication kits remain.
Active review/package links and all remaining current artifact pins passed checks.
No cloud deletion, new generation, publication or release was performed.

See the [public evidence manifest](../public-evidence.json). This closeout adds the
already-executed native test to that index; it is not a newly conducted trial.

Generic checkpoint limitation: intentionally retired pilot pins cause two historical
technical observations to appear stale in `project.py brief`. This does not reopen
the accepted full films. The availability receipt and case status distinguish them;
a retirement-aware generic summary is queued, not implemented in this closeout.
