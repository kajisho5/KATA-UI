# T4 Textarea: release procedure (KATA.md contract items 11, 14–16)

Main base: `619f1192aec3fdf59901b726d64cef30e357edc9` (after #46, Field). No JavaScript.

## What changed

- `box-sizing: border-box`: `width:100%` plus 24px padding and 2px border
  overflowed the container by 26px, and the 92px minimum rendered as 110px.
  The preview and the Settings block are now 18px shorter (the declared size).
  Settings Page (inside a Field since #46) and Inbox are pixel-identical.
- `:focus` → `:focus-visible`; `aria-invalid="true"` styled like the original
  `data-invalid="true"` (kept); hover no longer changes a disabled field;
  disabled gets a not-allowed cursor; read-only gets a soft background and keeps
  its focus ring.
- Samples: the label wraps the textarea (no `id`/`for`); new `examples.html` with
  an error and a disabled/read-only pair (fictional content).
- `tests/textarea-multi.html` (three sets, set 3 RTL) and
  `tests/test_textarea_browser.py`, run in CI after Chromium installs.
- meta.json: measured behavior and missing manual checks; status stays beta.

## Browser test

Per set: no `id`/`for`; 12 textareas named by their own labels; clicking the
label focuses its own field; typing Japanese text appends at the end; focus
ring; invalid border differs; disabled is not-allowed and skipped by Tab while
read-only is reached with a ring; the field fits its label and an empty field is
92px tall; RTL direction in set 3. At 375px: 16px or more and no sideways
scroll. Console clean.

Text contrast (pixels at 2x, light / dark): value 17.72 / 16.12, read-only
16.54 / 13.55, placeholder 5.74 / 6.95; disabled (exempt) 4.0 / 5.63.

`before-after-{light,dark}.png`: Textarea preview and the Settings block.

## Not verified

Screen readers, real IME conversion (the test types already-converted
characters), Safari, Firefox, real devices, 200% zoom.
