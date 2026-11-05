# T4 Checkbox / Radio (`.check`): release procedure (KATA.md contract items 11, 14–16)

Main base: `450c0fd8aa9288998079c3fe97b85f3f1e7f81f0` (after #48, Select). No JavaScript.

## What changed

- **Boundary contrast (WCAG 1.4.11).** The unchecked border used
  `--k-border-strong`: 1.65:1 on white and 2.29:1 on the dark page, below the 3:1
  a control boundary needs. It now uses `--k-ink-3`: 4.83:1 (light), 5.6:1
  (dark). `--k-border-strong` is unchanged (other parts use it for hover).
  `before-after-{light,dark}.png` shows the preview.
- New states: hover darkens an unchecked box; `:indeterminate` shows a bar on the
  checked fill (set `input.indeterminate = true` from script; there is no HTML
  attribute, and samples carry no script, so there is no sample for it);
  `aria-invalid="true"` draws the danger border; disabled is dimmed, the label
  muted and the cursor not-allowed.
- `tests/checkbox-multi.html` (three sets, set 3 RTL, per-set radio names) and
  `tests/test_checkbox_browser.py`, run in CI after Chromium installs.
- meta.json: status beta (was a legacy stable label) and measured behavior.

## Browser test

All 21 inputs are named by their wrapping labels; Space toggles a checkbox and the
focus ring shows; clicking the label text toggles it back; ArrowDown moves the
radio selection; the set-1 radio group is not changed by set 2; the mixed box is
indeterminate and filled like a checked one; the invalid border differs; a
disabled box ignores clicks; RTL direction in set 3; console clean.
Contrast (pixels at 2x, `--k-mscale 0`): boundary 4.83 / 5.6, label 17.72 / 16.12
(light / dark). The test fails on the old CSS (1.65 / 1.79–2.29).

## Known limits

- A radio group is its `name`. A sample pasted twice joins the two groups unless
  the names differ; meta.json says so.
- The separate Radio part (`.k-radio`) has the same low-contrast border; it is
  fixed in the Radio PR.

## Not verified

Screen readers, Safari, Firefox, real devices, 200% zoom. IME does not apply.
