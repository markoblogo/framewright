# Two ways to compose a film for landscape and portrait

10 November 2026 · CENTRE-CROP-01, R04/R05, M3/M4.
Bounded production evidence: two different 90-second English stories,
[Copilot addressed metrics and Final Cut/Pixelmator image repair](../productions/radar-pair-centre-crop-2026-11-10.md).
Both aspect versions and covers were owner-accepted; publication links are owner-reported.
The owner considers both visual techniques useful. No overall time/cost winner,
independent-user reproduction or causal audience result is established.

## Shared production recipe

1. Freeze two independently useful stories, comparable narration and six beats,
   common tool versions, source quality and sound scope before the pilots. Preserve
   rejected choices and setup costs. Here A uses a dark review lab; B a warm coastal
   editing scene. Illustrations explain official announcements, not a hands-on
   Copilot/Apple application test. Obtain script, pilot and full-film decisions.
2. Build named rigid objects and real action in Blender 4.5.15 Eevee: a response
   stamp/test gate for A, brush/boat/lighthouse for B. Evaluate parent transforms
   before preserving child world matrices. A doubled parent offset caused floating
   parts; selected-frame probes caught it before full export. Keep the failure and
   correction cost rather than calling the first render successful.
3. Measure narration chunks with the same offline Supertonic-3 M1 route. Reuse the
   accepted opening; generate only the remaining paragraphs. Use measured lengths
   for one 90-second timeline per story. Retain speech, score and SFX stems; keep the
   common quiet original score audible under speech. Do not rerun TTS for a picture fix.
4. Compose explanatory action, large type, progressive reveals, semantic image layers
   and soft joins with Pillow/FFmpeg. Draw logical layers separately: colour masks
   split the tower into duplicate fragments in the rejected trial. Keep movement
   meaningful rather than extending one still. The optional FW sting is omitted
   from both comparison films; its recurring placement is a separate experiment.
5. Decode all four exports. Check frames/duration, faststart, levels, audio identity,
   selected layouts/joins and actual native forward/backward seeking through the
   [standard range-capable preview](../../skills/video-production-router/references/preview.md).
   Obtain separate full-film listening/creative decisions. Package covers, copy,
   comments/tags and measured-paragraph English SRT/VTT; subdivision is approximate,
   not forced word alignment.

## Route A — independent compositions

Use one story, scene/action timing and audio mix, with separate 3840×2160 and
1080×1920 layouts. Reposition and resize type/panels/3D objects for each aspect;
review both. In this case portrait cards stack where landscape cards spread
horizontally. Encode portrait video independently and copy the landscape AAC
payload so the aspects do not acquire different speech timing.

Choose this route when framing, labels or subject placement need to change between
aspects. Layout freedom still costs authoring/review effort; that effort was not
independently timed in this production.

## Route B — landscape with a self-contained centre

Author a 3840×2160 landscape whose essential story and text fit a central portrait
column. Side regions contain secondary illustration, not missing instructions.
Keep primary portrait text at least 42 px and check the actual phone UI; the planning
critical-safe guide was x=80–900/y=160–1580 at 1080×1920. A safe-area check is not a
promise that every future TikTok interface crop will match.

Derive the 1080×1920 portrait from the encoded landscape master only:

```text
RGB crop: x=1312, y=0, width=1215, height=2160
Then proportional downsample to1080×1920; no portrait reflow or tracking crop.
```

This integer crop is 0.5 source pixel off exact centre. Convert to RGB before the
odd-width crop so subsampled YUV cannot silently round it. Copy the same AAC
payload. Compare representative decoded portrait frames against that exact crop
of the encoded landscape; lossy re-encoding means pixel identity is not expected.
If a portrait-only rescue is required, retain its cost and report that the pure
crop route failed. Correcting the shared landscape before both exports is not a
hidden portrait reflow.

A 1080p landscape supplies only about 608×1080 central pixels; these films deliberately
used 4K masters. Their 1440×1440 3D sources do not gain native 4K object detail from
compositing. This test does not compare the usual 1080p baseline with 4K or qualify
an upscaler. Use the centre route when the resulting landscape and portrait both
remain useful, not because a crop is automatically a good composition.

## Measured scope and result

Tool elapsed seconds, retained 10 November. These phases are not active human/agent
labour, total production wall time or monetary costs.

| Phase | A: independent layouts | B: fixed centre crop |
| --- | ---: | ---: |
| Pilot 3D source render | 291.74 | 219.67 |
| Full-stage source render, selected passes | 361.21 | 582.03 |
| Full-stage rejected attempts/probes, additional | 253.26 | 344.69 |
| Full-stage source render, all attempts | 614.47 | 926.73 |
| Full landscape composition/export | 247.86 | 290.92 |
| Full portrait composition/export | 142.75 | 40.47 |
| Full landscape + portrait exports, sum | 390.61 | 331.40 |
| New full-stage speech inference | 50.96 | 38.80 |

A reused the pilot's first 300 source frames; B's first full sequence was completely
rerendered after its boat-parenting correction. Both retained pilot costs and full
failed attempts count in the underlying ledger. Earlier rejected B0 preparation is
separate disclosed overhead, not erased or counted as a completed third story.
Shared final technical/package QA took 111.96 tool seconds, recorded once; generic
setup stays raw once with any 50/50 allocation explicit. Archive-excerpt preparation
is closeout maintenance, excluded from the original production comparison.

The B portrait export step was faster in this observed pair. Unknown active work,
model/subscription/compute money and numeric quality category scores prevent a
whole-workflow saving or the planned 20% active-effort conclusion. No provider
credits or new purchases were used; that is not zero total cost. Different topics,
geometry, order, correction burdens and packaging confound the comparison. The
owner accepted both visual results; later audience observations remain separate.

## Retention and transferable use

Keep all four accepted masters, editable selected Blender states, original static
assets/font, current compositing helpers, measured timeline, raw/processed speech
and score/SFX stems, packages, journals and source/rights records. The selected
assembler still reads 1752 PNG source frames, including the A pilot prefix; those
are retained inputs. B pilot, failed/probe and benchmark frame caches can retire
because the selected full assembler does not read them. Retain their historical
hashes/receipts and bounded before/after rig evidence; do not claim the retired
historical pixel caches remain available.

The owner requested material for a later experiment film: retain twelve accurate
local excerpts, three intervals per story in both aspects, with source hashes and
intervals. These re-encoded excerpts are preparation, not an independently approved
third film. Keep the accepted masters and stems for any later edit.

**With Framewright:** keep the frozen conditions, native project/COST-01 journals,
exact reviews, publication links and dependency inventory. Use only YouTube URLs
through the existing Radar exchange. Receipt/duplicate checks prove transport,
not analytics, experimental preregistration or altered recommendations.

**Without Framewright:** use a normal folder containing a source sheet, timed
script/stems, scene/layout files, aspect-safe guides, export settings, hash manifest
and review log. Follow the same two layout choices and preview/QA steps in an editor
or the same local tools. This written alternative is not a completed independent-user
reproduction. Check image/font/model licences before reuse; the production retained
original local imagery/music/SFX and existing Manrope/Supertonic provenance.


## Turn the experiment into a sourced film

The [90second YouTube-only results film](../productions/centre-crop-results-film.md)
uses twelve retained excerpts from the two completed stories. Show both routes,
then label each number with the measured phase. Export time is not active labour,
total production cost or an audience effect. Different stories, preparation, rig
corrections and order confound the comparison; keep inconclusive criteria open.

Its later voice correction copies the accepted encoded picture packets/PTS/DTS
unchanged. Measure the new natural speech, cut only at retained inter-paragraph
silences, and fit those chunks into existing scene beats without speed/pitch shifts.
Keep original score/SFX, caption-map limits, full decode/levels and owner listening
acceptance separate. Verify packet preservation rather than claiming it from
`video copy` settings alone. The final Knox take was explicitly accepted after
publication; its public URL alone was not that listening decision.

Retain the current v2 master, v1 picture-copy source, original new voice, stems,
cut map, package, source-render/font inputs and twelve excerpts. The3720 JPEG
proxies are rebuilt automatically by the retained assembler from those clips;
temporary decoded floats and superseded per-phrase M1 takes are not current v2
inputs. Preserve their retirement hashes and the earlier rejection.

With Framewright, bind those files and component decisions in its existing journal.
Without it, keep the same manifests, timed script, immutable picture source, WAVs
and correction/QA receipts beside an ordinary editor project. This written route
is not independent-user reproduction or evidence of causal audience benefit.
