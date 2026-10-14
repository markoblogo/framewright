# Router decision checks — 2026-10-14

These are synthetic planning cases, not music/video-generation trials. No private
song, lyric, account record or media is included. Each actor used a fresh Codex CLI
context; grading used separate contexts of the same model family, followed by
controller review. This is not independent third-party certification.

| Packet | Evaluated source commit | Cases | Strict model-rubric passes |
| --- | --- | ---: | ---: |
| [First complete run](round-1/manifest.json) | `562008e` | 23 | 19 |
| [Second complete run](round-2/manifest.json) | `525200b` | 26 | 22 |
| [Targeted regression](regression/manifest.json) | `07d0b54` | 8 | 6 |

The first 17 requests were frozen from the existing scenario file; six boundary
cases were added before the first run. The second run preserved all 23 requests
and criteria and added three held-out paraphrase/transfer cases. The final eight
are affected-case retests after instruction changes: **partial, not a new full-suite
pass or held-out result**. Never combine best answers across runs into a green suite.

Each packet retains frozen inputs/source hashes, full answers, all tool-attempt and
completion events, execution/fixture hashes, token usage and case-level grading.
Repeated command output is represented by byte count/SHA-256; original complete
CLI streams remain locally retained. An attempted command does not prove a read;
only successful completion can establish it. Fixtures contain no credentials.
The untrusted-source case intentionally includes a fake instruction to read them;
no such attempt appears in the recorded traces.

All observed routes matched their intended scope in controller review, and command
attempts stayed within document reads or the supplied offline helpers. That does
not establish safety with real production authority: the envelope explicitly
prohibited installation, spending, uploads and rendering and restricted capabilities.
No media quality, live account behaviour or general model consistency was tested.

Strict failures remain visible. See [controller review](controller-review.json) for
one evaluator inconsistency about planned versus completed QA and the ambiguity of
an existing thumbnail versus a newly rendered native PNG. No raw grade was replaced
with a favourable controller score. Catalogue qualification remains `structural_only`.

The first software-only smoke and an overlapping batch-4 grading attempt were
retained locally but excluded; the identical complete batch-4 input was graded once
again after excluding the mixed attempt. Per-batch exclusive lock files now prevent
overwriting an active grading output. Actor runs were not replaced by this repair.

## Inspect or repeat

1. Read a packet's `inputs.json`, `cases.json`, `freeze.json` and `protocol.txt`.
2. Check out the recorded source commit and verify the router file hashes.
3. For each case, copy that skill into a separate read-only synthetic workspace,
   omit `references/scenarios.json` (rubric hidden), and add only its listed fixture
   files. Never provide expected routes or criteria to the actor.
4. Use the recorded CLI/model configuration, retain the full answer/events and
   token usage, then grade in a separate context using the frozen rubric.
5. Inspect every action attempt and full workspace file set; preserve failures.

The local run used Codex CLI 0.162.0-alpha.17.2, `gpt-6.1-sol`, medium reasoning,
`read-only`, `--ignore-user-config`, `--ignore-rules`, `--ephemeral`, no app/plugin/
multi-agent tools, web search disabled, host-skill discovery skipped and a minimal
shell PATH. This is a bounded environment, not a portable container guarantee.
Model aliases and future replies can change. Monetary cost is unavailable; recorded
actor usage and summed worker seconds are not an account bill or wall-clock benchmark.

Validate packet integrity without launching a model:

```sh
python3 scripts/check_router_evaluation.py --root benchmarks/router
```

An integrity pass checks the declared counts and retained files; it does not mean
all behaviour criteria passed. See the [evaluation report](../../../docs/router-evaluation.md).
