# T4 Dropdown: release procedure (KATA.md contract items 11, 12, 14–16)

Repository slug: `components/dropdown` (the queue's "dropdown-menu").

## What changed

- **dropdown.js** was four lines: no IIFE, no `data-kata-ready` guard, one
  `document` click and keydown listener per instance, no ARIA state, no arrow
  keys and no focus return (meta.json listed these as not implemented). It now
  follows the WAI-ARIA APG menu button pattern and contract item 11:
  - trigger: `aria-haspopup="menu"`, `aria-expanded`, `aria-controls`;
    menu: `role="menu"` named by the trigger; links are `menuitem`s with
    `tabindex=-1`; `<hr>` is a `separator`; the `.mh` heading is presentational.
  - Enter/Space/ArrowDown open on the first item, ArrowUp on the last;
    ArrowUp/Down wrap; Home/End (and PageUp/PageDown) jump; `aria-disabled`
    items are skipped; Space activates a link item.
  - Escape and choosing an item close and return focus to the trigger; Tab,
    an outside `pointerdown` and window blur close without moving focus.
    A `focusout` with a null `relatedTarget` does not close.
  - Opening one menu closes the others. IME composition keys are ignored.
  - Outside-press and blur listeners are registered once per script load, not
    per instance. A `kata-dropdown-toggle` event (bubbling, `detail.open`)
    reports open and close.
- **dropdown.css**: a focused item gets the hover background (keyboard users
  could only see the ring before), `:active`, a danger hover/focus background
  (`--k-danger-bg`) and an `aria-disabled` style.
- preview.html: the chevron SVG is `aria-hidden`.
- meta.json: `stable` → `beta`; the accessibility text lists what the browser
  test checks.
- `tests/dropdown-multi.html` (three instances, the third RTL, script loaded
  twice) and `tests/test_dropdown_browser.py` (CI after Chromium installs).

## Browser test (Chromium, headless, --k-mscale 0)

Per instance: roles and states, Enter/ArrowUp opening, wrap, Home/End, Escape
focus return, one-open-at-a-time, Tab closing, null focusout, outside press,
item choice. Disabled item skipped. RTL menu aligns to the trigger's right edge.
Unique IDs, 0 console errors. On the old dropdown.js the test fails at the
first check (no `data-kata-ready`).

Item text on the focused background (2x pixels, `tools.verify_button.text_contrast`):

| Theme | Edit | Delete (danger) |
|---|---:|---:|
| light | 17.72:1 | 6.26:1 |
| dark | 13.55:1 | 7.26:1 |

`before-after-{light,dark}.png`: open menu with keyboard focus on Delete, old
(left) and new (right).

## Not verified

Screen readers (VoiceOver, NVDA), a real IME, Safari and Firefox, touch devices.
Beta until a recorded screen-reader pass.
