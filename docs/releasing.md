# Release the methods library

Use the version in `VERSION`; update CHANGELOG and run tests, record/link validation,
tool-matrix drift check and standalone package smoke check. No video rendering or
provider calls are release prerequisites for a documentation/selection-only update.
Keep router evaluation labels honest. Publish the archive and SHA256SUMS as an
experimental GitHub prerelease, tag the reviewed merge commit and verify its target.

```sh
python3 -m unittest discover -s tests -q
python3 scripts/validate.py
python3 scripts/render_tool_reference.py --check
python3 scripts/build_release.py --output /absolute/path/outside-the-checkout
```

The ZIP is a standalone router skill, not the entire source example or a renderer.
The tagged repository includes the open reference project. Do not overwrite existing
skills during installation: review and back up local changes before replacing them.
