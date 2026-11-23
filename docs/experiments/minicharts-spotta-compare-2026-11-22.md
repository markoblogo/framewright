# Minicharts vs GiveMotion on the Spotta stat card

22 November 2026. An internal silent comparison on the same data as the
[accepted Spotta film](../productions/spotta-bed-pod.md). The earlier estimate is
about 50%. During the first-year company study, guests were first to report 4
of 120 known cases (3.3%). This measures the share of known cases and is not a
bed bug incidence rate.

[Spotta company report](https://blog.spotta.co/hubfs/Spotta%20Bed%20Pod%20One%20Year%20In%20white%20paper.pdf)
· [Minicharts developer](https://april-zhu.com/minicharts)
· [GiveMotion control and original data revision](givemotion-spotta-chart-2026-11-21.md)

## What ran

- Kept both retained GiveMotion 0.1.6 exports as controls. Used the November 18
  MIT Minicharts archive already retained for the AllWeb3 case. Its native
  builder and engine made the SVG with two data marks and interactive parts.
  A local Chromium/FFmpeg adapter provided timed entry, film layout and MP4.
- Both routes produced silent 6.4-second clips at 30 fps in 960×540 and
  540×960. All four MP4s fully decoded, 192 frames each. The two Minicharts bar
  heights share a baseline and a linear 0–100 scale.
- The two JSON inputs differ only in the qualifier field. At 3.5 seconds,
  changing the qualifier to the explicit denominator changed pixels only
  inside the text bounding box in landscape. In portrait, two pixels
  outside that box differed by one channel value. Chart geometry and timing
  were unchanged.
- The illustrated room tags take more custom layout work than GiveMotion's
  reusable chart. The Minicharts card names bed bugs explicitly in the title,
  so the comparison is editorial as well as technical. It does not isolate a
  causal advantage from the engine alone. Capture and encoding took 7.23 s
  and 7.80 s on the existing Mac. GiveMotion's earlier CLI logs were 7.3 s
  and 7.4 s. Setup, active authoring time and cache were not matched.

## Owner review

Both treatments read quickly in the owner's review. Landscape and portrait
communicate the same information, with no material comprehension difference
between aspect ratios observed by the owner. The Minicharts treatment with
illustrated room cards read faster to the owner, who initially read the cards
as phones. Both treatments were rated positively. No timing or audience test
was performed.

Keep GiveMotion as the default. Keep Minicharts as a local reserve for
subject-specific illustrated charts with authored motion. This proves the
adapted export path for one card. No new paid calls or native Minicharts MP4
export were involved. Private recipe and proofs are under
`productions/spotta-bed-pod-2026-11-21/minicharts-comparison/`.
