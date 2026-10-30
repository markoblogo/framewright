# Framewright as an agent-led production agency

Design detail beneath the [global roadmap](roadmap.md), which owns current priorities,
milestone exits and intake/change rules. Keep this document for the profile, catalogue,
quota and contribution design; historical first-slice descriptions below are not
a second execution backlog.

Owner direction, 27 October 2026. This is a staged product plan, not a claim that the
full service or external integrations already exist. It does not start a production,
generation, spending, network probe, account connection, publishing or community sync.

## Experience

A client describes a result, such as a book promo. Framewright combines an explicit
local environment/profile with the existing project journal and tool catalogue; asks
only the missing decisions that affect feasibility; offers free-local, free-quota and
paid approaches when the client permits; and explains concrete tools, tradeoffs,
confidence, estimated money and elapsed time. The client selects a plan. Execution,
local QA, human review, handoff and eventual publication remain separate actions.

A first-time profile defaults to showing free and paid possibilities without buying
anything. An explicit free-only preference persists and hides paid and unknown-price
routes; free-quota candidates still require verified entitlement and current terms.
Existing owner preference remains free/open-source/macOS first, with paid only for a
specific approved production or an existing entitlement. Profiles are personal, not
one global policy for all users. Paid visibility never authorizes a paid call.

## Existing foundation and staged work

1. **Catalogue normalization.** Extend current `tools.json`, `review-ledger.json`,
   `arsenal-facets.json` and documented research as a single indexed discovery view.
   Preserve feature-specific tested/documented/failed/unknown evidence and actual
   platform/version scope. For historical and new finds add sourced, dated fields:
   OS/architecture, local/cloud, installation and resource constraints, cost mode,
   free-quota reset/terms, eligible use/rights and provider/account requirements.
   Missing/unindexed is `unknown`, never free or compatible. Keep research candidate
   distinct from qualified capability; no blanket promotion. Import in small reviewed
   batches, including existing tested tools and queued candidates, with regression tests.
2. **Environment and preferences.** Reuse `environment.py` for per-tool readiness;
   add a private, opt-in machine/profile layer for OS, architecture, total RAM,
   relevant volume free space and user-declared entitlements. Store only nonsecret
   status, not credentials or tokens. Network-speed test is separate and opt-in;
   no implicit account lookup or scan. Preference updates survive sessions and are
   reversible. First slice: `intake.py` creates a local profile, remembers option
   visibility and performs a bounded host snapshot; subscriptions remain manual
   profile data and do not prove access.
3. **Client intake and proposals.** Capture idea, duration, format, audience,
   language, source/rights, delivery, deadline and budget as needed; ask only
   missing facts affecting this task. Build routes from the indexed catalogue and
   profile, not canned statements: explain exclusions and source evidence; split
   tested components from untested combinations; include real inputs, outputs,
   required approvals, version/terms freshness and fallback. Offer paid only if
   preferred; new quotes and capability claims need dated evidence. Estimate ranges
   from actual benchmark data and include setup, human review and likely retries;
   otherwise say unknown. First slice can filter explicit supplied route candidates;
   it does not query the catalogue, calculate estimates or claim a completed offer.
4. **Free-quota schedule.** Add dated provider rules (quota type, reset timezone,
   limits, output/watermark/usage rights and price); separate them from the private
   user's actual remaining credits, observed time, uncertainty and entitlement.
   Plan accepted shots, retries, cadence and cross-provider continuity as a range;
   never infer exact replenishment or that first attempts succeed. No scheduler,
   background generation, remote account query or upload until separately authorized.
5. **Execution and feedback.** Integrate one selected proposal with existing
   checkpoint, asset/rights and review journal. Run one explicitly allowed step at
   a time, record receipts and provenance, and stop for approval or missing input.
   Quota/provider readiness is not permission to upload, spend, publish or retry.
   Reuse the existing bounded executor and review/comparison helpers; no competing
   production database. Measure local resource pressure and stop on failure.
6. **Opt-in community experience exchange.** Default sharing off. Provide a local,
   inspectable, versioned experience packet: method, tool/version, OS/hardware class,
   synthetic or approved input description, actual outcome, constraints, reproducible
   steps, time/cost basis, rights and source, plus explicit unknowns. Exclude account
   identities, keys, private prompts, media, client data and absolute paths by default;
   automated redaction is not proof of safety. User reviews the exact packet and
   explicitly approves each transmission. Prefer a fork/PR for human review, not
   automatic writes to the owner's repository. Credit contributors as they request.
   Label community-reported vs locally verified evidence; validate schema, duplicates,
   provenance, version and malicious/untrusted content before merging. Never run
   contributed code or accept capability claims blindly. Public upstream updates
   remain available to non-contributors; sharing is not required to receive them.
   There is no current sync, sharing setting execution, automatic PR or telemetry.

## Acceptance examples

- Same book brief, two users: one chooses free-only and sees no paid routes; another
  sees both. Unknown quota or pricing never becomes zero or an exact schedule.
- A licensed service on Windows is not claimed usable on Mac from a missing OS field.
- A failed/unverified combination is disclosed even when its individual components
  were tested; human and technical acceptance remain separate.
- A later quota reset and ten-second clips yield a tentative schedule that accounts
  for retries, timestamp and time zone; absent entitlement stays unknown.
- A shared packet is inspectable and sanitized, owner consent is explicit and a
  community result never silently becomes a local production qualification.

## Current implementation and next slice

28 October: [PR #46](https://github.com/markoblogo/framewright/pull/46) is merged.
[Local admission](experiments/route-admission.md) links one selected intake stage to
inspection/proxy execution with pinned inputs, requirements, limits and expected
output. [Studio foundations](experiments/studio-foundations.md) add bounded resource
observations, cost evidence, recovery and offline assertions. [Completion diagnosis](experiments/completion-diagnosis.md)
reads existing tasks/decisions. [Capability review](product-progress-2026-10-27-28.md)
retains the exact limits. Paid dispatch, quota scheduling and community sync remain
unimplemented.

The [global roadmap](roadmap.md) records completed internal R01 saved-shot admission
and [R02 unified producer brief](experiments/r02-producer-brief.md). R03 is the next
real proposal/production check. The bounded cost/platform catalogue and route-comparison
slices described below already exist; broadening them is need-driven, not a new
blanket classification task. A whole-route production test remains separately selected.

## Initial representative classification — not yet a complete price/OS index

These are historical, scoped evidence examples for migration planning. Their current
pricing, subscriptions, quotas, rights and actual host capability must be checked;
no row is a verified live offer or an automatic plan.

| Tool | Existing evidence | Initial economic class | Pending checks |
| --- | --- | --- | --- |
| FFmpeg | [Scoped assembly/QA](tool-research.md) | Free local executable; assets and labour separate | Build, codecs, disk, CPU, source rights |
| Blender | [Saved-shot local CPU probe](experiments/blender-shot-replay.md) | Free local application; assets and labour separate | Per-scene render load, licences, continuity |
| Supertonic 3 | [Scoped local narration](experiments/framewright-micro-lesson.md) | Local method; model/voice terms distinct | Exact voice, language, version and runtime |
| Openverse | [Research and retained results](tool-research.md) | Search is not asset or provider entitlement | Actual licence/source, attribution, file rights and current limits |
| PlayMCP | [Production case](experiments/playmcp-service-review.md) | Cloud credit-based; historical credits not a current price or balance | Current entitlement, pricing, costs, rights and export |
| Marble | [Scoped world/plate production](experiments/marble-compositing.md) | Cloud; plan-dependent | Current account, generation plan, terms and reuse rights |
| Audacity / iMovie / OBS | [Mac app intake](research/mac-native-free-production-2026-10-27.md) | Free desktop candidates | Installation, specific feature, agent control and real runtime untested |

A full catalogue migration is a separate tested implementation slice; neither this
table nor the intake prototype changes canonical evidence or auto-categorizes tools.
An optional pilot terms catalogue annotates explicit PixVerse, Runway and Meshy routes
with dated sources and conditions. It is separate from the existing discovery index;
account access, costs, licence, selection and ability to execute remain unverified.
The `recommend` prototype now links those records to existing arsenal task tags and
scoped evidence, plus five explicit cost facets. It requires a task selection, returns
individual candidates rather than end-to-end plans, and omits unclassified costs in
free-only mode. This does not classify the full arsenal, estimate time, or check installs.

28 October: local cost facets now include Kokoro, MLX-Audio, Supertonic3, Piper and
Hyperframes based on retained software/model notes. Remotion remains cost-unknown
until Free/Company eligibility is confirmed. This records the local-operation slice;
it does not clear models, voices, assets or optional paid services. Language-aware
discovery keeps documented language support separate from tested support.
`intake.py routes` compares five bounded recipes (saved Blender shot, local authored, supplied-media
montage, quota generation and conditional authoring) across picture, optional voice
and finishing. It retains capability gaps, explicit voice choice, dated quota terms,
unknown costs/time and human integration checks. Free-only hides the conditional
cost-unknown route. No paid quote, machine-fit conclusion or production execution
is inferred; music, captions and delivery packages are outside this comparison slice.
