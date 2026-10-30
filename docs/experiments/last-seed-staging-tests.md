# The Last Seed — greenhouse and dawn staging tests

28 October2026. Owner authorised two short visual tests following the proposed
[60s storyboard](last-seed-storyboard.md). Both reuse the accepted pilot scene v5
at mature frame171, preserving its original seed, stem, leaf and tray geometry.

## What is being tested

- **Wide,3s:** a slow camera push around the living station, surrounded by empty
  trays and dried stems. The growing station should read clearly in a coherent
  greenhouse set with supported benches and connected visible structures.
- **Dawn,3s:** the hanging lamp fades, followed by warm sunlight through framed
  windows. The leaf/soil exposure and moving window shadow should make the change
  legible. This condenses the longer proposed film transition into a timing study.

Both previews are intentionally silent. They do not replace the accepted pilot,
change the full-film cut, or establish final sound/movement approval. New original
geometry is created by [stage_tests.py](../../examples/last-seed/stage_tests.py).
Run it in Blender on a retained v5 scene: `--python ABSOLUTE_SCRIPT -- NEW_DIR wide`
or `dawn`; add `--controls` for only frames1,36,72. The source and prior outputs
are not overwritten. Render sequentially on the Mac.

## Discovery and correction

Initial wide control frames made the isolated plant readable. The first dawn
control remained dark: an opaque rear backdrop blocked the sunlight. The corrected
builder lowers that backdrop below the window aperture, adds side-bench supports
and changes the world tint with dawn. The corrected end control shows warm soil,
a lit leaf edge and window-frame shadows. Original negative controls are retained.

This is original procedural staging in manual Eevee, outside the admitted Cycles
executor. No external uploads, models, subscriptions or installations are used.
PREVIS-01 three alternative compositions and DJV review were not performed here.

## Evidence and next decision

[Measured test evidence](../../experiments/2026-10-28/evidence/last-seed-staging-tests.json)
records frame/source/output hashes, render time, format/decode checks, camera/light
endpoints and sampled luminance. Numerical changes do not establish perception
or artistic acceptance. Owner review remains pending.

After review, use the selected set and light treatment for cheap cassette/reservoir
staging and a timed full-film animatic. Full production, final audio, fresh-session
recovery and local YouTube kit remain R03 work; REL-A has not been reached.

## Completed local measurements

Both v2 previews passed72frames/3s/1280×720/24fps, frame hashes and full decode.
No audio stream is intentional. Wide rendering took122.81s; dawn119.90s.
Sampled mean grayscale in dawn went42.72 →32.03 →63.27 (frames1/36/72),
consistent with dimming then brightening; this is a numerical observation, not
a perceptual pass. Camera and lamp/sun endpoints are in the evidence file.
The private journal retains both scene revisions, source script, outputs,
technical receipts and separate pending owner-review tasks.

## Owner feedback and glazing revision

Owner accepted the lamp-to-dawn v2 treatment, while requesting cloudy glazing
for the wide set: roof, sides and rear enclosed; the camera-entry/front stays open.
The accepted dawn preview remains retained unchanged; its acceptance concerns the
light treatment. Light transmission in the eventually combined glazed dawn set
will need a separate control before final film rendering.

The v3 wide builder adds framed pane meshes with restrained tinted transparent/rough
surface mixing and procedural cloud variation. This is an authored Eevee look, not
a validated optical simulation. Control still inspection shows enclosed surfaces
while keeping the plant readable. New scene/script/output revisions preserve v2.

### Glazing resource comparison

The v3 layered transparent surface cost about11s/frame on this Mac and its
full preview was deliberately stopped/reaped; partial frames remain negative
resource evidence. The v4 alpha-blend controls cost about20s/frame. The v5
wide preview therefore uses an explicitly **opaque frosted-glass look-development
proxy**, with rough reflections and cloud variation. It is not transmission-
qualified glass. Owner review concerns the enclosure appearance; final dawn
through the combined set still requires a separate lighting solution/control.

### Delivered glazed wide test — 29 October2026

[Measured evidence](../../experiments/2026-10-28/evidence/last-seed-wide-glazing.json):
v5 passed72frames/3s/720p24fps, frame hashes and full decode. All72 recorded camera
positions match v2. Rendering took170.63s. The local comparison preserves v2 and
shows v5 by default; the accepted dawn-v2 file stays unchanged. Journal records
owner acceptance for dawn-v2, requested revision for wide-v2 and pending review
for wide-v5. The frosted appearance proxy does not establish light transmission.

### Owner rejects opaque proxy — translucent exterior revision

29October: owner said the v5 enclosure reads as green plastic and asked for
semi-transparent glass with a faint surrounding landscape. Record v5 as requiring
revision, not accepted glazing. The revised builder uses low-alpha Principled
surfaces, roughly10–23% surface opacity with cloud variation, and actual exterior
geometry: distant relief and layered conifer silhouettes. Front entry stays open.

The v6 dithered16-sample control transmitted the landscape but showed grain.
The v7 blended-alpha control reduced that grain and was selected for the wide
preview. This is alpha transparency, not a physical refraction/blur simulation;
exterior geometry can be seen through the panes. The original pilot and accepted
dawn-v2 preview are preserved. The eventual combined dawn set still needs checking.

### Delivered translucent wide test v7

[Measured evidence](../../experiments/2026-10-28/evidence/last-seed-translucent-glazing.json)
records72frames/3s/720p24fps, full decode, source-frame hashes and unchanged
camera positions across72samples. Render time: 114.17s,16samples.
The private journal retains the new scene/script/preview and owner-review wait.
The comparison page shows v7 against rejected opaque v5; owner acceptance is pending.

## Owner acceptance — 29 October2026

Owner viewed staging-glass-v7 and accepted the translucent greenhouse wide test
("Принимается. Нормально уже."). Its creative receipt and review task are
accepted/done. Together with accepted dawn-v2, this fixes the selected enclosure
appearance and light treatment; the combined glazed dawn shot still needs a
control. Next: seed cassette and last-water details, then a full timed animatic.
No full-film acceptance or release/publication is inferred.
