# Interim product audit — 2026-10-18

Current release ordering and status: [2026-10-19 release audit](release-audit-2026-10-19.md). Earlier sequencing and waits below are historical snapshots.

Owner authorised audit, sanitation and feature preparation while SSI work prevents
recording the Toki Pona excerpt. This is an interim review, not the final
post-PlayMCP closeout. No render, model call, spending, publication, commit or
release is part of this pass. At the audit checkpoint the two features below were proposals. The owner later
selected project state and the evidence/decision lifecycle; see the implementation
record below. The capture-manifest proposal was initially unimplemented; the later selected
scene/reuse/kit increment below implements its planning subset.

## Baseline and verdict

Baseline HEAD: `13b94537a46da21be489ca3f6e48b3a698531913`, plus the existing
modified/untracked PlayMCP, studio and evidence work. All were included in the
inspection; they were not reset or treated as newly authored by this audit.
Baseline entry sizes: AGENTS 10 lines, README 155, router SKILL 119, game SKILL 108,
queue 192. The agent startup contract is already small; growing case narratives
and duplicated statuses are the main documentation problem.

The product is useful as an agent-operated methods library with offline planning,
arsenal discovery, saved checkpoints and retained production recipes. It is not
an autonomous renderer or general game engine. Current inventory contains 17
planner profiles, 42 discovery IDs and 10 methods; these are different units, not
counts of fully qualified tools. The integrity catalogue holds 22 video exports.
SSI remains a supplied field report outside that export total; Jekyll is a local
alpha, not another rendered film. No new model evaluation was performed.

## Findings and sanitation

| Finding | Action and remaining limit |
| --- | --- |
| Arsenal search failed after Tesseract was added only to the review ledger | Added explicit discovery facets and licence-note pin, preserved manual/converter-only status, added a CLI regression. Initial baseline: 213 tests, 12 failures + 3 errors. Do not weaken the fail-closed registry/index contract. |
| Tests still expected no tested transcription component | Updated expectations to the retained mlx-whisper clean-English timing trial; candidates remain excluded and Ukrainian coverage remains unqualified. Refreshed the generated search example. |
| Workflow still called the delivered SIRTET films proposals | Reconciled delivered overview/Short states with their retained records; no new creative acceptance inferred. |
| TP probes still described as awaiting owner review | Recorded both as owner-rejected, retained negative evidence, deferred owner recording during SSI work. English narration and game/music acceptance stay independent. Refreshed the private voice-manifest hash; no media changed. |
| Queue/readme implied narrower subjects or obsolete production pauses | Generalised subject choice, marked agricultural pause as historical and linked current evidence; replaced repeated game-film history in README with workflow/case links. No historical reports deleted. |
| Current planning-source pins became stale after the index fix | Refreshed only current-source pins; historical frozen evaluation and `not_evaluated_current_source` remain intact. Passing deterministic checks does not promote model qualification. |

SSI is valuable cross-task evidence: another agent used Framewright's method
selection for a real OAuth demonstration. The supplied report also retains failed
captures, manual owner intervention and caption-filter workarounds. It does not
measure setup time saved or prove universal independent adoption. Playback and
temporary unlisted access are owner-confirmed; Google's decision is unknown.

Repository file inventory found no versionable MP4/MP3/WAV/WebM/MOV/AVIF/JPG/JPEG
or ONNX artifacts. A bounded text scan found no matches for GitHub-token,
Google-API-key or private-key signatures. This is not a full secrets/security audit.
Private-path breadcrumbs exist in retained evidence; do not equate paths with
credentials or delete provenance indiscriminately.

## What worked; what remains weak

- Planning, component evidence and execution are separate; this allowed a second
  agent to choose OpenScreen/FFmpeg without Framewright becoming the renderer.
- Owner playtests caught problems beyond technical checks: control cancellation,
  unclear objectives, held-object anatomy and unacceptable TP speech. Negative
  results must stay searchable and distinct from successful English synthesis.
- Reusable captures, separate soundtracks and deliberate landscape/portrait edits
  support several outputs from one game; there is no measured virality claim.
- Evidence is fragmented across output JSON, case prose, queue, discovery facets
  and private project files. Status repair is manual; CLI checks missed some prose
  contradictions. This is the largest leverage point for product work.
- The shipped ZIP packages only the router skill. The game-engine skill and repo
  workflow documents are not a standalone packaged game-production capability.
  Installation/package scope needs an explicit decision before the next release.

## Proposal 1 — evidence and decision lifecycle (first priority)

Extend existing production checkpoints with one typed, local evidence record per
artifact revision. Avoid another scheduler or database. Keep technical QA, owner
listening, creative acceptance, publication visibility and provider decision as
independent observations, each with actor, time, provenance and artifact identity.
Owner rejection must be representable without pretending that bytes disappeared.

Support temporary URLs and a planned removal note. A broken/deleted upload must
not erase a completed local export or turn an old URL into current public proof.
Generate a concise status view from the record and flag conflicts with migrated
queue/case summaries; do not automatically rewrite historical supplied reports.
Existing `project.py` hashes, history and dependency invalidation remain the base.

Acceptance for a future implementation:
1. Record failed TP listening alongside passing English QA without status leakage.
2. Record owner-supplied versus independently checked URLs, then removal, without
   inventing an upload, provider approval or a permanent live showcase.
3. Replacing an artifact reopens its dependent checks but retains earlier receipts.
4. A read-only summary exposes outstanding gates and stale revision evidence.
5. Old checkpoints remain readable via a tested version/migration policy; no network
   requests, publication or media inspection occur merely by recording a status.

## Proposal 2 — review and capture manifest (second priority)

Extend the existing source/claim/edit workflow and readable production packet with
review-specific shot records. Each factual statement names a real demonstration,
source/build, required permission, capture interval, framing, narration and intended
landscape/portrait use. A review is a reusable content contract, not a PlayMCP-only
recipe. OAuth demonstration, game review and virtual-set book promo are examples.

Acceptance for a future implementation:
1. Unsupported statements produce a visible missing-demonstration item.
2. Distinguish real gameplay, scripted legal inputs, authored footage and terminal
   fixtures; record seed/build differences without changing a live game for a shot.
3. Mark safe capture regions and sensitive/owner-controlled steps; the manifest
   plans these checks but never certifies that a recording is secret-free.
4. Derive separate long-form/Short shot lists and reveal where portrait framing
   loses the promised action; no automatic smart-crop claim.
5. Link actual takes and final intervals after capture; planned footage cannot
   silently become evidence that a function worked.

## Sequence and deferred scope

Discuss these proposals before implementing product APIs. Prefer lifecycle first,
then capture manifest; migrate one existing case before expanding. Keep strict
budget/download enforcement deferred as previously decided, rather than silently
adding it to this release. Do not add more engines, hosted infrastructure, model
benchmarks or a universal renderer merely to expand the catalogue.

Jekyll production still waits for owner recording/review and its existing hosting
and service gates. The overall service review, full programme closeout, release
scope, PR integration and release remain separate later work. This audit neither
spends the remaining PlayMCP budget nor authorises a public test link.

## Verification

Final `python3 scripts/check.py --scope docs`: PASS — 214 unit tests, archived
router/storyboard evidence integrity, 10 methods / 22 outputs / 17 scenario
specifications, local links, generated tool matrix and temporary standalone ZIP
smoke. The ZIP was only a temporary installation check of existing version 0.2.0,
not a new release. Model qualification remains `not_evaluated_current_source`.
Private Jekyll evidence: all 19 artifact pins match after the TP-status correction.
README shortened 155 → 143 lines; AGENTS remains 10 lines. Detailed case history
stays behind workflow links; historical source reports remain unchanged.

Completion: interim audit, scoped sanitation and proposal preparation complete.
Product features, remaining production and release are not declared complete.

## Subsequent selected implementation

The owner selected unified project state and the evidence/decision lifecycle.
[Schema-2 project memory](../skills/video-production-router/references/projects.md)
implements that increment on existing checkpoints, with an explicit schema-1
migration and a manual-project mode for existing game production. The paused
[Jekyll case](experiments/jekyll-toki-pona.md) is the real checkpoint trial.
The owner then selected scene/capture/edit coordination, reuse and local kits;
see the subsequent implementation below. No new release is authorised.


## Subsequent scene/reuse/kit implementation

[Production composition](../experiments/2026-10-18/production-composition.md) implements
the owner-selected next increment in the same saved project: scenes and independent
cuts, a version/rights/provenance-aware catalogue, and checked local final-file kits.
The paused Jekyll checkpoint is used for planning/draft-report verification only.
The original broader capture proposal's automatic/visual evaluation and privacy
redaction are not claimed. Selected feature development stops here; actual media
production and the full post-PlayMCP closeout remain separate work.
