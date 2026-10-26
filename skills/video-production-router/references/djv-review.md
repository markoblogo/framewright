# DJV review sessions — provisional procedure

Use for an authorised comparison of retained revisions. Tested with DJV3.7.5 on
macOS arm64; [real trial](../../../docs/experiments/djv-review.md) is partially
successful. Keep DJV a candidate until repeat tests on the next one or two
productions establish reliable picture access and owner-reviewed usability.
This procedure does not install software, edit the film or confer approval.

1. **Pin the pair.** Preserve both exports. Record hashes, frame rates, start
   offsets and durations. Put review copies in `media/` beside `review.djvr`.
   A is the reviewed revision; B is its baseline. Use relative-time comparison
   only when their timing matches; document any mapping. Never infer a frame
   from another file's timecode. DJV uses A for timeline/audio; do not infer B's
   audio quality or sync from hearing A.
2. **Check actual pictures first.** Open both media, choose horizontal comparison
   or wipe, and inspect first/middle/last nonblack frames plus a short played
   passage. Set an explicit sensible zoom if auto-fit produces a blank view.
   `Playback/Seek {"frame":72}` uses a frame index, not seconds. Exit0, timeline
   thumbnails or a populated timecode are not picture evidence. Stop a failed
   scope rather than recording a pass. FFV1 diagnostic copies only helped one
   tested frame; do not prescribe them as a general fix. Pin any proxy's source
   interval, rate and offset, and keep the originals available.
3. **Anchor a bounded note.** Record source revision, exact frame/range, defect,
   desired change and preservation requirements. A drawing belongs to its source
   and frame; check it is absent on the adjacent frame. Distinguish actual defects
   from control/check notes. An exclusive range end is not the final displayed
   frame: [9,14.5) at24fps is216–347. Inspect neighbouring seconds when assessing
   motion. Programmatically authored session marks must be labelled as such.
4. **Save and verify.** Save `.djvr` (Mac: Cmd+Alt+S), close/reopen, then relocate a
   copy together with `media/`. Check actual resolved files, A/B, notes, frame/range
   anchors and drawing; verify masters' hashes unchanged. Positional launch is
   tested: `/Applications/djv.app/Contents/MacOS/djv /absolute/review.djvr`.
   Native Open-dialog selection has a retained gap. Startup `-screenshot` can run
   before decoded pictures. For the documented native capture harness,
   `-captureManifest manifest.json -captureShot id -captureOutput evidence`
   was exercised; pass a review file positionally, not as media in setup.open.
   Inspect every actual PNG; captures may still be black. Do not automate generic
   UI clicks through the capture harness.
5. **Bind existing evidence.** Declare/retain `djv-session`, `djv-notes`, `djv-report`
   with `project.py asset`/`retain`. Record separate technical receipts for
   persistence and visible-picture access, depending on the exact before/after
   export IDs and report. A pending/failed picture check remains pending/failed.
   Do not use a custom JSON field as a second approval database or auto-clear an
   owner-review wait. Replacing sources must stale dependent receipts through the
   normal journal rules. Regenerate the project summary; owner acceptance,
   listening, technical checks and publication remain separate.

Installed help/commands and version-pinned upstream docs define supported fields:
[reviews](https://grizzlypeak3d.github.io/DJV/reviews.html),
[format](https://grizzlypeak3d.github.io/DJV/review-format.html),
[automation](https://grizzlypeak3d.github.io/DJV/automation.html).
Keep original failures. Current-source docs may differ from the installed version.
