# Hy-Nomas — launch-route-gated world-video candidate

Reviewed and queued by the owner on 2026-10-26; refreshed 2026-11-02. **Documentation-reviewed only**;
no installation, weights download, account connection, generation or GPU rental.

## Evidence and fit

- [Official repository](https://github.com/Tencent-Hunyuan/Hy-Nomas): free-form
  interactive video-world generation with segment-level text changes and camera
  trajectory conditioning. Code covers inference, training and web demo.
- [Runtime guide](https://github.com/Tencent-Hunyuan/Hy-Nomas/blob/main/reactor/README.md):
  live prompts and camera controls; this particular Reactor path still documents
  text initialization only. Separately, the main README announces reference-image
  initialization on 2026-10-31; the [web-demo guide](https://github.com/Tencent-Hunyuan/Hy-Nomas/blob/main/apps/README.md)
  documents image input and a required DCAE-V encoder checkpoint for self-hosting.
  Do not generalize one adapter limitation to the hosted demo. Generated video is
  not an established editable mesh, rig, splat or persistent reusable 3D set.
- Main README documents Linux/NVIDIA and an offline low-memory RTX 4090 path with
  quantization, bounded history and CPU offload. This does not establish interactive
  RTX 4090 performance or native Apple Silicon support. The web-demo guide also
  offers a single-GPU low-memory video worker, but requires a separate running
  Nomas-PE service with its own GPU resources; one video GPU is not proof that the
  complete demo stack fits one consumer GPU. Output fps is not generation speed.
- The tested resident streaming profile uses eight B200 GPUs, at least 128 GB host
  RAM and at least 200 GB free disk. Native world horizon is 120 seconds; retained
  history does not establish infinite stable generation. Long continuations can
  drift in geometry, colour and prompt adherence; controls affect future segments.
- [Licence](https://github.com/Tencent-Hunyuan/Hy-Nomas/blob/main/LICENSE): Tencent's
  released code, parameters and weights Apache-2.0; third-party components retain
  their terms. Hosted-demo terms/availability and source/output rights need their
  own check before use. No upstream code or weights copied into Framewright.

Potential use: atmospheric travel, world footage and selected book-adaptation
inserts. Exact hero continuity, returning to locations and separately animated
characters remain unqualified. A later Good Dog use depends on the actual trial.
Sources were reviewed at mutable main; pin a revision/build before execution.

## Video refresh, 2026-11-02

[Owner-supplied video](https://youtu.be/3n9RCoXGbuQ), “Tencent Hy-Nomas:
Open-Source AI World Model Runs on a Single RTX 4090!”, 2:21, published by
ABV — AI · Books · Validation on 2026-11-01. Title and expanded description
inspected; transcript unavailable. No full listening/viewing or runtime test
claimed. Technical conclusions above checked against official documentation.

Useful for M4/R05 discovery and a possible M5/R07 book-film insert: initialize
from an approved hero/environment image, then test a short controlled movement.
This extends the existing trial, not a new queue entry or a required REL-C step.
Image input does not yet qualify hero identity, exact geometry or returning to
locations. First preference is an accessible hosted route with a verified free
allowance/export; Linux/NVIDIA deployment remains a resource-gated reserve.

The main README lists WanGP (history/save/resume/record), ComfyUI, SGLang and
Reactor integrations. These are alternative launch routes to investigate only
if needed, not four additional installs. Availability, limits and output rights
remain unknown until checked at use time.

## Owner-selected first trial

**After confirming an accessible launch route:** original world → 5 seconds of
movement → one change of action or camera → another 5–10 seconds. Prefer one
approved reference image if the selected route supports it; compare hero and
landmarks to that image before/after the change.

1. Choose hosted access or a suitable GPU route; verify export, current terms,
   resources and total cost before committing to a run. A demo-fetch timeout is
   not proof that the service is unavailable. No silent provider substitution.
2. Use one original non-sensitive scene with a visible character and spatial
   landmarks. Retain prompt, selected model/config/revision, seed if exposed,
   camera commands, timestamps and unedited exported video.
3. Inspect spatial continuity, character preservation, responsiveness to the one
   change, visual quality and motion. Note geometry/colour drift, delayed control,
   artefacts and any manual repair. Record generation time, latency and full cost.
4. Review the encoded complete fragment, including the change boundary. Record
   technical results and owner preference separately; unsupported export or access
   stays blocked. One short pass does not qualify long worlds or a full film.

Queue retention authorises no install, download, spending, upload or publication.
No automatic runtime provider is added. [Queue](../experiment-queue.md) ·
[Inventory](../tool-research.md).
