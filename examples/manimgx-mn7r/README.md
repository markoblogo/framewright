# MN7R workflow promo source

Original ManimGX0.1.1/Python3.14.5 scene. This author-project example needs an
operator-authorised `assets/owner-cover.jpeg`;book art is not redistributed.
[Experiment](../../experiments/2026-10-15/mn7r-manim-mlx.md) records setup and QA.

```sh
manimgx inspect scene.py
manimgx render scene.py -o native.mp4 --fps 30 -r 1920x1080 --crf 18
```

The pilot's native VFR MP4 needs the retained timing adaptation before a CFR master:

```sh
ffmpeg -i native.mp4 -vf "fps=30,setpts=PTS-STARTPTS" -frames:v 600 -an -c:v libx264 -crf 18 picture-cfr.mp4
```

Preserve original VFR output,
normalised picture, separate voice/music/effect stems and assembled final hashes.
Do not use `setpts=N/(30*TB)` on deduplicated VFR frames: that would shorten held
pauses. Do not combine `-r` with passthrough output mode. This is not a portable
installer or a native-still/3D/UK-voice test. Models,runtimes,fonts,artwork and media
stay outside Git. See [the series plan](../../docs/experiments/agro-series-plan.md).
