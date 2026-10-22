# SSI logistics: illustrated demos and Openverse

Trial: 2026-10-19. Owner qualification: 2026-10-20. This private manual-report
pilot has no SSI data connection, recurring job or public media publication.
Media and the raw report are not included in this repository.

## Scope and outcome

One owner-supplied logistics report supported six 20-second, 1920×1080p30
alternatives for Telegram. No separate covers, subtitles or publication copy.

| Variant | Treatment | Sound |
| --- | --- | --- |
| A | Six editorial shots; Ukrainian commentary explains context rather than reciting the displayed numbers | Offline Supertonic 3 F1 narration |
| B | Ten kinetic headline/metric shots | No audio track |
| C | Eleven labelled comparison/callout shots | No audio track |
| D | Original miniature 3D port, grain handling, truck, rail and border queue; eight camera shots | Original instrumental score and admitted CC0 effects |
| E | Original light SVG transport story; ten shots | Original instrumental score and admitted CC0 effects |
| F | Original dark abstract 3D flow machine; nine shots | Original instrumental score and admitted CC0 effects |

D/E/F followed owner feedback that the initial treatments were too similar and
needed animated illustrations and sound. The owner praised the D preview and
reported sending all six variants to partners on 2026-10-20; personal favourites
are D and F. These are owner preferences only; partners later did not accept the
weekly-report treatments (22 October owner report). A new specification is pending.

HyperFrames 0.8.174, GSAP, Three.js r186 and local FFmpeg were used. Animation and
cameras use deterministic absolute time; no paid generation or new model download.
Illustrations are qualitative staging, not geographic or calibrated simulations.
Report metrics retain distinct comparison windows: daily export pace must not be
presented as cumulative-volume growth.

## Openverse experiment

Exactly three anonymous audio API queries returned HTTP 200, one per sound need,
with `license=cc0,by,pdm` and `source=freesound,jamendo`. Three CC0 Freesound preview
files totalled 721,409 bytes, each within an 8 MB cap. Private receipts retain
request/result metadata, URLs, byte counts, SHA256 and unchanged attribution
strings. All files decoded successfully.

| Need | Selected source | Licence |
| --- | --- | --- |
| Train motion | [kyles, freight train pass](https://freesound.org/people/kyles/sounds/455775) | CC0 |
| Granular handling texture | [Wagna, sandfall5.wav](https://freesound.org/people/Wagna/sounds/326304) | CC0 |
| Transition | [DJT4NN3R, whoosh_short_low.wav](https://freesound.org/people/DJT4NN3R/sounds/449992) | CC0 |

The sand recording is designed granular texture, not a claimed wheat recording.
Effects were manually admitted and placed alongside a locally composed original
instrumental score for each version. This tests bounded discovery, acquisition,
provenance and local use; automatic scene-to-SFX placement was not tested. Three
requests do not establish service-wide daily limits or catalogue size.

Primary references: [audio API](https://api.openverse.org/v1/),
[media metadata](https://docs.openverse.org/meta/media_properties/api.html),
[CC0 terms](https://creativecommons.org/publicdomain/zero/1.0/).

## Tested production workflow

1. Reuse admitted project effects first. For a missing sound, name its scene,
   purpose and bounded search/download budget; search once per sound type in this
   trial. Do not infer a service-wide quota from that local cap.
2. Inspect each result's source, landing page, licence and intended use. Search
   filters do not clear assets; retain attribution unchanged. Only CC0 Freesound
   acquisition was exercised here; other providers/licences need their own checks.
3. Retain the selected URL, metadata, byte count and SHA256 with the downloaded
   file. Enforce the acquisition cap and decode before admission. Fail explicitly
   when retrieval or licence evidence is unavailable; do not substitute silently.
4. Keep score, effects and mix separate. Place effects to support the scene,
   review their final mix and inspect the encoded output. Technical level/decode
   measurements do not replace listening.

## Evidence and qualification

All D/E/F exports passed full decode and faststart checks: H264/yuv420p, 600 frames,
20 seconds and AAC. Six encoded frames per video were inspected. Integrated
loudness D/E/F: −19.19/−19.11/−19.04 LUFS; true peaks: −2.11/−4.85/−3.48 dBTP.
Browser checks passed; nested-timeline authoring warnings remain. Numeric copy was
compared with the supplied report, not independently verified economic data.

On 2026-10-20 the owner explicitly declared the Openverse SFX experiment successful
and approved it for the tested production arsenal. Qualification covers SFX
search, per-item licence/provenance admission, download and manual montage use.
This is owner acceptance of the workflow, not independent model listening or
blanket acceptance of every mix. Music discovery and automatic semantic placement
remain untested. Partner acceptance was not obtained; repeated-report automation
remains unimplemented pending a separate specification and owner resumption.
Local fonts/logo are private demo assets; template transfer requires appropriate
rights. No media, raw report or third-party code is committed.

## Current pause — updated 2026-10-22

The owner paused weekly video production on 21 October. On 22 October the owner
reported that partners did not like the experiments and will supply a separate
specification. Detailed objections and the replacement format are unknown. This
is not cancellation. D and F remain owner preferences, not a partner selection.
Preserve all demos, source pins and admitted SFX; wait for the specification and
owner resumption before another weekly render, integration or recurring publication.
The successful Openverse workflow qualification remains distinct from acceptance
of these creative treatments. The independently requested [site Reels](ssi-site-reels.md)
was delivered and accepted by partners (owner report); a matching English version
was requested. That separate commission does not resume this weekly branch.

## Reuse and handoff

For 3D, tie travel, wheel rotation, loading and attached parts to one absolute
clock, then inspect camera-cut boundaries and final encoded frames.

After partners select a treatment, apply a common template to each of the report's
three parts and assemble an aggregate for the format decision: three short clips
or one longer summary. These other sections and the aggregate are not delivered
by this logistics-only pilot.

SSI then receives the editable template, field mapping, retained dependency
versions, rights notes, rebuild instructions and QA examples. SSI owns report
generation, native mapping, video production, scheduling and Telegram publication.
Validate a second report and edge cases there before enabling recurring production.
