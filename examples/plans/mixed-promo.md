# Production plan

Status: **proposed** · execution: **not_started** · qualification: **planning_only**.
No assets were inspected and no checks were verified by this command. Filenames below are suggestions, not delivered files.

Canvas: 1920×1080 · 30 fps · total: 900 frames (30s).

## Scene timeline

| Scene | Frames (end-exclusive) | Duration | Overlap | Input kind | Tool chain |
| --- | --- | --- | --- | --- | --- |
| intro | 0–180 | 6.0s | 0 frames | brand | remotion |
| interface | 180–420 | 8.0s | 0 frames | react-ui | flute |
| object | 420–600 | 6.0s | 0 frames | object | anatomy → hyperframes |
| book | 600–780 | 6.0s | 0 frames | book-art | hyperframes → kokoro |
| outro | 780–900 | 4.0s | 0 frames | brand | remotion |

## Before production

- [ ] planned: Compare source claims, title, attribution and CTA against the named product source.
- [ ] planned: Identify actual authorised artwork, fonts, components and media; input kinds are not inspected files.
- [ ] planned: Check selected versions, installed guides/APIs, dependencies and licence eligibility.
- [ ] planned: Confirm resource availability, input rights and execution authority; allow_paid is not spending permission.

Cost/setup estimates are unavailable. This view does not enforce a spending, download or runtime budget.

## Scene 1: intro

Primary: remotion. Style: editorial; match: true (preference, not a quality guarantee).
Required source kind: brand. Language: en.
Explicit picture choice: remotion.

| Requirement | Provider | Evidence | Source key |
| --- | --- | --- | --- |
| typography | remotion | tested | remotion |
| video-export | remotion | tested | remotion |
| still-export | remotion | tested | remotion |

### Intended outputs and QA

**01-intro.mp4** — proposed scene export via remotion; codec/container must be verified.

- [ ] planned: Decode the complete encoded video; inspect dimensions, fps, duration/frame boundaries, codec and colour.
- [ ] planned: Inspect scene action, camera, crop, occlusion, title/CTA legibility at full and reduced size.
- [ ] planned: Inspect encoded transition/effect timing across adjacent frames; verify holds and seams.
- [ ] planned: If audio is present, inspect encoded sync, loudness, true peaks and human listening; otherwise confirm intentional silence.
- [ ] planned: Retain native and final export size/SHA-256 with QA evidence.
**01-intro-still.png** — remotion; proposed native still; verify the installed renderer supports this exact export.

- [ ] planned: Inspect this image independently: source identity/rights, decoded format/dimensions and crop.
- [ ] planned: Read all titles/labels/CTA at intended size and a reduced preview; inspect edges and clipping.
- [ ] planned: Record the image provenance, size and SHA-256 separately from video QA.

### Retained tool limits

- remotion: Explicit Chromium and 120s load allowance used for full film; cold default browser failed twice, later still passed. 3D/captions/extra transition packages are documented, not locally tested. Dev audit repair retained separately.

## Scene 2: interface

Primary: flute. Style: unspecified; match: false (preference, not a quality guarantee).
Required source kind: react-ui. Language: en.
Explicit picture choice: flute.

| Requirement | Provider | Evidence | Source key |
| --- | --- | --- | --- |
| camera-travel | flute | tested | flute |
| depth-of-field | flute | tested | flute |
| video-export | flute | tested | flute |

### Intended outputs and QA

**02-interface.mp4** — proposed scene export via flute; codec/container must be verified.

- [ ] planned: Decode the complete encoded video; inspect dimensions, fps, duration/frame boundaries, codec and colour.
- [ ] planned: Inspect scene action, camera, crop, occlusion, title/CTA legibility at full and reduced size.
- [ ] planned: Inspect encoded transition/effect timing across adjacent frames; verify holds and seams.
- [ ] planned: If audio is present, inspect encoded sync, loudness, true peaks and human listening; otherwise confirm intentional silence.
- [ ] planned: Retain native and final export size/SHA-256 with QA evidence.

### Retained tool limits

- flute: Browser-host CoqPi success does not establish packaged Electron or arbitrary React support. Keep real data and IPC outside demo. No Flute audio workflow was tested.

## Scene 3: object

Primary: anatomy. Style: unspecified; match: false (preference, not a quality guarantee).
Required source kind: object. Language: en.

| Requirement | Provider | Evidence | Source key |
| --- | --- | --- | --- |
| isometric-svg | anatomy | tested | anatomy |
| object-motion | anatomy | tested | anatomy |
| video-export | hyperframes | tested | hyperframes |

### Intended outputs and QA

**03-object.mp4** — proposed scene export via hyperframes; codec/container must be verified.

- [ ] planned: Decode the complete encoded video; inspect dimensions, fps, duration/frame boundaries, codec and colour.
- [ ] planned: Inspect scene action, camera, crop, occlusion, title/CTA legibility at full and reduced size.
- [ ] planned: Inspect encoded transition/effect timing across adjacent frames; verify holds and seams.
- [ ] planned: If audio is present, inspect encoded sync, loudness, true peaks and human listening; otherwise confirm intentional silence.
- [ ] planned: Retain native and final export size/SHA-256 with QA evidence.

### Retained tool limits

- anatomy: Local visual prototype only; combined sound QA failed. Beta 3D is not a calibrated physics simulator. Historical accuracy remains unverified.
- hyperframes: New VFX, captions, vertical/4K/cloud paths were not validated by our horizontal pilots. Media and animation timing must share the seekable timeline.
- hyperframes: Current docs note conflicts between capturing VFX chains and page-side shader transitions; test the combined layer, do not assume independent effects compose safely.

## Scene 4: book

Primary: hyperframes. Style: unspecified; match: false (preference, not a quality guarantee).
Required source kind: book-art. Language: en.
Explicit picture choice: hyperframes.

| Requirement | Provider | Evidence | Source key |
| --- | --- | --- | --- |
| video-export | hyperframes | tested | hyperframes |
| narration | kokoro | tested | kokoro |

### Intended outputs and QA

**04-book.mp4** — proposed scene export via hyperframes; codec/container must be verified.

- [ ] planned: Decode the complete encoded video; inspect dimensions, fps, duration/frame boundaries, codec and colour.
- [ ] planned: Inspect scene action, camera, crop, occlusion, title/CTA legibility at full and reduced size.
- [ ] planned: Inspect encoded transition/effect timing across adjacent frames; verify holds and seams.
- [ ] planned: If audio is present, inspect encoded sync, loudness, true peaks and human listening; otherwise confirm intentional silence.
- [ ] planned: Retain native and final export size/SHA-256 with QA evidence.
**04-book-narration.wav** — proposed synthetic speech via kokoro; singing is not implied.

- [ ] planned: Compare spoken copy with approved script/source claims; disclose synthetic speech as required by model terms.
- [ ] planned: Measure decoded speech duration/sample rate and placement; check clipping, pronunciation, pauses, stress and intonation.
- [ ] planned: Keep speech separate until the common mix; human listening remains required.

### Retained tool limits

- hyperframes: New VFX, captions, vertical/4K/cloud paths were not validated by our horizontal pilots. Media and animation timing must share the seekable timeline.
- hyperframes: Current docs note conflicts between capturing VFX chains and page-side shader transitions; test the combined layer, do not assume independent effects compose safely.
- kokoro: Local FR/EN tested; other documented languages require a voice/pronunciation and timing trial. No voice cloning tested.

## Scene 5: outro

Primary: remotion. Style: unspecified; match: false (preference, not a quality guarantee).
Required source kind: brand. Language: en.
Explicit picture choice: remotion.

| Requirement | Provider | Evidence | Source key |
| --- | --- | --- | --- |
| typography | remotion | tested | remotion |
| video-export | remotion | tested | remotion |

### Intended outputs and QA

**05-outro.mp4** — proposed scene export via remotion; codec/container must be verified.

- [ ] planned: Decode the complete encoded video; inspect dimensions, fps, duration/frame boundaries, codec and colour.
- [ ] planned: Inspect scene action, camera, crop, occlusion, title/CTA legibility at full and reduced size.
- [ ] planned: Inspect encoded transition/effect timing across adjacent frames; verify holds and seams.
- [ ] planned: If audio is present, inspect encoded sync, loudness, true peaks and human listening; otherwise confirm intentional silence.
- [ ] planned: Retain native and final export size/SHA-256 with QA evidence.

### Retained tool limits

- remotion: Explicit Chromium and 120s load allowance used for full film; cold default browser failed twice, later still passed. 3D/captions/extra transition packages are documented, not locally tested. Dev audit repair retained separately.

## Final assembly

Proposed owner: ffmpeg. New combinations require an integration test; component evidence does not qualify the chain.
Suggested final file: **final-video.mp4** (not yet created).

- [ ] planned: Normalise actual size/fps/colour/alpha and frame boundaries; inspect encoded seams and transitions.
- [ ] planned: Use one master audio timeline; declare trims, gains and source preservation before mixing.
- [ ] planned: For multiple stems, inspect relative alignment, polarity/phase and stereo/mono cancellation.
- [ ] planned: Decode final video/audio; check sync, loudness, true peaks, human listening and retain size/SHA-256.
- [ ] planned: Inspect each requested still independently; deliver only existing files under current authority.

## Handoff status

All QA above is planned or blocked. Human listening, creative acceptance and publication are separate decisions; none is inferred here.
This packet covers common export checks, not the complete tool/effect contract. Read references/handoff.md and selected recipes before execution.

Source keys resolve in references/tools.json; local evidence and scope live in references/catalog.json.
- anatomy: https\://github.com/wheresryan22/anatomy/blob/e6600ffc4e8e6620eeb45bf49bcdbd5e4b84163f/README.md
- flute: https\://github.com/webprodigies-org/flute/blob/4ab8c4a310ed051db9990e5a10a35fbcf2080cb1/README.md
- hyperframes: https\://hyperframes.heygen.com/concepts/compositions
- kokoro: https\://github.com/thewh1teagle/kokoro-onnx/blob/3596b26764286a7de9d90c363e988d50578918e5/README.md
- remotion: https\://www.remotion.dev/docs/
