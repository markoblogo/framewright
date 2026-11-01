# FFMPEG-OPS-01 — bounded local operations

30October2026. [Adoption plan](../research/agent-video-toolkits-2026-10-30.md).
Temporary external checkout of kajisho5/ffmpeg-skill at
`8b6c30528d70b262d8211c6ad0cf88b0de93d8c2`; no skill installation, copied upstream
code in this repository, model download, cloud call or payment. Python3.14,
existing Homebrew FFmpeg on macOS Apple Silicon. MIT upstream; media rights remain
separate. No complete safety audit or executor integration is implied.

## Controls and observations

- Missing original Downloads path was rejected with structured INPUT_INVALID.
  Used the separately retained source GIF; never replaced accepted film bytes.
- Source: Afterimage's25.3s,600×338,10fps GIF with three artworks. Threshold10
  detected only0/8.8s boundaries and merged dark material. One bounded retry,
  threshold3/ratio2, found0/8.8/17.2/20.9s: robot, body sculpture and two views
  of Covering Letter. Contact sheet inspected. Four visual segments do not mean
  four artworks; boundary timing and artistic identity still need human review.
- Exact2s excerpts at1s and10s completed; both retained picture-only inventory.
  Join at640×360/24fps completed with4s measured duration. Its default join added
  a silent audio track, explicitly reported by its output inventory. Do not
  describe this as unchanged stream inventory across the join.
- Upstream probe/stream/duration/head-tail decode checks passed for the cut/join
  outputs. Final full decode and production-level checks are recorded separately.

`--no-timecode` avoided the current FFmpeg build's absent drawtext filter. Caption,
HDR, subtitles, other codecs, MCP and every other operation remain untested.
`scenes --dry-run` still performs source analysis before planning the sheet;
never interpret it as a guarantee that no decoder/process runs.

## Disposition

Keep scene suggestions/contact sheets and cut/join as a scoped external candidate.
No automatic catalogue-wide qualification. First compare source ranges visually,
then check exact output inventory and elapsed/resource bounds. Any future executor
adapter must pin the external tool, arguments and sources and preserve failure,
output and human-review gates. The existing local method remains the fallback.

## Production follow-up

On R04, individual1s/14s extraction completed and produced actual source frames.
The automatic timed3×2sheet instead contained only an incomplete black tile; it
is retained as a failure, not accepted as a visual review. A direct six-frame
sheet and full final-master decode are the fallback. This narrows the candidate
qualification; no automatic integration or current-source model evaluation.

## R05 repeat on Beyond the Letters — 1 November 2026

Same upstream revision8b6c30528d70b262d8211c6ad0cf88b0de93d8c2, existing macOS
Apple Silicon/FFmpeg, no install/update/network/model/purchase. Accepted36s master
pinned and unchanged. First probe, then --no-timecode/320px PNG extraction and
960px3×2automatic sheet, sequential60s outer timeouts (upstream30–45s).

**Negative confirmation:** automatic sheet exits0 and reports completed, but actual
968×366 PNG contains one nearly black tile and otherwise empty grey padding.
Agent inspected the PNG and retained tile measurements/commands. Earlier R04
failure reproduces on this second production. Do not use exit0/probe as proof of
a populated sheet. Automatic sheet is excluded from the working route on this
revision/host; root cause not established and no upstream patch or general rejection.

**Positive confirmation:** explicit look.py --at PNG extraction at3/9/15/21/27/33s
matched direct FFmpeg pixel-for-pixel. Some correct frames were black because the
chosen times hit scene fades. A second bounded set at2/8/14/20/26/32s also matched
pixel-for-pixel; its local six-frame composition visibly contains artwork,
architecture and captions in all tiles. Choose midscene times, then assemble with
our existing image helper. Six-frame visual inspection is not full-film QA.

Scoped disposition: explicit --at extraction, --no-timecode, width320, PNG on this
host/revision is confirmed across two suitable production cases. Keep the direct
FFmpeg/local composition fallback. Scene suggestions/cut/join retain their prior
limited statuses; no captions/HDR/MCP/full-library qualification, automatic adapter
installation or rights clearance. This completes the bounded R05 comparison with
both positive and negative outcomes. [REL-B assessment](../rel-b-readiness-2026-11-01.md).
