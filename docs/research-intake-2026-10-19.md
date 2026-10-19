# New findings and PlayMCP review —collection closed,2026-10-19

Current release ordering and status: [2026-10-19 release audit](release-audit-2026-10-19.md). Earlier sequencing and waits below are historical snapshots.

Owner-directed order; planning only. No new installation,credit spend,render or release now.

1. Collect the new owner findings,group them,check primary sources and prior arsenal evidence. Exclude unsuitable/duplicate items; prioritise the rest into bounded experiments. Owner closed the four-item batch with Odyssey. Documentation assessment and scoped priorities: [review](research-review-2026-10-19.md). Historical intake claims below remain distinct from that assessment.
2. Make one overall English PlayMCP service review: site screencast,creation workflow and contest pages; three games (Disco Coffee Showdown,SIRTET,Jekyll/Hyde),what each demonstrates,and excerpts from their existing films. Jekyll's delivered book promo can supply its footage. Reconcile actual credits by game from job/account receipts; separate game development from later video costs and unknown totals. Do not present budget caps or partial reconciliations as final spending. Recheck current contest terms/deadlines when producing the review.
3. Select useful trials from the refreshed queue for this actual review. Prepare the English script for owner reading; after receiving the recording,clean/edit it,fit it to the screen capture and excerpts,and build the publication kit. Do not synthesize the owner's voice or assume a new recording already exists.
4. After the review: project audit,consolidated game/virtual-set/review lessons,documentation cleanup,agreed product fixes and a new release after checks. No additional intervening films are queued here.

Jekyll Short: explicitly cancelled by owner. Standalone Jekyll game overview: deferred outside the active sequence,not silently marked delivered or cancelled. Existing films and historical proof records remain intact.

## Audio discovery and sound design

### AUDIO-01 — Openverse fallback search for missing SFX

- Source:owner-supplied third-party recommendation,2026-10-19; [Openverse API](https://api.openverse.org). No API/docs requests made during intake.
- Proposed role:when the local project/music/SFX bank lacks a suitable effect,search for a transition,click,clap,room tone or other scene-action sound; select a result,retain it locally and place it against the shot/action timeline. Existing suitable project assets remain the first choice. The anecdote names Opus5.5; no model-specific qualification is inferred.
- Reported claims,all unverified:anonymous API access without a key or payment;5.2million free audio files,including590,000 SFX and640,000 music tracks;200 anonymous searches per day. These figures are retained as supplied,not a reconciled inventory or current limits.
- Suggested filters,retained literally for later verification:`license=cc0,by,pdm` and `source=freesound,jamendo`. One search per sound type;download the selected result URL using curl into `sfx/`;copy each returned `attribution` field unchanged into `credits.txt`.
- User-supplied instruction template:

> Если в проекте нет подходящего звукового эффекта, выполни поиск через Openverse - https://api.openverse.org
>
> Используй только результаты с `license=cc0,by,pdm` и `source=freesound,jamendo`. Для каждого типа звука выполняй поиск только один раз (для анонимных пользователей действует ограничение в 200 поисковых запросов в сутки).
>
> Подбери наиболее подходящий эффект с учётом действия в каждом кадре, скачай выбранный файл по его URL с помощью `curl` в папку `sfx/` и скопируй поле `attribution` каждого результата в `credits.txt` без изменений.

- Later assessment:verify official endpoint/filter semantics,anonymous limits,actual downloadable file URLs,per-result licence/provenance/attribution,preview vs original distinction,and reuse/caching by sound type. Distinguish finding an asset from choosing a good audible effect and synchronising it correctly. Check overlap with the existing media-use/SFX workflow before adding another integration.
- State at intake:collected only. No experiment priority,registry qualification,installation,API test,asset download,rights clearance or automatic production fallback enabled. Analyse with the rest of the batch after owner closes collection.

## Design references and website capture

### DESIGN-01 — INSANE0777/Awwwards-mcp

- Source:owner-supplied third-party recommendation,2026-10-19; [repository](https://github.com/INSANE0777/Awwwards-mcp). Reported193 stars and TypeScript are intake claims,not a current repository audit. Repository/docs not fetched during collection.
- Proposed role:agent-accessible visual reference search,website design analysis and live-site motion/video capture; possible source of composition/motion references or website-tour materials. Relevance to Framewright and overlap with Lazyweb/Inspo/existing capture tools remain to be assessed.
- Reported capabilities,unverified:search across Awwwards-winning sites/screenshots,design “DNA” and page-structure analysis,live-page recording;local FTS5 index with BM25 across thousands of sites;25+ tools including build verification and motion-video recording;five bundled Agent Skills;Claude Code/Cursor/Codex integration. Authors reportedly position it as a Mobbin alternative without API keys/accounts; equivalence is not established.
- Reported requirements,unverified:Node.js22.13+;Playwright and ffmpeg-static for browser capture. Reportedly fully offline after installation,with a daily npm check and optional self-update via `AWWWARDS_AUTO_UPDATE=1`.
- Later assessment:inspect primary repository/docs/licence and actual tools/skills;separate offline indexed search from live-page/network capture and update checks;verify reference freshness,content provenance/use scope,download/runtime footprint and reproducible version control. Compare capture outputs and useful design evidence against existing tools before queue admission. Do not assume reference access authorises reusing site imagery in published films.
- State at intake:collected only. No installation,MCP connection,auto-update,network/browser capture,capability qualification or experiment priority enabled. Analyse after owner closes the batch.

### DESIGN-02 — AThevon/genjutsu: animation and design-system skills

- Source:owner-supplied third-party recommendation,2026-10-19; [repository](https://github.com/AThevon/genjutsu). Reported569 stars,Python and MIT licence are unverified intake claims; repository/docs not fetched during collection.
- Proposed role:skills for expressive interfaces,animation,microinteractions and coherent design systems. Assess whether they can help author reusable motion/scenes or interactive virtual sets for Framewright,or mainly duplicate existing UI guidance. Video export and timeline determinism are not demonstrated by an interface demo.
- Reported targets,unverified:Claude Code,claude.ai,Cowork;React,Vue,Svelte,Astro,GSAP,Framer Motion,Three.js for web;Jetpack Compose/SwiftUI for mobile.
- Reported modes:`cast` builds one interface;`paint` designs an entire product;`bunshin` builds a website with art-director,builder and reviewer agents (web only). Reportedly proposes an interaction thesis and waits for approval before coding,marketed as anti-AI-slop. This describes the recommendation; no new approval gate or delegated work is activated here.
- Reported installation command,retained as text only:`npx skills add https://genjutsu.athevon.dev -g`. Do not execute during intake.
- Reported example costs:$1.53–5.93 per run and about10.5million tokens for a full bunshin website. Model,pricing,date,context and run comparability are unverified;these are not our budget estimates or benchmarks.
- Later assessment:inspect actual skill contents/licence,installation footprint and model/tool assumptions;compare with Hyperframes,existing GSAP/Three.js methods,anti-slop-review and frontend guidance. Identify a bounded video-relevant question,check renderability/repeatable timelines,and evaluate whether multi-agent overhead adds useful evidence before prioritising. No installation or multi-agent execution is implied by this entry.
- State at intake:collected only;not analysed,prioritised,installed or tested. No spend or capability promotion.

## World models and virtual production

### WORLD-01 — Odyssey worlds as source footage

- Owner's fourth/final finding: [Introducing Odyssey-3](https://odyssey.systems/introducing-odyssey-3). Intended use:generate interactive worlds as material for unrelated videos; the world is a virtual set/source of shots,not necessarily a game product.
- Collection closed by owner: «это было последнее». No account connection,credit spend,stream session or generated footage during intake.
- Documentary review separates Odyssey-3 research preview from the model/recording/simulation interfaces actually documented in the public API. Access,exact model,pricing and publication-use scope remain trial prerequisites; see [assessment](research-review-2026-10-19.md).
