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

For labelled workflows, the scoped `manimgx` diagram-explainer adapter is an option;
its qualified export includes FFmpeg timing normalisation. Explicit narration can
use `preferred_voice` with a known voice-tool ID. Missing language support remains
blocked; do not silently swap an explicitly requested voice runtime. MLX-Audio's
current tested profile is Kokoro English only,not the whole upstream model range.

## Scoped route choices

Prefer Brag full for a short software launch; prefer the local narrated montage
recipe for existing book imagery with speech. Brag itself also supports voice:
our silent Brag tests do not establish a product limitation. Anatomy is a visual
prototype option, not a validated physics or finished sound workflow here. Do not
choose it just because a video contains an object. Historical reconstruction and
new AI-video services require bounded tests, not an invented capability claim.

For camera travel and focus around an existing React interface, consider the
tested `live-react-scene` Flute recipe. An explicit Flute request overrides the
default renderer choice; load its installed guide. Its browser-host success does
not prove full Electron or arbitrary React support. Keep the ordinary app and
production bundle outside the demonstration. Scope capture-style overrides to the
development host so genuine components retain their ordinary app styling.

For authored React motion graphics with a controllable frame timeline, native
audio and stills, consider `authored-react-film` (Remotion). Distinguish it from
camera treatment of existing app UI. Keep its own licence and observed browser
workaround visible; a successful pilot does not prove every rendering mode. If a
native still is a requested deliverable, plan its own inspection alongside the
encoded picture/audio rather than substituting an extracted or pre-existing frame.

For a miniature world with purposeful object action and camera travel, consider
`staged-3d-scene`: an authored Three.js scene inside Hyperframes, not Anatomy.
Use `three-scene` with `staged-3d`, `object-3d`, `object-motion` or `camera-travel`
requirements, or miniature/low-poly style. Do not infer it from a book cover alone.
The tested 20s 1080p30 pilot has grain loading, truck delivery, quote convergence
and a genuine-cover book reveal. Keep geometry/staging work explicit. Read its
[recipe](recipes.md#staged-3d-scene); other formats, physics, new assets
and cross-tool seams need their own checks. Kokoro and FFmpeg are separate layers.

For a labelled workflow/process diagram, consider `diagram-explainer` (ManimGX
plus the retained FFmpeg timing adapter). Its20s 2D English pilot does not qualify
native timestamp portability,3D/math plots or Ukrainian. Inspect the native
storyboard and preserve held-frame timing before CFR assembly. `mlx-audio` is a
separate English Kokoro voice option; respect an explicit `preferred_voice` and
read the [recipe](recipes.md#diagram-explainer) before another setup.

When the chosen tool misses a requested deliverable, compose the smallest useful
chain rather than drop the deliverable or replace the whole workflow. Read
[tool chains](tool-chains.md) for handoff checks and tested combinations.
A successful component does not prove the combined chain; preserve the original
export, check the final file and record each tool's contribution and limitations.

For Ukrainian narration,prefer `supertonic3` within its scoped M1/F1 evidence.
Owner found both usable and much better than Tetiana;F1 has a slight preference.
Residual pauses/stress errors remain;do not claim perfect Ukrainian or long-form
quality. Model terms require explicit synthetic-content disclosure.
Retain Piper/Tetiana as a low-quality explicit fallback with a visible warning;
`default_narration_eligible:false` prevents silent automatic substitution. Preserve
explicit provider choices and inspect new scripts/final integration. Other voices,
languages,singing and cloning need separate review. Paper-cut/LCD picture treatment
is independent of the voice engine. See [recipes](recipes.md).
