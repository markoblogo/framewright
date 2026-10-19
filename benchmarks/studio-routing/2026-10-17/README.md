# Conditional studio routing — targeted check, 2026-10-17

Frozen source:[905c400967](https://github.com/markoblogo/framewright/commit/905c400967dda42fe1dd9d86b65dfc8c0b8511eb),after PR36 fixes. Scope:repackaging,Insight→Video and hybrid planning on newly authored fictional requests. No actual footage,article,music folder or media model. This is a targeted source-bound check,not an independent held-out benchmark,render test or new broad router qualification.

## Results kept separate

| Layer | Observation |
| --- | --- |
| Deterministic workflow CLI | **11/12 matched frozen expectations**;one expectation incorrectly assumed an automatic EN Supertonic3 profile |
| Capture integrity | **8/8 complete**,51/51 commands terminal,all exit0,all actor workspaces unchanged |
| Semantic decisions | **8/8 manual controller passes**,56/56 frozen required/forbidden criteria;no independent calibrated grader |
| Media production / publication | None;no renderer,voice inference,transcription,model download,folder scan,upload or release |

These numbers are not added to earlier70/70,62/70 or13/18 records. `router-qualification.json` stays unchanged. The eight requests were frozen before one pass through the existing runner;no retry,actor tuning or new grader-model calls. Constraint classes overlap known boundaries;new wording does not prove generalisation to every new task.

## Natural-language cases

| Case / retained answer | Main boundary | Controller result |
| --- | --- | --- |
| [Recut:unknown original music](evidence/recut-separate-audio-rights/answer.txt) | Telegram provenance≠video/audio rights;replace audio only under separate permission | PASS |
| [Recut:interesting quote selection](evidence/recut-manual-semantic-boundary/answer.txt) | auto-editor/PySceneDetect are not semantic selectors;human context labels/manual assembly | PASS |
| [Recut:explicit Flute](evidence/recut-explicit-flute-input-gap/answer.txt) | Flat video does not become live React,depth or tested rack focus;explicit choice stays blocked | PASS |
| [Insight:unsupported42% claim](evidence/insight-source-claims-native-still/answer.txt) | Retain measured cadence and measurement limitation;reject marketing claim;preserve native still/voice preference | PASS |
| [Insight:vertical physics](evidence/insight-vertical-evidence-and-budget/answer.txt) | Horizontal staged3D evidence does not qualify vertical/native still/calibrated wind;UK voice scope retained | PASS |
| [Hybrid:music-purpose downgrade](evidence/hybrid-purpose-music-downgrade/answer.txt) | Noncommercial music subplan cannot clear a commercial whole-film use | PASS |
| [Hybrid:separate layers/delivery](evidence/hybrid-multilayer-still-and-speech/answer.txt) | Silent retained footage,Remotion chart/native still,SupertonicUK,master mix,stems/captions/copy/provenance/QA | PASS |
| [Hybrid:feasibility only](evidence/hybrid-blocked-phase-no-authority/answer.txt) | No checkpoint/scan/asset intake;SDXL/Whisper/ACE-Step not safe tested defaults under CPU/no-download caps | PASS |

`cases.json` has exact criteria;`inputs.json` has prompts and fictional context. Actors saw source guidance and request only,not expected routes or criteria. Each required verdict in `actor-results.json` cites an exact answer quotation/line. Controller reviewed all command attempts and answers for forbidden behavior. Absence of a provider action is observed evidence for this run,not a promise of enforcement in production.

Two interpretation notes remain visible:preserving an explicit EN Supertonic preference can mean conditional/blocked rather than silent substitution;preserving manual MoviePy status does not require naming MoviePy when the plan uses FFmpeg instead. Neither rule requires inventing support or adding an unnecessary tool. No case received a pass from keyword matching alone.

## The CLI mismatch is an expectation error

The final CLI case expected a ready FFmpeg→Remotion+SupertonicEN chain. The current structured profile indexes Supertonic narration only for UK,so it correctly returns `blocked` with narration unmet. A retained English film/listening assessment exists,but its record explicitly says it does not promote an automatic EN recommendation.

[Original CLI results](cli-results.json) remain **11/12**,with the failed expectation intact. [Adjudication](cli-adjudication.json) records the source evidence and classification;no convenient12/12 replacement score. The separate insight actor found the same distinction unaided. This is a discovery/coverage limitation to consider later,not evidence that the selector must ignore its language gates. A future owner-approved change can index the exact tested ENF1 scope,or a new brief can choose the indexed English Kokoro route explicitly.

## Reproduction without model calls

```sh
python3 scripts/check_studio_cases.py benchmarks/studio-routing/2026-10-17 --verify-retained
```

This checks retained byte hashes,source/fixture identities and complete command/turn capture. It does **not** independently validate manual semantic grades.

Optional deterministic replay,from a checkout with the frozen router source:

```sh
python3 scripts/check_studio_cases.py benchmarks/studio-routing/2026-10-17
```

The expected exit is1 for the documented frozen expectation mismatch. It calls only the public workflow helper on temporary JSON,no media. A changed source tree is rejected;it is not relabelled as the old evaluation. Do not overwrite `cli-results.json` or rerun actors just to improve scores. Full prompts/freeze let a separately authorised future run reconstruct clean workspaces from published905c400,with `scenarios.json` withheld,using the existing `run_router_actors.py` contract. Private authentication home is outside the packet;its disposable credential copy was removed after the run.

## Resources and limitations

Model under test:gpt-6.1-sol,medium,CLI0.162.0-alpha.17.2;one worker,180s/case cap. Eight model calls,zero retries,314.04s summed actor runtime. CLI reports1,071,447 input tokens including803,328 cached input tokens,10,229 output tokens;cached tokens are a subset,not an additional total. Billing cost is unknown. No new paid media-provider API was used.

All eight logs contain the same nonfatal under-development warning for `skip_host_skill_discovery`,encoded by this CLI as an `item.type=error`. Warnings are retained verbatim in raw logs/metrics. There are no failed turns,unfinished commands or parse errors;these warnings are not silently removed or portrayed as production guarantees.

**Efficiency finding:** actors repeatedly read entire matrix/catalogue/selection documents. Cached-token accounting explains some of the volume,but broad repeated reads remain overhead. Prefer targeted search/profile lookup before adding more test calls or a larger benchmark. No runtime/router instructions were changed during this frozen run.

[Metrics](metrics.json) · [Protocol](protocol.txt) · [Freeze](freeze.json) · [Actor grades](actor-results.json) · [File hashes](evidence-hashes.json).
