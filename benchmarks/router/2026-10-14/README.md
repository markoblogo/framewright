# Router decision checks — 2026-10-14

Latest: [protocol v3 52/52 with fresh 22/22 controls](grading-v3-complete/README.md).
Earlier [integrated 43/46](storyboard-integrated/README.md),
[transfer 9/12](transfer-1/README.md) and [v4 30/30](qa-v4/README.md) remain.

All earlier packets below preserve their own source, rubric and results.

These are synthetic planning cases, not music/video-generation trials. No private
song, lyric, account record or media is included. Each actor used a fresh Codex CLI
context; grading used separate contexts of the same model family, followed by
controller review. This is not independent third-party certification.

| Packet | Evaluated source commit | Cases | Strict model-rubric passes |
| --- | --- | ---: | ---: |
| [First complete run](round-1/manifest.json) | `562008e` | 23 | 19 |
| [Second complete run](round-2/manifest.json) | `525200b` | 26 | 22 |
| [Targeted regression](regression/manifest.json) | `07d0b54` | 8 | 6 |
| [Stage-aware v2](qa-v2/manifest.json) | `62c52c8` | 29 | 29 |
| [Post-review v3](qa-v3/manifest.json) | `b1b454e` | 30 | 29 |
| [Historical v4](qa-v4/manifest.json) | `9c2ec79` | 30 | 30 |
| [First-exposure transfer](transfer-1/manifest.json) | `6af1f50` | 12 | 9 |
| [Storyboard integrated](storyboard-integrated/manifest.json) | `7c67b1f` | 46 | 43 |
| [Initial v3](grading-v3/manifest.json) | `c142ff6` | 52 | 50 |
| [Second v3](grading-v3-final/manifest.json) | `8c21ee1` | 52 | 49 |
| [Isolated v3](grading-v3-isolated/manifest.json) | `5befe6d` | 52 | 51 |
| [Complete v3](grading-v3-complete/manifest.json) | `5befe6d` | 52 | 52 |

Each packet now includes a `source-snapshot.zip` with exactly the router files
listed in its frozen source hash map. Commit IDs are provenance labels; those
intermediate commits need not be reachable after a squash merge. Source snapshots,
not Git reachability, are the reproduction basis. The packet checker verifies every
archived member against the frozen hashes without executing or extracting it.

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
with a favourable controller score. The catalogue retains its legacy `structural_only` status; the separate current
scope record is tied to the isolated-v3 snapshot; a record with gaps is not
a complete passing qualification.

V3 added an execution-request contract-read case; one existing language case failed
to request a missing choice or propose a bounded test. V4 repeats all 30 cases
after that instruction was clarified. No favourable answers were stitched across
runs. V3/v4 reuse the retained opaque-ID controls with unchanged grader protocol
and core configuration. See the report for scope and response-budget differences.

The first software-only smoke and an overlapping batch-4 grading attempt were
retained locally but excluded; the identical complete batch-4 input was graded once
again after excluding the mixed attempt. Per-batch exclusive lock files now prevent
overwriting an active grading output. Actor runs were not replaced by this repair.

## Inspect or repeat

1. Read a packet's `inputs.json`, `cases.json`, `freeze.json` and `protocol.txt`.
2. Verify the packet, then extract its `source-snapshot.zip` into a separate
   directory. Compare archived files with `freeze.json`; no historical Git object
   or old branch is needed. The repository MIT licence covers these original files.
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
