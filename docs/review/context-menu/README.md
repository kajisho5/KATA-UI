# Context Menu review (T4)

## Changes
- **Contract item 11.** `context-menu.js` added one document `pointerdown` listener per menu for outside presses. It now keeps a list of menus and adds one shared listener per script load; a second load finds no new menu and adds none. The window `blur` listener already had a document-level guard and is unchanged.
- `context-menu.css`: `min-height` → `min-block-size`, `border-top` → `border-block-start`.
- `meta.json`: accessibility text records the shared listener.

## Evidence
- `tests/test_context_menu_browser.py` over `tests/context-menu-multi.html` (three menus, script loaded twice): 1 document pointerdown listener (main: 3), right-click opens only that menu, a press outside closes it, a press inside the open menu keeps it open, 0 console errors.
- `tests.test_command_context_date` (existing keyboard and independence checks) still passes.
- Screenshots of an open menu with main's CSS and this branch: pixel-identical in light and dark.

## Not verified
- Touch long-press, real IME input, screen readers (VoiceOver, NVDA), Safari and Firefox.
