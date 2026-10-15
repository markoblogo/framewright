# MN7R Product Guide — ManimGX + MLX-Audio

2026-10-15. Owner selected the [English free guide](https://abvx.xyz/books/mn7r-product-guide)
and supplied its cover; English narration was explicitly confirmed. First paired
picture/audio-tool experiment in the proposed [five-book series plan](../../docs/experiments/agro-series-plan.md).
No public media upload or release. Owner listening/creative review remains pending.

## Question, input and predeclared checks

Can ManimGX produce a readable workflow promo and MLX-Audio its English voice?
[Pre-render criteria](evidence/mn7r-acceptance.json):20s1920×1080/30fps,scattered
cards becoming a workflow,roles/AI reveal,genuine cover and free-English CTA,
separate stems/picture master,encoded QA and independent thumbnail inspection.

The official page was fetched and retained after the web reader failed. It describes
a living public guide to brokerage workflow,execution,role model,AI-assisted
operating support and public-safe demo surfaces;free PDF/EPUB. Copy was compared
with that source. Diagrams are illustrative,not genuine UI or private data. No
invented prices,counts,results or capabilities;the cover remains owner-supplied art.

| Time | Picture / narration |
| --- | --- |
|0–3s | Compass and brokerage hook |
|3–8s | Clients/offers/deals/execution cards align and connect; moving signal |
|8–12s | Brokerage role model |
|12–15s | Operating discipline and AI support |
|15–20s | Genuine cover,title and free English PDF/EPUB CTA |

## Results and component roles

- **ManimGX 0.1.1**,Python3.14.5: authored2D vector/workflow motion and image import.
  Native render reported10.6s;native layout passed21samples after enlarging a17px
  footer. These timings exclude unmeasured cold setup/import. Native3D,math plots,
  arbitrary data bindings and native still were not exercised.
- **MLX-Audio 0.5.9**,Python3.12.13: Kokoro 82M MLX weights327115152bytes,
  `am_michael`,language`a`/English,speed1.03. Five phrases,total18.15s speech,last
  ends19.525s,without retiming. The first phrase took68.649s including pipeline
  initialisation;later0.966–1.618s. Not a fair speed comparison with the prior ONNX
  engine. This is the same voice family under a new runtime,not a new voice/model
  quality claim. [Timing](evidence/mn7r-voice-timing.json). Ukrainian untested here.
- **FFmpeg**: preserves native VFR timing while normalising to CFR30,then mixes
  local voice with original synthesized music/effects and creates AAC master.
  No cloud music,stock recording,paid API or voice cloning.

## Native timing limitation and workaround

[Native probe](evidence/mn7r-native-probe.json):409 frames across20.033333s. Static
waits are retained as held-frame duration;fewer frames alone are not loss. PTS is
monotonic;final17s image has3.033333s duration. Direct stream-copy mux emitted
`Invalid DTS` / `Invalid timestamps`. Do not treat CLI success as proof of compatible
native timestamps. The initially copied final is discarded,not a delivery pass.

Explicit FFmpeg`fps=30,setpts=PTS-STARTPTS`,600 frames and H264 re-encoding produced
600 frames/exactly20s with correct observed stages/closing hold. No source scene or
voice was regenerated for the fix. A discarded normalization command combined`-r`
and passthrough;its error is retained. Do not use`N/(30*TB)` to compress VFR holds.
Original VFR,normalized silent picture and final voiced MP4 remain separately local;
[outputs](outputs.json) hash the final,native original and PNG independently.

## Encoded QA and handoff

[Media QA](evidence/mn7r-media-qa.json): H2641080p30/600 frames/20s,AAC48kHz stereo20s,
full decode0errors,−17.81LUFS,−1.51dBTP,mix correlation0.999933 and zero lag over
960000common samples.512trailing decoded samples are codec padding. These are
technical checks,not listening. Native21sample storyboard,six encoded stage/action
samples and full/contact-sheet1280×720thumbnail layout were inspected. PNG is
extracted at18.5s,not native still. [Literal evidence](evidence/mn7r-manim-mlx.txt).

Local folder`mn7r-guide-video-pilot-20261015` contains final MP4,native/normalized
picture masters,English YouTube title/description/tags,SRT,voice/music/effects/WAV
mix,source/model hashes,requirements,original source and logs. Diagram labels/copy
are baked into the picture master;the editable scene permits later text changes.
No textless-master or automatic series compilation is claimed.

## Setup/resource failures — retained,not retried blindly

Missing soundfile was our WAV-writer setup error. A local`kokoro82m`directory caused
model-type inference failure;renaming it to`Kokoro-82M-bf16`resolved it without a
model redownload. Misaki's automatic spaCy-model install failed to detect the venv;
installed official`en_core_web_sm3.8.0`explicitly in the audio venv. Old attempts and
deprecation warning remain in local logs. Reuse the prepared environment.

The small 327MB neural model still pulled a much larger NLP/ML runtime. One directory
snapshot summed approximately 3.2GB including two environments,model and download
cache;the planned 2GB setup cap was exceeded. This is not exact peak or shared-clone
accounting. Task-only uv cleanup removed 29334files/1.2GiB,retaining runtimes/model.
Audio venv alone was roughly1.2GB. Do not report all original acceptance gates passed.
The machine has 16GB RAM;working media and packages are on external Work.

## Sources and scope

[ManimGX](https://github.com/academa-labs/manimgx) code MIT;bundled fonts,FFmpeg and
x264 retain separate notices. [MLX-Audio](https://github.com/Blaizzy/mlx-audio) MIT;
[Kokoro MLX model card](https://huggingface.co/mlx-community/Kokoro-82M-bf16) declares
Apache-2.0;NLP dependencies retain their own terms. Package pins:
[visual](evidence/mn7r-visual-requirements.lock),[audio](evidence/mn7r-audio-requirements.lock).
Book art,packages,weights and rendered media are not distributed in Git.
[Authored source](../../examples/manimgx-mn7r/README.md). New profiles qualify this
adapter/English scope only;old router model scores remain historical. No release.

## Later owner feedback / publication

Owner found the result basic but good/acceptable,with its own infographic style.
[Owner-supplied YouTube URL](https://youtu.be/TISOtCghMVY). No byte matching or
audience measurement;no separate pronunciation assessment was supplied. Original
at-run pending QA statuses remain historical.
