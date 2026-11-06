# Data Table review (T4)

## Changes
- **Clipped at narrow widths (bug).** `.k-dt` has `overflow:hidden` for its rounded corners, so a table wider than its container was cut off and could not be scrolled. At 360px on the built site: the preview table needs 381px in 292px, the combo 356px in 292px, the Dashboard demo 325px in 266px and the Dashboard listing preview 325px in 200px. The table now sits in `.k-dt-scroll` (`overflow-x:auto`), a named, focusable region (`role="region"`, `aria-label`, `tabindex="0"`), the same pattern as Table (#64). The footer stays outside the scroller.
  - Markup: `components/data-table/preview.html` ("Members"), `combos.html` ("The roster"), `templates/dashboard/preview.html` ("Recent orders"). The combo and Dashboard tables, which had no caption, also get a matching `aria-label` (the script used to fall back to "Data table").
  - `tests/data-table-multi.html` gets the same wrapper.
- Borders use logical properties (`border-block-start`/`-end`). `.k-dt-scroll:focus-visible` draws a 2px inset outline (`outline-offset:-2px`, as List and Split Panel do): an outer ring would be clipped by `.k-dt`. `tools.verify_focus_ring --check` reports 0 clipped and 0 below 3:1.
- `meta.json`: accessibility text records the scroll region.

New class: `.k-dt-scroll`. Existing classes and attributes are unchanged.

## Evidence
- `tests/test_data_table_browser.py` over `tests/data-table-multi.html` (three tables, third `dir="rtl"`, script loaded twice): regions "Members 1–3"; sorting one table sets `aria-sort="ascending"` on that header only; header text ≥ 4.5:1 in light and dark (4.51 / 4.71); at 360px the region scrolls with ArrowRight and the page does not scroll sideways; 0 console errors. With main's CSS the region does not scroll (`0 not greater than 0`).
- At 1280px the data-table page and both Dashboard pages render pixel-identical to main.
- Screenshots: `before-after-360-light.png`, `before-after-360-dark.png`.

## Not verified
- Touch swipe on real phones, screen readers (VoiceOver, NVDA), Safari and Firefox.
