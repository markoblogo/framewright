# AMI Books — archived OpenScreen tour

Private author-project snapshot,not the open-asset starter. No book/site art,
recordings,voices,weights or application bundles are redistributed. Use
[the reference film](../../docs/first-video.md) for an open starter. Authorised
recording does not grant rights to third-party publications linked by a site.

Tested OpenScreen2.0.0 AppleSilicon official ZIP,revision
`eff86dcba48fac490a0e153141bf8537df7ffc54`,MIT. Upstream MCP guide was ahead of
the released executable:the run used its documented CLI. Recording used one
public Chrome window,no mic/system audio/camera. OS permissions remain user-owned.
The released CLI records under its application-data directory even when
`--project` points to another disk;`pack` copies media to the selected destination.
Check both disks first. Do not assume all caches/recordings live beside the app.

`OPENSCREEN` points to the installed executable;`VOICE_PYTHON` is the existing
Supertonic3SDK1.3.1 environment with numpy,soundfile,onnxruntime;
`SUPERTONIC_SOURCE_ROOT` is the retained voice/model root. Model/config/style hashes
are checked against `model-manifest.json`,not a downloaded manifest. Code is MIT;
Supertonic3 weights use BigScienceOpenRAIL-M. No new model or dependency install
was tested here. FFmpeg and Pillow are needed for finishing/inspection.

```sh
"$OPENSCREEN" help
"$OPENSCREEN" sources --json
# Choose the unique authorised public window,not an entire display.
"$OPENSCREEN" record --window 'AMI Team Publishing' --duration 8 --project probe.openscreen --json
"$OPENSCREEN" pack probe.openscreen --out probe-portable
# Inspect raw dimensions and actual frames BEFORE a longer take.
# The retained take was driven via computer-use,then copied here as capture.mp4.
python3 build-picture.py
"$VOICE_PYTHON" synthesize.py
"$VOICE_PYTHON" build-audio.py
ffmpeg -hide_banner -y -i Narration-raw.wav -af loudnorm=I=-16:TP=-2:LRA=9:print_format=json -f null - 2> loudnorm-measure.txt
"$OPENSCREEN" export film.openscreen -o AMI-Books-OpenScreen-native.mp4 --json
python3 finish.py
ffmpeg -hide_banner -loglevel error -xerror -i AMI-Books-1080p.mp4 -f null -
ffmpeg -hide_banner -loglevel error -ss 0.5 -i Screen-Assembly.mp4 -frames:v 1 -vf scale=1280:720 AMI-Books-YouTube.png
```

The retained capture hash is enforced;different site footage needs a newly
inspected edit map,crop and freeze boundaries. Do not reuse timestamps blindly.
`build-picture.py` selects six scenes;the Contract page uses0.4s plus a7.6s freeze.
Native output is1080p60;`finish.py` converts to30fps,normalises the six-line voice
and copies the checked picture stream into the final narrated42s MP4.
Inspect every scene/cut,short callouts and thumbnail at full/reduced size. Check
1260frames,stereo48kHz AAC,full decode,encoded loudness/peak,voice placement and
private-surface exclusion. No automatic ASR,model routing qualification or public
reproducibility is claimed. Source snapshot is not a new autonomous installer.
