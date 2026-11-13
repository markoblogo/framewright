# InShot — physical Android control and basic export

Executed 13 November 2026 at the owner's request to prioritise tablet control. This is one bounded control/export trial, not broad editor or AI qualification.

## Setup and resolution

Owner-connected Redmi Pad Pro (2405CRPFDG), Android 16, InShot 2.243.1555. Owner reported Premium; the settings UI independently displayed annual InShot Premium membership. USB debugging was authorised on the device. Official Google platform-tools ADB37.0.1 and Homebrew scrcpy5.0.1 were used. Existing global FFmpeg8.0.1_1 was preserved; scrcpy uses a separate FFmpeg9/runtime under the external studio tools folder.

An ADB server started in the restricted execution environment did not enumerate the device. Restarting that task-owned server with normal host USB access exposed it, first unauthorised, then authorised by the owner. The native automation catalogue could not select the bare scrcpy/SDL window. Direct Android UI accessibility inspection, screen capture and input supplied working agent control; this did not require a macOS app wrapper or weaker global permissions. No root, emulator or app modification was used. Ordinary input worked without changing another Xiaomi security toggle.

## Observed actions and results

- Opened InShot settings, returned to its home and selected each of Video, Photo and Collage from the Mac.
- Transferred three original synthetic fixtures (3-second MP4 and two PNGs), selected them in native media pickers and opened the real editors. The owner also explicitly permitted use of other tablet media; this trial used the synthetic fixtures.
- Video: imported the 3-second fixture and exported with the displayed1080p/30fps/MP4 settings. Pulled the output to Work: H.264,1920x1080,3.000s; decoded92frames, versus90 in the input. Decode-to-null emitted one non-monotonic endpoint-DTS warning. Basic export/transfer succeeded; frame-exact timing and AV sync are not qualified.
- Photo: changed one fixture's canvas to1:1, applied it and exported a1920x1920JPG.
- Collage: selected Grid, chose two synthetic images and exported a1920x1920JPG; the two panels were visually inspected. Freestyle, AI Blend and Stitch were visible menu modes, not executed tests.
- Returned the tablet to InShot home. scrcpy's keep-awake mode was active (`stay_on_while_plugged_in=7`). Current mirror audio was disabled; no audio-delivery result is claimed.

Video editor controls observed: canvas, audio, stickers, text, effects, filter, PIP, trim, split, delete, volume, background, speed, animation, AI Cut, voice enhancement, crop, track switch, video enhancement, stabiliser, cutout and mask; undo/redo, preview and a keyframe button were present. Presence is not an executed feature test. Photo controls observed: canvas, filter, adjustment, effect, background, portrait, sticker, text, PIP, removal, enhancement, cutout, drawing, crop, frame and rotation. No AI processing/cloud upload was initiated.

## Retained recipe and limits

Private instructions/helpers: `tools/android-control/README.md`, `tablet.py`, `mirror.py` under `/Volumes/Work/Work/FramewrightStudio/`. Private source/output/hash receipt: `records/android-inshot-2026-11-13/receipt.json`; media stay outside Git. Helpers detect exactly one authorised device, inspect current accessibility labels and stop on ambiguous targets. Canvas/gallery widgets need coordinates derived from a fresh screenshot. Concurrent owner input can change state; re-observe before acting. No automatic publishing or background schedule was added.

The same-day [feature follow-up](inshot-functions-2026-11-13.md) subsequently exercised captions, text/PIP/chroma, audio, speed, photo cutout/HSL and more collage modes. The observations above preserve the initial control-only scope. Next production application: the owner-selected Babylon tour. Check save/reopen, corrections, AV sync, crop, feature allowance and export. Full-function catalogue, tracking quality, AI tools, audio mirroring, long edits and unattended resilience remain open.

References: [scrcpy control](https://github.com/Genymobile/scrcpy/blob/master/doc/control.md), [device selection](https://github.com/Genymobile/scrcpy/blob/master/doc/connection.md), [Android developer options](https://developer.android.com/studio/debug/dev-options).
