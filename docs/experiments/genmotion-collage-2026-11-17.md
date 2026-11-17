# GenMotion0.8.1 - newspaper collage trial

17November2026. Existing M4 arsenal-development direction; owner requested another Radar film with a changed style and queued-tool test. One executed trial for [The Mars Dispatch](../productions/nasa-eyes-collage.md), not a NASA science/app benchmark. Distinct from the skeletal-motion library with a similar name.

## Observed scope

Official [CLI documentation](https://genmotion.dev/docs/install-cli) and [haxzie source](https://github.com/haxzie/genmotion). Installed pinned @genmotion/cli0.8.1, Apache-2.0, Node22.14.0, macOS arm64. Tools, dependencies, caches, textures and outputs on Work. Existing headless Chrome and FFmpeg reused through explicit environment variables; automatic browser download disabled. No account, model weights or paid API.

Built original deterministic Three.js paper layers, photographic halftone texture, torn edges, text, moving keys, orbiting cutouts and rocket. Native landscape/portrait staging. First static compile passed with an explicit not-rendered warning; stills and actual video exports followed. A missing prepared PNG was caught and fixed before the final build. Reduced inspection led to separated text/credit areas and a proper NASA photographic print instead of an overly schematic planet.

Four-second24fps landscape proof: software125.041s, GPU34.296s; portrait GPU23.332s. These are CLI-reported local runs, not controlled comparative benchmarks; source revisions/caching/load differed. Full50s paper exports at12fps: landscape138.415s,portrait149.550s,one worker each, launched concurrently. A final correction moved landscape stamps below the source/credit, separated the scaled orbit heading from the masthead and moved the rocket away from closing text;full paper revision147.618s/157.267s. Portrait colour framing was shifted to retain the whole rover. Final24fps composites add24fps colour NASA footage and audio with FFmpeg. Paper12fps is a deliberate collage cadence and lower render load, not AI frame generation. Aspect/revision/retry variants count once.

## Limits and reuse

Useful candidate for authored 2.5D editorial layers, deterministic timing and local export on this host. It did not generate character acting, NASA terrain, source screen recordings, narration or scientific data. Colour source insertion and finishing are a separate local FFmpeg step. Fonts are host Georgia/Courier; no font binaries distributed. GPU/driver, Chromium and external storage behaviour must be rechecked on another machine; other stacks and operator transfer remain untested. Owner accepted both resulting films,sound and covers17November2026;owner supplied both publication URLs the same day,with independent visibility/identity/metrics unchecked. This acceptance does not qualify other tool uses.
