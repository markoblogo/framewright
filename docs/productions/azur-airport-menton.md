# TRAIN-AZUR-ROUTE-01 — Nice Airport to central Menton

> Current result: owner-accepted90s bus-first/train-second film with restored F1 voice; YouTube owner-reported. Earlier train-first proposals and pending pilot sections are historical. Native720p final, bilingual metadata and provenance retained. See [training consolidation](../methods/training-to-fiction-2026-11-03.md).

3 November2026. Owner explicitly resumed the route production, superseding the previous wait until4November morning. Scope: useful horizontal travel-guide film, beyond a decorative route drive; guide and location illustrations, English female narration. Owner selected train as primary, bus/taxi briefly.75–90s proposal,84s storyboard/script prepared; actual speech timing not measured yet.

## Saved state and first review

Private root `productions/azur-airport-menton/` in the external studio. Existing `project.py` checkpoint, pinned source illustration hashes/manifest/claims/script, brief and review page retained. Four proposed16:9donors: airport, Nice-Saint-Augustin station, Menton station and guide hero for the bus alternative. Guide images are illustrative, not proof of present-day entrance/vehicle appearance. Nice-Ville/Garavan remain reserves; Monaco does not imply a required change. Owner accepted these exact donor crops, schematic style and narration direction on3November2026 and authorised a short moving pilot. This is input approval, not acceptance of a rendered film.

[Editorial source](https://azurmenton.com/en/guide/how-to-get-to-menton-from-nice-airport). Current ending proposal: station → Biovès gardens → central seafront. Exact footpath and rail geometry need verification before pilot. No fixed fare, guaranteed connection or door-to-door travel duration quoted.

## Source findings retained

- [Airport train access](https://www.nice.aeroport.fr/en/directions/train) describes free airport tram to GrandArénas, moved platform access across avenue Maître Maurice Slama, and a Terminal1 pedestrian alternative. The illustration is not a current entrance photo.
- [Airport public transport](https://www.nice.aeroport.fr/en/directions/public-transport) identifies the free T2–T1–GrandArénas zone and current2/B lines. [SNCF station information](https://www.ter.sncf.com/sud-provence-alpes-cote-d-azur/se-deplacer/gares/nice-st-augustin-87756254) gives the newer station address but retains anL3 reference. Do not propagate that inconsistent line label; pilot should use current airport signage and a clear tram-to-walk mode change.
- The guide station card gives Boulevard René Cassin; official station access is avenue Maître Maurice Slama. Retain this as editorial discrepancy, not a live site correction performed here.
- [Official line80 PDF](https://www.niceairportxpress.com/assets/Ligne-80_FH_2026-10.pdf), validfrom29September2026: some departures do not continue toMenton. Avoid a frequency claim that confuses Monaco service with Menton service; check the actual destination.
- [Tourism transport information](https://www.menton-riviera-merveilles.fr/sorganiser/se-deplacer-sur-la-destination/) supports the station/gardens/seafront relationship; it is not validation of a particular footpath. Exact day-specific rail fares/times and taxi quotes are unverified and omitted.

## Picture, sound and bounded experiments

Alternate a bright legible map with full-frame guide illustrations, short transfer/ticket explanations, coastal geography and a real guide-interface ending. Proposed illustration motion: distinct foreground/background planes, controlled light/sky detail and map anchors continuing through the picture; no nervous integer crop jitter, slide-only rhythm or routine blurred portrait pillars. Exact masks/animation remain a pilot question, not a completed effect.

[Nantes Pixel Path](../experiments/nantes-pixel-journey.md) sources exist under the migrated workspace, including road/layout files and capture recipe. That experiment was a car/taxi route. It does not qualify placing a train on road geometry. Historical capture imports point into an old npm path; runtime/browser availability needs preflight. Real rail/foot geometry and map attribution remain necessary before any capture; no new stack installed.

Two selected trial questions: (1) regional map→station illustration→local walk without losing geographic orientation; (2) edit one route leg/caption without re-rendering unrelated segments. Use existing local rendering where feasible. No whole-queue tool testing or speculative GPU install.

English female voice: offline Supertonic3 F1 from the first Azur guide; shared model located in productions/spot-market-uk-voice-probe-20261015 and its retained manifest hashes verified. First session load stalled in the ONNX vocoder constructor and was interrupted; a second local retry also stalled and was stopped. For the16s pilot only, installed macOS Samantha female English is the temporary fallback. No new model downloaded. Owner additionally requested named places along the journey, train sound and quiet music under explanatory narration. Pilot uses original synthesised rail ambience and a quiet musical sketch; these must not be attributed as real field recordings.

## Next permitted action

Donor review is accepted. Pilot rail geometry extracted from retained OpenStreetMap data:652vertices, approximately30.1km, Nice-Saint-Augustin→Menton. Transfer remains an explicitly schematic tram→walk connection. Last-mile pedestrian geometry remains pending for full production. Finish the short pilot and stop for owner picture/listening review. Full production, publication and audience performance remain separate. No live guide/account edit, new installation or paid call.


## Pilot01 — generated, owner review pending

Private `pilot/pilot-v1.mp4`,16s,1280×720/24fps; `pilot/render.py`,source hashes and `pilot/receipt.json` retained. Full MP4 decode passed; transfer/station/map stills inspected. This uses an original local Pillow/ffmpeg map adapter, not execution of Nantes’ road engine. The pilot tests labelled geographic continuity, separate tram/walk/train modes and low original train/music layers. Voice and creative acceptance remain pending; no full production or publication. The short pilot uses a temporary macOS female voice because two shared Supertonic loader attempts stalled; this does not replace the accepted Azur F1 preference.


## Owner revision — bus first,3November2026

Pilot picture direction broadly accepted; native macOS voice not accepted for the full film. Full production authorised, revised to: direct80coach first as a Nantes-like pixel journey with labelled landmarks/approved illustration inserts; train second using the accepted map; taxi only a fleeting end option.90s revised script retained privately. Preserve historical train-first proposal as superseded, not current.

Official operator timetable confirms Monte-Carlo Casino/Grimaldi Forum and Roquebrune-Cap-Martin stops, with some departures ending beforeMenton. Tourism information identifies the motorway express approach toMonaco. Two public Overpass queries for exact bus relations timed out (one initialPOST rejected406); there is no verified bus driving trace. Therefore the new road sequence is original editorial pixel scenery tied to the verified place order, explicitly labelled stylised/not turn-by-turn. It must not be described as the Nantes geographic renderer or real-world street reconstruction. No exact bus time/fare promise. Retained guide images remain illustrations.

Voice retry diagnosed long model-byte reads on Work, not an established incompatibility: the bounded150s attempt expired reading vector_estimator.onnx. A longer bounded offline load with per-stage logs is running; no installation, paid call or large new download.


## Full draft01 —90s, awaiting owner review

Preferred Supertonic3 F1 restored after fixing the local loader adapter. Twelve English phrases produced offline, no new weights or API charges. Slow Work reads measured about232s for the256MB vector estimator and92s for the101MB vocoder; not a general model-performance result. Exact phrase files/settings/hashes and actual scene windows retained in `film/voice-receipt.json` and `voice-timing.json`. Native macOS voice is absent from this draft.

`film/route-draft-v1.mp4`,1280×720/24fps/90s, is the review candidate, not an accepted/publication master. Original pixel coach scenery with labelled places and approved guide-image inserts precedes the real-rail map. Original synthesised transport bed/quiet music; brief original pixel taxi rank. Ending is a readable original guide-link card, not a website capture. Place names on the rail map derive from retained station coordinates; bus scenery is explicitly stylised.

Bounded reuse check: only changed picture leg13–44s was re-rendered to refine the urban frontage; other picture sections and existing voice timing were reused. Final audio level adjusted without picture rendering. This demonstrates scoped reuse here, not labour savings or exact bus navigation. During owner review retain the accepted pilot, one full candidate and indispensable patch/base evidence; retire extra intermediates after acceptance under storage policy. Human listening/creative approval and YouTube packaging remain next.


## Accepted final and YouTube package —3November2026

Owner accepted the exact complete90s film with restored F1 voice and authorised finalisation/packaging. Picture/listening observations and final selection recorded in the existing journal. Private `publication/` contains the accepted native720p24fps H.264/AAC master (hardlink, no duplicate media bytes), original built-in-generated cover plus1280×720JPEG upload, English title/description with requested short French summary, bilingual English/French tags and English SRT. Cover checked at full size and320px. Exact metadata hashes and cover prompt/provenance retained in `publication-receipt.json`. No YouTube upload/publication or audience-result claim; awaiting owner URL.

Final full decode passed,90s; sound mean−21.7dBFS/peak−2.9dBFS (sample measurement, not integrated LUFS). Subtitles derive from actual speech windows with grouped text, not word-level alignment. Dependency-aware cleanup retained final/recipes/phrase originals/donors/data, retiring only rebuildable generated stems, adjusted WAVs, bus patch/base and inspection frames. Private cleanup plan/receipt list exact files; historical partial-render base is retired, while `render-film.py` remains the full rebuild entry.


## Owner-reported YouTube publication —3November2026

[Published video](https://youtu.be/ih43aF1zeaM), URL supplied by owner. Existing journal and private publication receipt updated with `owner_provided_url` provenance, preserving prepared master/cover/text hashes. Independent public visibility, uploaded file/text identity, site embedding and audience metrics remain unverified. No further upload or account action performed.
