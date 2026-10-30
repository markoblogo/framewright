# Agent video toolkits — adoption plan

Reviewed 30 October 2026. Research only: no installation, model download or upstream
skill activation. Free/macOS-first policy and one heavy operation at a time apply.
These candidates extend the existing journal/executor, not a second studio.

| Source / adoption level | Useful scope | First bounded experiment / stop condition |
| --- | --- | --- |
| [OpenMontage](https://github.com/calesthio/OpenMontage) — architecture reference, optional external trial | Backlot read-only production view; source-corpus retrieval | OM-BOARD-01: existing original fixture → derived stage/version/wait view; no mutation. OM-CORPUS-01 later: 3–5 permitted clips against SOURCE-01 baseline. Confirm download size and resources first. |
| [ffmpeg-skill](https://github.com/kajisho5/ffmpeg-skill) — candidate bounded local adapter | Machine-readable operation contract, scene cuts/contact sheets, extraction/join/verification | FFMPEG-OPS-01: retained Afterimage GIF-derived source → three-scene detection/contact sheet → two short excerpts/join → decode and duration check. Preserve accepted film. |
| [awesome-claude-video-skills](https://github.com/zhuyansen/awesome-claude-video-skills) — discovery reference | Find specific missing techniques, deduplicate by canonical repository/version | VIDEO-SKILL-DISCOVERY-01: assess one candidate before testing. Shortlist: continuous camera transitions in [onetake](https://github.com/feitangyuan/onetake), painted animation in [ClaudeAnimationBase](https://github.com/JohnHeibel/ClaudeAnimationBase). No bulk import. |

## Evidence and restrictions

OpenMontage reviewed revision: `195eab24478dc9363326aec437aefc3701635ddf`.
AGPL-3.0: retain links and architectural observations; copying/integration needs a
separate licence review. The reviewed CLIP helper selected CUDA or CPU, not MPS;
corpus dependencies/model downloads are substantial. Documentary montage was beta
and Remotion-dependent. Its warning-mode budget is not our spending authority.
Do not treat a working dashboard as successful end-to-end production.

ffmpeg-skill reviewed revision: `8b6c30528d70b262d8211c6ad0cf88b0de93d8c2`.
MIT source, Python/FFmpeg local operations; MCP is optional. Host inspection found
`scdet` and `loudnorm`, but did not list `drawtext`, `subtitles` or `zscale`.
Gate each operation against the actual build; no automatic replacement/upgrade.
Audio energy or scene-cut rankings do not establish semantic understanding.
Qualify only tested operations after output, failure and repeatability checks.

The discovery catalogue's list licence does not cover every linked tool. Its
benchmark and safety labels are upstream claims, not Framewright qualification.
A similarly named `smwbev/framewright` listing is a different repository.
Review shortlist licences, dependencies and current suitability individually.

## Roadmap placement

All four experiment IDs support M4/R05, with R09 documentation. OM-BOARD-01 can
support M2 recovery visibility; OM-CORPUS-01 connects to SOURCE-01/R02. First finish
release closeout and recovery limitations, then select one fitting trial. Any
later executor integration needs pinned inputs, explicit outputs, timeout/failure
controls and a separate human review. Research does not authorize execution.
