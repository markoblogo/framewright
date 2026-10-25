# Nantes: an illustrated mapped journey

25 October 2026. [Owner-supplied YouTube link](https://youtu.be/kh-MTl8K5pE) ·
[Retained export and QA](../../experiments/2026-10-25/evidence/nantes-pixel-journey.json).

An 82-second, 1920×1080/24 fps French travel film combines actual mapped route
geometry with Pixel Path's pseudo-3D road renderer and original animated airport,
Tour LU and castle illustrations. It is an illustrated journey, not photographed
streets or turn-by-turn navigation. Edited route excerpts do not imply travel time.

The route runs 11.1 km from the mapped airport terminal taxi rank to Tour LU.
French captions and seven local Supertonic3 guide phrases accompany the journey.
A separate original Breton-inspired score uses one retained CC0 harp sample;
voice/music remain separate and music ducks around the guide.

## Reusable method and limits

Verify route anchors → retain real map sources → load both route chunks → capture
at canonical absolute times → include DOM captions/attribution → add explicit
landmark illustrations → mix separate voice/music → decode and review the master.

[Pixel Path](https://github.com/jonwheatley/pixel-path) was retained at revision
`74341a96bb81e95aa62137b435512c91d7355301` (MIT); no upstream skill was installed.
The filming fork corrected history-dependent lane easing and unnamed-landmark
handling. Overpass failures were resolved with real OSM extracts. The rejected
airport-centroid route was replaced with the mapped terminal taxi rank.

Full decode passed: 82 seconds / 1,968 frames. Four paired frames matched on the
retained run; an earlier failed repeatability attempt remains recorded. This does
not qualify arbitrary routes, landmark fidelity or engine-wide deterministic capture.
French pronunciation, final listening and continuous artistic review remain
unrecorded. Pre-AAC normalization measurements are not encoded-master loudness.

Map attribution: [OpenStreetMap contributors, ODbL](https://www.openstreetmap.org/copyright).
The [CC0 harp recording](https://freesound.org/people/tarane468/sounds/347626) is by
tarane468. Other retained references include [OSRM](https://project-osrm.org/),
[Terrain Tiles](https://registry.opendata.aws/terrain-tiles/) and
[Wikidata](https://www.wikidata.org/). Private map/media/source archives are not
redistributed. No paid generation ran.

Publication is owner-reported. Public/unlisted visibility, uploaded-byte identity,
platform metadata and audience performance have not been independently verified.
The proposed Nantes green-line walking film remains a separate, unstarted production.
