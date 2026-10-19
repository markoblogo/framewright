# Four findings: assessment and experiment priorities

Current release ordering and status: [2026-10-19 release audit](release-audit-2026-10-19.md). Earlier sequencing and waits below are historical snapshots.

2026-10-19. Collection closed. Primary-source documentation review only: no new installation,MCP connection,asset download,world generation,render or spending. Existing23 authored exports are unchanged. All four remain candidates; prioritisation below is our product judgement,not a runtime benchmark. Individual modes/use cases are excluded where they do not serve video production.

| Within-batch priority | Candidate and decision | First useful question | Placement |
| --- | --- | --- | --- |
| P1 | Openverse: retain for missing SFX | Can the agent find,admit,credit and place three useful effects? | Overall PlayMCP review,only if local bank lacks them |
| P2 | Awwwards-mcp: retain motion capture/evidence subset | Does one recorded page plus filmstrip help make a better website-tour shot than our retained capture route? | Optional bounded PlayMCP walkthrough trial |
| P3 | Odyssey: retain as a strategic virtual-set experiment | Can a controlled world session yield an editable,usable shot with exact model/cost/provenance? | Separate world-material task after the review/release; access-gated |
| P4 | genjutsu: retain cast only for first trial | Does one authored effect improve a repeatable video scene? | Optional chapter-card trial; otherwise later |

## Openverse — useful acquisition layer

The [primary API description](https://api.openverse.org/v1/) documents anonymous access,audio search and licence/source filters. API-root browsing returned403 in this research tool; search-indexed primary API docs were readable. No live audio-search request was executed. Therefore runtime reachability and supplied200-searches/day claim are not qualified. Do not use the supplied inventory counts as verified evidence or hard-code quotas;inspect actual headers/errors at trial time.

Keep the suggested `license=cc0,by,pdm`/`source=freesound,jamendo` as a proposed filter set to verify against current providers. Preserve result metadata and raw attribution. [CC BY4.0](https://creativecommons.org/licenses/by/4.0/) also requires appropriate credit,a licence link and change indication: retaining the raw field does not alone prove the final credits are complete.

Trial proposal:three needed sound types,one initial query each,one selected file per type. Bound download sizes before transfer;log URL,creator,licence/version,landing page,hash and edits. Accept only if files decode,credits accompany the publication kit,and an operator checks audible suitability,timing and speech masking. Reuse the project bank before another search. Exclude automatic indiscriminate downloading and the anecdote's model-specific performance claims.

## Awwwards-mcp — capture/evidence rather than another full UI stack

The [upstream README](https://github.com/INSANE0777/Awwwards-mcp) documents `record_site_motion`,filmstrips/Motion Evidence Sheets and GSAP/pose helpers. It also describes live scraping,on-demand detail fetches,CDN screenshots,seven-day refreshes and npm checks. Fully offline is not an accurate description of every operation. The [MIT software licence](https://github.com/INSANE0777/Awwwards-mcp/blob/main/LICENSE) does not relicense reference-site assets;upstream limits their use to inspiration and warns against republication.

Trial proposal:pin a release,leave self-update off,record one public PlayMCP page at a fixed viewport and scripted scroll. Compare the saved WebM/filmstrip against our known capture route using the same page/action. Check preloader handling,missing content,scroll pacing,frame timing and caption-safe composition. Use the tool for evidence and permitted own/subject-site footage;exclude bulk indexing,clone-and-rehost workflows and third-party award-site imagery as automatic production assets. Lazyweb/Inspo remain reference-search alternatives. Native capture and renderer QA still apply.

## Odyssey — promising world footage,model access unresolved

The owner's [September introduction](https://odyssey.systems/introducing-odyssey-3) is followed by an [October8 launch/research-preview announcement](https://odyssey.systems/meet-odyssey-3). The [API introduction](https://documentation.api.odyssey.ml/) still describes Odyssey-2 Pro. Record the actual model used;do not label a trial Odyssey-3 without that evidence. Owner clarification:the goal is usable world footage across Odyssey and later other providers,not access to one particular model. An available earlier model can satisfy the first creative trial.

The SDK documents [MP4 recordings plus event logs](https://documentation.api.odyssey.ml/sdk/javascript/recordings) and [scripted asynchronous simulations](https://documentation.api.odyssey.ml/sdk/javascript/simulations). These are useful candidate routes for reusable footage;they do not demonstrate an editable mesh/scene export or exact shot repeatability. [Session guidance](https://documentation.api.odyssey.ml/faq) requires explicit disconnect/cleanup. [Published API terms](https://odyssey.systems/legal/api-terms) refer to Odyssey-2 and leave exact model entitlement,applicable order/fees and intended publication use to resolve before a paid trial. No current price or account allowance was verified. Unrelated Odyssey-branded streaming products are excluded from sources.

Trial proposal after access/use/budget checks:use whichever accessible Odyssey model fits the shot,then later compare other world providers;one original10–15s environment,one camera-direction request and one object-action request. Save exact model,inputs,timing,recording/events,actual usage and failures. Inspect continuity,geometry drift,control latency,capture quality and whether at least one3–5s shot survives editorial review. Compare interactive recording with scripted simulation only if the exact account supports both. Never show generated Odyssey footage as a PlayMCP feature. Exclude robotics/driving benchmarks from our qualification.

## genjutsu — narrow creative aid

The [README](https://github.com/AThevon/genjutsu) and [cast docs](https://genjutsu.athevon.dev/docs/cast) describe interaction-led creative coding. [MIT](https://github.com/AThevon/genjutsu/blob/main/LICENSE) is confirmed for the software with vendored notices. The [bunshin documentation](https://genjutsu.athevon.dev/docs/bunshin) estimates millions of tokens and hours for whole-site work;reported example costs are neither our budget nor a general performance measure.

Trial proposal:cast one original5–8s chapter/three-game card in the review's existing visual direction. Use approved original assets;translate any scroll/input-driven motion into the renderer's absolute-time contract. Retain a replayable scene,inspect fixed seek positions and final encoded motion,and measure actual authoring effort. Exclude mobile modules,whole-product paint and multi-agent bunshin from the immediate video queue;they do not answer this shot-level question. No new skill is installed or invoked by reading its documentation. Existing Hyperframes/GSAP/Three.js and visual-review skills remain the baseline.

## Active programme

For the overall PlayMCP review,prefer Openverse if a sound is missing and a bounded Awwwards capture comparison if it adds value. Do not force four new tools into one film. genjutsu is optional;Odyssey belongs to the next virtual-production block. Proposed tests need a concrete shot,limits and applicable access/rights before execution;queue admission alone is not spend/install authority.

The new-findings task is complete. Next:overall English PlayMCP review with site/contest screencast,three games and receipt-reconciled costs,existing film excerpts,and a script for the owner's recording. Jekyll Short stays cancelled;standalone game overview remains deferred. After review:project audit,documentation/accepted fixes and release. No new film or release was made during this assessment.
