# Select by block and layer

Framewright helps an AI agent choose and execute a suitable video pipeline using
documented experiments. It is not a new video engine. The agent directs existing
tools; the offline planner only makes an inspectable shortlist.

## Turn the request into a brief

Extract purpose, audience, language, duration, aspect ratio, fps, available authorised
assets, style references, requested effects, narration, deliverables and cost/account
constraints. Preserve explicit tools. For comparison-only requests, recommend and stop:
no installation, asset preparation, model call, render or publication.

Split the film into blocks, then picture, text, voice, music/SFX and finishing layers.
A global style is a continuity target, not a demand to use one engine everywhere.
Match actual inputs before style: Flute needs live React components; Remotion authors
new React compositions; Anatomy makes object illustrations. An object appearing in
a book cover is not by itself a reason to choose Anatomy or an authored 3D scene.
For a process explained by object action/camera, `three-scene` offers the scoped
`staged-3d-scene` route. Its feature/style activation prevents generic export
requests from silently acquiring3D work. It needs authored geometry/staging.

## Evidence and capabilities

Read [tool-matrix.md](tool-matrix.md) for the concise inventory; load matching profiles
in [tools.json](tools.json) and the selected [recipe](recipes.md) on demand.
`tested` means only the stated local scope. `documented` needs installed-version
verification and a small feature trial; `failed` remains a known failure even if a
companion supplies the output. Missing features are unknown. None of these states
proves a new combination. Styles describe affordances or observed direction, not
fixed engine boundaries, measured quality rankings or exhaustive API coverage.

The planner in `scripts/plan.py` takes JSON after the agent decomposes natural
language. It does not interpret prose, install, render or call an AI model. Set
`minimum_evidence` to `tested` to reject capabilities without local evidence.
`allow_paid` only affects the shortlist; it grants no purchase/account authority.
If a preferred tool cannot consume the input, preserve that choice and report a
blocked plan; propose an adapter explicitly instead of silently replacing it.

For the picture shortlist, compare complete feasible chains: coverage of requested
features, number supported by tested evidence, then chain size, primary ownership of requested effects, style and task
default. Preserve an explicit primary. A direct documented feature must not displace
a tested companion route merely because it is native. Finishers need real inputs;
their own export capability does not prove those inputs exist.

For music, singing, an existing soundtrack or a provider's video export, read
[music-workflows.md](music-workflows.md). Select the timeline owner and inspect the
independent music plan; picture coverage alone does not clear music or its rights.

## Common assembly contract

For every block retain source/tool version, feature evidence, inputs/rights, start
frame, duration and any transition overlap. Use one width/height, fps/timebase,
colour space and intended audio sample rate. Unknown durations stay unknown; measure
speech before locking cuts. Overlaps subtract from the total duration.

Declare each handoff: image/SVG versus encoded clip, codec/container, alpha versus
flattened background, colour conversion and transition handles. Keep voice/music/SFX
stems separate until one master mix. SVG is an input asset, not an MP4. Flute's silent
clip can receive an FFmpeg audio mux; its failed portable snapshot can be replaced by
an extracted encoded frame, with that distinction retained.

Choose one assembly owner. The sample planner proposes FFmpeg; a Remotion or
Hyperframes master is possible when its installed guide and imports support the
actual inputs. Stream-copy only compatible streams. Normalising fps, colour or
transitions normally needs re-encoding. Test seams, sync, text legibility, crop,
loudness/peaks and encoded thumbnail dimensions. Preserve native and final hashes.
Use shared palette, typography, grain, pacing and transitions to join stylistically
different tools. Hyperframes capture-side VFX and page shader transitions have a
documented compatibility warning; do not combine them without a feature trial.
Keep original effect settings and exports. Separate passes can be a reversible
fallback; any fallback that removes/replaces a requested effect or changes a
required output must remain a proposal pending the owner's explicit acceptance.
Do not present a scope-changing fallback as an automatic next action.

## Example: one film, several tools

A brand introduction can use Remotion typography; an interface block can use Flute
camera/focus; an object block can provide Anatomy SVG to Hyperframes; a book montage
can add Kokoro narration; FFmpeg can finish the common timeline. This is a proposed
mixed chain, not a ninth tested export. See the repository's mixed-promo JSON example.

## Stop and deliver

Show per-block tools, reasons, evidence/limits, unresolved requirements, timeline and
assembly owner before execution. Follow selected renderer guides; Hyperframes is
required only for its own routes. Do not launch unrelated tools. After authorised
execution, report technical QA, human listening, owner acceptance, publication and
audience performance separately. A successful render does not qualify agent routing.
