# Contract execution dossier — archived authoring example

32s1920x1080p30,Remotion4.0.535,Supertonic3 SDK1.3.1 F1 English,FFmpeg.
Original book art,voice weights and media are absent. This is an author-specific
archived example,not the open-asset starter:[first video](../../docs/first-video.md).
Place authorised art at `public/cover.jpeg`;review every claim/CTA for that book.

The five-scene structure was adapted from
[Alex Prompter's catalogue entry](https://prompt-motion.com/alex-prompter-1ea044),
using original wording,animation and audio. No creator media/code is included.
Prompt Motion supplies references,not rendering or a licence to creator assets.

Inspect the pinned Remotion Free/Company licence eligibility before installing.
The pilot reused existing packages/models;it was not a clean-install test.
`synthesize.py` loads this example's committed `model-manifest.json` and verifies all
model/config/style hashes against that pin;an external manifest cannot redefine it. Set `SUPERTONIC_SOURCE_ROOT` to your verified model workspace,containing `models/Supertonic-3`;its own manifest is not trusted.
retain SDK1.3.1 and the experiment's model revision. No automatic download.
Model weights use BigScienceOpenRAIL-M;disclose AI-generated narration.
Do not run this example unchanged against an unrelated book or voice model.

The source timing has five measured utterances. `audio-build.py` uses NumPy,
SoundFile and installed FFmpeg to resample/mix;keeps separate voice/music/effects.
Python environment/version pins and model manifest belong to retained experiment
evidence. No voice-quality approval is implied by a technical export.

```sh
npm install
REMOTION_BROWSER='/absolute/path/to/working/chrome-headless-shell'
npx remotion still src/index.tsx Thumbnail Contract-Execution-YouTube.png --browser-executable="$REMOTION_BROWSER" --timeout=120000
npx remotion render src/index.tsx Contract Contract-Execution-Picture-1080p.mp4 --codec=h264 --crf=18 --concurrency=1 --browser-executable="$REMOTION_BROWSER" --timeout=120000
```

Cache disabled in config. The pilot isolated its writable cache from reused
packages after a shared-cache permission failure. Keep browser/cache failures in
[the experiment record](../../experiments/2026-10-15/contract-execution-prompt-motion.md).
Inspect native thumbnail and final encoded video/audio separately.

Every synthesis run regenerates selected WAVs,including existing names;there is no filename-based audio cache. Preserve accepted masters externally before a new trial. Scoped ignores exclude generated audio/metadata,cache,guides,authorised public assets and root PNG/JPG/SRT outputs from Git. Ignore rules prevent accidental adds,not automatic storage cleanup.
