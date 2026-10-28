# PR #46 — publication checks and review corrections

28 October 2026. [PR #46](https://github.com/markoblogo/framewright/pull/46)
collects the locally accumulated production-method, execution, source-editing,
research and documentation slice. No new video, paid call, release or merge is
implied by this packaging pass.

The original head `0ed70f1` passed both GitHub validation jobs: 464 tests,
15 optional-dependency skips, historical evidence integrity, links, generated
reference and temporary packaging. The initial local full run passed 463 tests;
the extra TMPDIR-independent lock regression then passed among 14 executor tests.
The final committed GitHub run included it in its total of 464.

## Automated review corrections

- **OTIO composition trims:** a native-library control reproduced a false unchanged
  result for a trimmed Track. Track and Stack source ranges now fail explicitly;
  callers must flatten these into child clips. The bounded profile does not claim
  general composition/FX preservation.
- **Corrected settlements:** replacing a four-unit bill after a three-unit refund
  with a two-unit bill incorrectly produced negative exposure. The same control
  now rejects the correction without changing the ledger; a valid three-unit bill
  reaches zero, not negative, net exposure.
- **Manifest-relative models:** the same retained manifest now resolves its relative
  model path from its own folder. A same-named file under the project cannot satisfy
  a missing neighboring prerequisite. Project/output disk checks remain separate.
- **Interrupted workers:** original controls reproduced a surviving worker after
  TERM and a prematurely released lock after KILL. Inspection/proxy workers now
  inherit the lock and their own process-group deadline. TERM/HUP/INT cleanup kills
  and reaps their group; executor KILL leaves its intent unresolved and the worker
  retains exclusion until exit. A separate one-second deadline control requires
  no executor supervision. Synchronous revision-comparison remains outside this
  managed-worker adapter scope.

Each correction retains private before/after logs. OTIO controls use the already
installed optional native library, not a skipped substitute. Final full checks and
follow-up review are recorded in the PR after the fix commit. Historical model
qualification is unchanged; no new model-evaluation result is asserted.

## Second review

A further native OTIO control reproduced rejection of a valid audio-only render
when its sound came from an audiovisual source. Required stream kinds now come
from timeline tracks, not unused streams in the media inventory; a picture-format
reference is selected from media actually used on picture tracks. A picture track
without a usable reference fails explicitly.

The first fix commit `07fe558` passed all 470 tests locally with the existing
native OTIO environment (one conditional skip), plus the complete offline integrity,
link, reference and packaging checks. Its GitHub runs passed 470 tests with 16
optional-dependency skips. The additional audio-only regression is verified in the
native OTIO suite and follow-up CI; current-source model qualification stays unset.
