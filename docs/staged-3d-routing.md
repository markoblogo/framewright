# Scoped staged 3D routing — 2026-10-15

Production evidence: [Spot-Market pilot](../experiments/2026-10-15/spot-market-3d-miniature.md).
New method `staged-3d-scene`, profile `three-scene`: original authored Three.js scene
inside Hyperframes, with local voice/audio/still layers. Anatomy scope remains
unchanged. Owner liked the new 3D picture and the narration. No render or release
was performed in this routing update.

## Selection and composition

Ask for `staged-3d`, `object-3d`, `object-motion`, `camera-travel`, miniature-diorama,
low-poly style or explicitly name `three-scene`. Available inputs: object, book-art,
brand. The activation gate prevents ordinary export/montage requests acquiring
unrequested 3D authoring. Full-chain tested coverage still ranks first; when equally
covered/sized, prefer the primary that owns more requested effects before style/default.
Explicit primary choices remain preserved. Another tool can supply missing layers,
but that does not certify a new combination.

Only 1920×1080/30fps is locally tested. Other canvas/fps downgrades this profile's
capabilities to documented/needs-test; strict tested briefs leave them unmet.
Calibrated physics remains unsupported. Do not infer geometry from a flat cover,
new native still/alpha/vertical output, automatic reconstruction or live data.

[Example brief](../examples/briefs/staged-3d-mixed.json) →
[actual planner output](../examples/plans/staged-3d-mixed.json):

```sh
python3 skills/video-production-router/scripts/plan.py examples/briefs/staged-3d-mixed.json
```

The plan is proposed, not executed: 20s 3D/Kokoro/FFmpeg block, 5s Flute UI and 5s Remotion
closing title. One FFmpeg master; the actual 30s timeline is 900 frames.
The output retains feature evidence, per-tool limits and required encoded integration
QA. This mixed film has not been rendered. The still is FFmpeg extraction, not a
new native-still capability of the 3D adapter.

## Verification boundaries

Eight deterministic selection regressions in `tests/test_plan.py` cover:

1. 3D action/camera plus tested local voice and extracted still.
2. Plain object/book/brand requests retain their ordinary choices.
3. Style-only miniature activation.
4. Explicit Anatomy primary stays explicit; 3D companion is a proposed chain.
5. Unknown calibrated physics stays unmet.
6. Vertical format marks 3D evidence as requiring a feature test; strict tested blocks.
7. 60fps is not passed off as tested.
8. Mixed 3D/Flute/Remotion blocks retain duration, ownership and integration limits.

Existing planner tests also cover requirement-order invariance, music-provider
boundaries and unsupported outputs. Qualification-state tests reject unrecorded
source changes and promotion of changed sources using old answers.
These are deterministic regressions, not fresh model trials or unseen scores.
The historical model packet remains intact; current source is explicitly
`not_evaluated_current_source` in [qualification](../router-qualification.json).
