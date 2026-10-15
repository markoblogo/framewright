# Agricultural library — MoviePy compilation archive

An author-project snapshot,not a new open-asset starter or clean-install guarantee.
Use [the reference film](../../docs/first-video.md) for open demo assets. No book art,
clips,voice/model files,music or fonts are redistributed. Source identities in
`sources.json` refer to the owner's retained media under `FRAMEWRIGHT_MEDIA_ROOT`;
`render.py` checks hashes before decoding and disables all input audio.

MoviePy2.2.1 MIT;tested Python3.12.13 and FFmpeg8.0.1. Python dependencies pinned in `requirements.lock`. Existing
FFmpeg is explicit;the code does not ask ImageIO to fetch a binary. Tested system
Arial fonts remain external assets;other fonts need independent clipping/layout
checks. Supertonic3SDK1.3.1 uses the existing separate voice environment and the
committed model/config/style hashes:code MIT,weights BigScienceOpenRAIL-M.

```sh
python3 -m venv env
# Set TMPDIR/PIP_CACHE_DIR to a disk with space BEFORE installation.
env/bin/pip install -r requirements.lock
export FRAMEWRIGHT_MEDIA_ROOT='/path/to/retained-media-root'
export FFMPEG_BINARY='/path/to/working/ffmpeg'
export SUPERTONIC_SOURCE_ROOT='/path/to/retained-voice-model-root'
# VOICE_PYTHON points to the separate pinned Supertonic runtime.
"$VOICE_PYTHON" synthesize.py
env/bin/python render.py
env/bin/python audio.py
env/bin/python thumbnail.py
python3 finish.py
ffmpeg -hide_banner -loglevel error -xerror -i Agro-Library-1080p.mp4 -f null -
```

`render.py` first writes eight silent framed scenes,then dissolves them with
seven0.5s overlaps:63.5s becomes60s. New editorial headings sit on a separate
non-overlapping layer. `REUSE_SCENES=1` repeats only assembly after an assembly
change;it must not be used after changing the scene renderer without rebuilding.
Pillow measures glyph bounds to avoid the observed baseline clipping.

`audio.py` validates all eight voice rows/WAV hashes,loops the original author
instrumental stem at0.18gain,and writes60s PCM plus SRT. `finish.py` measures and
normalises to−16LUFS/−2.5dBTP before AAC encoding and stream-copy mux. Inspect
encoded loudness/true peak,voice placement,mono,each scene/overlap and full decode.
Expected1800frames,H2641920×1080/30,AAC48kHz stereo. Subtitle timings are measured
TTS timings,not independently aligned ASR.

The native1280×720PNG is a separate MoviePy/Pillow composition using an inspected
landing frame;`with_mask=False` makes its raster RGB. Check full/reduced legibility
and separate hash. Other formats,models,fonts and generic auto-editing are untested.
Paths were adapted for archiving;the complete commands were not rerun as a fresh
public installation. See [experiment and QA](../../experiments/2026-10-15/agro-series-compilation.md).
