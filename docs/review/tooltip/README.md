# T4 Tooltip: release procedure (KATA.md contract items 14–16)

CSS only (no JavaScript). There was no three-instance page before this pass.

## What changed

- **Accessible names (bug).** The tip is `::after` generated content. Chromium
  adds generated text to a button's accessible name, so the three sample
  buttons were named "Copy Copy link", "Settings Open settings" and "Save
  Nothing to save yet". meta.json claimed the tip "never replaces" the name.
  `content: attr(data-tip) / ""` gives the generated text empty alternative
  text (CSS Generated Content Level 3), so the names are now "Copy",
  "Settings" and "Save". The rendered tip is pixel-identical (light and dark,
  `before-after-*.png`).
- meta.json: the accessibility text now states what is implemented and what is
  not (below). Status stays beta.
- `tests/tooltip-multi.html` (three sets, the third RTL) and
  `tests/test_tooltip_browser.py` (CI after Chromium installs).

## Browser test (Chromium, headless, --k-mscale 0)

Accessible names of all nine triggers equal their visible text (the old CSS
fails here). The tip appears on keyboard focus and on hover for each trigger.
Tip text contrast inside the tip (2x pixels): 17.72:1 light, 16.12:1 dark,
for top and `data-side="bottom"` tips. 0 console errors.

## Known gap (owner decision)

WCAG 1.4.13 (content on hover or focus) asks that the tip can be dismissed
(Escape) without moving focus or the pointer, and that the pointer can move
onto the tip without it disappearing. Neither is possible in CSS alone: there
is a 7px gap between trigger and tip, and Escape needs a key handler. Meeting
1.4.13 needs a small tooltip.js, which changes the part's "Pure CSS, no JS"
description. This PR does not add it; the gap is recorded in meta.json and
HANDOFF for the owner to decide.

## Not verified

Screen readers (VoiceOver, NVDA), Safari and Firefox support for the
alternative-text syntax, touch devices (no hover).
