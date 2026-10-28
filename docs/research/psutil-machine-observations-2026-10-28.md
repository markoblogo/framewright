# psutil: measured host/process observations — 28 October 2026

Status update: optional RESOURCE-01 is implemented and internally tested;
[actual bounded Mac probe and limits](../experiments/studio-foundations.md).
psutil7.2.0 was installed only in a private isolated test environment, not as a
default dependency. Root/child coverage can be partial; no host-fit qualification.
The design below records the original proposal; the linked implementation contract
states which parts are available.

## Official basis

[psutil repository](https://github.com/giampaolo/psutil) identifies BSD-3-Clause and
cross-platform system/process monitoring, including macOS, Windows and Linux.
[API documentation](https://psutil.readthedocs.io/stable/) distinguishes available
memory from merely free memory. The first nonblocking CPU percentage sample is
meaningless and should be discarded; process and platform-specific metrics may be
unavailable or raise access/process-lifetime errors. Verify the installed version's API.

## Fit to Framewright

Extend existing [environment/readiness reports](../../skills/video-production-router/references/trials-and-readiness.md)
and the intake machine snapshot, rather than adding a second capability database.
Current `environment.py` already checks platform, total RAM, free disk, explicit
program/model presence and optional version/hardware probes. Those meanings must
remain intact; adding available RAM cannot silently reinterpret total-memory checks.

Proposed RESOURCE-01 measurement layer:

| Evidence level | Example | Interpretation |
| --- | --- | --- |
| Detected | OS/architecture, total/available RAM, swap, free disk | Time-bound observation, not workload compatibility |
| Checked against requirement | Observed free disk exceeds a declared requirement | Passes that requirement at that time only |
| Runtime observed | Selected process's sampled RSS/CPU, duration and output check | Scoped behaviour under the retained run settings |
| Unknown / unavailable | GPU framework fit, codec support, denied metric, unsampled peak | Explicit gap; never converted to zero or “computer fits” |

Availability is workload-relative. A small current process footprint does not prove
the next model or full-resolution export will fit. Keep GPU/Metal/CUDA framework and
model execution, codec/container support, storage throughput and media-output checks
in dedicated adapters. Network byte counters do not measure internet speed. Core
count, free disk and battery state do not establish rendering performance.

## RESOURCE-01 — bounded observation contract

For an owner-selected local task, record UTC/time-zone-aware observation timestamps,
monotonic elapsed time, psutil/runtime version, host platform, units, sampling interval,
sample count and missing/failed metrics. Read only explicit working/scratch/output
volumes; no recursive disk scan or large speed test. Initial snapshots should include
available memory and swap alongside total memory/free disk, with their distinct labels.

Attach a sampler only to the executor-owned process and, where supported, its child
tree. Bind process identity to PID plus creation time to avoid PID reuse confusion.
Record the worker lifetime and child coverage; handle exited or inaccessible children
as partial coverage. Do not enumerate unrelated process command lines, environment,
open files or network connections. No persistent background monitoring by default.

Report sampled peak RSS as **sampled**, not a guaranteed high-water mark. RSS is not
unique memory; sums across children can double-count shared pages. Keep system load
and process usage distinct, and avoid equating CPU percentages with whole-machine
utilisation without stating their convention. Missing sensors/counters and permission
errors remain unavailable/unknown, not zero usage or failed rendering.

Bound the interval, duration and output size so observing does not become another
heavy workload. Thresholds require a stated workload/resource basis and sustained
samples where appropriate. This first measurement proposal does not automatically
kill/pause a process or provide hard memory enforcement. Any later stop policy must
use executor ownership, record its reason and preserve partial-result evidence.

If psutil is absent, retain existing observations and mark the additional metrics
unavailable. Do not auto-install it, infer adequate resources, or fail unrelated
source review merely because optional telemetry is absent.

## First internal test and pass boundaries

1. After normal installation/resource approval, use a pinned optional psutil adapter
   in an isolated environment. No model, paid API or new production is needed.
2. Observe a deliberately small owned child workload for a few seconds with capped
   allocation. Compare available/total memory and sampled process values; inspect
   known units and timestamps rather than demanding exact machine-wide numbers.
3. Test no library, denied access, process exits/PID identity mismatch, missing
   platform metric and incomplete child coverage with synthetic controls. Confirm
   that missing observations stay unknown and no unrelated process is changed.
4. On a later authorised renderer trial, retain measured resource/time observations
   with input/model/settings/output pins. Compare a small run with that exact
   bounded scope only; do not extrapolate unmeasured full-video feasibility.

Pass: honest detected/checked/unknown reporting, bounded observer overhead, explicit
partial coverage and stable operation when metrics are missing. Synthetic controls
validate software behaviour; only real retained samples qualify the exact host run.

## Relationship to the queue

RESOURCE-01 is a small supporting component for intake, the existing trial workbench
and COMFY-01. COST-01 may use observed runtime as a measurement, not invent monetary
cost from CPU/memory alone. This is a planned optional enhancement; current readiness
and sequential execution behaviour remains unchanged.
