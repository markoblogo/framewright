# YUMINA-STATE-01 — native local state, checkpoint and rewind

26 November 2026. Technical scope passed; no owner gameplay or visual verdict.

## Route and fixture

Pinned Yumina OSS f44419c5f47325ee964c9f7a7d3310a0a640cf8d (0.0.85.0),
Node/pnpm, native TypeScript engine, server route handlers and PGlite on the
current Apple Silicon Mac. Installed filtered server/engine/shared dependencies
on Work with lifecycle scripts disabled; 539 packages, first install 17m 9.9s.
Built shared and engine with native tsup. No model weights, paid requests,
provider keys, hosted account or public upload. Upstream code was not patched.

Original three-choice lighthouse fixture: inspect equipment, switch on lamp,
open door. Native rules enforce prerequisites and change battery/flags. User
and assistant history are synthetic test records; assistant snapshots contain
actual persisted engine state. They are not generated model conversations.

## Results

20 native assertions passed, plus six independent-process backup checks:

- Invalid early door action leaves it closed. Inspect changes battery 80 to 70;
  native checkpoint saves that state and message history.
- Lamp changes battery to 45 and emits the native low-power audio event;
  door changes it to 35 and opens. The short original cue was locally synthesized.
- Native message rewind restores the preceding assistant snapshot: 45, lamp on,
  door closed. Native checkpoint restoration returns 70, lamp off, door closed,
  with rule counters and saved history length restored, rather than defaults 80.
- Replaying the lamp action fires the threshold cue again. Repeated checkpoint
  restoration preserves variable values; missing checkpoint and wrong-owner
  requests are refused. Engine snapshot reconstruction preserves variables.
- Native PGlite backup is reopened in a separate process: session variables,
  rule counters, checkpoint and message count match. Both test processes prohibit
  fetch and record zero attempted fetch/provider calls during execution.

Native test body took 2.67s; full test invocation including startup took 95.2s.
This is one fixture, not a performance benchmark. Dependencies were downloaded
during setup; network prohibition applies to execution, not installation.

## Boundaries and decision

Use as a tested local candidate for branching-state prototypes with checkpoints.
Do not replace PlayMCP or claim native UI/game quality, audible music playback,
HTTP authentication, AI dialogue, full app restart or clean-machine portability.
Native handlers were invoked directly using the upstream test-fixture pattern;
wrong-owner refusal tests handler ownership logic, not the complete login flow.
Fresh-process verification reads a native database backup, not a running frontend.

Readability, motion, drawing stability and visual artifacts: not assessed.
Controllability: observed within this rule/checkpoint/history fixture.
No provider charge; local compute/work unpriced. AGPL-3.0-only code, CC BY 4.0
docs and separate hosted/model terms remain unchanged; no copied vendor code
enters the Framewright repository. A later visual or model-backed test needs a
specific selected use case and separately confirmed access. No repeat needed
for these unchanged state mechanics. Production ranking profiles remain unchanged:
this nonvisual interface/software probe does not qualify a video renderer.

## Retained evidence

External studio: productions/yumina-state-trial-2026-11-26. Retained world JSON,
original cue, native database backup, expected reopen values, both runnable test
harnesses, build/test logs, result JSON and source/checksum receipt. Source runtime
stays under tools/yumina-f44419c; all new files are on Work.

## Later native UI follow-up

[Browser mini-game follow-up](yumina-ui-state-2026-11-26.md): stock checkpoint-list
wiring defect reproduced; save/restore/page reload passed with a retained local
client repair. Earlier unmodified handler and backup results remain separate.
