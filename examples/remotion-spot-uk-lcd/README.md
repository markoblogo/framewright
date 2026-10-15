# Ukrainian spot-market LCD authoring example

Original Remotion4.0.53524s1080p30 picture. Pixel-grain field,factor selectors,abstract
field→elevator→port route and slat-to-cover reveal. Illustrative design,no live
quotes,real geography,service screenshot or physical simulation.

Owner cover/voice/weights/media are absent. Put authorised portrait cover at
public/cover.jpeg and review every title/claim. For open demonstration assets use
[first video](../../docs/first-video.md). Read Remotion Free/Company eligibility
before setup;pilot reused a local runtime,not a clean-machine install.

```sh
npm install
REMOTION_BROWSER='/absolute/path/to/working/chrome-headless-shell'
npx remotion still src/index.ts SpotUK preview.png --frame=600 --browser-executable="$REMOTION_BROWSER" --timeout=120000
npx remotion render src/index.ts SpotUK picture.mp4 --codec=h264 --crf=18 --concurrency=1 --browser-executable="$REMOTION_BROWSER" --timeout=120000
```

This example exports silent picture. The film uses Supertonic3 F1 from the exact
reviewed model/config/style manifest,then a shared48kHz voice/music/effects mix
and FFmpeg mux. Preserve the accepted raw intro,measure new script before cuts
and check the final encoded picture/audio. ModelOpenRAIL-M requires intelligible
synthetic-content disclosure;retain it in publication copy/metadata.

[Experiment](../../experiments/2026-10-15/spot-market-uk-lcd.md). No new release.
