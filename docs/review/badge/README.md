# T4 Badge: release procedure (KATA.md contract items 14–16)

CSS only, not interactive. The browser test found no defect, so only
meta.json changed (legacy `stable` → `beta`, per KATA.md item 16).

## Browser test (Chromium, headless)

`tests/badge-multi.html` (three preview sets, the third RTL, plus examples)
and `tests/test_badge_browser.py` (CI after Chromium installs):

| Badge | Light | Dark |
|---|---:|---:|
| Draft (neutral) | 7.22:1 | 5.81:1 |
| Live (asagi) | 5.66:1 | 8.27:1 |
| Needs action (red) | 5.57:1 | 7.26:1 |
| In review (yamabuki) | 5.26:1 | 8.65:1 |
| Pro (dark) | 17.72:1 | 16.12:1 |

Text contrast measured on 2x pixels for every badge on the page. In RTL the dot
sits at the inline start. With WCAG 1.4.12 text-spacing overrides (line height
1.5, letter spacing .12em, word spacing .16em) no badge clips its label.
0 console errors.

## Not verified

Screen readers (VoiceOver, NVDA), Safari and Firefox, browser minimum font
size settings (the badge height is fixed at 23px). Beta until a recorded
screen-reader pass. No visual change, so no images.
