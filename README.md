# Framewright

![Framewright — craft the cut, keep the evidence](assets/framewright-cover.png)

[![License: MIT](https://img.shields.io/badge/license-MIT-E7BA6A?style=flat-square)](LICENSE)
[![Stage: experimental](https://img.shields.io/badge/stage-experimental-293F48?style=flat-square)](experiments/2026-10-14/README.md)
[![Planning check: 29/29](https://img.shields.io/badge/planning__check-29%2F29-526C73?style=flat-square)](docs/router-evaluation.md)
[![8 recorded exports](https://img.shields.io/badge/recorded__exports-8-293F48?style=flat-square)](experiments/2026-10-14/outputs.json)
[![ABVX ecosystem](https://img.shields.io/badge/ecosystem-ABVX-E7BA6A?style=flat-square)](docs/ecosystem.md)

**Framewright helps an AI agent choose and execute a suitable video pipeline,
based on documented experiments.**

Not a new video engine. Tested recipes, limitations and result checks for existing
tools. Choose tools per scene and layer, then verify the assembled film.

## One concrete result

**Task:** a 30-second horizontal film introducing Framewright.
**Chain:** authored Remotion scenes + original locally synthesized music → native MP4
and PNG still.
**Video:** [watch the published example](https://youtu.be/s3BBP698_r8).
**Checked:** H264 1920×1080, 30 fps, 900 frames, stereo AAC, native PNG, sampled encoded
frames and transitions. Listening/owner artistic acceptance and audience performance
are separate; the public URL was supplied by the owner, not matched byte-for-byte.

[Reproduce the open reference project](docs/first-video.md) with shared demo assets,
pinned versions, exact commands, an agent prompt and expected outputs.
[Release 0.1.1](CHANGELOG.md) remains experimental. Unreleased updates now include a
[29-case scoped planning check](docs/router-evaluation.md); no new release is made.

## Plan by scene, style and effect

Start with [selection guidance](skills/video-production-router/references/selection.md)
and [the capability matrix](skills/video-production-router/references/tool-matrix.md).
Ten tool profiles distinguish tested, documented, failed and unknown functions.
Styles guide direction; they are not fixed engine limits or quality scores.

For a multi-tool film the agent decomposes the request into blocks/layers. The offline
planner can check the shortlist and frame timeline without installing or rendering:

```sh
python3 skills/video-production-router/scripts/plan.py examples/briefs/mixed-promo.json
```

That 30-second mixed example is a **proposed plan**, not another tested film. Each new
combination needs an integration test. [Selection audit](docs/selection-audit.md).

## Music, songs and native video

Plan in three directions: **brief → music/song → picture**, **fixed video → music**,
or **existing music → video**. Keep singing distinct from spoken narration. Suno and
Flow Music have documented provider profiles; native song cards, animated cover art
and generated scenes are different assets that can join a larger toolchain.

[Music workflow guide](skills/video-production-router/references/music-workflows.md)
explains timing, lyrics, supported downloads, independent usage-rights checks and
encoded QA. Personal/noncommercial restrictions do not mean a tool cannot work.
Account access and an asset's permitted use need separate verification.

```sh
python3 skills/video-production-router/scripts/music.py examples/briefs/music-video-first.json
```

This is an offline plan, not a service integration or rendering command. These
additions are unreleased; private microtests do not qualify public capabilities.
See [related projects and borrowed ideas](docs/related-work.md) and the
[prioritised experiment queue](docs/experiment-queue.md). No queued job runs itself.

## Choose a workflow

| Need | Starting point | Evidence / limits |
| --- | --- | --- |
| Short software launch or landing-page introduction | Brag full workflow + Hyperframes | AsciiTheme and AMI delivered and accepted; narration not tested in these runs |
| Voiced book/product trailer using existing imagery | Hyperframes montage + local Kokoro + sound-layer mixing/QA | French and English book trailers delivered; not a general turnkey generator |
| Very short announcement | Short edit of an established composition | Six-second Good Dogs teaser; no audience-performance comparison |
| Cinematic camera/focus around existing React UI | Flute + a development-only component host | CoqPi browser-renderer export verified; full Electron and snapshot CLI remain limited |
| Authored React motion graphics and editable scene timing | Remotion + official skills | Framewright film: native audio/still/MP4; explicit browser workaround and own licence |
| Detailed object visualisation | Anatomy + deterministic timeline adapter | Visual prototype worked; combined sound prototype failed QA and was stopped |
| Historical reconstruction, calibrated physics, new generative-video workflows | Research candidate | Not validated here; agree a bounded experiment first |

See [recipes](skills/video-production-router/references/recipes.md),
[catalogue](skills/video-production-router/references/catalog.json),
[experiment evidence](experiments/2026-10-14/README.md), and
[the local machine map](docs/local-workspace.md).

## Combine tools when needed

A workflow can use several tools. Keep the renderer that does its job, then add a
small companion for a missing deliverable. In the CoqPi pilot, Flute supplied the
camera/React video; FFmpeg added music and extracted a thumbnail after the portable
snapshot command failed. Validate the assembled file and keep each tool's limits
visible. See [tool-chain guidance](skills/video-production-router/references/tool-chains.md).

## Quick start

1. For a first result, follow the complete [open reference route](docs/first-video.md).
   For your own brief, ask `$video-production-router` or use the table above.
2. Follow the selected recipe with your own authorised product inputs.
3. Record the result, including failures, before adding a new tested capability.

**Not a renderer, hosted service, or one-click historical simulator.** Framewright
is the selection and learning layer around production tools you choose to run.

## Use with Codex

The original skill is [video-production-router](skills/video-production-router/SKILL.md).
Install only that skill folder in your Codex skills directory, or link it from a
stable checkout. For a clone already reviewed locally:

```bash
git clone https://github.com/markoblogo/framewright.git
mkdir -p ~/.codex/skills
ln -s "$(pwd)/framewright/skills/video-production-router" ~/.codex/skills/video-production-router
```

The link command refuses to overwrite an existing skill. Keep the checkout mounted
and use the skill in a fresh Codex session. No upstream video tools are installed.
 It recommends a workflow; it does not install dependencies,
render a video or publish anything by itself. Follow the selected renderer’s guide. Installed Hyperframes skills are required
for Hyperframes-backed routes; Flute and Remotion use their own guides.

Example: “Make a French trailer from this book page and cover. Use
$video-production-router to choose a workflow.”

The current decision sources passed **29/29 synthetic planning cases**; the evaluator
passed **12/12 positive/negative controls**. [Results and reproduction](docs/router-evaluation.md)
retain earlier failures and the new unambiguous rubric. The
[scoped qualification](router-qualification.json) is checked against current source,
prompt and fixture hashes. This covers planning with the named model/configuration;
automatic discovery, production permissions and media quality remain separate scopes.

## Add the next experiment

Follow [the contribution protocol](docs/experiments.md), add an experiment record
using [the template](templates/experiment.md), then update the catalogue only if
the evidence justifies changing its tested scope. Tools may remain candidates.
No scheduled jobs or autonomous downloads are configured.

Run `python3 scripts/validate.py` to check catalogue integrity and retained evidence.
Run `python3 scripts/check_router_evaluation.py --root benchmarks/router --qualification router-qualification.json`
to verify current planning qualification and its source snapshots.
Run `python3 -m unittest discover -s tests -v` for validator regression tests.
With `--local-root /Volumes/Work`, the validator checks both final and recorded
native export files and recorded thumbnails against their sizes and SHA-256
hashes; PNG thumbnail dimensions are checked too.
This check needs no network or third-party packages and does not run video tools.

## Part of the ABVX ecosystem

[ABVX Agent Skills](https://github.com/markoblogo/abvx-agent-skills) provides general
workflows; [SET](https://github.com/markoblogo/SET) coordinates optional plans;
[AGENTS.md Generator](https://github.com/markoblogo/AGENTS.md_generator) maintains
repository context; [ABVX Lab](https://github.com/markoblogo/lab.abvx) is the public
discovery surface. Framewright owns video methods and their evidence. None is a
mandatory runtime dependency. See [the integration boundaries](docs/ecosystem.md).

## Published examples and notes

- [Framewright identity film: Remotion](https://youtu.be/s3BBP698_r8)

- [CoqPi cinematic React demo](https://youtu.be/rqKXx_Z5AR0)

- [French book trailer: Jeanne la bataillonneuse](https://youtu.be/PmhWa-V00zc)
- [English series trailer: Good Dogs of the Apocalypse](https://youtu.be/89kTx1LhEP0)
- [First experiment: Brag review](https://abvx.xyz/writing/brag-ai-agent-skill-launch-videos-review)

YouTube links are supplied publication references, not byte-verified copies of the
local exports. No viewer-engagement or conversion improvement is claimed.

## Scope and licensing

This repository contains our original routing instructions, recipes and small
technical evidence records. It does not bundle upstream skills, software, model
weights, book art, music or video masters. Follow each upstream project's licence;
do not assume the MIT licence here grants rights to any linked assets.
Local media and reproducibility workspaces remain on the external Work drive.
