# File Upload / Color Picker / Carousel

Main base: `20ca626109a755deb696ddc9c8c8847408f6f9b6`, after merged PRs #25, #27
and #28. After #27, these three are the first JS-failing parts in the HANDOFF T1
order. All three failed both JS rules and focus-visible.
Their release status stays **Beta**. No shared tokens or checker rules change.

| Audit | Before | After |
|---|---:|---:|
| Mold Verified | 103 / 164 | 106 / 164 |
| UI | 70 / 121 | 73 / 121 |
| Lab | 33 / 43 | 33 / 43 |
| js-single-instance findings | 12 | 7 |
| js-global-bindings findings | 31 | 18 |
| focus-visible findings | 119 | 112 |
| spacing-values / type-values (warn) | 891 / 638 | 891 / 638 |
| token-values | 0 | 0 |

## Source and behavior

Each script is an IIFE that initializes every root once (`data-kata-ready`),
checks generated IDs for collisions and keeps IDs the application supplied.
None of them registers a document or window listener. Existing classes and data
hooks (`data-upload`, `data-up-list`, `data-cp`, `data-cp-hex`, `data-cp-chip`,
`data-cp-custom`, `data-car-track`, `data-car-prev`, `data-car-next`,
`data-car-dot`) keep working; nothing is renamed.

- **File Upload.** The old sample hid the file input with `hidden`, so the
  keyboard could not reach it. The input is now visually hidden but focusable;
  the script also removes `hidden` from older markup. The zone shows the ring
  through `:has(input:focus-visible)`. In Chromium, Space on the input opens the
  native picker; Enter did not open it reliably, so the metadata only promises
  Space. Remove buttons are named `Remove <file name>`, and focus moves to the
  next remove button or back to the input. A `role=status` region announces
  additions and removals. `kata-file-upload-add` (detail.files) and
  `kata-file-upload-remove` (detail.name) bubble from the root. A drag-depth
  counter keeps child elements from flickering the zone's drag state; state
  never leaks to another zone. File names only use `textContent`. A new
  optional `data-rm-icon` lets created remove buttons use the sample's icon.
- **Color Picker.** Swatches stay `role=radio` buttons in a labelled
  radiogroup, with a roving tabindex (one tab stop). Arrow keys move and
  select: horizontal arrows follow visual direction, Up/Down move to previous/next,
  and Home/End jump to the ends. Selection keeps `--k-ring-offset`; keyboard
  focus on the selected swatch adds an outline outside it (KATA.md item 6).
  `kata-color-picker-change` fires only when the value changes. The custom
  native input previews on `input` and notifies once on `change`. There is no
  drag handle in this part, so the HANDOFF pointer-capture item does not apply.
- **Carousel.** The root is a labelled `role=group` with
  `aria-roledescription=carousel`, not a region: a region repeated by pasting
  the sample twice fails axe `landmark-unique`. Slides are groups named
  `n of N`. The track is a tab stop (this fixes axe
  `scrollable-region-focusable`); horizontal arrows follow visual direction,
  and Home/End jump. Index math measures from the track's inline-start edge, so
  RTL works. Previous/Next icons mirror in RTL. Smooth scrolling becomes
  instant with reduced motion or `--k-mscale: 0`. Dots update while scrolling,
  but the status text and `kata-carousel-change` wait until the scroll settles
  (`scrollend`, with a 150 ms fallback), so a jump does not report the slides
  it passes. There is no autoplay, so there is no pause control to add.

## Verification

```sh
node --check components/file-upload/file-upload.js
node --check components/color-picker/color-picker.js
node --check components/carousel/carousel.js
python3 check.py --json mold-results.json
python3 -m tools.verify_upload_color_carousel
python3 -m unittest discover -s tests -p 'test_*.py'
python3 -W error::SyntaxWarning build.py
python3 -m tools.mold_ratchet --report mold-results.json --reference-ref <main SHA>
python3 -m tools.verify_mold_distribution
python3 -m tools.mold_publish --check
NODE_PATH=<axe-core and playwright> node tools/check-browser.cjs file-upload color-picker carousel
```

`results.json` and the screenshots cover nine Chromium cases: three copies, one
RTL, the script loaded twice (then again), light with normal motion, dark with
a zero multiplier, and dark with reduced motion. Checks include independent
state, unique and preserved IDs, synthetic composition keys (keyCode 229),
body clicks, null-relatedTarget focusout and window blur, event counts, visual
arrow movement and XSS-safe file names. Console errors: zero. The browser audit
(`tools/check-browser.cjs`) reports 0 axe violations for File Upload and Color
Picker. Carousel goes from 2 to 1: `scrollable-region-focusable` is fixed, and
the remaining `heading-order` (`h4` slide titles) predates this change.

Real Japanese IME, screen readers, Firefox/Safari, mobile native file and color
pickers, and real drag and drop from the operating system are not verified.
Synthetic events do not replace device checks. No part is promoted to Stable.

## Remaining JS failures (6 targets)

In priority order: split-panel, reorder, follow-frame, blocks/pricing,
blocks/site-header, blocks/use-cases. Use Cases fails only global bindings; the
other five fail both JS rules.
