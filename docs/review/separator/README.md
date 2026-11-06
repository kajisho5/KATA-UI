# Separator review (T4)

## Changes
- **The plain rule was 0px wide in grid and flex containers (bug).** The browser's default `<hr>` margin is `0.5em auto`; auto inline margins shrink a grid or flex item to its content, which is nothing. `.k-sep` now sets `margin-inline:0`.
  - The component preview (grid): 0px → 430px in `tests/separator-multi.html`.
  - Inbox template demo (`/templates/inbox/demo/`): 0px → 702px at a 1280px viewport.
  - App Shell, Settings, Pricing, Landing and Inbox pages keep the same widths (measured before and after; full-page screenshots identical except measurement noise also present between two runs of main).
- **Forced colors.** The vertical form and the lines beside the label were background fills; forced-colors mode replaces backgrounds with the page color, so they disappeared. They are now 1px borders (`border-inline-start`, `border-block-start`), which forced colors keep. Normal rendering is pixel-identical.
- `border-top` → `border-block-start`, `width`/`height` → `inline-size`/`block-size` (logical properties).
- `preview.html`: the vertical separators get `aria-hidden="true"`, matching meta.json.
- `meta.json`: accessibility text records the above.

## Evidence
- `tests/test_separator_browser.py` over `tests/separator-multi.html` (three sets, third `dir="rtl"`): every `hr.k-sep` matches its container's content width (main's CSS fails: `0 != 430`), 3 `separator` nodes, vertical separators aria-hidden, "OR" text ≥ 4.5:1 in light and dark, 0 console errors, and under forced colors each line is a 1px border in a color other than the page background.
- Screenshots: `before-after-light.png`, `before-after-dark.png` (the rule appears), `before-after-forced-light.png`, `before-after-forced-dark.png` (all three line kinds appear).

## Not verified
- Real Windows High Contrast; the forced-colors checks use Chromium's emulation.
- Screen readers, Safari and Firefox.
