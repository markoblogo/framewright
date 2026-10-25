# Hand an accepted production to its owning project

Framewright retains the creative method and evidence. A producer such as SSI owns
its source data, runtime, schedule and delivery. Transfer reusable material once;
do not route every future report through another Framewright chat or scheduler.

## Transfer contract

1. **Accepted baseline:** exact master hashes and acceptance provenance, owned or
   cleared renderer source, selected brand assets/font licence, timing/voice examples.
2. **Inputs:** immutable source/report revision and claim references; typed text,
   numbers, units, bases, periods, chart data and voice text. Languages are explicit.
   Dates and missing facts never silently fall back to the baseline week.
3. **Assembly rules:** escape supplied text, compute new chart geometry, generate
   changed narration, measure it, retime all scene/audio boundaries and preserve
   the accepted reading hold. Keep authoring assets separate from account secrets.
4. **Checks:** render short/long/missing-optional controls and a historical replay;
   compare facts, layout, pronunciation, timing and encoded outputs separately.
   A template or file-hash pass is not a successful receiving runtime.
5. **Operations:** receiving project supplies a durable worker/store, job identity,
   existing schedule, readiness gates, delivery receipts, retries and runbook.
   Keep production holds until receiving activation is evidenced. Do not infer
   deployed automation from a transferred package, commit or accepted old video.

## SSI receiving example

[Proposed input contract](../examples/ssi-weekly-video/input.schema.json).
Reports are Ukrainian; video copy and speech are English. All three files must be
ready from the same validated report before the existing SSI delivery slot.
Send six ordered items: text I → video I → text II → video II → text III → video III.
Keep full report text separate from the short video caption. No baked music/SFX.

A scene cannot cut until at least two seconds after both narration completion and
final data settling. At 30 fps, a minimum-duration rule is:
`ceil_to_frame(max(7.6, voice_start + measured_speech + 2, data_settled_at + 2))`.
The historical 7.6-second scene is a floor for this SSI style, not every production.
Final lengths change with each narration; old master lengths are not fixed budgets.

Prepare/render before send time. Use the receiving project's current timezone,
DST guards, quality hold, tenant/channel auth and catch-up policy. A heavy browser/
voice render needs an actually available worker, not an assumed serverless request
or a sleeping developer computer. Do not create another scheduler in Framewright.

Telegram delivery is not atomic. Persist a lock and per-item in-flight/confirmed
receipts; report complete only after all six confirmed message IDs. Retry only
known-unsent items. An ambiguous timeout requires reconciliation, not a blind resend.
Never mix report revisions, send old videos or silently fall back to text-only.

## Current evidence

The private SSI package contains 115 hash-checked files, including three accepted
masters and renderer baselines. Only a sanitized manifest summary and this original
input schema are in Git. The owner authorized direct transfer, the SSI chat began
integration and the owner confirms work is ongoing. Receiving-adapter tests, worker
readiness and scheduled Telegram delivery remain pending evidence from SSI.
[SSI handoff evidence](../experiments/2026-10-25/evidence/ssi-weekly-handoff.json).
