# Physics-backed research explainer

A bounded R04/R05/R09 method from [Real2Sim](../productions/real2sim-twins.md), 6 November 2026. Use when a research claim benefits from an original, small controlled physical example. This is not a general robot-reconstruction route.

## Recipe

1. Freeze the audience, English script and 90–120s horizontal scope. Separate the primary source's demonstration from the experiment the studio can actually perform. Approve three direction boards, then a short moving pilot.
2. Specify one controlled variable. In this case: identical0.24m cubes,0.25kg mass, initial horizontal velocity1.25m/s; change cube friction0.05→0.80. Both run on the same plane, gravity and timestep. Initial speed represents a common initial condition, not a measured applied-force pulse.
3. Compute and copy positions/quaternions from MuJoCo3.17.0 on CPU. Assign initial state only; subsequent trajectory comes from `mj_step`. Run3seconds at0.002s steps; two independent repeats per setting agree in position within absolute1e-12. Repeatability is not real-world accuracy.
4. Render original diagrams from those states. Keep camera movement and explanatory robot-arm kinematics separate from calculated object dynamics. Use rotated surface normals and visible-face selection for solid rotating cubes; fixed face lists can make a rotating solid appear open.
5. Measure local narration phrases before arranging scenes. Keep the quiet original sound bed audible under speech. Use explicit replays instead of silently speeding up or freezing a still-moving simulation. Introduce parameters and comparison questions progressively; don't fabricate measured force curves.
6. Review the moving pilot, then the complete encoded film with sound. Test forward/backward native seeking on the standard preview server. Freeze the accepted master before preparing a cover, captions and source-qualified copy.

## Presentation decisions

The accepted direction uses charcoal, large cream type, lime/purple comparison accents and coral cubes. The exact hidden parameter is revealed after the opening outcome. Labels belong high in the frame; bottom provenance is supplementary rather than necessary explanation.

An authored page compressed into the background was tried and rejected as unclear. The correction directly reveals the two required checks. Preserve this negative result; a successful render did not qualify PAGE-TO-SCENE-01. Do not repeat it unchanged as a proven technique.

## With and without Framewright

With Framewright: use one schema2 project for the brief, approved boards/pilot, retained outputs, exact-version technical/listening/creative observations and selected master. Bind an owner-selected Radar card before production when available; return the owner-reported publication with source provenance. Keep private sources/media outside Git.

Without Framewright: maintain a folder with the frozen brief/script, source links and claim limits, experiment XML/code/states, voice timings, scene list, editable renderer, versioned output hashes and explicit review decisions. Assemble with an available renderer/FFmpeg, use a range-enabled local player, and deliver the same MP4/JPG/SRT/copy kit. This alternative is written guidance, not a separately completed reproduction.

## Boundaries and next suitable test

- The demonstrated scope is cube/plane friction on one Mac/runtime. Native MuJoCo graphics, real camera reconstruction, robot control, tactile-force calibration and arbitrary material accuracy remain untested.
- Equal initial speed is not equal measured impulse. Mass, inertia, collisions and joints in the film are explanatory concepts; only the friction contrast has calculated toy dynamics.
- Sentence subtitle timing is estimated from measured phrase duration and word proportions, not forced alignment. Check reading/sync separately when dialogue becomes denser.
- Render wall time excludes scripting, review, TTS setup, editing and waiting. No measured labour saving, audience gain or monetisation result follows from this case.
- Next test only when needed: a small contact task with a known reference measurement, or native MuJoCo rendering on this host. Neither is started by this recipe. An independent receiving operator must actually use/resume the route before REL-D/M6 can close.
