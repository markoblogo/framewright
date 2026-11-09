# GLB Car Lab — named parts, controlled revisions, two formats

Closed 9 November 2026. Both 69.75s English films (24fps; 1920×1080 and
1080×1920) were accepted with sound. Owner supplied [YouTube](https://youtu.be/SrWeTSaQ4DQ)
and [TikTok](https://vt.tiktok.com/ZSpA8gYqf/). Provenance: owner_provided_url;
independent visibility, uploaded-file/cover identity, views and revenue remain unknown.
This is an owner-selected tool experiment, not a Radar recommendation; no Radar
handoff or audience result is claimed.

## Repeatable recipe

1. **Inspect before animating.** Retain a licensed GLB, upstream commit, attribution
   and hashes. Inventory nodes, meshes, names, hierarchy, materials and animations.
   Car Concept has 101 nodes, 97 meshes, four unnamed tire meshes inside named
   wheel groups and no ready animations. Mesh count is not a count of independent
   mechanical parts. Choose meaningful named groups, not arbitrary triangles.
2. **Preserve the source pose.** Load with pinned Three.js 0.180.0, normalise scale
   and ground placement, then save local position/quaternion/scale plus world
   positions of target parts. Add a pivot with world-preserving attach; choose the
   actual hinge axis. Names alone do not identify hinges or mechanical constraints.
   At every seek, reset all transforms before applying time-based movement. Convert
   world-space offsets into each parent's local space. Do not accumulate motion.
3. **Direct action, not just camera drift.** Separate/reassemble groups, deliberately
   show a labelled wrong axis, then correct one door while preserving the dashboard.
   Use a pure time/state function so the camera and parts can seek out of order.
   Keep text legible and actions visible through each section, with a final fade.
4. **Compose each aspect.** Use one scene and timeline, separate cameras and native
   1080p typography for each aspect. Capture 24fps WebGL frames directly into FFmpeg;
   avoid a retained frame sequence. Review both layouts and forward/backward seeking
   on the standard Range-capable localhost preview server before handing over.
5. **Sound, approval and delivery.** Keep measured English narration and a timeline;
   add original local pulse, stylised motor, servo sweeps and latches at events.
   Music ducks with a 45% floor rather than cutting out under speech. Check decode,
   dimensions, levels, sampled layouts, returns and non-target transforms; obtain
   full creative/listening acceptance separately. Render new covers with safe text
   for portrait grid crops. Retain English metadata, attribution and approximate SRT.

## Tested boundary and limitations

- Existing rigid 3D geometry, not video diffusion or a newly generated car; no
  physics, collision solver, engineering teardown, deformation, rig or contact claim.
- Return-to-source sampled world-position error was zero; the inspected dashboard
  matrix stayed unchanged. This does not verify every object at every possible time.
- Door revision then restoration reproduced the same JPEG within the loaded page
  in both aspects. Fresh-load strict JPEG equality passed portrait and failed wide;
  measured wide PSNR was about 89.56dB. Keep that failed strict test. Source transform
  restoration is supported; fresh-context bitwise rendering is not guaranteed.
- GLB-NAMED-01 has scoped choreography, reassembly, two views and targeted correction
  evidence. Material recolouring, modified-GLB export, meshopt decoding and independent
  user reproduction were not tested; do not mark the entire original test qualified.
- Timing uses measured narration duration and proportional phrase estimates, not
  forced alignment. SRT timing was not separately accepted. Both films measure about
  -18.32LUFS integrated / -3.94dBTP; levels do not substitute for listening approval.
- Original renderer uses installed Chrome/Metal and an existing shared Playwright
  path. Recheck those external dependencies on another machine; no portable bundled
  runtime is claimed. Retained voice/stems avoid needing another TTS generation.
- Inkling 2 Small/OpenCode was deferred, not executed; no Inkling result in this film.
  No paid generation/API, Blender installation, cloud-video route or performance
  improvement measurement was part of this production.

## Rights and evidence

Car Concept: Eric Chadwick / Darmstadt Graphics Group GmbH (2024), based on Unity
Fan's original model; [CC BY4.0](https://creativecommons.org/licenses/by/4.0/).
[Source at pinned commit](https://github.com/KhronosGroup/glTF-Sample-Assets/tree/8f492390ddc7a2ae221a1369ef560589cf8c70fb/Models/CarConcept).
Staging, lighting, cameras, transforms, type and covers were adapted; marks do not
imply affiliation. Attribution remains in both publication packages. Supertonic-3 M1
uses its retained BigScience Open RAIL-M licence; music/SFX are original local
synthesis. The motor is stylised, not an authentic recording of this car.

Private studio: productions/glb-car-lab. Sources, node inventory, full/motion.js,
scene.html, timeline.json, capture.cjs, sound.py, finish.py, voice/stems, final masters,
QA/journal and publication package remain external to Git. The four reopen images
retain the exact-render limitation; the two accepted short pilot masters retain
approval/continuity reference and are not assembler inputs. Their explicit retention
is bounded evidence, not a policy of keeping every draft.

Closeout dependency inventory, retired hashes and deletion receipt live in closeout/.
Silent exports, scratch mixes and redundant check images can be recreated by the
retained scripts; they are unavailable after sanitation. Historical render receipts
preserve their hashes, not continued local availability. Rebuilding changes outputs
and requires fresh QA/acceptance. No new film generation, commit, PR or release is
implied by this closeout.
