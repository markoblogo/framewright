# Hy-Nomas — launch-route-gated world-video candidate

Reviewed and queued by the owner on 2026-10-26. **Documentation-reviewed only**;
no installation, weights download, account connection, generation or GPU rental.

## Evidence and fit

- [Official repository](https://github.com/Tencent-Hunyuan/Hy-Nomas): free-form
  interactive video-world generation with segment-level text changes and camera
  trajectory conditioning. Code covers inference, training and web demo.
- [Runtime guide](https://github.com/Tencent-Hunyuan/Hy-Nomas/blob/main/reactor/README.md):
  live prompts and camera controls; released inference starts from text, without
  exposed image initialization. Generated video is not an established editable
  mesh, rig, splat or persistent reusable 3D set.
- Main README documents Linux/NVIDIA and an offline low-memory RTX 4090 path with
  quantization, bounded history and CPU offload. This does not establish interactive
  RTX 4090 performance or native Apple Silicon support.
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

## Owner-selected first trial

**After confirming an accessible launch route:** original world → 5 seconds of
movement → one change of action or camera → another 5–10 seconds.

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
