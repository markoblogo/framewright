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
  YouTube metadata and validation logs. No public video URL yet.
