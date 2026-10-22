# FreeVideo / VDN-H3: local shot generation intake

Reviewed 22 October 2026. **P2 candidate, blocked on model-use rights before execution.**
This is adjacent to world production: offline generated shots from prompts/references,
not a demonstrated explorable world, mesh exporter or interactive scene engine.
No install, model download, generation or qualification ran. A research-only ledger
entry is discoverable with `--evidence any`; no runtime provider was added.

Reviewed engine revision: [`0afd01e`](https://github.com/FlashML-org/FreeVideo/tree/0afd01e37e0a01e2e1eafc50f0c0967878b695ed).
Execution-planning SHA256: `d4c7a9d04e4074dfb0952b4e825a805a0a4dc29e254185faad368a5f60c45e6f`.
Mac-guide SHA256: `d9e7a60df5472c7c0cbf08aab5cac4e48b398589a5a283f94c79e2f47be9d960`.
The reviewed VDN-H3 licence text has SHA256
`59b99642b95ea21630e311198ddbfffbfe05aadba0c2f5d884cbdf4efcc90f44`. These pin source observations,
not a reproduced benchmark or a legal permission grant.

## Fit for Framewright

[FreeVideo](https://github.com/FlashML-org/FreeVideo) runs the eight-step
[VDN-H3 adaptation](https://openvdn.github.io/) of MiniMax H3 through ComfyUI.
Potential uses are fiction inserts and animated book/product imagery. Keep this
separate from the earlier hosted MiniMax/fal candidate and from LingBot/Marble.

Its README documents LoRAs, first/last frames and image/video/audio references,
with launchers and an agent-oriented workflow. These are advertised capabilities,
not our tests; the Mac subset is narrower. Workflow/settings retention and the
[planner's request sidecars](https://github.com/FlashML-org/FreeVideo/blob/0afd01e37e0a01e2e1eafc50f0c0967878b695ed/docs/execution-planning.md)
are relevant to Framewright's evidence journal, but no integration exists yet.

## Resources: distinguish capacity, step time and complete output

The [execution-planning document](https://github.com/FlashML-org/FreeVideo/blob/0afd01e37e0a01e2e1eafc50f0c0967878b695ed/docs/execution-planning.md)
uses a memory-capped H200 for its capacity grid; that is not an 8 GB consumer-card
speed measurement. A sampling-step timing cannot establish total generation time.
Current Windows end-to-end examples for 10s at 1344×768, using two-pass sampling:

| Reported GPU | VRAM + RAM | Complete time | Evidence boundary |
| --- | --- | --- | --- |
| RTX 5060 Ti | 16 GB + 32 GB | 486s | Author-reported hardware result |
| RTX 4060 Ti | 16 GB + 32 GB | 558s | Author-reported hardware result |
| RTX 4060 Ti | 8 GB + 64 GB | 603s | Community report linked as issue 22; not 8 GB/16 GB |

These are source reports, not reproduced Framewright benchmarks. The supplied
older claim that no full consumer 8 GB result is documented is now outdated; a full
8GB VRAM +16GB RAM result is still not established by this table. Disk streaming
makes storage capacity/speed part of the resource assessment.

## Mac route

The [experimental Mac guide](https://github.com/FlashML-org/FreeVideo/blob/0afd01e37e0a01e2e1eafc50f0c0967878b695ed/docs/Mac.md)
documents Apple Silicon, macOS 14+, Metal/MLX execution, and prompt/first-frame/two-pass
support. It reports these Light-level results on an M5 with 24 GB unified memory
and about 14 GB available: 10s at 1344×768 takes about 42min; 10s at 960×544 about 22min;
1.6s at 512×512 about 3min. Earlier chips use a different BF16 path and are described
as slower. Do not transfer NVIDIA VRAM thresholds or M5 timings to the owner's Mac.
Full last-frame/reference/LoRA parity on Mac is unverified here. Before any later
install, inspect actual chip, memory, free disk and selected model-pack sizes.

## Rights gate

The engine code is Apache 2.0, but its weights use the separate
[MiniMax H3 Community License](https://huggingface.co/OpenVDN/vdn-minimax-h3-edge/blob/main/LICENSE).
Definitions I.3/I.5 exclude the EU, UK, South Korea and US from its territory;
V.4 also restricts use of the works and outputs outside the applicable territory.
France is therefore outside this standard grant. II describes a separate licensing
request for excluded territories. Keep local trials and production on hold until
an applicable separate authorisation is retained. A VPN, remote GPU or hosted endpoint
alone does not establish permission. Check exact checkpoint, base assets and LoRAs
individually; the engine's Apache licence does not grant model/output rights.

## First bounded test if rights and resources are cleared

Use one owner-approved book/fiction image: animate it into a 2–3s insert with one
specified camera move. Fix model/runtime revisions, seed, quality and input hashes;
retain the workflow, request sidecar and original output. On Mac start with the
small supported prompt/first-frame path. Check identity, requested motion, temporal
artifacts, usable cut boundaries and actual full-run time/memory/disk. Compare a
second take only within an agreed resource ceiling; stop after an unsuitable first
trial. Later last-frame/LoRA tests require their own supported platform and rights.

[Experiment queue](experiment-queue.md) · [World shortlist](world-production-intake.md).
