# Publication copy for YouTube and TikTok

Framewright standard. Platform sources and connector access checked 22 November 2026.
Use with the [standard publication page](../skills/video-production-router/references/preview.md)
when a film reaches publication packaging. Keep the research and test notes in
the existing production record. The English copy fields on the page are for the
author to publish.

For account audits and publishing tools, see the [publishing and audit research](research/social-publishing-audit-2026-11-22.md).

## Research before writing

1. Define the viewer, language, market, format and payoff in one line. Choose a
   primary discovery path for each version: search, recommendations, or series
   navigation. Ground each claim in what the cut actually shows or proves.
2. Check one or two relevant queries if the evidence can change the wording.
   Use YouTube Studio Trends or public YouTube search for YouTube. Use TikTok
   Creator Search Insights where available, with native search as the fallback.
   Compare like formats and inspect a small number of current results. Record
   source, query, market and date. Search suggestions and existing titles show
   vocabulary. Label demand as unknown when no native or estimated demand
   measure is available. [YouTube Trends](https://support.google.com/youtube/answer/11962757)
   · [TikTok Creator Search Insights](https://newsroom.tiktok.com/creator-search-insights?lang=en)
3. Give the title, cover and opening a common promise. Let each contribute
   different information. For an explainer, lead with the concrete question or
   result. For a series, pair the viewer benefit with the mission identity.
   Keep tool claims, timings and numbers scoped to their evidence.

## YouTube

- **Titles** (`publication.titles`). Write a primary title and up to two distinct
  alternatives when useful. A search-led option names the subject or task in
  natural viewer language. A browse-led option makes the specific result,
  tension or surprise legible on its own. Move episode numbers and channel
  branding toward the end when the subject is the main reason to click.
- **Description** (`publication.description`). Open with one or two sentences
  that say who the film is for and what it delivers. Use the main phrase
  naturally near the start. Follow with useful details, checked chapters when
  they help navigation, primary sources and credits when relevant, and the
  verified links or series block. Shorts description and comment URLs are
  non-clickable. Use YouTube’s Related Video field where available for a
  clickable route from a Short. [YouTube title tips](https://support.google.com/youtube/answer/12340300)
  · [Description tips](https://support.google.com/youtube/answer/12948449)
  · [Link behaviour](https://support.google.com/youtube/answer/13748639)
- **Tags** (`publication.tags`). Use for useful aliases, spelling variants or
  disambiguation. Leave the field empty when it adds nothing. Search considers
  query match, engagement and quality. Recommendations also consider viewer
  response, including choosing to watch, staying and satisfaction.
  [YouTube Search](https://support.google.com/youtube/answer/16090438)
  · [Recommendations](https://support.google.com/youtube/answer/16559650)
  · [Video settings](https://support.google.com/youtube/answer/57404)

## TikTok

- **Caption** (`publication.caption`). Give the clip its own first sentence.
  Name the subject and the specific reason to watch. Use the target phrase
  where it reads naturally. Add relevant topic, niche or series hashtags only
  when they classify the clip. Keep the caption, in-video opening and cover
  consistent. For You prioritizes viewer interactions, including how people
  watch or skip. Search generally gives greater weight to content information
  such as query match. [TikTok recommendation factors](https://support.tiktok.com/en/using-tiktok/exploring-videos/how-tiktok-recommends-content)
  · [TikTok caption and hashtag guidance](https://newsroom.tiktok.com/5-tips-for-tiktok-creators?lang=en)
- **First comment** (`publication.first_comment`). Add useful context, a
  source, a viewing-order cue or a specific question if useful. A generic
  engagement prompt or repeated caption can be omitted. A profile-link call
  to action requires a verified destination. Treat pasted URLs as references
  until clickability is confirmed on the actual surface.
- **Series**. Keep the [RUN//SIGNAL link order](productions/run-signal-m01.md#episode-and-launch-promo-links).
  Put the viewer promise before the ordered links. The launch promo requires
  verified URLs for all three missions.

## Tools and open-source options

| Tool | Use in Framewright |
| --- | --- |
| YouTube Studio Trends and Reach, TikTok Creator Search Insights and native search | Default for wording and measurement. Record missing surfaces or data. |
| [Google Trends](https://newsinitiative.withgoogle.com/resources/trainings/advanced-google-trends/) with **YouTube Search** selected | Free comparison of relative interest for a fixed region and period. Its normalized index does not provide monthly search counts. |
| [TikTok Creative Center Trends](https://ads.tiktok.com/resources/help/article/how-to-use-trends) | Optional regional check for relevant hashtags or topics. Creative Center advertising keyword data describes ads. Keep it separate from organic search evidence. |
| vidIQ YouTube SEO and Packaging Studio skills | Reuse the workflow for audience, search phrasing, evidence and distinct title variants. The connector balance was zero at review. Charged keyword estimates and outlier searches are optional and outside the default route. |
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | Existing open-source CLI for small samples of public YouTube result titles and IDs. Read metadata only. Useful for vocabulary and packaging examples. Keep samples separate from demand and ranking measurements. Fall back to native search if extraction fails. |
| [Google API Python Client](https://github.com/googleapis/google-api-python-client) with [YouTube Data API](https://developers.google.com/youtube/data/reference/rest/v3/search/list) | Open-source client and official endpoint for a repeatable public-metadata sample if volume later justifies integration. Requires a configured Google project and quota. |
| [pytrends](https://github.com/GeneralMills/pytrends), [TikTok-Api](https://github.com/davidteather/TikTok-Api) and [TikTok Research API](https://developers.tiktok.com/products/research-api/) | Reference only. pytrends is archived. The unofficial TikTok wrapper depends on a web session and exposes no verified Creator Search Insights equivalent for this workflow. The official Research API requires qualified access. |

### Verified local sample

The existing studio yt-dlp 2026.10.26 returned three public IDs and titles for
`guided running for beginners` on 22 November 2026. The sample contained general
beginner advice and a follow-along interval run. Use this lightweight read to
spot differences in viewer intent. Verify the selected intent in native search.
From the studio root:

```sh
tools/python/media-acquisition/bin/yt-dlp --ignore-config --skip-download \
  --flat-playlist --print '%(id)s | %(title)s' 'ytsearch3:guided running for beginners'
```

## Check after publication

For YouTube, review impressions, CTR and retention or watch time by source
where available. Read actual Search terms separately from Home and Suggested.
For eligible videos, use the native A/B test when testing is warranted. Change
one dimension to isolate it and read the result by watch-time share. Record an
inconclusive result as such. [Reach reports](https://support.google.com/youtube/answer/9314355)
· [Native title and thumbnail tests](https://support.google.com/youtube/answer/16391400)

For TikTok, compare search exposure where available and watch time, completion
and shares across similar edits. Record the date, metric and traffic source.
A change in traffic, audience or edit can affect the result. Keep observations
from organic posts separate from controlled tests.
