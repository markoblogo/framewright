# Framewright0.7.0 — Repeat production and reuse (REL-B)

Experimental prerelease. Reuse a production approach while retaining exact-version
review, known failures and honest measurements. This is an operator-led methods/
skills library, not an autonomous hosted video studio.

## What changes

- **Find the right starting point.** README now leads to start / continue / correct,
  with compact current priorities. Older detailed entries remain as linked history.
- **Check time as well as geometry.** The source montage example offers an English
  caption-time CLI and opt-in render guard. Title/subtitle share the budget; short
  scenes fail before output/media access. It never silently stretches accepted
  content or assumes narration remains aligned after timing changes.
- **Carry reuse through a real repeat.** Beyond the Letters reuses retained sources,
  assembler, score and voice recipe, with a new script/cut/voice. Both36s formats
  are owner-accepted internal tests. The audio-only correction preserves picture
  packets; fresh-agent continuation recovers the next step without regeneration.
- **Qualify specific operations.** Pinned ffmpeg-skill explicit midscene frames
  match direct FFmpeg on another film. Its automatic sheet repeats failure and is
  excluded. SSI v2.1 and the AzurMenton guide retain separate receiving-project,
  approval and publication evidence. Channel/book automation remains a staged plan.

## Evidence

Local `scripts/check.py`:514tests,18skips; schema/link/tool-reference checks and
standalone package smoke pass. One independent read-only reviewer approved the
behavior diff and navigated all three entrypoints. GitHub Codex review on5a00706
completed without findings; PR50 and exact merged-main CI onff84b1d pass.
[Detailed local record](rel-b-local-review-2026-11-01.md) ·
[REL-B matrix](rel-b-readiness-2026-11-01.md).

Reading-time assumptions are2.5words/s,15nonspace characters/s, minimum2s plus0.4s
for transitions, rounded to frames. A particular long-copy control moved3→9.75s;
that is a heuristic check, not a reader study. New voice timing/layout and human
creative/listening approval remain independent. Accepted masters are unchanged.

## Compatibility and limits

No mandatory project migration or new runtime dependency. Existing montage calls
keep their behavior; `--enforce-caption-timing` is explicitly opt-in. Unknown
operator labour and baseline effort remain unknown; scripted stage durations are
not a savings percentage or full turnaround quote. Whole-route admission, paid
providers, arbitrary platforms and automatic social publishing are not qualified.
Historical model-evaluation gaps remain; no fresh model calls in this release.

## Assets and source examples

- `framewright-router-0.7.0.zip`: standalone router skill and its local helpers.
- `SHA256SUMS`: checksum for that ZIP.

The montage example and its new timing script live in the source repository's
`examples/production-reuse/`, not inside the standalone router ZIP. Optional package
case/example links point to the v0.7.0 source tag. Private media, model weights,
credentials and copied provider code are excluded.

[Canonical release](https://github.com/markoblogo/framewright/releases/tag/v0.7.0)
records actual publication, tag and downloadable assets; prepared source links do
not by themselves prove availability. [Publication audit](release-audit-0.7.0.md).
