# Editing from source recordings

SOURCE-01 now has a [bounded lexical retrieval pilot](../../../docs/experiments/source-first-playmcp.md)
over revision-bound supplied transcripts and visual observations. It does not
perform new ASR, semantic search or automated media understanding. StoryToolkitAI
runtime remains untested. Proposed edits still use this workflow's ordinary map.

The [MN7R ASR follow-up](../../../docs/experiments/source-asr-mn7r.md) separately
ran retained local mlx-whisper weights and imported the raw result. The indexer
itself still makes no model calls.

```sh
python3 skills/video-production-router/scripts/source_search.py index local/source-plan.json --output local/source-index.json
python3 skills/video-production-router/scripts/source_search.py search local/source-index.json --kind transcript --query 'connect agent' --output local/speech-hits.json
```

Each source requires `annotation_provenance` with nonempty `method` and `scope`.
Timed media reuse the source schema below. Explicit `kind: image` accepts observations
with unique `id` and `text` only; no invented time or speech. Optional `evidence_files`
records sidecar path/hash pairs. The index pins the specification and all supplied
source/sidecar bytes. Search refuses changed inputs or index contents; rebuild and
review selections explicitly. Outputs are new files, never overwritten.

All query tokens must occur in one annotation. Matches retain their evidence channel,
range/still ID and provenance; they are candidates, not verified actions or facts.
No negation, synonym or semantic interpretation is performed. A miss means only
`not_found_in_index`. Human viewing/listening and selection remain separate.

For several sources, follow the [MN7R proposal-stage trial](../../../docs/experiments/source-multicut-mn7r.md):
use one coherent goal, keep source ID plus cue ID/hash on every selection, retain
context handles and validate the ordinary cut map. Record existing reusable media,
required adaptations and conditional new-material gaps separately. A still-card
hold or future adaptation is not part of the cut-only video's measured duration.
Search other retained sources before commissioning a missing shot. An annotation
miss alone does not justify generation. Proposed structure is agent-authored;
source identity/ranges are mechanically checked, not semantic understanding.

Use for owner recordings, multiple takes, screencasts and source-based recuts. This
optional module extends the existing [studio workflow](studio-workflows.md) and
[production checkpoint](projects.md); it is not another project ledger or renderer.
The helper needs Python 3 and existing FFmpeg/ffprobe on PATH. It installs nothing,
calls no model/ASR/service and accepts explicit local files only.

## 1. Inspect before choosing

Start with the authorised files, message, audience, language, target length and
must-preserve statements. Copy the [plan example](../../../examples/editing/source-plan.json)
into the private production folder. Paths resolve relative to the specification,
not the shell's working directory. `sources` needs unique `id` and local `path`.
The same source/edit IDs and `in_seconds`, `out_seconds`, `reason` fields can be
used alongside `workflow.py`'s source/rights intake. This helper does not grant rights.

```sh
python3 skills/video-production-router/scripts/editing.py inspect local/source-plan.json --output local/inventory-v1.json
```

Inventory records SHA-256, duration, streams (including fps, size, rotation tags,
start times and audio layout when available). Container duration is not a full
decode or proof that every stream covers every second. Review VFR, delayed audio,
rotation and absent streams before choosing a working format. Originals stay intact.

Use authorised ASR separately if needed; retain its provider/model and original
output. Supply corrected or uncorrected transcript explicitly in the source entry:

For a complete original-source local Whisper run, `import-whisper` converts raw
segments without correcting words or altering/clamping times:

```sh
python3 skills/video-production-router/scripts/source_search.py import-whisper local/original.mp4 --transcript local/asr-raw.json --receipt local/asr-receipt.json --source-id original --output local/source-plan.json
```

The receipt requires `schema: framewright-local-whisper-receipt-v1`, matching
`source_sha256` and `transcript_sha256`, `timing_origin: source_playback_zero`, and
`model` with `package`, `version`, and nonempty `weights` identities. Keep the run's
parameters/resource observations in that same receipt. It is an operator-supplied
attestation, not independent proof of model execution or authenticity. Imports pin
raw output and receipt as sidecars and reject missing/invalid/empty/out-of-source
segments. An excerpt or offset stream needs explicit timing mapping first.
ASR segments give candidate ranges, not verified word-accurate cut boundaries.
Recognition errors can cause false misses; review a broader query and source audio
before declaring material absent. Corrected transcripts must be separately versioned.

```json
{
  "id": "take-1", "path": "originals/take-1.mp4",
  "evidence_sha256": "<actual SHA-256 from the inventory>",
  "transcript": [{"id": "line-1", "start": 1.2, "end": 3.4, "text": "Actual spoken words."}],
  "observations": [{"id": "view-1", "start": 1.2, "end": 3.4, "text": "Operator reports: launcher is visible; suitable opening."}]
}
```

Times are seconds from source playback zero. Transcript/observations must name the
matching file hash and lie within its duration. They are supplied evidence, not
verified content or tool-generated perception. Missing transcript, visual review,
listening and motion review remain unperformed. Preserve uncertain words and names.

Agent output: a concise take table with file/range, actual phrase, visible action,
observed sound/picture problems and proposed story role. Cite the observation or
inspected excerpt supporting each judgement. Suggest up to three openings from
available, source-backed intervals; if none is supported, ask for the missing shot.
Do not invent scene descriptions from metadata or extract meaning from loudness.

## 2. Map the chosen cuts and retime cues

Write `edits` in final playback order. Each entry needs a known source, nonnegative
`in_seconds`, greater `out_seconds` within the measured duration and a nonempty
selection `reason`. The current implementation supports cuts at normal speed only.
Speed changes, transitions, overlaps and extra edit fields are rejected. Use the
selected renderer for those features and a new explicit time mapping.

```sh
python3 skills/video-production-router/scripts/editing.py map local/source-plan.json --output local/edit-map-v1.json
python3 skills/video-production-router/scripts/editing.py retime local/edit-map-v1.json --output local/retimed-v1.json --srt local/captions-v1.srt
```

The map retains source and output ranges, selection reasons, unused source ranges,
file hashes and its own digest. Intervals are half-open. Reordering/repeated source
passages create separate output occurrences. Subsequent commands reject changed
source bytes or an edited map; revise the source plan and regenerate sidecars.
These hashes detect drift, not reviewer approval or authenticity of statements.

`retime` maps supplied transcripts, plus optional `--cues local/overlays.json`:

```json
[{"id":"label-1","source":"take-1","source_sha256":"<actual source hash>",
  "kind":"overlay","start":1.4,"end":2.4,"text":"An explanatory label"}]
```

Cue kinds are `subtitle` or `overlay`. Removed cues are listed; crossing cues are
split/clipped by retained occurrences and marked `needs_review`. Text is not
rewritten. A clipped caption can contain words no longer audible: fix its source
text/timing before exporting SRT. SRT export rejects clipped/overlapping subtitle
cues, invalid delimiters and spans that collapse at millisecond precision. Generate
JSON alone to inspect unresolved cases. Whole removed cues still require a meaning
check; no automatic system can approve the omission solely from this time map.

Review preserved negation, numbers, conditions, natural breath and the relationship
between action and consequence. Keep required qualifications. Map overlays to the
new timeline; in the chosen renderer review face/interface overlap and readability.
This command prepares cues, not graphics layout, forced alignment or a final film.

## 3. Inspect each join in context

```sh
python3 skills/video-production-router/scripts/editing.py joins local/edit-map-v1.json --output local/joins-v1 --context 1
```

By default prepares all boundaries (maximum 20 in one call). Select one with
`--join 2`. Context is 0.1–5 seconds on each side, clipped to selected intervals.
Open `review.md` and play the linked preview. Each join includes:

- `preview.mp4` (or `preview.wav` for two audio-only passages), with original sound;
- `frames.png`: first, immediately before, immediately after and last sampled frame;
- `waveform.png`, and `words.json` with source/output/preview times;
- `report.json` at pack root with source handles, preview hash, actual duration,
  boundary position, normalization, inserted silence/background and pending reviews.

Video review proxies use 640×360, 24fps, stereo 48kHz, preserving aspect ratio with
padding; audio-only proxies are PCM stereo 48kHz. Video handle lengths round up to
frames; source audio is trimmed before padding. `proxy_padding_seconds` records up
to one frame of inserted silence/held picture per side. This can affect perceived
pause length, so compare a questionable word edge to the source excerpt. Thus the recorded preview cut time can differ slightly from requested context.
Missing audio is explicitly represented by silence; an audio-only side of a mixed
join uses a plain background. These are review aids, not source restoration, color
masters or synchronization repair. Only the first eligible video and first audio
stream are selected. Multiple tracks/cameras need a separate deliberate decision.

Encoded previews receive a full decode check. Listening, visual and semantic
reviews remain pending. Check complete words, breath, audio clicks, abrupt pose or
exposure changes, and whether the selected sentence still means what it meant.
Use the original excerpts for context outside the retained handles. A contact sheet
cannot establish motion or listening quality. Review the whole assembled film too.

The pack stages into a temporary sibling directory and appears only after completion.
All outputs require new names; no source or previous review is overwritten. Processes
have a 120-second per-command timeout. FFmpeg filters/encoders use bounded threading
for these small proxies; this avoids a locally reproduced scheduling hang. Failure
is not a negative creative verdict, and no automatic retry/installation occurs.

## Existing project integration and limits

Retain the plan/map/cue report and review-pack manifest as inputs/outputs of the
existing project using `project.py retain`. Record actual owner/editor decisions
through its existing tasks/journal; do not hand-edit the journal or mark a task
complete because a preview exists. These sidecars are not `media_review.py` reports
and must not be imported as perceptual approval. Changing cuts requires rebuilding
cues, affected joins and dependent renderer checks.

The selected renderer still assembles the final film. Publication rights, authority,
source-content review and owner preference are separate. No cloud transfer, paid
call, automatic publication, final-film qualification or audience claim is implied.

## Origin and qualification

Original Framewright implementation informed by the owner-supplied Russian guide
*Вайб-монтаж с AI-агентами*, Точки над ИИ / AI Camp, dated 15 October 2026:
source inspection and EDL pp.21–26; joint picture/word/audio review pp.12–13;
sound and revision checks pp.28–33. PDF and its prompts are not redistributed.
See [research and scoped checks](../../../docs/research/ai-editing-guide.md).
This is deterministic helper coverage and a synthetic local smoke, not a real
editorial production trial or a new qualification of model-based perception.

## Continue with revisions and series

Use [precise revisions](revisions.md) for a source-pinned defect/change/preservation request, playable before/after context and a checked journal decision. Use [accepted-film templates](templates.md) to freeze explicit design separately from typed content and prepare three boundary-case packets. Data validation is not visual review or final-film approval.

## External editorial handoff

For an authorised retained cut, use the optional [OTIO exporter](otio-export.md).
It requires explicit frame ranges and packaged pinned media; unsupported effects
stay explicitly baked. Native readback and consumer checks remain separate.
