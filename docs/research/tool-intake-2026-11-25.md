# Tool intake, 25 November 2026

Owner selected the practical candidates for queued testing. Source review and
test design only; no execution or qualification.

| Candidate | Route and bounded test |
|---|---|
| [CVT CorridorKey 2](https://github.com/creativevideotips/cvt-corridorkey2) · [Author demo](https://www.youtube.com/watch?v=GQ8ufGuzqV8) | Extend existing CorridorKey 2.0 candidate with the unofficial Apple Silicon Resolve OFX route. Confirm Resolve/plugin/model version, compatibility, resources and licence. Compare the same 5–8s owned green-screen shot against conventional keying; inspect moving edges, spill, transparency, flicker and time. |
| [Button Sounds](https://github.com/joshwcomeau/button-sounds) · [Playground](https://buttons.joshwcomeau.com/) · [Package](https://npmx.dev/package/button-sounds) | MIT repository, recorded click/toggle assets and JS library. Compare 8–12s silent-interface shot with and without two carefully timed sounds; check alignment, audibility beneath speech, repetition fatigue and asset-level terms. Prefer reusable local audio files when suitable. |
| [FluidVoice](https://fluidvoice.com/) | Developer describes local dictation and cleanup, macOS 15+. Use a short synthetic English production note offline; compare transcript, punctuation, retained technical names, latency and correction effort against the current dictation route. Verify personal/commercial scope, model resources and permissions. |
| [DBS SplatTrain](https://github.com/dborrull/DBS_SplatTrain) | MIT node, Nuke 17 + Brush toolchain, documented Windows route tested on RTX 4060 Ti. Current Mac compatibility unproven. Conditional test: train one short owned tracked shot and reimport the splat; verify camera alignment, scale, occlusion and novel-view artifacts. Confirm suitable host, GPU and Nuke usage terms first. |
| [Maya Assistant](https://help.autodesk.com/cloudhelp/2027/ENU/Maya-Assistant/files/MAYA_ASSISTANT.html) · [3ds Max 2027.3](https://help.autodesk.com/cloudhelp/2027/ENU/3dsMax-WhatsNew/files/whats_new_in_3ds_max_2027.3/GUID-88DD6F51-EAFA-4817-B399-47847E1DE749.html) · [Preferences](https://help.autodesk.com/cloudhelp/2027/ENU/3dsMax-Customizing/files/preferences/GUID-85FE4F61-CBE6-403A-A607-193B52D9F1D5.html) | Conditional watchlist trial. Max release notes describe scene analysis and editable actions; Maya and preferences pages were not retrievable. Verify host/entitlement and permissions, then on a disposable scene ask for one reversible light or camera change and inspect actual editable result and undo. No purchase or migration. |

First practical probe: Button Sounds, then CorridorKey when the native route is
confirmed; FluidVoice for production-note dictation. The Windows/Nuke and
Autodesk trials stay conditional on a compatible already-authorized environment.
