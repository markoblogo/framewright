# Working here

- Read README.md; use docs/start-here.md for start / continue / correct and docs/next-cycle.md for current work. Then load only the selected recipe/evidence, not all experiments or docs/history/.
- For priorities or new ideas/tools/orders, consult docs/roadmap.md; link to an existing milestone/task and preserve active scope and owner pauses.
- On resuming an existing production, run `project.py brief PROJECT.json`; preserve explicit waits and distinguish its proposed next step from execution authority.
- This is a methods/skills library, not a renderer or automatic publishing service.
- Before proposing or reviewing video, read only applicable rules in docs/video-taste.md; apply them in the existing brief/handoff and capture reusable owner corrections using skills/video-production-router/references/video-taste.md.
- Honour explicit tool choices. Prefer tested scope over tool novelty.
- Keep failures, human preference, technical QA and publication separate.
- Do not label structural checks as model evaluation or successful rendering as audience validation.
- Do not commit media, caches, models, credentials or copied upstream code/skills.
- Follow docs/storage-policy.md: keep studio files on the external disk, retain accepted finals/recipes instead of all drafts, and sanitize after production or before large downloads. Internal storage is temporary scratch only.
- Creating a video is not permission for paid API calls, account grants or public uploads.
- Use `python3 scripts/validate.py`; no new video experiment is needed for documentation changes.
- At completed-film or executed-trial closeout, update docs/public-evidence.json with one source-linked case per story/trial; aspect/language variants and retries are not new entries. This keeps visitor-loaded site counts current. See docs/site.md.
- At executed-trial/production closeout, update the matching application in skills/video-production-router/references/arsenal-facets.json from retained sources; keep style/technique/version, technical checks, five quality observations, owner decision and resource unknowns separate. Follow references/arsenal-search.md; discovery annotations do not qualify planner providers.

- For review and publication packages,use delivery.py and the fixed page/check procedure in skills/video-production-router/references/preview.md. Change package data per film;update the shared template only for a concrete requested improvement. Publication UI is English in the FW site black/silver style. Desktop:equal-height YouTube/TikTok previews plus one download column;YouTube copy below both previews,TikTok copy below downloads. Mobile order:YouTube preview,TikTok preview,all downloads,YouTube copy,TikTok copy. Optional/missing assets remain supported. Run delivery_check.cjs in its default shared-baseline mode:unchanged template/server/browser reuses player proof without launching a browser. Do not manually repeat playback/seek tests for each film;force --full-player after a reported player failure. New media still require their own integrity/decode/aspect checks.

- Delivery text uses per-field copy buttons with visible confirmation:YouTube titles/description/tags;TikTok caption/first comment. Never add publication-text downloads or TikTok subtitle/title fields. The TikTok player container itself must be portrait.
