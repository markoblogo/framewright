# Tool intake — 7 November 2026

Historical intake plus8November outcome note: original Cinecode-inspired pilot and full Copilot film were subsequently accepted in both aspects; native Cinecode remains unexecuted. See [current state](../next-cycle.md). All other proposed tests below remain unexecuted.

Original research scope, supporting R04/R05 (task-specific methods), R09 (sound/subtitles), M3–M5. No installation, model download, inference, paid call, provider switch or production started. Separate uncommitted follow-up to frozen PR60; no release requested.

## Deduplication and evidence

Ten supplied links resolve to eight main subjects: Mischief's model card and press release are one subject; Proglib is a secondary roundup, not a ninth tool. Exact-name search found no earlier entries in the current catalogue/queue. A newly discovered related model, Parakeet Redux, is explicitly additional. Listings and benchmarks below are vendor evidence, not our qualification. Prices/access are dated snapshots and require rechecking before execution.

## Priorities and dispositions

### Cinecode — first animation-method candidate

[English README](https://github.com/sarpstar/cinecode/blob/main/README.en.md), [MIT licence](https://github.com/sarpstar/cinecode/blob/main/LICENSE).
Quick mode authors deterministic Canvas/Three.js motion in a self-contained HTML film with shared picture/audio cues and MP4 capture. Film mode adds staged production and QC. Documented clients are Claude Code/Cursor; Codex adaptation is our proposed work, not native support proved here. Node22+, Python3.9+, FFmpeg and Chrome/GPU require host admission. Reuse the timing/scene method, not its entire agent setup. Upstream hooks do not replace our permissions or review rules.

**CINECODE-01, proposed:** one 12–15s original memory-card scene, deterministic timeline, existing/local sound, 16:9 and9:16. Compare with current compositor on readability, audio sync, seek/repeat, render effort and peak storage. Pin source/version and preserve attribution before adapting code. External scratch only; no cloud TTS/API fallback. The original local timing-method pilot was subsequently accepted; native upstream execution and the proposed A/B remain untested.

### Parakeet Ultra and Redux — transcription, not voice generation

[Ultra model card](https://huggingface.co/moondream/parakeet-ultra), [OpenRouter](https://openrouter.ai/moondream/parakeet-ultra), [Redux model card](https://huggingface.co/moondream/parakeet-redux).
Ultra is a0.6B post-trained NVIDIA Parakeet model, CC-BY4.0, with word/segment timestamps and25 European languages. Its published performance measurements use Photon on NVIDIA GPU; that does not prove Mac Ultra performance. OpenRouter lists$0.000017/audio-second, a paid route. Lack of EU in-region routing is a residency limitation, not proof of denial to French users.

Redux is a separate178MB ternary sibling with documented CPU/Apple Silicon/Metal routes and CC-BY4.0 weights. Published speed is vendor measurement. Its own evaluation reports weaker noisy-audio and French accuracy than the original: compactness is not universal quality improvement.

**ASR-PARAKEET-01, proposed local-first:** admit Redux/Photon compatibility and dependencies before any download. Compare a cleared60–90s English/French sample with the retained Whisper baseline: proper names, diacritics, omissions, silence hallucinations, word timing, background music/noise, real RAM/time. Retain attribution. Ultra is an optional separately budgeted comparison, not an automatic paid fallback. No test run yet.

### Riverflow V2.6 Pro — paid typography/editing reserve

[Sourceful model card](https://openrouter.ai/sourceful/riverflow-v2.6-pro).
Unified image generation/editing with up to10 image inputs, custom dimensions and up to two custom fonts; published limits include16.8MP total. Listed starting price$0.13/image is not a fixed upper cost: job settings affect the charge. Useful hypothesis: exact typography and protected-region edits for covers, compared against built-in imagegen.

**RIVERFLOW-TYPE-01, conditional:** one cleared typographic card in both aspects; check spelling, font compliance, protected regions, identity and actual cost. Requires an explicit budget and upload permission before calling. No quality/savings claim.

### Mischief1 — paid previs reserve

[OpenRouter model card](https://openrouter.ai/tbc/mischief-1), [TBC announcement](https://tbc.co/press-releases/neuron-derived-ai-video-model).
Image-to-video marketed for quick ideation/previs; listing starts at$0.005/second. TBC describes biological discoveries used to improve models running on ordinary silicon. “Neuron-derived” and efficiency superiority remain vendor claims, not independently established science or proof that live neurons execute our generation. Page was accessible by read-only HTTP fallback after the browsing extractor failed.

**MISCHIEF-I2V-01, conditional:** one5–8s cleared still with simple smoke/fabric movement; compare identity, deformation, continuity, download quality, actual cost and reuse rights with an existing baseline. Not a hand/contact solution until tested. No paid execution authorised by this entry.

### Inkling2 Small — cloud coding/scene-authoring reference

[Thinking Machines announcement](https://thinkingmachines.ai/news/inkling-2-small/).
594B total/17B active MoE with vision and agentic coding demonstrations. Initially closed weights through Tinker; planned Apache2 release is a future promise, not weights available at this review. Potential use: scene-code assistance. Not a lightweight local Mac model or a video generator. Reserve only; no new provider account, download or agent replacement.

### Crouton Alpha — public-data-only coding reserve

[OpenRouter card](https://openrouter.ai/stealth/crouton-alpha).
Anonymous stealth coding/multimodal endpoint, listed free with1M context. Provider may retain prompts/responses; no assumption of permanent free availability. EU in-region routing unavailable does not establish a France access ban. No private manuscripts, account data or closed repository uploads. Low-priority synthetic/public-data comparison only after provider admission; no routing change.

### PortCode — engineering reference; no current video trial

[Supplied site](https://lakomoor.github.io/portcode/), [linked repository](https://github.com/LakoMoor/portcode).
Read-only HTTP fallback confirmed the exact site's identity. Rust port/reverse-engineering agent with pinned originals, evidence ledger and golden-output/parity checks; documented macOS binaries and local/self-hosted model routes. “Proof” means tested parity against chosen observations, not mathematical equivalence. Useful transferable idea: separate observation/inference/unknown and compare golden outputs. No measured need to rewrite Framewright in Rust; no install or porting trial queued. Do not confuse it with the author's Android OpenCode project.

### Kuwayama marks — visual reference only

[Symbools archive](https://www.symbools.com/kuwayama-trademarks-symbols-vol-2).
Digitised collection of1504 marks from a1973 volume, credited to Yasaburo Kuwayama and digitiser Kelvin Adithya. Page expressly limits use to noncommercial and retains owners' mark rights. Our monetised production must not treat this as a reusable logo/asset pack. Shape/motion study only; create original forms rather than copying marks. No commercial asset test queued.

### Proglib roundup — secondary leads, not qualified additions

[Supplied roundup](https://proglib.io/p/openrouter-dobavil-modeli-dlya-koda-rag-i-golosa-sravnivaem-ceny-2026-11-06).
Useful grouping: coding/router models, structured decisions/RAG and speech/image endpoints. Crouton/Parakeet overlap the primary checks above. Additional names such as Ripple, Hy4, Particle-1, Auto Code, Joey1, d1.1, Reflex, Clairic and Parallel Decisions Fast remain secondary-source leads, not verified compatibility/licence/price entries or active tests. No present Framewright deficit justifies a blanket coding-provider or RAG switch. Revisit only a specific scene-authoring/indexing bottleneck, then verify its primary card and budget. Publication/listing/release dates must remain distinct.

## Execution order

On a fitting owner-selected production: Cinecode timing probe → local Redux transcription probe; typography/I2V reserves only if an actual deficit and approved budget warrant them. Do not run this entire queue merely to make a film. Except for the later original Cinecode-inspired local pilot/full-film case, proposed tool tests remain unexecuted; current working tools stay available.
