# FILMCRAFT-01 — native lesson edit,save,reopen and bounded correction

20November2026. Owner explicitly authorised this isolated test after the [tool intake](../research/tool-intake-2026-11-20.md). **Technical pass at the tested scope;owner accepted20November2026.** No accepted lesson was used as a working timeline. M1/M2 editable continuation/correction,M4/R05–R07 tool admission;this does not start a course expansion,release,Klap trial or frozen Quixote.

## Exact route

Official FilmCraft CLI0.20.1 universal macOS ZIP downloaded from its tagged GitHub release. Archive SHA256 matches the accompanying official checksum list. macOS codesign verification passed;Developer ID signature:Learning Machines LLC,teamDJ6XS33FX8. No launcher,system installation,global MCP registration or security-setting change. CLI retained under external tools/filmcraft-0.20.1/,with MIT/Apache licences,NOTICE and bundled font notices. Verified ZIP removed after extraction;binary and archive hashes retained privately.

Native headless CLI imports three original6s H.264 teaching slates,each containing a moving progress marker;places them back-to-back;adds two separate18s stereo WAV signal tracks,one editable4s native title and three imported English captions. This tests assembly of prepared footage,not native authoring of all slide animation. Two distinct signal frequencies/channels provide measurable audio-preservation evidence;there is no narration or music-quality claim.

The18s1920×1080,30fps sequence is saved to lesson-before.fcproj. A separate process reopens it. Native graphics.setText changes only LESSON CHECK to LESSON VERIFIED and saves lesson-after.fcproj. Another process reopens that version. Both exports are rendered by FilmCraft itself using its High Quality1080p HD preset,CPU rendering,H.264/AAC,burned captions and SRT sidecars. FFmpeg generated input fixtures and independently inspected outputs;it did not assemble or repair FilmCraft's exports.

## Results and bounds

| Check | Observed evidence |
| --- | --- |
| Save/fresh reopen | Both projects reopen with3video clips,2audio tracks,one native graphic and3captions. No missing/offline media reported. |
| Native export | Each540frames,1920×1080,30fps;container duration18.005s includes audio framing. Both fully decode with strict error detection. |
| Bounded correction | Semantic project diff contains only two save-as project/bin-name changes and one native text value. Before project bytes unchanged. |
| Pixel preservation | All encoded frames120–539 are identical;only frames0–119 change. Native PNG samples at8s and14s match exactly;2s difference is confined to title pixels. |
| Audio | Before/after decoded PCM hashes match exactly. Both signal stems correlate>.999999 with their source channels,without clipping. This is signal alignment/preservation,not voice intelligibility or owner listening acceptance. |
| Subtitle/title readability | Operator inspected actual encoded2/8/14s samples at full/reduced size;native title/captions visible. Tiny fixture footer is not essential teaching text. Not a full-course/mobile readability qualification. |
| Resources | Native renderer reported16.56s before and15.78s after;single observations on this fixture,not a benchmark or speed/savings claim. Paid usage0;local compute and active labour unpriced. |
| Course protection | Original accepted pilot MP4 and19November owner-acceptance receipt retain identical SHA256. No course project/media edited. |

The local adapter initially parsed JSONL as one JSON object;corrected without redoing the saved native project. An initial export invocation used fps inside ExportSettings;FilmCraft rejected it before rendering. Native preset query established frameRate/frameSize semantics;the successful call uses the actual preset. A trial-bookkeeping call initially supplied paths where retained subject IDs were required;fixed in the experiment record. These are retained harness/invocation errors,not hidden native export failures. No assertion of a first-attempt or unattended route.

## Reuse decision

FilmCraft is now a **scoped tested option for prepared lesson assembly,native title correction,save/reopen and1080p export**. Existing FFmpeg/HyperFrames/OpenMotion/Kdenlive routes remain intact. Candidate next use:an owner-selected short lesson fragment needing an editable timeline. Do not migrate the accepted6minute pilot or claim a complete six-lesson course pipeline from this test.

Unexecuted:desktop UI/control bridge,MCP client integration,OTIO/FCP round-trip,source relocation/missing-media recovery,voice production,long camera/phone footage,portrait export,complex transitions,hardware encoding and cross-machine operation. fcproj media references are absolute;the downloadable project files require retained studio sources and are not portable self-contained packages. Reopen after changed source bytes has not been tested.

## Retained evidence and review

Private root:records/filmcraft-01-2026-11-20/. project.json and trial.json use the existing studio journal;ab-review/ retains pinned comparison evidence. sources/,both fcproj files,source commands,preset,signature/checksum evidence,project-diff.json,qa.json and comparison.png are retained. delivery/ uses the unchanged shared course-review template. Its video is a technical fixture;no publication title,cover,voice approval or finished-film count is invented. The original Udemy teaching materials remain the source of truth.

[Shared review method](../../skills/video-production-router/references/preview.md) · [Current work](../next-cycle.md) · [Queue](../experiment-queue.md).
