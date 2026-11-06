# Command review (T4)

## Changes
- **Contract item 11.** `command.js` added one document `keydown` listener (Cmd/Ctrl+K) per palette. It now keeps a list of palettes and adds one shared listener per script load; a second load finds no new palette and adds none. The target rule is unchanged: the open palette, else the palette whose trigger has focus, else the first in document order. Composition is still ignored (`isComposing`, keyCode 229, and each palette's composition state).
- `command.css`: `border-bottom` → `border-block-end`, `max-height` → `max-block-size`.
- `meta.json`: accessibility text records the shared listener.

## Evidence
- `tests/test_command_browser.py` over `tests/command-multi.html` (three palettes, script loaded twice): 1 document keydown listener (main: 3), a composing Ctrl+K opens nothing, Ctrl+K with nothing focused opens the first palette only, a second press keeps one open, Ctrl+K on the second trigger opens the second palette, Escape returns focus to that trigger, 0 console errors.
- `tests.test_command_context_date` (existing) still passes.
- Screenshots of the open palette with main's CSS and this branch: pixel-identical in light and dark.

## Not verified
- Real IME input, screen readers (VoiceOver, NVDA), Safari and Firefox, macOS Cmd key (the test uses Ctrl).
