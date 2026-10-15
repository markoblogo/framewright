# AMI Books — real-site tour with OpenScreen

Owner asked for the agricultural library landing promo before a later compilation
of the six delivered book films and this landing film. Sources inspected live:
[books.1d3x.com](https://books.1d3x.com/) and the owner-supplied
[project card](https://abvx.xyz/work/ami-books-physical-commodity-markets).
The card link was supplied as context;only the library and two book detail pages
were inspected for this film's claims. No website source was changed.

## Predeclared acceptance and actual result

Before the capture/export probe,the retained local plan required one public window,
no mic/system audio/camera,a bounded8s capture/export probe,real scrolling and two
book-page visits,readable horizontal1080p30 output,voice alignment/full decode,
separate thumbnail inspection and reusable silent picture. Owner review remains
separate. The initial40s target became42s to leave room for six voice lines.

The probe captured and exported successfully. The initial longer fullscreen take
instead became a304×324 miniature despite exit0. The ordinary-window take retained
usable hero,scroll,product catalogue,brokerage navigation and Contract page frames,
but later collapsed/black frames were rejected. A short closing take also failed.
The final edit uses verified portions only:the Contract page is0.4s of inspected
footage held for another7.6s,with manual zoom. The Ukrainian section was inspected
live but its attempted capture is not used;that factual language callout appears
over reused hero footage. This is an edited guided tour,not an uninterrupted
whole-site walkthrough or a successful continuous Ukrainian-section capture.

## Exact scope and tools

- OpenScreen2.0.0 AppleSilicon official release,source
  [`eff86dcba48fac490a0e153141bf8537df7ffc54`](https://github.com/getopenscreen/openscreen/tree/eff86dcba48fac490a0e153141bf8537df7ffc54),MIT.
  Installer ZIP SHA256:`f257d63c55d229d4e8eb0511e546b7c8e16b80cc4d47b835df8396b75736db51`.
  App signature verified. CLI `record`,`pack`,`export`;manual project zooms,
  annotations,crop and16:9 composition exercised. The
  [upstream agent guide](https://github.com/getopenscreen/openscreen/blob/main/skills/openscreen-demo/SKILL.md)
  described MCP absent from this release's help;the pilot adapted the
  [official CLI](https://github.com/getopenscreen/openscreen/blob/eff86dcba48fac490a0e153141bf8537df7ffc54/website/docs/cli.md).
- Chrome live public page,driven through computer-use. One selected window only.
  Raw useful capture2498×1800;browser chrome cropped at y356,retaining2498×1444.
- FFmpeg:source selection,crop,freeze,assembly;native60fps export converted to30fps;
  external narration normalisation and final stream-copy mux. No new music generator.
- Supertonic3 SDK1.3.1,F1 English;existing pinned model/config/style manifest and
  six newly synthesised lines. Original helper reused;code MIT,weights
  BigScienceOpenRAIL-M. Prior F1 acceptance does not approve this new script/film.

The site FAQ says most AMI Team editions are free;commercial Amazon titles are
marked. Audio/M4B exists for selected books. VO/copy avoids “every book is free”
and universal format claims. No files were downloaded by clicking format buttons.
Author book art is not redistributed;linked external publications have separate rights.

## Retained outputs and QA

[Machine-readable evidence](evidence/ami-books-openscreen.txt) and
[output identities](outputs.json);[original authoring adapter](../../examples/openscreen-ami-books/README.md).
Final42s H264,1920×1080,30fps,1260frames;AAC48kHz stereo. Full decode passed.
Encoded loudness−16.06LUFS,true peak−1.69dBTP. Six voice lines fit without overlap;
raw generation rejected clipping and checked every WAV hash before assembly.
Picture and final encoded video stream hashes match.84half-second samples passed
a dark-raster guard;12scene/cut/zoom samples were inspected visually,including the
previously bad Contract frame. This is sampled inspection,not continuous semantic
video understanding or an independent ASR/listening pass.

PNG thumbnail1280×720 RGB is a frame from the inspected screen assembly before
OpenScreen's outer framing;full and320×180 views inspected. Native MP4 was60fps,
not a native30fps capability. Native/final/PNG have separate validated identities.
Silent30fps master,source segments,scene map,narration WAV,SRT and English YouTube
copy remain local;the evidence retains their identities where recorded.

## Limits and next action

Internal free space was1.7GiB at preflight;external Work had382GiB. App and delivery
were placed externally,but released CLI recordings still used app-data storage,
then `pack` copied them externally. No cleanup/deletion claimed. A future run must
check that actual recording/cache destination,not only the project path.
Accessibility was not trusted in the first probe;automatic click tracking/zoom is
not qualified. Manual native zooms were used. AI provider features,MCP,other OSes,
foreground/capture-boundary reliability and clean-machine reproduction remain open.
No claim of independent router-model evaluation or automatic provider integration.
The catalogue adds a scoped manual recipe;the deterministic planner is unchanged.

Owner final-film listening/style review remains separate. Owner supplied the published URL
[YouTube](https://youtu.be/RpxHRWhH4Yw);provenance is `user_provided_url`,not an independently matched playback. Later compile
from silent masters,replace narration on one master timeline,inspect seams/claims
and revalidate the resulting film. Compilation is not started here. ACE-Step stays
deferred until at least two intervening completed experiments and a changed resource
preflight;this tour alone does not clear that gate. No release/tag or public upload.
