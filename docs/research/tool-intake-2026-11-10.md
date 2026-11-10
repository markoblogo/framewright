# Tool intake —10November2026

Research only, M4/R05/R06/R07. **22 supplied link occurrences ->14 families.**
All useful families are retained, including those requiring a different machine.
No binary/model download, installation, authentication, execution, generation or
paid call. No new tested profile, production, trial count or release.

## Catalogue across devices; admit on the actual host

Owner clarification10November: a stronger machine is planned within months and
other users may have different devices. Current Mac incompatibility is a routing
constraint, not grounds to discard a useful tool. Keep the capability, supported
OS/backend, reported memory/VRAM, rights, unknowns and a bounded next test.
Re-evaluate when the host/backend/terms change; do not infer that more Apple RAM
provides CUDA or that a GPU purchase clears licensing. No purchase recommendation
or universal hardware minimum is established here.

Observed host: Apple Silicon arm64,16GiB unified RAM, macOS27.0.1. Existing
Blender/FFmpeg/local authoring routes are baselines, not evidence that a new engine
works. Source docs/benchmarks are vendor-reported; none is our runtime measurement.

The existing [review ledger](../../skills/video-production-router/references/review-ledger.json)
now stores `stack_admission` on these14 records: current status, alternative
stack targets, requirements/unknowns and a recheck trigger. This is catalogue
metadata, not a new executing selector or device detector. Existing history is
not retroactively qualified or rewritten. See the permanent
[selection rule](../../skills/video-production-router/references/selection.md).

## Deduplication

- Normalising bare `opentoonz.github.io` collapses its repeated website URL.
  OpenToonz was already a reserve in [3November manga tooling](manga-film-tooling-2026-11-03.md);
  update the same role rather than schedule another identical test.
- Tesseract engine is new scope. The historical MIT Tesseract-Converter round trip
  does not qualify the engine or its custom terms. Tesseract OCR is unrelated.
- Viggle Image Swap is a Qwen still-image LoRA, distinct from the earlier
  [Viggle Remake video review](tool-intake-2026-11-06.md).
- Group Matrix source/model/site/paper; Sophon source/model; and Freefield
  gateway/wrapper. Different H3 derivatives retain separate weights/terms records.

## Findings and stack routes

| Family / supplied sources | Production value | Current and alternative stack; decision |
| --- | --- | --- |
| [Tesseract engine](https://github.com/mirage-hq/Tesseract), [site](https://mirage.app/tesseract) | Editable agent-directed motion graphics, text, masks, media and3D; potential smaller corrections without a whole-film rebuild |0.6.0 arm64 CLI distribution exists. **Conditional candidate:** use/entity and substitute-product/integration terms first; then TESSERACT-RUNTIME-01. Not MIT or already locally tested. |
| [Image2Sculpt](https://github.com/gokayfem/image-to-sculpt) | Owned illustration/prop -> fitted volume -> editable Blender/GLB turntable | Best offline-first candidate: supplied views/synthetic controls. Front-only depth is guessed. MIT code; view/depth providers and assets separate. IMAGE-SCULPT-01; higher-memory model routes retained. |
| [OOOSplat](https://github.com/ooolabdev/ooosplat) | Owned-location reconstruction for camera moves and later guide/game settings | Apple Silicon macOS15+ alpha: CPU COLMAP, Metal Brush; Windows CUDA route also retained. Unsigned/unnotarized app,16GiB run and Mac movie export unproven. OOOSPLAT-MAC-01 starts with trust/resources. Apache2 app; engine/asset terms separate. |
| [ReelMimic](https://github.com/edenfunf/reelmimic) | Analyse rhythm/colour/shot length, then original painted/crayon/pixel/paper-cut scenes | Method-first candidate on current tools; Node22.18+/Python3.10+, Mac/Linux less-tested than author's Windows. MIT; optional service charges/rights independent. REELMIMIC-LOOK-01; no duplicate studio or automatic delegation. |
| [PhotoDeblur](https://github.com/porfeng/ComfyUI-PhotoDeblur) | Restore a selected blurred still before compositing | HI-Diff CPU is documented, MPS unknown; MISCFilter explicitly requires CUDA. PHOTO-DEBLUR-01 is a conditional small still diagnostic. MIT nodes; HI-Diff Apache2 and MISCFilter MIT code, checkpoint clearance still open. Not VSR. |
| [OpenToonz site](https://opentoonz.github.io/), [source](https://github.com/opentoonz/opentoonz) | Traditional2D/cutout/Plastic mesh motion for a fitting book scene | Existing reserve, no duplicate queue. Mac/Windows/Linux routes retained; exact current arm64 build/resources unverified. Modified BSD core; brushes/third-party assets separate. |
| [Edits](https://edits.instagram.com/) | Phone captions, timelines, storyboard/teleprompter, owner finishing and later Instagram handoff | iOS/Android proprietary reference; no verified desktop CLI/MCP or autonomous publishing. Meta documents exports without an added watermark; current EU AI entitlement/quota and music rights remain separate. |
| [Viggle Image Swap](https://huggingface.co/Viggle/Viggle-Image-Swap) | Still character swap preserving pose/background as an intended affordance | Reference GPU benchmark46GB/55GB on B200; not16GiB Mac admission or proven minimum. **Non-commercial research weights:** hold monetised/public production pending permission. High-memory NVIDIA/appropriately licensed hosted route retained. |
| [TurboH3-FL2VA/I2VA](https://huggingface.co/TurboDiffusion/TurboH3-FL2VA-I2VA) | Fast image/first-last-image -> audio/video | CUDA/PyTorch/TurboDiffusion NVIDIA reference, no Mac runtime evidence. Retain for an eligible future host, but MiniMax H3 default territory excludes EU/UK/Republic of Korea/US. Separate permission gate before local use. |
| [HyperFlow H3 Flash](https://huggingface.co/VideoRebirthAI/hyperflow-h3-flash) | Accelerated14B video variants | Author RTX24/32GB measurements; Q4~9.1GB file is not runtime fit; some offload routes need much more system RAM. NVIDIA/multi-GPU reserve, same H3 territorial gate. No assumed16GB or Apple route. |
| [H3 x Z-Image hybrid](https://huggingface.co/taurusduan/MiniMax-H3-x-Z-Image-hybrid) | Experimental tensor/block mix for I2V behaviour | Future CUDA research reserve only. Apache2 metadata without a repository LICENSE does not resolve MiniMax base/derivative terms. RAM, robustness and rights unresolved. |
| [Matrix-Game source](https://github.com/SkyworkAI/Matrix-Game), [4.0 model](https://huggingface.co/Skywork/Matrix-Game-4.0), [site](https://matrix-game-v4-0.github.io/page/), [paper2610.27999](https://arxiv.org/abs/2610.27999) | Separate game state/physics, neural appearance, HUD and audio: useful future game/RUN architecture | Linux NVIDIA reference/presets: A10080GB, RTX5090/5080/5070Ti; exact VRAM/FPS admission per preset unknown here. V4 Apache2 vs older root MIT; third-party credits separate. Reference, not a current Mac trial or arbitrary-world generator. |
| [Sophon model](https://huggingface.co/adventists-ai/Sophon-Realtime-v1), [source](https://github.com/adventists-ai/sophon-realtime) | Realtime expressive dialogue/radio character research | vLLM-Omni backend; author recommends one80GB GPU for Tag/Flash and two GPUs for Base. Keep server/authorised hosted route; no current Mac or free endpoint established. Apache2 per cards, voice/input rights still checked. |
| [Freefield wrapper](https://github.com/neuregex/ComfyUI-freefield), [gateway](https://github.com/neuregex/freefield) | Model/input/licence/receipt manifests and reusable ComfyUI workflow recipes | MIT wrapper/gateway, individual model terms separate. Future approved local GPU/explicitly budgeted hosted ComfyUI route; Apple support only per demonstrated workflow. Reference principles, no new parallel orchestrator or claim of free hosting. |

## Bounded candidates for the current production stack

These are conditional proposals, not installation/execution authority and not a
reordering of active production. Select one when an authorised film needs it.

1. **IMAGE-SCULPT-01:** offline synthetic known shape and owned views -> fit -> held-out
   silhouette/depth inspection -> Blender reopen/turntable -> GLB/OBJ export. Retain
   topology/occlusion failures; do not describe inferred hidden surfaces as recovered truth.
2. **REELMIMIC-LOOK-01:** owned10–12s reference -> reviewed shot/colour/motion plan -> one
   original short look using current tools. Measure effort and export; no reference
   footage/character copying, new keys or automatic multi-agent flow.
3. **TESSERACT-RUNTIME-01:** resolve exact terms/entity/integration scope first. Check
   version/checksum/build and resources; original10–12s two-layer title/audio fixture
   -> correct one word and one position -> reopen -> both aspect exports -> decode,
   seeking, sync and time receipts. Preserve old converter evidence separately.
4. **OOOSPLAT-MAC-01:** trust/source distribution and external disk/RAM admission;
   owner-provided small orbit/still set -> bounded reconstruction -> reopen/PLY;
   separately prove Mac camera/movie export. No unsigned-app bypass or invented
   location capture. Gaussian splats do not replace named editable meshes.
5. **PHOTO-DEBLUR-01:** exact checkpoint rights/resources then HI-Diff CPU on one512px
   synthetically blurred owned still with retained clean control/local baseline.
   Inspect text, face/edge invention, colour, tile seams and time. MISCFilter waits CUDA.

OpenToonz stays the existing reserve. Edits is an optional owner-mobile handoff,
not a desktop-agent test. The GPU/server families stay discoverable even when their
nearest execution slot is deferred. New hardware triggers admission, not a blind
repeat or automatic qualification. Keep OS/driver/backend fit, RAM, VRAM and storage
separate; a service may solve compute only if terms, actual access and cost also fit.

## Sources, versions and evidence limits

Snapshot date10November2026. Full source bodies, HTTP receipt time, URL, byte count
and SHA-256 are retained privately under the canonical studio
`records/tool-intake-20261110/`; `review-assessment.json` verifies retained successful
source hashes and preserves failed/superseded fetches. Git/HF revisions below pin
what was reviewed; web/service behaviour is dated, not guaranteed permanent.
No copied upstream implementation, weights or media enters Git.

| Family | Retained upstream source/model revision |
| --- | --- |
| Tesseract creative runtime | runtime: f8a6caa07c90986a256838763b02484ddd56c580 |
| Image2Sculpt | source: 454381c13f2506b12d392e9286a8d32fc9549566 |
| OOOSplat | source: 82d46203635dfb338f8fa5118c9c09bd66f905ec |
| ReelMimic | source: 4e645857faefe34ff83596b09a43d7f610a4d481 |
| ComfyUI-PhotoDeblur | source: 4ffd73a7d244ea01b87ec0c7245497cdc51749fc |
| OpenToonz | source: a2504560093f1e7104badef58d94a0f196ebae67 |
| Edits by Meta | Dated official web documents; no source/model revision supplied |
| Viggle Image Swap | weights: 572d4971fd0d11f643232a95c126f9317e13f937 |
| TurboH3 FL2VA/I2VA | weights: 60266aa6c44e2ff371bc6aa89af8437ed9494507 |
| HyperFlow H3 Flash | weights: 61f1311bb1c8fac290d1c5121f4ebbb44525f446 |
| MiniMax H3 x Z-Image hybrid | weights: 6ff453a950d37ded994a6ac37a59856b808aa2c1 |
| Matrix-Game4.0 | source: 51913b2bfa78a6d54de912b8348b1d318f4d36e2; weights: 2c53100457da7abcf0e966f75637c644d3423a63 |
| Sophon Realtime | source: 59b687b56cfd3c44a3733eef9413dc3cf740478c; weights: 2e52bd4ade5ab9353a387de0b8930d305b1aff88 |
| Freefield and ComfyUI Freefield | wrapper: 56c2f6bb435510d1bb36b6c6218488052d974381; gateway: f3d32ce2e3128c58bb2fe38c8942edf87cdb2e4c |

Further primary detail: [Tesseract custom terms](https://github.com/mirage-hq/Tesseract/blob/main/LICENSE),
[Viggle weight terms](https://huggingface.co/Viggle/Viggle-Image-Swap/blob/main/LICENSE),
[TurboH3 territory terms](https://huggingface.co/TurboDiffusion/TurboH3-FL2VA-I2VA/blob/main/LICENSE),
[HyperFlow terms](https://huggingface.co/VideoRebirthAI/hyperflow-h3-flash/blob/main/LICENSE),
[PhotoDeblur third-party notice](https://github.com/porfeng/ComfyUI-PhotoDeblur/blob/main/THIRD_PARTY.md),
[Meta introduction](https://about.fb.com/news/2025/04/introducing-edits-streamlined-video-creation-app/)
and [Meta one-year update](https://about.fb.com/news/2026/04/one-year-of-edits-built-for-and-with-creators/).
A model-card marketing example/benchmark, library test count or public demo is not
our test, owner creative approval, reusable donor permission or audience result.

Hardware-independent architecture/method notes are reusable references, not code
copied into Framewright. No claim of unrestricted commercial rights, measured
savings, current free service credits or universal user-device support follows.

## Documentation checks

Repository link/catalogue validator and whitespace check pass. All14 newly indexed
research records are discoverable with `evidence=any`, excluded at `tested`, and
ineligible for feature planning. No model or renderer runs in these checks.

At intake time, the existing21-test search suite had17 passes and four failures. The same four
failures reproduce with the pre-intake ledger/facets and the pre-existing local
voice-policy change: old expectations still select Supertonic narration by default,
whereas the owner has moved that voice route to reserve. The intake did not
revert that decision or change runtime code to satisfy obsolete expectations.
Retained outcomes: private `records/tool-intake-20261110/validation.json` and the
pre-intake comparison output; the exact temporary comparison fixture was removed.

During the authorised production closeout/PR preparation, the four stale test
expectations and retained example were updated to the owner-approved reserve
policy. The21test search suite now passes: no automatic narration chain when
no eligible voice is present, explicit `--voice supertonic3` for the intentional
reserve example, and unchanged conditional rights boundaries. This is an offline
policy regression check, not a new model/tool qualification. Before/after logs
are retained under private `records/production-closeout-20261110/`.
