# Storyboarder and low-cost staging alternatives — 28 October 2026

Status: official documentation/source layout reviewed; interaction/method reference
and queued internal trial. No install, upstream build, scene generation or import
test. The proposed Framewright feature is not implemented by this research.

## Confirmed sources and limits

- [Repository](https://github.com/wonderunit/storyboarder): boards/animatics and
  Fountain screenplay workflow.
- [Wonder Unit overview](https://wonderunit.com/storyboarder/): board dialogue/action,
  timing/shot type, and description/parameter-driven Shot Generator references.
- [Shot Generator source directory](https://github.com/wonderunit/storyboarder/tree/master/src/js/shot-generator):
  camera and scene components; inspected as a reference, not vendored.
- [Current master package metadata](https://github.com/wonderunit/storyboarder/blob/master/package.json):
  source version 3.0.0 and Mac arm64/x64 build commands. The marketing page still
  displays 1.0.0. Neither proves a usable released Apple Silicon binary or reliable
  local build. Verify an actual release, signature, footprint and runtime separately.

The README links the author's free/open-source discussion, while the installer
references a [custom EULA](https://github.com/wonderunit/storyboarder/blob/master/build/license_en.txt),
including software redistribution limits and clauses about shared user settings/poses.
This does not establish a standard permissive licence for embedding. Treat code, included
models and textures as unverified for embedding/redistribution until exact terms
are inspected. Studying the workflow does not require copying that implementation.
The described Shot Generator is not evidence of an available generative-video API,
automatic final animation, physics, or natural-language control in Framewright.

## Fit to the existing project

Extend the [existing storyboard contract](../../skills/video-production-router/references/storyboard.md),
which already records purpose, time, sources, action/camera, copy and QA gaps.
Use [scene/material/variant entities](../../skills/video-production-router/references/production.md)
and the [saved Blender shot probe](../experiments/blender-shot-replay.md) where useful.
Keep a recurring hero/set version pinned through the existing passport mechanism.
Avoid a separate screenplay database or a mandatory Storyboarder dependency.

The reusable principle is to make storytelling choices visible while changes are
cheap. Rough original geometry, simple drawings or supplied cleared references can
be sufficient. Show staging, not a promised finished look. A simple recut or already
approved supplied sequence does not need a new mandatory storyboard gate.

## PREVIS-01 — three staging choices for one scene

Proposed request: “Show three ways to stage this scene before final production.”
Each variant links the same scene ID/version and intended story beat to a concrete
camera/composition specification:

| Field group | Proposed fields |
| --- | --- |
| Narrative | Purpose, information revealed, dialogue/text and intended duration |
| Composition | Shot size, subject positions/scale, foreground/background, focal subject |
| Camera | Position/orientation, projection or lens/FOV with units, optional camera path |
| Movement | Subject action/path, screen direction, eyeline and continuity axis |
| Scene | Hero/set/prop version IDs, light intent, unresolved assets |
| Review | Variant ID/revision, preview pin, selected/deferred/rejected decision and reason |

Use existing saved camera/action/light controls when their scope fits. Keep the
story beat, characters, source versions and duration target fixed; vary composition,
camera and reveal order deliberately. Suggested alternatives: an establishing wide,
a closer character/reaction view, and a prop/reveal-led view. They are choices, not
three mandatory final-film shots. Display differences, assumptions and limitations.

### Bounded test and acceptance

1. Choose one original/cleared scene, preferably a parcel/reveal interaction relevant
   to the retained robot-film lessons. No new final film is started.
2. Produce three low-resolution labelled boards from saved settings, sequentially
   on the Mac. Limit initial output to stills; no paid generation or new asset models.
3. Check framing, screen direction, prop visibility and whether the intended beat
   is understandable. Retain each preview, settings and exact asset/scene revisions.
4. Ask for a staging choice; record it as a decision scoped to the exact variant.
   A choice does not approve final picture, spending or publication. Changed inputs
   must make the old choice stale rather than silently carrying approval forward.
5. Only after selection and within the authorised test scope, make a short rough
   animatic with real or explicitly temporary voice timing; test one parameter edit
   and replay. Report unresolved action, contact, speech and asset details.

Pass: materially different intelligible alternatives, reproducible settings, one
retained choice and a rough timed preview without misrepresenting production quality.
Measure operator effort and whether the test catches a staging/causality issue before
expensive production. An exported board alone is not creative acceptance.

## Relation to OTIO and production diagnosis

PREVIS-01 supplies approved staging to scene tasks; PROD-01 can expose an unselected
or stale variant as a blocker only when that project requires staging approval.
The later concrete cut can feed [OTIO-01](otio-kitsu-production-model-2026-10-28.md).
Keep planned durations separate from measured media ranges; OTIO export must not
invent final clips from rough boards. Storyboarder runtime integration remains a
separate optional candidate, subject to compatibility/licence checks.
