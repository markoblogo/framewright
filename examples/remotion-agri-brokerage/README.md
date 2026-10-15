# Agri-Commodity Brokerage — archived 3D trading-table source

Author-specific30s1920x1080p30 example:Three.js0.186.0 + Remotion4.0.535,
React19.2.3,Supertonic3F1 English with a voice-only final soundtrack. Original
book art,voice/music weights and media are not redistributed. Put authorised
book cover at `public/cover.jpeg`;review every claim and crop. For an installable
open-asset starter see [first video](../../docs/first-video.md).

This pilot reused the existing qualified Remotion runtime with an isolated writable
cache;no complete tested transitive lock was retained. No clean-install command
or byte-identical reproduction is claimed. Inspect Remotion Free/Company licence
eligibility. Commands below assume that runtime is already available locally;
do not substitute an automatically fetched CLI version.

```sh
set -e
REMOTION_BROWSER='/absolute/path/to/tested/chrome-headless-shell-152'
./node_modules/.bin/remotion still src/index.tsx Thumbnail Agri-Brokerage-YouTube.png --browser-executable="$REMOTION_BROWSER" --gl=angle --timeout=120000
./node_modules/.bin/remotion render src/index.tsx Brokerage Agri-Brokerage-Picture-1080p.mp4 --codec=h264 --crf=18 --concurrency=1 --browser-executable="$REMOTION_BROWSER" --gl=angle --timeout=120000
```

## Narrated assembly

Use the recorded Python3.12/Supertonic1.3.1 voice environment. The sibling
Contract Execution helper verifies this example's committed model/config/style
manifest. Set `SUPERTONIC_SOURCE_ROOT` to the verified workspace containing
`models/Supertonic-3`;external manifests cannot redefine the pin. All four lines
are regenerated. Full metadata is published only on completion;assembly checks
expected lines,WAV hashes,clipping and timing. SDKMIT;weightsBigScienceOpenRAIL-M,
including explicit AI-content disclosure. No cloned voice.

The owner selected narration without music after the separate ACE-Step attempts
remained incomplete. The [experiment](../../experiments/2026-10-15/agri-brokerage-ace-step.md)
retains the integrity failure/retry,system interruption and CPU resource-guard stop.
No ACE-Step music or fabricated silent music stem is included in this final output.
`audio-build.py` creates only the verified narration timeline and English captions.

```sh
set -e
export SUPERTONIC_SOURCE_ROOT='/absolute/path/to/verified/model-workspace'
python synthesize.py
python audio-build.py
ffmpeg -hide_banner -y -i audio/voice-timeline.wav -af loudnorm=I=-16:TP=-2:LRA=9 -ar 48000 -c:a pcm_s24le audio/final-mix.wav
ffmpeg -hide_banner -y -i Agri-Brokerage-Picture-1080p.mp4 -i audio/final-mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -t 30 -metadata 'comment=AI-generated English narration:Supertonic3 F1;voice-only soundtrack;original conceptual3D scene,not live market data or MN7R UI' -movflags +faststart Agri-Brokerage-1080p.mp4
ffmpeg -v error -i Agri-Brokerage-1080p.mp4 -f null -
ffmpeg -hide_banner -i Agri-Brokerage-1080p.mp4 -af loudnorm=I=-16:TP=-1:LRA=11:print_format=json -f null -
```

The table uses authored transforms and a two-sided composition,not physics or
independent-camera split screen. A shared real cover continues over the22.2s hard
background cut. Inspect encoded camera framing,chip/cover legibility and consecutive
cut frames;separately inspect native opaque1280x720 thumbnail at full/reduced size.
Decode/loudness alone do not establish sync,mono compatibility or listening quality.
