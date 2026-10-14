# Compose tools around the requested result

Use one main renderer and add a complementary tool when it closes a concrete gap:
missing audio, subtitles, thumbnail, format conversion or another requested output.
Keep the chosen renderer when its core job works. Do not install a second tool
when the existing chain already delivers the brief. Explicit user tool choices
remain binding; explain any necessary substitution before abandoning that choice.

## Handoff contract

1. Identify the unmet requirement and check the installed version's documentation.
   Distinguish an absent feature, a failed command and a feature merely untested here.
2. Choose the smallest available complement. Check input/output compatibility,
   duration, frame rate, dimensions, timestamps, audio sample rate and asset rights
   as relevant to that handoff. Preserve the original export and write a new output.
3. Keep narration, captions and cues on the same measured timeline. When only adding
   audio or extracting a still, preserve the video stream when the container allows;
   otherwise record re-encoding and inspect its effect. A voice from another tool
   still needs pronunciation, timing, intelligibility and final-mix checks.
4. Validate the assembled artifact, not just the separate tools: inspect encoded
   picture and sound, sync, duration and requested delivery format. Record failures
   and unresolved checks. A companion cannot make inaccurate simulation or missing
   source evidence valid; revise the effect or report the unmet requirement.
5. Stop once the authorised deliverables and QA are complete. Existing permission
   covers ordinary local processing for the brief, but not new paid calls, account
   grants, private uploads or public publishing. Do not weaken QA to force a pass.

## Retained combinations and boundaries

| Requirement / observed gap | Chain | Evidence and remaining limits |
| --- | --- | --- |
| CoqPi cinematic React UI plus music | Flute export → FFmpeg audio mux | Verified 23s/1080p30; original local instrumental added, encoded video stream hash unchanged. Flute's audio capabilities beyond this silent export were not evaluated. |
| Thumbnail after portable-host snapshot command failed | Encoded Flute MP4 → FFmpeg frame extraction | Verified thumbnail from the actual output. The failed snapshot command remains failed; no claim of fixing upstream Flute. |
| French/English voiced book imagery | Hyperframes montage + local Kokoro + sound-layer mixing/QA | Existing narrated book-trailer evidence; speech duration and encoded audio checks apply. |
| Voice or subtitles on a future Flute scene | Flute + a suitable speech/caption tool | Candidate combination only. Kokoro worked for the book route; that does not establish a tested Flute narration or subtitle chain. |
| Anatomy scene with failed sound QA | Anatomy + sound-layer prototype | Recorded failure. Additional tools do not turn this chain into a validated finished workflow. |

Keep the method catalogue scoped to demonstrated capabilities. For each new chain,
record the gap, tool roles/versions, artifact handoff, transformations, final QA and
retained output hashes in the experiment record. No new render or model evaluation
is required merely to document these rules.
