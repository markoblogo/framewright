# v0.6.0 REL-A experimental release audit

1November2026. **Pre-publication evidence frozen for the authorised release.**
The owner first requested preparation, then explicitly authorised release-branch
PR/CI, merge and publication of0.6.0. This source record captures readiness; actual
publication/tag/download proof must be checked against the canonical release
records below, rather than inferred from this text.

[Release notes](release-notes-0.6.0.md) · [REL-A matrix](release-readiness-2026-11-01.md)
· [independent review](independent-review-2026-11-01.md).

## Identity and baseline

Repository: markoblogo/framewright. Local candidate branch: release/0.6.0.
Source base: merged PR48, `5a98bd64a0f2f11940e088e4a69afb03f36060df`.
Reviewed head: `1345590d40d63328d089b15ed3f0117a887313b3`; merged tree matches it.
The latest published release observed at preparation is experimental v0.5.0.
Version0.6.0 is a minor experimental capability increment, not a stable1.0 claim.

[Exact merged-main CI](https://github.com/markoblogo/framewright/actions/runs/41289256681)
completed successfully on5a98bd6. Both PR48 runs and GitHub Codex review had
already passed. Candidate changes are version/README/changelog/release documents;
no renderer, routing or journal behavior changes are introduced in this step.

## Release verification matrix

| Domain | State | Evidence / boundary |
| --- | --- | --- |
| Repository/base identity | PROVEN | PR48 merged, reviewed and merged trees match; candidate is based on5a98bd6 |
| Baseline/diff | PROVEN | Main was clean; candidate changes are release metadata/docs only |
| Tests/build/package | PROVEN | Source CI/full local checks passed; candidate schema/link/matrix/package smoke, ZIP integrity and checksum passed. Full suite not repeated for metadata-only edits |
| Runtime evidence | PARTIAL | Recorded Last Seed short Eevee trial and fresh-agent Good Dog recovery; no arbitrary hardware/full-film guarantee |
| Public release/tag/assets | UNKNOWN | v0.6.0 is not published; prospective source links are not live evidence |
| Deployment/HTTP/SEO/browser/locale | N/A | This release is a Python/Markdown skill ZIP, not a deployed website or hardware product |
| Human gate | PROVEN | Owner authorised release PR/CI, merge and publication; actual publication remains unverified |

## Compatibility

No mandatory data migration. The additive final-selection command binds exact
retained versions; reviews/constraints remain distinct. Existing unchanged
workflows remain optional. Changes to pinned worker/adapter implementation require
new prepared/reviewed execution contracts. Native graphics access may be needed;
Eevee AUTO does not promise CPU-only execution or model/GPU fit.

## Publication and verification procedure

Commit/review the release metadata and run its CI under the already supplied
publication authority. The final changelog/date/badge are prepared in the release branch. Create the real tag from the verified commit, rebuild or verify matching assets,
publish as an experimental prerelease, then verify the public page/tag/downloads
and SHA256. Do not treat this local candidate or a temporary smoke as publication.

## Candidate package verification

`framewright-router-0.6.0.zip` built successfully from byte-verified inputs,
381204bytes/87entries. SHA256:
`92911ed69b5a10357de79ef50b20922d4f9d02a5a1f6f0f74ca2949a757ee668`.
`SHA256SUMS` matches; ZIP integrity and installed skill smoke pass. No private
media, models, caches or Git metadata are bundled. The source CI is green; only
version/release metadata changed, so the full suite was not repeated. Candidate
commit/CI, public tag, source links and downloadable assets remain unverified
until the publication workflow. Overall release-publication status: **PARTIAL**.

## Canonical publication evidence

[Release page](https://github.com/markoblogo/framewright/releases/tag/v0.6.0),
[source tag](https://github.com/markoblogo/framewright/tree/v0.6.0),
[ZIP](https://github.com/markoblogo/framewright/releases/download/v0.6.0/framewright-router-0.6.0.zip)
and [checksums](https://github.com/markoblogo/framewright/releases/download/v0.6.0/SHA256SUMS)
are the intended records. The publishing operator must verify the actual tag
commit, prerelease/non-draft state, HTTP availability and downloaded ZIP SHA256
after publication. Their presence as links in this pre-publication audit is not
proof that they were live when the source was committed.
