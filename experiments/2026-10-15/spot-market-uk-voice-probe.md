# Ukrainian spot-market book — Supertonic3 voice microprobe

Owner selected [the Ukrainian spot-market guide](https://abvx.xyz/books/spot-market-handbook-ua-free-edition)
and requested a different Ukrainian speech tool after weak Piper/Tetiana results.
Scope:short audio first;the book film is conditional on owner voice acceptance.
No picture render,full narration,new release or public media upload.

## Predeclared test

Local acceptance-before-probe.json was retained before installation/generation.
Two stock voices,M1/F1,same Ukrainian text and settings;maximum two generations,
30seconds per voice,500MB model download cap,1.2GB new setup target. No cloning,
cloud API,purchases or account actions. Full model/config/style hashes checked
before local synthesis;auto_download=False and HF_HUB_OFFLINE=1.

> Чому ціна на зерно різна навіть в один день? Базис поставки, якість і логістика формують ціну фізичного ринку. Розберімося, як працює спотовий ринок.

The source page supports physical agricultural spot markets,basis,quality/location,
logistics/pricing and Ukrainian/free PDF/EPUB context. The probe introduces no
market quotations,returns or invented product capability. The two owner images
were copied unchanged;not used to produce any video. Their hashes are retained.
This differs from the previous Tetiana script,so it is not a controlled direct
engine-quality comparison. M1/F1 do share the same text/settings.

## Exact tool and rights

[Supertonic3 model](https://huggingface.co/Supertone/supertonic-3),revision
`3cadd1ee6394adea1bd021217a0e650ede09a323`,declares Ukrainian31-language support.
[SDK](https://github.com/supertone-oss-archive/supertonic-py)1.3.1,Python3.12.13,
local ONNX CPU;SDKMIT,weightsBigScienceOpenRAIL-M. The source SDK repository now
resolves to an archive;hosted support/service continuity is not implied.
[Exact model/config/style hashes](evidence/supertonic3-model-files.json) and
[installed dependency lock](evidence/supertonic3-voice-requirements.lock).

Model licence output/use restrictions include an explicit machine-generated-content
disclosure. These files are labelled AI-generated;future public promo must retain
appropriate disclosure. No copied engine,model/style weights,art or audio in Git.
No voice identity impersonation or cloning. Rights status is separate from quality.

[OmniVoice](https://huggingface.co/k2-fsa/OmniVoice) was reviewed,not downloaded or
run:codeApache2.0 does not override the pretrained weights'CC-BY-NC restriction.
[MLX4bit card](https://huggingface.co/mlx-community/OmniVoice-4bit) follows upstream
licensing. Deferred for this promotional use without separate permission;not a
claim of technical failure. No unchanged Piper voice retest.

## Observed results and limits

Both raw stock-voice clips are12.190476s,mono44.1kHz PCM16. M1 generation20.067s,
F1 generation15.792s after model load12.565s;one run,not a performance comparison.
No clipped samples or non-finite values. Raw sample peaks:M1−6.19dBFS,F1−9.74dBFS.
Listening copies use FFmpeg loudnorm−18LUFS/TP−2 target,with original duration,
no cuts,silence removal or retiming. Complete decoded listening copies had0errors.
[Raw/listening filenames,hashes,size,settings,pause intervals](evidence/supertonic3-uk-probe.json).
Silence detection at−40dB/150ms is descriptive,not a stress/intonation judge.

Approximately123MiB voice environment,408MiB model directory and131MiB task cache
in the retained directory snapshot;not exact peak storage/RAM or shared-block
accounting. Downloads stayed within500MB cap. ONNXRuntime emitted a device-ID
cache/telemetry warning before the telemetry-disable call;network traffic was not
independently audited. No third-party voice service was called.

**At-probe owner listening was pending:**pauses,word stress,question/declarative intonation,
clarity of зерно/базис/поставки/логістика/фізичного/спотовий. No naturalness or
production qualification inferred from technical WAV success. At that stage this candidate was in the decision ledger,not an automatically
eligible router profile;the owner review and subsequent authorisation follow. Existing Piper quality
warnings and default-selection exclusion remain unchanged.

## Later owner review and next step

{
  "source": "owner conversation2026-10-15",
  "overall": "usable,recommended among tools tested for Ukrainian",
  "pauses": "still present,but much less frequent and shorter than previous voice",
  "stress": "about2–3 errors over the short speech;male seemed to have one more error",
  "intonation": "good",
  "voices": "M1/F1 very close;slight preference for F1,not a measured score",
  "limits": "One owner assessment of one23-word script;not general Ukrainian quality or long-form qualification",
  "decision": "Supertonic3 primary Ukrainian option;Piper/Tetiana low-quality explicit fallback"
}

Owner explicitly authorised the next book film using this engine. F1 is the
production default;M1 is also acceptable. Piper remains low-quality explicit
fallback,not a silent automatic substitution. Full-film QA is a separate trial.

[Subsequent full LCD film](spot-market-uk-lcd.md) completed technical QA with F1;
final-film owner listening remains separate from the accepted microprobe.
