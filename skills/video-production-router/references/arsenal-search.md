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
promoted to usable providers. Low-quality Piper is excluded by default; use explicit
`--tool piper` or `--include-fallbacks` to inspect it. It remains an explicit fallback.

## Compare proposed picture chains

```sh
python3 skills/video-production-router/scripts/search.py --task video --input book-art --style paper-cut --feature paper-cut-regroup --feature narration --feature still-export --language uk --rights commercial --evidence tested --combinations --format markdown
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
