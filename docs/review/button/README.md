# T4 Button: release procedure (KATA.md contract items 11, 14–16)

Main base: `cbc90730d267596403b9b76803acd5fef6f366d4` (after #42; rebased onto #43).
Button has no JavaScript, so contract item 11 (initialization, IDs, IME guards)
applies only to its samples.

## What changed

- `combos.html`: the subscribe row no longer has a fixed `id`/`for`; the label
  wraps the input, so pasting the sample twice cannot duplicate an ID
  (item 11, from the open #12 remainder). Rendered pixels are identical before
  and after in light and dark.
- `tests/button-multi.html`: three sets of every variant, size, disabled and
  loading state; set 3 is `dir="rtl"` (from #12).
- `tests/test_button_browser.py` (from #12, Chromium path from `CHROMIUM_PATH`):
  per set and variant, keyboard focus draws a box-shadow, pressing moves the
  button, Enter and Space click once each, disabled opacity is .45, loading
  buttons are disabled, `btn-asagi` paints the same background as
  `btn-accent`, spinners stop under reduced motion, no horizontal scroll at
  375px, and the console is clean. A second test runs the table below.
- `tools/verify_button.py`: the variant × state contrast table.
- `meta.json`: status **beta** (was a legacy stable label), and the a11y text
  states only measured behavior and the missing evidence.

## Variant × state text contrast (Chromium, `button-states.json`)

Pixel measurement on `tests/button-multi.html`, set 1. Sets 2 and 3 (RTL) match
set 1 within 0.05. Enabled states must reach 4.5:1; the lowest is 5.57:1 (light
Danger hover). Disabled text is exempt from 1.4.3 and recorded for reference.

| Theme | Variant | default | hover | pressed | focus | disabled |
|---|---|---:|---:|---:|---:|---:|
| light | Primary | 17.72 | 7.73 | 17.72 | 17.72 | 2.96 |
| light | Secondary | 17.72 | 16.54 | 15.02 | 17.72 | 2.96 |
| light | Ghost | 7.73 | 16.54 | 15.02 | 7.73 | 2.16 |
| light | Accent | 6.16 | 6.88 | 6.16 | 6.16 | 1.86 |
| light | Danger | 5.79 | 5.57 | 5.79 | 5.79 | 2.3 |
| dark | Primary | 16.12 | 6.91 | 16.12 | 16.12 | 4.19 |
| dark | Secondary | 16.12 | 13.55 | 13.55 | 16.12 | 4.19 |
| dark | Ghost | 6.91 | 13.55 | 13.55 | 6.91 | 2.43 |
| dark | Accent | 6.16 | 6.88 | 6.16 | 6.16 | 2.24 |
| dark | Danger | 5.79 | 7.26 | 5.79 | 5.79 | 3.08 |

Keyboard focus ring: `tools/verify_focus_ring --check` measures every Button
stop at 3:1 or more against its blurred state in both themes (0 below 3:1,
0 clipped across 437 stops).

## Why beta

Item 16 requires a recorded manual screen-reader pass. None was run in this
session (no screen reader in the container). IME does not apply: a button takes
no text input. To mark Button stable, record one pass, for example iPhone
VoiceOver on the preview page: each button is announced with its name and
"button"; the disabled and loading ones are announced as dimmed/unavailable;
the icon-only buttons are announced as "Settings" and "Close".

Not verified: screen readers, Safari, Firefox, real devices, 200% zoom.
