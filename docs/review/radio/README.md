# T4 Radio (`.k-radio`): release procedure (KATA.md contract items 11, 14–16)

Main base: `7bb190bbcdec88fe7940ef9a09eceebbb8db4afb` (after #49, Checkbox). No JavaScript.

## What changed

- **Boundary contrast (WCAG 1.4.11):** the unchecked border used
  `--k-border-strong` (1.65:1 light, 2.29:1 dark); it now uses `--k-ink-3`
  (4.83:1 / 5.6:1), as `.check` does since #49. `before-after-{light,dark}.png`.
- Hover darkens an unchecked circle; `aria-invalid="true"` draws the danger border.
- `tests/radio-multi.html` (three sets, set 3 RTL, per-set names, an invalid
  group) and `tests/test_radio_browser.py`, run in CI after Chromium installs.
  The contrast test fails on the old CSS.

## Browser test

Every input named by its wrapping label and every fieldset has a legend; ArrowDown
moves the selection with a focus ring and skips the disabled option; a disabled
option cannot be chosen; the invalid border differs; clicking a label chooses it;
set 2 does not change set 1; RTL direction in set 3; console clean. Contrast
(pixels at 2x, `--k-mscale 0`): boundary at least 3:1 and label at least 4.5:1 in
light and dark.

## Not verified

Screen readers, Safari, Firefox, real devices, 200% zoom. IME does not apply.
A sample pasted twice joins groups with the same name (documented in meta.json).
