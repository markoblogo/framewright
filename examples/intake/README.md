# Local producer intake — experimental first slice

The files are fictional options, not vendor recommendations or a ready-to-run
production. Create the profile outside Git; no accounts, credentials or media are
read, uploaded or shared.

```sh
python3 skills/video-production-router/scripts/intake.py init /tmp/framewright-profile.json
python3 skills/video-production-router/scripts/intake.py inspect --disk-root .
python3 skills/video-production-router/scripts/intake.py subscription /tmp/framewright-profile.json example-service --status unknown
python3 skills/video-production-router/scripts/intake.py propose /tmp/framewright-profile.json examples/intake/book-brief.json examples/intake/routes.json
python3 skills/video-production-router/scripts/intake.py propose /tmp/framewright-profile.json examples/intake/book-brief.json examples/intake/provider-routes.json --catalog skills/video-production-router/references/provider-terms-pilot.json
python3 skills/video-production-router/scripts/intake.py recommend /tmp/framewright-profile.json examples/intake/book-brief.json --task video
python3 skills/video-production-router/scripts/intake.py routes /tmp/framewright-profile.json examples/intake/comparison-brief.json --format markdown
python3 skills/video-production-router/scripts/intake.py preference /tmp/framewright-profile.json --options free-only
```

`propose` filters explicit supplied options and asks for missing fields. With the
optional pilot catalogue, a route's explicit `provider_id` attaches its dated
research snapshot; it does not automatically choose tools or build a production route.
All snapshots require rechecking. It does not verify a cost, schedule quotas, probe a network, connect a
provider, execute a production or establish rights. A null amount is unknown; a
free-quota label needs current terms and entitlement. Subscription status is a
user declaration, not an account check; never put credentials in the profile. The
optional local profile is private; `sharing: off` is a placeholder and no sharing exists yet.
`recommend` searches existing indexed task tags and attaches evidence and the small cost
facet/terms slice. Select an indexed task explicitly; free text is not interpreted.
Candidates are individual components, not complete production routes. Evidence is
scoped, current availability and rights are not established, and free-only excludes
unknown-cost tools (the count is shown). Many legitimate free tools remain unclassified.
The narration shortlist honours the brief language at its retained evidence level.

`routes` compares bounded recipes for picture, optional voice and finishing. It reuses
the shortlist and cost facets: a prepared saved Blender shot, local authored motion,
supplied-media montage, quota generation and conditional-licence authoring. The last is omitted in free-only mode.
See the [retained comparison](route-comparison.md). These are comparable stage plans,
not promises of identical visuals or completed creative production.

Use `visual_source: supplied|generate|unknown`, boolean `narration` (default true),
and optionally `preferred_voice` (canonical tool ID). Missing or incompatible voices
stay unresolved; no replacement is inferred. `cost.provider_fee: 0` covers only
classified local software fees when every stage has a candidate. Total project cost,
time, installed access, hardware fit, current plan terms and integration remain
unknown. A documented language is not promoted to tested. Known licence/model notes
are included in JSON; asset clearance and required synthetic-content disclosure remain.
This slice neither prices paid offers nor promises how many days quota work will take.
See [roadmap](../../docs/producer-agency-roadmap.md).


A selected proposal can now bind **one supported local action** through
[route admission](../../skills/video-production-router/references/route-admission.md).
The original comparison stays planning-only; selection does not execute other stages,
qualify a chain, verify a provider quote or grant publication.

## One readable producer proposal (R02)

```sh
python3 skills/video-production-router/scripts/intake.py brief /tmp/framewright-profile.json examples/intake/comparison-brief.json --format markdown
# Optional: --source-index /private/path/index.json --project /private/path/project.json
```

Retained outputs for the same brief: [free-only](producer-brief-free-only.md) and
[both options](producer-brief-both.md). The output explains task, scene purposes,
materials, route tradeoffs, constraints and next action. Generic scene purposes are
proposed, not approved; the example has no supplied source index. Optional explicit
scene queries reuse revision-checked lexical search. Project waits and file problems
remain visible. Human work, small-pilot and fallback suggestions are not execution
authority. See the [input contract](../../skills/video-production-router/references/producer-brief.md)
and [internal evidence](../../docs/experiments/r02-producer-brief.md).
