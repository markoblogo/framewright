# Eight incomplete CLI captures — targeted recovery

2026-10-15. **8/8 complete captures, 34/34 command lifecycles, 8/8 rubric passes**.
Eight fresh actors and two separate grader calls; no automatic retries. Same
requests, fixture contents, router snapshot, model/effort and v5 criteria as the
[eight incomplete cases in the parent run](../qa-v5-complete/README.md).
This is a targeted infrastructure regression, not a new 70-case score or unseen test.
The overall qualification record remains tied to the historical 62/70 packet.
No renderer, audio generation, provider account, publication of media or release.

## Diagnosis and scope of the fix

The eight original raw streams contain valid JSON and `turn.completed`, but each
has one `/bin/zsh -lc` command without its terminal event. Their other reads often
use `/bin/zsh -c`. The old collector ignored malformed lines and treated exit 0 plus
a finished answer as adequate for grading; it did not gate on command completion.

[Paired shell probes](shell-probes.json): `pwd` took 0.1 s without login semantics;
the login version exceeded the 8 s timeout. All eight exact missing reads succeeded
without login semantics in 0.048–0.137 s. Those operator probes do **not** repair or
prove the outcome of the original calls. They identify login-shell startup as a
reproducible contributor; the particular local startup hook and the upstream CLI
handling of abandoned executions were not traced. No claim of an upstream fix.
The installed CLI was `0.162.0-alpha.17.2`.

The new reusable [actor runner](../../../../scripts/run_router_actors.py) disables
login shells with the documented [`allow_login_shell=false` setting](https://developers.openai.com/codex/config-reference/).
It retains stdout bytes/stderr, checks all started/terminal command pairs and rejects
malformed, duplicate, changed, unfinished or out-of-turn execution events before
grading. Exit 0 and a good answer cannot rescue a missing command completion.
Synthetic regressions cover interleaved completions, truncation, timeout, frozen
source drift and preventing overwrite. Account/global shell settings were not changed.

## Evidence and reproduction

- [Manifest](manifest.json), [summary](summary.json), [results](results.json),
  [grades](grades.json), [inputs](inputs.json), exact [router snapshot](source-snapshot.zip).
- Every new actor raw stream is retained as `<case-id>-events.jsonl` and hashed in
  the manifest. The validator compares its commands and final answer with results;
  capture completeness is recomputed, not trusted from a declared PASS.
- [Original gaps](original-gaps.json) name all affected IDs. Original logs/grades
  stay in the parent packet and were not overwritten or assigned invented events.
- [Prelaunch freeze](prelaunch-freeze.json) retains the original preparation verbatim,
  including the inherited parent's case hash/prompt map; [packet freeze](freeze.json)
  derives only the subset map/hash for the exported packet. Source/prompt contents
  were unchanged. The exact loaded actor runner and capture/grading helper are
  retained; their hashes match the prelaunch freeze. The maintained runner adds
  import support for tests and reports actual turn completion separately from
  complete command capture; actor configuration is unchanged.
- The 46/46 v5 calibration evidence is reused **unchanged**, not freshly rerun.
  Protocol, shared source facts, grader settings/model/effort are unchanged.
  Two fresh grading streams are retained. Controller review covers all actual
  attempted commands and complete answers; only authorised local reads were observed.

To reproduce, unpack the retained source into a new isolated root's `runs/<id>/router`
(omit `references/scenarios.json`), write the exact prompts and declared fixture text
from `inputs.json`, and use `cases.json`/`freeze.json`. Keep evidence outside those
workspaces and prepare an isolated Codex home. Follow the runner command in the
[checking policy](../../../../docs/checking-policy.md); name only these eight IDs.
The prelaunch collector hashes identify the retained `actor-runner.py`,
`cli_capture.py` and `prepare_router_grading.py`. Its flat runner accepts the same
arguments as the maintained entry point. Never overwrite an existing attempt.

Integrity-only check, no model call:

```sh
python3 scripts/check.py --scope capture
```

Actor median elapsed time was approximately 45 s. Usage is retained in summary;
actual billing cost is `NOT_AVAILABLE`. No controlled speedup/cost estimate follows:
concurrency and cache conditions differ from the earlier run. Using eight actors
instead of repeating seventy reduces the number of actor calls, not a proven bill.
This follow-up establishes capture recovery on these known cases only; it does not
qualify arbitrary environments, provider permissions, rendering or audience response.
