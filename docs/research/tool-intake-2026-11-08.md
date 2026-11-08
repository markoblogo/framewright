# Tool intake — 8 November 2026

Research supporting M4 / R05 / R07: reusable animation, bounded tool selection and production corrections. No installation, model/media download, inference, purchase or new production. Separate follow-up after [PR60](https://github.com/markoblogo/framewright/pull/60); no release.

## Recommended order

1. **GLB-NAMED-01:** named-part choreography using the existing Three.js stack.
2. **SCREENPLAY-01:** reproducible owned-app screencasts and selective corrections.
3. **REA-VIDEO-01:** offline shot/timing analysis against a known edit.
4. **VORK-01:** optional small 3D/VFX comparison when a production needs it.
5. **SOLIDCRAFT-01 / UIUX-PACK-01:** later task-specific CAD and packaging tests.

All are proposed, not qualified. Test one useful capability on an approved production; do not install an entire new studio. External storage and current resource preflight apply.

## GLB: useful method, with asset admission

[glTF2 specification](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html), [Three.js GLTFLoader](https://threejs.org/docs/pages/GLTFLoader.html), [Hugging Face discovery](https://huggingface.co/datasets?sort=likes&search=glb).

GLB packages glTF JSON and binary data. A suitably prepared scene can expose rigid parts through named nodes: code can isolate, colour, move and reassemble them without manual Blender editing. This fits explainers, engineering mechanisms, educational cutaways and props. We already have GLB/Three.js environment evidence through [Rokehan](manga-film-tooling-2026-11-03.md); the new question is named-part choreography, not whether GLB exists.

Names, hierarchy, semantic parts, rigging and self-contained textures are not guaranteed by the extension. Inspect names/duplicates, transforms, units, dependencies and licence first. GLTFLoader is an imported addon. Meshopt requires the decoder dependency and loader configuration; calling setMeshoptDecoder does not remove those dependencies. Rigid transforms are not anatomical deformation or character animation.

**GLB-NAMED-01:** one small cleared low-LOD asset → node inventory → isolate/recolour/explode/reassemble → two camera views → deterministic 10s renders in 16:9 and9:16 → save/reopen/revise one named part. Pass: stable identities/transforms, intact textures, legible movement, reproducible output and documented storage. No new large model or Blender install.

### CT anatomy case: distinguish collection from prepared pack

[Dataset card](https://huggingface.co/datasets/codepawl/ct-anatomy-glb), [card source](https://huggingface.co/datasets/codepawl/ct-anatomy-glb/raw/main/README.md), [TotalSegmentator source](https://doi.org/10.5281/zenodo.10047292), [supplied video](https://youtu.be/oPvkNkSqqwk).

Current card describes **7 bodies and20 organs/groups**, with **up to115 named structures** in full bodies; coverage varies by scan. It does not provide1,228 ready GLB bodies. The supplied117/1,228 formulation is not adopted as verified pack inventory. The prepared body/organ downloads total about20MB according to the card; no full CT archive is needed for a small graphics trial.

CC-BY4.0 attribution includes TotalSegmentator/Wasserthal and University Hospital Basel. Units/axes and node extras are documented. Meshopt and uncompressed engine variants exist. Segmentation gaps, smoothing, missing body regions and illustrative colours limit anatomical fidelity. Use as graphics/education material, not clinical evidence. Dataset licence does not automatically cover the demonstration soundtrack.

The YouTube page and sampled frames at5s/15s were inspected: separated bones and an assembling skeleton are visible. This is visual case evidence, not independent reproduction, full listening acceptance or measured performance. A CT example can serve GLB-NAMED-01; do not create a second duplicate test.

## Agent Screenplay — strong screencast candidate

[Repository/README](https://github.com/gmpetrov/agent-screenplay), [MIT licence](https://github.com/gmpetrov/agent-screenplay/blob/main/LICENSE).
Documented Node20+ browser/desktop recorder with agent CLI/MCP, cursor/zoom/callouts, captions and repeatable editing. Codex is supported. Existing audio can avoid cloud TTS. Desktop capture on Mac needs applicable OS access; browser fixtures can remain scoped.

**SCREENPLAY-01:** 15–20s owned local/staging fixture → record → adjust zoom/callout without re-recording → reopen → both aspect exports; compare readability, edit time and storage with our current route. Pin version; keep cache/output external. Its check/record steps actually operate the app: no live Send/Delete/purchase controls in fixtures. Init can download Chromium and change agent configuration; not run here. Optional Cartesia/ElevenLabs calls are separate paid/provider decisions.

## REA-video — analysis helper

[Repository](https://github.com/JuneYaooo/rea-video), [Apache2.0 licence](https://github.com/JuneYaooo/rea-video/blob/main/LICENSE).
Python3.10+/FFmpeg offline video analysis plus optional remote multimodal models; proposed cut/motion/audio/remake-plan extraction. Published accuracy is upstream benchmark evidence with narrow conditions, not a forensic guarantee.

**REA-VIDEO-01:** analyse one retained film and recompressed derivative against its known edit list; measure cut errors, shot classification, timing drift and uncertainties. Offline first. No automatic upload, generation or replacement of creative review. Review install scripts before allowing changes to agent folders.

## Vork — promising 3D/VFX, source-available reserve

[Repository](https://github.com/voyager-so/vork), [preview licence](https://github.com/voyager-so/vork/blob/main/LICENSE).
Rust/Slang renderer with JSON/Python/TypeScript scene authoring, GLB, animation and effects. Documented Apple Silicon/Metal/macOS26+ route makes it a host candidate, not a tested Mac qualification. The licence is **source-available preview, not open source**: own outputs can be commercial, while modified redistribution/hosted rendering has restrictions. Pin and reread exact licence/version at admission.

**VORK-01:** one primitive/cleared GLB, simple camera and one effect, 10s; compare current Three.js on visual control, deterministic re-render, render time, memory and disk. External install/cache only. Avoid large particle/water scenes initially. Upstream notes include shader compilation delay, unsupported/ignored volume features and scene-dependent failures/flicker. Do not treat preview renders or vendor benchmarks as production proof. An unrelated npm package name is not the official distribution.

## SolidCraft — parametric prop reserve

[Repository](https://github.com/tangency-labs/solidcraft).
MIT OR Apache2.0, documented Mac/browser/headless/MCP routes for parametric CAD and assemblies. Useful for precise mechanism props, not a replacement for character rigging. Early upstream geometry tests do not qualify our pipeline.

**SOLIDCRAFT-01:** make one simple assembly, modify one parameter, export glTF where supported and verify units/names/transforms in existing Three.js. Later, only when a selected explainer needs the prop; no install now.

## Reference and deduplication

- **UI UX Pro Max:** [repository](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill), MIT, documented Codex integration. **UIUX-PACK-01**, low priority: selectively compare typography/layout rules for a review/package page. It is UI guidance, not a video-motion engine. Use existing Lazyweb evidence first for product UI; inspect before any agent-config install.
- **ThinkRail:** [repository](https://github.com/JetBrains/thinkrail), Apache2.0. Useful living-spec/worktree/context ideas; a separate agent IDE around pi. Reference only: no migration from Codex or duplicate orchestration.
- **MotionSites:** [site](https://motionsites.ai/). Website/motion inspiration and prompts; overlaps existing inspiration tools. Reference only; inspect individual asset/code rights and dependencies before reuse. No inference of video export or unrestricted commercial licence.
- **Awesome-REA:** [catalogue](https://github.com/reacher-z/Awesome-REA). MIT catalogue of reverse-engineering agents/cases; individual dependencies and examples have separate rights and risk. Reference discovery, not an executable studio or a mandate to copy a broad catalogue.
- **sand3d:** [repository](https://github.com/Sandflow-ai/sand3d) is already [SAND3D-01](tool-intake-2026-11-06.md). Keep that single test; no duplicate queue entry.

## fal / FLUX3 Max — conditional access check

[Landing page](https://fal.ai/flux-3-max), [official image-to-video endpoint](https://fal.ai/models/blackforestlabs/flux-3-max/image-to-video).
Checked8November2026. Official pages describe video/audio,720p and an I2V duration range5–20s. The visible720p price is **$0.085/s**, advertised as50% off; landing/endpoint promotion end dates differ by about a day. These are dated advertised conditions, not our invoice or entitlement.

The supplied claim of free15s guest generation through9November was **not confirmed**. Try free led to fal Agent, then a sign-in dialog; no usable zero-charge quota was visible. No prompt submitted, image uploaded, account created or credits spent.

**FAL-I2V-01, conditional only:** if the actual account proves a free grant and owner-approved source-upload scope, test one short RUN//SIGNAL finale alternative with an exact attempt/cost cap. Preserve accepted M01 and compare mouth timing, thermal registration and helmet orientation. Do not regenerate the whole episode. The accepted M01 finale remains one-use; this research does not reopen production or bypass its outdoor-test gate.
