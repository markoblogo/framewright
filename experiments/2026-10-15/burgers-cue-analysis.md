# Burgers, Lipstick & Underwear — narrated 15s promo and cue analysis

2026-10-15. Owner requested the [agreed plan](../../docs/experiments/burgers-cue-analysis-plan.md),
English narration, an MP4, YouTube thumbnail/copy, local retention and documentation.
No new release. Owner-provided publication URL: [watch on YouTube](https://youtu.be/GVrbTMZxbpg).
Recorded2026-10-15; public playback was not independently verified.

## Result and tool roles

- Hyperframes0.8.161 (Apache-2.0): five artwork/typography scenes, native H.264/AAC
  export,1920×1080,30fps,450frames,exactly15.000s. Render54.6s, screenshot/hardware GPU.
- Existing local Kokoro ONNX code (MIT; Kokoro82M model Apache-2.0): am_michael,
  en-us,speed1.03,10.88s total speech. Fitted phrases on the timeline without audio
  retiming. The owner subsequently rated the English narration positively.
- Original deterministic bass/keys/percussion score, no sampled recording or paid
  music provider. FFmpeg owns the voice/music mix; no audio claim about cloud music.
- librosa1.0.0 (ISC): music-stem onset/beat candidates. PySceneDetect0.7.2
  (BSD-3-Clause) with OpenCV5.0.0.93: cuts from the final encoded MP4.
  [Reusable analysis example](../../examples/cue-analysis/README.md).

Upstream: [librosa onset API](https://librosa.org/doc/1.0.0/api/generated/librosa.onset.onset_detect.html),
[PySceneDetect detectors](https://www.scenedetect.com/docs/latest/api/detectors.html),
[Kokoro ONNX](https://github.com/thewh1teagle/kokoro-onnx),
[Kokoro model card](https://huggingface.co/hexgrad/Kokoro-82M),
[Hyperframes](https://github.com/heygen-com/hyperframes).
Installed package versions and the [dependency lock](evidence/burgers-analysis-requirements.lock)
are retained; this is version evidence, not legal clearance for arbitrary models/assets.

## Inputs, copy and planned criteria

[Official book page](https://abvx.xyz/books/burgers-lipstick-underwear), locally saved
page, owner-supplied promo and matching higher-resolution site image. The title,
subtitle and everyday economic-indicator theme were compared with that source.
No invented quotes, sales, forecasts or investment claims. The flattened promo was
reframed, not converted into real3D objects. Local macOS fonts were used for the
render; fonts, book images, model files and masters are not redistributed in Git.

Before detection, freeze [reference markers/parameters](evidence/burgers-cue-reference.json):
three musical accents at6,9,12s (at least2/3 within100ms), three target hard cuts
within one30fps frame. All four expected cuts3,6,9,12s are also retained. At most
one labelled adjustment was allowed; none was used.

**Reference limitation:** timing comes from the authored score and cut schedule,
not independent manual listening annotation. Encoded boundary frames were inspected,
but an independent listener has not labelled the track. This departs from the
plan's intended ear-annotated reference; results qualify only authored-marker
recovery, not general musical judgement or human perception.

| Check | Observed result |
| --- | --- |
| librosa target onsets |3/3; absolute errors13.97,9.34,16.33ms |
| PySceneDetect hard cuts |4/4 at exact frames90,180,270,360; no extra cut |
| Cut precision / recall on these four labels |1.0 /1.0; tiny authored sample only |
| All-onset precision |Not estimable from sparse accent labels; other legitimate attacks are not false positives |
| Beat/tempo estimate |120.185BPM versus authored120BPM; exploratory, no downbeat claim |
| Analysis wall time |50.484s cold run, including analysis/JIT; no comparative speed claim |

## Final-file QA and handoff

[Media evidence](evidence/burgers-media-qa.json): complete decode without errors,
H.2641080p30/450frames, AAC48kHz stereo,15s per stream,−17.36LUFS and−1.48dBTP.
Decoded mix correlation0.99965, zero lag over720,000 common samples;896 trailing
samples are retained codec padding beyond declared presentation duration. Stereo
channel correlation0.99981 and mono RMS ratio0.99995 show no unexpected cancellation
for this predominantly centred mix. These metrics are not listening or lyric QA.
Five midpoint frames, both sides of four encoded cuts and final frame were inspected.
Hyperframes check passed:0errors,26/26 contrast checks;7 structural/editor warnings
remain (monolithic scene/timeline organization, not media failures).

The YouTube PNG is an **extracted encoded frame at13.5s**, scaled to1280×720;
it is not a native snapshot test. Full/reduced layout, title, crop and file size
were inspected separately. JPEG is also retained locally. Final video/PNG hashes
and sizes are in [outputs](outputs.json); [literal QA markers](evidence/burgers-cue-analysis.txt),
[comparison](evidence/burgers-cue-comparison.json), [cue sheet](evidence/burgers-cue-sheet.json),
[cuts CSV](evidence/burgers-cuts.csv). The public helper reproduced identical
markers/matches on the same inputs; [replay provenance](evidence/burgers-helper-replay.json)
is an integration check, not independent media evidence.

Workspace: `/Volumes/Work/burgers-video-pilot-20261015`. Deliverables: MP4, PNG/JPEG,
`YouTube-EN.txt` and English SRT. The owner supplied the YouTube URL above; the
agent did not upload the media. Audience results remain unmeasured. No new release.

## Owner assessment after viewing

The owner rated the narration as good. The picture was acceptable but very basic,
not particularly engaging, and similar to trailers already produced. The clip is
usable with reservations; it does not demonstrate a meaningful creative improvement.
Detector results remain a technical capability result, separate from visual appeal.
This feedback is not independent landmark annotation or an audience study.

## Setup failures and budget boundary

Old `scenedetect[opencv]` did not install a decoder; installed/pinned OpenCV explicitly.
Hyperframes' updater attempted global skill writes and was denied; the official
workflow guide was fetched to Work and read. Initial missing mix dependencies and
an invalid loudness option were corrected before the sole delivery render.
The old failed commands/logs remain local; they are not analysis passes.

Analysis setup observed420MiB environment +541MiB download cache (~1.01decimalGB):
slightly over the proposed1GB cap before measurement. Task download cache was then
cleaned (521.1MiB removed), with no additional model download. Do not report that
all original budget/reference criteria passed. The main30-package install reported
4.54s resolution,74s preparation,26.49s installation; whole setup wall time and
actual account billing were not captured. There were no paid provider calls.

This adds a narrowly demonstrated **post-export analysis pair**. It does not promote
routing behaviour, dense alignment, fades, arbitrary music or general beat-based
editing. No full model benchmark was needed for this production experiment.
