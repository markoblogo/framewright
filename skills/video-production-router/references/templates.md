# Accepted-film templates and content variants

A template is a renderer-independent design/data contract, prepared from an accepted
film and an explicit design specification. It does not reverse-engineer a video
into animation code. Use the accepted source project to author the specification;
its fixed styling is separated from editable text, numbers, picture and voice inputs.
The selected renderer consumes the resulting packet; adaptation/rendering remains
explicit. Guide inspiration: p.72; [source review](../../../docs/research/ai-editing-guide.md).

## Freeze the design

Start from [the example design](../../../examples/templates/design.json). It defines:

- Fixed canvas, frame rate, palette/type/layout data and renderer description.
- Typed content fields: text with length thresholds; bounded numbers; local image,
  video or audio media. Narration text and a narration recording can be separate fields.
- Scene timings and explicit bindings from scene slots to content fields.
- Layout alternatives for long text and missing optional media; optional audio can
  request silence, optional picture can request omission.

```sh
python3 skills/video-production-router/scripts/templates.py extract local/project.json output:accepted-film local/design.json --output local/template-v1.json
```

Extraction checks the actual source pin and a current creative-accepted journal
receipt for that exact video. A pending/rejected or stale effective creative review
blocks extraction. The immutable template records baseline provenance and acceptance
receipt, then registers a proposed template-design decision in the existing journal.
Film approval does not approve the new reusable design contract; its review stays
pending. Use a new template ID/file to change the design. No source media, credentials,
renderer code or old project's asset licences are copied into the template.

The baseline record is a historical snapshot at extraction. The project journal
tracks whether that dependency later changes. A portable template can still prepare
new packets outside the original computer; it never inherits baseline approvals or
publication clearance. Downstream projects must retain their own template revision.

## Provide new content

[Example values](../../../examples/templates/values.json) contain only declared
fields. Text cannot exceed `max_chars`; numbers must be finite, correctly typed and
within bounds. Unknown fields cannot override canvas/style. Local media values need:

```json
{"path":"assets/illustration.png","origin":"Owner-selected illustration",
 "rights_status":"unknown","rights_evidence":""}
```

Media paths resolve against the values file. The helper checks actual media kind and
records file hashes. Unknown/noncommercial-only terms remain publication blockers;
denied media is rejected. A supplied grant needs evidence text but is not independent
legal verification. Fixed fonts, code, music and new intended use still need the
normal project rights/preflight checks. Source-film acceptance grants none of these.

```sh
python3 skills/video-production-router/scripts/templates.py instantiate local/template-v1.json local/values.json --output local/variant-v1.json
```

The packet contains fixed style/canvas, resolved scene content and selected layout
hints. Long-text and missing-media choices are separate so they can apply together.
Fallbacks are explicit. Renderer, layout, creative and new-narration timing checks
remain unperformed/pending. A narration replacement can require retiming scenes;
the helper deliberately does not pretend fixed durations fit every reading.

## Prepare three boundary cases

```sh
python3 skills/video-production-router/scripts/templates.py check local/template-v1.json --values local/values.json --output local/template-checks-v1
```

This prepares short-text, maximum-length text and missing-optional-media packets.
Use actual baseline media in `--values` to exercise present/absent alternatives.
When no values file is supplied, examples seed text/numbers and optional media is
absent. Required media needs an explicit current file; otherwise preparation fails.
Outputs require new names and the pack appears only after all three validate.
Each case has a hash and a report distinguishing passed data validation from
unperformed rendering and pending visual review.

Render those three packets with the selected renderer before treating the template
as production-tested. Inspect reading time, wrapping, overlap, alignment, fallback
composition, audio and final encoded exports. Character counts do not measure pixel
fit; selecting an `expanded` hint does not implement a renderer's layout. Keep actual
render commands/source revision with the accepted design. Change the design only
through a new template revision and rerun affected cases.

## Handoff to another project

Transfer the template, chosen renderer's owned/cleared source, input contract,
three rendered controls when available, commands and known limits. Do not transfer
private account configuration or silently copy media rights. SSI or another producer
owns its data integration, scheduling and publication; Framewright prepares a local
contract and evidence. Each new variant receives its own source/fact, media, voice,
layout and final-export review through the existing production workflow.
