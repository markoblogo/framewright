# Publishing and auditing YouTube and TikTok content

**Status: deferred by the owner on 22 November 2026.** Retain this research for
future planning. Resume evaluation when the owner selects it and recheck
platform rules and plan limits at that point.

Provider documentation reviewed 22 November 2026. This is a shortlist for
Framewright. Account access, available metrics and posting behavior have not
been tested. Keep using the [publication copy standard](../publication-copy.md)
and the existing production records.

## Publishing routes

| Route | Relevant capability | Framewright decision |
| --- | --- | --- |
| YouTube Studio and TikTok Studio | Native upload, scheduling where available and post management. Free account tools. | Baseline for both channels. Verify the account, platform fields, visibility, processing and public URL as separate events. [YouTube upload and scheduling](https://support.google.com/youtube/answer/57407) · [TikTok Studio](https://newsroom.tiktok.com/helping-creators-bring-creativity-to-life-with-tiktok-studio?lang=en) · [TikTok scheduler](https://ads.tiktok.com/business/en-US/blog/introducing-video-scheduler-now-you-can-plan-tiktoks-in-advance) |
| YouTube Data API and the open-source official Python client | Resumable upload, metadata edits and scheduled visibility. As of 2 November 2026, uploads from unverified API projects are no longer forced to Private. OAuth and the channel's current capabilities still apply. | First candidate for a small controlled own-channel integration. Test with an explicitly Private authorized fixture. Verify description, language, thumbnail, captions and playlist independently. [Revision history](https://developers.google.com/youtube/data/revision_history#november-2-2026) · [Upload](https://developers.google.com/youtube/data/reference/rest/v3/videos/insert) · [Python client](https://github.com/googleapis/google-api-python-client) |
| Metricool Free and its official MCP | Hosted, one brand, up to 20 planner posts/month, 30 days of analytics. Vendor documents YouTube and TikTok in the MCP and documents web scheduling for standard YouTube videos and TikTok. Access and field coverage through the connector require a live check. | First hosted candidate. Start with one existing video per platform and compare metrics with Studio. Check publishing fields, historical coverage and chart lag before adopting. [Free plan and MCP access](https://help.metricool.com/plans-add-ons-and-api-access-explained-xux1u) · [MCP FAQ](https://help.metricool.com/faqs-about-the-metricool-mcp-1i3w0) · [YouTube](https://help.metricool.com/schedule-and-publish-on-youtube-gof0k) · [TikTok](https://help.metricool.com/schedule-and-post-on-tiktok-bkepi) |
| Postiz self-hosted | AGPL-3.0 calendar, YouTube and TikTok providers, CLI/API, account and per-post metrics where supported. Its own documentation calls for platform app credentials in self-hosted setups. Vendor docs also describe limitations on data from before an account was connected. | Open-source reserve if a common calendar justifies deployment. Validate native-post history and platform fields before relying on it. [Source and license](https://github.com/gitroomhq/postiz-app) · [Provider settings](https://github.com/gitroomhq/postiz-docs/blob/main/self-host/configuration/reference.mdx) · [Analytics](https://github.com/gitroomhq/postiz-docs/blob/main/general/analytics.mdx) |
| Buffer Free and Mixpost | Buffer's documented free publishing scope includes TikTok and YouTube Shorts, with up to 10 queued posts per channel. Mixpost Lite lists Facebook Pages, Mastodon and X. YouTube and TikTok are in its commercial self-hosted offering. | Buffer is a short-form scheduling reserve. Mixpost stays in the reference list. [Buffer Publish](https://buffer.com/publish) · [Buffer plans](https://buffer.com/pricing) · [Mixpost source](https://github.com/inovector/mixpost) · [Mixpost self-hosted editions](https://mixpost.app/self-hosted) |

TikTok Direct Post restricts unaudited clients to private visibility, and its
intended-use guidelines exclude an internal utility that publishes solely to
accounts run by its own team. Self-hosting a scheduler does not grant a
different audit status. TikTok's Upload API can deliver a draft for the creator
to finish in TikTok. Availability depends on app and account access.
[TikTok Content Sharing Guidelines](https://developers.tiktok.com/docs/en/content-sharing-guidelines)
· [Content Posting API](https://developers.tiktok.com/products/content-posting-api/)

## Audit existing content

- **YouTube.** Start with Studio Advanced Mode exports and the video Reach and
  Engagement tabs. Use impressions, CTR, watch time, average view duration,
  retention and search terms where shown. Use the Analytics API for sanctioned
  repeatable reads of supported reports. Since 24 August 2026, public views
  across formats count play starts. Keep that measure distinct from engaged
  views and annotate date comparisons that cross the change.
  [Studio export](https://support.google.com/youtube/answer/9717005)
  · [Channel reports](https://developers.google.com/youtube/analytics/channel_reports)
  · [View-count definition](https://support.google.com/youtube/answer/12220281)
- **TikTok.** Use Studio for existing-post watch time, completion, traffic
  sources and search data where the account shows them. Use Display API for
  the public video inventory and counters it actually exposes, such as views,
  likes, shares and comments. The documented `video.manage` permission includes
  editing existing posts. This review did not establish endpoint availability,
  fields or approval for our account. Use native editing where available.
  [Studio](https://newsroom.tiktok.com/helping-creators-bring-creativity-to-life-with-tiktok-studio?lang=en)
  · [Display API fields](https://developers.tiktok.com/docs/en/tiktok-api-v2-video-object/)
  · [Scopes](https://developers.tiktok.com/docs/en/tiktok-api-scopes)
- **Local analysis.** Use CSV and Python or [DuckDB](https://duckdb.org/docs/stable/data/csv/overview)
  to join exports with the existing production registry by platform video ID.
  Keep account, format, age at measurement, date range and source with each
  row. Missing values remain unknown. Compare within platform and format.

## First bounded test after resumption

Start with 6–10 comparable published posts per platform in read-only mode.
Bring over metrics already visible in the native tools. Look for one decision
per candidate. On YouTube, above-baseline impressions and retention with
weaker CTR can justify testing a title or cover. On TikTok, a fast early drop
is a reason to inspect the hook, while strong viewing with weak search exposure
can justify a caption experiment. These are hypotheses and need a suitable
baseline. Keep any approved metadata changes small, record before and after,
and reread the actual post after saving. For API edits, read the full mutable
part first because YouTube's update method replaces fields in a supplied part.
[YouTube native title and thumbnail tests](https://support.google.com/youtube/answer/16391400)
· [YouTube metadata update](https://developers.google.com/youtube/data/reference/rest/v3/videos/update)

For the separate publishing test, exercise one approved asset per route
against the existing Framewright package. Verify account, metadata, cover,
subtitles, disclosure, schedule, upload status and URL. Keep a per-platform
record keyed by the video asset and confirmed platform ID before retrying.
A successful upload or draft receipt is separate from a confirmed public post.
