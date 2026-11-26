# Landing SEO / AI-search baseline — 26 November 2026

Scope: owner requested basic SEO and LLMO improvements, followed by gradual work;
no redesign, paid service, analytics installation or ranking guarantee.

Canonical: https://markoblogo.github.io/framewright/ . Editable site:
`/Volumes/Work/Work/FramewrightStudio/sites/framewright/dist/`.

## Observed live baseline

Anonymous HTTP 200; live HTML matched the editable source before changes.
Canonical URL, English language, description, Open Graph image, semantic headings,
static service copy, Studio Notes and collaboration links already existed.
The title was a brand slogan; no JSON-LD, Twitter card, sitemap or text facts file.
No-script HTML advertised v0.8.0 and a 9 November catalogue despite a public v0.12.0.

`https://markoblogo.github.io/robots.txt` returned 404: this is no explicit crawler
block. The project-path `/framewright/robots.txt` returned 200 but cannot control
host-wide crawling; do not present it as an effective robots policy. Changing the
host root is outside this project. No training-bot policy was changed.

## Prepared changes

- Descriptive title and metadata; canonical preserved; social URL/image/card data.
- Person, Organization, WebSite and WebPage JSON-LD tied to visible, sourced facts.
  No invented ratings, prices, clients or search eligibility claims.
- Static studio identity, concise visible about/licensing/scope answers, and direct
  film + production-case links, available without JavaScript. Keep the slogan.
- Updated static snapshot from published public main and releases API:
  165 films,119 executed trial cases,10 methods,17 profiles,207 review entries;
  v0.12.0 experimental. Not lifetime totals or qualified-tool counts. Unpublished
  local production records were deliberately excluded from these counts.
- One canonical-URL sitemap and optional linked `llms.txt` factual summary.
  The latter is an aid for tools that choose to read it, not a search standard.
- Hide the introductory overlay without JavaScript so the content remains usable.

Private before files, checks and screenshots:
`records/site-seo-2026-11-26/`. Source changes are local pending website publication;
local checks do not establish live deployment or indexing.
Final local browser result: PASS, all six viewport/JavaScript combinations.

## Verification and limits

Site playlist regression: 5 passed. Repository structural validation passed.
Browser checks cover desktop1280/mobile390/narrow320, JavaScript on/off, metadata,
JSON-LD parsing, fragment targets, release fallback, no horizontal overflow and
no script errors; inspect retained browser-check.json for the final result.
Sitemap XML parses; share image is1280×720.

GSC Wizard refused read-only property discovery with payment_required; no repeat
or purchase. Impressions, clicks, indexing and assistant citations remain UNKNOWN.
No Search Console submission, account changes or analytics added.

Primary guidance:
- https://developers.google.com/search/docs/appearance/ai-features
- https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics

Foundational SEO and accessible useful text matter for AI search too; there is
no required special AI schema or file. Validate live file identity after publishing.
Review the optional facts summary with future positioning changes; update shipped
HTML/snapshot as well as public-profile.json. Preserve the three confirmed brands.
Later optional pass: Search Console baseline through existing free access/export,
sharing-preview design, performance measurement and richer source-linked cases.
