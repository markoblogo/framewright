# Bruno Simon — roads optional

28 November 2026. Owner-supplied screen recording of [Bruno Simon’s portfolio](https://bruno-simon.com/), edited into one 98-second landscape YouTube review. The owner explicitly excludes assessment of the site as a production tool. No portrait adaptation, new experiment or tool candidate. Creative, listening and cover acceptance remain pending; no public upload.

## Story and retained source

Bruno Simon describes himself as a creative developer, mostly web. His portfolio invites visitors to drive around and discover his work. The film is a personal tour: portfolio name, playful objects, sensitive keyboard handling, road obstacles and exploding crates, then escape into the sea. Handling and the non-sinking car describe this recording and the owner’s experience, not a universal physics or performance verdict. Facts and source links are retained in `qa/claims.json`.

Private production: `productions/bruno-simon-portfolio-review-2026-11-28/`. The original 391.968-second, 2940×1912/60fps Desktop recording is unchanged; a hashed copy is retained at `source/screencast.mov`, with provenance in `qa/source.json`. The source was sampled every eight seconds across its full duration; 49 frames were inspected. This is not a claim of full real-time source playback. Initial unrelated browser material is not used.

`edit/plan.json` retains eight source intervals: 84–93, 130–141, 173–183, 216–229, 279–289, 356–368, 45–63 and 374–389 seconds. Each uses a 2816×1584 crop at 112,320, scaled to 1920×1080. Browser chrome is removed; native site HUD remains. All driving stays at 1× speed, with no interpolation, digital pan or zoom. The sea insertion is an earlier night segment: this is a curated tour, not a continuous chronological playthrough. Five brief editorial labels support the story; narration captions are separate SRT with approximate phrase timing.

## Sound, cover and checks

Existing local Kokoro ONNX 0.6.1/model v1.0, af_heart English at speed 1.0. Nine measured takes fit their scene budgets without time stretching. `edit/voice.py`, `voice-cues.json` and `voice.wav` retain the script and placement. Voice identity, pronunciation, cadence and mix quality still need owner listening; duration and decode do not establish that approval.

Owner-stock **Ethereal Void**, SHA256 `c1b42b75599a49f3781f3574a89368f99106fd08c08262fbf1678976bacb1217`, excerpt 32–130 seconds, provides a continuous quiet bed. Target bed RMS .036 before .3 ducking during narration, 180ms smoothing, music-only 1-second entrance and 2-second ending fades. Original capture audio is removed. `qa/audio-recipe.json` retains the mix; stock reuse authorisation is not a universal provider or client-rights grant. Existing compute and labour are unpriced; no paid requests, new models or installs.

Cover uses a real frame at source time 376 seconds, with a further thumbnail crop removing the upper-right HUD. Title “THIS IS A PORTFOLIO?” and “ROADS OPTIONAL” badge preserve the sea/car punchline. Native and 480px-wide cover were inspected. Source frame and `edit/cover-recipe.json` are retained; no generated scenery.

Final master: 98 seconds, 2940 frames, 1920×1080/30fps H264 with AAC 48kHz stereo. Full decode passed. Sixteen encoded frames, two per shot, were inspected for crop, visible car, readable labels, obstacles and water during the sea narration. Initial QA found that the sea line preceded actual water; two picture shots were repaired. Failure frame, initial plan/hash and timing correction remain in `qa/`. Voice, cue schedule and mix hashes stayed unchanged, proven by `qa/correction-protected-check.json`. This sampled check does not imply full human audiovisual playback or owner approval.

## Delivery and reuse

Standard [local Framewright page](http://127.0.0.1:8969/review.html), `package/delivery.json`, `bruno-simon-review-youtube-v1.mp4`, `cover-youtube.png` and separate `youtube.srt`. Titles, description and tags are on the page; the description credits Bruno Simon and links to the portfolio. Standard builder integrity checks and the default smart shared-player check are retained in `package/delivery-receipt.json`. No automatic browser opening or external publication.

`project.json` registers the chosen files, recipes and check evidence with an explicit owner-review wait. The existing FFmpeg/Pillow source-editing and Kokoro route is reused; no 3D creation or new tool qualification. Matching arsenal applications and music use are recorded; primary ranks and the test queue remain unchanged. Intermediate shot exports and inspection frames are cleanup candidates after owner review; source, final recipe and master remain retained.

## Owner-reported publication — 28 November 2026

[YouTube](https://youtu.be/_ziZIZ9nj0w). The owner supplied this publication link. Independent visibility, uploaded-file identity and metrics remain unverified; no separate creative, listening or cover appraisal is inferred. Earlier preparation paragraphs are historical. Retained master, cover and package are unchanged.
