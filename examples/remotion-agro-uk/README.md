# Ukrainian paper-route book promo source

Authored SVG/React animation in Remotion4.0.535. Different creative treatment from
ManimGX infographic panels:90kernels regroup into a route,then a contract;paper
truck,execution stamp,book reveal. Frame-driven24s1920×1080/30.

Original owner book art,models,voices and media are deliberately absent. This is an
archived authoring example,not the open-asset reference film. For a public starter
use [first video](../../docs/first-video.md). Put an authorised book image at
`public/book.jpeg`;check its crop and every rewritten title/claim before rendering.
Do not imply sample Ukrainian promotional copy applies to an unrelated book.

Read Remotion's exact Free/Company licence eligibility before installation.
Dependencies are pinned in package.json;the pilot reused an existing runtime and
working Chromium,not a clean new install. Exact voice pins are in the
[retained lock](../../experiments/2026-10-15/evidence/agro-uk-voice-requirements.lock).

```sh
npm install
REMOTION_BROWSER='/absolute/path/to/working/chrome-headless-shell'
npx remotion still src/index.ts AgroUK preview.png --frame=600 --browser-executable="$REMOTION_BROWSER" --timeout=120000
npx remotion render src/index.ts AgroUK picture.mp4 --codec=h264 --crf=18 --concurrency=2 --browser-executable="$REMOTION_BROWSER" --timeout=120000
```

Picture is silent. Piper1.4.2/Tetiana produces separate mono22.05kHz phrases using
`synthesize.py`,after exact model/hash and terms review. Create `models/` and
`audio/`,place the pinned model/config under the expected names;no implicit model
download or paid API. EngineGPL3,voice cardApache2.0,no cloning. Resample/mix on a
common48kHz24s timeline,then mux picture with checked voice/music/effects;do not
stretch Ukrainian speech to rescue an overloaded script. Narration starts at
0.3,6.5,11.7,15.3,18.8seconds;last voice end23.722646s.

[Experiment and limitations](../../experiments/2026-10-15/agro-uk-paper-piper.md).
Owner accepted the simple visual style but found this Ukrainian voice weak;use a different tool for the next Ukrainian narration. Technical export remains valid.
