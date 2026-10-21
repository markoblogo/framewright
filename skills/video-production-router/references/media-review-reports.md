# One report for audio/video inspection

`media_review.py` combines local technical measurements with explicitly supplied
listening/viewing observations. JSON is the retained report; Markdown is a readable
view of that same report. It does not call a model, upload media, alter recordings,
clone voices, approve publication or finish project tasks.

## Generate and read a report

Requires existing FFmpeg/ffprobe. Use an explicitly selected regular local audio/video
file, up to **20 minutes / 1 GiB / 16 streams**. Metadata inspection has a 30-second
limit; full audio/video decode has a 180-second limit. A timeout records incomplete
inspection, never a completed decode. Still images are outside this command's scope.

From the checkout, create a private output folder explicitly:

```sh
mkdir -p local/review
python3 skills/video-production-router/scripts/media_review.py /absolute/path/take.mp4 > local/review/take-review.json
python3 skills/video-production-router/scripts/media_review.py --read local/review/take-review.json --format markdown
```

The first command measures metadata and decodes the file. For files within the
existing 60-second / 100-MiB calibration limits, it also reuses `capture_check.py`:
per-channel sample peaks/RMS, silence/near-full-scale guidance and sampled video
luma. Longer or larger files show that calibration was not performed. Saved reports must
keep calibration status consistent with decode success and the short-capture limits;
a performed calibration must include measurements for every applicable stream. A technical pass means
metadata, positive decoded duration/frame evidence and decode completed, not that loudness, focus, pronunciation or style passed.
Calibration failure/limits and individual flags remain visible in the report.
Stream metadata is retained. Decode timing substantially shorter than metadata is
flagged for investigation; it is not silently accepted. Multi-stream sources keep
perceptual acceptance pending: review separate selected-stream derivatives first.
A source changed during inspection is rejected. No packages are installed automatically.

`--read` validates/displays the historical report without decoding or checking the
current media path. It cannot establish that the media still matches. Project import
below verifies current retained media and report bytes.

## Add actual review observations

Use a separate JSON file whose `source_sha256` is the exact inspected source hash.
Each applicable kind has at most one consolidated review: `content`, `visual`,
`motion`, `listening`, `sync`. Audio-only sources need content/listening; video-only
sources content/visual/motion; audiovisual sources need all five.

```json
{
  "source_sha256": "REPLACE_WITH_EXACT_SOURCE_SHA256",
  "reviews": [
    {
      "kind": "listening",
      "actor": "owner",
      "reviewer_version": "human",
      "provenance": "owner_report",
      "method": "audio",
      "coverage_type": "continuous",
      "coverage": [[0, 12.5]],
      "result": "rejected",
      "findings": [
        {
          "start": 4.1,
          "end": 5.2,
          "severity": "error",
          "note": "The product name needs another take.",
          "action": "Record this phrase again with the agreed pronunciation.",
          "reshoot": true
        }
      ]
    }
  ]
}
```

This is a format example, not an actual review. Replace hash, coverage, timestamps,
reviewer and observations with facts about the selected file. Provenance may be
`owner_report`, `operator_observation`, `supplied_report` or `independent_check`;
the command records that assertion, not independent verification of it. Model
reviews must identify the model/version and actual delivered input modality.

```sh
python3 skills/video-production-router/scripts/media_review.py /absolute/path/take.mp4 --observations local/review/observations.json > local/review/take-review.json
```

Methods are `audio`, `video`, `audio_video` or `frames`. Frame reviews must be marked
`sampled`; they cannot pass motion/sync checks. Transcripts cannot pass listening.
Optional `sampled_fps` records a known sampling rate (positive, at most 240);
use null/omit when unknown, and never attach it to continuous coverage.
An accepted continuous review must cover the full duration to resolve its kind;
partial or sampled acceptance stays pending in the summary. A rejection in a covered
interval remains a rejection. Timed findings must be within reviewed coverage.
An accepted review cannot retain error findings or a reshoot request.

The summary lists results by kind, supplied findings/actions with timestamps,
explicit reshoot requests and unresolved scopes. Zero recorded reshoot requests
means none was supplied; it does not mean no reshoot is needed. Source words and
findings render as literal Markdown text. Input JSON is limited to 8 MiB; malformed,
non-finite, stale-source and inconsistent-summary reports are rejected.

## Attach to the existing production journal

Retain media and report separately. The JSON report becomes a revision dependency
of the imported observations; do not pin just its Markdown presentation.

```sh
python3 skills/video-production-router/scripts/project.py create local/review/project.json --goal 'Review take' --note 'Local inspection; no production or publication'
python3 skills/video-production-router/scripts/project.py retain local/review/project.json take /absolute/path/take.mp4 --input
python3 skills/video-production-router/scripts/project.py retain local/review/project.json take-report local/review/take-review.json --input
python3 skills/video-production-router/scripts/project.py review local/review/project.json input:take --report input:take-report --actor operator
python3 skills/video-production-router/scripts/project.py journal local/review/project.json --json
```

Existing projects may use an `output:ID` media subject and either retained input or
output report ID. Both files must already be pinned and unchanged; report source
hash/bytes must match the media pin. `project.py review` reads JSON only: it does not
rerun FFmpeg or call a reviewer. Imported receipts use **supplied_report** provenance,
with separate technical, creative and (when applicable) listening results. The
original reviewer details remain in the pinned report. Creative acceptance requires
all applicable non-listening perceptual scopes; technical pass cannot fill them in.
The imported technical QA receipt requires both successful local decode and accepted
applicable visual, motion and sync reviews. A rejected playback scope makes this
receipt fail; a pending scope keeps it pending, blocking linked QA/delivery tasks.
The report's local `technical.result` still describes metadata/decode only.
Its `perceptual_result` reflects the applicable review judgments; a decode failure
remains a separate technical blocker even when all supplied reviews are accepted. Content
preference remains a separate creative receipt; listening remains separately gated.

The command creates journal observations with `media-review:KIND` topics. Pending,
rejected or stale evidence blocks relevant existing check tasks. Replacing media or
report revisions invalidates linked evidence using the existing journal/dependency
rules. Historical approvals are retained, not resurrected. Import never automatically
marks checks or delivery done, and it grants no publication permission.

Reports contain local paths, voice/media metadata and operator findings: keep them
in private project storage. Tests use generated synthetic media only; no personal
recording or test clip is committed. General model-based audio/video understanding,
language accuracy and creative judgement remain unqualified until their own pilots.

For an original known-defect test set and compatible observation export, use the
[video-perception control pilot](media-perception-pilot.md). It does not itself
execute or qualify any model.
