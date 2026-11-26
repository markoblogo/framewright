# VIDEO-MD-01 — boundary-only OTIO and cold reopen

26 November 2026. Owner authorised checking the available route and running a trial on retained studio material. Second task after [selected-delivery recovery](radar18-selected-delivery-recovery-2026-11-26.md). No paid call,cloud upload,model download or accepted-film change.

## Available route

Existing videomd1.2.0 in the isolated REA environment successfully checked/read the actual [REA fixture package](reverse-video-rea-2026-11-25.md). Current general uv offline cache had no OTIO distribution; this failed resolution is retained as an access result,not a model failure. Reused the previously retained official OpenTimelineIO0.18.1 macOS arm64 CPython3.12 wheel from the28October handoff. Created shared external `tools/python/otio-0.18.1` with that single local wheel,offline/no dependencies/no network. Its interpreter is the already installed uv CPython3.12.8 under the user's .local/share/uv; the environment is not a clean-machine portable bundle. No global Python changes.

Kdenlive's retained26.08.2 app launched through native Computer Use,but stayed at Quick Setup: Start Editing action timed out,Return produced no transition. No OTIO editor import/save/reopen/render completed. No browser opened,AppleScript workaround,reinstall,settings rewrite or owner rescue requested. Library readback and GUI editor qualification remain separate.

## Material and exact mapping

The existing silent12s1280×72024fps fixture has three known4s segments: moving Blue Lagoon photograph,recorded browser game and code animation. Original SHA256 `2bb1229bac497a880dd77e16f513881114f7dff0cc2357136fa01e9360ac0e57`. Source card hash matched that media before conversion; videomd's real parsed timeline supplied boundaries. Seconds converted with exact rational arithmetic; fractional-frame boundaries would be rejected rather than rounded.

| Shot | Timeline start | Source in | Duration |
|---|---:|---:|---:|
|01|0|0|96 frames|
|02|96 /4s|96|96 frames|
|03|192 /8s|192|96 frames|

Three clips reference one unchanged flattened media copy. The original image motion,screen content and code animation remain baked,not reconstructed layers. No audio track exists in this fixture; audio/effects/transitions/retiming are untested. Source VIDEO.md's made~/material~/confidence claims remain in source-videomd.json as uncertain diagnostics; incorrect inferred capture route is not converted to fact.

Existing otio_export.py exported `BoundaryCut.otio` from an explicit spec using the official library. No product exporter changes or general automatic importer introduced. The small retained conversion script only covers this measured straight-cut profile.

## Actual reopen and retained failures

A separate isolated Python process from `/private/tmp` copied the handoff folder to a new location,read the actual OTIO file,resolved relative media,verified their hashes,and checked all clip IDs/source ranges/positions and288-frame duration. It wrote a second OTIO file and reopened it with identical serialized structure.

Initial picture verifier used a global FFmpeg split→frame trim→concat. At4s the H.264 source changes from yuvj420p to yuv420p. Filtergraph reinitialisation reset the frame-trim counters,producing193rather than288frames. Source showinfo and failed frame hashes retained. This is a failed verifier,not an OTIO boundary loss.

A second input-side fast-seek verifier returned288frames but different payload hashes from frame96onward. Independent full-decoder-initialisation/output-side seeking plus the same explicit yuv420p comparison format on both paths passed: **288/288 per-frame payload MD5 values match**. The ranges were read from OTIO,not a hard-coded recreated montage. This verifies mapping and decoding under the stated comparison; not calibrated colour or arbitrary-consumer seek parity. No media was re-encoded or source metadata rewritten to make the comparison pass.

Original fixture,VIDEO.md,timeline card and retained YouTube master hashes unchanged. The original project journal was unchanged during cold verification; result registration afterward appended new OTIO assets/technical observation. All prior artifacts/journal prefix,including the failed REA production-route-inference observation,were preserved. No creative approval or selected-film replacement.

## Retained files and decision

Private folder: `productions/reverse-video-2026-11-25/otio-followup/` contains package/media,source JSON,spec,OTIO/export receipt,relocated copies,conversion/cold-read scripts,and evidence including both failed checks and final trial-receipt.json. Keep the .otio and media folder together. Source recipe/accepted package unchanged.

**Bounded result passed:** VIDEO.md measured boundaries→official OTIO→relocated cold library reopen and decoded-picture parity. VIDEO-MD-01 closes this boundary-only question. **GUI editor import remains unconfirmed in this attempt.** Historical MN7R Kdenlive success is not re-used as proof for this input. No new screenshot/player,creative review,listening,audio roundtrip or independent-operator test claimed.

Use this route for verified straight-cut edit lists,not automatic recovery of an original layered project. Before an actual NLE delivery on mixed sources,check consumer seeking/colour or explicitly create a separately verified normalised derivative. No general automatic normalisation added here.

Next selected task: CAPSULE-RECIPE-01,not executed by this trial. Existing Radar pause,storage guard and release boundaries remain unchanged.
