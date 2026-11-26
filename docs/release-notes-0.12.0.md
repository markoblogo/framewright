# v0.12.0 — recover the selected delivery

Experimental prerelease,26November2026. Version0.12.0 packages selected-delivery recovery and scoped preview refinements. The owner authorised PR,integration and publication conditional on passing final checks;the GitHub release and its exact assets are the authority for publication state.

## Exact functional scope

- Explicitly bind an accepted selected master to its existing review/publication manifest with `project.py attach-delivery`.
- Recover that package through `project.py brief` and `open-delivery`:revision,exact master,cover,subtitles,copy,review page/restart command,owner waits and proposed next action.
- Recheck retained files and acceptance;changed or rejected packages need review instead of reopening as accepted. Existing publication/field-test waits are not retired by reopening.
- Preserve previous-version projects;absence of a new delivery binding remains explicit,not fabricated from folder names or publication URLs.

Core implementation:`project.py`,`project_delivery.py`,`project_summary.py`;regression cases in`tests/test_project_delivery.py`. [Recovery contract](../skills/video-production-router/references/projects.md#reopen-an-accepted-review-delivery) · [Actual Radar18 case](experiments/radar18-selected-delivery-recovery-2026-11-26.md).

## Supporting changes included

Existing standard preview refinements in`delivery.py`/`preview_server.py`:explicit YouTube Shorts portrait presentation and explicit download disposition while retaining normal aspect/path/range policies. Current source-linked production cases,catalogue observations,queue reconciliation and compact working instructions accompany the release. They do not qualify every listed tool or imply new model evaluations. Exact changed-file grouping and candidate hashes are retained with the local readiness audit.

The current unqualified-source digest binding is refreshed to match retained catalogue/preview changes;historical actor snapshots/results and`not_evaluated_current_source`status remain intact. No actor or model run is part of this release preparation.

## Excluded claims and work

No portable copy of private media,full historical rebuild,clean-machine or independent-human transfer. Full reverse-analysis OCR/ASR/listening,GUI OTIO import,new models/providers,automatic social publication and new game productions are excluded. The two planned game reviews remain useful later repeatability work,not required films to unlock this scoped release.

The archive contains the router,its local references/scripts and licence. Original projects,media and required local tools remain separately available on the studio Mac. Optional repository documentation links target the candidate tag and can only be publicly verified after authorised publication.

## Verification and publication gates

See the [dated local readiness audit](release-readiness-0.12.0-2026-11-26.md) for actual results,source/archive pins and failures. The final commit must pass the complete offline check entry point and GitHub CI. The owner has authorised merge and prerelease publication when those checks and bounded review pass. Public tag/archive/checksums still require post-publication verification.
