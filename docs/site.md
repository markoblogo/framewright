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
  The9November observation was v0.8.0, published4November. Source0.9.0 is now prepared under owner authority; the visitor-loaded API supplies actual publication state. This source edit does not itself prove release availability.

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
