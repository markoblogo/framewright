# Search the arsenal before choosing a chain

`search.py` is an offline discovery interface over the capability registry and
review ledger. It finds scoped tools, manual recipes, components and candidates;
only compatible registry providers enter the existing block planner. It installs,
executes and publishes nothing. Python standard library only.

## Find and narrow

```sh
python3 skills/video-production-router/scripts/search.py --list-filters
python3 skills/video-production-router/scripts/search.py --task narration --language uk --evidence tested --rights commercial --format markdown
python3 skills/video-production-router/scripts/search.py --task editing --evidence tested --format markdown
```

Use `--query TEXT` for literal name/ID/task/retained-scope text, not a semantic model
search. `--task` uses the listed task IDs; `--style` is an exact indexed affordance,
not a promise of aesthetic quality. `--input` uses planner input kinds. An absent
style/input/language entry remains unknown rather than being guessed from a name.

`--language` filters explicitly requested narration/speech tasks. To request a
narrated picture chain, add `--feature narration`. Song-language support is not
indexed; a language-filtered song query returns no confirmed match. This is not a
claim that the service cannot sing that language. Visual font/glyph coverage is
separate from speech language. Without a language filter, a voice result lists its
scoped tested/documented languages; it does not assume they all have equal quality.

`--evidence tested` accepts retained task/component evidence, not every function of
a tool. `documented` (default) also admits documented features. `any` exposes queued,
unknown or failed diagnostic records: read their disposition/coverage. They are not
promoted to usable providers. Piper and Supertonic stock are excluded from default
narration after their recorded quality limitations. Use `--tool supertonic3` or
`--include-fallbacks` to inspect a reserve record. Discovery does not select a voice
for a chain: an intentional reserve example needs `--voice supertonic3`. The
[owner voice policy](../../../docs/voice-selection.md) remains authoritative.

Openverse is a **tested manual SFX acquisition workflow** after the SSI pilot and
owner acceptance on 2026-10-20. Find it with
`python3 skills/video-production-router/scripts/search.py --task acquisition --tool openverse --evidence tested --format markdown`.
Its tested scope covers discovery, per-item admission, download and manual montage
use; it is indexed only under `acquisition`, not generic audio mixing/QA or music.
It is not an automatic planner provider. Reuse retained effects first,
preserve source/licence/attribution and check the final mix. Music discovery and
automatic semantic placement remain untested. [Trial](../../../docs/experiments/ssi-logistics-illustrated.md).

## Compare proposed picture chains

The retained example deliberately names the reserve voice. Omitting that choice
leaves narration unmet; it does not silently fall back after a quality rejection.

```sh
python3 skills/video-production-router/scripts/search.py --task video --input book-art --style paper-cut --feature paper-cut-regroup --feature narration --feature still-export --language uk --rights commercial --evidence tested --combinations --voice supertonic3 --format markdown
```

[Generated result](https://github.com/markoblogo/framewright/blob/main/examples/plans/arsenal-search-paper-uk.md) for this
command proposes Remotion + Supertonic3. A complete chain can exist even when no
single tool covers every requested feature. Task/style/input filters apply to the
picture owner; compatible voice/finishing layers may supply missing features without
sharing its visual style. Every selected layer must pass the rights filter.

Picture combinations require `--input`; narrated combinations require an explicit
`--language`. Task presets add a core requirement (e.g. diagram→workflow-diagram,
3d→staged-3d); `--feature` adds effects/deliverables, including glossary aliases.
Default context is1920×1080/30fps; use `--width`, `--height`, `--fps` for another
profile context. Unrecorded format evidence must not be called tested.
Manual records describe their retained method scope; their format compatibility is
not evaluated by the automatic solver because they are not solver providers.

The search reuses `plan.py` coverage/evidence/minimal-chain rules, not a second
chain solver. All combinations are proposed and require integration checks; related
component experiment IDs do not qualify the combination. Native failures remain
failures when a companion supplies a fallback (e.g. Flute + FFmpeg still extraction).
Only picture/editing task families use this solver. For audio-only, preproduction
or manual recipes, discover the entry and follow its scoped guide instead.

Use `--tool ID` to keep an explicit picture owner and `--voice ID` for an explicit
voice in a narrated combination. Incompatible choices stay blocked; no silent
substitution. `--include-fallbacks` broadens discovery only; it does not make Piper
a default voice in combinations. New provider integration is separate from indexing
a manual recipe. Cloud music stays outside picture chains: search `--task music`
or `song`, then use the independent music workflow/gates, never a TTS substitute.

## Rights and accounts

`--rights commercial` excludes recorded noncommercial-only and unknown classes.
Returned conditional entries still require exact licence/model/build/account,
asset and intended-use review. `noncommercial` also admits records with retained
noncommercial-only terms; `any` does not filter those classes. Nothing grants rights
to source media, clears a track or authorises publication. Suno/Flow account and
asset history remain unresolved until inspected. `--allow-paid` admits only declared
paid capabilities; it is not spending authority or a licence/subscription grant.

Discovery classes are bound to the retained licence note's hash. If that note
changes, the class becomes unknown until reviewed. This guards metadata drift;
it is not fresh upstream legal verification. Source rights/permission gates remain
independent, and stale external terms cannot be detected from local metadata alone.

## Output and maintenance

JSON is the default; `--format markdown` produces a readable comparison. Results
include task facts, evidence/disposition, limits, rights conditions and references.
No-match counts explain filtering; `--explain` includes all per-tool exclusions.
`--limit` controls displayed results/chains without changing total counts. An empty
or blocked result is valid; do not relax a filter or execute a trial automatically.

Keep capability facts in `tools.json`, outcomes in `review-ledger.json`, and only
search tags/retained-rights classes in `arsenal-facets.json`. The Three.js component
ID aliases its staged adapter; new unique records require explicit indexing. The
standalone package smoke checks this join. No new model evaluation, renderer trial
or general reliability/rights-clearance qualification is established by this helper.

## Ranked choices by production task

Use the existing catalogue to select a primary route, a fallback and the next
worthwhile test for a particular job. Start with editorial graphics, local
English narration, editable montage and manual portrait adaptation.

```sh
python3 skills/video-production-router/scripts/search.py --list-rankings --format markdown
python3 skills/video-production-router/scripts/search.py --rank-profile all --format markdown
python3 skills/video-production-router/scripts/search.py --rank-profile editorial-graphics --rights commercial --format markdown
python3 skills/video-production-router/scripts/search.py --rank-profile editorial-graphics --unavailable givemotion --confirmed minicharts --format markdown
python3 skills/video-production-router/scripts/search.py --rank-profile local-english-narration --include-fallbacks --format markdown
```

Production ratings in the existing `arsenal-facets.json` link to a tested
application. Use 1 for poor fit, 2 for limited, 3 for workable, 4 for strong,
and 5 for a particularly good fit with direct evidence. Rate output quality,
control over edits, repeatability (save/reopen/export), end-to-end speed and
incremental budget fit. The quality score is a studio assessment; the owner's
evaluation stays in the application. For cost, 5 can mean the retained local
route needed no new paid service; local compute and labour stay unpriced.
Record render time separately from active work, waiting and time to a usable
result. An unknown score stays blank. Each profile weights its own priorities.
The weighted score uses only axes rated for all options in that pool. Ties
keep the recorded order. Scores from different profiles or from the reserve
and production pools are not comparable.

Referenced but untested routes use a separate test ranking. Rate relevance to
the gap, readiness of the access/setup and value of the proposed comparison.
Each entry names the smallest useful probe. Its priority is not a quality
rating. Routes requiring confirmed access remain listed with the reason they
are blocked. Use `--confirmed TOOL` once access, equipment and setup are
available for this run. Add `--allow-paid` for an authorised comparison of a
paid route. Use `--unavailable TOOL` for a temporary project constraint and
`--include-fallbacks` to consider explicitly reserved tools. Rights filtering
uses the retained classifications. The output does not confirm current
licences, subscriptions or workflow compatibility outside the named profile.

After each trial, production or owner correction, update the matching
application and then review affected rankings. Retain the earlier evidence.
Promote a queued route only after scoped execution and assessment, review a
changed version or access condition before relying on the previous result, and
exclude routes rejected by the owner. Add profiles as production needs them.
The rankings propose choices; they do not select a planner provider or run a
test.


## Maintain the discovery index

Adding or removing a review-ledger/profile ID also requires an explicit entry in
`arsenal-facets.json` (after aliases). Index the task and retained licence-note hash;
never infer asset clearance or an executable provider from a manual record.
Run `python3 -m unittest discover -s tests -p test_search.py -q` and refresh retained
CLI examples when diagnostics change. A stale index fails discovery closed rather
than silently omitting tools. The full offline gate also checks the installed ZIP.

An unindexed input kind (`null`) cannot satisfy an explicit `--input` filter.
A review-only candidate may still be found without an input filter using
`--evidence any`; that result is not a compatibility or production claim.

## Retained applications, style and quality

The same `arsenal-facets.json` now links task → style → technique → tool/version →
retained case. `review-ledger.json` remains the review history; `tools.json` remains
structured planner capability coverage. An application is a discovery annotation,
not another production journal or executable provider. Original experiments and
owner decisions remain authoritative.

```sh
python3 skills/video-production-router/scripts/search.py --query 'газетный коллаж с цветными вставками' --evidence tested --format markdown
python3 skills/video-production-router/scripts/search.py --task video --style paper-collage --technique colour-footage-insert --evidence tested --format markdown
python3 skills/video-production-router/scripts/search.py --tool manim-community --style ascii --evidence tested --format markdown
python3 skills/video-production-router/scripts/search.py --tool inshot-android --details --format markdown
```

Literal name lookup remains supported. Application queries match all significant
words,case-insensitively,against retained annotations,including curated English and
Russian terms. This is token matching,not semantic search,translation or stemming.
Task/style/input/technique/text filters must match the **same application**;a video
fixture cannot borrow a photo-collage style from another fixture. Historical profile
style directions remain affordances,not proof that every style was tested.

JSON retains all matching application records. Ordinary Markdown shows up to two
applications per tool and concise historical summaries; `--details` expands them.
`--list-filters` includes indexed techniques and application styles. New manual
records do not become planner providers or fulfill narration/arbitrary features.

### What the observations mean

| Field | Meaning |
| --- | --- |
| Scope,version,sources,example | Exact retained application and its limits. Owner-provided publication URL is an example,not a fresh visibility/metrics check. |
| Technical | Recorded execution,passed,failed or partial for the named scope;not overall visual quality. |
| Readability | Text/line contrast,size,overlap and reduced-view inspection. |
| Motion | Meaningful subject/action movement and timing;not just successful encoding. |
| Drawing stability | Shape/silhouette/identity observations;deterministic vectors do not qualify generative acting. |
| Artifacts | Defects and corrections observed in the case;not a guarantee of artifact-free future output. |
| Controllability | What could actually be adjusted and rerendered within this route. |
| Owner evaluation | Explicit accepted/rejected/mixed/not-recorded scope,kept separate from technical checks and publication. |
| Resources | Observed host/formats/time/cost,or explicit unknowns. Render time is not active labour or a controlled speed comparison. |
| Alternatives | Related candidates with a reason;currently marked not-compared,not a quality ranking. |

Initial17November backfill:47 application/scope cards across44 tools,including three new
scoped tools:GenMotion0.8.1,GiveMotion0.1.6 and Manim Community0.22.1. Legacy records
cover one explicitly tool-level retained ledger summary per tool;they are not
cloned under individual experiment IDs or used as technique-specific evidence. Their
`retained_scope_summary` granularity,missing style/version/time/cost and
`not_assessed` quality dimensions are intentional gaps,not completed new reviews.
Detailed recent cards retain operator observations and separate owner decisions.
GiveMotion publication does **not** fill its missing explicit creative acceptance.

At each executed trial/production correction closeout:update the matching tool's
application from the actual source record;preserve the source link,scope/version,
technical result,per-axis observations,owner decision,resources and restrictions.
Do not copy the full journal into the index,derive quality from views,guess a score,
or generalise a rejected/accepted take to every feature/voice/style of that tool.
Use comparable controlled trials before adding numeric rankings. `validate.py`
checks application structure,unique IDs,local sources and alternative tool IDs;
these checks assess documentation integrity,not media quality.

The Peter comparison also indexes a technically decoded but owner-rejected I2V
performance and a failed native-GIF request. They remain partial diagnostics under
`--evidence any`,not default usable tools or an approval to resume paused Quixote.

Source references are checkout-relative. Installed discovery validates their structure
but does not require a full repository checkout; `scripts/validate.py` additionally
checks source existence inside the repository. Manim Community/GiveMotion accept
only authored composition input in these retained trials;image/video import is
not inferred from their exported PNG/MP4 files.

## Latest documentary intake —18November2026

[26-family assessment and sources](../../../docs/research/tool-intake-2026-11-18.md) deduplicates existing routes and maps new rendering,effects,avatar and design-reference candidates to the existing queue. Keywords:ThreeRT,Canvas UI,AVA,Duo,LoreMax,Kling Image4,21st,Originkit,Transitions,DESIGN.md,Mobbin,Recent/Godly,Designeer. These are documentary discoveries,not executable providers or tested applications returned by search.py. Read exact access/licence/hardware/quality boundaries in the intake;refer to existing application records for Manim/MotionCanvas/HyperFrames/GiveMotion and GenMotion. Do not reset historical tests or infer qualification from a link.

Course preparation discovery: [15-family Udemy tool assessment](../../../docs/research/udemy-course-tools-2026-11-18.md) links retained Claudemy/Kdenlive/Whisper scope to conditional NotebookLM,Coursebox,Mindsmith,SubtitleEdit and Descript comparisons,with other supplied tools kept as references. This is documentary intake,not new tested providers or automatic planner qualification.
