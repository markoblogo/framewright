# SSI: one brand profile across three report films

25 October 2026. Local production and product trial; new exports are not publication
or partner acceptance receipts.

The owner supplied two SPIKE Brokers decks and a three-part weekly report. Partners
preferred a presentation-led report with main figures and narration over the older
illustrated transport experiments. They accepted the enlarged Part I visual style,
then requested removal of background music and about two additional seconds before
slide changes. Approval is owner-reported. Revised audio/pacing and Parts II/III still
need their own review.

## Reusable profile

The new local `branding.py` helper freezes manually selected source files/assets,
palette, typography, layout and motion. The trial reuses the supplied original
SPIKE logo, Commissioner font, white/black/grey, lime and orange accents. It exports
renderer-neutral CSS variables and original assets with a hash-bound origin record.
All three productions use the same profile, CSS and logo hashes. Report values,
voice and shot timing remain production content. No 2024 deck statistics are reused.

Source changes block a new export; existing output folders are not overwritten.
Unknown/noncommercial-only rights stay blockers, denied assets are refused. No
file is fetched, model called, renderer run, film accepted or upload authorized by
the helper. Export metadata replaces local source paths with filenames; supplied
origin prose must still be checked before sharing. Native CSS URLs need the selected
renderer’s normal asset-root adaptation.

Six public-CLI tests passed: same profile across independent bundles, changed files,
profile tampering, unsafe/invalid tokens/layout, and unresolved/denied rights. The
profile does not bypass the existing accepted-film template gate. These are file/
contract tests, not evidence of universal brand extraction or arbitrary PPTX reuse.

## Production trial

One adapter uses the profile for 5 logistics, 7 grain and 10 oilseed slides. The same
brand is applied to short numbers, longer unit/table labels and a real website
ending. A long rapeseed heading initially collided with its number block and was
shortened while preserving its meaning. Automated checking was supplemented by
viewing settled frames; a passing layout report alone was insufficient in the
first logistics draft.

Delivered: 40.0 / 56.6 / 79.4 seconds, 1080×1920 / 30 fps,English commentary only. Information
slots are 7.6 seconds. Measured speech-to-cut holds are at least 2.08 / 3.94 / 2.36 seconds.
The initial 30-second demo ceiling was superseded by the owner’s readability request.
Voice/music separation made it possible to remove music without reconstructing the
approved visual design. Local Supertonic3 provided speech; no voice cloning or audio
cloud upload. Partners may add their own licensed platform music after delivery.

Parts II/III include a 3.4-second actual English homepage scroll. The first browser video
had grey padding and was rejected; frame-based page screenshots corrected the
capture. This is real interface imagery with a selected scroll, not a fake UI.

Source report dates/bases remain explicit. Grain futures, delivery bases and
lagged export-sales weeks are distinct; Danube road arrivals are not seaborne
shipments. Source market truth was not independently audited. The workflow is not
yet a deployed weekly-report generator and does not connect to SSI data or Telegram.

[Brand profile contract](../../skills/video-production-router/references/branding.md)


## Delivery and closeout

The owner sent all three revised voice-only masters to the partner. Further
comments and publication links are pending. The owner considers the revised pace
too slow but preserved the partner's requested reading holds; this is not a partner
rejection. No further redesign or recurring automation starts while feedback is pending.

[Final hashes, decode reports and feedback status](../../experiments/2026-10-25/evidence/ssi-brand-series.json)
retain the same profile/CSS/logo across all three bundles. Closeout checked the
bundle bytes independently. The two original deck paths are now unavailable, so
a fresh export from the private profile correctly stays blocked. Restore matching
references or freeze a deliberate new revision; do not silently repin the old one.
The delivered bundles and film hashes remain intact.

Audit found that `settled_hold_seconds`, already present in the retained SSI
profile and documented contract, was rejected by the helper. A public-CLI regression
failed before the fix and passes afterward; zero-to-ten-second holds now validate
and export to CSS. Other unknown fields and invalid values remain rejected.
