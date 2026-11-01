# Abstract reward-cycle insert

Original Good Dog scene, Three.js r186 (MIT dependency, not vendored). This is a non-diegetic process explanation: FIND→REWARD→REPEAT, then a dog-paw controller links to the reward. Tokens move along a repeatable path. It deliberately differs from canonical factory architecture.

Supply an approved localThree.js r186 distribution alongside index.html, including its relative imports. Do not infer that dependencies are installed in another checkout. No automatic install or external model/API. The production used an existing trusted Chrome/FFmpeg frame renderer:1280×720,24fps, frames0–143, window.sceneReady then window.renderAt(frame/24). This example exposes those scene hooks, not a standaloneCLI or the complete FramewrightCapture controller.

Reusability controls are in scene.js: node positions, labels and label width, CatmullRom token path, palette, control appearance at3.5–4.4s, and camera. Retain a new version after changing any of them. Source video/audio not needed for this original scene.

Observed production result:144frames/6s rendered, no page errors, three identical reseeks;v1 labels crowded,v2 separated controller and enlarged text. Full decode and owner review remain independent. This is kinematic motion, not physics, a validated model of dependency or a new renderer qualification. Sound intentionally absent for the visual trial.
