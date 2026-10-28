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
[42 final exports](docs/experiments.md); production evidence, human acceptance and
audience results remain separate. Faster production and better retention are goals,
not established comparative results.

[MN7R production trial](docs/experiments/mn7r-promo.md): native Motion Canvas, locally authorised own-voice cloning and separate horizontal/portrait edits; technical checks passed, [overview publication link](https://youtu.be/kcFco2HbFCY) owner-reported; complete owner review and independent playback remain unverified. Spline authoring is partial with a native export gate; Canva Craft was not run.

For this workspace, prefer **free and open-source tools on macOS**. Paid and other-platform tools are reference reserves; a specific production may use a minimal paid trial only within its approved budget. Existing paid subscriptions and purchased apps are considered separately. [Selection policy](docs/production-guide.md#owner-preference-free-open-source-and-macos-first).

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

The [selected-route admission](skills/video-production-router/references/route-admission.md)
bridge pins one local action to an actual intake route/stage, its sources, requirements,
limits and expected file. Bound tasks recheck before dispatch and validate output
before retention. It currently supports inspection/review proxies, not a full recipe
or paid provider. [Original-fixture walkthrough](examples/admission/prepare_demo.py).


The optional [studio foundations](skills/video-production-router/references/studio-foundations.md)
add bounded host/owned-worker observations, an exact-decimal project cost ledger,
durable local-executor intents with explicit recovery/retry, and six offline
production-decision assertion contracts. [Internal controls](docs/experiments/studio-foundations.md)
keep unavailable metrics, unknown costs and incomplete traces explicit. These are
not automatic host-fit, paid-dispatch enforcement or model qualification.

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

The optional [safe OTIO return](skills/video-production-router/references/otio-export.md#safe-return-from-an-external-editor)
compares retained media/ranges and explicitly stages a returned edit as a new
candidate. It preserves the original and creates pending technical, listening and
creative checks; editor metadata cannot transfer approval or replace the final film.
The [MN7R review follow-up](docs/experiments/otio-mn7r-handoff.md#review-and-explicit-final-choice)
closed those checks separately and records the owner's explicit choice of the
42.13s B cut, preserving the accepted original and without a public upload.

## Continue after an input changes

Retain the intended revision in the existing project. Its dependent checks become
stale or reopen. At the next session, generate a short working brief:

```sh
python3 skills/video-production-router/scripts/project.py brief local/my-film/project.json
```

The brief shows current accepted work, file problems, recorded replacements,
unresolved checks and explicit waits. It proposes a next step without approving
or executing it. [Commands and a real project example](skills/video-production-router/references/project-insights.md#start-a-session-with-a-working-brief).

The optional [sequential executor](skills/video-production-router/references/projects.md#one-explicit-local-execution)
can explicitly run one local media inspection, create a contextual review clip,
or prepare a before/after comparison for a ready step. It retains the output and
stops for human review; it does not run arbitrary commands or publish work.

## Scope and further reading

[Source-first partial pilot](docs/experiments/source-first-playmcp.md) finds timed
candidates in supplied transcripts/observations, detects changed inputs and proposes
a recut from retained PlayMCP media. It is lexical retrieval, not automatic media understanding.
The [local-ASR follow-up](docs/experiments/source-asr-mn7r.md) feeds raw recognised
speech into that index; a measured false miss keeps source review necessary.
The [multi-source trial](docs/experiments/source-multicut-mn7r.md) links found passages
to an edit proposal and distinguishes adaptation from missing new material.
Its authorised internal draft also exercises portrait adaptation, existing clean
voice/music reuse and separate review clips extracted around the actual encoded joins.
The optional [OTIO handoff](docs/experiments/otio-mn7r-handoff.md) preserves that
1279-frame cut and separate audio tracks, with native-library round-trip and three
DJV picture checks. A [Kdenlive follow-up](docs/experiments/otio-mn7r-handoff.md#same-day-follow-up-actual-kdenlive-import-edit-and-render)
now passes native import, a15-frame edit, OTIO re-export and MP4 render; metadata/ID
loss and other-editor limits are retained. The returned B cut subsequently passed
its own technical check and owner listening/creative review; final choice is
recorded separately from intake and publication.

[Completion diagnosis](docs/experiments/completion-diagnosis.md) explains current
project blockers using tasks, exact review revisions, waits and variant requirements.
Run `project.py blockers PROJECT.json`; it reads the journal without executing work.

[Remotion licence classification](docs/research/remotion-conditional-licence-2026-10-28.md):
technical production evidence is retained; its custom licence requires user/use
eligibility checking before inclusion in a free route.

[Planned resource observations](docs/research/psutil-machine-observations-2026-10-28.md)
adds optional psutil measurements to existing host/readiness reports, with explicit
detected/checked/unknown distinctions. The adapter has not been implemented or tested.

[Planned project cost journal](docs/research/litellm-project-costs-2026-10-28.md)
separates approved budgets from observed/reconciled costs across production categories.
LiteLLM is an optional model-spend adapter candidate; enforcement is not implemented.

[Planned production-decision regression](docs/research/promptfoo-production-decisions-2026-10-28.md)
adds six source/resource/permission-sensitive cases to the existing router evaluation
approach; Promptfoo remains an untested adapter candidate.

[Planned state and approval loop](docs/research/langgraph-state-and-approvals-2026-10-28.md)
extends the current journal/executor with explicit branching and recovery tests.
LangGraph is a model reference and optional comparison candidate; no dependency added.

[Planned ComfyUI execution adapter](docs/research/comfyui-workflow-executor-2026-10-28.md)
admits individual versioned workflows with model/resource checks and bounded failure
handling. It remains unimplemented; ComfyUI is an optional task executor.

[Planned source-first story assembly](docs/research/storytoolkitai-source-first-2026-10-28.md)
extends the existing media catalogue and source-editing workflow with find/adapt/create
choices and evidence-backed fragment selection; StoryToolkitAI is an untested candidate.

[Editorial handoff and production diagnosis](docs/research/otio-kitsu-production-model-2026-10-28.md)
connects an OTIO draft-cut export with the existing scene/material journal and
version-bound reviews. A bounded OTIO exporter and read-only diagnosis are available; Kitsu/Zou
is an architectural reference and optional future team integration.

[Planned staging alternatives](docs/research/storyboarder-previsualization-2026-10-28.md)
extends the existing storyboard workflow with three rough composition/camera choices,
a revision-bound selection and an animatic; Storyboarder is a method reference.

The [producer-agency roadmap](docs/producer-agency-roadmap.md) describes profile-aware
planning, free/quota/paid alternatives and optional community evidence. An
[offline intake prototype](examples/intake/README.md) records local option preferences
and filters supplied examples. An optional small dated provider-terms catalogue can
annotate explicitly selected examples. Task-based discovery also returns scoped
catalogue candidates using a small cost classification. A route comparison covers
picture, optional language-aware narration and finishing, with scoped evidence and
unresolved costs/access/integration. It remains a planning prototype; total production
budgets and turnaround times require further evidence.

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

## Ecosystem references

The executor applies explicit task and checkpoint ideas also used by [SET](https://github.com/markoblogo/SET)
and the behavior-first testing workflow in [ABVX agent skills](https://github.com/markoblogo/abvx-agent-skills).
These are references, not runtime dependencies. [AGENTS.md Generator](https://github.com/markoblogo/AGENTS.md_generator)
is an optional source of repository-instruction practices; [ID](https://github.com/markoblogo/ID)
and [Pomerado](https://github.com/Pomerado/pomerado) remain conditional candidates, not integrated components.
