# Framewright

[![Framewright — silver FW ribbon unfolding](assets/fw-unfold.gif)](https://markoblogo.github.io/framewright/)

[![GitHub releases](https://img.shields.io/badge/GitHub-releases-293F48?style=flat-square)](https://github.com/markoblogo/framewright/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-E7BA6A?style=flat-square)](LICENSE)

**Research-driven filmmaking. Every production adds to the method.**

Framewright is an independent creative studio and production lab by
[Anton Biletskiy-Volokh](https://abvx.xyz). I create films, explainers and visual
experiments while investigating how **AI tools, visual styles and production
techniques work together**.

The research unit is a real production: a creative result, the combination of
tools and techniques behind it, and the revisions that made it work. Findings,
failures and useful corrections are retained as recipes and checks for later
projects. The process grows through practical work and human review.

**The ambition is creative freedom across styles and toolsets**: build the right
approach for the idea, with technical feasibility, access, time and budget guiding
what can be achieved. This is an open-ended research direction, not a claim to
have tested every tool or solved every kind of scene. Current capabilities and
limits are linked to actual cases below.

[Watch the work](https://markoblogo.github.io/framewright/#work) ·
[Work with me](https://markoblogo.github.io/framewright/#contact) ·
[Explore the methods](docs/start-here.md)

## Three ways to work together

### Make a film

For brands, authors and organisations with a product to explain, a story to tell
or a visual idea to explore. Discuss a film, explainer, product story or media-art
piece, with creative direction, sound and a publication-ready package composed
for the selected screens.

[Discuss a creative project](https://markoblogo.github.io/framewright/#contact).

### Test a tool in real production

For AI platforms and creative-tool developers. Explore a partnership built around
a concrete production question: use the product in a real project, retain the
results and limitations, and develop a review or demonstration from that work.
When a tool proves useful, it can also become part of a documented production
recipe rather than disappearing after one review.

Partner access is an opportunity to test, not a guarantee of a recommendation.
Testing scope, editorial independence and any compensation or affiliate
relationship should be agreed and disclosed. Audience results and sales are not
promised.

[Propose a tool partnership](https://markoblogo.github.io/framewright/#contact).

### Build on the process

For content teams and production studios: discuss a repeatable AI-assisted video
workflow, including tool selection, review steps and reusable recipes, scoped
to your production needs and available tools.

For fellow creators and agent-assisted developers: explore the open repository,
adapt the methods and contribute observations. Start with a
[production plan](docs/start-here.md#start-a-film), a
[worked correction](docs/productions/pantheon-chatgpt-orb.md#worked-example-v2-to-v3)
or the [task/style/tool search](skills/video-production-router/references/arsenal-search.md).

## See the work and what it taught us

| Work | Production lesson |
| --- | --- |
| [Same Ticker, Different Rights](https://youtu.be/NQX0F57Iy7g) | A glossy animated financial magazine combining sourced product material with distinct explanatory scenes. [Case and revisions](docs/productions/kriptok-same-ticker.md). |
| [I See You as Art](https://youtu.be/hb9oYAK37w4) | Media art made from supplied calligraphy footage and photographs, with music and separate screen compositions. [Sources and method](docs/productions/i-see-you-as-art-pl1.md). |
| [The Last Seed](https://youtu.be/ZQTORLBw9Zs) | An original Blender short refined through precise contact, mechanism, rain and sound corrections. [Worked case](docs/experiments/last-seed-recovery.md). |
| [Night Shift: After the Final](https://youtu.be/Gxn_w0Bvdlk) | A five-case PlayMCP game and two walkthroughs, refined through character, anatomy, interface and sound corrections. [Game, production case and limits](docs/productions/night-shift-after-the-final.md). |
| [Riemann Explorer](https://youtu.be/TBY5TcF4Vac) | A sourced walkthrough of a mathematical visualisation, built from owner-recorded material. [Fact checks and production case](docs/productions/riemann-explorer.md). |

Publication links are owner-reported; individual case records distinguish
technical checks, creative decisions, rights and publication. Views, revenue and
uploaded-file identity are not inferred from a link.

## How the studio learns

**Brief → moving pilot → review and refine → retain the useful recipe.**

![Framewright research cycle: brief, moving pilot, review and refinement, then a reusable recipe feeding the next project.](assets/fw-process-loop.gif)

Framewright explores combinations of generation, code animation, 3D, real footage,
screen capture, sound and local editing according to the scene. A tool is assessed
in context: what it contributes to the chosen style, how it works with the rest
of the pipeline and how precisely the result can be revised. The methods keep sources, selected
versions, corrections and known limits connected, so a later project can build on
actual work rather than repeat the same discovery.

Public methods and original repository materials are open; private project
assets, client material and confidential partner terms are not. External tools,
models and media retain their own licences. [Purpose and development path](docs/vision.md) ·
[Studio Notes](docs/editorial/README.md).

## Use Framewright yourself

Today the open project is an **experimental methods and agent-skills library**.
An agent uses selected tools in your environment; this repository is not a hosted
renderer or an automatic publishing service. Start with the task you need:

## Start / continue / correct

| Your task | Begin here | What you get |
| --- | --- | --- |
| **Start a film** | [Brief and production proposal](docs/start-here.md#start-a-film) | A concept, available sources/gaps, feasible route, constraints and a small pilot |
| **Continue a project** | [Recover the current state](docs/start-here.md#continue-a-project) | Exact selected version, accepted work, waits/blockers and the next permitted step |
| **Correct a fragment** | [Bounded change and A/B review](docs/start-here.md#correct-a-fragment) | A precise request, preserved original and corrected version, comparison in context |

[Purpose and development path](docs/vision.md) · [Current priorities](docs/next-cycle.md) · [Strategic roadmap and release gates](docs/roadmap.md)

## Try one production plan

From a local checkout with Python3, without additional Python packages:

```sh
python3 skills/video-production-router/scripts/plan.py examples/briefs/mixed-promo.json --format markdown
```

This prints a plan; it does not render, install, call a model or spend money.
[Example output](examples/plans/mixed-promo.md) · [Agent setup](docs/production-guide.md#use-the-agent-skill).

## Current release and tested scope

**[v0.12.0 — recover the selected delivery](https://github.com/markoblogo/framewright/releases/tag/v0.12.0)**
is an experimental prerelease. It binds an accepted master to its existing
publication package and reopens the exact video, cover, copy, review page and
recorded next step. Changed or explicitly rejected packages require review.
[Release notes and limits](docs/release-notes-0.12.0.md) ·
[Worked recovery case](docs/experiments/radar18-selected-delivery-recovery-2026-11-26.md).

| What you can build on | What has been checked |
| --- | --- |
| Continue selected work | Same-Mac isolated-process recovery of a real delivery; not a clean-machine or independent-operator transfer. |
| Exchange an edit | [VIDEO.md → OTIO](docs/experiments/video-md-otio-reopen-2026-11-26.md): three clip boundaries and library reopening, including relocated media. GUI editor import remains unqualified. |
| Carry a production recipe | [Capsule trial](docs/experiments/capsule-recipe-2026-11-26.md): a curated recipe reopens offline. It is not automatic semantic reconstruction or a generated remake. |
| Study an existing montage | [Known-edit analysis](docs/experiments/reverse-style-known-edit-2026-11-26.md): measured cuts compared with an authored edit; motion/OCR/ASR and listening limits remain explicit. |
| Link music and picture | [Music-cue A/B](docs/experiments/music-cue-ordinary-track-2026-11-26.md): two cuts adjusted around detected acoustic changes in one game recording; bounded evidence, not automatic music editing. |

Framewright combines an author-led production practice with an open methods
library. It is **not a self-service production app or automatic social publisher**.
Optional tools require their own access, installation and licence checks. Public
methods do not include private source media, client material or confidential terms.

Technical QA, creative/listening acceptance, rights and publication are separate
records. General tool qualification, labour savings and audience results are not
inferred from successful exports or publication links. The landing's
[catalogue](https://markoblogo.github.io/framewright/) reads source-linked film
and trial cases; variants count once, failed trials remain trials, and review
entries include untested candidates.

[Earlier releases](https://github.com/markoblogo/framewright/releases) ·
[Production cases](https://github.com/markoblogo/framewright/tree/main/docs/productions) · [Experiments](docs/experiments.md) ·
[Current priorities](docs/next-cycle.md) · [External-storage policy](docs/storage-policy.md).


## Test a method before production

Use the [experiment workbench](skills/video-production-router/references/trials-and-readiness.md)
for one bounded question with pinned inputs, an existing-method comparison and
separate output/review evidence. [Queue](docs/experiment-queue.md).
Free/open-source/macOS tools are preferred for this workspace; other platforms and
paid tools stay reserves. Existing subscriptions require actual access/terms checks.
[Selection policy](docs/production-guide.md#owner-preference-free-open-source-and-macos-first).

## Correct a film and reuse its design

[Revisions](skills/video-production-router/references/revisions.md) retain the
interval, defect, desired change and protected properties. [Templates](skills/video-production-router/references/templates.md)
separate design from copy/media/voice, but variants need their own render and review.
[Learn from owner corrections](docs/video-taste.md): apply relevant lessons before the next proposal and full-film review, with their scope, reasons and concrete checks.

[Worked correction: A Window to the Sky](docs/productions/pantheon-chatgpt-orb.md#worked-example-v2-to-v3) follows a real opening-only change through comparison, preservation checks and owner acceptance.

[Caption-time preflight](examples/production-reuse/README.md) flags overly short
English copy; it never silently retimes accepted films.

[Source-first editing](skills/video-production-router/references/editing.md) ·
[OTIO handoff/return](skills/video-production-router/references/otio-export.md) ·
[Saved-shot execution](skills/video-production-router/references/shots-and-passports.md) ·
[External-project handoff](docs/external-project-handoff.md) · [Production guide](docs/production-guide.md).

## Checks and contribution

```sh
python3 scripts/check.py
```

Offline checks and temporary package smoke; no model calls, installs or release.
Optional dependency skips are reported. [Checking policy](docs/checking-policy.md).
MIT for original repository materials; tools/models/media have separate terms.

[Book methods and cases](docs/book/README.md) · [English Studio Notes](docs/editorial/README.md).

## Ecosystem references

The executor draws on explicit task/checkpoint ideas also used by [SET](https://github.com/markoblogo/SET)
and behavior-first checks in [ABVX agent skills](https://github.com/markoblogo/abvx-agent-skills).
These are references, not runtime dependencies. [AGENTS.md Generator](https://github.com/markoblogo/AGENTS.md_generator)
is an optional instruction-practice reference. [ID](https://github.com/markoblogo/ID)
and [Pomerado](https://github.com/Pomerado/pomerado) remain conditional candidates.

## Collaborations

Completed product collaborations and practical evaluations:

- [Tulvo](https://tulvo.io/) — business workflow reviews and case studies.
- [Klap](https://klap.app/) — short-form repurposing trials and comparative review.
- [PlayMCP](https://playmcp.io/) — interactive game and video-production experiments.

New projects are added after the collaboration has been completed.
