# EmbeddingGemma 2 · tool retrieval on a 12-card fixture

24 November 2026. One text-only local trial derived from the earlier
[illustrative media search](../productions/media-semantic-search.md).
Reference selected before ranking: Inworld Voice Isolator, the owner’s
preferred sample in the earlier
[controlled listening comparison](inworld-voice-isolation-2026-11-23.md).
This is a reference for the fixture, with no new denoising evidence.

Twelve authored tool cards, two paraphrases of the same offline Mac
dialogue cleanup task. EmbeddingGemma 2 (Unsloth UD-Q4_K_XL) ran locally with
llama.cpp b12675. The existing b7030 binary rejected the architecture.
Cosine ranking placed the reference first in both runs, satisfying the
predeclared top-three criterion. MLX Whisper also appeared in both
shortlists. It provides transcription rather than a cleaned audio stream.

| Query | Top three in order |
| --- | --- |
| Remove steady background hiss from dialogue | Inworld, Audacity Noise Reduction, MLX Whisper |
| Keep the talk clear and tame the fan | Inworld, MLX Whisper, FFmpeg afftdn |

Full card JSON was 3,213 B. Names and summaries for all 12 tools plus one
deferred parameter set occupied 1,823 B. These are exact local byte
counts for the fixture, independent of ranking. Gemini API requests,
token use, field performance and other tasks were not tested.

Retained private fixture, results and exact runtime/model receipts are under
`productions/tool-retrieval-shortlist-2026-11-24/full/`.
