# Music accents and encoded cuts — complementary analysis

A post-export helper, not a renderer or automatic editor. Tested on one authored
15-second book promo. It compares sparse musical landmarks with librosa onsets and
all declared hard cuts with PySceneDetect. Speech must be a separate stem; analyze
the music alone. Do not infer beat/downbeat quality from a tempo number.

Use a local Python3.12 environment and `requirements.txt`; the exact tested
[transitive lock](../../experiments/2026-10-15/evidence/burgers-analysis-requirements.lock)
is retained separately. PySceneDetect0.7.2 needs OpenCV installed explicitly; the
old `[opencv]` extra does not supply it. Code terms: librosa ISC; PySceneDetect
BSD-3-Clause; inspect the exact OpenCV wheel/build dependencies before redistribution.

```sh
python3 -m venv /path/on/Work/cue-env
/path/on/Work/cue-env/bin/python -m pip install -r examples/cue-analysis/requirements.txt
/path/on/Work/cue-env/bin/python examples/cue-analysis/analyze.py \
  --music /path/to/authorised-music.wav \
  --video /path/to/encoded-master.mp4 \
  --reference experiments/2026-10-15/evidence/burgers-cue-reference.json \
  --output /path/on/Work/cue-results
```

For the retained Burgers workspace, substitute `audio/music-original.wav` and
`Burgers-Lipstick-Underwear-EN-1080p.mp4`. Media is intentionally outside Git. Other
media needs its **own reference frozen before detection**; do not reuse Burgers
markers as universal defaults. Landmarks should be well separated relative to the
100ms window: this small nearest-landmark comparison is not a dense event aligner.
A new output directory is required; existing attempts are never overwritten.
The reference supplies tolerances/minimum matches; the detector parameters remain
the pilot defaults. These are not a universal QA policy.

Outputs: `cue-sheet.json`, `cuts.csv`, `comparison.json`. The authored reference
passed3/3 accent matches and4/4 exact cuts without parameter adjustments. Its
sparse accent labels cannot estimate all-onset precision; independent listening is
pending. No automatic retiming, recutting, cloud call, rights clearance or tool
selection qualification follows. See the [experiment](../../experiments/2026-10-15/burgers-cue-analysis.md).
