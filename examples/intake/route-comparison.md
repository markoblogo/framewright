# Production route comparison

Bounded recipes for picture, optional narration and finishing. No music, subtitles, delivery kit or complete creative production inferred.

| Route | Picture / voice / finishing | Provider fee | Coverage | Main tradeoff |
|---|---|---|---|---|
| Pinned local Blender shot | blender / supertonic3 / ffmpeg | 0 USD local software fees; total unknown | gaps_require_resolution | Requires a prepared saved-shot card and installed Blender; scene creation and full-film approval are separate. |
| Locally authored motion | hyperframes / supertonic3 / ffmpeg | 0 USD local software fees; total unknown | documented_components_only | Authoring work required; not photorealistic generative motion. |
| Local supplied-media montage | ffmpeg / supertonic3 / ffmpeg | 0 USD local software fees; total unknown | documented_components_only | Requires suitable source media; motion from stills is limited. |
| Quota-generated picture | pixverse / supertonic3 / ffmpeg | Unknown / check quota or eligibility | gaps_require_resolution | Retries, continuity, export and actual operation affordability require a bounded trial. |
| Conditional-licence authoring | remotion / supertonic3 / ffmpeg | Unknown / check quota or eligibility | documented_components_only | Confirm Free/Company eligibility and selected paid features; no price inferred. |

## Pinned local Blender shot

Restore an existing trusted scene, render a bounded frame range, then finish locally.

- picture: blender; {"video-export": "unknown"}
- narration: supertonic3; {"narration": "tested"}
- finishing: ffmpeg; {"concat": "tested", "media-mux": "tested"}

Unresolved:
- picture: required capability needs a trial
- Installed runtime, hardware fit and available disk
- Asset/output rights and required attribution or disclosure
- Cross-tool timing, formats and final human viewing/listening

## Locally authored motion

Author layout, camera-like movement and graphics from supplied materials.

- picture: hyperframes; {"video-export": "tested"}
- narration: supertonic3; {"narration": "tested"}
- finishing: ffmpeg; {"concat": "tested", "media-mux": "tested"}

Unresolved:
- Installed runtime, hardware fit and available disk
- Asset/output rights and required attribution or disclosure
- Cross-tool timing, formats and final human viewing/listening

## Local supplied-media montage

Arrange supplied clips or stills, then mix voice and finish.

- picture: ffmpeg; {"video-export": "tested"}
- narration: supertonic3; {"narration": "tested"}
- finishing: ffmpeg; {"concat": "tested", "media-mux": "tested"}

Unresolved:
- Installed runtime, hardware fit and available disk
- Asset/output rights and required attribution or disclosure
- Cross-tool timing, formats and final human viewing/listening

## Quota-generated picture

Generate selected shots, then edit locally.

- picture: pixverse; {"video-export": "unknown"}
- narration: supertonic3; {"narration": "tested"}
- finishing: ffmpeg; {"concat": "tested", "media-mux": "tested"}

Unresolved:
- picture: required capability needs a trial
- Current plan terms and account balance
- Credits per selected operation, retries and reset; calendar estimate unavailable
- Installed runtime, hardware fit and available disk
- Asset/output rights and required attribution or disclosure
- Cross-tool timing, formats and final human viewing/listening

## Conditional-licence authoring

Author frame-driven scenes, then mix voice and finish.

- picture: remotion; {"video-export": "tested"}
- narration: supertonic3; {"narration": "tested"}
- finishing: ffmpeg; {"concat": "tested", "media-mux": "tested"}

Unresolved:
- Licence eligibility and provider fee quote
- Installed runtime, hardware fit and available disk
- Asset/output rights and required attribution or disclosure
- Cross-tool timing, formats and final human viewing/listening

Questions: None

Time and total cost remain unknown. Tool selection and execution need a separate decision.
