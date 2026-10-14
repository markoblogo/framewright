# Storyboard as a preparation layer

For a new multi-shot film, start with a shared visual direction and shot plan, then
select picture, voice/music and finishing tools per shot. Framewright's original
[adapter](../skills/video-production-router/references/storyboard.md) applies this
pattern before rendering. It does not impose a storyboard on comparisons, finishing,
recuts, an existing approved shot plan or a single-shot prompt.

## What we borrowed and changed

[AI Video Storyboard](https://github.com/aicontentskills/ai-video-storyboard-skill/tree/93f8a6d6935858bc4acd7ff3bbea2411edf88caa)
was inspected at `93f8a6d6935858bc4acd7ff3bbea2411edf88caa`. Its useful pattern is a
shared palette/light/motion language plus coordinated shot instructions and a
post-production checklist. README and SKILL declare MIT; no separate LICENSE file
exists at this inspected revision. The upstream checkout is retained on Work;
Framewright links and attributes it without vendoring its skill or examples.

The adaptation is tool-neutral and constraint-first:

| Upstream convention | Framewright contract |
| --- | --- |
| About five seconds per shot | Preserve requested cadence, master duration and exact frame boundaries; subtract transition overlaps |
| Cinematic 1080p with synchronized audio suffix | Preserve actual format and silence/audio constraints; a prompt cannot establish native audio support |
| Generate all shots, then edit | Reuse authorised assets and genuine UI; generate only where requested and authorised |
| General narrative proof slot | Use only source-backed claims; do not invent testimonials or results |
| One prompt style for all clips | Hand authored scenes, live React panels, book art and object prototypes to suitable tools |
| Referenced cinematography guides | Four listed references are absent upstream; do not pretend to have read them |

A plan identifies intended sources, per-shot tools, timing, audio and evidence gaps.
It records proposed versus approved state and retains rights, account, credit and
publication boundaries. The ordinary renderer preflight and final-file QA still
apply. Storyboard approval does not prove visual continuity, sound sync or an export.

## Text-only upstream trial

Four fresh Codex contexts exercised a six-shot editorial promo, silent square 4K,
a single-shot exclusion and an untrusted brief with zero spend. All completed with
unchanged fixture trees; observed commands were reads only. No video, audio, image,
account or provider action was performed.

The context-corrected strict score is **3/4**. The untrusted-brief answer preserved
facts, budget, rights and future QA but did not explicitly distinguish storyboard
approval before assembly. The adapter adds that state to its handoff. This is a
narrow missing handoff, not evidence that the tool cannot make useful shot plans.
[Raw trial packet](../benchmarks/storyboard/2026-10-14/raw/README.md).

Initial grading omitted the supplied source text and reported 0/4, mostly because
copy could not be verified. That grading input was incomplete: source text was
added and **all identical actor answers** were graded again. Initial grades remain
retained and excluded; no favourable per-case grades were selected. One other
criterion changed between the two passes, illustrating model-grader variance.

The source registry keeps these capabilities **documented**: its `tested` feature
labels refer to retained production artifacts, whereas this trial produces only
text plans. The earlier integrated adapter subset scored **4/4** within its retained 43/46
run. Protocol v3 subsequently passes the complete 52-case source check, including
those four adapter requests. This is development/regression evidence, not an
unseen transfer result. The integrated router/adaptation is evaluated in the
[planning report](router-evaluation.md); these results cannot qualify video quality,
provider compatibility, actual costs or automatic discovery.

## Example request

“Plan a 24-second square Framewright promo: four six-second shots, silent flat
monochrome diagrams. Use existing authorised text/assets, with no generation or
accounts. Give the continuity sheet, exact timing, tool per shot and QA handoff.”

Expected output is a text plan. No installation, image generation or rendering is
needed to review it. If the owner later asks to execute, the agent follows the
selected renderer's guide within the existing authorisation.
