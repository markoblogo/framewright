# Recipes — tested 2026-10-14

## software-launch

Use for a short product introduction grounded in source code or a landing page.
Start from the full [Brag workflow](https://github.com/latent-spaces/brag), then
follow installed Hyperframes instructions. Check upstream requirements at use time.
The tested renderer was Hyperframes 0.8.157 with Node 24 and FFmpeg.

Inspect real product behaviour/assets; agree a single communication angle; prepare
the storyboard and composition; inspect representative frames and full playback;
render and inspect the final export. Deliver reusable copy/thumbnail as requested.
AsciiTheme used its real UI; AMI used current public branding and imagery.
Use source verification to avoid presenting a preview as a live operational feed.

Tested: 20-second AsciiTheme and 24-second AMI, horizontal 1080p/30fps, instrumental,
accepted by user. Full Brag supports optional narration, but that was not tested
here. Brag-slim and other model-specific dispatch paths were not tested.
User preferred this AsciiTheme presentation to the later retro-computer prototype.

## narrated-montage

Use for a book/product trailer built around existing authorised artwork. This is
a reusable method, not a packaged one-command generator. Do not recreate covers
or invent book excerpts, product capabilities, awards or testimonials.

1. Verify page facts, title/author/translator roles, artwork and CTA. Plan a few
   narrative beats, with the imagery's palette and typography guiding the treatment.
2. Use local [Kokoro ONNX](https://github.com/thewh1teagle/kokoro-onnx) if permitted
   and suitable for the requested language. Check its current voices/licences and
   available environment; use actual speech durations for the scene schedule.
3. Compose in Hyperframes with deterministic timing, restrained camera movement
   and readable type. Inspect cut boundaries; crossfades produced doubled text in
   our French test, so clean cuts worked better for that composition.
4. Mix voice, original/licensed music and only useful effects with
   [opus-sound-layer](https://github.com/Bodila51/opus-sound-layer). It supplies
   scripts and PROMPT.md; do not assume it is an installed root SKILL.md.
5. Run its encoded-file QA using unchanged thresholds, inspect/listen, and retain
   the log. Automated QA is not proof of natural pronunciation or marketing quality.

French test: ff_siwis, fr-fr, speed 0.86; approximately 28 seconds; no extra SFX.
English test: am_michael, en-us, speed 0.94; approximately 34 seconds. These voice
choices worked for these exports, not a universal language/voice recommendation.
Final audio was approximately -18 LUFS; music roughly 16–17 LU below speech.
These are measured results, not mandatory targets for every platform.

Good Dogs: page-turn effects failed audibility; replacement book-placement sounds
improved the result; the middle effect still failed and was removed. Two remaining
accents passed. Kenney recordings used here were CC0; a full sound library was not
tested. Do not turn this into a blanket licence claim for other libraries.
Visual/editor-structure advisory warnings are separate from the zero-warning
sound QA reports. Windows/Linux portability has not been tested.

## short-teaser

Use the established product/series composition for a short hook and CTA. The
six-second Good Dogs edit passed local audio QA; no audience A/B test was run.
Preserve the longer version as a separate deliverable. Shorts/vertical formats
need their own reframing and verification; horizontal success does not prove them.

## object-prototype

[Anatomy](https://github.com/wheresryan22/anatomy) already supports Codex. The test
adapted its bundled desk-computer example; it was not a newly authored 3D machine.
Replace wall-clock/random behaviour with deterministic seek(t), using one event
ledger for picture and audio. Test seeking out of order. Fix geometry issues with
the supplied line checker and inspect frames before adding many effects.

Five adapter tests and the visual checks passed. Combined encoded sound QA failed
with 22 audibility failures and 38 picture-motion warnings; global picture-motion
checks may not capture tiny key movements well. Do not declare the sound mix passed
or disable thresholds to compensate. The user stopped this direction, preferring
the earlier AsciiTheme promo. Historical-photo reconstruction, calibrated physics,
general 3D beta and agent swarms remain untested.
