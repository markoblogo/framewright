# Framewright0.6.0 — Recoverable production (REL-A)

Experimental prerelease; bounded operator-led production, not a stable autonomous studio.

Framewright can now recover a chosen final video with its exact checks and
limitations, and run an explicitly selected Eevee shot through the bounded local
executor. The production loop remains led by an operator, with manual film stages
recorded rather than presented as automatic execution.

## What changes

- **Recover the right final.** Selected delivery includes path, bytes, SHA256 and
  exact-version review receipts. Historical waits remain visible; new ready work
  keeps its priority. Provider and publication observations are shown separately.
- **Run a bounded Eevee shot.** Explicit Eevee Next/AUTO joins Cycles CPU with pinned
  inputs/settings/runtime, output checks and human review still pending. A retained
  Last Seed scene verifies repeat/light change, interruption and explicit retry.
- **Keep reuse honest.** Oversized montage titles/subtitles fail before a clipped
  caption is exported. Scoped PixVerse/Odyssey component use remains separate from
  structured feature coverage, current quotas/access and publication rights.
- **Retain production experience.** Good Dog and One Artist, Two Cities case records
  preserve accepted versions, failures, corrections and focused follow-up tests.

## Evidence

The complete local check ran510tests with18skips, plus retained benchmark integrity,
schema/link/matrix checks and a standalone-package smoke. A separate read-only
OpenAI reviewer approved the full scoped change in two rounds, independently ran
22tests and confirmed the engine-label nit fixed; eight affected tests passed again.
GitHub Codex review on1345590 completed without findings. PR48 and the exact merged
main commit5a98bd6 passed CI.

## Compatibility and limits

Unchanged projects need no data migration. Final selection is explicit and does
not delete waits or grant execution/publication authority. Changed saved-shot
implementation fingerprints require newly prepared/reviewed contracts; do not
repin old approvals to bypass drift checks.

Eevee qualification is a short480×270 scene test on one Blender4.5.15 ARM64 build,
not full-film/final-resolution or cross-platform qualification. Whole-film manual
steps remain manual. Current model routing is not newly evaluated. Media/account
terms, commercial use, human creative/listening acceptance and public uploads stay
separate. No models, private media, credentials or vendor binaries are bundled.

## Assets

- `framewright-router-0.6.0.zip` — standalone router skill and local helpers.
- `SHA256SUMS` — checksum for that ZIP.

The ZIP's optional case links target the v0.6.0 source tag. The canonical
[release page](https://github.com/markoblogo/framewright/releases/tag/v0.6.0)
retains publication state, source commit and downloadable assets.
