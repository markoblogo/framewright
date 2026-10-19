# SSI OAuth demo: external-agent field report

Received from the owner on 2026-10-18. This is a supplied field report, not an independently rerun experiment. The report below is retained unchanged; its pending-upload statements describe its earlier checkpoint.

- Owner-supplied video: [SSI Drive OAuth demo](https://youtu.be/dIpiFyTPVUc).
- `publication_verification: user_provided_url`. On 2026-10-18 the owner confirmed working playback and temporary unlisted (link-only) YouTube access. These are owner-verified observations; independent playback was not checked here.
- Publication lifecycle: temporary verification demo. The owner plans to delete the YouTube upload after Google reaches a decision. Deletion has not occurred or been independently verified; this note does not schedule or perform deletion. Retain the URL as historical provenance, not a permanent public showcase or durable evidence endpoint.
- Technical QA and artifact hash below are reported by the producing agent; the final MP4 and private production sources were not supplied here for reinspection.
- The supplied URL records the owner's upload report. Explicit creative acceptance, Google submission and provider approval remain unconfirmed. No audience-performance claim.
- Framewright supplied method selection and prior evidence; OpenScreen/FFmpeg/Pillow performed capture and assembly. This demonstrates one cross-task use by another agent, not general autonomous-production qualification or measured time savings.
- Proposed follow-ups: visible normal-window and decoded-frame readiness; PTY/owned-process stop guidance; consent-language/permission-text and owner-only warning handoff checks. These are retained proposals, not completed recipe changes.
- Kept outside the existing 22 validated export records until an artifact/evidence record is reconciled; no renderer, registry capability or release change.

Source attachment SHA-256: `611a8a8c6ba6dc400c9cfae448fd48e0aa254e98ccd159dec2fc791be62f66b7`.

---

# SSI Drive OAuth verification demo: Framewright field experiment

Date: 2026-10-18. Status: local render and technical/sample-frame QA complete; owner acceptance, upload and Google submission remain pending.

## Goal and authorization

Produce an authentic, English-captioned demonstration of SSI Context Drive Sync for Google's Drive scope review. The owner chose Framewright, approved recording only the isolated Comet window without microphone, system audio or camera, and will upload the reviewed MP4 as an unlisted YouTube video. Creation is not authority to publish or submit the review.

## Tool selection and exact roles

- Framewright, pinned to `905c400967dda42fe1dd9d86b65dfc8c0b8511eb`: method selection, recipes and prior evidence, not a renderer. Used `live-site-tour`, the tested OpenScreen record and the existing OpenScreen/FFmpeg example. The actual offline search returned one scoped, manually tested OpenScreen record; this is not general provider qualification.
- OpenScreen 2.0.0: official macOS arm64 release, code signature checked. Archive SHA-256: `f257d63c55d229d4e8eb0511e546b7c8e16b80cc4d47b835df8396b75736db51`. Recorded one real browser window, system cursor, no automatic zoom or audio.
- Codex native computer control: actual browser navigation and observations. No injected browser script, synthetic consent UI or browser-security bypass by the agent.
- FFmpeg 8.0.1: extraction, trimming, permanent browser-chrome crop, caption compositing, constant-frame-rate H.264 assembly and technical QA.
- Pillow 12.3.0: deterministic English caption images. The installed FFmpeg lacks `drawtext` and `subtitles`; PNG overlays avoid replacing the renderer or installing another FFmpeg build. The accompanying SRT remains reusable.

No generated actors, AI-recreated interface, voiceover, paid render service or HyperFrames migration was used.

## Actual workflow

1. Isolate the intended browser window and test an eight-second recording. Check the pixels, not just exit status. Keep the window visible and out of fullscreen/Stage Manager miniature state.
2. Start recording and wait for the native `Recording started` receipt. The captured window ID stays stable as page titles change.
3. Record public app identity and privacy notice, then the real administrator reconnect workflow. At Google's unverified-app warning, hand control to the owner. Record the actual English consent screen, existing permission details and return to SSI.
4. Run actual folder synchronization and inspect actual imported material cards. Preserve original/extract separation, review warnings, unknown freshness and the distinction between import and report publication.
5. Edit real footage at normal speed. Remove waiting and unrelated navigation. Crop browser chrome consistently to exclude tabs, autocomplete, OAuth state/code parameters and unrelated settings. Put captions below, not over, permission text. Finish with metadata, decode and frame inspection.

The selected take shows Google saying the app already has access. Its expanded permission is **See and download all your Google Drive files**, including viewing files, downloading files and collaborator metadata. This is account-wide read-only OAuth, not a folder-specific permission. The application's folder boundary is separate. No edit/delete scope was added, and no existing grant was revoked merely to stage a first-time permission screen.

## Observed functional evidence

- The SSI interface showed a connected account and 424 stored Drive material records.
- Two operator syncs completed with 8 processed files and 0 skipped folders/oversized files. The later recorded receipt displayed a checked timestamp of 18 October 2026, 14:57 in the application. It is an application-displayed time, not a new timezone conversion.
- Actual XLSX material cards showed Google Drive provenance, source filenames, received times, extracted Ukrainian tables, stored originals and extraction review notes.
- `Freshness: unknown` and `USED IN REPORT: not yet` remained visible. Successful import is not proof of a validated/current report, generation, site publication or channel sending.
- The privacy notice explains processing/storage, the broader Google permission, application-level collection bounds, revocation and retention.
- No source Drive file was edited/deleted. No report was published/sent during the demonstration.

## Failures and recovery, retained rather than hidden

- Two long captures timed out in the native ScreenCaptureKit helper. The successful short probe did not establish long-capture reliability.
- UI screenshots later showed a tilted window miniature. Raising it through automation did not recover it; a Dock attempt also timed out. The owner brought the intended normal window visibly forward, after which the same long recording started. This is a useful workaround, not a proven root-cause diagnosis.
- Normal-pipe recording had closed stdin, so the documented `stop` input failed. Only the exact owned recording process was stopped with SIGINT and saved successfully. Later PTY captures accepted `stop` normally.
- The first usable take captured Russian consent plus unrelated browser-settings navigation during owner interaction. It was not treated as final English evidence. Those spans stay private and are excluded.
- Keyboard Home/Down selection in Google's language control selected Filipino rather than English because the dropdown order/focus semantics differed. The error was observed and corrected through the real visible English item. Locale was asserted before the final flow.
- Google reverted its warning locale after account choice. Only `hl=en` on that same observed warning URL was changed through the address bar; private OAuth parameters were not logged. The protective warning remained, and the owner personally continued past it.
- Google's return landed on SSI Daily input rather than an explicit success receipt. The video says exactly that, then tests actual Drive access separately; it does not relabel the landing as proof of callback success.

## Editing and reproducibility

`scene-manifest.json` records source-take basenames, source intervals, output intervals, normal playback speed, captions, crop and output settings. `SSI-Drive-OAuth-Demo.en.srt` supplies the English narration. The local `build_demo.py` reproduces the assembly when the authorized private source recordings are available. Do not commit raw recordings, OpenScreen projects, browser profiles, credentials, tokens, private screenshots or large encoded media to Framewright.

Raw takes: 03 = 309.397 seconds; 04 = 79.703 seconds (not selected for final consent); 05 = 371.558 seconds. Native media is 2498 x 1842 and video-only. The capture header's `600/1` rate is not claimed as actual 600 fps; delivery is normalized to 30 fps. The final canvas is 1920 x 1440 to preserve readable page content; a separate 220-pixel caption footer does not cover Google permissions.

## Bounded improvements suggested for Framewright

- Add visible-normal-window readiness and a decoded-frame gate to the live-site-tour recipe; source discovery and successful process exit are insufficient.
- Document PTY/stdin versus owned-process SIGINT stop paths and privacy-safe capture receipts.
- Treat consent language, complete permission text and user-only security-warning hand-off as explicit OAuth-demo checks.
- Keep separate claims for capture success, technical QA, owner acceptance, upload and provider approval.

## Remaining human/provider gates

Owner review of the final MP4, owner unlisted upload, insertion of that URL into the Google verification request, and Google's actual review decision. The video does not itself verify `drive.readonly`.

## Final artifact and QA receipt

- File: `SSI-Drive-OAuth-Demo-2026-10-18.mp4`, 176 seconds, 4,924,181 bytes.
- H.264/yuv420p, 1920 x 1440, constant 30 fps, 5,280 frames, zero audio streams; complete decoding passed without errors.
- SHA-256: `9b5724822ead13ea642feeb76037237659b414061ef0ed458f01954a954c7008`.
- Visually inspected all 16 scene-midpoint samples and enlarged critical permission/receipt frames. Captions stay outside permission text; browser chrome and unrelated settings are excluded. No credentials were visible in the inspected delivery frames. This is bounded sample-frame review, not a claim of manual inspection of every frame or an automated secrets scan.
- Creation and QA are complete. Owner acceptance, unlisted upload, review submission and Google's approval are separate, unfinished gates. The demo shows reconnection of an already-authorized account, not a fabricated first-time grant.
