# Motion-studio libraries: assessment, 26 October 2026

Scope: user-supplied shortlist, compared against Framewright's current records. This is research, not a record of installation or a successful production trial. Prioritise free/open-source Mac-compatible tools; check the exact version, dependencies, model weights and licence before use. No cloud upload or paid test is implied. Repeatable offline rendering, frame timing and the delivered media matter more than an interactive demo.

| Tool and primary source | Role | Project disposition |
|---|---|---|
| [Remotion](https://github.com/remotion-dev/remotion) | React video | Already used in productions; retain. Source available under a special licence, **not blanket open source**; company/use eligibility and paid features must be checked. |
| [HyperFrames](https://github.com/heygen-com/hyperframes) | HTML-to-video | Already used; retain current verified scopes. |
| [OpenCut](https://github.com/OpenCut-app/OpenCut) | Editing | Candidate: compare one revision/export with the current edit workflow. Upstream says the main project is being rewritten; classic is the existing version and headless/MCP are planned. Inspect the chosen version, Mac/local availability, import/export and terms first. |
| [OBS Studio](https://github.com/obsproject/obs-studio) | Screen capture | Candidate comparison for a real narrated screen walkthrough; distinguish an existing record from an OBS-specific trial. |
| [FFmpeg](https://github.com/FFmpeg/FFmpeg) | Media processing | Widely used. Licence depends on build/configuration; verify shipped binaries and codec dependencies. |
| [Anime.js](https://github.com/juliangarnier/anime) | Timelines | Candidate for event-synchronised visual motion, compare with existing GSAP/HyperFrames. |
| [React Spring](https://github.com/pmndrs/react-spring) | Springs in React | Reserve for characterful UI; confirm deterministic seek/rerender before video use. |
| [GL Transitions](https://github.com/gl-transitions/gl-transitions) | Shader transition collection | Candidate for restrained transition between scenes; inspect the specific shader and renderer licence and attribution. |
| [tsParticles](https://github.com/tsparticles/tsparticles) | Particles | Candidate for dust, rain or sparks; test seeded repeatability and occlusion. |
| [PixiJS](https://github.com/pixijs/pixijs) | Web 2D renderer | High priority for layered 2D scenes with camera, depth and explicit asset animation; not a skeletal rig or a guarantee of natural gait. |
| [p5.js](https://github.com/processing/p5.js) | Generative imagery | Candidate for an original seeded background; compare complexity with existing tools. |
| [Paper.js](https://github.com/paperjs/paper.js) | Vector paths | Reserve for route tracing or hand-drawn motion; lower priority than existing graphics tools. |
| [Matter.js](https://github.com/liabru/matter-js) | 2D rigid-body physics | Candidate for believable object contact/fall, not a replacement for character rigging. |
| [Three.js](https://github.com/mrdoob/three.js) | 3D scenes | Already used; production results do not qualify every animation, asset or effect. |
| [Rapier](https://github.com/dimforge/rapier) | 2D/3D rigid-body physics | Candidate for contact and object interaction alongside Three.js; not a ready-made human or robot walk cycle. |
| [OGL](https://github.com/oframe/ogl) | Lightweight WebGL | Reference reserve for a concrete custom shader; compare against existing Three.js before introducing another renderer. |
| [glTF Transform](https://github.com/donmccurdy/glTF-Transform) | glTF inspection/optimisation | High priority for an authorised animated asset: compare size, appearance, skeleton, materials and animation before/after; preserve source. |
| [Chatterbox](https://github.com/resemble-ai/chatterbox) | TTS / voice cloning | Already in voice-candidate queue, not qualified by that listing. Probe only with owner's authorised voice and chosen local model; check Mac support, weights/terms, quality, time and per-use consent. No automatic upload. |
| [Tone.js](https://github.com/Tonejs/Tone.js) | Web audio synthesis | Candidate for authored film cues with repeatable timing and offline audio export; confirm browser support and source/render sync. |
| [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | Speech transcription | Candidate to compare against existing mlx-whisper: same authorised speech, timing, word errors, punctuation and Mac CPU time; inspect model/licence and diarization separately. Not automatic proof of caption quality. |

## Bounded tests when a fitting production is selected

1. **Character contact:** a licensed, genuinely rigged character, walk 5–8s across floor with start/stop. Evaluate foot planting, root speed, slipping and shadows at multiple frames; inspect actual render. Compare existing Blender route before optionally adding Rapier for loose props. Capture model provenance and modifications. Physics engines do not automatically animate a character.
2. **PixiJS + Matter.js:** 10–15s layered room with one falling parcel, grounded collision, reproducible camera and particles; two renders with identical seed and frame comparison. Log GPU/browser and capture costs. Choose either tsParticles or a simple built-in effect, and add a GL transition only if the shot needs it.
3. **glTF Transform:** original authorised rigged GLB → optimise a copy → compare visuals, bones and action frame counts plus file size; play the same action before/after. No destructive replacement of master.
4. **Audio and captions:** 20–30s authorised English voice → faster-whisper CPU versus existing mlx-whisper → side-by-side transcript, time, errors, manually corrected subtitles; optional Tone.js cue matched to an action and checked in encoded output. Chatterbox stays a separate consented voice test.
5. **Tool comparison when useful:** 15s actual edit in OpenCut or OBS and/or Anime.js against current workflow; track elapsed time, editability, export and Mac availability. Prefer a concrete gap over installing all 20.

Repeated first/last frame and actual pixel/audio inspection are required for deterministic captures. A local code licence alone does not cover downloaded music, voices, models or a hosted service. Existing subscription exceptions follow [owner policy](../production-guide.md#owner-preference-free-open-source-and-macos-first).
