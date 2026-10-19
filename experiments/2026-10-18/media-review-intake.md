# Operator recording intake and media-review routing

Owner requested actual listening/viewing routes and a helper to catch recording
problems before a full operator take. Implemented local technical rehearsal CLI;
added perception workflow and two untested candidates to arsenal discovery.
No personal voice cloud transfer, model download, paid API call, video render,
public upload or release in this pass.

## Real local probes

Two privately retained owner M4A files: 22.73 and 18.97 decoded seconds, mono 44.1kHz.
Their source peaks were -23.01 and -19.42 dBFS. Both flagged low input; neither had
samples at full scale. Whole-clip peaks do not prove speech loudness or noise quality.
Source copies/hash checks retained; local 48kHz/24-bit alternatives use 60Hz highpass,
fixed gain to -3dBFS sample peak and 15/25ms edge fades with identical sample lengths.
No internal edit, speed/pitch change or synthetic words. Not chosen or accepted.
Private reports and exact commands: current Jekyll project's owner-voice-20261018.

Existing Jekyll close-up clip: 8s, 1280x720, 24fps; calibration inspected metadata
and 16 resized luma samples. Sampled average 51.73; no full-video or sync verdict.
Original media unchanged; no new video generated.

## Perception limitation retained

The attempted assistant audio input returned: `audio content omitted because you
do not support audio input`. No listening, transcription or pronunciation verdict
was invented. Owner recording receipt is complete; listening/selection remains
pending. The current two takes can be previewed locally by the owner.

Gemini audio/video and Qwen3-Omni documentation reviewed; indexed as candidates,
not tested providers. Unknown evidence is deliberately excluded by tested and
default documented search filters. Native agent image viewing is a separate route.

## Checks and limits

Five calibration unit cases: quiet signal, clipping per channel without phase
cancellation, all-silence handling, explicit room/speech intervals, invalid/nonfinite
values. Real local two-audio/one-video probes above. Full offline gate log is kept
privately with the case; no fresh model benchmark or linguistic validation.
CLI success means measurement completed, not that a take is acceptable.

Validation outcome: 236 unit tests ran; one stale saved-search example failed after
adding two candidate IDs (exclusion count only). Regenerated that example and all
16 search tests passed. The other 235 tests passed in the full run, including the
five new calibration cases. Remaining offline integrity/link/registry checks and
temporary standalone package smoke passed; temporary ZIP removed, no release.
