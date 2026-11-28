# YUMINA-STATE-01 — native browser mini-game follow-up

26 November 2026. **Stock UI partial; bounded game/save/restore/reload passes
with a retained local upstream wiring repair.** This extends the same trial
family, not a new film or additional duplicate public trial.

## What actually ran

Pinned Yumina OSS f44419c5f47325ee964c9f7a7d3310a0a640cf8d, native Vite6.4.1
app, Hono HTTP server, single-user local authentication, sandbox rootComponent
SDK and on-disk PGlite. Ego Lite browser, separate task space; original tiny
lighthouse scene authored with React/SVG. No replacement web shell, mocked
server, injected game state, LLM dialogue, paid requests or new model weights.

The prior technical database backup was copied into an isolated UI directory.
Fixture setup associates its synthetic user with Yumina's documented automatic
local account and adds the custom world interface. Existing technical backup
remains unchanged. Game actions and saves/restores were clicked on screen;
read-only session API/store inspection provides supporting assertions.

## Checks and discovered defect

- Local edition descriptor reports single-user auth, local storage, billing,
  official models and telemetry disabled. Automatic browser sign-in succeeds.
- Native UI restart returns battery80. Inspect panel changes it to70. Clicking
  Save checkpoint creates a real server checkpoint. Lamp and door choices
  produce45 then35 and visible beacon/door changes.
- **Unmodified client defect:** the checkpoint is in the database/store but not
  visible to the custom game's documented `api.checkpoints`. `chat-view.tsx`
  hardcodes `checkpoints: []` into both sandbox API payloads. Its documented
  save/load API promises a pushed checkpoint list. Consequently the original
  mini-game cannot offer its restore buttons; do not call stock UI fully passed.
- Local repair subscribes to existing native checkpoint state, replaces those
  two empty arrays and updates memo dependencies. No backend, save format,
  rule engine or checkpoint restoration code is changed. Patch and before/after
  source hashes are retained externally; source revision must be labelled
  **f44419c + Framewright checkpoint wiring patch** for this UI result.
- Initial page reload still served stale transformed source from Vite on Work.
  Read-only fetch confirmed old code. Restarting only Vite loaded the repair.
  This is a development-server observation, not evidence of lost game saves.
- After repair: existing saves appear; restoring70 works. Creating a new save
  adds it to the list without a reload (three total). Repeat lamp45/door35,
  restore newest save70: inspected=true, lamp=false, door=false. Page reload
  preserves variables, rule state and saved checkpoint list. Screenshots show
  the restored70 state, unlit beacon and closed door. 13 recorded UI checks.

One early automation wait selected a standalone numeric text node rather than
its complete label; that timeout was a test selector error, not a Yumina failure.

## Resources and limits

Filtered app dependencies installed on Work with lifecycle scripts disabled:
362 additional packages, 29m31.1s first install. Native server cold-start and
Vite module loading also waited heavily on disk file operations; sampled stacks
showed filesystem reads/stats. Patched Vite reported38.976s to ready. These are
observed setup timings, not controlled performance benchmarks. This first UI
setup was heavy for a small warm-up; retained dependencies avoid reinstalling.

Server wrapper uses sanitized environment, suppresses dotenv, and refuses
external fetches; zero external server fetch attempts were recorded. Browser
HTTPS requests were blocked. No provider keys, model downloads, paid generation,
hosted account action or publication. Code/font packages are dependencies, not
model weights. AGPL-3.0-only upstream code stays outside the MIT repository.

This qualifies one deterministic local custom-UI game path **with local repair**.
It does not qualify generated dialogue, music/audio playback, quality of a full
story, hosting, complete backend restart, clean-machine transfer or PlayMCP
replacement. Page reload is the tested reopen boundary. Owner creative/gameplay
acceptance is not recorded. Video production ranking profiles remain unchanged.

## Retained result and replay

Private studio production: productions/yumina-state-trial-2026-11-26/ui/ and qa/.
Keep world JSON, authored lighthouse.tsx, run.py, checkpoint-wiring.patch,
source hashes, UI result JSON, stock defect screenshot/snapshot, repaired
screenshots and live UI database. ui/README.md gives exact local restart and
manual replay steps. Browser result remains at local app8932; API8931, both
loopback-only. No public URL or deployment was created.

[Previous native handler/backup test](yumina-state-2026-11-26.md).

## Owner decision

Owner adopts Yumina as an additional tool with the explicit local checkpoint-wiring
repair caveat. This accepts the retained deterministic local scope,not unmodified
stock operation,live dialogue,hosting or replacement of the existing game stack.
