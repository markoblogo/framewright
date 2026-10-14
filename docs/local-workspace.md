# Local artifact map (optional, machine-specific)

These external-drive paths are pointers, not portable dependencies. Missing paths
do not invalidate the retained summaries, but prevent local reruns. Do not upload
their contents wholesale.

| Workspace | Contents |
| --- | --- |
| /Volumes/Work/brag-pilot-20261014 | Brag skill snapshot, scoped Hyperframes toolchain, AsciiTheme/AMI compositions and exports |
| /Volumes/Work/anatomy-sound-pilot-20261014 | Upstream clones, deterministic adapter, failed prototype, sound mixer/QA scripts |
| /Volumes/Work/book-trailer-jeanne-20261014 | French build_trailer.py, composition, synthesize.py, local Kokoro models/venv, audio, QA, delivery |
| /Volumes/Work/good-dogs-trailer-20261014 | English build.py, synthesize.py, composition/teaser, audio revisions, final QA and delivery |
| /Volumes/Work/video-experiment-article-20261014 | Generated article cover |

There is no frozen portable environment or clean-machine reproduction test yet.
Inspect project scripts and upstream docs before reusing them. Kokoro and sound
scripts ran in an isolated Python 3.12 environment after a Python 3.14 dependency
loading stall. Do not automatically reinstall or relocate the archived workspaces.

- /Volumes/Work/flute-pilot-20261014 — isolated CoqPi branch, Flute source inspection,
  pinned installed package/browser, native and finished exports, thumbnail, English
  YouTube metadata and validation logs. Owner-provided video URL is retained in the experiment record.

- /Volumes/Work/remotion-pilot-20261014 — official skill mirror, isolated Remotion
  composition, browser/cache, native MP4/still, audio sources, English YouTube copy
  and QA logs. Our authored source is also retained in examples/remotion-framewright.

## Text-only evaluations and new source inspection

- /Volumes/Work/framewright-transfer-20261014 — first-exposure 12-case router
  trial; unchanged actor answers and both grading-context attempts.
- /Volumes/Work/framewright-storyboard-upstream-20261014 — pinned upstream source
  inspection; not a global installation or a vendored skill.
- /Volumes/Work/framewright-storyboard-test-20261014 — four raw upstream text
  cases, no media generation.
- /Volumes/Work/framewright-storyboard-integrated-20261014 — complete 46-case
  integrated-source run, raw traces, package smoke and fresh-clone checks.

Public evidence lives in benchmarks/router and benchmarks/storyboard. Original
upstream files, full machine-local streams and trial workspaces stay on Work.
Source-snapshot reconstruction is verified without old Git objects; it does not
establish clean-machine media-render reproducibility. No new render or release.
