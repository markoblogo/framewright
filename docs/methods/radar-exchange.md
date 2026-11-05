# YouTube Radar ↔ Framewright: explicit local exchange v1

An optional local adapter links an owner-selected research idea to a studio
project and returns production/publication receipts. It does not select a film,
render, acquire analytics, publish, register an experiment or run on a schedule.
This is local development after0.8.0, not a released capability.

## Evidence and limits

The5November2026 bounded control linked Living Muscle (`LIbkbgDCgKM`) and
InfraDev (`h3xC5FRlW30`) to their exact retained Radar cards. Two deliveries of
each association/status produced two project links and two video mappings.
The existing InfraDev intake was referenced unchanged, not duplicated/promoted.
Original project JSON, retained masters, research and existing core adapters
retained their hashes. Both analytics exports returned `pending`: the retained
2November acquisition has no matching reports for these videos. No live API
request or prospective experiment was performed.

Private evidence: studio `records/radar-framewright-contract-2026-11-05/`
contains the approved contract, control inventory, owner acceptance and
`manual-control-result.json`; exchange state lives separately in
`records/radar-framewright-exchange-v1/`. Do not commit those private packets.
Synthetic tests additionally cover corruption, unavailable storage, stale status,
identity conflicts, missing ideas, nullable metrics and a crash after apply before
acknowledgement. These are transport tests, not future production proof.

## Contract

The envelope uses `radar-framewright/v1` and five kinds: `idea_menu`,
`association`, `production_status`, `analytics_snapshot`, `receipt`.
The [JSON schema](../../skills/video-production-router/references/radar-exchange.schema.json)
checks envelope structure; `radar_wire.py` also checks hashes, identities and
kind-specific payloads. Both repositories vendor the same small stdlib wire
implementation; neither imports the sibling at runtime. Keep the copies/schema
identical when changing the contract and rerun both test sets.

Each side writes only its own state/outbox. Explicit commands or enabled checkpoint/run
hooks pull immutable JSON messages from the peer outbox. Apply and the processed marker commit together;
acknowledgements follow, can be retried, and never acknowledge acknowledgements.
Pending/rejected payloads cannot partly alter application state. Invalid envelopes
return a rejection without a persisted acknowledgement. Sequence numbers prevent
an older production state rolling back a newer state. Hashes detect corruption;
they are not sender authentication. Use a trusted, local owner-controlled root.
Files/state are capped at1MiB; the root must already exist and cannot use symlinks.
Capacity exhaustion stops a write; there is no automatic pruning or disk fallback.

The selected card is frozen beside the project in `radar-link.json`; source
`project.json` is unchanged. `retrospective_observation` records an existing film,
never backdates a hypothesis. `prospective_hypothesis` requires explicit owner
selection/before-production attestation, no retained output and sources checked
within72hours. It still does not register or approve a Radar experiment: the
existing preregistration/approval guards remain authoritative.

Native journal projection checks all dependency pins and excludes stale/superseded
acceptance and publication receipts. Current status derivation supports selected, blocked, ready_for_review, accepted
and published. There is no started event yet. Only YouTube associations and
analytics are implemented; TikTok remains outside this adapter. Creative and
listening acceptance are separate pinned receipts. Owner-provided URLs preserve
`owner_report`; they do not establish independent visibility or uploaded identity.

Analytics imports require a known project/video, configured channel, explicit
period/timezone, availability, currency when revenue is present, and a verified
retained acquisition digest. Calendar7/28-day query windows are not elapsed time
since upload. Missing metrics remain null, missing videos remain pending, and
synthetic metrics are rejected in normal state. Duplicate matching report rows
are rejected, rather than summing average durations. YouTube Analytics daily
boundaries use [Pacific time](https://developers.google.com/youtube/analytics/dimensions).

## Manual operation

Set `EXCHANGE` to an existing external directory and `PROJECT` to the explicit
project JSON. Commands preview without `--apply`; `status` is read-only.

```sh
python3 skills/video-production-router/scripts/radar_exchange.py --exchange "$EXCHANGE" status
python3 skills/video-production-router/scripts/radar_exchange.py --exchange "$EXCHANGE" --apply configure --channel-id "$CHANNEL"
python3 skills/video-production-router/scripts/radar_exchange.py --exchange "$EXCHANGE" --apply receive "$MENU_JSON"
python3 skills/video-production-router/scripts/radar_exchange.py --exchange "$EXCHANGE" --apply select "$PROJECT" --project-id "$PROJECT_ID" --research-revision "$PACKET_SHA" --idea-id "$IDEA_ID" --mode retrospective_observation --owner-approved
python3 skills/video-production-router/scripts/radar_exchange.py --exchange "$EXCHANGE" --apply export-status "$PROJECT"
```

Deliver the returned message's matching outbox file to Radar's explicit receive
command. Return receipts the same way. Do not run wildcard imports from untrusted
folders. On failure retain source/outbox evidence, fix the cause and retry the
same message; do not delete processed markers to force a second application.
Frozen links cannot be silently reassigned; an actual mapping correction needs a
separate migration design/owner decision. Do not edit source records to repair it.

## Opt-in automatic checkpoints and normal runs

After review, the owner authorised enabling the existing local work-loop hooks,
without adding a schedule. `enable-auto PROJECT` writes a private `radar-auto.json`
beside an already linked studio project. Its next successful project CLI save pulls
Radar messages and exports the pinned status. Read-only brief/status commands do
not trigger the hook. A missing external exchange produces a local pending receipt,
not a failed project save or another storage tree.

On the Radar side `enable-auto --radar-root ROOT` enables the existing `run`
boundaries: pull associations/statuses, include known linked video IDs in the
existing acquisition, then export the retained research/menu and available7/28-day
calendar report snapshots. This does not make an extra API acquisition or change
its schedule. Optional exchange failures preserve the primary Radar report/result.
Each side processes at most250 peer outbox files and100 linked videos per run;
capacity exhaustion requires manual rotation and is recorded pending.

New projects still need explicit owner selection and explicit opt-in. No automatic
choice, production, experiment registration, public upload or algorithm adjustment
is enabled. Actual next weekly run and future prospective feedback are separate
observations, not proved by synthetic run tests or configuration.

## Remaining gate

The next owner-selected film can exercise a truly prospective cycle. Actual
mature analytics, interpretation and the first actual normal-run outcome remain
open. This control does not close REL-D or justify a release.
