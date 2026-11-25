# Video, avatar, roto, 3D and music intake — 25 November 2026

Owner-supplied links; primary-source review only. Supports M4/R05 (bounded
comparison), M1 (feasible offers) and R07 character/scene work. Existing
production order and pauses remain unchanged. Host observed arm64, macOS
27.2.1; physical RAM query was denied, so verify capacity before installing.
Current local routes include Blender/Three.js, ComfyUI, FFmpeg and local
speech/audio editing; no available NVIDIA runtime is established.

| Family | Disposition | Reason |
| --- | --- | --- |
| Silhouette 2027 | Conditional test, highest tool priority | Native Mac standalone; meaningful temporal matte/correction gap; commercial trial required |
| Taan AI / TimingBench | Local method queued; provider conditional | Music cue timing and selective revisions useful now; paid service, no verified free entitlement |
| MAGI-2 | Catalogue reserve, cloud access gated | Promising reference/timeline video; distributed 480B model, documented paid API |
| CUPID + ComfyUI wrapper | Catalogue GPU reserve | Mesh and recovered camera can improve integration of 3D with photos; CUDA mandatory in documented routes |
| AURA 1.3B/5B | Noncommercial research reference | Speech-driven avatar, CUDA and both checkpoints noncommercial |

## Silhouette 2027 — bounded candidate

[Release](https://borisfx.com/news/silhouette-2027-faster-ai-assisted-roto-more-controllable-mattes/),
[walkthrough](https://borisfx.com/videos/silhouette-2027-whats-new/),
[product requirements](https://borisfx.com/products/silhouette/?collection=silhouette&product=silhouette),
[2027 guide](https://borisfx.com/documentation/silhouette-2027.0/).
Release announces Body ML, Roto ML, combined Matte ML (mask, track, refine,
deflicker), Video Inpaint ML and wider 3D capabilities. Standalone and OFX
hosts supported; product requirements list macOS 12+, Apple Silicon GPU for
ML, 16 GB+ RAM and fast storage. Actual 2027 compatibility with our OS and
memory must be checked. Proprietary: advertised from $545/year or $103/month;
free-trial offer exists but account eligibility, duration and export terms
are unverified. No subscription, installation or activation now.

**SILHOUETTE-ROTO-01 (conditional):** use owned 5–8s moving foreground with
hair/edges and one occlusion, compare existing local mask/compositing route
with Silhouette Matte ML; black/white/contrasting backgrounds, inspect edge
leak, flicker and lost detail, manually correct one troublesome frame, reopen
project and export alpha/matte without changing original. Record setup,
correction effort, render, watermark/licence and resource use. Compare with
SAM 2 where feasible; CorridorKey is a distinct chroma-key baseline, not a
substitute for arbitrary-background roto. Inpaint and 3D are later separate
checks. Stop after trial/access preflight if no permitted free route.

## Taan AI — useful method and conditional service

[Application](https://app.taan.ai/) (fetch unavailable), [product and plans](https://taan.ai/),
[TimingBench](https://taan.ai/research/control-benchmarks/), [MCP/API guide](https://taan.ai/docs/).
This is music for picture, not video generation. Vendor describes timed
instrument entrances, selective edits and WAV/MP3/stems. Its own 250-prompt
benchmark reports 96.1% instruction success and 91.3% events within ±500ms;
these are provider measurements, not our results or independent proof of
musical quality. Fidelity metric in same table is worse than comparison
systems (4.8 FAD vs 2.6–3.5); do not infer overall superiority. Plans shown:
Creator $15/month, Agency $45/month; commercial rights claimed for plans.
No free generation entitlement confirmed. MCP balance/progress reads are
free; generation/refinement consume credits. No login, connection or spend.

**MUSIC-CUE-01 (local method):** select owned 12–20s edit; freeze cue sheet
(e.g. entrance, transition accent, ending, narration gap), compare ordinary
library track placement to timed local edit using FFmpeg and cleared stems
or existing audio. Log target vs observed onset in ms, ±500ms count,
transition smoothness, voice masking and ending; revise one cue without
changing the rest, retain timings and listening judgment. Inspired by
TimingBench, not reproducing its benchmark or testing Taan. Existing
SUNO-MCP-01 stays separate. **TAAN-SCORE-01** is conditional only: if a
permitted no-extra-cost account/partner trial is confirmed, compare same
cue sheet and owned clip, export stems and edit one event, independently
measure timing and preservation, verify rights before public use. Otherwise
retain Taan as reference; no paid plan solely for this experiment.

## MAGI-2 — frontier video reserve

[Research announcement](https://sand.ai/blog/magi-2/), [Sand homepage](https://sand.ai/),
[API pricing](https://platform.sand.ai/docs/model-pricing/). Vendor announces
480B total/~28B active parameters, up to 30s 1080p25 with synchronized sound,
multiple image/video/audio references, timeline/cut control and targeted
editing. Distributed inference and dedicated upscaling; future open-source
release promised, not a confirmed downloadable flagged model today. Active
parameter count does not imply 28B local memory footprint. Official site
points to VidMuse partner; API $0.08/s (10s $0.80 before retries), top-up status
limited according to docs. No verified free allocation, commercial terms or
local Mac route. Do not confuse with MAGI-1/preview or SAND3D-01.
Possible later 8–10s two-beat reference-conditioned shot with exact cue and
one targeted change vs existing eligible I2V route; check identity, contact,
cut timing, sound, unchanged surroundings and accepted-shot cost. Vendor
notes rapid-motion artifacts and imperfect complex sound. No new active test
until suitable access, rights and budget are established.

## CUPID / ComfyUI-Cupid3D — useful GPU reserve

[Upstream](https://github.com/cupid3d/Cupid), [wrapper](https://github.com/Nekodificador/ComfyUI-Cupid3D).
Upstream jointly reconstructs object geometry and camera intrinsics/extrinsics
from an image; mesh/gaussian/radiance-field outputs and Blender conversion;
Linux tested, NVIDIA >=16GB VRAM, CUDA. Model and most code MIT per upstream;
submodules carry separate terms. Experimental GPL-3.0 wrapper simplifies
installation but still requires NVIDIA CUDA 12.x, spconv-cu126, ~7GB weights
plus DINOv2; reported peak ~11.5GB VRAM on one 719-square image. No baked
texture, multiobject, Gaussian/radiance-field output in wrapper. No documented
Metal/MPS route; ComfyUI's presence doesn't resolve CUDA. Preserve as one
family, not two redundant trials. Intended future test: reconstruct original
prop from known Blender camera plate (optional mask), align mesh to original
image, compare projected silhouette and landmarks against ground truth,
reopen/export in Blender and inspect alternate viewpoints. Compare Tripo
Orbit/Blender asset route, not claim unseen geometry reconstruction accuracy.
Require compatible GPU, licence checks and separate environment before any
install. No active Mac test or purchase.

## AURA — avatar researcher reserve, noncommercial only

[Kyutai announcement](https://kyutai.org/blog/2026-11-20-aura/),
[repository](https://github.com/kyutai-labs/aura),
[5B card](https://huggingface.co/kyutai/AURA-5B) (card direct fetch failed),
[Kyutai model list](https://huggingface.co/kyutai). GitHub README supplies
explicit model and licensing evidence: portrait+speech to streaming talking
head; 1.3B 576p16fps, 5B 720p25fps; reference optimized actual code reported
~16/~8fps on H100 respectively, distinct from paper speeds. CUDA required;
1.3B weights CC BY-NC 4.0; 5B Snap Non-Commercial. Ancillary model licences
separate. Live demo linked by upstream, not tested. No supported local Mac
route, no commercial tutorial/partner/monetised use inferred. Potential
private noncommercial benchmark with consented or original synthetic portrait
and own audio: lip-sync, identity, pauses, expression, crop and reveal;
compare with existing avatar routes if explicitly selected and rights allow.
Never equate streaming inference with qualified long-form Udemy teaching.

No hardware inference, download, account/profile modification, paid call,
or film production occurred. Results are sourced capabilities/access notes,
not qualification; actual account, cost, quality and commercial permissions
remain separate gates. No release or roadmap reprioritisation.
