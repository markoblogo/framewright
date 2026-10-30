# Real spaces as reusable film sets — RECON-01

Reviewed 28 October 2026 from official sources. Research only: no installation,
account connection, subscription, upload, reconstruction or render. All five tools
remain untested here. This records a missing production capability, not a new priority.

## Roadmap fit

[Roadmap](../roadmap.md): **M4 / R05** bounded improvement to an existing route;
potential **M5 / R07** environment for Good Dog or other fiction. The useful outcome
is a retained real location with repeatable camera moves, not another world-model
demo. It can support a location promo, virtual visit, transition from footage to a
digital set, or a separately staged character against a reconstructed environment.
Current R01/R02 priorities and production pauses remain unchanged.

## Candidate decisions and official evidence

| Candidate | Documented scope | Cost/platform boundary | Disposition |
| --- | --- | --- | --- |
| **SpAItial Echo-3** | Phone capture → Gaussian-splat space; vendor claims metric scale and completion of unseen regions; browser sharing | iPhone, iOS 18+; subscription with introductory month, not a permanent free route. Android announced, not available evidence. Exact export formats, usable camera control, output terms and account entitlement unresolved | Conditional candidate after suitable device, entitlement and export/rights checks; no trial enrollment now |
| **Polycam** | Photos/video → splats, editing/viewing; product page also advertises downloadable mesh | Official Object Mode table excludes splats from Free; Basic and above include them on iOS/web. Android listed as photogrammetry only. Exact output export entitlement and publication rights need checking | Conditional candidate if an existing eligible plan or a specifically approved production supports it; not a free splat route |
| **Postshot** | Local reconstruction, animated cameras/movie output, AE integration and splat PLY export documented | Windows builds; historical official requirements specify NVIDIA. Free plan noncommercial; watermark-free video and radiance-field export listed under Indie, CLI under Studio. Current GPU minimum and actual paid quote must be refreshed | Windows/NVIDIA reference reserve; no current Mac trial |
| **Nerfstudio** | Open-source NeRF/splat tooling; viewer camera paths and video rendering | Core Apache-2.0; documented setup uses PyTorch/CUDA and tiny-cuda-nn, Docker NVIDIA. Native Apple Silicon training not established. Compute, dependencies and data terms separate | Technical reserve pending compatible available compute; no heavy install on current Mac |
| **Splatframes** | Capture alignment, splat editing, camera position/look-at/FOV/roll keys; H.264, ProRes 4444 alpha, PNG; scene/data exports | Windows 10/11; viewer OpenGL 4.3, Trainer NVIDIA. Standard and Trainer differ. Early access with code/key; pricing unannounced | Windows reference reserve; no current test or free-cost classification |

Sources and details that affect selection:

- Echo-3 [product](https://spaitial.ai/echo-3), [27 October announcement](https://spaitial.ai/blog/echo-3-release),
  [App Store](https://apps.apple.com/gb/app/spaitial/id6803571420).
  Accuracy and plausible completion are vendor claims, not independently verified
  measurements. Enterprise API is announced; it is not evidence of ordinary account
  access. Store prices depend on region/term and are not a production quote.
- Polycam [splat feature](https://poly.cam/tools/gaussian-splatting),
  [explicit mode/plan table](https://learn.poly.cam/hc/en-us/articles/27425185907348-How-to-Use-Object-Mode),
  [pricing](https://poly.cam/pricing). Prefer the explicit plan table over a “free
  tools” menu label; a seven-day trial is not ongoing free entitlement. Website price
  tables extracted as text may lose availability icons. Capture availability alone
  does not establish export access.
- Postshot [overview](https://www.jawset.com/),
  [camera/render guide](https://www.jawset.com/docs/d/Postshot%2BUser%2BGuide/Getting%2BStarted),
  [plan restrictions](https://www.jawset.com/shop/pricing/),
  [Windows builds](https://www.jawset.com/builds/postshot/windows/),
  [historical GPU requirements](https://www.jawset.com/docs/d/Postshot%2BUser%2BGuide/Release%2BNotes/v0.1.24).
  Extracted pricing showed zero values even for paid tiers; do not interpret these
  dynamic placeholders as a free commercial offer. Old GPU minima are not current
  compatibility evidence.
- Nerfstudio [repository/licence](https://github.com/nerfstudio-project/nerfstudio),
  [installation](https://docs.nerf.studio/quickstart/installation.html),
  [camera-path/render guide](https://docs.nerf.studio/quickstart/viewer_quickstart.html).
  No paid cloud compute or alternate Mac implementation selected.
- Splatframes [features, editions and requirements](https://splatframes.com/).
  Standard advertises editing/export; local training is a distinct Trainer entitlement.
  Vendor comparison charts are not our performance/quality evidence.

## Proposed bounded test — not started

**Trigger:** a selected film needs a camera move in a real location that existing
footage or the current photo-staging method cannot supply. First resolve a genuinely
available route under the owner's free/OSS/Mac-first policy. Existing subscriptions
can be considered; activating a renewing trial is a separate decision. None of this
list is currently qualified as a free end-to-end reconstruction route on this Mac.

1. **Capture:** one permitted static corner/room, modest footage/photo coverage,
   including a chair/doorway and two measured distances as scale references. Keep
   originals; avoid personal documents/people in any proposed cloud upload. Choose
   provider-compatible capture instructions before recording; define the desired
   virtual camera path so coverage serves the actual shot.
2. **Reconstruct once:** one tool, no parallel GPU jobs. Record input hashes, app/model
   version if exposed, settings, environment, observed time/resources, plan/cost and
   output. Set numeric duration/resource/retry limits in the trial card before launch;
   stop at the agreed bound or if required export is unavailable. No automatic paid
   upgrade or provider switching.
3. **Prove the handoff:** save/export the actual scene; reopen in the same tool or a
   confirmed compatible receiver. Retain format, scale/orientation and a 10–15s
   camera path. Change one camera key and render again without reconstructing. A
   browser share link alone does not pass reusable-scene handoff. Do not assume
   installed Blender can import/render the specific splat format.
4. **Review against a baseline:** compare with a direct captured move or existing
   photo-staging approach. Inspect stable architecture, holes/floaters, thin edges,
   reflections, invented areas, readable details, scale error and camera-path repeat.
   Require an artifact-free usable chosen shot, retained camera settings and a
   successful revised render; label any scale tolerance before the test. Log artistic
   preference separately from technical checks and actual cost/time.
5. **Optional fiction control, only after the basic pass:** put one existing character
   or proxy against the environment and test foreground occlusion, floor contact and
   lighting. A splat is not automatically a collision mesh, riggable object or relightable
   set. Use proxy geometry or a rendered background if needed; qualify only what passed.

Fallback: real footage, controlled photo-based camera staging or a simple existing
Blender set. A failed capture/export should not strand the film. Promotion requires
retained evidence and human review in the existing trial/project journal; otherwise
keep `documented`, `blocked` or `failed` rather than calling the tool production-ready.

## Reusable lesson to capture

Separate **observed location**, **inferred reconstruction**, **generatively completed
areas** and **added characters/effects** in provenance. For factual location films,
unseen generated detail is not evidence of how the real place looks. For fiction it
may be useful set dressing, with its origin retained. Metric-scale claims need a
measured control, not a visual impression. The same recorded camera/source contract
can later feed saved-shot/revision workflows, but no adapter is implemented here.
