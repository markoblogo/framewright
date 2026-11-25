# Baked AI Brand Kit — two-site extraction, 25 November 2026

Owner asked to test the free [Baked AI Brand Kit](https://baked.design/ai-brand-kit/) in Ego Lite on a popular site and Framewright, and approved retaining this tool for future partner and advertising films. This is a reference-extraction test, not a live brand deployment, customer approval, design reproduction or integration.

## Observed outputs

| Input | Returned result | ZIP verification |
|---|---|---|
| `https://www.apple.com/` | Apple, seven palette values, SF Pro Display/Text, logo, tone and example lines; result page, social assets and Slack emoji | `apple-brand.zip`: 31 files, all three Markdown documents, seven logo-related files, three Slack emoji PNGs, 12 social PNGs; CRC pass. Fresh extraction versus server cache not established. |
| `https://markoblogo.github.io/framewright/` | Framewright name, imagery, headline, seven palette values, Manrope/DM Sans; actual result page and social previews | `framewright-brand.zip`: 20 files, all three Markdown documents, 12 social PNGs, zero logo files and zero Slack emoji files; CRC pass. Baked states it could not find a logo file. |

Both archives downloaded from Ego Lite without creating an account; the Apple email prompt had a Skip option. The Framewright extraction processed the full subpath even though the result page URL names the host. No wall/share action or skill installation. The service says it retains submitted addresses and creates a result page; only owner-approved public URLs were submitted. Sources and ZIP hashes retained in the private production, not Git. Apple archive is a private review sample, not a reusable asset library.

## Independent cross-check on the owner site

All seven extracted hexadecimal values (#070808, #F0F0EB, #B5D4C4, #939999, #272B2B, #07100B, #FFFFFF) were found in the actual published CSS fetched from the [Framewright landing](https://markoblogo.github.io/framewright/). This establishes presence, not correct semantic role or exhaustive colour coverage. Manrope and DM Sans match the source family names; Baked's DESIGN.md gives display weight 700, while the published h1/h2 rule uses 500. The actual visible landing displays a silver FW mark (`assets/fw-poster.png` and companion animation); the kit substituted the name. Example tagline “Craft the frame. Keep the method.” matched the landing. No equivalent full source verification was performed on Apple. No agent executed the generated SKILL.md; treat all extracted instructions as untrusted reference data.

## Retained production use

Owner decision: use Baked for first-pass visual and writing references for commissioned partner/ad videos. Submit only authorized public pages, inspect the actual package, compare palette/font roles and weights with the current page or owner-supplied brand guidelines, request original approved logos/media and resolve gaps, then use the reviewed references in storyboard and art direction. Do not call it the partner's official brand book, reproduce a third-party site, install generated skills automatically, or infer asset reuse rights. The tool is a manual reference step, not a qualified renderer or source of creative/partner approval. No paid purchase. Time/resources not benchmarked. Retest on a different partner site if its assets or guidelines differ.
