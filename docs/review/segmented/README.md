# T4 Segmented: release procedure (KATA.md contract items 14–16)

CSS only, native radios. There was no three-set page before this pass.

## What changed

- Hover: an unchecked segment darkens its text on hover (no hover state
  before). No other part file changed.
- meta.json: accessibility text states the measured contrast and that each
  group needs its own `name` (a sample pasted twice with the same names joins
  one radio group; the same note as Radio in #50).
- `tests/segmented-multi.html` (three sets with per-set names, the third RTL)
  and `tests/test_segmented_browser.py` (CI after Chromium installs).

## Browser test (Chromium, headless, --k-mscale 0)

Radiogroups Range/Density and radios Day/Week/Month/Comfort/Compact per set;
ArrowRight moves the selection within one group only; the focused segment
shows the ring; clicking a label selects it. 0 page errors.

Text contrast (2x pixels): selected 17.72:1 light / 16.12:1 dark; unchecked
6.55:1 / 5.81:1.

Screenshots: `before-after-hover-light.png`, `before-after-hover-dark.png`
(pointer on "Week"). The resting state is unchanged.

## Not verified

Screen readers (VoiceOver, NVDA), Safari and Firefox, touch devices. Beta until
a recorded screen-reader pass.
