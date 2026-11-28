# Yumina, OpenRouter media models and Video Explainer — 26 November 2026

Documentation and public-metadata review only. No skill installation, provider call,
account creation, purchases, model download, new film or executed trial. Existing
production/release waits and the Radar pause remain unchanged. Suggestions below
are studio assessments; vendor quality/performance claims are not our measurements.

## Decisions for this stack

| Candidate | Studio use | Admission and next step |
|---|---|---|
| Video Explainer | Continuous 3D explainers and editable motion, sound-event timing, frame-pinned review | First reserve; silent original12s comparison with our existing HyperFrames route. |
| Yumina OSS / hosted | Stateful interactive fiction, branching dialogue, conditional music, game-to-video work | Second reserve: local rule/checkpoint/export fixture first, no model calls; model-backed play is a separate access gate. |
| MAI-Image2.7 + Flash | Controlled reference edits, character/product continuity, cover and storyboard variants | One paired test, blocked on confirmed paid access and a bounded authorised budget. |
| Seed-TTS3.0 | Expressive short narration and dialogue | Blocked cloud comparison against a retained local narration baseline. |
| HY-World2.1Panorama | 360 backgrounds and same-position camera rotations | Add provider option to existing PANORAMA-PLATES-01; generation remains paid-gated. No duplicate family. |
| HeyGen Avatar6 | Brief presenter/character lines driven by supplied speech | Blocked paid lip-sync comparison; use only when a presenter serves the film. |

### Video Explainer: strongest immediate production fit

[Repository](https://github.com/petergyang/video-explainer), pinned
`be2f729161585be2482f6a5699e8cfb47da3daeb`. MIT code; bundled Inter OFL.
The documented motion, illustrated and continuous Three.js styles can use web
media, optional local/cloud voice and audio. Core requirements are Python3.10+,
Node22+ and FFmpeg. This host currently has Node22.14.0, Python3.14.5,
FFmpeg and pnpm; installed versions alone do not prove integration.

Source inspection of [setup.sh](https://github.com/petergyang/video-explainer/blob/be2f729161585be2482f6a5699e8cfb47da3daeb/skills/video-explainer/scripts/setup.sh)
shows pinned HyperFrames0.9.79, browser setup, cached Three.js0.149.0 and optional
Kokoro/Parakeet installation. Do not run the default installer globally: reuse
external runtimes where compatible and isolate any necessary version. No new
speech weights for the first test. The native render script prunes older drafts
and final rendering replaces earlier versions: run on a disposable original
fixture, never on an accepted Framewright production folder.

**VIDEO-EXPLAINER-01:** one12s silent landscape continuous action: a camera follows
an original document through three work stages, with no slide sequence. Compare
native export with the existing route; change one label while protecting timing
and camera. Check decoded duration, motion across boundaries, legibility at mobile
size and saved-project reopening. Reuse the standard Framewright review/delivery
page; upstream review UI is reference, not a second studio system. Keep our
separate YouTube/TikTok caption policy. Setup/storage failure is recorded, not
worked around through unapproved downloads.

### Yumina: useful interactive research, not a replacement video renderer

[Hosted service](https://yumina.io/) and [OSS repository](https://github.com/lovetimo0421/yumina-oss)
are two routes to the same project, not two experiments. Pinned source
`f44419c5f47325ee964c9f7a7d3310a0a640cf8d`, package0.0.85.0. Browser/Node-based
current architecture: TypeScript engine, React player/editor, Hono server and
embedded PGlite or Postgres. Godot describes its origins, not a current mandatory
runtime. Node22+ and pnpm fit the host; exact dependency footprint and build on
this Mac are unverified. A model can be remote or an existing Ollama endpoint;
a chat subscription does not establish API access. Hosted free/unlimited-model
availability is a vendor claim, not tested entitlement.

Typed state, declarative rules, branches/checkpoints and conditional audio are
relevant to a future interactive story following the PlayMCP experience. Avoid
porting Night Shift wholesale before a small deterministic check.

**YUMINA-STATE-01:** isolated local original lighthouse-room fixture, three choices,
one state threshold and one music cue; apply scripted responses, save/checkpoint,
rewind and export/reimport JSON with identical state. This first scope needs no
LLM inference; real multi-turn model consistency remains untested. An optional
later10–20turn model probe requires actual existing access and separate selection.
Code AGPL-3.0-only, documentation CC BY4.0, trademarks separate: retain as a separate
application, not vendored MIT router code. Inspect dependency install scripts and
keep the single-user service on127.0.0.1. Back up persistent data and the generated
secret before any selected portability test. No hosted world uploads in this intake.

### OpenRouter: compatible cloud delivery, unconfirmed paid access

All five requested model IDs are present in the anonymous
[Models API](https://openrouter.ai/api/v1/models?output_modalities=all), with provider
metadata also retained. The default list returns text-output models, so absence
there is not absence of these media models. API routes differ: images use
`/api/v1/images`, speech `/api/v1/audio/speech`, video `/api/v1/videos`.
A chat-completions-only integration is insufficient. Metadata discovery is not
successful generation, quota, output licensing or an enabled Framewright adapter.
No account keys, balances or entitlements were read or inferred.

- [MAI-Image2.7](https://openrouter.ai/microsoft/mai-image-2.7) and
  [Flash](https://openrouter.ai/microsoft/mai-image-2.7-flash): advertised up to five
  reference images; compare one owned character/product scene and one localised
  edit, same references and aspect. Score protected identity, unrequested changes,
  typography, repeatability, latency and actual billed cost. Flash is the vendor's
  faster/cheaper tier; no studio superiority finding. Public page input rates
  ($8/$2.50 per million) disagree with observed model/provider metadata
  ($5/$1.75); output-image rates agree at $34/$10 per million image tokens.
  Do not quote these as a fixed per-image cost. Resolve current units/quote before
  any run. **MAI-EDIT-01**, paired blocked family, not two queue items.
- [Seed-TTS3.0](https://openrouter.ai/bytedance-seed/seed-tts-3-0): tags, delivery/speed
  controls and MP3/PCM/WAV. Published $20/million input characters;600characters
  would be about$0.012 at that listed rate, not a spend authorisation. Chinese Han
  characters count twice. **SEED-TTS-01:** same20s English text containing an
  acronym, number and expressive turn versus a retained local take. Check natural
  pacing, pronunciation, no artificial acceleration, listen in the final mix.
  Requested language/voice support must be verified explicitly, not inferred from
  the large voice catalogue. A zero completion-token price is not free speech.
- [HY-World2.1Panorama](https://openrouter.ai/tencent/hy-world-2.1-panorama): one
  equirectangular panorama per text prompt;600character prompt cap. Vendor page
  quotes$1.60/million; metadata specifically prices image tokens. Confirm full
  request cost/resolution before use. It supplies an environment image, not a
  controllable3D world, geometry, translation/parallax or playable game. Extend
  **PANORAMA-PLATES-01** with an optional generated input: check seam/poles and
  render10s camera rotation with our existing3D tools. Owned-panorama preparation
  remains possible without this provider.
- [HeyGen Avatar6](https://openrouter.ai/heygen/heygen-avatar-6): supplied audio plus
  image/video reference drives expression and lip sync; motion prompt and
  expressiveness control,1080p/2K. Published from$0.10/s at1080p,$0.145/s at2K:
  a10s sample is approximately$1/$1.45 before any other charges. Metadata's zero
  prompt/completion rates do not make video free. **AVATAR6-LIPSYNC-01:** one owned
  fictional presenter and same8–10s local audio, compare restrained/expressive
  motion; inspect mouth/audio alignment, teeth, identity, unintended movement and
  end hold. Not evidence of general full-body animation or game-character control.

These cloud routes do not require local CUDA/ComfyUI or weight downloads. Their
actual blockers are selected provider access, authorised budget, compatible API
route and output/reference terms; unavailable paid access is not a failed quality
trial. Current hardware fit and asset rights stay separate. Recheck exact provider
terms before production; OpenRouter listings do not confer open-source model
licences. No replacement of working local narration/visual defaults is made.

## Registration and next action

Seven unique tool/model entries added to the existing review ledger and discovery
facets, with no tested applications or quality scores. Five new bounded families:
two reserve, three blocked. The existing panorama family receives an optional
provider branch. Nothing is active or executed. Suggested order is Video Explainer,
then the Yumina deterministic state fixture; paid comparisons only after access
and budget are actually selected. Retained public source snapshots and metadata
live in external `records/tool-intake-2026-11-26/`, not the MIT repository.
