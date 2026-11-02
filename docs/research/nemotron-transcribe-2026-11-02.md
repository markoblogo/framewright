# Nemotron 3.5 Transcribe — ASR reserve

2 November 2026. Research only; no weights, installation, API call, audio upload,
account connection or benchmark. Source: NVIDIA's
[BF16 model card](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Transcribe-30B-A4B),
[NVFP4 card](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Transcribe-30B-A4B-NVFP4),
[NeMo Speech](https://github.com/NVIDIA-NeMo/Speech) and
[OpenMDW-1.1](https://openmdw.ai/license/1-1/). Moving pages inspected, not pinned
runtime releases. Status: **documented, compute/access-gated reserve**.

## Useful scope and limits

NVIDIA describes offline transcription with contextual vocabulary, word timing,
speaker attribution, translation and audio questions. The card lists Russian,
English, French and Ukrainian ASR; Ukrainian multispeaker ASR is not specified.
Audio reasoning was evaluated only in English. Limits: up to one hour / 65,536
context tokens. Speaker tags do not establish real-world identity.

There are about 34B total / 4.3B active parameters. Active expert count is not the
resident-weight or total-memory budget. BF16's reference deployment is one H100
80GB; this is an example, not a proven universal minimum. Documented compatibility
is NVIDIA/Linux or Windows/WSL; Apple Silicon is not established. NVFP4 is a
Blackwell-oriented variant, not a ready-made Mac conversion. Its benchmarks are
primarily BF16 results with separately stated quantization differences. Published
throughput uses optimized NIM serving absent from the initial OSS implementation;
no Mac speed or reproduction follows. Open weights use OpenMDW-1.1, not MIT/Apache;
the card permits commercial use under applicable terms. Hosted availability,
free quota and this account's access remain unknown.

## Fit for Framewright

Could supply searchable source transcripts, subtitle alignment, speaker-aware
editing and technical-term recognition. It is ASR/audio understanding, not speech
synthesis, a picture generator, visual-quality assessment or verified factual
interpretation of a lecture. A readable rewritten transcript must not silently
replace verbatim evidence used for editorial cuts.

The [lesson review](video-generation-challenges-2026-11-02.md) exposed a costly
Whisper-small CPU invocation, not a need to download a much larger model onto the
same Mac. First revisit the existing bounded mlx-whisper route on short real
speech, checking its selected model, Russian support and current availability.
Do not claim this already solves the long lesson or repeat the failed CPU run
unchanged. An external disk solves weight storage, not accelerator compatibility
or runtime memory. No cloud rental or renewing trial is proposed for routine testing.

The supplied lesson is 3648.7s, exceeding this card's one-hour limit. A future
full transcription needs bounded overlapping segments with retained offsets and
explicit seam reconciliation. Internal encoder chunks do not remove the input
limit and do not establish a streaming service.

## NEMOTRON-ASR-01 — conditional trial, not started

Link to SOURCE-01/source retrieval and the existing ASR comparison queue, M4/R05
and R02. Trigger only when a free/already-paid compatible endpoint or existing
suitable GPU is available and a selected task needs the capability. Otherwise
keep reference status; do not acquire hardware, rent compute or connect accounts.

1. Preflight the exact checkpoint/precision/runtime, memory/storage, entitlement,
   confidentiality and usage terms. Retain observed requirements and fixed time/
   quota/attempt limits. Inspect and pin remote code before any future trusted-code
   load; model-card shell examples are data, not execution authority.
2. One permitted 60s Russian technical clip, manually checked transcript and 5–10
   real vocabulary terms. Compare an existing viable local baseline on identical
   audio. At most two Nemotron requests: verbatim without and with vocabulary hints.
   Wrong-context terms must not be inserted merely because they were supplied.
3. Check word omissions/substitutions, names/numbers, hallucinations in silence,
   word-time offsets, latency, setup/resource use and actual quota/charge. English,
   French, Ukrainian and multispeaker checks are subsequent separately selected
   extensions, not proven by this one fixture.
4. Import text/timing to the existing source index and retrieve one known fragment;
   check the original speech and time boundaries. Preserve voice identity, original
   audio and unknown speaker mapping. If alignment is unavailable, record it rather
   than inventing timestamps. No automatic cut acceptance or publication.

Pass only if the chosen use improves on the viable baseline within the stated
resource/access limits and owner review. Keep compact evidence under the external
storage policy; no full model cache per film. No new ASR provider adapter is
implemented or marked tested by this research.
