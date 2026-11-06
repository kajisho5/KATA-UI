# T4 Alert Dialog: release procedure (KATA.md contract items 11, 13–16)

The #24 instance work (IIFE, data-kata-ready, generated IDs, focus on the
least destructive action, Tab cycling, no backdrop dismissal, native
Escape/cancel, IME guard, opener focus) and `tests/alert-dialog-multi.html`
already exist; `tools/verify_overlay_instances` checks them in CI since #54.

## What changed

- **Narrow screens.** At 320px the dialog is 280px wide with 24px padding, and
  the two buttons (Keep project, Delete project) need 248px; the row did not
  wrap, so the buttons ran 16px into the left padding. `.kalert-row` now wraps;
  the buttons stay inside the padding and keep their end alignment.
- `tests/test_alert_dialog_browser.py` (CI after Chromium installs): role
  `alertdialog` named "Delete project", the 320px layout (fails on the old CSS)
  and text contrast.

## Measured

Heading 17.72:1 light / 16.12:1 dark; body 7.73:1 / 6.91:1 (2x pixels).
0 console errors. `before-after-{light,dark}.png`: 320px, old (left) and new
(right).

## Not verified

Screen readers (VoiceOver, NVDA) announcing an alertdialog, a real IME, Safari
and Firefox, touch devices. Status stays beta until a recorded screen-reader
pass.
