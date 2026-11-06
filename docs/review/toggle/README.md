# T4 Toggle: release procedure (KATA.md contract items 5, 11, 14–16)

## What changed

- **Double load undid every click (bug).** toggle.js bound a click listener
  per button without a guard. With the script on a page twice, each click
  flipped `aria-pressed` twice, so nothing changed. It is now an IIFE with
  `data-kata-ready`; one click flips once. A bubbling `kata-toggle-change`
  event reports `detail.pressed`.
- **Names.** The formatting toggles were named "B", "I" and "U"; they now carry
  `aria-label` Bold, Italic and Underline.
- **States (item 5).** Added `:active` (unpressed and pressed) and `:disabled`
  (dimmed, not-allowed); hover skips disabled buttons.
- meta.json: accessibility text updated.
- `tests/toggle-multi.html` (three sets, the third RTL, script loaded twice)
  and `tests/test_toggle_browser.py` (CI after Chromium installs). The old
  script fails it.

## Measured

Text contrast (2x pixels, `tools.verify_button.text_contrast`): pressed Bold
17.72:1 light / 16.12:1 dark; unpressed Italic 7.73:1 / 6.91:1. The double
load, disabled and name checks pass; 0 page errors.

## Not verified

Screen readers (VoiceOver, NVDA) announcing pressed state, Safari and
Firefox, touch devices. Status stays beta. No visual change except the new
active and disabled styles.
