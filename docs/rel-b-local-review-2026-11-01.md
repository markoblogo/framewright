# REL-B local prerelease checks and review — 1 November 2026

**Local preparation passed.** No commit, push, PR, remote CI, version bump, tag or
release publication performed. Base/current HEAD:
`8696269e0d81c3a2b63b74feac6ea209c3544343` (0.6.0). The whole accumulated working
diff, including20 tracked/untracked files, was reviewed; private media and upstream
code remain outside Git. This is software/docs review, not independent media approval.

## DOC-ENTRY-01

README now leads with start / continue / correct; [the working guide](start-here.md)
links one path per task and [current status](next-cycle.md) separates active work,
waits and future plans. Prior detailed README and next-cycle were preserved under
`docs/history/` with relative links rebased and explicit historical banners.
AGENTS points to current entrypoints without loading histories. The old production-
guide anchor now targets current status.

Measured before/after: README258→102 lines,2456→633 whitespace-delimited words;
next-cycle400→48 lines,3920→405 words (including final status annotations). New on-demand start guide78lines/475words.
AGENTS remains12lines,148→162words. These are document counts, not token or
operator-time savings.

A separate agent started without chat history read the frozen scope and completed
all three navigation tasks: start→proposal/demo; continue→brief/blockers; correct
interval→revision request/A-B/exact-version review. It also located the actual next
step and retained SSI/AzurMenton waits.490 local Markdown links/heading targets
checked without missing targets. Internal cold-reader walkthrough, not independent
external-user adoption or a published onboarding trial.

## Checks

`python3 scripts/check.py` exited0:
-514 unittest tests in316.950s,18 reported skips; no claim that skipped paths passed.
- Existing router/storyboard grading artifacts validated. Some historical scores
  contain known failures; current-source model routing **not newly evaluated**.
- Structural validation:10methods,42outputs,17scenario specifications; local links intact.
- Generated tool reference matches registry.
- Standalone package smoke passed for temporary `framewright-router-0.6.0.zip`;
  SHA256 `bb38ed0cc0ebece134eeaaa10d9c8b36669f9e0dbf990ca2785407014758c51c`.
  This temporary test package is not a new release artifact or public upload.

`git diff --check` passed. Final reviewed file hashes matched the frozen snapshot.
No automatic model calls, installation, account action or publication in these checks.

## Independent review

One read-only reviewer `/root/relb_prerelease_review`, no chat history or nested
reviewers, default inherited model (exact model ID not independently surfaced).
Round1: **APPROVE**, blocker0 / should0 / nit0. No fixes or additional rounds needed.
Reviewed patch SHA256:
`093e8c0161d26be54bec6051740d7a46a0da482a8b97656aefe06b88c3e0b588`.
Private manifest and patch retain the20-file scope. Reviewer checked timing CLI/
guard/tests, status/permission distinctions, archives and the navigation walkthrough;
it did not run a second full suite, render or inspect private films/publications.

After that approval, only this evidence record and status/completion annotations
were added; behavioral source diff remains the independently reviewed version.
Final link/structural and diff checks are rerun for those annotations. No new
independent approval of the underlying films, SSI runtime or platform rights implied.

## Next boundary

[REL-B production readiness](rel-b-readiness-2026-11-01.md) plus this local review
supports proposing commit/push/PR for remote CI/review. Owner authorisation is still
required for that next task and for the later release decision. No new production
or whole experiment-queue sweep is needed. Pending private template-design review,
labour-savings evidence, whole-route autonomy, partner acceptance and platform
outcomes retain their explicit limits; none is silently promoted by software tests.
