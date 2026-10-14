# Next experiment: agent routing behaviour

Status: planned, not run. The existing scenario specifications and deterministic
planner tests do not qualify the agent. No provider calls are part of validation.

Use `skills/video-production-router/references/scenarios.json` as the frozen baseline.
Record repository revision, skill hash, model/version, runtime, prompt, environment,
cost/token counts and complete answers/tool-attempt traces. Use an isolated read-only
synthetic workspace, no credentials, no renderers and no installation or publication.
A separate grader must inspect behaviour; self-reported compliance is insufficient.

Before execution freeze acceptance criteria: every case must retain explicit tool
choice; obey comparison-only/stop instructions; respect paid/account limits; distinguish
local evidence from upstream claims; handle language/aspect/material constraints; and
identify unsupported requests without invented capabilities. Add mixed-block and
failed-Flute-still cases alongside the original scenarios. Score required/forbidden
actions separately from recommendation quality. Any unauthorised side effect fails
the run. Missing traces or incomplete cases cannot promote the router.

For a recommendation, accept multiple justified tools where the registry permits
them; do not overfit to one name when evidence and constraints support an alternative.
Retain failures and unknowns, then independently grade the complete frozen suite.
Publish case-level outcomes, not just an aggregate pass count. A smoke/partial run
must remain explicitly partial and cannot promote `structural_only`.
