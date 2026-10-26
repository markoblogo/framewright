# Prepare a recurring character and environment

These incomplete specifications are starting forms for later production, not approved
Good Dog assets or canon. Copy to a private project, fill them from owner-approved
references and retain actual files first. Keep null/empty fields until resolved.

- [Character draft](character-draft.json): images, scale/proportions, clothing,
  palette, material sources, rig, idle/walk/run actions and continuity constraints.
- [Environment draft](environment-draft.json): reference images, scale, layout,
  materials, lighting intent, spatial anchors and continuity constraints.

```sh
python3 skills/video-production-router/scripts/passports.py create local/project.json local/character-spec.json --output local/character-v1.json --actor operator
python3 skills/video-production-router/scripts/passports.py status local/project.json output:passport:future-hero:v1 --json
```

Creating the supplied draft succeeds as an **incomplete** definition. Real references
must be retained subjects, not external URLs or invented approval. Once complete and
actually reviewed, record owner acceptance under topic `passport-review` in the
existing journal. A new version uses a new output and optional `--supersedes`; old
shots remain bound to the old version until explicitly revised. `uses` lists bindings.

[Full contract and shot binding](../../skills/video-production-router/references/shots-and-passports.md).
No automatic visual-identity or rights verification, generation, paid call or publication.
