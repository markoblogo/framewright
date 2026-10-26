# Rokehan: a Nantes quarter as a manga camera set

26 October2026. Owner authorised one local manga-style test, following tool review.
**Technical trial passed; owner accepted the lighter-street v2.**15s,1920×1080,
24fps, intentionally silent. No upload, publication, paid call, account grant or
software installation. This is a test export, not another published film or a
change to the39-final-export registry. [Receipt](../../experiments/2026-10-26/evidence/rokehan-manga.json).

## Native output versus our finishing

In Location Scout beta, opened Nantes47.2162,-1.5491, near300m/far2km, chose Lines+
tone and central-street eye level,24mm. Saved a native2400px-long-side PNG and GLB
through public export controls. One export retried to obtain a usable browser
local download path; no bulk download or upstream-program extraction. Native
preview automatically enabled low-spec settings. PNG was independently inspected.

GLB contains40 mesh definitions and431 loaded mesh instances (~9M vertices summed
per draw instance), colour materials and detailed windows/trees/street objects.
It contains no camera or native manga shader. The selected far preview does not
prove the2km surroundings were included in the model; model bounds are about414×358m.
The export's generator/copyright and source hashes are retained. Building heights
can be inferred by the service; actual Nantes accuracy is not qualified.

Blender was unavailable and was not installed. Imported the actual GLB into the
existing Three.js0.186.0 runtime; an original local depth/normal contour and halftone
shader restores a manga direction. **This is not native Rokehan video export or an
exact reproduction of its renderer.** The service's code/shaders were not copied.
0–7.5s: overhead orbit/dolly around the castle;7.5–15s: street dolly. Both views use
the same exported set, so this tests reusable geometry rather than a pan over PNG.

## Checks and retained limits

Chrome155.0.8059.86 captured360 frames; FFmpeg8.0.1 encoded H264/yuv420p. Full decode:
15s/360frames. No page errors; repeated seeks at frames72 and240 matched pixels.
Source GLB unchanged. Representative encoded frames72/180/359 show architecture,
parallax, title and attribution. No full-frame black/freeze event detected; largest
mean-luma change aligns with the intended cut before180. Measurements do not prove
absence of fine-line shimmer or comfortable motion. Render capture measured35.647s
in this run, excluding preparation; no comparative efficiency claim.

Owner accepted the revised sample; this is a scoped preference observation, not a general temporal-quality guarantee. Static people/cars, untested
Blender import and lack of audio remain explicit. No real-time FPS benchmark,
character animation, second location, geographic-fidelity guarantee or production
promotion. Fine foliage and halftone sampling warrant review at delivery size.

## Reuse and rights

Retain the native GLB/PNG, original renderer/camera source, source pins, encode and
QA in one production journal. A second angle worked from the same set. [Procedure](../../skills/video-production-router/references/location-scout.md).

Terms allow output inside works including commercial video with map-data credit:
OSM and OpenMapTiles as applicable; preserve elevation credit. Exported files must
not be redistributed as standalone or lightly modified asset packs. Media/models
remain private and outside Git; no upstream source is vendored. The service is
free without registration at review time; its version/availability can change.

Sources, viewed26October2026: [tool](https://tools.oyasumi-gamedev.com/rokehan/),
[author guide](https://oyasumi-gamedev.com/tools/rokehan/),
[terms](https://oyasumi-gamedev.com/tools/terms/).

## Street-brightness revision

Owner liked the manga result but found the street dark. Kept v1; v2 lifts only
the street interval7.5–15s before halftoning, preserving the black edge treatment.
Camera samples/timing match; first-shot frames0/72/179 are byte-identical native
captures. Full v2 decode15s/360frames and reseeks72/240 pass. Frame240 inspected:
facades/shadows lighter, lines and credit retained. Existing precise-revision
module retained a source-bound change request and before/after context clips.
This is the same15s trial, not another published export. Owner subsequently accepted v2 (owner report: “да ок”).
