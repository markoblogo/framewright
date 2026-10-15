# Capture incident hypotheses, before implementation
1. Abandoned login-shell commands: predict all eight gaps use zsh -lc, while fallback -c finishes. Probe retained raw streams and paired timed shell reads. Result: all eight match; timing probe pending. Status: strongest correlation, startup cause unproven.
2. Parent collector drops output: predict malformed/truncated JSON or missing final event. Probe parse every retained stream, check terminal turn. Result: pending. Status: open.
3. CLI lifecycle lacks completion for still-running child: predict syntactically complete stream, started command, final turn but no terminal command. Probe raw event accounting and tiny fresh no-login CLI runs. Result: observed on eight streams. Status: confirmed symptom, upstream cause not yet proven.
4. Grading handoff trusts exit/turn only: predict records() accepts incomplete stream. Probe synthetic missing-completion fixture. Result: source confirms no command-completeness guard. Status: confirmed application defect.

## Final results
1. Login-shell contribution: reproduced. pwd -c 0.1 s versus -lc timeout8 s; eight exact abandoned reads completed under -c. Local startup hook untraced.
2. Truncated parent output: rejected for these eight cases; zero malformed lines and terminal turn in each original stream. Silent malformed-line handling remains a separately reproduced collector defect and is removed.
3. Abandoned child lifecycle: confirmed original symptom; all34 started calls in eight new no-login actors have matching terminal events. Upstream internals remain unproven.
4. Missing handoff guard: reproduced with a failing unit test, then fixed. Incomplete capture cannot enter grading.
