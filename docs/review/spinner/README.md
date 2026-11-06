# Spinner review (T4)

No source change. The component already meets the checks below; this adds regression tests.

## Evidence
`tests/test_spinner_browser.py` over `tests/spinner-multi.html` (three sets, third `dir="rtl"`):
- 9 `status` nodes named "Loading"; the 3 disabled buttons are named "Saving…" (the inner spinner adds no text).
- Rendered outer sizes 18 / 22 / 32px (content-box: 14/18/26px plus the 2px/2px/3px ring) and 18px inside the button.
- The button with a spinner has the same height as the same button without it (38px for `btn-md`; `btn-sm` measured 32px both ways).
- Moving edge (`--k-ink`) against the page: 17.72:1 light, 16.12:1 dark (WCAG 1.4.11 needs 3:1). Track against page: 1.27 / 1.70; the track is not the activity signal.
- `k-spin` runs by default and stops under `prefers-reduced-motion`; 0 console errors.

## Not verified
- Screen readers: an empty `role="status"` with `aria-label` may not be announced when it appears; meta.json already says to pair it with text.
- Windows High Contrast / forced colors: in Chromium forced-colors emulation the edge and the track both compute to `rgb(0, 0, 0)`, so the ring shows no moving edge. Real Windows was not tested. No part in the repo handles forced colors yet; left for a separate decision.
- Safari and Firefox.
