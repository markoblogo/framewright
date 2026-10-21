# Gemini media-review free UI pilot

21 October 2026. **Attempted, not qualified.** One Gemini 3.8 Flash run in an
already-authenticated Google AI Studio session, with no paid API key selected,
no billing activation and no paid spend. This demonstrates access in that session,
not guaranteed future free quota or an automated API connection.

Eight frozen, original synthetic H.264/AAC clips were attached to one fresh prompt
without gold, generation source or prior conversation. Static video sampling was
set to 12 fps for all eight; agentic video mode, search and tools were off. One
failed Drive attachment was reuploaded before the sole generation request. The
UI reported 71,163 input tokens and 80,029 final tokens; these are interface counts,
not a raw API usage/billing receipt. Backend model snapshot was not exposed.

The returned JSON has eight rows and seven timestamped findings, but substitutes
`input_file_0` through `input_file_7` for the requested frozen source IDs. An exact
binding to the clips was not established. Several failed checks lack a finding in
the corresponding scope. The importer rejects the response; no ID inference,
semantic repair, TP/FP/FN calculation or accuracy percentage is retained. All rows
declare video-only input and leave listening/sync unknown, so this is not an
acoustic or AV-sync qualification.

The original rendered code-block answer, prompt, file hashes, settings record,
validation failure and screenshot remain private. No owner voice or production
media was sent. The source kit still has authored labels awaiting independent
per-label human validation; general owner approval of the kit is distinct.

A useful follow-up must change the protocol: one clip per fresh session with
caller-bound identity, then a separate check of actual audio availability. Do not
repeat this unchanged batch, repair its result into a pass, or promote the
candidate to a default production reviewer. The owner permits free use only;
any paid fallback requires new explicit authorization.

Sources checked: [video input](https://ai.google.dev/gemini-api/docs/video-understanding),
[model](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash),
[pricing](https://ai.google.dev/gemini-api/docs/pricing),
[quota](https://ai.google.dev/gemini-api/docs/rate-limits).
This is a scoped UI workflow result, not evidence that Gemini generally cannot
review video or that sampled video proves continuous perceptual acceptance.

## Follow-up: one attachment per fresh session

A separately authorized free follow-up changed the protocol: one freeze clip,
one audio-only WAV derivative and one clean video control in three fresh sessions.
No prior response, gold or source was supplied. Video settings remained static12fps;
search/tools were off and no paid key or billing was enabled. Paid spend remained$0.

The video response localized the authored hold at4.00–5.25s. The same prompt in the
clean-control session returned no findings. However, the explanation additionally
claimed the timeline kept moving during the hold: decoded timeline geometry stays
at the same264px edge at4.25 and4.75s, so that detail is unsupported. Matching a fault's
timing does not validate every explanatory assertion. Audio was explicitly not
accessed from either video's sampled frames.

The independent audio prompt gave no expected event types/count/times. The model
claimed female speech instead of the two authored880Hz tone bursts at2s and8s.
WAV bytes exposed by the provider's player exactly matched the uploaded derivative
SHA-256, ruling out a wrong UI attachment; hidden inference processing remains
unobserved. The acoustic smoke test failed. Its confident audio-availability claim
is not evidence of correct listening.

Caller-bound source identities and a findings-only response resolve the previous
contract failure without rewriting the old batch: original findings are preserved,
category scopes become failed checks, and all other checks stay unknown. This
mapping is retained explicitly. The scorer accepts this new response: one matched
authored finding, no extra findings in these two visual responses, five remaining
authored events unassessed. No overall accuracy or continuous acceptance is claimed.

Keep Gemini a candidate for further scoped visual controls, with human verification.
Do not qualify audio, speech, languages, AV sync, general video quality or unattended
acceptance. Three new generations and their raw rendered answers remain separate
from the rejected first batch; no paid fallback is authorized.
