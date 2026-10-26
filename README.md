# Framewright

![Framewright — craft the cut, keep the evidence](assets/framewright-cover.png)

[![Version: 0.4.0](https://img.shields.io/badge/version-0.4.0-293F48?style=flat-square)](https://github.com/markoblogo/framewright/releases/tag/v0.4.0)
[![License: MIT](https://img.shields.io/badge/license-MIT-E7BA6A?style=flat-square)](LICENSE)
[![Stage: experimental](https://img.shields.io/badge/stage-experimental-293F48?style=flat-square)](docs/router-evaluation.md)

**Reusable workflows, project memory and local tools for a video studio run with an AI agent.**

Turn approved sources into videos, keep the decisions and materials together,
and continue the next session without reconstructing the project from chat history.
Framewright helps the agent plan scenes, choose tools, reuse footage, check outputs
and prepare a local publication kit. The agent runs selected tools in your environment.

Watch the [two-minute Framewright workflow lesson](https://youtu.be/n1wuySSYQcQ): two-host dialogue and real production examples. Publication is owner-reported.

## Selected results

| Production | What it demonstrates | Watch / evidence |
| --- | --- | --- |
| A Dog Follows a Falling Light | An animated rig, deterministic camera/pose reconstruction, a motivated light event and actual travel into the ending | [30s film](https://youtu.be/B4zdWfFIkNE) · [Case](docs/experiments/little-light.md) |
| Seals of Good Intentions | Six photographs staged as a cinematic set, source-preserving calligraphy, reusable camera plan and revised soundtrack | [30s film](https://youtu.be/6c3JXdIiosg) · [Case](docs/experiments/photo-series-cinema.md) |
| The Same Forest | An existing virtual-world plate, independent character and three coordinated color/sound states | [42s film](https://youtu.be/wHOpypqPyCs) · [Case and original source](docs/experiments/marble-compositing.md) |
| Nantes green-line walk | Whole official route map, selected eye-level scenes and timed pixel/detail transitions; accepted first edit, sharper revision delivered | [100s film](https://youtu.be/IQ3CdzPzFHw) · [Case](docs/experiments/nantes-green-line.md) |
| Nantes illustrated journey | Real mapped road geometry, animated landmark illustrations and a French guide | [82s film](https://youtu.be/kh-MTl8K5pE) · [Case](docs/experiments/nantes-pixel-journey.md) |
| One Random Life | A complete browser-life playthrough condensed to 118s, with fictional age portraits and OCR source retrieval | [Film](https://youtu.be/bNpRyDZsCHg) · [Case](docs/experiments/one-random-life.md) |
| SSI report series | Three English voice-only films reuse one pinned brand profile; partner acceptance/publication owner-reported; SSI reports production integration deployed; first scheduled run pending | [Case](docs/experiments/ssi-brand-profiles.md) |
| SSI website Reels, Ukrainian and English | Real pages scrolling beneath fixed captions; an accepted edit reused for another language | [English Reels](https://www.instagram.com/reel/DezcjZ0tXuz/) · [Case](docs/experiments/ssi-site-reels.md) |
| Jekyll & Hyde book promo | A playable learning game used as a set for a book video, with owner-recorded Toki Pona narration | [Book promo](https://youtu.be/GPfkz36JWbI) · [Case](docs/experiments/jekyll-toki-pona.md) |
| Dream Walk films | A generated 60s cinematic film and a separate 20min ambient recording from an actual game canvas | [60s film](https://youtu.be/oyQXmJI4aK0) · [20min game capture](https://youtu.be/rfClK3jPHlw) · [Case](docs/experiments/dream-walk.md) |

Publication links and partner acceptance are owner-reported; the forest film’s watch-page title/duration were also observed. The repository records
[40 final exports](docs/experiments.md); production evidence, human acceptance and
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

For short educational films, the optional [micro-lesson recipe](skills/video-production-router/references/micro-lessons.md) joins two-host dialogue, source-backed explanations and real footage. [Two-minute Framewright pilot](docs/experiments/framewright-micro-lesson.md): technically checked and owner-accepted for publication, with a local YouTube kit; facial naturalness is a documented follow-up.

For short story-led book and project promos, the optional [narrative module](skills/video-production-router/references/narrative-promos.md) adds visible action, continuity and picture/sound cues to the same project workflow. It is planning-only; no generator or audience result is implied.

[DJV 3.7.5](docs/experiments/djv-review.md) passed A/B frame-note and session-persistence checks, with black-frame capture gaps retained. Repeat on the next one or two productions before production qualification. Chaos Vantage is retained as a Windows-only reference candidate, with no current test/use plan.

For recorded takes and screencasts, the [editing module](skills/video-production-router/references/editing.md) adds local source inspection, cut-only time maps, subtitle retiming and short review clips around joins. The helper is covered by synthetic CLI tests; editorial quality on a real recording remains to be assessed.

## Test a method before production

The [experiment workbench](skills/video-production-router/references/trials-and-readiness.md)
pins a bounded question and common sources, collects existing A/B outputs, records
time/cost and checks, and prepares a local review pack in the same project journal.
The separate readiness helper checks declared local prerequisites; rights, cost,
runtime/export success and execution authority stay distinct. Nothing installs,
generates or becomes a tested provider automatically.

Try the [text-only example](examples/trials/README.md), or read the
[saved-production replay and limits](docs/experiments/experiment-workbench.md).

For a controlled 3D correction, the optional [saved-shot adapter](skills/video-production-router/references/shots-and-passports.md)
restores a pinned Blender scene, edits one declared control and renders a selected
range. [Internal CPU probe](docs/experiments/blender-shot-replay.md):36 repeat frames
and12 subrange frames matched; light-only changes preserved action and PCM timing.
[Versioned passport drafts](examples/passports/README.md) prepare recurring characters
and sets; real production approval and visual identity checks remain separate.

## Correct a film and reuse its design

A [precise revision](skills/video-production-router/references/revisions.md) records the affected interval, defect, desired result and what must stay intact. The local helper prepares before/after clips with context; verification is recorded against the exact file revisions in the existing journal.

An [accepted-film template](skills/video-production-router/references/templates.md) separates fixed design from typed text, numbers, media and voice inputs. It prepares three content checks: short text, long text and absent optional media. These are renderer-independent packets; render and review the cases before using the template for a series. New variants receive their own approvals.

A [brand profile](skills/video-production-router/references/branding.md) pins a selected logo, font, palette and layout/motion rules, then exports the same assets and CSS variables for another production. Source changes are detected; new films retain their own content, rights and approval checks. [SSI three-part profile trial](docs/experiments/ssi-brand-profiles.md).

For production owned by another project, use the [external-project handoff](docs/external-project-handoff.md): accepted sources, typed inputs, measured voice timing, checks and receiving-project scheduling. SSI reports integration deployed at `fc8360e`, with its first run planned for 1 November 2026; scheduled delivery and new-video quality remain unverified.

[Source-editing example](examples/editing/source-plan.json) · [Template design](examples/templates/design.json) · [Template values](examples/templates/values.json) · [Curated prompt experiments](docs/research/prompt-library/README.md).

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

[Weekly English Studio Notes](docs/editorial/README.md) connect project development
to actual video examples, with ABVX metadata and a generated cover for every draft. A separate [book-readiness milestone](docs/book-milestone.md)
collects methods for AI-assisted video production. The [working book base](docs/book/README.md)
now has an outline, three case studies and future-example links, with parallel routes
using Framewright and other tools. Draft preparation and publication remain separate.

Framewright is experimental: workflows and local utilities, not a hosted renderer
or automatic publishing service. Human viewing/listening and creative approval
remain separate from technical checks. Paid calls, account access and uploads need
their own authority. Tools/models/media have separate terms; private assets stay outside Git.

[Production guide](docs/production-guide.md) · [Project and scene workflow](skills/video-production-router/references/production.md) ·
[Experiments and limits](docs/experiments.md) · [Current priorities](docs/next-cycle.md) ·
[Research queue](docs/experiment-queue.md) · [Contributing checks](docs/checking-policy.md) ·
[Current release audit](docs/release-audit-2026-10-26.md) · [Earlier production closeout](docs/closeout-2026-10-25.md).

MIT for original repository materials. v0.4.0 is an experimental prerelease. The [release audit](docs/release-audit-2026-10-26.md)
records package/check scope; current-source model routing is not newly evaluated. [ABVX ecosystem](docs/ecosystem.md).
