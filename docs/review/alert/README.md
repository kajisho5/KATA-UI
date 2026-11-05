# T4 Alert: release procedure (KATA.md contract items 14–16)

CSS only. There was no three-set page before this pass.

## What changed

- **Unnamed images.** Each tone icon was an `<svg>` without a name or
  `aria-hidden`, so Chromium exposed four unnamed "image" nodes in the preview
  (and one in the Settings Page template). The title already states the tone,
  so the icons are decorative: they now carry `aria-hidden="true"`.
- **Danger tone shown.** alert.css styles `data-tone="danger"`, but the preview
  showed only info, success and warning. A danger example is added
  (`before-after-{light,dark}.png`).
- meta.json: accessibility text states the icon handling and measured contrast.
- `tests/alert-multi.html` (three sets, the third RTL) and
  `tests/test_alert_browser.py` (CI after Chromium installs).

## Browser test (Chromium, headless)

No unhidden image nodes (the old markup fails with four per set); in RTL the
icon sits at the inline start; 0 console errors.

| Tone | Title light / dark | Body light / dark | Icon light / dark |
|---|---:|---:|---:|
| info | 16.42 / 14.56 | 7.16 / 6.24 | 5.66 / 8.27 |
| success | 16.22 / 13.92 | 7.08 / 5.97 | 4.52 / 3.10 |
| warning | 16.49 / 12.68 | 7.19 / 5.44 | 5.26 / 8.65 |
| danger | 15.77 / 15.64 | 6.88 / 6.71 | 5.57 / 7.26 |

(2x pixels; the test asserts 4.5:1 for text and 3:1 for the icon.) The dark
success icon is the lowest pair at 3.10:1.

## Not verified

Screen readers (VoiceOver, NVDA), Safari and Firefox, touch devices. Beta until
a recorded screen-reader pass.
