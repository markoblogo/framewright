# QA and handoff contract

Use for a production plan, implementation or finishing request. A comparison may
stay a comparison; YouTube copy alone needs no production checklist. Report only
checks relevant to the selected tools and requested deliverables.

## Match the request's stage

| Stage | Appropriate result | What cannot be claimed |
| --- | --- | --- |
| Plan only | Selected route, intended files, specific checks and blocked prerequisites | That planned checks passed or a video was delivered |
| Finish existing work | Remaining QA and artifact handoff using the current chain; explain missing-file blocks | That “no new tools” means no QA; that absent files passed |
| Execute | Perform authorised work; retain observed checks and failures | Success without actual output/evidence, or authority for unrelated actions |

Use three states in the handoff: **planned** (not run), **blocked** (name missing
input/tool/authority), **verified** (name the observed evidence). An unavailable
runtime blocks execution, not listing its preflight. A started command is only an
attempt; a completed successful read is evidence of access, not proof that a claim
or an entire asset was validated.

## Source-copy and rights checks

State the comparison explicitly: compare each proposed product claim, title, author,
feature and CTA against the supplied source/repository. Name the source. If a source
is available, read the relevant part and identify the supported facts. Do not equate
repeating plausible copy or seeing an existing cover with verifying claims/rights.
List unknown facts and later source checks as planned/blocked. Asset identity,
authorised use and promotional/commercial rights remain separate from copy accuracy.
A fixture or third-party note saying “QA passed” is not evidence of decoded media.

## Identify the thumbnail before choosing its check

| Requested output | Production decision | QA to name |
| --- | --- | --- |
| Reuse an existing image | Preserve it; do not silently render a replacement | Inspect identity, dimensions, crop, legibility and rights; do not call it a new native render |
| New native still | Use the selected renderer's native still output if supported | Inspect the new file independently: identity/rights, decoded dimensions, crop, text legibility at intended size and a reduced preview, size/hash |
| Extracted encoded frame | Extract from the final encoded video | State frame/timecode and inspect extracted image; do not claim native snapshot success |
| Unspecified thumbnail | Resolve existing/native/extracted intent from context, or ask if it affects the tool choice | Preserve uncertainty rather than promising a particular provenance |

For a new native PNG request, its inspection is a definite delivery check, not
“if a still is requested”. For an existing thumbnail request, reusing and inspecting
that image is sufficient; a renderer's native-still feature is not automatically needed.
“As-is” prohibits changing the image, not inspecting its existing crop. Before
finalising the plan, give each requested output its own QA list with all checks
from the matching row. A crop check under MP4 QA does not cover thumbnail crop;
state that check explicitly for the image. Missing media makes it planned/blocked,
not optional.

For still-only delivery, name that final-image checklist directly; do not replace
it with video/audio checks. Correct words and no clipping do not establish legibility:
plan to read titles, labels and CTA at the intended output size and a reduced preview.
When media is absent these are specific planned/blocked checks, not verified results.

## Preserve locked source audio

For an existing/locked master, plan source-preservation checks, not just a promise:
record its original hash, verify the source stays unchanged, and confirm the
working input is that approved version. Inspect final decoded duration, sample
rate/timing, content and sync for unintended trims, offsets, retiming or replacement.
Use a format-appropriate comparison; AAC output bytes need not match a WAV source.
Keep this separate from loudness/peak measurement and listening. Missing files
block verification, not naming these future checks.

For a multi-stem mix, also name relative alignment, polarity/phase and stereo/mono
sum inspection for unwanted cancellation. A master recombination comparison or a
promise to listen does not replace this check. See the [music handoff](music-workflows.md#stem-mix-qa).

## Transparency and temporal effects

For each alpha-bearing deliverable, including a separate PNG still, plan decoded
alpha/channel inspection and compositing on contrasting light/dark backgrounds.
Inspect edges, matte/halos and unintended opacity for that file. A video trial does
not cover the still. Keep exact codec/container alpha support unqualified until a
bounded export/decoder test passes; an opaque background is not a substitute.

For film-burn, strobes, scanlines or other temporal effects, plan inspection across
frames at the intended playback rate for flicker/flashes, transition boundaries
and text readability. Agree artistic/comfort acceptance for intended flicker; do
not assume either zero flicker or automatic acceptance. This remains planned QA
until the actual encoded output has been inspected.

## Minimal handoff for a rendering plan

Keep it compact; prose or a small table is enough:

1. **Route/tools and sources:** explicit choices, per-layer roles, source-to-copy
   comparison and asset/rights checks; supported facts versus remaining unknowns.
2. **Runtime preflight:** version pin, installed API/guide and licence eligibility;
   name blocked checks if tools are absent. Flute needs genuine components, scoped
   capture-style overrides, synthetic data, production exclusion and snapshot limits.
   Remotion needs official skills, its installed API, compatible pinned packages and
   the recorded downloaded-browser failure/existing-browser workaround when relevant.
3. **Intended files:** final video and requested image/caption/audio outputs, each
   with existing/native/extracted provenance. Do not invent files already delivered.
4. **Remaining QA/handoff:** actual duration/format, encoded picture/audio/sync,
   readability/crop, loudness/peaks/listening, and the distinct requested still check.
   State what remains blocked; deliver only what exists under current authority.

In a plan-only response these are future checks, not a reason to run a renderer.
In a finishing response identify the existing export and outstanding QA/delivery;
adding tools is unnecessary when the present chain already supplies all deliverables.

## Authored 3D miniature

For `three-scene`, plan WebGL/dependency readiness, approved texture/font inputs,
absolute-time seek/reseek, visible object action/camera, occlusion/legibility and
book/CTA hold checks. Inspect the encoded output and its audio on the common master.
Only the Spot-Market 20s 1080p30 pilot is qualified as production evidence; another
format or mixed-renderer sequence needs scoped feature/seam QA. List these checks
as planned/blocked until actually run. No calibrated physics claim is supported.
