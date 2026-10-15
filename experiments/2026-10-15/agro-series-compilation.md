# Agricultural library — compilation from seven delivered promos

Owner authorised the final series film after providing the landing tour's
[publication URL](https://youtu.be/RpxHRWhH4Yw),recorded as `user_provided_url`.
The brief is about the six books,the library and future additions;the ABVX
project/card page must not become the subject or CTA. No site source was changed.

## Planned acceptance before the first probe

Retain source identities and reject changed media;use footage from all six books
plus the landing tour;strip every old soundtrack;author one new English voice
and master mix. Test MoviePy with a4s720p cut/crossfade probe before the full film.
Target60s1920×1080/30,1800frames;inspect headlines,all scene handoffs and encoded
file/audio;retain a silent master,SRT,separate1280×720thumbnail and English YouTube
copy. Owner listening/artistic acceptance and publication remain separate.

## Tool decision and scope

Tested Python3.12.13 and FFmpeg8.0.1. New tool:[MoviePy2.2.1](https://zulko.github.io/moviepy/),MIT,isolated Python runtime
on the external media disk. Existing FFmpeg executable was selected explicitly;
no automatic binary download. Exact dependency versions are retained with the
[archived adapter](../../examples/moviepy-agro-series/README.md). This is a concrete
NLE task:subclips,animated multi-panel composition,chapter framing,half-second
picture dissolves,native poster/thumbnail,looped instrumental bed and timed voice
mixing. It is not a new generative video model.

[Editly](https://github.com/mifi/editly) was considered from the existing queue and
left deferred:its declarative editing overlaps this task,while its additional
native graphics dependencies were unnecessary here. No Editly install/runtime or
compatibility failure is claimed. ACE-Step was not run. The intervening OpenScreen
and MoviePy experiments do not remove its separate resource/diagnostic gate.

The first4s probe passed timing but used swapped target-resolution tuple values,
producing portrait output. Correcting this adapter call yielded1280×720/30,
120frames,full decode. This was an integration mistake,not a renderer defect.
Initial title rendering clipped this font's baseline;the adapter now uses measured
Pillow text bounds with MoviePy image layers. Final picture dissolves keep chapter
headings on a separate hard-switched overlay,avoiding doubled editorial titles.
These corrections were inspected;they do not establish general font compatibility.

## Source and timeline contract

Seven retained files were matched to prior SHA256 records before selection. All
VideoFileClip inputs use `audio=False`,including the two sources that contain old
narration. Six sources cover:Spot-Market Handbook EN,Agri-Commodity Brokerage EN,
Contract Execution Officer Handbook,MN7R Product Guide,and the two Ukrainian
editions. Landing footage is a seventh source. Existing baked text/art remains;
this is not a textless multilingual-master qualification.

| Chapter | Start | Duration before overlaps | Treatment |
| --- | --- | --- | --- |
| Work behind the deal | 0s | 6s | Six animated panels |
| Physical market | 5.5s | 7.5s | Spot-market3D footage |
| Brokerage | 12.5s | 7.5s | Trading-table footage |
| Execution | 19.5s | 7.5s | Dossier/action footage |
| Workspace | 26.5s | 7.5s | MN7R diagram footage |
| Two languages | 33.5s | 8.5s | Two Ukrainian films side by side |
| Explore the library | 41.5s | 10.5s | Two retained site-tour excerpts |
| More to come | 51.5s | 8.5s | Inspected library frame and new CTA |

Total63.5s minus seven0.5s overlaps =60s. Main chapter headings switch at overlap
midpoints;source baked text may dissolve with picture. Source timing is not
silently time-stretched. The final library card is deliberately held. Some new
narration bridges chapter changes;subtitle timings follow measured speech.

Supertonic3SDK1.3.1,F1 English,reuses the previously pinned model/config/style
manifest and newly synthesises eight lines. Code MIT;weights BigScienceOpenRAIL-M;
synthetic voice is disclosed. The original Contract Execution instrumental stem
is reused at0.18gain,looped/faded beneath narration. No old VO or new music generator.
New-script/final-film listening remains pending despite prior scoped F1 acceptance.

Claims about subject matter and EN/UK editions come from retained book/landing
records and inspected source frames. “More books are coming” is the owner's stated
plan,not a date/count promise. Formats vary by title;the copy does not claim that
every listed publication is free or has audio. No investment/financial outcome is
promised. Original media remains owner-authorised and absent from Git.

## Result and checks

[Output identities](outputs.json),[retained evidence](evidence/agro-series-compilation.txt).
Final local delivery includes narrated MP4,silent picture master,native dedicated
1280×720thumbnail,JPEG,SRT and English title/description/tags. The thumbnail combines
an authorised landing frame with original measured typography;it is not an
independently generated illustration or a frame pretending to be native still export.

Full decode,1800frames and60s1080p30;AAC48kHz stereo;120sampled half-second frames,
16scene samples and21transition samples inspected. Encoded loudness/peak and
master-versus-AAC sync/mono checks are recorded separately. The silent picture
contains no audio;final encoded picture stream matches it. Technical verification
does not establish pronunciation quality,artistic acceptance or audience response.
The native thumbnail was regenerated without an alpha mask and inspected at full
and320×180sizes. Final identities only;failed intermediate outputs are not qualified.

## Resource and reuse limits

Internal disk had867MiB free at preflight;external disk382GiB. No cleanup was
performed. New environment,package cache,temp files and media were kept externally;
CPU FFmpeg encodes used two threads,no new large model/GPU experiment. Python
wall timings and dependencies are retained;an OS peak-RSS timing command could not
read the sandboxed system clock and is not offered as a memory measurement.
Installation/correction time was not comprehensively measured,no comparative cost
or speed claim. No paid service was called;agent/provider costs are not calculated.

This qualifies a scoped manual MoviePy compilation recipe,not a new deterministic
planner provider or fresh independent router-model evaluation. Other codecs,
vertical versions,automatic semantic clip selection,ASR alignment,singing,new
fonts and clean-machine reproduction remain untested. Future edits need new
source/cut/audio/thumbnail checks. No release,public media upload or next trial
is triggered automatically. Owner supplied the [published film](https://youtu.be/vAPgNupIp2s). Publication provenance is `user_provided_url`;playback and uploaded bytes were not independently verified. Owner final-film listening/style review remains separate and pending.
