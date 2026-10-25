# Photo series → cinematic scene: experimental reusable workflow

25 October2026. First bounded private case: a30s16:9 art study from six owner-supplied photos of Pokras Lampas’s Seals of Good Intentions. Owner accepted the picture, rejected classical piano as a mismatch, and requested a slightly Asian soundtrack. V2 preserves the accepted picture stream/timing exactly and replaces only audio; the owner accepted the revised soundtrack on 25 October 2026. The artist’s context is supplied by the owner, not an independently transcribed reading of the calligraphy. No agent upload or paid video job. The owner subsequently supplied a corrected publication URL after re-upload, recorded in the experiment case.

## Choose the route from the actual photos

Audit resolution, overlapping viewpoints, object silhouette, lighting, protected text/art and intended framing. A series of photos is not automatically a calibrated3D scan. Use a layered/proxy scene for shallow parallax and exact-source artwork; use genuine reconstruction only when geometry/access is available; use image-to-video when meaningful action/disocclusion requires it and budget/upload authority exists. Do not quietly substitute a zooming slideshow for requested scene movement.

For portrait → landscape, preserve the object’s proportions. Supply authored/generated surroundings with explicit provenance or agree a crop; do not silently stretch the source. In this case ImageGen prepared a wider clean gate environment from two supplied views. Original photographed scrolls were placed as independent shallow3D paper meshes; another original close-up supplies the ink detail. Remaining views inform framing and paper-tip reference; not every photo becomes a separate slide.

## One project, five connected layers

1. **Source/identity:** pin original files and artist/context. Keep photographer/artwork/publication rights separate from owner-supplied access. Do not invent translations of decorative calligraphy or claim recreated surroundings are documentary footage.
2. **Scene:** identify background, protected subject, silhouette/matte, depth, anchors and free-moving regions. Retain original artwork pixels where fidelity matters; generated clean background does not license repainting the artwork. In this case top edges stay anchored and free paper ends move gently. Geometry/matte are approximate.
3. **Shots:** put duration, scene/asset IDs, camera start/end, target and lens in a [camera plan](../../examples/photo-series-camera/README.md). Validate exact contiguous coverage and use absolute time. Camera moves, close inserts and motivated cuts serve one visual story; transitions are not its main content.
4. **Sound:** keep music/environment/effects stems on the same timeline, with source credits and finite fades. Stylised field recording or designed city-like ambience is not original location audio. Verify input sample rate, common headroom, relative alignment and mono behaviour before mastering/muxing.
5. **Review/handoff:** inspect final encoded video, cut boundaries, protected artwork, edges/disocclusions, readable credits and sound. Full decode/count/loudness/correlation do not replace viewing/listening. Keep representative sample, failed attempts and owner response in the existing production journal.

## Findings from the first private pass

| Failure or risk | Correction / retained limit |
| --- | --- |
| Dark ink touching paper edges truncated a simple red contour | Use a local-row edge envelope; contour remains approximate and needs viewing |
| Unsigned image arithmetic could overflow in colour tests | Promote analysis data to a signed type or use bounded channel comparisons |
| Linear render-target values displayed too dark | Apply output colour-space conversion in the final shader pass |
| Portrait detail plane exposed side gaps during a landscape move | Enlarge source coverage and inspect encoded camera extremes; do not fill with hidden black bars |
| Scene-specific camera values trapped reuse in one script | Extract a validated absolute-time data component; compare retained native frames after extraction |

## Evidence and qualification

Retained local final:30.000s,720frames,1080p24,H.264/AAC stereo48kHz; full decode passes. Final audio−22.0LUFS/−5.27dBTP and zero-offset master correlation0.999984. Both stems start at sample0; measurements do not establish emotional/audio quality. Original photos remain hash-identical. One generated environment plate was used; no chargeable cloud video job or new subscription was launched. Agent effort, generation cost under the existing app entitlement and audience results were not measured.

Two native frames, a close-up at9s and a wider view at21.5s, matched exactly after camera extraction. The code component has narrow timeline/seek/invalid-input tests. That evidence qualifies preservation in this job, not automatic segmentation, full3D reconstruction, photorealistic arbitrary-photo animation or cross-runtime pixel identity.

Music-revision finding: generic art-associated piano can pass meters yet fail the object’s mood. Retain picture acceptance separately from combined video/audio receipts. V2 uses a documented CC0 bell-toned electronic ambient excerpt, quiet original pulse and the retained environment, with−22.04LUFS/−8.59dBTP and full decode checked. Exact attribution and excerpts remain in the private production. The owner accepted this fit; it is not verified traditional instrumentation.

Accepted case and local publication kit: see [the experiment](../experiments/photo-series-cinema.md). The useful next gate is a second materially different photo series before calling the method general. Do not publish source photos, artist media, prompts/metadata or a new public example without the relevant scope/rights review.
