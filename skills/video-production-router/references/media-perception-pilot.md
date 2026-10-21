# Video-perception control pilot

A local kit for evaluating a proposed video reviewer against known **authored**
controls. It generates synthetic clips, freezes reviewer/operator packets, validates
supplied responses, reports detection errors and exports observations into the
[unified media report](media-review-reports.md). No model/API call, installation,
voice upload, account connection, spending or publication is performed.

The kit is prepared infrastructure. Generation, technical inspection and successful
scorer tests do **not** qualify Gemini, Qwen3-Omni, Claude Video or another reviewer.
A [free Gemini UI batch](../../../docs/experiments/gemini-media-review.md) was attempted,
but its response failed source-ID/evidence validation and left audio unknown.
A changed-protocol single-video follow-up matched one freeze and returned no
findings on one clean control; the separate audio-only smoke failed. Five other
authored events remain unassessed. No provider is qualified; independent per-label
human confirmation remains pending.

## Eight controls, six authored defect events

Each clip is 10s, 640×360, 12fps, with original block graphics and synthetic tones.
There are no voices, external fonts, third-party footage or copyrighted music.
The neutral task specifies the same desired sequence for every clip: heading,
light/beep cues, opening/closing door and a card moving between 3s and 6s.

| Operator control | Authored expectation |
| --- | --- |
| Continuous reference | No injected defect |
| Interrupted movement | Whole-frame hold at 4–5.25s |
| Black interval | Missing picture at 5–6s |
| Missing action | Door remains shut throughout the commanded-open interval, 2–8s |
| Cue mismatch | Beeps lag flashes by 0.65s; two events around 2–3s and 8–9s |
| Weak heading | Main heading is 7px high at low contrast; normal-size readability requires human confirmation |
| Allowed cut | One intentional hard cut at 5s; no injected defect |
| Allowed ending hold | Intentional static final state from 8.5s; no injected defect |

These are targeted controls, not natural footage, lip-sync, language/pronunciation,
colour grading or general creative judgement qualification. The block graphics
avoid confusing an actor's expression with an authored technical fault. Future
natural-footage controls need a separate labelled set and intended-use criteria.

## Build once into a new private directory

Requires existing FFmpeg with the libx264 encoder, ffprobe and Python standard library only.
Clips use H.264/AVC (`avc1`, yuv420p) plus AAC in fast-start MP4.
The earlier MPEG-4 Part 2 (`mp4v`) kit decoded in FFmpeg but showed audio only
in the built-in browser. A decode pass does not prove player compatibility: before
requesting human review, play the new frozen packet in its intended player and
confirm visible video dimensions and picture. If encoding changes, build a new
suite and answer template; old source hashes and answers do not transfer. The directory
must not exist; its parent must already exist. A failed build leaves an incomplete
folder to inspect; no existing data is overwritten. Use a fresh directory to retry.

```sh
python3 skills/video-production-router/scripts/media_pilot.py build /absolute/private/path/controls --seed 17
python3 skills/video-production-router/scripts/media_pilot.py verify /absolute/private/path/controls
```

The optional seed fixes the opaque case mapping/order. It does not promise identical
encoded bytes across machines, tool versions, build paths or generation timestamps.
The actual files and source/scorer revisions are hashed. No media is committed.

The layout separates:

- `reviewer/`: neutrally named MP4s, `task.json`, `answers-template.json` only;
- `operator/`: case mapping/gold, source manifest/generator snapshot, runtime versions, encoded reports and perturbation measurements;
- `freeze.json`: file hashes and the suite identity to which answers bind.

Encoded QA checks decode/duration, actual retained frame differences, black-frame
luma, heading contrast separation, door-state differences, final hold and actual
sound-versus-flash onset times. These measurements verify the injected signals,
not whether an independent viewer understands the scene or finds text unreadable.
The suite retains `authored_not_human_verified` / `pending_human` label status.
Keep any later independent human validation as a separate pinned receipt; do not
rewrite the frozen gold to improve provider scores.

Generation is bounded to eight 10-second clips; each encode has a 45s timeout,
local inspections use their existing limits, and frozen files are capped at 25 MiB.
Temporary raw frames use roughly 83 MB, reused per clip. Failed/changed/missing or
unexpected reviewer-packet files prevent verification/scoring.

## Review without exposing the answer key

Give the reviewer **only** the `reviewer/` files and the neutral task. Do not expose
`operator/`, gold, source recipes, encoded perturbation checks or previous scores.
Use a fresh reviewer session without generation history or prior calibration answers.
Use the same frozen packet for provider comparisons and retain the original raw
response separately. Submit a completed copy of the answer template **outside**
`reviewer/`; that folder rejects additional files to help prevent label leakage.

The public generation recipes are inspectable: this is label-blinded input packaging,
not an unseen/causal or adversarial benchmark. No automatic upload route is supplied.
Before a real cloud run, select the provider/model, actual data destination, account
and bounded budget. Local alternatives require resource preflight.

The response declares reviewer/version and run kind (`model`, `human`,
`synthetic_control`, or `not_run`). Each case pins source hash, actual input method,
continuous/sampled coverage, optional sampled fps, intervals, five explicit
`pass`/`fail`/`unknown` checks and timestamped findings. Supported finding categories
are `freeze`, `blackout`, `missing_action`, `av_sync`, `unreadable_text`,
`audio_artifact`. This batch injects no audio-noise fault; that category allows
spurious sound complaints to be retained and counted as false alarms.
Each failure needs observed evidence; an absent modality must stay unknown.
If raw output requires transformation, retain the raw response and explicit mapping;
do not silently rewrite answers to improve the result.

A declaration that video/audio was delivered remains supplied evidence, not proof
that provider bytes reached a model. Record the actual request/input receipt for
real trials. A transcript or frame sheet cannot pass audiovisual temporal checks.

## Score supplied answers

```sh
python3 skills/video-production-router/scripts/media_pilot.py score /absolute/private/path/controls /absolute/private/path/answers.json
python3 skills/video-production-router/scripts/media_pilot.py score /absolute/private/path/controls /absolute/private/path/answers.json --format markdown
```

The grader rejects duplicate/missing case IDs, stale suite/source pins, invalid
coverage/timestamps, contradictory passed checks and source/gold changes. It reports:

- true detections, false alarms and missed events;
- unassessed events and cases with sufficient modality/coverage;
- defective cases incorrectly given all-pass and clean controls correctly accepted;
- per-case effective checks, matched/missed event timestamps and unsupported findings.

Transient findings other than A/V sync match the same category with start error
≤0.5s and temporal intersection-over-union ≥0.25. A/V-sync findings may localise
the cue comparison window or the delayed beep: overlap must cover at least half
the shorter interval, and the finding may exceed the label duration by at most0.5s. Persistent heading-legibility and missing-action findings may use a
representative overlapping interval. Matching is one-to-one; duplicate reports do
not earn extra detections. A broad 2–9s sync claim does not replace two localised events.
A supported observed rejection may identify a fault in partial footage; acceptance
requires supported, continuous full-clip coverage. Sampled/partial passes and
unsupported modalities remain unknown. No missing evidence becomes a correct pass. An unreviewed event window stays
unassessed even if another event of the same kind was rejected.

Precision is null when no supported findings exist. Recall uses **all six authored
events**, so inspect unassessed counts alongside it. No scalar score or automatic
qualification is issued. The result always says `diagnostic_only`; label validation
remains pending. Synthetic scorer tests and the empty template say model evaluation
`not_performed`; user-supplied model answers are labelled as supplied, not independently
verified execution. The exact answer-byte hash and scorer hash are retained.

## Export to the existing report/journal

```sh
python3 skills/video-production-router/scripts/media_pilot.py observations /absolute/private/path/controls /absolute/private/path/answers.json --case c_OPAQUE_ID > /absolute/private/path/observations.json
python3 skills/video-production-router/scripts/media_review.py /absolute/private/path/controls/reviewer/c_OPAQUE_ID.mp4 --observations /absolute/private/path/observations.json > /absolute/private/path/review.json
```

Use an actual ID from the task; the placeholder is not executable. Export records
supplied reviewer/version, method, coverage, optional fps and findings. Unsupported
review kinds stay absent/pending; the unrun template cannot export observations.
A fault recommendation asks for inspection/correction, not an invented reshoot decision.
New builds label the missing-action condition for the full commanded-open interval
2–8s. Missing-action and unreadable-text findings match representative overlap,
rather than transient start/IoU limits. Keep existing frozen suites unchanged and
retain the scorer revision when comparing old results. Older suites whose
missing-action gold ends at3s have an incomplete label for that condition: archive
them unchanged and build a new suite before further missing-action comparisons.
Retain raw response, graded result and JSON report privately. Import the report with
`project.py review` as described in the unified-report guide; pin any additional
raw evidence separately when recording a real trial. No project check is auto-finished,
no reviewer is promoted and no production permission is inferred.
