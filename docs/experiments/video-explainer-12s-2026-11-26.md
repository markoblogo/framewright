# VIDEO-EXPLAINER-01 — silent matched 3D trial

26 November2026. Owner requested a12s landscape Video Explainer trial compared
with our current approach,without paid requests or new model downloads.
Status:both exports technically checked;owner adopted Video Explainer as an additional tool. No A/B superiority or default-route replacement selected.

## What was actually used

Pinned upstream `petergyang/video-explainer` source
`be2f729161585be2482f6a5699e8cfb47da3daeb`;native `build.py`,ExplainerStage,
Studio3D and HyperFrames0.9.79. Isolated external npm runtime installed with
scripts disabled;no global skill installation or default setup.sh. New code,
JavaScript libraries and local-render font cache are dependencies,not model
weights. Existing system Chrome/hardware Metal path,Python/numpy and FFmpeg.
Native voices,ASR,cloud generation,stock media,models and billing were not used.

Wrapper supplies the matching local CLI path and external Three.js cache.
Generated GSAP script references were localised for render independence. Original
upstream engine source was not patched. Standard fixed Framewright delivery
reused;the upstream review server was not installed or substituted.

## Controlled comparison

- A:retained direct Three.js/Chrome frame capture and FFmpeg local encode.
- B:native Video Explainer3D rig/build and HyperFrames local renderer,then
  stream-copy video-only extraction. Upstream mix is silent but contains an audio
  stream;the delivered file deliberately removes it.
- Both use the same original scene function,geometry,positions,camera trajectory,
  labels and12s timing:one document moves from preparation through inspection to
  a mechanical ready stamp;camera pulls back and the ending holds. Lighting,
  environment/bloom and capture/encoding implementations differ intentionally.
  This is a workflow/rig comparison,not a blinded equal-pixel benchmark.
- Initial fixtures had a scanner support crossing the travel corridor and a
  detached stamp rod. Both arms received the same geometry correction. A shared
  authored canvas-font race affected fresh-page text textures;locking the plaque
  font to existing Arial fixed the delivered fixture. This was shared authoring
  code,not evidence of an upstream Video Explainer defect. Early failures retained.

## Actual checks

A,B and synchronised comparison:1920×1080,H264/yuv420p,30fps,360frames,
12.000s,zero audio streams;full decode passes. Native lint had0errors/0warnings.
Seven state samples including backwards seeking match across both routes;
native independent browser reopen matches sampled state. One native `REVIEW`→
`CHECK` plaque edit preserves sampled object/camera state. After font correction,
fresh-browser raster at4.8s is identical;edit differences over2levels are confined
to bbox[963, 222, 1103, 250],with2792changed pixels. Pixels outside the station-label region
have maximum channel difference0.
These are bounded checks,not universal seek/renderer determinism.

Native final render reported 1m 16.6s;baseline capture/encode took
32.373s in its retained measurement. Different capture,
encoding and lighting paths,one final run each;startup/setup/authoring/revisions
not jointly controlled. No generic speed or labour-saving conclusion. Provider
charge0;local electricity,compute and active work unpriced. No new GPU/model
qualification. Actual media/revision/browser receipts and hashes remain external.

Operator inspected sampled encoded frames and continuous source action. B adds a
visible glow/softer lighting treatment to the same geometry;A is plainer. This
simple fixture does not establish a better story or stronger viewer response.
Both depend on authored choreography:Video Explainer does not turn arbitrary
briefs into good films automatically. Keep the current primary route;retain B
as an optional3D rig pending owner choice. Existing editorial ranking defaults
were reviewed and left unchanged;no speculative quality scores added.

## Scope and next decision

Only silent continuous3D,one local export and one protected text revision tested.
Motion/Illustrated styles,narration,music,ASR,generated media,native review UI,
long films,portrait layouts,clean-machine transfer and model evaluation untested.
Code MIT and bundled Inter OFL;original geometry/animation,no third-party footage.
System Arial used for rasterised plaques,not redistributed as a font file.

Private project:`productions/video-explainer-trial-2026-11-26/`.
Final sources:`scene-delivery.js`,`native/script.md`,native generated project,
`baseline/index.html`;earlier scene versions retained as preflight evidence.
Standard page:`http://127.0.0.1:8924/review.html`,B in main player;A and synchronised
A/B as separate downloads. Owner adopted the tool as an additional route;no public publication inferred.
One executed trial family,not three films or additional counts for corrections.

## Owner decision

Owner adopted Video Explainer as an additional tool after reviewing the probe. This closes VIDEO-EXPLAINER-01 at the tested silent3D scope;no A/B superiority,default-route replacement,untested modes or universal quality approval is inferred.
