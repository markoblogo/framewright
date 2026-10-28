# Mac-native and free production applications — intake, 27 October 2026

User-supplied Perplexity list checked against primary vendor documentation. Research only: no software installation, launch, recording, import, rendering, account action or test. Existing FFmpeg production experience is not proof that any GUI application or agent integration is production-qualified. On this Mac, `/System/Applications/QuickTime Player.app` was found; the named alternatives were not found in `/Applications`. This is a narrow path check, not an exhaustive app inventory or version check. iMovie and GarageBand are Apple applications that may be downloaded separately; do not claim they are preinstalled.

## Practical candidates

| Tool | Classification | Relevant use / small future probe | Boundaries |
| --- | --- | --- | --- |
| [QuickTime Player](https://support.apple.com/en-mide/guide/quicktime-player/qtp356b55534/mac), [Screenshot](https://support.apple.com/en-ie/102618) | Queue, built-in | Record 15–20s of a safe local window and microphone, trim/export; compare video, audio sync and capture controls with existing workflow. | Screen/mic permissions when needed; native app presence is not proof of actual capture, desktop-audio support, automation, or no dropped frames. |
| [iMovie](https://support.apple.com/imovie) | Queue, free Apple app | One 20s two-clip edit, voice, title and cut; save/reopen and export, compare with current approach. | App availability/version and rights of included content to be checked; interactive workflow/agent reproducibility unproven. Apple documents external library storage. |
| [GarageBand](https://www.apple.com/mac/garageband/) | Queue, free Apple app | One cleared voice take with simple EQ and one music bed; export WAV and compare against unprocessed sample. | Recording, plugins/loops, local storage and applicable rights/terms need verification. Not a video editor or open-source tool. |
| [Audacity](https://www.audacityteam.org/features/noise-reduction/) | Queue, free/open source | One 15–20s voice with a clean noise sample: mild noise reduction → A/B listening against original and existing FFmpeg chain. | Steady noise is easier than speech/music; excessive reduction introduces artifacts. Plugin compatibility and Mac performance untested. |
| [OBS Studio](https://obsproject.com/) | Queue when complex capture is useful, free/open source | Capture a safe demo window, voice and one overlay; measure sync and playback, compare with Screenshot/OpenScreen. | [ScreenCaptureKit](https://obsproject.com/kb/macos-screen-capture-source) documents desktop audio on macOS 13+; permissions and real local capture remain untested. |
| [Shotcut](https://www.shotcut.org/download/) | Candidate for one editor comparison, free/open source | A 20s multi-layer clip → one precise revision → save/reopen → export; record memory and time. | macOS universal build documented; actual performance/automation untested. Compare one editor at a time. |
| [Kdenlive](https://kdenlive.org/download/) | Alternative editor candidate, free/open source | Same fixture as Shotcut, only if the first editor leaves a relevant gap. | Vendor lists Mac Silicon build; actual machine fit and agent reproducibility untested. |
| [Shutter Encoder](https://www.shutterencoder.com/) | Queue on a real export/subtitle need | Transcode a 10–20s cleared clip and add an existing SRT; compare streams, sync, file size and readback to existing FFmpeg. | Uses FFmpeg under its GUI; not evidence of better speed, automation or text-to-speech. Check actual available build, licence and bundled features. |
| [HandBrake](https://handbrake.fr/docs/en/1.10.0/get-handbrake/where-to-get-handbrake.html) | Reference/conditional comparison, free/open source | Try only if a hand-operated compression or delivery preset is needed; compare like-for-like with FFmpeg. | Transcoder, not a timeline editor. [Official description](https://handbrake.fr/docs/en/1.7.0/introduction/about.html). |
| [DaVinci Resolve Free](https://www.blackmagicdesign.com/uk/products/davinciresolve/) and Fairlight | Deferred resource-gated candidate | One small 1080p 15–20s color/audio fixture, export and inspect only if an actual production needs those controls. | Free and paid Studio editions differ; do not assume Studio AI, external scripting or plugins are free. Check current version, installation size, GPU/RAM and terms; large workloads may be unsuitable for this Mac. |

No candidate in this list is ruled out entirely. GUI workflows can complement agent/CLI workflows; none is assumed to be an autonomous agent tool. Do not run these tests concurrently on this Mac. Test one real production need, retain its own result, version, resource use, visual/listening QA and owner decision; avoid forcing an editor change or duplicating existing work. User's physical Android/InShot comparison remains deferred.

## 28 October follow-up

[Kdenlive26.08.2 OTIO trial](../experiments/otio-mn7r-handoff.md#same-day-follow-up-actual-kdenlive-import-edit-and-render)
selected this alternative because native OTIO import/export was required; Shotcut's
listed roadmap did not establish that capability. Apple Silicon official build on
external storage passed this native cut/edit/re-export/render task with two encoder
threads. This is scoped evidence, not a blanket editor/UI-automation qualification.
