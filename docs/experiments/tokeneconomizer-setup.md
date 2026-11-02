# TokenEconomizer — scoped Codex setup

1 November 2026 · operator tooling · roadmap M4/R05/R09.

[Microsoft TokenEconomizer](https://github.com/microsoft/TokenEconomizer) is an
optional agent-session plugin, not a video renderer or a required Framewright
dependency. Apache-2.0; Python 3.10+. No copied upstream source is committed.

## Installed configuration

An existing native Codex installation was discovered and reused:
`tokeneconomizer@tokeneconomizer`, plugin version `0.1.0`. Its 54 Python core
files match upstream revision `ced014b468083139f4c1baf193cc0b176c1cc652`.
The temporary clean audit checkout was removed after verification; the installed
self-contained plugin remains. This also keeps external Markdown out of the
project's recursive documentation validation.

The existing user marketplace points at another local project's self-contained
bundle. It was not replaced or removed. The installed cache contains the core;
marketplace refresh still requires that original source. Reconfigure the source
explicitly if it is moved; do not silently replace another project's installation.

Only Framewright's TokenEconomizer profile was changed, using the installed CLI:

```sh
~/.codex/plugins/cache/tokeneconomizer/tokeneconomizer/0.1.0/scripts/te \
  --host codex --cwd /Volumes/Work/framewright config set \
  enabled=true microskills=envfacts toolprune=propose loopguard=off repomap=off
```

This profile is stored privately under
`~/.tokeneconomizer/repos/framewright-921aae5102/config.json`, keyed to this
repository. Existing global settings remain unchanged (`enabled=false`).
Other projects keep their existing overrides. No native hook trust entries were
written by this setup.

- `envfacts`: learn bounded facts from repeated failures, without model proposals.
- `propose`: suggest tool pruning; do not apply capability changes automatically.
- Loop guard and repo map: off. No extra model calls enabled by this profile.
- Private session-derived state stays outside the committed repository.

## Verification and activation boundary

Host inspected: Codex CLI `0.166.0-alpha.5.1`, newer than upstream's documented
tested range (`0.153.1–0.164.0`). Compatibility is therefore a bounded local
observation, not full host qualification.

62 upstream checks passed: configuration, plugin packaging, local-write safety
and environment facts. The installed cached launcher also processed synthetic
SessionStart, UserPromptSubmit, PostToolUse and Stop events in isolated state,
returning valid JSON with no stderr or error log. Evidence remains ignored at
`local/token-economizer-smoke/smoke-result.json`. No model generation was run.

These direct launcher checks do not prove native hook delivery in a fresh Codex
session. Start a new session rooted in Framewright. If Codex displays a hook
review, inspect and approve it through the host UI (`/hooks` where available).
Do not manufacture trust hashes. Then inspect status through
`$tokeneconomizer:status` or the installed CLI's `status` command.

The first real-session test remains queued: confirm delivery, inspect learned
facts for accuracy and measure overhead before considering broader activation.
Token savings have not been measured. Do not enable automatic pruning or paid
side calls as part of ordinary production without a separate decision.

The first settings write hit transient `No space left on device`; a retry
succeeded. The internal disk had about119MiB available at inspection. No user
files were deleted during that setup. Subsequent owner-authorized sanitation is
recorded separately in the [storage report](../storage-maintenance-2026-11-01.md).

## Disable / reproduce

Disable only this repository with the same command prefix and
`config set enabled=false`. Keep private state for inspection; no deletion or
global uninstall is needed. A different machine needs its own native plugin
installation and repository profile; committed documentation is not installation.

[Codex project plugin configuration](https://developers.openai.com/plugins/build/plugins#enable-or-disable-a-plugin-for-a-repo)
documents project overrides; native installation and hook approval remain
host-managed.

## Post-relocation check — 2 November 2026

The installed CLI's read-only `status` command, run against the canonical
`/Volumes/Work/Work/FramewrightStudio/repository` path, resolves the same
`framewright-921aae5102` profile by the origin remote. The enabled settings remain
unchanged. It reports zero observed sessions and zero effective tokens; the move
did not establish native activation or token savings. No setup or hook trust
changes were made in this check.
