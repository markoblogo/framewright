# Tripo: rig and reusable text-generated action

Reviewed 2026-10-26. Owner-selected **active candidate for a short bounded test**:
one cleared character → rig → 5–8s motion → export → playback from two cameras.
Start with a simple humanoid. A dog for Good Dog is a separate subsequent stage;
this decision does not start that production. No upload, account setup, installation,
generation, export or paid test has run. Source character and action remain unselected.

## Documented scope

[Official Rigging & Animation article](https://www.tripo3d.ai/blog/rigging-animation)
describes full-body/hand bones, five humanoid presets (UE5 Mannequin, Mixamo, VRM1.0,
Unity Humanoid, ActorCore), 1–10s Text to Motion and up to five motion segments in a
sequence. Humanoid input should be T/A pose and at most100000triangles. Non-humanoids
use the separate v2.5 algorithm without engine-specific presets; humanoid motion
generation support must not be inferred for dogs or other creatures.

The article quotes20Studio credits per rig and20per generated animation, with free
library presets. These are dated documented prices, not an approved budget or total
cost: initial model creation, multiple segments, retries, exports and plan entitlement
must be quoted separately. [Studio pricing](https://www.tripo3d.ai/pricing) currently
labels Free models public/noncommercial and paid plans private/commercial. No public
or monetised use is cleared by free credits. [Developer API](https://developers.tripo3d.ai/)
has separate endpoints/pricing; Studio Text to Motion does not establish identical
CLI/API feature availability or tariff. Verify the actual selected interface first.

[Auto-rigging feature page](https://www.tripo3d.ai/features/ai-auto-rigging) advertises
exports, but the actual FBX/GLB must retain skin, skeleton, actions and materials in
the receiving renderer. OBJ alone is not a skeletal-animation handoff. No remapping
or production-ready claims have been tested here. Facial-expression generation,
speech/lip sync and animal gait quality remain unconfirmed.

## First test and pass conditions

1. Choose an original or cleared simple humanoid and a short action; check topology,
   pose, scale and the receiving renderer. Review actual upload/privacy/output rights,
   current account/plan, credits and per-step quote before upload or spending. Keep
   model/service versions, prompts and actual costs/attempts in the journal.
2. Rig once, then generate5–8s motion. For a staged action such as walk→turn→stop,
   check availability and cost of each segment before submitting; do not assume one
   price covers a sequence. Keep the exported editable action and original model.
3. Import actual rig/action into the selected existing renderer and play it from
   two cameras. Inspect skin deformation at shoulders/elbows/knees/hands, penetrations,
   foot contact/sliding, real root travel versus walking in place, rotation and stage
   joins. A second view is a plausibility test, not ground-truth motion recovery.
4. Save/reload and reuse the same retained action in another shot/camera without
   regenerating. Verify clip duration, materials, scale, root-motion interpretation,
   repeatable time samples and decoded output. Viewing/creative approval and technical
   checks are independent. If sound is added, review it separately; model movement
   alone does not qualify narration/audio. Preserve defects and manual repair effort.

An acceptable result supplies an editable reusable action with credible deformation,
contact and travel across two views; not merely a successful export. A dog requires
its own compatibility/rig/action trial and evaluation of spine, paws, jaw and gait.
Do not use a humanoid pass as animal/facial/lip-sync qualification.

This direct Tripo action route complements the earlier
[video-guided rig research](video-guided-rig-animation.md). It neither reproduces the
external shark demo nor proves motion can be reconstructed exactly from an MP4.
No upstream code, private media, generated models or account data enter Git; no
automatic runtime provider is added by this research record.

[Queue](../experiment-queue.md) · [Inventory](../tool-research.md).
