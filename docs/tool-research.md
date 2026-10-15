# Tool review and test inventory

Reviewed2026-10-15. Initial upstream README/code metadata was inspected without installations.
Later bounded runtime trials are linked below; no blanket benchmark is claimed. [Decision ledger](../skills/video-production-router/references/review-ledger.json)
is the lookup point for previous tests, partial results, rights and revisit conditions.
A documented feature, code licence and model/media licence are separate claims.

| Tool / official source | Local state and retained limits | Bounded next test / stop |
| --- | --- | --- |
| [Hyperframes](https://github.com/heygen-com/hyperframes) | **supported_scoped**: HTML rendering used in delivered pilots; only recorded formats/effects qualified. | Existing tool profile and experiment records; no blanket retest. |
| [FFmpeg](https://github.com/FFmpeg/FFmpeg) | **supported_scoped**: Assembly, encoded audio mixing/QA and frame extraction used; permissions and build licences differ from media rights. | Test only a new codec/filter/handoff requirement. |
| [auto-editor](https://github.com/WyattBlue/auto-editor) | **candidate**: Automatic timeline cuts by audio loudness/motion; not semantic judgement of which words can be removed. | Authorised60–90s spoken sample; label pauses first, protect phrase edges, check edit list and sync. |
| [OpenScreen](https://github.com/getopenscreen/openscreen) | **supported_scoped**: [AMI Books42s tour](../experiments/2026-10-15/ami-books-openscreen.md),CLI capture/pack,manual zoom/callouts,native1080p60 with FFmpeg30fps/voice finishing. Miniature/black-window failures retained;automatic cursor/MCP/AI unqualified. | Retest only changed capture-control need,released MCP or explicit automatic-cursor trial;owner review pending. |
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | **candidate**: Acquisition utility, not a renderer/editor or licence to reuse downloaded media. | Only an authorised owner clip if no retained local master exists; test segment timing/metadata; do not import browser cookies implicitly. |
| [Puppeteer](https://github.com/puppeteer/puppeteer) | **component_used**: Browser/seek harness used for Spot-Market; this is not a separate continuous recorder qualification. | Reuse existing browser harness; test only new seek/readiness/capture requirements. |
| [ManimGX](https://github.com/academa-labs/manimgx) | **supported_scoped**: [MN7R2D workflow pilot](../experiments/2026-10-15/mn7r-manim-mlx.md),FFmpeg timing normalization required;native mux warnings retained | Reuse runtime;3D/math plots,other formats and native still remain untested |
| [Anatomy](https://github.com/wheresryan22/anatomy) | **prototype**: Desk/isometric adaptation is a visual prototype; original combined sound QA failed. New Three.js success does not repair that chain. | No repeat of the same prototype. Revisit only a specific changed component or new illustration requirement. |
| [GSAP](https://github.com/greensock/GSAP) | **component_used**: Paused absolute-time timelines used inside Hyperframes; not every plugin/effect tested. | Use existing installed runtime; new plugins, text morphs or capture timing need their own scoped checks. |
| [Three.js](https://github.com/mrdoob/three.js) | **supported_scoped**: Authored Spot-Market miniature/action/camera via three-scene profile; no calibrated physics or arbitrary model reconstruction. | Reuse tested adapter; ASCII treatment, new geometry/import or formats are new scoped experiments. |
| [opus-sound-layer](https://github.com/Bodila51/opus-sound-layer) | **partial**: Sound-layer methods/mix QA are retained; a library-level CC0 statement does not clear every chosen recording. Anatomy combined failure remains retained. | Inspect each sample provenance; test only missing sound/mix capability, not the whole pipeline again. |
| [librosa](https://github.com/librosa/librosa) | **supported_scoped**: Burgers:3/3 authored target onsets; no independent listening labels, general beat/downbeat or song alignment qualification. | New genuine music reference with manual labels, not the same authored-marker recovery. |
| [MLX-Audio](https://github.com/Blaizzy/mlx-audio) | **supported_scoped**: [Kokoro English TTS pilot](../experiments/2026-10-15/mn7r-manim-mlx.md);not Ukrainian/diarization/cloning. Setup snapshot exceeded planned budget | Reuse environment/model;new exact model/language/task needs rights/resources and listening gates |
| [pyannote-audio](https://github.com/pyannote/pyannote-audio) | **candidate**: Speaker diarization/embeddings. Anonymous speaker clusters are not verified real-person identity. | Two-speaker20–30s sample with manual turns/overlap; inspect model conditions, token/telemetry and local-vs-premium route first. |
| [mlx-whisper](https://github.com/ml-explore/mlx-examples) | **candidate**: MLX Whisper speech transcription; word timing is an estimate, not proven lyric alignment. Exact path is whisper/README.md. | Same10–15s EN narration and known transcript as Parakeet/WhisperX; errors, timing and real resource use. Singing separately. |
| [parakeet-mlx](https://github.com/senstella/parakeet-mlx) | **candidate**: Apple Silicon implementation of Parakeet ASR, documented word-level caption outputs; speed/accuracy unmeasured here. | Share the transcription fixture/model budget; record exact language/model, omitted words, timestamps and output SRT. |
| [claude-video / Watch](https://github.com/bradautomates/claude-video) | **candidate**: Documented Agent Skills/Codex path, sampled frames plus transcript; this is not proof of continuous video/audio understanding. | Existing local10–15s owned MP4; inspect planned paths/dependencies/cloud fallback first. Compare known visual events and transcript, no automatic installs/uploads. |
| [Prompt Motion](https://prompt-motion.com/) | **reference_only**: Public catalogue, prompts/skills and customizer; creator-owned material. Improved prompt may be Untested while original has a video. | Brief → metadata filters → shortlist → finalist → original bounded prompt adaptation → agreed render/QA. Current trial stops at prompt. |

## Source pinning and rights

The ledger retains immutable revisions for newly inspected GitHub candidates;
MLX Whisper was read at `whisper/README.md`. Existing proven components retain
their tested revisions in experiment/profile evidence; reviewing upstream does not
upgrade those scopes. Candidate code licence labels are preliminary repository
metadata/README checks, not clearance for models, fonts, bundles or media.

Important corrections: MLX-Audio does document diarization through specific models;
it is broader than that task. Pyannote speaker clusters are not identity proof.
librosa onset/beat candidates are not a verified downbeat grid. Watch can expose
frames/transcripts to Codex; sampled evidence does not replace full decode, listening
or motion checks. Local inputs should stay local unless the chosen cloud path is
separately authorised. Do not let upstream auto-install or fallback instructions
override the current task boundaries.

## Retain negative and blocked decisions

Record the attempted version, task/inputs, expected output, observed result and
evidence; record rights/account/hardware blocks separately. A functional failure
does not mean licence rejection; unavailable rights do not mean broken software.
Use `rejected` only with an actual reason; `candidate` means not executed. A new
trial must name what changed and which finding it addresses. Keep old failures
and superseding evidence together rather than erasing either.

The ledger also backfills prior router profiles and queued studies. For exact
feature states see [the matrix](../skills/video-production-router/references/tool-matrix.md),
for scheduling priorities see [the queue](experiment-queue.md).

## Productive paired experiments

The owner prioritises useful ABVX book/service promos: one new picture tool plus
one new audio tool where justified, otherwise a proven counterpart. Preserve the
brief/assets/script/format and stems so each component can be assessed separately.
Music-video and animation-series research follows those promos. See the phase/pair
[queue](experiment-queue.md), including the proposed next-release checkpoint after
one agreed production experiment and its documentation. No release now.

## Ukrainian voice / paper-route follow-up

[Piper/Tetiana](../experiments/2026-10-15/agro-uk-paper-piper.md) is the new exact
Ukrainian TTS candidate,paired with reused Remotion and original paper-cut motion.
EngineGPL3/modelcardApache2.0 are separate;human pronunciation is not inferred
from a valid WAV. MMS Ukrainian remains rights-blocked for this promotional brief
under its noncommercial model terms,not technically failed. No repeated unchanged
Kokoro language trial. Creative technique and renderer novelty are recorded
separately;an SVG animation is not a physical simulation.

## Supertonic3 Ukrainian audio-first gate

[Two short preset probes](../experiments/2026-10-15/spot-market-uk-voice-probe.md) use a different model/engine from Piper,with local synthesis and pinned files. Owner subsequently accepted both as usable and much better than Tetiana,with residual pauses/stress errors;F1 is a slight preference and the scoped UK default. Full-film integration remains a separate check. OmniVoice code/weight licensing differs and was retained as rights-blocked for the intended promo,not technically failed.

[MoviePy2.2.1](https://github.com/Zulko/moviepy) now has a
[scoped compilation trial](../experiments/2026-10-15/agro-series-compilation.md):
subclips,multi-panel scenes,picture crossfades,independent headings,native RGB PNG
and timed audio mix. MIT code;fonts/media/weights retain separate rights. Editly
remains deferred,not failed. This manual recipe is not an automatic planner provider.
