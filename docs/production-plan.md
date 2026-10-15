# Review a production plan

The production packet is a Markdown view of the offline planner's actual result.
It helps an operator review scene ownership, intended files and remaining work
before using external tools. Python 3 standard library only.

```sh
python3 skills/video-production-router/scripts/plan.py examples/briefs/mixed-promo.json --format markdown
# Save outside your source tree, or to a deliberate project handoff path:
python3 skills/video-production-router/scripts/plan.py examples/briefs/mixed-promo.json --format markdown > /tmp/production-plan.md
```

See [the structured brief](../examples/briefs/mixed-promo.json) and
[its generated packet](../examples/plans/mixed-promo.md). Omitting `--format`
preserves the JSON interface. The standalone skill ZIP includes the formatter;
it does not require this checkout's example/media directories.

## Read the result

- Timeline: frame boundaries, durations, overlaps and selected chains. Missing
  timing stays unknown; a proposed plan is not an executable rendered timeline.
- Scene evidence: providers, tested/documented capability, source keys, explicit
  choices, feature-test requirements and unmet requests. Style matches are preferences.
- Inputs: required source kinds, not inspected files or proven access/rights.
- Outputs: suggested unique filenames and common video/still/voice checks. A still
  identifies proposed native export or encoded-frame extraction; extraction also
  needs a verified intermediate video. Unsupported outputs remain blocked.
- Handoff: common picture/audio assembly, independent music gates if present,
  human listening and publication boundaries. No checkbox is verified by generation.

Files are suggestions only; a producer can rename them and retain the mapping.
A narration-only or still-only request does not get a fabricated final video.
Generated packets contain brief content and may reveal local references: review
before sharing. They contain no embedded media and do not upload anything.

## Limits

The packet covers common output QA. It is not an exhaustive checklist compiler:
read the selected recipe and the [full handoff contract](../skills/video-production-router/references/handoff.md)
for renderer/effect-specific checks, alpha, locked sources and native export details.
Planned checks need observed evidence before being marked verified by an operator.
The [project helper](../skills/video-production-router/references/projects.md)
can now persist this packet, manual step states and actual file pins. It does not
inspect/decode assets, detect runtimes or run production.

Selection/ranking is unchanged. Unknown top-level brief fields, including custom
budget objects, are not enforced by the existing planner. Only documented brief
fields affect routing; `allow_paid` is a capability filter, not a quote or permission.
Strict brief/resource validation is deferred by owner choice. No new model behaviour
qualification, provider integration or video experiment is claimed for this feature.
