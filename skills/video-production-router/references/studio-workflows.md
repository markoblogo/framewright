# Shared experimental studio workflows

For repackaging an existing film, sourced insight stories and hybrid production.
These helpers extend the existing router/checkpoint, not a new editor. Current
qualification is **experimental planning only**; no A/B/C film has been produced.

## Conditional intake → existing production checkpoint

In a checkout, inspect `examples/workflows/repackaging.json`, `insight.json` or
`hybrid.json`. They use placeholders. Copy one into an ignored `local/` folder
when real sources are chosen. No folder/assets are needed to inspect the example:

```sh
python3 skills/video-production-router/scripts/workflow.py examples/workflows/hybrid.json
```

For a later selected brief, after creating a private project directory explicitly:

```sh
python3 skills/video-production-router/scripts/workflow.py local/story.json --format brief > local/story-brief.json
python3 skills/video-production-router/scripts/project.py init local/story-brief.json local/story-project.json
python3 skills/video-production-router/scripts/project.py resume local/story-project.json
```

Standalone installs contain the helpers and schemas but not repository examples;
use the schema to author the same spec. `--format brief` embeds its shared intake
under `production` and enforces `minimum_evidence: tested`. No sources are fetched.
The original `plan.py` supports this optional field directly; legacy briefs keep
their existing behavior. Styles/preferences do not upgrade evidence or prove seams.

Contract: [workflow schema](production-workflow.schema.json). `workflow.py` applies
explicit semantic checks; this is not a generic JSON Schema validator. Source IDs
must be unique, claims reference a declared source plus locator/review, and edits
are ordered source-time intervals with a selection reason. A declared duration is
not probed media. EDL order permits reordering; cuts must not distort original meaning.

Video `origin` describes where it came from. `video_rights` and `audio_rights`
remain independent. Explicit `audio_policy: remove|replace|keep` is required.
Unknown retained rights block publication; denied retained media also blocks
production. Removed audio is excluded from rights reuse, not magically licensed.
`granted`/`noncommercial_only` require an evidence reference covering the intended
use (including composition, recording and synchronization for music). An operator
claim is not independent legal clearance. Telegram/X/public availability grants nothing.

Owner reviews concept, source context, claim table, EDL, music choice and limits
before executing a bounded trial. `production-review` must precede every scene.
Missing facts/limits remain frozen unmet checks: revise the spec and create a new
checkpoint rather than force an old approval. Core private trials can be planned
while public rights remain unresolved; `publication` cannot be manually marked
done with those unresolved blockers. This CLI never uploads even when all pass.

Extra retained output IDs are `production:audio-stems`, `production:subtitles`,
`production:first-screen`, `production:thumbnail`, `production:youtube-copy`,
`production:provenance`, `production:technical-qa`, `production:time-resource-log`.
Use the existing `final-video` for MP4. Multiple stems can be a manifest of separately
pinned files; pin each actual input/output before declaring delivery. File pins
verify identity, not audio quality. `delivery-materials` and `qa:delivery-materials`
require these files; manual QA evidence must address every output independently.
Do not mark a delivery bundle verified merely because a list of filenames exists.

## Private music/sound library

No archive is scanned automatically. Later, choose an explicit local folder and
put the catalogue outside Git, or under ignored `local/` / `.framewright/`:

```sh
python3 skills/video-production-router/scripts/library.py scan /absolute/path/to/music local/music-index.json
python3 skills/video-production-router/scripts/library.py annotate local/music-index.json TRACK_SHA256 --mood calm --genre ambient --bpm 90
python3 skills/video-production-router/scripts/library.py annotate local/music-index.json TRACK_SHA256 --rights granted --evidence 'Reviewed owner provenance for composition, recording and synchronization'
python3 skills/video-production-router/scripts/library.py find local/music-index.json --use commercial --mood calm --duration 15
```

Requires an already installed `ffprobe`; no implicit install. `scan` recursively
indexes regular supported audio files without following symlinks. Metadata includes
duration,container,codec/sample-rate/channels,relative path,bytes and content hash.
`mood`, `genre`, `bpm`, `origin` and rights are **operator annotations**; unknowns
stay null/unknown. Embedded genre tags are only hints. No emotional/genre/beat
classifier has been evaluated; existing librosa evidence is authored accents only.
Catalogue filenames/paths and notes are private even when the audio is original.

Optional `scan --analyze-seconds 15` uses already installed FFmpeg volumedetect on
the first window. Mean/sample-peak dBFS is not integrated LUFS or true peak, and
cannot replace full-song/final-mix QA. Default scan limits:100 files,200MiB/file,
120s wall; subprocesses time out. Explicit flags can narrow/raise these limits.
Hashing and directory traversal have no process supervisor; wall time is checked
between operations. Unreadable/invalid media is recorded as an error. A budget stop
preserves the old index; successful rescans retain annotations only for identical
content and archive unavailable previous rows. Writes are atomic and exclusively
locked on macOS/Linux; final catalogue permissions are0600. No portability claim.

`find` rechecks hashes and excludes changed/missing sources. Commercial search
requires an evidence-bearing granted record; noncommercial also accepts recorded
noncommercial-only permission; private-test can show unknowns for review. Denied
tracks are never returned. These are operator records, not publication grants.
An unannotated BPM/mood does not match a filter. Longer tracks get a trim hint;
shorter ones get a loop/seam-review hint, never a loop-quality claim.

Select the actual track only after listening. Retain its hash/path via `project.py
retain ... --input`, add its origin/rights to the workflow's audio source, and use
the existing `music` object (`mode: existing`, `audio_source`) for the locked audio
handoff. Music selection/trim/loop/ducking is currently agent-directed through the
existing FFmpeg/MoviePy recipes, not executed by this catalogue. Preserve separate
voice/music stems, cut/loop points and gain/ducking decisions, then inspect the final
encoded mix. No private audio/catalogue/paths are uploaded to GitHub or cloud tools.

Catalogue contract: [audio-library schema](audio-library.schema.json). The catalogue
is a local index, not a portable licensed media collection or a backup of the audio.
