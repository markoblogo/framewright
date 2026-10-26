# DJV installation and Chaos Vantage reference decision

26 October 2026. The owner authorised DJV installation and a queued real review
trial. Chaos Vantage is retained for reference only: no Windows environment is
available, so no test or current production use is planned. No paid account,
media upload or new video render was authorised or performed by this intake.

## DJV — installed; later trial partially successful

DJV **3.7.5**, native Apple Silicon, installed through the official Homebrew cask
into `/Applications/djv.app`. The downloaded official release DMG independently
matches the cask SHA-256. Bundle version/architecture were checked; the DJV 3.7.5
window and first-run FFmpeg Setup page were observed. Setup detected the existing
FFmpeg. At installation no video was opened. That historical startup observation is **not**
proof of playback, sync, colour, annotations, review persistence or production
readiness. [Sanitized installation receipt](../../experiments/2026-10-26/evidence/djv-installation.json).

The source article describes 3.6.0; the installed version is the official 3.7.5
release. Its review session, frame annotations, A/B comparison and CLI/Python
interfaces are documented candidates for our precise-revision workflow. Bind the
trial to the installed version: current upstream docs may describe later changes.

### Real trial outcome and retest decision

The subsequent owner-authorised [Nantes A/B trial](../experiments/djv-review.md)
verified visible comparison at frame72, notes/drawing, save/reopen/relocation and
unchanged master hashes. Native captures at other frames can remain black; a
30s FFV1 diagnostic proxy helped at240 but not612. Cause is unconfirmed. Retain
candidate status and repeat on the next one or two productions, as requested by
the owner. Listening, sync, calibrated colour and general production readiness
remain unqualified. [Provisional procedure](../../skills/video-production-router/references/djv-review.md).

### Original trial plan: existing Nantes green-line revisions

1. Use retained v1/v2 masters, known 1920×1080/24fps and their hashes. Make the
   actual reviewed master A, the comparison B; verify source identity and timing.
2. Compare the pixel sections at native scale, mark a frame and a short range,
   and add a drawing plus a note describing defect, desired change and what to
   preserve. Verify H.264/AAC playback and audio/frame alignment. If needed, use
   the existing FFmpeg fallback; no codec-pack installation is implied.
3. Save a `.djvr`, close/reopen it and move a copy together with the media. Check
   that source links, A/B settings, frame/range anchors and marks survive. Retain
   missing-media or decode failures. Approved masters must remain byte-identical.
4. Inspect the session JSON/installed automation interface and test a thin link
   to Framewright’s existing revision journal. Do not introduce another tracker,
   import machine settings into it or infer acceptance from the absence of notes.
5. Record actual playback, sync, colour and save/reopen outcomes separately, then
   obtain owner review before promoting the demonstrated scope for production.
   No generic perceptual-AI quality or autonomous editing capability is claimed.

Sources: [review announcement](https://grizzlypeak3d.com/2026/09/10/djv-v3-6-0-new-review-mode-annotate-frames-and-run-full-review-sessions-without-leaving-the-player/),
[3.7.5 release](https://github.com/grizzlypeak3d/DJV/releases/tag/3.7.5),
[review sessions](https://grizzlypeak3d.github.io/DJV/reviews.html),
[session format](https://grizzlypeak3d.github.io/DJV/review-format.html),
[automation](https://grizzlypeak3d.github.io/DJV/automation.html),
[install/codecs](https://grizzlypeak3d.github.io/DJV/install.html).
The application is BSD-3-Clause; bundled codecs/plugins have separate licences.

## Chaos Vantage — reference only, not in the active test queue

Vantage 3.4.0 documents additional camera focus modes, animated camera FOV from
DCCs, OpenPBR materials and fire/smoke presets. Broader Vantage capabilities include
ray-traced scenes, camera animation, Gaussian splat relighting and integrated
3D elements. These could be relevant to virtual film sets if another environment
is deliberately selected in future; Marble import, our rigs and agent control
have not been tested.

Current requirements specify Windows 10 2004 or newer, x86-64/AVX2, a compatible
discrete DXR GPU and a Vantage licence. There is no native Mac path documented
for our current setup. **Do not install, purchase, test, route current productions
to Vantage, or create a Windows/cloud workstation for this item.** The owner
explicitly chose documentation only. Reconsider only if the owner or a future
operator deliberately adopts a compatible Windows environment and approves a
specific licence/resource budget and trial. This is a platform-based deferral,
not a failed quality test or a claim that the tool is unsuitable in general.

Sources: [3.4.0 release notes](https://documentation.chaos.com/space/LAV/1265139715/3.4.0),
[requirements](https://documentation.chaos.com/space/LAV/124753566),
[features](https://www.chaos.com/vantage/features).
