# PHYSICS-CHAIN-01 · Same ID, Twice

24 November 2026. Radar #9 tests whether an authored 3D shot can read out
recorded sphere motion and a gate contact while keeping the two input
conditions identical apart from the height of the gate. This extends the
existing [physics-backed explainer method](../methods/physics-backed-research-explainer.md)
from friction to a bounded contact shot.

MuJoCo 3.17.0 generated 120 states at 30 fps per condition on Apple Silicon,
at ten simulation steps per frame. Both conditions reused radius 0.23 m and
the same initial position, linear and angular velocity. Two runs per
condition matched at the stored precision (eight decimals in pose arrays).

| Gate | First contact with gate | Maximum sphere-center X |
| --- | --- | --- |
| Raised | None | 2.95901502 m |
| Closed | 1.300 s | −0.16097448 m |

The goal plane was X = 0. The closed condition never reached it. Three.js
r187 rendered the recorded translations and quaternions, using authored
lighting, framing and gate transition. The 246-frame insert decoded as
1280×720, 30 fps and 8.2 s. The 3D shot is a visual analogy for a separate
sequential, synthetic queue replay. The physics engine did not process
GitHub events and the GitHub service was not connected. Longer chains,
cross-machine reproducibility, owner evaluation of the full cut and
production time savings are unmeasured.

Private evidence is under `productions/render-complete-events-2026-11-24/`:
`full/simulate.py`, `full/physics.json`, `full/physics-scene.js`,
`full/physics-insert.mp4` and `pilot/replay-result.json`.
