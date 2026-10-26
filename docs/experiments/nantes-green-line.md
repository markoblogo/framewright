# Nantes green line: walking, full-route map and pixel/detail transitions

25–26 October 2026. [Owner-supplied YouTube link](https://youtu.be/IQ3CdzPzFHw). A separate 100-second, 1920×1080/24 fps French illustrated
walking film. The owner accepted the overall first preview, then identified muddy
pixel resolution. The clarity revision preserves timing, route, voice and music;
world granularity changes from 8 to 4 pixels, bloom from .32 to .12 and facade
textures use nearest sampling. Delivery and owner review are distinct.

## What the film shows

Selected eye-level scenes: station, Jardin des plantes, Musée d’arts, cathedral,
Château des ducs de Bretagne and Tour LU. A visible green line guides the camera;
it turns to landmarks, whose generated detailed interpretations appear briefly
before the world returns to pixels. French local Supertonic3 F1 guide, original
Breton-inspired score, speech ducking and original walking/transition cues remain
separate layers. A text-bearing thumbnail and loose FR/EN YouTube metadata kit are
prepared locally. Publication is owner-reported; audience results remain unknown.

Whenever a map appears, **the entire geometry supplied by the official route map
is shown**, not just the film’s six stops. The partial OSM relation 19355322 was
rejected as a full-route source. All 13 official LineStrings / 371 vertices were
retained and independently compared to both scene inputs; projection checks keep
all vertices inside the map. The map credits Le Voyage à Nantes and OSM. The
walking footage remains selected, illustrated excerpts rather than continuous
navigation or a claim about actual walking time.

Sources: [official route](https://www.levoyageanantes.fr/les-parcours/arpenter-la-ligne-verte/),
[official interactive map](https://www.levoyageanantes.fr/wp-content/themes/levoyageanantes2026/map/cartographie_parcours.php?id=9885&lg=fr),
[OSM attribution](https://www.openstreetmap.org/copyright),
[CC0 harp](https://freesound.org/people/tarane468/sounds/347626/).
Raw map extracts, generated media and provider HTML are private production assets,
not redistributed here. No Google/Carto tile key is used in the film.

## New bounded experiments

- **pmndrs postprocessing 6.39.5 / Three.js 0.186.0:** timeline-driven
  PixelationEffect and restrained BloomEffect. The attempted 6.39.2 pairing failed
  its peer dependency range; this was resolved with a compatible pinned version,
  without force-installing. Same-instance canvas replay passed exact hash pairs
  at 19→10→19 and 25.5→78→25.5 seconds. This excludes DOM overlays, audio,
  different devices and arbitrary effects. It is not qualification of CRT or all
  VFX in the library.
- **Architectural-exploration prompt:** adapted the queued MIT reference
  `lexnlin-241739` ([pinned library data](https://github.com/yihui-dev/awesome-opus5-5-videos/blob/92aee2f586ac0715cb3cbcb6384834f98a33383d/data/videos.json))
  to a real named itinerary. No upstream code was copied. OSM footprints supply
  context; landmark models, inferred heights and generated image interpretations
  remain approximate and labelled. This does not establish an exact city twin.

## Reuse and checks

[Original asset-dependent scene](../../examples/nantes-green-line/README.md) retains the
camera/effect timing and pinned dependencies without shipping media or upstream
runtime code. Follow the same chain: verify complete map coverage → retain source
geometry → author eye-level excerpts → deterministic landmark turn/resolve/return →
record from the timeline → add separate guide/music/SFX → decode the final file.
Do not substitute a partial route while claiming a full overview.

Both the first preview and sharper delivery revision fully decoded: 100 seconds / 2,400 frames, H.264 picture
and AAC stereo. AAC packet hashes match between revisions. Fourteen encoded stills were inspected. Native composition checks
passed after the test entry page was moved outside the film root. Canvas-only
motion triggered DOM-based dead-stretch warnings; separate replay/encoded checks
are retained. Fine-print attribution remains below the checker’s mobile reading
floor; main headings are larger. Owner overall acceptance does not independently
prove French pronunciation, continuous listening, public visibility or performance.

[Evidence](../../experiments/2026-10-26/evidence/nantes-green-line.json) records
revision hashes, delivery checks and the owner-supplied publication URL. Uploaded
bytes, playback and visibility have not been independently verified. Publication
does not add a separate pixel-clarity or focused listening receipt; audience
results remain unknown.
