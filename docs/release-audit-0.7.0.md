# Framewright0.7.0 REL-B — frozen pre-publication audit

1November2026. Owner explicitly authorised preparation and publication of REL-B.
This document records the release candidate; canonical GitHub records and an
operator verification receipt establish later publication, not this text alone.

## Identity and scope

Repository markoblogo/framewright. Release branch release/0.7.0; base merged PR50,
`ff84b1d6760c7be5f866821bbed7afda14050be0`. Latest observed published release before
preparation: experimental0.6.0. Version0.7.0 is an experimental minor capability
increment. This branch changes version/README/changelog/release status and notes,
not runtime behavior. [Notes](release-notes-0.7.0.md) ·
[REL-B readiness](rel-b-readiness-2026-11-01.md) ·
[local review](rel-b-local-review-2026-11-01.md).

| Domain | Preparation evidence and boundary |
| --- | --- |
| Source/base | PROVEN: clean main, PR50 merged; reviewed and merged trees match |
| Tests/review | PROVEN:514local tests/18skips, one-round independent approval; PR50 and merged-main CI pass. Candidate metadata/package checks and release PR/CI recorded separately by publisher |
| Runtime/production | PARTIAL: bounded repeat, two accepted aspects, protected correction/read-only recovery; no full autonomous route or labour-savings proof |
| Human authority | PROVEN: owner asks to prepare and publish REL-B; authority includes release PR/CI/merge/publication, not unrelated production or platform posting |
| Tag/public release/assets | UNKNOWN at this frozen source point; verify actual final tag commit, experimental non-draft state, asset downloads and SHA256 after publication |
| Deployment/SEO/locales/device UI | N/A: Python/Markdown skill ZIP and source examples, not a deployed site/device release |

## Candidate procedure

Run narrow metadata/link/matrix checks and build the ZIP outside the checkout.
Inspect contents, ZIP integrity and SHA256SUMS. Source full-suite evidence and CI
already exist; metadata-only edits do not require an additional local full run.
Release PR/CI still runs the repository suite. Merge only a reviewed/check-green
release head; verify the merged tree and its CI before publication. Create the tag
from the verified final merge commit and publish a non-draft experimental prerelease.
Verify anonymous canonical-page availability, exact tag commit and downloaded ZIP
checksum. Never infer these from local build, prepared links or release-create exit0.
No models, private media, credentials, Git metadata or provider sources are bundled.

No mandatory data migration. Caption timing is an optional English heuristic in a
source example, not a new mandatory installed-skill requirement. Separate platform/
media terms and per-version creative/listening approvals remain in force.

## Canonical publication records

[Release](https://github.com/markoblogo/framewright/releases/tag/v0.7.0) ·
[Source tag](https://github.com/markoblogo/framewright/tree/v0.7.0) ·
[Router ZIP](https://github.com/markoblogo/framewright/releases/download/v0.7.0/framewright-router-0.7.0.zip) ·
[Checksums](https://github.com/markoblogo/framewright/releases/download/v0.7.0/SHA256SUMS).
The publishing operator retains a separate exact-commit/CI/download receipt after
these become live, avoiding a circular change to the commit being verified.


## Locally verified candidate package

Standalone build/smoke and ZIP integrity passed. Router ZIP: 381210bytes,
87entries; SHA256 `1ec7b6721f1355e1ae2b3b208afea4c77e67676378832ac51b2b2508daeb9331`. SHA256SUMS matches.
This is candidate build proof only; exact release commit/CI/tag/download identity
will be verified by the publishing operator. No local full-suite repetition for
metadata-only edits; release CI remains required.
