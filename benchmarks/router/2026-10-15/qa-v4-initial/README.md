# Initial protocol-v4 regression — retained67/70

This is the first complete70-case run after the five transfer-2 corrections.
Last18 passed18/18. Strict full score67/70 is retained with no overrides:

- locked-score-frames: genuine omission of an explicit source-master preservation check;
- comparison-stop-v3 and blocked-plan-v3: INSUFFICIENT_EVIDENCE because the grader
  lacked decision-source text to verify catalogue claims. Successful read events
  alone were supplied without outputs; this is a grading-context gap.

This snapshot is not the current qualified source. A later source revision adds
locked-audio QA, and the accepted grading context includes frozen decision text.
See [complete correction record](../qa-v4-complete/README.md). Original13/18 stays unchanged.

The38-control calibration passed before these actors. One grader batch timed out
without any answer; the interrupted attempt is retained locally and recorded in
[grading-interruption.json](grading-interruption.json), then that unchanged batch
was evaluated again. No actor answer was retried on this source or discarded.

All raw actor answers, traces, model grades, source snapshot and hashes are retained.
No rendering, provider action, media publication or release occurred. This is known-case
regression evidence with gaps, not an unseen test or a causal quality score.
