# Inworld Voice Isolator on one controlled speech clip

**INWORLD-ISOLATE-01 · 23 November 2026.** Offline Inworld Voice Isolator 1.0.0
and its checksum-pinned 48 kHz mono v1 checkpoint ran locally on an Apple
Silicon Mac. The 24-second input mixed existing dry Framewright narration with
an original sound bed and controlled added noise. The dry stem was retained
for timing and level checks. This fixture does not represent a field recording.

All three clips used the same source and length. Speech-active RMS matched
to within 0.1 dB, and all three WAVs decoded. The light FFmpeg control used a
65 Hz high-pass and adaptive FFT noise reduction. The method key was held
outside the listening page until the owner rated the anonymous files.

| Blind sample | Method | Owner report |
| --- | --- | --- |
| A | Inworld offline on Metal | Cleanest |
| B | FFmpeg high-pass and afftdn | Somewhat dirty |
| C | Unprocessed mixture | Poor |

Metal completed in about 105 seconds with cached weights, including 83 seconds
reported by the CLI for processing. The parallel CPU attempt was stopped at
6:59 after Metal succeeded, so it has no completed timing. No speech was sent
to an external processor. Local compute and active labour were not priced.

Retain Inworld as a candidate backup for this kind of noise cleanup. Compare
again on an owned real recording before using it by default. Naturalness by
language, room reverberation, competing speakers, and streaming remain
untested. [Inworld repository](https://github.com/inworld-ai/voice-isolator).
