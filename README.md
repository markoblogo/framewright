# Framewright

![Framewright — craft the cut, keep the evidence](assets/framewright-cover.png)

[![Version: 0.3.1](https://img.shields.io/badge/version-0.3.1-293F48?style=flat-square)](https://github.com/markoblogo/framewright/releases/tag/v0.3.1)
[![License: MIT](https://img.shields.io/badge/license-MIT-E7BA6A?style=flat-square)](LICENSE)
[![Stage: experimental](https://img.shields.io/badge/stage-experimental-293F48?style=flat-square)](docs/router-evaluation.md)
[![Planning evidence: scoped](https://img.shields.io/badge/planning__evidence-scoped-526C73?style=flat-square)](docs/router-evaluation.md)
[![26 recorded exports](https://img.shields.io/badge/recorded__exports-26-293F48?style=flat-square)](docs/experiments.md)

**Framewright helps an AI agent plan and resume video production, reuse materials
and prepare a reviewable local publication kit, using documented methods.**

Built as a personal AI video studio for YouTube, ABVX and other projects; open
source, with quality and saved production time as the priority.

Framewright provides instructions and planning checks; your agent executes the
selected tools in your environment. Choose tools per scene and layer, with evidence,
known limitations and output checks visible before production.
Books and software promos are the first test cases, not the product boundary.
New genres and tool combinations need scoped evidence before qualification.

| Start here | What you get |
| --- | --- |
| **Try a production plan** — command below | A readable timeline, tools, intended files, blockers and QA; no rendering |
| **[Find tools and combinations](skills/video-production-router/references/arsenal-search.md)** | Task/style/language/rights/evidence filters with scoped results |
| **[Save and resume work](skills/video-production-router/references/projects.md)** | Goal, frozen plan, file pins, revision-bound decisions and next steps |
| **[Connect scenes, reuse assets and collect a kit](skills/video-production-router/references/production.md)** | Shared materials, independent main/Short cuts and visible delivery checks |
| **[Inspect audio/video and retain a review](skills/video-production-router/references/media-review-reports.md)** | Local technical report, supplied timestamped findings, unresolved checks and revision-bound journal import |
| **[Render the reference film](docs/first-video.md)** | Open demo assets, pinned dependencies, exact commands and expected outputs |

Before a full operator take, run the local [recording rehearsal check and media-review workflow](skills/video-production-router/references/media-review.md). Technical measurements, actual listening/viewing and owner acceptance remain separate. The [video-control pilot](skills/video-production-router/references/media-perception-pilot.md) provides frozen known-defect clips and diagnostic scoring. [Free Gemini UI trials](docs/experiments/gemini-media-review.md) produced a correct freeze finding and no findings on one clean control, but failed the separate audio check. No multimodal reviewer or automatic acceptance route is qualified.

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

Use [arsenal search](skills/video-production-router/references/arsenal-search.md) before freezing a brief,
then [save a project](skills/video-production-router/references/projects.md) for work across sessions.
Search rights remain conditional;resume checks file pins and never executes production.

**Production workflows:** [repackaging, insight → video and hybrid production](docs/personal-studio.md)
share source/rights, facts, edit decisions and delivery gates. A private audio catalogue
indexes owner-selected folders;[first2-track bank use](docs/workflows/private-music-bank.md)
is recorded separately. A/B/C remain infrastructure only;no new A/B/C films or models tested.
For another project’s recurring videos, use the [demo-to-template production handoff](skills/video-production-router/references/studio-workflows.md#production-handoff-to-another-project): validate the format here, then transfer production and publication ownership to that project.

## Games and game engines

Game engines are also a production direction: **create playable games, make
reviews of games and engines, and stage original video stories in interactive
worlds**. A world may supply an interior, characters, camera moves and action for
a film whose subject has nothing to do with the engine.

Three PlayMCP games are published. Two have retained overview/Shorts evidence;
the third supplied a virtual set for a book promo. The owner also supplied the
[completed service review](https://youtu.be/NVeMJLidncU) URL: real site captures,
three working examples, owner narration and recorded credit usage.
[Case and tool limits](docs/experiments/playmcp-service-review.md) ·
[Game-engine workflow](docs/workflows/game-engines.md) ·
[Agent skill](skills/game-engine-production/SKILL.md).

**Next cycle:** the [SSI site Reels](docs/experiments/ssi-site-reels.md) is delivered
and accepted by partners (owner report); the matching English version is delivered,
with owner preview acceptance.
Weekly-report demos were not accepted; that branch is paused pending a separate
partner specification. Pocket OS capture preparation follows this closeout and adaptation.
A YouTube Radar-led video and a short-fiction/world-production pilot are in intake.
[Status, inputs and development priorities](docs/next-cycle.md).

A separate [SSI OAuth demo](docs/experiments/ssi-oauth-field-report.md) records
another agent using Framewright for real-screen evidence video; its temporary
unlisted upload and playback are owner-confirmed, Google approval is pending.
Other engines and general autonomous production remain unqualified.

## One concrete result

[Watch the 60s book-library compilation](https://youtu.be/vAPgNupIp2s)
(owner-supplied URL): retained films + real-site tour, MoviePy/FFmpeg and Supertonic.
[Method and QA](experiments/2026-10-15/agro-series-compilation.md) ·
[Closed eight-film stage](docs/experiments/agro-series-plan.md).
Private author assets are not redistributed; use the open reference film to start.

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
| Vertical site promo with fixed captions | Native browser frames → FFmpeg → HyperFrames | Two 15s SSI Reels (UK/EN); sampled QA retained; UK partner acceptance owner-reported |
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

For games, engine reviews and virtual sets, also link
`framewright/skills/game-engine-production` into your skills folder from this
complete checkout. The release ZIP installs the router skill only; GitHub source
archives include both skills and their case documentation. ZIP case links point
to the matching tagged source; core planning/project references remain local.

Keep the checkout mounted and start a fresh Codex session. The command refuses to
overwrite a skill. Example: “Plan a French trailer from this page and approved cover.
Use $video-production-router. Do not render yet.” Follow the selected tool’s guide
before authorised execution.

## Evidence and experimental scope

Current source has **no fresh model qualification**. Historical scores are
source-bound and do not establish general reliability or render quality.
[Evaluation, exact scores and limitations](docs/router-evaluation.md).

[Storyboarding](docs/storyboard-adapter.md) is a preparation layer.
[Music/song workflows](skills/video-production-router/references/music-workflows.md)
are offline planning, with independent rights/account gates; public service integration
is unqualified. Strict budget/download-limit validation is deferred; `allow_paid`
filters capabilities and grants no spending authority.

## Develop and extend

Run `python3 scripts/check.py --scope docs` for offline validation; no model/render.
[Checking policy](docs/checking-policy.md) · [Record an experiment](docs/experiments.md) ·
[Research queue](docs/experiment-queue.md) · [Release audit and remaining work](docs/release-audit-2026-10-19.md).

The MIT licence covers original repository materials. Tools, models, music and art
have their own terms. Large media remain outside Git. [ABVX ecosystem](docs/ecosystem.md) ·
[Project page](https://abvx.xyz/work/framewright).
