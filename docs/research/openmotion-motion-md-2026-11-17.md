# OpenMotion / Motion.md: adopt the useful contract

Reviewed17November2026 for M1–M4/RV01: less repeated explanation on continuation and correction.
Owner authorised implementation, local bounded trials, PR/checks/review/merge; release decision remains separate.
Pinned upstream: [`fcbaa2b0296167b0f14f47aa6c414f5bdd41316f`](https://github.com/nexu-io/openmotion/tree/fcbaa2b0296167b0f14f47aa6c414f5bdd41316f).
[Product page](https://open-design.ai/motion/). Sources were read, not merely the promotional page.

## Decisions implemented here

1. A readable [motion specification](../../skills/video-production-router/references/motion-spec.md) links existing intent, design, state, sound, editable implementation and review. It supplements the producer brief and project journal; it is neither an animation parser nor another status store.
2. The existing router, producer brief and reuse templates now lead to that entry. A [filled structural example](../../examples/production-reuse/MOTION.md) is explicitly unexecuted; it does not inherit a trial's acceptance.
3. Retain directorial distinctions: an important change with a viewing payoff, meaningful holds, cross-scene object state, a representative risk pilot and a full-duration moving draft. Avoid imposing a universal palette, effect quota or shot count.
4. Separate functional checks from perception: attachment is not table support; correct geometry is not readable annotations; seek equivalence is not interesting acting. Real recent corrections remain the source of these constraints.
5. Test the upstream native editing/export route externally, with local assets and no paid models. Keep Framewright's journal canonical. See the [bounded trial](../experiments/openmotion-reuse-2026-11-17.md).

## What the source actually provides

| Source at pinned revision | Useful scope / limit |
| --- | --- |
| [Motion.md](https://github.com/nexu-io/openmotion/blob/fcbaa2b0296167b0f14f47aa6c414f5bdd41316f/docs/motion-md.md) | Agent-readable creative context; execution still requires real source, assets and a compatible runtime. |
| [Motion Package draft0.2](https://github.com/nexu-io/openmotion/blob/fcbaa2b0296167b0f14f47aa6c414f5bdd41316f/docs/motion-package-spec.md) and package module | Inventory, portable paths, declared dependency shape and hashes. Does not validate creative semantics, Markdown references, rights, host installation or rendered quality. Checker/packer use Node built-ins and do not execute package scripts. |
| [Director](https://github.com/nexu-io/openmotion/blob/fcbaa2b0296167b0f14f47aa6c414f5bdd41316f/skills/openmotion-director/SKILL.md) and production review | Intent, state, action, sound and exact candidate review are reusable concepts. These are reviewed references, not global agent instructions. |
| Native production / verification / HyperFrames guides | Editable HTML/GSAP source shared with Studio, version/revision guards and snapshot-pinned exports. Observed installation uses HyperFrames0.9.7 and GSAP3.15.0. Native checks do not replace viewing/listening. |
| Remix profiles / retained evidence | Source-backed material substitutions. The examples' own silent12fps excerpt evidence does not establish native Studio export acceptance or arbitrary video reconstruction. |

The site's “99%” fidelity wording has no retained reproducible support in this review; upstream architecture documentation also distinguishes that aspiration from demonstrated reconstruction. No such score is adopted.

## Boundaries

No upstream source or skill is copied into this repository. The external pinned checkout retains Apache-2.0; fonts/media keep their individual notices. No linked document can authorise account grants, paid generation or unreviewed installation. No global MCP/plugin registration or provider credentials were added.

OpenMotion is a companion authoring environment, not a replacement project database or a newly qualified Framewright planner provider. A simple local motion-graphics trial cannot solve Quixote's anatomy, character stability or acting. Quixote remains owner-paused. Installing a source-backed runtime does not qualify every advertised workflow or establish transferable operation on another machine.
