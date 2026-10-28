# Seals of Good Intentions: a photo series used as a cinematic set

25 October 2026. A 30-second horizontal art study of Pokras Lampas’s calligraphic installation. The owner accepted the picture, requested a music change, then accepted the revised soundtrack. The owner supplied the correct [YouTube publication URL](https://youtu.be/6c3JXdIiosg) on 25 October 2026 after re-upload. The prior URL is withdrawn and retained only in history. The English local kit and accepted final remain unchanged. Publication is owner-reported; visibility, uploaded-byte identity, monetization and audience results have not been independently verified.

## What was actually made

Six supplied portrait photographs supported one authored shallow 3D/2.5D set. One original photograph supplies three calligraphic paper textures; a closer view supplies the ink insert. Two supplied views guide an ImageGen-prepared clean/wider background. Other views guide framing, lighting and paper-tip reference. Protected ink is not regenerated. The five shots approach the gate, inspect ink, follow free paper ends, move across the three scrolls and retreat to a minimal artist credit. This is a reconstruction, not photogrammetry or newly recorded documentary footage.

The [workflow](../workflows/photo-series-cinema.md) and [camera component](../../examples/photo-series-camera/README.md) can be reused. Contiguous data-driven shots and absolute-time camera sampling were extracted from the working scene. Two same-environment frames matched byte-for-byte after extraction; ten timeline/seek/invalid-input tests pass. The component does not segment arbitrary photographs or automatically stage a new scene.

## Revisions that mattered

- Dense black ink broke a naive red contour, and unsigned channel arithmetic overflowed. Bounded signed comparisons plus a local-row contour envelope improved the matte; the boundary remains approximate.
- Linear render-target output looked too dark; explicit output colour conversion corrected it. A macro plane exposed side gaps in landscape framing; increasing source coverage corrected them.
- Generic soft piano passed technical checks but the owner rejected its mood. A documented CC0 bell-toned electronic ambient excerpt, quiet original pulse and retained night environment were accepted instead. No claim of authentic traditional instruments or original Bangkok location sound is made.
- Picture approval was retained separately. The replacement soundtrack was muxed without re-encoding the approved picture; coded video hash and every video packet timing/size/flag match v1. Sound acceptance belongs to v2, not to the superseded piano mix.

## Retained evidence

| Output / check | Result |
| --- | --- |
| Final | 30.000s, 1920×1080, 24fps, 720 frames, H.264/AAC stereo 48kHz; full decode passes |
| Audio | −22.04LUFS, −8.59dBTP; zero-offset encoded/master correlation 0.999807 |
| Mono | RMS change −3.09dB, stereo correlation −0.018; numeric scope only; owner listening separately accepted |
| Picture | Original inputs hash-unchanged, five encoded samples viewed, owner accepted; v2 coded stream/timing unchanged |
| Cover | Final frame at 21.500s, resized to 1280×720 PNG; 1,289,213 bytes; viewed full and at 320px; no added lettering |
| Local kit | Byte-identical accepted MP4, English title/description/tags, optional authored descriptive SRT, credits and manifest; separate files, no ZIP |

[Output registry](../../experiments/2026-10-25/outputs.json) and [bounded evidence](../../experiments/2026-10-25/evidence/photo-series-cinema.json) retain hashes and scope. Original photos, generated plate, private journal, runtime and binary media stay outside Git. Owner approval of picture/music is separate from later approval of the new copy/cover, publication and audience response.

## Sources, rights and cost

Artist/context comes from the owner-supplied artist account: the first “Seals of Good Intentions” work, leftover paper/ink during a Bangkok studio farewell, and wishes left by the gate. No independent reading or translation of the decorative calligraphy was attempted. Photographer identity and publication permission for supplied art/photos are not independently established. A prepared local package does not resolve them or establish artist endorsement.

V2 music: [“Lotus music.wav” by nemaavla](https://freesound.org/people/nemaavla/sounds/507957/), CC0 1.0; preview source, 40–70s excerpt, filtering, fades and level. The download was bounded, provenance/hash retained and exact attribution copied. Environment: felix.blume’s CC0 night field recording reused from retained sources, plus original electrical/air/paper/pulse textures. V1 piano is absent from v2.

One built-in ImageGen environment edit ran; its entitlement cost was not independently measured. No chargeable cloud video/audio job, subscription, agent upload or new release ran. The owner subsequently re-uploaded and supplied the corrected publication URL above. Full effort, comparative production speed and audience impact are unknown.

## Next useful proof

Apply the same source audit → protected layers → staged camera plan → coordinated sound → separate picture/audio approval → local handoff to a materially different photo series. Retain its own geometry, continuity and rights checks. This accepted case supports a scoped production method, not automatic cinematic quality from any photographs.

## Follow-up: photo-to-film breakdown and executor trial

On 27 October 2026 the owner accepted a 131.875-second English breakdown of this
case and supplied its [YouTube link](https://youtu.be/JDjvazj9zb4). Publication is
owner-reported; uploaded-byte identity, rights and audience response remain separate.
The first sequential-executor production trial decoded the retained 30-second source
and saved a technical report in the local project journal. It did not edit the video
or determine artistic quality: montage was performed separately and the owner reviewed
it. The practical gap is explicit task/output setup and carrying the report into the
next decision; any editor adapter remains untested.

On 27 October a later local executor trial created a four-second review proxy from
the breakdown's retained master (requested 42–44 s, with one second of context on
each side). The file decoded and one frame was inspected; listening and owner review
are pending. The source and proxy are separately pinned; this demonstrates bounded
preview creation, not an edited correction or automatic artistic evaluation.

The subsequent sequential-executor comparison trial used the original piano version
and accepted soundtrack revision as distinct retained sources. It prepared 9–13 s
before/after clips around the 10–12 s request, source-pinned report and keyframes.
Both files decoded and matching keyframes were visually inspected; no new listening
or preservation approval was recorded. The existing revision tool performed the
comparison under the executor's project and host locks. This is a real-source
integration trial, not an automatic judgment or a new film release.
