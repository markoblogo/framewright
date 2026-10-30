# Unified producer proposal — R02

`intake.py brief` joins existing intake preferences, bounded route comparison,
source-search evidence and optional project-journal state. It is a read-only planning
view, not a new scheduler or a replacement for the production journal.

```sh
python3 skills/video-production-router/scripts/intake.py brief PROFILE.json BRIEF.json --format markdown
python3 skills/video-production-router/scripts/intake.py brief PROFILE.json BRIEF.json --source-index INDEX.json --project PROJECT.json --format json
```

The output includes the task, materials and gaps, scene purposes, at most three
proposed routes, constraints and one proposed next step. JSON preserves the underlying
component capabilities, evidence references, terms and unresolved conditions.
Markdown is the human review version. Output goes to stdout; keep private proposals
outside Git. Neither source files nor the profile/project are updated.

## Input and evidence boundaries

Use the existing intake brief (`idea`, duration, format, language, source rights,
deadline, budget instruction, visual source, narration and preferred voice). Optional:

```json
{
  "preferred_route": "local-montage",
  "constraints": {"allow_uploads": false, "allow_installation": false},
  "scenes": [
    {"id": "opening", "purpose": "Show why the book matters", "query": "cover"},
    {"id": "example", "purpose": "Show a concrete page example", "query": "page"}
  ]
}
```

These fields supplement, rather than replace, the required `idea`. A route preference
must name an existing recipe; an excluded preference is not silently substituted.
Scene IDs are unique, purposes mandatory, queries optional. With no scene list, three
rough narrative purposes are **proposals requiring confirmation**, not an approved
script, a generated storyboard or timed shots. Unknown constraint keys are rejected.
Other ordinary intake fields are not interpreted as executable instructions.

`--source-index` accepts the existing `source_search.py index` output. All retained
media/spec/annotation hashes are rechecked. The command searches only explicit scene
queries, keeps original evidence IDs, source ranges and annotation provenance, and
shows up to three matches per scene with the full match count. An empty result means
**not found in this lexical index**, not “the footage does not exist.” Indexing and
matched words do not establish visual quality, speech correctness or rights.
Without an index, materials are declared, not inspected. Supply or create missing
material explicitly; no generation is launched automatically.

`--project` reuses the existing project load/status/working-brief functions. Current
file problems, stale checks, unresolved operations, waits and blocking decisions can
override the proposed next step. Retained approvals stay version-bound. Recorded
ready tasks remain visible but do not authorize the newly proposed route. Free-text
journal decisions are displayed for review, not automatically parsed into creative
constraints; reconcile them with the brief before selecting a route.

## Route selection and costs

- Supplied media: propose local montage and local authored motion; broader policy
  may add conditional-licence authoring. No artificial third option in free-only mode.
- Generation: propose the indexed quota route, with its current capability gaps.
  Unknown visual-source intent: ask for clarification before proposing a route.
- A saved Blender shot appears when explicitly requested via `preferred_route`;
  the generic catalogue evidence does not imply that a particular shot is prepared.
- Declared-unavailable tools are excluded. No-upload excludes routes lacking a
  confirmed local-only profile. No-installation requires verification of existing
  runtimes; it never treats them as installed or installs them.
- Free-only excludes paid/unknown-cost recipes, while free-quota remains conditional.
  Subscription declarations are not verified entitlements. Zero local software fees
  are not zero production cost. Time, total cost, current balances, hardware fit and
  rights remain unknown unless a separate check establishes them.

Every route retains its method, human work, tradeoff, scoped evidence, prerequisites,
small-pilot suggestion and fallback proposal. Routes with gaps are visibly conditional;
this is not feasibility certification, a price quote or permission to spend. The
fallback also needs a decision. There are no model, provider or network calls.

After owner selection, retain the existing `intake.py routes` comparison and bind one
supported action through [admission](route-admission.md). The producer proposal itself
is not an admission receipt. R03 will test this planning view in a complete real
production, including owner choice and fresh-session continuation.

[Retained examples](../../../examples/intake/README.md) · [Internal results](../../../docs/experiments/r02-producer-brief.md).
