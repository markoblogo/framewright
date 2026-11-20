# Framewright public landing

Public canonical address: https://markoblogo.github.io/framewright/ . English only.
Owner requested9November2026: minimalist black/silver identity, accepted responsive
FW intro, project explanation, animated evidence counters, current release, GitHub,
AMI-like video carousel and contact. No analytics or background update schedule.

## One source for the facts

- [Public profile](public-profile.json): editable project headline, description,
  capabilities and present/roadmap boundary. This is project documentation, consumed
  directly by the site; update it when the public description changes.
- [Public evidence manifest](public-evidence.json): count unique film and executed-trial cases.
- Router [catalogue](../skills/video-production-router/references/catalog.json): count `methods`.
- Detailed [tool profiles](../skills/video-production-router/references/tools.json): count `tools`.
- [Review ledger](../skills/video-production-router/references/review-ledger.json): count `tools`.
- GitHub releases API: newest non-draft release, including experimental prereleases.
  The9November observation was v0.8.0, published4November. Publication of experimental0.9.0 was verified14November; the visitor-loaded API supplies the actual newest release state. Experimental0.10.0 publication and anonymous release-feed/asset checks were verified17November;the feed returned v0.10.0 as its newest non-draft item. Browser display/layout was not re-tested for this data-only release. Documentation changes do not themselves publish a release.

The browser reads these public main-branch sources **once on each page opening**.
No visitor means no requests. It uses a dated shipped snapshot or last successful
local cache when GitHub is unavailable. Partial failures are labelled. There is no
timer, polling service or new automation. GitHub's normal HTTP caches still apply.

Initial checked values: **72 documented films,44 executed trial cases,10 router
methods,17 detailed tool profiles and139 tool-review entries**. Film stories are
deduplicated across formats/languages/revisions. Trials include failed and partial
attempts. This is a conservative documented set, not an asserted lifetime total. These are different units. Reviews include untested/blocked candidates;
they must never be described as139 qualified tools or independent experiments.
No lifetime-film total is claimed from the older42-export registry.

## Playlist and contact

Playlist: https://www.youtube.com/playlist?list=PLXX_Mo7C9ZvA .
The YouTube IFrame API reads the playlist on a visit when its section approaches
the viewport. Current API response provided50 IDs; that is the loaded set, not a
claim about the playlist's lifetime total. Previous/next previews and player use
those IDs. A dated six-film fallback and full-playlist link survive API failure.
New playlist additions require no site rebuild. Playback connects to YouTube.

The contact form opens an email draft to the owner-provided public address,
`a.biletskiy@gmail.com`. It explicitly says this, never pretends a message was sent,
and stores no enquiry. Automatic server-side email delivery is not configured.
It needs a mail application or the visitor can use the visible address directly.

## Source, deployment and QA

Canonical editable website checkout: external studio `sites/framewright/`.
GitHub Pages deployment checkout: `sites/framewright-pages/`; source is the public
repository's `gh-pages` branch. Pages is configured for that branch's root.
The Sites project is retained as the build/hosting route with its exact identity in
the checkout's `.openai/hosting.json`; never recreate the project when resuming.
No server, database, build framework or package installation is needed.

Browser QA9November: desktop1280px and mobile390×844, logo/intro, 16:9/9:16 source
selection, no mobile horizontal overflow, live counts, live50-ID playlist and next
selection. Input labels/types/required fields checked; no test email sent.
Portrait/readability and technical checks are not owner creative approval.
Future code changes need layout/interaction checks and source publication; updates
to the public data sources do not need a site rebuild.

## Keeping the public evidence index current

At production or trial closeout, add the completed/executed case ID and source to
`docs/public-evidence.json`. Do not enter a second row for another aspect, language
or revision. Check source links and the eligibility definition; do not add a plan
or infer success from execution. The site counts the entries on each visit, so no
website edit, hardcoded total or redeployment is required for catalogue updates.

## Social channels —16November2026

Owner-selected YouTube channel https://www.youtube.com/@ABV_Creative and TikTok profile https://www.tiktok.com/@lumierenoire.films appear as labelled, inline monochrome brand icons in both header and footer. Each target is44px; responsive header uses a separate navigation row on small screens. Desktop1280/mobile390 geometry and visible header/footer were checked with no horizontal overflow. Official Simple Icons vectors are embedded locally, with no extra runtime request. Both canonical GitHub Pages and the existing public Sites mirror were updated; Sites version3. Exact source/deployment hashes and screenshots remain in the private site-social-links-2026-11-16 record.


## 20November latest playlist and delivery checks

The carousel now initially selects the first valid entry of the live YouTube playlist instead of preserving a hardcoded older fallback film. The owner playlist is **newest-first**:20November public Atom timestamps and live IFrame IDs agreed on Robot meets CAPTCHA (`zZx5ZM5p59g`) first;74 IDs were loaded in that observation,not a lifetime-total claim. This ordering is an input contract:reordering the playlist changes which item is first;the site does not infer publication dates from video IDs. Keep the public playlist newest-first. No API key,proxy,server or polling schedule was added.

Initial selection updates on each fresh visit;deliberate previous/next/play choices survive a late playlist response. Invalid IDs retain native playback-index mapping. When YouTube is unavailable,a clearly dated six-film snapshot remains;freshness is not guaranteed offline. Newest-first selection,manual navigation and desktop/mobile no-overflow checks passed locally using the actual playlist. Public deployment status is retained in private records/delivery-site-2026-11-20/;a local test is not itself deployment proof.

The shared publication page is now template2.2:all platform downloads first,then YouTube copy and TikTok copy. [Smart validation procedure](../skills/video-production-router/references/preview.md) caches player regression across productions,with precise invalidation and per-package file/HTTP checks. Full cold and warm reuse were executed on copies of the already published CAPTCHA media;the warm run launched no browser and rejected an intentionally changed page. Original film masters were not modified. This routine UI regression is not a new film or generative-tool trial.


20November deployment proof:GitHub Pages commit`ee3a883f10e3fc191c3af141c2bd0241fb3df3f9`,native Pages build44767850214succeeded. Existing Sites mirror version4deployed successfully from source`1750875a3f5e8aa0b1f2432c37bc03ef101802ce`,with the same project and public audience. Anonymous public asset reads on both addresses match checked app.js/playlist.js bytes. No software tag/release or new schedule was created. The final delivery2.2sketch uses the same black/silver FW visual family and English UI;desktop/mobile geometry was checked,not a new creative film approval.


## Audience-led positioning —20November2026

Owner selected three audiences:creators/developers,AI platform/tool partners,and film/workflow clients. The minimal landing keeps its sections,FW identity and visual family. Its lead presents research-driven production and names Anton as the author:tools,styles and techniques are investigated together,with each production feeding documented learning into the next. Creative freedom across styles/toolsets is explicitly an ambition,not exhaustive coverage or universal production capability. The existing three capability rows explain films,real-production tool partnerships and team workflows;the primary paths are work and contact,with open-source methods in the method section and footer. No client result,exclusive market claim,partner endorsement or guaranteed review outcome is asserted. The README leads with this proposition,audience paths and source-linked films before setup/current technical evidence. See [public proposition](vision.md#public-proposition-and-audiences).

`public-profile.json` and the deployed snapshot share the selected copy. The browser selects the newer dated profile across the shipped snapshot,local cache and live main-branch source,so an older remote/cache response cannot undo deployed editorial changes. A newer live profile still applies;offline fallback remains dated. Desktop1280/mobile390 layout,old cache plus old live response,newer response and offline preservation were checked with screenshots. This is UI/behaviour QA,not an independent visitor-comprehension or conversion test. Private evidence:records/site-audiences-2026-11-20/.
