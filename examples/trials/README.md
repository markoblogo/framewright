# Text-only experiment-workbench example

Run from the repository:

```sh
python3 examples/trials/run_demo.py --output /tmp/framewright-trial-demo
```

Choose a new folder; no overwrite. This creates a project and original text files,
one deliberately failing baseline, one passing candidate, source/evidence pins,
a local prerequisites report and `comparison/review.html` plus JSON/Markdown.
It invokes neither media software nor a model/provider. Timings measure fixture
file operations only. No owner acceptance or catalogue promotion is made.

Expected status: `ready_for_owner_review`, `eligible_for_manual_scoped_update: false`.
Edit a copied artifact to observe stale evidence; retain a new attempt instead of
rewriting history. For a real media experiment use existing cleared outputs and
actual per-criterion evidence; do not substitute these text checks for media QA.

[Complete contract](../../skills/video-production-router/references/trials-and-readiness.md).
