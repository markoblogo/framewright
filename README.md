# ABVX Video Lab

An evolving, evidence-led collection of video-production methods and agent skills.
Start with the task, choose the smallest useful workflow, keep the evidence, and
promote only the capability that was actually tested.

## Choose a workflow

| Need | Starting point | Evidence / limits |
| --- | --- | --- |
| Short software launch or landing-page introduction | Brag full workflow + Hyperframes | AsciiTheme and AMI delivered and accepted; narration not tested in these runs |
| Voiced book/product trailer using existing imagery | Hyperframes montage + local Kokoro + sound-layer mixing/QA | French and English book trailers delivered; not a general turnkey generator |
| Very short announcement | Short edit of an established composition | Six-second Good Dogs teaser; no audience-performance comparison |
| Detailed object visualisation | Anatomy + deterministic timeline adapter | Visual prototype worked; combined sound prototype failed QA and was stopped |
| Historical reconstruction, calibrated physics, new generative-video workflows | Research candidate | Not validated here; agree a bounded experiment first |

See [recipes](skills/video-production-router/references/recipes.md),
[catalogue](skills/video-production-router/references/catalog.json),
[experiment evidence](experiments/2026-10-14/README.md), and
[the local machine map](docs/local-workspace.md).

## Use with Codex

The original skill is [video-production-router](skills/video-production-router/SKILL.md).
Install only that skill folder in your Codex skills directory, or link it from a
stable checkout. It recommends a workflow; it does not install dependencies,
render a video or publish anything by itself. Existing Hyperframes skills remain
the rendering entry point and must still be followed when making a video.

Example: “Make a French trailer from this book page and cover. Use
$video-production-router to choose a workflow.”

The router is structurally validated. Its scenario suite has **not** yet been
evaluated by an independent model. This is separate from the completed video tests.

## Add the next experiment

Follow [the contribution protocol](docs/experiments.md), add an experiment record
using [the template](templates/experiment.md), then update the catalogue only if
the evidence justifies changing its tested scope. Tools may remain candidates.
No scheduled jobs or autonomous downloads are configured.

Run `python3 scripts/validate.py` to check catalogue integrity and retained evidence.
This check needs no network or third-party packages and does not run video tools.

## Published examples and notes

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
