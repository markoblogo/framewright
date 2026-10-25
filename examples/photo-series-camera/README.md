# Photo-series camera-plan component

Original renderer-independent camera sampler extracted from the private30s Pokras Lampas photo-series art study. The [workflow](../../docs/workflows/photo-series-cinema.md) separates source fidelity, layered reconstruction, shots, sound and QA. Owner accepted the picture and revised soundtrack; no general photo-to-video quality qualification is claimed.

`camera-plan.json` holds five end-exclusive shots in a30s24fps1920×1080 master. `camera-plan.mjs` validates contiguous timing, unique IDs, finite position/target triples and field of view. Call validation once before rendering; sample by absolute seconds for playback, seeking or deterministic frame capture. `scene` is a caller-owned scene key, not a provider/model ID.

```js
const plan = validateCameraPlan(yourPlan);
const shot = sampleCamera(plan, frame / plan.fps);
camera.fov = shot.fov;
camera.position.fromArray(shot.position);
camera.lookAt(...shot.target);
camera.updateProjectionMatrix();
// Render the caller's existing scene keyed by shot.scene.
```

Run the bounded data/seek checks with `node --test examples/photo-series-camera/test-camera-plan.mjs` from repository root. This component does not load photographs, segment subjects, generate missing views, add sound, render files, install runtimes or publish. Changing input photos still requires authored layout/mattes and quality review.

In the retained job, two native JPEG frames at9s and21.5s matched byte-for-byte before and after extracting the camera plan. This is same-environment component preservation, not a clean-machine, arbitrary-input or cross-GPU guarantee. Media/artist images and generated background are not redistributed here.
