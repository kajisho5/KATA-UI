# T4 Modal: release procedure (KATA.md contract items 11, 13–16)

## What changed

- **modal.js** follows item 11 (the Drawer and Alert Dialog pattern from #24):
  IIFE, `querySelectorAll` roots, `data-kata-ready` guard (loading twice is
  safe), collision-checked generated IDs, existing IDs kept.
- **Item 13 (was missing, HANDOFF contract gap):** a click on the backdrop now
  closes the modal. Before, it stayed open.
- The trigger gets `aria-controls` and `aria-haspopup="dialog"`. The first
  heading names the dialog (`aria-labelledby`) and the first paragraph describes
  it (`aria-describedby`). Before, the dialog had no name link.
- Focus moves to the first control (or an `autofocus` control) on open, Tab and
  Shift+Tab cycle inside, and focus returns to the opener on close. Before,
  focus did not return after a backdrop or button close in this test.
- A trigger whose modal is already open does nothing (no second `showModal`).
- Escape is ignored while an IME is composing (`cancel` is vetoed, keyCode 229).
- combos.html: the label wraps the input instead of a fixed `id`/`for` (item 14).
- meta.json: status `stable` → `beta`; the accessibility text lists only what
  the browser test checks.
- `tests/modal-multi.html` (three instances, the third `dir="rtl"`, script
  loaded twice). `tools/verify_overlay_instances.py` now covers Modal, and CI
  runs `tests.test_overlay_instances` after Chromium is installed.

## Browser test (Chromium, headless)

`tools.verify_overlay_instances` for Modal, normal/zero/reduced motion: three
independent instances, double load, RTL, unique IDs, existing IDs kept, a
paragraph click and a null focusout keep it open, Tab/Shift+Tab wrap, Escape
closes and refocuses the trigger, backdrop click closes, synthetic IME guard.
0 console errors. On the old modal.js the same run fails (no `data-kata-ready`);
a separate backdrop check reads open after a backdrop click, no
`aria-labelledby`, focus not on the opener.

`before-after-{light,dark}.png`: the Rename combo open, old (left) and new
(right). The CSS is unchanged; the label now wraps the input with the same look.

## Not verified

Screen readers (VoiceOver, NVDA), a real IME, Safari and Firefox, touch devices.
Beta until a recorded screen-reader pass.
