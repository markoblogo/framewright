# Auto-Editor for speech-led lesson pacing

Internal trial on 22 November 2026. A 58-second, 960×540 synthetic-data lesson
excerpt was prepared from retained Transit Speed inputs. No publication or
account action. Tool: Auto-Editor 31.9.0, upstream macOS arm64 binary with
matching release SHA-256. [Release](https://github.com/WyattBlue/auto-editor/releases/tag/31.9.0)
· [Export skill reference](https://github.com/WyattBlue/auto-editor/blob/master/skills/auto-editor-export/SKILL.md)

| Route | Result |
| --- | --- |
| Original mixed audio, threshold 0.038, 0.20 s margin | About 57.6 s retained, as one interval. Music fills the pauses in this excerpt. |
| Dry voice, same threshold and margin, fixed 24 fps | 35.35 s. Three source intervals. A screen-reading hold was cut along with empty pauses. |
| Dry voice plus one protected range (43.2–46.6 s) | 38.68 s. The useful table hold was restored. MP4 and Kdenlive projects exported. |
| Hand-selected cuts, same dry input | 39.68 s. A three-range FFmpeg reference preserved the visual hold with wider speech padding. |

One explicit keep range was required to preserve the visual pause. The
fixed-rate dry scan took 0.68 s elapsed. The manual reference MP4 encode took
4.72 s elapsed. These operations measure different work. No matched active
editing time or audible comparison with an independent reviewer was obtained.
The four review exports completely decoded. Kdenlive's bundled MLT rendered
the protected .kdenlive project to a 38.72-second MP4 with picture and audio.
The graphical editor stayed in first-run setup, so interactive reopen,
editing, saving and export were not confirmed. The keep range was applied
before export, in Auto-Editor.

**Owner review.** The 35.35-second dry-voice cut was preferred. Viewers can
pause the player to read the table, so the extra hold was optional in this
lesson excerpt. For similar pauseable screencasts, review the compact cut first
and add a hold when it serves the lesson.

Keep Auto-Editor as a scoped trial for a dry voice or dialogue stem, with an
editorial check before accepting its cut list. A voice-only rule does not
detect which visuals deserve a pause. No ranking promotion or speed claim.
Private recipe and results are in
`productions/transit-speed-mandok/tutorial-2026-11-22/auto-editor-trial/`.
