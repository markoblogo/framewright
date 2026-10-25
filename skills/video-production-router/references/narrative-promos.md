# Short narrative promos for books and projects

Use for a short promotional film whose interest comes from a visible situation,
a change and a consequence. A book may supply a fictional world; a project may
supply a real action. This module prepares the story and production handoff; the
existing router selects tools and the existing project records assets and checks.
Skip it for a factual walkthrough, a supplied approved shot plan, a simple recut
or a request for publication copy alone.

## Choose the story promise

Use the actual brief: subject, viewers, language, duration/canvas, authorised
sources, intended feeling, desired next action and tool/cost constraints. Reuse
known choices; ask only about missing information that changes the treatment.
Do not assume mobile games, a demographic, distressed characters, silent audio,
a cliffhanger, portrait format or a particular generation model.

Separate **source-backed facts**, **fiction from the book** and **new symbolic
staging**. Name the source for a product claim or quotation. A metaphor is not a
working feature, real gameplay, a quote from the book or a customer result.
For a book, do not invent plot events presented as canonical; a new symbolic
scene should be labelled as an interpretation. For a project, demonstrate real
functionality with actual footage when the promise depends on it.

Propose one coherent treatment unless variants were requested. Establish what
makes the first moments interesting, what changes, why the next action follows,
and what the viewer is left wanting. A complete payoff can serve the brief as
well as an open ending. Do not promise virality or retention from story structure.

## Convert the premise into shootable beats

Use the shared [storyboard contract](storyboard.md), keeping the shot table compact:

| Field | Record |
| --- | --- |
| Shot/time | One viewpoint or coherent camera action; exact start/end |
| Visible event | Subject, action, reaction and resulting scene state |
| Story/source | Why this shot follows; fact/fiction/symbolic status and material IDs |
| Framing/movement | Shot size, gaze/screen direction, motivated camera movement |
| Sound boundary | Ambience, effect, music change or narration tied to a named event/time |
| Inputs/gaps | References, picture method, missing assets and output-specific checks |

If seeing a reaction and its cause needs different viewpoints, specify the cut or
continuous reveal. Avoid packing several invisible events into one literary beat.
Choose readable timing for the action; do not impose a shot count or three-second
cadence. Include transition overlaps when calculating the master duration.

Keep a compact continuity note: actor identity, prop IDs, spatial layout, light,
direction of travel, gaze target and each shot's start/end state. The object that
causes a reaction must be the same object shown in the consequence. A running
cycle requires visible world travel if the story promises reaching a destination;
state camera tracking separately so it cannot accidentally cancel that motion.

Tie sound to the same event clock as picture. For an impact-driven change, record
one timestamp for impact, light response and music transition, with any deliberate
delay explicit. Music, silence, dialogue and voice-over follow the brief rather
than a global default. A sound prompt is not proof of synchronized encoded audio.

## Hand off to the selected picture method

Distinguish reference roles: strict first-frame composition, character identity,
style/environment inspiration and cleared product/book artwork. Do not assume a
style reference must remain an identical first frame. Record permitted changes.

For generated clips, prepare only the prompts needed by the chosen model and
clip limits. State subject/action, camera, start/end state and reference mapping;
use current model-specific syntax when known. Split into clips when required,
with continuity anchors and actual handles/overlaps planned. There is no universal
3000-character limit or guaranteed cross-model prompt. For authored engine scenes,
use timed actions, root/camera paths and cues instead of pretending a video prompt
is executable scene code. Keep actual cover/title typography as a separate layer
when generation would distort it.

A proposed treatment needs review when the user requested it or consequential
creative choices remain unresolved. Existing approval and production authority
carry forward; do not add repeated approvals for routine steps already authorised.
Planning alone never starts generation, new spending or public upload.

## Save, check and deliver

Map the plan into the existing [composition](production.md): materials with
origin/rights; scenes with tell/show, narration and missing inputs; variants with
independent edits, music and local delivery mappings. Put additional continuity
and cue detail in the shot plan, without adding unsupported JSON fields.
The [16s book-promo example](../../../examples/production/narrative-book-promo.json)
is plan-only: all media/rights are unresolved. It is not a film or a verified book.

Follow the [QA/handoff contract](handoff.md). Inspect action readability, causal
continuity, identity/prop consistency, encoded audio/cue timing and factual copy
against sources. Keep technical checks, owner creative acceptance and publication
separate. Prepare only the requested output kit; a Telegram-only clip need not
acquire a YouTube pack. For this owner's YouTube covers, use the recorded
[text-cover preference](../../../docs/production-guide.md#owner-workspace-packaging-preference).
Record rejected takes and changes in the project journal; do not count a revision
as a new final export or label this module production-tested before an actual run.

## Provenance and qualification

Original Framewright integration, informed by the owner-supplied mobile-ads ZIP
reviewed on2026-10-25 (SHA-256
cfc2e7453198ef00e5156922fcb6d88250d790d9aec2a0f12bcde9e0fae02d43).
That archive contains instructions/references/icon, no executable scripts or
licence grant. Its files, icon and model-specific assumptions are not vendored or
installed. This module uses an original contract and existing Framewright systems.
Status: documented/planning-only; no new render, model trial, ad-performance test
or audience validation. Prior films are context, not tests of this new module.

Offline example smoke: create/compose/board yields four scenes and16s; missing
media/rights remain blockers and an unfinished kit is refused. This verifies the
existing bookkeeping seam, not the quality of a generated story or rendered film.
