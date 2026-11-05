# T4 Switch: release procedure (KATA.md contract items 11, 14–16)

Main base: `1cdcbdf07e2bde4b44ff3ff6d0f11eff2d97953a` (after #50, Radio). No JavaScript.

## What changed

- **No accessible name (all samples).** The text sat outside `label.switch`
  (`<span class="switchrow"><label class="switch"><input>…</label>Text</span>`),
  so Chromium's accessibility tree gave every switch an empty name, and clicking
  the text did nothing. meta.json claimed both worked. Samples (Switch preview,
  examples, combos; Select and Tabs combos) now use
  `<label class="switchrow"><span class="switch"><input role="switch">…</span>Text</label>`.
  Class names are unchanged; `.switch` works on a span. Settings block, Settings
  Page and Landing put the text in another element, so their inputs get an
  `aria-label` from the row title; Pricing already had one.
- `role="switch"` on every switch, so screen readers announce on/off.
- **Boundary (WCAG 1.4.11).** The off track measured 1.48:1 (light) and 2.29:1
  (dark) against the page; the accent-on track 2.88:1 on white. A 1px outline
  (`--k-ink-3`, `--k-accent-ink` for the accent) keeps the edge at 3:1 or more.
  The default-on (ink) track looks unchanged. `before-after-{light,dark}.png`.
- Hover darkens the off rim; disabled is dimmed, not-allowed and does not toggle;
  the RTL knob rule also matches `:dir(rtl)`.
- `tests/switch-multi.html`, `tests/test_switch_browser.py` (CI after Chromium).

## Browser test

Accessibility tree: 15 switches with role switch and names Notifications,
Auto-save, Public, SSO (Scale plan), Login alerts per set. Clicking the text
toggles; Space toggles back with a focus ring; a disabled switch does not toggle;
the on knob sits at the inline end (left of centre in RTL). Edge contrast
(pixel just inside the track vs the page, 2x): 3:1 or more for off and accent-on
in light and dark; on the old CSS it fails (1.48, 2.88, 2.29).

## Checker gap (owner decision)

`accessible-label` passes any input that has a `<label>` ancestor, even one
with no text, which is how this shipped. Detecting empty labels is a checker
rule change; it needs owner approval and fixtures (KATA.md workflow).

## Not verified

Screen readers (how role=switch is announced), Safari, Firefox, real devices,
200% zoom. IME does not apply.
