# Music, songs and video: three directions

This is a planning and handoff guide, not a cloud integration. The optional
`scripts/music.py` helper makes no service calls, reads no referenced media and
never grants permission to upload, spend or publish. Suno and Flow Music profiles
are **documented**, not publicly qualified experiments. Private probes do not
promote the public catalogue. Use each service's authorised UI/download workflow;
no official public automation API is claimed here.

## Choose the timeline owner

| Direction | Freeze first | Work to perform | Acceptance check |
| --- | --- | --- | --- |
| brief-first | Story, audience, language, format and cue sheet | Decide instrumental bed versus foreground song; draft authorised lyrics if needed; generate/select audio, then measure it and build picture | Hook, actual duration, intelligible lyrics, closing cadence and picture support the brief |
| video-first | Approved picture version and its timecoded cues | Compose/select a bed to suit cuts and narration; trim/loop/crossfade with explicit edit decisions | Picture timing preserved; no accidental double soundtrack, masked speech or abrupt music cut |
| music-first | Approved audio version and trim | Mark sections/onsets, verify a beat grid manually if used; align supplied lyrics; build scenes around the track | Cuts follow the verified map; lyric timing checked by listening; no unapproved retiming of the song |

An onset candidate, waveform and true musical beat/downbeat are different things.
Do not advertise beat-synced editing from a waveform alone. Generated duration and
BPM in a prompt are requests, not measured properties. Keep the native original;
use an explicit excerpt/edit to meet a precise runtime.

## Instrumental, spoken voice and song are separate layers

Kokoro is the existing spoken narration route. It does not establish singing.
For a song, approve original/licensed lyrics, sung language, pronunciation, structure
and vocal character before generating. Do not imitate a named artist or upload
someone's voice without the needed authority. Keep voice, sung vocals, music and
SFX stems separate where exports permit; a stereo master is not a guaranteed stem
export. Prefer a music bed under product narration and a foreground song only when
its words serve the film. Review the actual singing, not just the submitted lyrics.

## Reuse a service's native video deliberately

| Asset class | Suitable reuse | What it does not establish |
| --- | --- | --- |
| Song/lyric card | Short lyric insert, social card, source preview | A directed multi-scene narrative or editable subtitle file |
| Animated cover loop | Opening, bridge, background, music visualiser | Full-length continuity, exact lyric timing or a complete music video |
| Generated scene/music-video export | Selected shot or full film after inspection | Arbitrary formats, usable cuts, audio sync or rights on every source |

Suno documents song video downloads and a separate cover-art generation feature;
paid availability of generated art differs from ordinary song-card download.
Uploaded looping cover art is another input workflow. Flow Music documents music
video generation; do not confuse it with Google's separate Flow filmmaking product
or Autodesk Flow Studio. Inspect the actual account/model/version before selecting
an output class; an unverified export remains unknown, and a failed attempt remains
a failure even when the underlying feature is documented.

Download through supported controls. Retain the native file, its classification,
source/version, dimensions/fps/audio/duration, size and hash. Preserve required
branding, watermarks and provenance. Crop/pad/scale intentionally; scaling creates
no detail. A vertical lyric card can be a bounded insert inside a landscape master.
Import compatible clips into Remotion/Hyperframes or finish with FFmpeg. A good
native clip need not force replacement of the rest of the chosen pipeline.

## Technical availability and usage rights are independent

Record four separate decisions: generation available, approved export available,
quality accepted, intended use permitted. A personal/noncommercial-only asset may
be technically usable for a private/noncommercial brief. It is not automatically
cleared for a product advertisement; absence of monetisation alone does not settle
whether promotion is commercial. Check current terms and the specific source and
download entitlement; a paid plan name alone is not evidence of an asset's rights.
Do not buy a plan or accept new terms as an implied part of planning.

Retain account-specific evidence privately: terms date, source/lyrics rights,
approved export receipt, generation/download quotas and actual debit if visible.
Unknown cost stays unknown. A generated or exported file is not publication approval.
Never publish private trials, prompts, lyrics or account records without permission.

## Offline helper

From a full checkout:

```sh
python3 skills/video-production-router/scripts/music.py examples/briefs/music-video-first.json
```

The standalone installed skill uses the same script relative to its folder. A
picture brief passed to `plan.py` can include this object under `music`; its picture
`status` covers picture requirements only. Inspect the independent music permission,
rights and native-visual fields before execution. `minimum_evidence`/`allow_paid` in
the picture planner do not qualify a cloud song or authorise its generation.
`visual_source` chooses `external-renderer`, `native-export` or `generated-scenes`;
for Suno the last maps to documented cover art, not a claim of a full narrative film.

Before delivery inspect decoded duration, dimensions, frame count, encoded sound,
seams, crop, loudness and true peaks. Listen to transitions and lyrics. Keep automated
QA, human acceptance and publication separate. Private probes may stay outside Git;
public qualification still requires distributable evidence under the contribution
protocol.

## Primary references (checked 2026-10-14)

- [Suno Custom/lyrics](https://help.suno.com/en/articles/2415873),
  [available files](https://help.suno.com/en/articles/13926081),
  [download changes](https://help.suno.com/en/articles/13614785).
- [Suno terms](https://suno.com/terms) and
  [cover-art improvements](https://suno.com/release-notes/cover-art-improvements).
- [Flow Music](https://www.flowmusic.app/?version=published),
  [plan features](https://www.flowmusic.app/pricing?plan=monthly),
  [privacy notice](https://www.flowmusic.app/privacynotice).

External claims describe available product documentation, not Framewright tests or
legal clearance. Recheck effective terms and account access at the next execution.
