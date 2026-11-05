# T4 Drawer: release procedure (KATA.md contract items 11–16)

The #24 instance work (IIFE, data-kata-ready, generated IDs, Tab cycling,
Escape/backdrop/close buttons, opener focus, inert when closed, IME guard) and
`tests/drawer-multi.html` already exist; `tools/verify_overlay_instances`
checks them in CI since #54.

## What changed

- **RTL placement.** The panel used physical `margin: 0 0 0 auto` and
  `inset: 0 0 0 auto`, so in an RTL page it still opened from the right. It now
  uses logical properties (`margin-inline-start`, `inset-inline-end`) and sits
  at the inline end: the right edge in LTR, the left edge in RTL.
- **RTL slide.** The entry animation moved from +36px; RTL now uses
  `kdrawer-in-rtl` from −36px. Reduced motion removes both (the RTL rule is
  more specific, so the reduce rule names it too).
- `tools/verify_overlay_instances.py`: the backdrop click now picks a point
  outside the panel (the left edge is the panel in RTL).
- `tests/test_drawer_browser.py` (CI after Chromium installs): panel at the
  right in LTR and the left in RTL (fails on the old CSS), RTL animation name,
  no animation under reduced motion, text contrast.

## Measured

Title 17.72:1 light / 16.12:1 dark; body 7.73:1 / 6.91:1 (2x pixels).
`before-after-rtl-{light,dark}.png`: RTL instance at 800px, old (left image:
panel on the right) and new (right image: panel on the left).

## Not verified

Screen readers (VoiceOver, NVDA), a real IME, Safari and Firefox, touch
devices and swipe-to-close (not implemented). Status stays beta until a
recorded screen-reader pass.
