# Tool intake, 23 November 2026

Four owner-supplied links. Source review only. No installation, asset upload,
weight download, benchmark, provider qualification or change to production ranking.

| Reference | Decision and evidence | Value for Framewright |
| --- | --- | --- |
| [Inworld Voice Isolator](https://github.com/inworld-ai/voice-isolator) | **Queue first.** The project documents Apache-2.0, an offline model and a streaming model, with 48 kHz mono output by default, optional background residual, and Apple Metal support with a compatible PyTorch version. Weights download on first use. | Clean archival interviews, location audio and noisy screencasts before mixing. Start with offline recordings. Several voices may survive isolation, and speech restoration is a separate problem. |
| [Tripo Orbit](https://www.tripo3d.ai/3d-tools/tripo-orbit) ([submitted Russian page](https://www.tripo3d.ai/ru/3d-tools/tripo-orbit)) | **Queue as a secondary utility.** The vendor documents a free macOS/Windows viewer with glTF, FBX, OBJ and STL support, materials/textures and animation preview. Vendor performance figures remain untested here. | Fast acceptance check on incoming props and animation before opening the production scene. Keep Blender or the established viewer as the baseline. |
| [AO — Programmatic Character Reveal Trailer](https://sites.google.com/view/aoprogrammaticcharacterrevealt/full-page-embed) | **Visual reference only.** The primary page identifies the trailer. The embedded contents, implementation, export path and reuse rights were not established during intake. | Revisit when staging a character reveal. Existing [AO motion-package evidence](../experiments/openmotion-ao-title-2026-11-21.md) concerns a separate verified workflow. |
| [Sentinel7/h3](https://huggingface.co/Sentinel7/h3/tree/main/2834417/3446189) | **Unverified reference, held.** The repository shows a sensitive-content interstitial; the submitted subfolder exposes no verified artifact identity, license or usage requirements in the reviewed public view. | Revisit only with an attributable model card, specific artifact/version, terms and a concrete use case. |

## INWORLD-ISOLATE-01

Use a 20–30 second owned noisy recording with a matching clean speech reference.
Compare the original, the existing local cleanup baseline, and the offline model
at matched loudness. Listen for word endings, speaker character, speech leakage
into the residual and watery artifacts. Record runtime, output alignment,
hardware and effective resource use separately. Check whether the local Mac
can run the pinned model before treating it as available for production.

## TRIPO-ORBIT-01

Open one owned textured, animated glTF and one representative static asset in
Orbit and the existing Blender/viewer route. Check missing textures, material
appearance, animation playback and time to a usable first inspection on the Mac.
Use the same inputs. A pass would qualify the tested inspection workflow only.
