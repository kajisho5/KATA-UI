# T4 Tabs: release procedure (KATA.md contract items 11, 12, 14–16)

## What changed

- **Panel text was in the script.** tabs.js held the three sample panel texts
  in a `PANES` array and wrote them into a single `[data-tabpane]`, so a pasted
  Tabs part always showed the sample text. Panels are now real markup: one
  `[data-tabpane]` per tab after the tab list, shown or hidden by the script.
  preview.html has three panes; the combo's card body is split into three
  panes (Email, Chat, Push).
- **No roles, no keyboard.** It was a row of buttons with a class. It now
  follows the WAI-ARIA APG tabs pattern with automatic activation: `tablist`,
  `tab` with `aria-selected`/`aria-controls`, `tabpanel` labelled by its tab,
  roving `tabindex`, ArrowLeft/ArrowRight (visual direction, so reversed in
  RTL, per KATA.md "Keyboard direction") with wrap, Home/End. A text-only
  panel takes `tabindex=0` so Tab reaches it.
- **Contract item 11.** IIFE, `data-kata-ready`, collision-checked IDs, no
  globals; one shared `ResizeObserver` keeps the thumb under the selected tab
  when fonts or widths change. A bubbling `kata-tabs-change` event reports
  user changes. The thumb is `aria-hidden`.
- tabs.css: `[data-tabpane][hidden]{display:none!important}` so a hidden
  panel stays hidden when the author sets `display` on it (the combo does).
- meta.json: `stable` → `beta`; usage and accessibility text describe the
  panel markup and implemented behaviour. Existing classes (`.tabs`, `.on`,
  `.thumb`, `.tabpane`) and data attributes are unchanged.
- `tests/tabs-multi.html` (three instances, the third RTL, plus the combo;
  script loaded twice) and `tests/test_tabs_browser.py` (CI after Chromium).

## Browser test (Chromium, headless, --k-mscale 0)

Four tab lists: roles, `aria-selected`, roving tabindex, panel links; arrows
follow the visual direction in RTL; wrap; Home/End; click; thumb under the
selected tab (within 1px); Tab moves into a text-only panel; combo panels
hidden despite inline `display:grid`. Unique IDs, 0 console errors. The old
tabs.js fails at the first check.

Tab text on the segment background (2x pixels): unselected 6.55:1 light /
5.81:1 dark, selected 17.72:1 / 16.12:1.

`before-after-{light,dark}.png`: preview and combo on load, old (left) and new
(right), pixel-identical.

## Not verified

Screen readers (VoiceOver, NVDA), Safari and Firefox, touch devices.
Beta until a recorded screen-reader pass.
