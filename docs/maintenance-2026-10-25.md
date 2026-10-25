# Closeout audit — 25 October 2026

Scope: accumulated local work since `9a5d458`, documentation/status drift, the new
brand-profile helper and tests, retained production receipts, publication hygiene
and the normal offline check entry point. This is not a comprehensive security
assessment, new media production, model evaluation or release.

## Changes and checks

| Area | Finding and action |
| --- | --- |
| Production inventory | Added four omitted exports: the Nantes illustrated route film and three SSI voice-only report films. The registry now contains 37 final exports, with size/hash pins and explicit QA limits. Revisions are not counted again. |
| Current status | Replaced stale SSI pause statements in current entry points. All three revised films are delivered; partner feedback and publication links are pending. The earlier six rejected demos remain historical evidence. |
| Documentation | Updated README, production guide, next-cycle plan, experiment index and tool research. Detailed cases hold evidence; the short startup policy stays unchanged. Read README, then only the relevant case or current plan. |
| Brand helper | `settled_hold_seconds` was documented and used in the private SSI spec but rejected by validation. A public-CLI regression reproduced the rejection. The fix accepts optional finite holds from zero to ten seconds and exports the CSS token; invalid values remain rejected. |
| Source retention | All three delivered CSS/logo/font/licence bundles match their retained hashes. Two original presentation references are missing from their saved locations. A new export from that private profile remains blocked; no source was silently repinned. |
| Research | Spline is queued for a bounded editable-scene/export trial. It remains documentation-reviewed, not connected or qualified. No installation or generation ran. |
| Public hygiene | Changed files contain no private absolute source paths or detected credential patterns. No raw reports, decks, screenshots, media, caches or model weights are included. These scoped checks are not a guarantee that arbitrary source prose is safe to publish. |
| Qualification | Current source inventory is refreshed without promoting `not_evaluated_current_source` or altering the historical model-evaluation packet. Offline tests do not qualify model behaviour. |

## Verification

Six focused brand CLI tests pass. The reading-hold test failed before the fix with
`Invalid motion fields`, then passed with the same invocation after the fix.
The normal full offline entry point is `python3 scripts/check.py`: unit tests,
router/storyboard packet integrity, records/local links, generated tool-reference
consistency and temporary standalone package smoke. It makes no model calls and
creates no tag, release or public upload. The completed run passed: **337 tests, one skipped**, followed by all packet,
record/link, generated-reference and standalone-package checks.
[Sanitized verification receipt](../experiments/2026-10-25/evidence/maintenance.json).

The first captured full-check attempt exceeded its recorder's 120-second limit;
it is not a passing run or an assertion failure. A later attempt uses a sufficient
limit and retains the result separately. Raw logs stay in the private production
workspace; only a sanitized result summary is committed.

## Remaining boundaries

- SSI revised-master creative/listening acceptance, partner comments and publication
  remain pending. The owner retained the requested slower pacing despite preferring
  a faster edit. SSI recurring automation is not deployed by this work.
- Nantes publication is owner-reported. Upload visibility/bytes, final French
  listening and audience results remain unverified. Its mapped pseudo-3D scene is
  not photographic street footage or current navigation advice.
- Restore matching deck references or deliberately freeze a new profile before a
  future export. Existing delivered bundles and masters are retained independently.
- Pocket OS remains paused. MN7R, the Nantes green-line walk and Good Dog remain
  proposed productions in the [current plan](next-cycle.md).

No cleanup removed user sources, production media or retained failed takes. New
paid work, account connections and publications require their own task authority.
The software version and release tag remain unchanged.
