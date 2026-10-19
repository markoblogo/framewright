# Disco Coffee Showdown: game → narrated video

2026-10-17. Owner-authorised game closeout and English presentation;no software release.
[Published game](https://playmcp.io/g/g_4FzN0mD8) · [game case](../../docs/experiments/playmcp-coffee-showdown.md).

## Delivered scope

88-second1080p30 game overview:opening title,actual scripted gameplay with original
game sound,two complete26-second routes,both finales and side-by-side comparison,
Supertonic3F1 English narration,PNG/JPG thumbnail,SRT and YouTube title/description/
chapters/tags. The supplied generated concept illustration is used in title cards
and thumbnail;the thumbnail is not a gameplay screenshot. Owner supplied the [published film](https://youtu.be/WLBxcM5JQ3U) link on2026-10-17;verification:user_provided_url.

## Production and limits

Capture the running local rev12 Canvas with captureStream and MediaRecorder;
connect SlicePlayer's final safetyTrim bus to the same recorder. Log scripted
inputs,song-time state and recording offsets. Shoot and hold takes prove different
outcomes. This is a tested capture adapter for this exact browser game,not a
universal game recorder or a human skill demonstration.

MoviePy2.1.2/Pillow11.3.0 compose static artwork once;FFmpeg edits recorded footage,
normalises the mixed soundtrack and muxes AAC. Supertonic uses pinned local model,
config and style bytes;no downloads or cloud TTS. Preserve the original captures
and voice files alongside hashes,rebuild scripts and QA in private storage.

The slow full-frame MoviePy pass was stopped. WebM packet warnings and a one-frame
comparison shortfall were retained and resolved in the converted delivery. An
initial mix buried narration more than intended;stronger ducking improved measured
voice separation. Full decode,encoded audio measurements,2640frames,27visual samples,
video-stream identity and thumbnail checks are retained in [evidence](evidence/disco-coffee-game-overview.txt)
and [output hashes](outputs.json).

Final film listening and creative approval remain pending. The game's music/finale
acceptance does not automatically approve the new film. The owner-supplied
[YouTube link](https://youtu.be/WLBxcM5JQ3U) is recorded with user_provided_url provenance;independent
playback and audience response are not verified. The next service review uses owner-recorded voice;
other engines and unrelated virtual-set films still need separate tests.

See [game-engine workflow](../../docs/workflows/game-engines.md) and
[agent skill](../../skills/game-engine-production/SKILL.md). This manual adapter does
not add a selectable engine provider or fresh planning-model qualification.
