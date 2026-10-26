# CorridorKey 2.0: bounded temporal keying comparison

Reviewed 2026-10-26. Owner selected a candidate test **after choosing an available
execution route**. No installation, weights download, purchase, inference, private
asset upload or production use has run. Queue retention does not authorise those
actions. The source fragment and target background remain to be chosen.

## Selected test

One cleared 5–8s green/blue-screen fragment with motion and difficult edges, such
as hair, fine fabric or motion blur. Compare CorridorKey with an ordinary chroma
key on the same frames. Composite both onto light, dark and the intended target
background. Inspect halos, lost details, coloured edges/spill and temporal flicker;
record processing time and full cost. Select one fixed input/timing/resolution and
document hint masks and comparator tuning effort for a meaningful comparison.

Keep the original, conventional-key baseline, alpha and foreground outputs, exact
settings/versions and final composites separate. Review boundary pixels and playback,
not just a checkerboard still. Verify frame count, duration, alpha interpretation,
colour handling and encoded output; retain source sound unchanged or review any
explicit audio change independently. Technical checks and owner preference remain
separate. Model output is an estimate, not proof of faithful recovery of fine detail.
Do not call a low-memory single-frame test temporally qualified. If a usable native
alpha already exists for a rendered character, preserve it rather than introducing
an unnecessary keying pass. Passing this sample does not qualify arbitrary background
removal, every resolution, lengthy shots or an entire host/plugin family.

## Execution routes and resources

- [GitHub inference package](https://github.com/nikopueringer/CorridorKey2.0): current
  README requires NVIDIA RTX 30-series or newer, CUDA PyTorch, FFmpeg and about 5 GB
  of weight downloads. It lists 4 GB VRAM up to 1440p and 6 GB for 4K; small-memory
  temporal windows trade context for memory. These are documented requirements, not
  our speed/quality measurements. No native Apple Silicon path was confirmed in
  this package. Pin exact code, weights and dependencies before any later run.
- [Separate official product](https://corridorkey.com/): paid standalone/plugins;
  the current detailed requirements list M-series Mac/macOS 14+ as well as Windows/
  NVIDIA. Confirm exact build, host compatibility, price/entitlement and Mac behaviour
  before choosing it. Website availability and marketing examples are not a tested
  local Mac route; the paid product and public inference package are separate scopes.

No GPU rental, paid plugin, OS change or asset transmission is approved by this
record. Start by checking the chosen route/resources and agreeing a bounded sample;
do not download models merely to populate the queue.

## Documented capability and rights

The README describes alpha/foreground prediction, no-hint/first-frame/full-video
hint modes, temporal windows, despill, native-resolution handling, ProRes 4444 and
linear EXR output. Preserve linear/display-referred and straight/premultiplied
interpretation at the handoff; video previews are not a substitute for HDR EXR.

[Corridor Key Licence](https://github.com/nikopueringer/CorridorKey2.0/blob/master/LICENSE)
adds conditions to CC BY-NC-SA: it explicitly permits commercial image/video
processing and output use, but restricts repackaging/resale, paid inference services
and commercial-software integration; released derivatives have naming/free-access/
share-alike conditions, and organisations above its revenue threshold have seat
requirements. Do not label it MIT or unrestricted open source. Review the exact
retained licence for the selected use; external production-tool use and incorporating
code/weights into Framewright are distinct decisions. No code/weights are vendored.
[Third-party notices](https://github.com/nikopueringer/CorridorKey2.0/blob/master/THIRD_PARTY_NOTICES.md)
list separate C-RADIO/NVIDIA, MoGe/MIT, and RVM code/weight conditions. Input footage,
likeness, background and sound rights remain independent. No blanket clearance or
runtime provider promotion follows from this assessment.

[Queue](../experiment-queue.md) · [Inventory](../tool-research.md).
