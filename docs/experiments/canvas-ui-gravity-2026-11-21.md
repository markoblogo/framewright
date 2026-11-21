# CANVAS-UI-01: glass over a moving scientific illustration

21 November 2026. Follow-up to the [robot pilot](canvas-ui-captcha-pilot-2026-11-20.md), applied to the [gravity explainer](../productions/gravity-through-wall.md). Question: does a glass annotation make a small signal label easier to read over the moving apparatus than a dark opaque label?

Reused the retained Canvas UI Glass GLSL and deterministic adapter from upstream commit `6d46250` with the upstream notice retained privately. Input was a raster sequence from the owned elevator cutaway. In Chrome 157.0.8103.79, the test rendered both treatments of the same 72 frames at 720×405 and 12 fps, using identical label text and motion. All 72 glass and baseline pairs differed. Repeating frame 34 returned identical pixels for each treatment. A six-second side-by-side MP4 and exact test inputs and receipts were retained. Browser API detection was positive. Native DOM capture was not performed.

The letterforms remain stable because the same text is composited after the effect in both samples. On inspected frames, the glass treatment retained more apparatus detail behind the label, reducing visual separation. The opaque label was clearer at a glance. The film uses plain data labels with their own reserved space. Operator observation only, with no owner verdict on the A/B or measured readability gain. Testing was local and used the existing Mac runtime. Labour, energy and speed advantage were not measured. This tests a single moving wide-layout callout, not a recommendation against glass in other styles.

Private evidence: `productions/gravity-through-wall-2026-11-21/verification/canvas-ui-comparison.mp4`, `canvas-ui.json`, and `trial/index.html`.
