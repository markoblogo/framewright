# Virtual worlds as film material: intake shortlist

21 October 2026. The owner selected this direction for a short-fiction adaptation
and a later series of world-production experiments. This is source review and
planning only: no accounts opened, installs, generations, captures or new tool
qualifications. No additional arsenal profile or discovery eligibility is implied.

## Candidate roles and what is still unknown

| Candidate | Why it is relevant | Next bounded question |
| --- | --- | --- |
| [Marble / World Labs](https://marble.worldlabs.ai/) | The owner reports an established account, existing worlds and previously published videos | Which existing world gives a reusable location, controllable camera and an editable or recordable output? Inspect actual assets and account rights before new generation |
| [Decart Oasis](https://decart.ai/oasis) · [model project](https://oasis-model.github.io/) | One candidate, two sources. The 2024 Decart/Etched project describes keyboard-controlled generated video and links code, a small checkpoint and a live demo | Can one intentional camera/action shot survive temporal drift and be captured usefully? Current demo access, recording/export, rights and local resource requirements remain unverified |
| [Odyssey](https://odyssey.systems/) | The current official site exposes experience and API-access links; already a research candidate in Framewright | Can an available account deliver a directed short shot with a retained action/camera record? Confirm access, cost and output use; do not require a particular model number |
| [Google DeepMind Genie](https://deepmind.google/models/genie/) | The current Genie 3 page links to Project Genie, an experimental world-creation/exploration prototype | Is the owner's account eligible, and can the result supply usable recorded footage? Account/region access, cost, capture/export and continuity are unknown |
| [LingBot-World](https://github.com/Robbyant/lingbot-world) / [Infinity (v2)](https://github.com/Robbyant/lingbot-world-v2) | Image-conditioned, directed video worlds; useful candidate for fiction establishing shots and action inserts | P2 after the Marble inventory; separate v1/v2 licences, hosted access and CUDA resources before a private shot test |

The Decart product URL timed out in the read-only web fetch; the model project page
was readable. Its 2024 research description is not a current hosted-service or
Mac hardware benchmark. Official demo/model claims are not Framewright trials.
A world that can be explored is not automatically an exportable 3D scene, and a
model page does not prove that the owner has production access.

Marble web access does not imply separate Developer API/beta access. Its
[official web quickstart](https://marble5.worldlabs.ai/docs/web-quickstart) is a
reference for a later API assessment, not an instruction to install a client or
obtain credentials now. No private account inventory has been inspected here.

## LingBot assessment — 22 October 2026

**Queue decision: P2, access/rights/resource-gated candidate.** Keep Marble first.
Reviewed code revisions: [v1 `a43bec7`](https://github.com/Robbyant/lingbot-world/tree/a43bec7f8091c83e9b30b16b912f6fc906236fa6),
[v2 `1895d30`](https://github.com/Robbyant/lingbot-world-v2/tree/1895d300d8ac936401689b26389f51cbd36530eb).
The v2 licence text SHA256 is
`9e502ba75fd0fd30cea5497b438a4bc12f07f02bc932a7a6041fd6a18b8f46a0`.
Research-only discovery is separate from a runtime provider or qualification.
The original repository now redirects development to Infinity/v2; retain both
versions as separate options rather than inheriting permissions between them.

For our fiction work, test a directed camera move and brief action as editable
film material. This is generated video: an explorable feed does not establish an
exportable mesh, stable scene graph or repeatable character performance.

- **v1:** the [repository](https://github.com/Robbyant/lingbot-world) and official
  [Base Cam model card](https://huggingface.co/robbyant/lingbot-world-base-cam)
  identify Apache 2.0. Pin the selected checkpoint and all dependency/input terms
  before admitting a production asset; v1 is no longer actively maintained.
- **v2 / Infinity:** the [repository licence](https://github.com/Robbyant/lingbot-world-v2/blob/1895d300d8ac936401689b26389f51cbd36530eb/LICENSE.txt)
  and [1.3B model card](https://huggingface.co/robbyant/lingbot-world-v2-1.3b-causal-fast)
  identify CC BY-NC-SA 4.0. Hold monetised/book-promo use pending explicit
  compatible permission or hosted terms, including output rights. Do not assume
  that every generated output inherits the model licence or that hosting removes it.
- **Execution:** the [official inference script](https://github.com/Robbyant/lingbot-world-v2/blob/1895d300d8ac936401689b26389f51cbd36530eb/generate.py)
  uses CUDA and saves video. README examples use eight GPUs for 14B and four for1.3B;
  these are reference configurations, not proven minimums. Mac/MPS support and
  actual memory/speed remain unverified. The 1.3B checkpoint needs shared T5/VAE/tokenizer assets.
- **Hosted route:** [Reactor's LingBot World 2 page](https://www.reactor.inc/models/lingbot-world-2)
  exposes a playground, recordings/API tabs and a displayed price of $0.007/s
  ($0.42/min) on this review date. Account eligibility, billing minimums, export,
  capabilities and commercial/output terms remain unverified. No session was started.

First proposed trial: one owner-approved reference, 5–10 seconds, one forward move
then a turn, followed by one repeat. Assess direction, continuity and editable
capture using the comparison below. Seek a usable film insert, not a general
world-model ranking. Check hosted rights/access first; obtain a resource ceiling
before spending. Source review only: no install, weights, uploads, generation or qualification.

## A film-led comparison

Start from one approved scene after reading the owner's source story. Freeze its
location, reference image, camera move, action and usable duration. Compare only
the candidates that can attempt that scene with the available access and budget.

Retain five observations for each actual trial:

1. **Direction:** did camera and action follow the intended shot?
2. **Continuity:** did the location, geometry and any character remain recognisable?
3. **Editing:** can the output be captured/exported cleanly, trimmed and matched to another shot?
4. **Provenance:** which project, inputs, service/model, rights and capture method produced it?
5. **Resources:** actual credits/time, resolution, frame rate and failed attempts; keep unknowns explicit.

Use existing Marble assets for the first inventory. A new provider is useful when
it resolves a particular scene requirement. Do not generate the whole film as an
unbounded tool comparison. Each paid trial needs a concrete scene, access check,
resource ceiling and acceptance conditions before execution.

[Story/capture intake and current production status](next-cycle.md) ·
[Experiment queue](experiment-queue.md).
