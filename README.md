# Framewright

![Framewright — craft the cut, keep the evidence](assets/framewright-cover.png)

[![License: MIT](https://img.shields.io/badge/license-MIT-E7BA6A?style=flat-square)](LICENSE)
[![Stage: experimental](https://img.shields.io/badge/stage-experimental-293F48?style=flat-square)](docs/router-evaluation.md)
[![Planning evidence: scoped](https://img.shields.io/badge/planning__evidence-scoped-526C73?style=flat-square)](docs/router-evaluation.md)
[![17 recorded exports](https://img.shields.io/badge/recorded__exports-17-293F48?style=flat-square)](docs/experiments.md)

**Framewright helps an AI agent choose a video pipeline and prepare its production
handoff, using documented experiments.**

Framewright provides instructions and planning checks; your agent executes the
selected tools in your environment. Choose tools per scene and layer, with evidence,
known limitations and output checks visible before production.
Books and software promos are the first test cases, not the product boundary.
New genres and tool combinations need scoped evidence before qualification.

| Start here | What you get |
| --- | --- |
| **Try a production plan** — command below | A readable timeline, tools, intended files, blockers and QA; no rendering |
| **[Render the reference film](docs/first-video.md)** | Open demo assets, pinned dependencies, exact commands and expected outputs |

## Try a production plan

From a local checkout, with Python 3; no third-party Python packages required:

```sh
python3 skills/video-production-router/scripts/plan.py examples/briefs/mixed-promo.json --format markdown
```

An agent first turns your request into a structured brief. This offline command
does not interpret prose or inspect your assets. Its [actual output](examples/plans/mixed-promo.md)
starts with this 30-second timeline:

| Scene | Duration | Selected tools |
| --- | --- | --- |
| Intro | 6s | Remotion |
| Interface | 8s | Flute |
| Object | 6s | Anatomy → Hyperframes |
| Book | 6s | Hyperframes + Kokoro |
| Outro | 4s | Remotion |

The packet then lists capability evidence, required inputs, suggested output files,
separate video/still/voice checks and retained tool limits. Checks are **planned**
or **blocked**, never automatically verified. This combined pipeline needs its own
integration test. Omit `--format markdown` for the unchanged JSON interface.
[Packet guide and limits](docs/production-plan.md).

## One concrete result

**Task:** introduce a library of practical commodity-market books.
**Chain:** retained book films + real-site tour → MoviePy/FFmpeg, new English
Supertonic narration and a retained original instrumental bed.
**[Watch the 60s compilation](https://youtu.be/vAPgNupIp2s)** ·
**[Method and QA](experiments/2026-10-15/agro-series-compilation.md)**

Recorded checks include 1080p30 H264/AAC, full decode, scene/transition samples,
audio sync/loudness/phase and a separate PNG thumbnail. Publication URL is
owner-supplied; final-film owner listening/style review remains separate.
The [completed stage](docs/experiments/agro-series-plan.md) contains six books,
one landing tour and this compilation. These author-project assets are not redistributed;
use the [open reference film](docs/first-video.md) for a public starting example.

## Choose a method

| Need | Starting chain | Scope / limitation |
| --- | --- | --- |
| Short software introduction | Brag → Hyperframes | Delivered software pilots; narration not tested in those pilots |
| Existing book art with speech | Hyperframes + voice + FFmpeg | EN/FR Kokoro; Supertonic EN/UK scopes recorded separately |
| Camera/focus around genuine React UI | Flute → finishing | Browser-host pilot; Electron/snapshot limitations retained |
| Authored typography or paper/LCD graphics | Remotion | Scoped films and native stills; licence/browser checks required |
| Object action and camera in a miniature world | Three.js → Hyperframes or authored Remotion | Recorded scenes; new geometry, physics and mixed seams unqualified |
| Workflow diagram | ManimGX → FFmpeg | Recorded timing adapter; setup-budget overrun retained |
| Live-site walkthrough | OpenScreen → FFmpeg | Manual recipe with capture/freeze workarounds; not an automatic planner provider |
| Recut existing films | MoviePy + FFmpeg | Manual compilation recipe; automatic semantic selection unqualified |

[Recipes](skills/video-production-router/references/recipes.md) ·
[Capability matrix](skills/video-production-router/references/tool-matrix.md) ·
[Per-layer selection](skills/video-production-router/references/selection.md).
A method can be documented without being an automatically selectable provider.

## Use the agent skill

For a reviewed clone in a stable location:

```sh
git clone https://github.com/markoblogo/framewright.git
mkdir -p ~/.codex/skills
test ! -e ~/.codex/skills/video-production-router && \
  test ! -L ~/.codex/skills/video-production-router && \
  ln -s "$(pwd)/framewright/skills/video-production-router" ~/.codex/skills/video-production-router
```

Keep the checkout mounted and start a fresh Codex session. The command refuses to
overwrite a skill. Example: “Plan a French trailer from this page and approved cover.
Use $video-production-router. Do not render yet.” Follow the selected tool’s guide
before authorised execution.

## Evidence and experimental scope

Current source has **no fresh model qualification**. Historical source-bound checks:
**70/70 rubric; 62/70 complete traces**, separate recovery **8/8**, original
first-exposure **13/18**. Scores are not added together and do not establish general
reliability or render quality. [Full evaluation](docs/router-evaluation.md).

[Storyboarding](docs/storyboard-adapter.md) is a preparation layer.
[Music/song workflows](skills/video-production-router/references/music-workflows.md)
are offline planning, with independent rights/account gates; public service integration
is unqualified. Strict budget/download-limit validation is deferred; `allow_paid`
filters capabilities and grants no spending authority.

## Develop and extend

Run `python3 scripts/check.py --scope docs` for offline validation; no model/render.
[Checking policy](docs/checking-policy.md) · [Record an experiment](docs/experiments.md) ·
[Research queue](docs/experiment-queue.md) · [Stage audit](docs/product-audit-2026-10-15.md).

The MIT licence covers original repository materials. Tools, models, music and art
have their own terms. Large media remain outside Git. [ABVX ecosystem](docs/ecosystem.md) ·
[Project page](https://abvx.xyz/work/framewright).
