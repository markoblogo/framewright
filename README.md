# Framewright

![Framewright — craft the cut, keep the evidence](assets/framewright-cover.png)

[![Version: 0.3.1](https://img.shields.io/badge/version-0.3.1-293F48?style=flat-square)](https://github.com/markoblogo/framewright/releases/tag/v0.3.1)
[![License: MIT](https://img.shields.io/badge/license-MIT-E7BA6A?style=flat-square)](LICENSE)
[![Stage: experimental](https://img.shields.io/badge/stage-experimental-293F48?style=flat-square)](docs/router-evaluation.md)

**Reusable workflows, project memory and local tools for a video studio run with an AI agent.**

Turn approved sources into videos, keep the decisions and materials together,
and continue the next session without reconstructing the project from chat history.
Framewright helps the agent plan scenes, choose tools, reuse footage, check outputs
and prepare a local publication kit. The agent runs selected tools in your environment.

## Three results

| Production | What it demonstrates | Watch / evidence |
| --- | --- | --- |
| SSI website Reels, Ukrainian and English | Real pages scrolling beneath fixed captions; an accepted edit reused for another language | [English Reels](https://www.instagram.com/reel/DezcjZ0tXuz/) · [Case](docs/experiments/ssi-site-reels.md) |
| Jekyll & Hyde book promo | A playable learning game used as a set for a book video, with owner-recorded Toki Pona narration | [Book promo](https://youtu.be/GPfkz36JWbI) · [Case](docs/experiments/jekyll-toki-pona.md) |
| Dream Walk films | A generated 60s cinematic film and a separate 20min ambient recording from an actual game canvas | [60s film](https://youtu.be/oyQXmJI4aK0) · [20min game capture](https://youtu.be/rfClK3jPHlw) · [Case](docs/experiments/dream-walk.md) |

Publication links and partner acceptance are owner-reported. The repository records
[30 final exports](docs/experiments.md); production evidence, human acceptance and
audience results remain separate. Faster production and better retention are goals,
not established comparative results.

## Try one production plan

From a local checkout, with Python 3 and no third-party Python packages:

```sh
python3 skills/video-production-router/scripts/plan.py examples/briefs/mixed-promo.json --format markdown
```

This prints a scene-by-scene plan with tools, intended files and remaining checks.
It does not render, install software or call a model. [Example output](examples/plans/mixed-promo.md).
For agent use, follow the [skill setup](docs/production-guide.md#use-the-agent-skill).

## Continue after an input changes

Retain the intended revision in the existing project. Its dependent checks become
stale or reopen. At the next session, generate a short working brief:

```sh
python3 skills/video-production-router/scripts/project.py brief local/my-film/project.json
```

The brief shows current accepted work, file problems, recorded replacements,
unresolved checks and explicit waits. It proposes a next step without approving
or executing it. [Commands and a real project example](skills/video-production-router/references/project-insights.md#start-a-session-with-a-working-brief).

## Scope and further reading

Framewright is experimental: workflows and local utilities, not a hosted renderer
or automatic publishing service. Human viewing/listening and creative approval
remain separate from technical checks. Paid calls, account access and uploads need
their own authority. Tools/models/media have separate terms; private assets stay outside Git.

[Production guide](docs/production-guide.md) · [Project and scene workflow](skills/video-production-router/references/production.md) ·
[Experiments and limits](docs/experiments.md) · [Current priorities](docs/next-cycle.md) ·
[Research queue](docs/experiment-queue.md) · [Contributing checks](docs/checking-policy.md).

MIT for original repository materials. Main includes work after the latest tagged
release; this update creates no new release. [ABVX ecosystem](docs/ecosystem.md).
