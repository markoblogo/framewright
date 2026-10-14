# Second v3 development run — 49/52 overall, 50/52 model rubric

This complete run is **not** a qualification. All52 actors/answers/grades and exact
source remain retained. The separate model grader gives50/52; controller trace
inspection rejects one additional case, so the overall result is49/52.

- `reuse-existing-thumbnail`: real omission of explicit existing-image crop QA.
  MP4 crop QA and preserving the image unchanged do not fill that requirement.
- `storyboard-single-shot-skip`: borderline missing explicit absent-logo condition.
  The short prompt correctly restricts artwork to the authorised logo and makes no
  completed-verification claim. The grader still demanded its absence/uncertainty
  be explicit. The subsequent router makes that prerequisite explicit in the prompt
  without expanding the task into intake or a production plan; no grade was overridden.
- `storyboard-shared-shot-plan`: controller found one successful local user-skill
  read outside the actor's allowed inputs. The model rubric omitted an explicit
  outside-read criterion for that case, but the controller trace gate still fails.
  CLI user-context isolation was incomplete despite ignored config/rules and the
  host-discovery flag. The later run uses a separate CODEX_HOME and explicit host
  skill disablement; no local user configuration or policy was changed.

The22 opaque-ID controls were freshly graded and all matched strict expected
verdicts. `calibration-history.json` retains earlier20/20 and20/22 attempts and the
excluded premature actor launch. The initial 18 control packet is separately
retained with 17/18 exact matches; uncertainty is never a successful rejection.

[Initial v3](../grading-v3/README.md) retains different50/52 misses. These runs are
not stitched together, nor a causal quality score or unseen-transfer estimate.
Source snapshots avoid dependence on old Git objects. Machine-local citation and
outside-command paths are minimised with original SHA-256 retained; full raw
streams stay locally on Work. No renderer, provider, purchase, upload or release.
