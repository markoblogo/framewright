# REVERSE-VIDEO-02 / Radar 16 — FrameLens and risk-based media review

25 November 2026. [Actual upstream FrameLens AI](https://github.com/suqivision/framelens-ai) v0.1.0.dev0, commit `cf9dc8c0a46aea49940dd3ff34520ddd0371fcac`. [Radar source: Copilot Adaptive Effort announcement](https://github.blog/changelog/2026-11-17-copilot-code-review-adaptive-effort-secret-detection-and-more/). GitHub describes a preview feature that chooses Lite, Balanced or Max subject to configured limits. Our scene is a local illustration of the broader review-depth principle, not a Copilot runtime test or proof of its choices. No real code changes, PR or account actions.

## Fixture and results

Original two-ink risograph-inspired camera illustration on cream paper, authored in local Pillow/NumPy (no third-party styling assets). Two silent 4s H.264 1280×720 / 24fps / 96-frame exports from the same illustration, A static crop; B camera pan from x=0 to approximately x=237.5px. The intended accepted fixture is B; no actual approved production master replaced. FFprobe basic codec/size/fps/frame count/duration check returned pass in both. Separate private receipt pinned the known intended SHA-256 and compared bytes, rejecting A and matching B. FrameLens measured global motion independently.

| Input | FrameLens result | Pinned hash |
|---|---|---|
| A, stale static fixture | static; confidence 1.0, global 0, residual 0 | mismatch (`f0dfcc3c5d0c0043912d28b5e006dd2d3633e1eec12e7256d45da08142405230`) |
| B, intended moving fixture | pan-right; confidence .808, global 14.319, residual .549 | match (`560b70dc4f73973c9a399bbbdb3aa9d92813ceceee630c4942aa1733a37c606d`) |

On this pair the local motion label usefully distinguishes the intended movement. Hash matching selects the exact intended file; FrameLens does not approve a master or prove identity. On the previously retained [REA fixture](reverse-video-rea-2026-11-25.md), FrameLens detected three shots with exact authored cuts at 4 and 8s, as REA did. Its motion labels for the three were all static; in particular it missed the known first-shot digital zoom/push-in (global intensity 5.147, confidence .82). The browser shot had residual intensity 4.008 despite its static global label; this is an estimate of camera motion, not a claim of no action. FrameLens recorded indicative dominant palettes and extracted keyframes; colour accuracy not independently benchmarked. No generalized superiority, calibrated confidence or automatic provenance determination.

## Runtime/provenance

Direct core `AnalysisPipeline.analyze`, no server or cloud/LLM calls; three local input files only. Python 3.12.8 and isolated external scratch runtime; numpy 2.5.5, SceneDetect 0.6.7.1, Pydantic 2.14.4, Pillow 11.3.0. Dependency installation resolved both headless OpenCV 4.14.0.94 and regular OpenCV 5.1.0.95 (transitive SceneDetect extra); loaded `cv2.__version__` 5.1.0. This mixed installation ran on the Mac but is not a clean supported dependency qualification. Resolve single compatible OpenCV wheel in a fresh environment before promoting or reusing beyond this bounded experiment. Reported analysis times 4.19/3.20/5.82s for A/B/prior fixture respectively; no controlled performance benchmark or asserted savings. No paid spend; local compute unpriced.

Retained private case `productions/radar-16-adaptive-review-2026-11-25/`: exact input clips, original texture recipe, matched-export-check receipt, FrameLens JSON plus keyframes. SHA-256 JSON: A `02a34b84fc122d65082c4f5c817881c8ede84baf10b7f0faa229688969e0f49f`, B `b4d346781d5337dd0afad35ee5a457c5cb7e9e0982851b98216f40d2deaa3bb5`, prior fixture `df8f6478e674aa609cecb04a77423a047a2f7c5d310bbbff9b1cc9abd65bacad`. The source repo is Apache-2.0; dependency terms and production/source asset rights separate. No third-party assets or source code committed.

## Editorial probe — STYLE-ROTATION-01 partial

12s silent landscape pilot, 1280×720 / 24fps, `2fab98c814577b0197448350356800392881c39a9afeec434855e707651965a5`. Full decode and sampled-frame visual inspection completed. New two-ink red/deep petrol blue over cream paper, halftone and overlay texture, independent sliding sheet layers and stamps, paired real excerpts from the synthetic export comparison. Important labels raised above the lower player-control area. Illustrates a wording-only PR versus a file-selection rule, then same basic metadata / differing motion / pinned master identity. No claims of actual Copilot operation. Owner should judge whether the difference is readable without sound and whether the new direction is suitable. Multi-style comparison still queued, no cross-style winner or owner approval. If accepted, full YouTube film will add actual news source context, fresh relevant real footage/screencast and English voice; preserve the distinction between source claims and our actual local test. No TikTok or publication authorized.

## Owner review — 25 November

Owner reported the silent probe was clear and approved proceeding with the new visual direction, horizontal only and enhanced with real photographs/video. This establishes acceptance of the probe, not a separate qualification of FrameLens or a cross-style winner. Full [Radar 16 film](../productions/copilot-adaptive-effort.md) retained for review. The multi-style comparison remains open.
