# Studio storage sanitation — 1–2 November 2026

Owner-authorized cleanup of Framewright production material and trial software.
The cleanup itself performed no commit, push, release, publication, generation
or model-download cancellation. Subsequent documentation closeout is a separate PR.

## Completed relocation

- 60 owned top-level entries were renamed into the external studio without copying
  their data. Repository and portable-tool paths retain two compatibility links.
- The legacy chat workspace,29 inactive preview-history caches, Whisper weights and
  a small release snapshot were moved with per-file SHA-256/size verification
  before removing each internal original: about11.19GiB,27266 receipt entries.
- The internal Codex workspace is a real entry directory with98 child shortcuts
  and only two short text files (1167bytes at inspection). Codex rejected a
  symlinked writable root; no sandbox setting was weakened. Media remains external.
- Six accepted masters were independently rehashed after relocation and matched
  their transfer receipts: Good Dog, The Last Seed, AzurMenton, Exin v2 and both
  Beyond the Letters aspects. The REL-B working brief loads from the migrated
  project and reports its selected accepted version with no current file problems.

Canonical home: `/Volumes/Work/Work/FramewrightStudio`; see its private README.
`repository/`, `productions/`, `workspace/`, `tools/` and `records/` separate code,
productions, legacy session material, retained tools and evidence. The move map
resolves older volume-root paths; historical references are not availability claims.

## Retired material and software

10703 listed draft/render/review files (about4.83GiB of logical file lengths)
were deleted, preserving selected masters and provider originals. A separate
temporary extraction cache of2527 files, including2514 generated JPEGs, was
deleted. Repeated embedded runtimes and old test fixtures were separately listed
for deletion with explicit owner approval; per-target outcomes are in the log.

Android Studio, GLEA and DJV were uninstalled; obsolete Chromium146/148 copies and
downloaded installers were removed. Blender and Kdenlive remain on external Work.
Prior trial results stay historical; reinstall removed tools only for a selected
experiment. Shared Codex state, browser profiles, other projects, personal/book
archives and the active external AI model download were not cleanup targets.

## Availability and filesystem exceptions

`Kazan-A-Roof-Rewritten.mp4` was absent from the initial inventory and its delivery
directory before this cleanup; no deletion of that final was performed here.
The owner also reported deleting older videos including Mobius before the audit.
Do not report those absent masters as retained or fetch/recreate them silently.

One old Torch environment initially resisted deletion: directory entries were
listed but returned ENOENT on `lstat` and direct `unlink`; recursive deletion
returned “Directory not empty”. Its residue was isolated under
`scratch/delete-pending-filesystem-check`. This observation does not establish
the cause or whole-volume health. No volume repair, unmount or formatting was
attempted while the model download was active. Any further residues are listed
in the private unresolved-cleanup record; review the volume later, separately.

During the final runtime purge Work briefly returned `Device not configured`;
the owner then confirmed reconnecting the disk. Cleanup was stopped until the
mount was readable again. All six selected masters were rehashed a second time
after reconnection and still matched. This interruption was not diagnosed as
hardware failure. A mount guard prevents creating an internal fallback tree.

Historical source/frame and review copies were deliberately retired under the
approved retention plan. Their notes/recipes remain, but this is not a claim that
every old film can still be rebuilt from its original frame sources unchanged.

## Evidence and operating rule

Private `records/storage-2026-11-01/` retains exact move/deletion plans, file
inventory, per-file transfer receipts, selected-master hashes, exception details
and action history. Transfer checks establish bytes at transfer time; intentional
later edits to instructions/maintenance metadata are not media changes.

[Storage policy](storage-policy.md) is linked from README and AGENTS.md. Keep one
accepted master per requested deliverable, selected publication assets, the final
recipe and necessary sources. Retire intermediates after acceptance; perform
sanitation after production, before releases/large downloads, and weekly during
active work. This adds a work-loop rule, not blind scheduled deletion.

Structural documentation validation passes; it does not assert that every retired
historical media file remains present. External cleanup completion and the final
space snapshot are recorded in the private summary after the last operation.

## Completion snapshot — 2 November 2026

The sequential purge finished successfully. All 35 approved cache source paths
and the legacy temporary test tree are absent. One environment residue remains
isolated in `scratch/delete-pending-filesystem-check`; it is not counted as
fully deleted. No cleanup worker is left running.

The internal compatibility entry now contains only two text files (1,167 bytes)
and 98 external shortcuts. At completion, available space was approximately
21.9 GiB internally and 252.5 GiB on Work; these are time-specific snapshots.
The post-reconnection checkpoint and final summary are retained with the private
records. No commit, push or release was performed during cleanup; its subsequent
documentation closeout does not authorize a new release.
