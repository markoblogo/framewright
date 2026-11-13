# InShot — feature study on the physical tablet

13 November 2026. Follow-up to the [control/export trial](inshot-android-control.md), using the same owner-connected Redmi Pad Pro, Android16 and InShot2.243.1555 with visible annual Premium membership. The owner allowed tablet files for experiments and selected a Babylon tour as the production application. No purchase, publication or new subscription. These observations do not qualify all advertised AI tools or long-form editing.

## Developer description versus executed scope

Sources: [official Android listing](https://play.google.com/store/apps/details?id=com.camerasideas.instashot&hl=en), [InShot](https://inshot.com/). The developer lists captions/speech, tracking, keyframes, PIP/chroma/blending, speed curves, cutout, colour controls, effects/transitions, photo tools and four collage families. Availability in one editor/version is separate from export quality, entitlement and processing location.

| Function | Actual result | Production use and limits |
| --- | --- | --- |
| Auto Captions, English | Generated captions for a13-second accepted Knox speech fixture. All spoken lexical words were recognised in this sample, including Dependabot/APM; punctuation/case differs. Captions visible in native export. | Fast first pass for English shorts; proofread names, timings and mobile placement. SRT export, other languages, cloud/local processing and long-form accuracy unverified. |
| Text animation/keyframes | Added FW TEST, selected entry fade, added two position keyframes; rendered text and changed placement visible. | Short titles/labels. Inspect interpolation and each aspect; not proof of arbitrary motion tracking. |
| PIP and chroma key | Imported synthetic green/red card; sampled green, removed it and exported red square over the main clip. | Simple overlays/stickers. Circular-mask attempt did not persist; mask is not qualified by this output. |
| Audio mix | Imported local WAV as a second track. Volume slider explicitly set to25; base voice retained. | Music under voice. Equal numeric percentages are not equal perceived loudness across tracks. Fade controls were reached but exported fade envelope was not verified. |
| Canvas9:16/background | Changed16:9 source to9:16, background preset inspected, exported1080x1920. | Layout starting point, not automatic final reframing. Recheck titles and important picture after aspect changes. |
| Speed and split | Set standard speed2.00x, split the base clip, exported6.500s versus13.000s input. | Simple accelerated inserts. Retiming of independently generated captions/PIP and pitch behaviour remain unverified. Transition panel was not successfully exercised. |
| Photo colour | Contrast/saturation adjusted; HSL blue saturation26 observed. | Targeted cover/thumbnail colour correction; settings are subjective, not colour calibration. |
| Photo cutout and outline | Standard cutout removed background, white outline applied, exported1920x1440 RGBA PNG. Source watermark preserved; hair edge has a halo. | Isolated figure for covers/cards/PIP. Check alpha on light/dark backgrounds before delivery. Not a precise masking qualification. |
| Grid collage | Prior trial exported two-image1920x1920JPG. | Comparison cards and social images. |
| Freestyle collage | Selected two images, changed position and exported JPG. | Flexible thumbnail/story layouts; source watermark and rights stay attached. |
| Stitch collage | Selected two synthetic images, chose horizontal stitch and exported JPG. | Before/after and interface strips; vertical/subtitle stitch modes only inspected. |
| AI Blend collage | Two synthetic images combined using the default feathered split template and exported JPG. No generative reconstruction inferred from the label. | Soft before/after or paired cover composition; other blend templates untested. |
| Tracking, curves, effects, enhancement/stabiliser, AI Speech | Developer-described and/or UI-visible; no verified exported result in this suite so far. | Keep conditional. Do not claim offline processing, unlimited Premium allowance, successful tracking or speech quality. |

## Export timing evidence

The13-second vertical export has392 decoded video frames, versus390 source frames. The2x export has197frames and6.500s. The earlier3-second test also had two extra frames. Treat endpoint/frame parity as an open limitation. A20ms speech RMS-envelope comparison gave zero best lag and correlation0.985654 for the13-second mixed export. Raw waveform correlation was low and inconclusive; its apparent sample lag is not a reliable sync measurement. This is coarse timing evidence, not frame-exact AV or perceptual approval.

Private fixtures, screenshots, exports, measurements and hashes live in `records/inshot-functions-2026-11-13/` under the external studio. Personal gallery material stays private and is not an authorised publication asset. Native drafts can be reopened on this tablet; project transfer to another device is not established.

## Adopt now / keep conditional

Use the physical tablet for bounded cuts, titles, colour, local audio mixing, simple PIP/chroma, English draft captions, cover cutouts and collage cards. Use Android UI inspection plus current-screen coordinates; wait for panel transitions and re-observe after owner input. Keep precise timing, perspective phone-screen replacement, long films and complex tracked compositing with the existing measured routes until separately tested. No unattended background process or publishing integration was added.

## Tablet browser and small Android working set

Chrome and Xiaomi screen recorder are installed. The Babylon artifact loaded in tablet Chrome and entered fullscreen; capture/edit/export is a separate production check, not established by page display. This route can leave the laptop browser free, although it still uses tablet resources and Mac-controlled input/transfer.

[LocalSend](https://localsend.org/) is a free/open-source Android/macOS local-network transfer candidate; no account/cloud required per developer. It is not installed/tested here. USB transfer already works, so no dependency is added. A dedicated preview player can be evaluated if native playback is insufficient; no extra recorder/editor is needed just to enlarge the tool inventory.

[VLC for Android](https://play.google.com/store/apps/details?id=org.videolan.vlc&hl=en) is a free/open-source preview candidate with local playback, subtitle and audio-track controls per developer. It was not installed/tested here. LocalSend and VLC are task-specific reserves; current USB transfer and native playback do not depend on installing them.

Production preflight found that a new edit inherited the previous9:16 canvas and text styling. Explicitly reset aspect and font size, then inspect a nonzero-time preview before exporting. A moving preview/export can prevent `uiautomator dump` from returning a root; use screen capture and a previously observed pause location, then inspect the tree after playback stops. Keep native export completion separate from the appearance of its share screen.

## Babylon application — review candidates

Actual tablet Chrome captures were used for two native InShot outputs:16:9 at1920×1080/43.933s and9:16 at1080×1920/44.000s. The heavy scene recorded at roughly7–12fps; Mac FFmpeg did selection/cropping/motion interpolation before InShot. Native finishing added colour, entry/end titles and original local ambient music. No narration. Exporting at1080p does not create new captured detail. Both decode successfully, sampled title/layout frames were checked and the loopback player played/seeks in both directions. Vertical null-muxer endpoint rounding warning and two extra endpoint frames remain recorded; frame-exact parity is not qualified. The owner subsequently accepted both full films with sound; [publication packages and limits](../productions/babylon-virtual-tour.md) are prepared.

Private application recipe, retained original music generator, source captures and output hashes: `productions/babylon-virtual-tour/edit/INSHOT-EDIT.md` and `productions/babylon-virtual-tour/receipt.json`. Babylon is one accepted film story in the evidence index; its two formats are not separate stories. Publication links are owner-reported; independent visibility/metrics remain unverified. This supports the tablet browser as a second capture surface, with performance preflight per world; it does not establish unattended simultaneous laptop/tablet production.


Owner later installed VLC/LocalSend/KORG. See the [companion trial](android-companions-2026-11-13.md) for actual results; the uninstalled/untested candidate paragraphs above describe the earlier baseline. Babylon publication links are now owner-reported, without independent visibility/metrics checks. Further app tests are stopped; Kaossilator is deferred separately.
