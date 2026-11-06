# T4 Combobox: release procedure (KATA.md contract item 11)

Combobox is the contract's initialization reference and already had its
three-instance page, `tests/test_combobox_browser.py` and the
`verify_overlay_instances` focus checks. HANDOFF listed one remaining item 11
gap: every instance added its own `document` click listener.

## What changed

- combobox.js: one `pointerdown` listener per script load replaces the
  per-instance `document` click listener; it closes every instance the press
  is outside of. Outside dismissal now uses `pointerdown`, as item 11 requires.
- `tests/test_combobox_browser.py`: a second test reads the document's
  listeners through the Chrome DevTools Protocol on the three-instance page
  (script loaded twice): 0 click listeners and 1 pointerdown listener; a
  pointer press outside closes an open list before the click. The old script
  fails it (3 click listeners).
- CI now runs `tests.test_combobox_browser` after Chromium is installed (it
  was only in the pre-Chromium discovery step, where it skipped).
- meta.json: the accessibility text mentions the outside-press behaviour.

## Not verified

Screen readers (VoiceOver, NVDA), a real IME, Safari and Firefox, touch
devices. Status stays beta. No visual change.
