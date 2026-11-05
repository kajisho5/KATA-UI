# T4 Popover: release procedure (KATA.md contract items 11, 14–16)

Popover already had the #24 instance work (IIFE, `data-kata-ready`, generated
IDs, Escape focus return, IME guard, null-focusout guard) and its three-instance
page. This pass found two gaps.

## What changed

- **Overflow on narrow screens.** The 306px panel is centred under its trigger.
  With the trigger at the inline start of a 360px-wide page it reached
  x = -77 (LTR) and 437 (RTL), cut off by the screen edge. popover.js now sets
  a component custom property, `--kpop-shift`, on open and on resize so the
  panel keeps a `--k-space-4` margin from both viewport edges; on a wide page
  the shift is 0 and the panel stays centred. `max-width` caps the panel below
  about 340px viewports. The panel keeps its size (content-box, 272px + padding).
- **Contract item 11.** Every instance added its own `document` click
  listener (HANDOFF item 11 gap). One `pointerdown` and one `resize` listener
  per script load now serve all instances; outside dismissal uses
  `pointerdown`, as the contract requires.
- meta.json: the accessibility text adds the viewport shift; status stays beta.
- `tests/test_popover_browser.py` (CI after Chromium installs). The existing
  `tools/verify_overlay_instances` run still passes for Popover.

## Browser test (Chromium, headless, 360px wide, --k-mscale 0)

All three instances (the third RTL) with the trigger at the inline start: the
panel stays within 16px of both edges. On the old CSS and JS the first case
reads x = -101 and fails. At 1100px the panel stays centred (offset under 1px).
An outside press closes each panel. 0 console errors.

Text contrast in the panel (2x pixels, `tools.verify_button.text_contrast`):

| Theme | Heading | Body text |
|---|---:|---:|
| light | 17.72:1 | 7.73:1 |
| dark | 16.12:1 | 6.91:1 |

`before-after-{light,dark}.png`: 360px page, trigger at the left edge, old
(left, panel cut off) and new (right).

## Not verified

Screen readers (VoiceOver, NVDA), a real IME, Safari and Firefox, touch devices,
on-screen keyboards resizing the viewport. Beta until a recorded screen-reader pass.
