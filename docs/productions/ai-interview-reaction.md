# Who’s Interviewing Whom? — dual-panel reaction edit

16November2026. Owner-selected adaptation of a [publicly playable interview clip](https://www.yaplakal.com/forum3/topic3141903.html). The brief preserves its original English dialogue, adds only brief emotional viewer reactions, replaces baked Russian captions, finishes the low-resolution picture and prepares YouTube/TikTok packages. No agent publication, purchase, paidAPI, commit or release is authorised by this production.

## Source and selected route

The retained source is428×480/60fps,118.793s with stereo audio: two428×240 panels, recruiter above and candidate below. The source post presents it as an AI interview. Original creator, system/model, authenticity, independent reuse grant and audience results remain unverified. Public playback/download is recorded separately from those questions. No login or account creation was needed.

A six-second InShot enhancement fixture produced1080×1920/30fps output with a central dual panel and duplicated background fill. At the inspected sample the operator found waxy/stylised faces and rejected it for the full film. The processing-start transition was only partly observed, so no fully unattended enhancement is claimed. The selected route uses proportional local Lanczos enlargement, low-strength spatial cleanup, restrained contrast/saturation and sharpening. Larger canvas dimensions do not establish recovered HD detail.

YouTube16:9 follows the speaking/action focus with upper/lower-panel cuts; TikTok9:16 retains both panels proportionally in one independent layout. Opaque English bands replace the source Russian text. English reading captions were edited from provisional local tiny.en ASR, visible source captions and context; they are not a certified verbatim transcript. No nonuniform stretching or new facial generation is used.

## Sound and timing

One completed Google AI Studio UI Knox take supplies four cut-only viewer remarks: “Wait…what?”, “CEO?”, “He folded.” and “So…she is hired?”. The owner saved the WAV; this is an assisted export, not an autonomous-production test. The unused “Already?” phrase stays out. Cost was not displayed; no purchase or paidAPI was used.

Original words, speech speed and pitch are retained. Source-clock pauses46.00/81.30s are extended0.4/0.6s so reactions fit without interrupting the original exchange. A short final held frame provides the ending remark. Both requested exports target123.0s/3690frames/30fps and use one shared48kHz stereo AAC mix. Levels, ASR and playback state do not constitute acoustic listening or owner approval.

## Recipe, packaging and evidence

Private `productions/ai-interview-reaction/` keeps the source/hash receipt, exact voice, ASR candidates, rejected InShot probe, timeline/caption/panel-cut JSON, editable local build and cover/package scripts, native/reduced inspection frames and first full candidate under `full-v1/`. During assembly, an empty near-end freeze and a caption-layer EOF mismatch were caught before delivery and corrected; explicit final frame-count checks are required. No source or paused-film files were removed.

Covers use actual source stills and local typography, in the film's charcoal/teal/amber palette. Publication copy includes a main YouTube title plus two alternatives, fuller description/source credit/tags/comment and TikTok caption/hashtags/first comment. Individual MP4, JPG, SRT/VTT and text downloads are prepared without ZIP. Source attribution does not create a reuse grant or prove the depicted system.

**V1 technical evidence before owner review:** both actualMP4s fully decode,123.0s/3690frames/30fps with square pixels and matching decoded48kHz stereo audio. Measured loudness is−15.80LUFS/−2.00dBTP. Twelve encoded samples per aspect were inspected at640×360/270×480, plus native frames; English bands and the selected source framing are readable in those samples. Native browser playback and seek controls were exercised without player errors; that state is not acoustic listening or continuous creative approval. At that handoff, owner acceptance was pending; the subsequent scoped decision is below. Publication and uploaded-file identity remain unverified. This is one production case, not two stories for its aspect variants and not a new general InShot/ASR qualification. The exact private delivery manifest and QA reports govern availability.


## Owner correction —landscape picture-in-picture,16November2026

The owner explicitly accepted the vertical version. The landscape edit lost some conversational context when showing only one screen. Requested correction: preserve the current film and add the other participant in a small corner window, as in a real video call. This is a case-specific application of [VT-FRAME](../video-taste.md#vt-frame--keep-the-subject-and-action-visible-in-each-format), not a requirement that every film use picture-in-picture.

Landscapev2 uses the exactv1 movie, captions included, as its main compositor input. A448×252 upper-left inset follows the opposite participant from the already retained source-derived timeline; it swaps with the original main cuts. Its English role strip masks the baked Russian text. No new speech, recut or timing change. The123-second/3690-frame output fully decodes and copies the exact existingAAC packets. The accepted portrait and all19pre-existingv1delivery files remain hash-identical; thev2package uses that same portrait and existing covers. The baseline is retained.

Actual native and640px encoded samples were inspected, including the first rapid view switches and final reaction. The inset stays clear of faces, the foreground action on the right and the main English caption band. Re-encoding produces small pixel differences outside the inset; sampled mean absolute differences are0.0375–0.169on an8-bit scale, rather than a claim of byte-identical picture. Source selection, retained invariants and checks are pinned in private `qa/revision-v2/`; editable recipe is `recipe/pip-v2.py`. The full-range request is retained; no claim is made that the30-second comparison helper reviewed the whole film.

**V2 handoff status before the publication report:** TikTokv1accepted and unchanged; landscapev2technical/sampled visual checks pass, owner revised-picture acceptance was pending. Publication packages are prepared as individual files; only the YouTube description's layout sentence was updated. No agent upload, new trial count, cleanup, commit or release.


## Owner-reported publication —16November2026

- YouTube: [owner-supplied publication URL](https://youtu.be/-ZjoRw8TY_Q). Intended prepared master: landscapev2with the second-participant inset.
- TikTok: [owner-supplied publication URL](https://vt.tiktok.com/ZSpgS2TEn/). Intended prepared master: accepted portraitv1, unchanged in thev2package.

Both URLs were supplied by the owner with `owner_provided_url` provenance. The private `full-v2/publication/owner-publication.json` preserves receipt date, actual intended master byte counts/hashes and the frozen prepared-manifest hash. Independent visibility, uploaded-file identity, metrics and reuse rights have not been checked. The links do not create an additional explicit creative/listening/cover approval for the revised landscape; the earlier vertical acceptance remains recorded. Media and prepared package hashes were preserved. No new render, cleanup, agent upload, commit or release was started to record publication.

## Documentation and retention review —16 November 2026

The current recipe is retained in private `recipe/README.md`, with the v2 PiP
instructions and `CLOSEOUT-2026-11-16.md` naming the selected files and rebuild order.
The 17-file `full-v2/manifest.json` was checked against retained bytes; its prepared
status and original hashes remain frozen. The later publication receipt supplies
the owner report without rewriting that package.

Keep `full-v1/youtube.mp4` and `sources/dual-panel-timeline-v1.mp4`: the current
PiP recipe directly consumes both. They are indispensable inputs, despite the
earlier version number/cache origin. Original source, exact Knox take, caption/cut/
timeline JSON, rejected enhancement probe, current masters, covers/copy/subtitles
and QA/provenance remain retained. The previously empty journal file bindings for
source, viewer voice and delivery manifest are now bound to their existing files;
this records retention, not a new render or creative approval.

Reusable lessons: retain the second speaker's context when the edit requires it;
mask source text before enlarging; use proportional framing; distinguish enlargement
from recovered image detail. The sampled technical checks, accepted portrait and
owner-reported landscape publication remain separate observations. Missing revised
landscape creative/listening approval is not manufactured. No media were deleted
during this documentation pass; dependency-checked retirement is a separate action.
