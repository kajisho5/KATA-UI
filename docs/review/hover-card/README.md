# Hover Card review (T4)

## Changes
- **Read twice (bug).** A closed card was only `opacity:0`, so its heading "Aoi Kimura", the initials "AK" and both paragraphs stayed in the accessibility tree right after the link (Chromium AX tree on main). Closed cards are now `visibility:hidden`; the visibility change is delayed by `--k-dur-base` so the fade-out still plays.
- **Escape (WCAG 1.4.13).** There was no way to dismiss the card without moving the pointer or focus. Escape now closes every open card; focus stays on the trigger. One shared document `keydown` listener per script load.
- **Script guard.** `hover-card.js` is an IIFE with `data-kata-ready`; a second load adds no listeners.
- **Viewport (bug).** At 360px the centred 262px card started at x = −73px. It now uses the Popover approach (#56): `--khover-shift` keeps it 16px (`--k-space-4`) inside the viewport, and `max-width:calc(100vw - var(--k-space-16))`.
- `text-align:left` → `start`.
- `meta.json`: accessibility text describes the timing, Escape, hidden state and fit.

## Evidence
- `tests/test_hover_card_browser.py` over `tests/hover-card-multi.html` (three sets, third `dir="rtl"`, script loaded twice): 1 document keydown listener, closed card text absent from the accessibility tree and present once when open, focus opens, Escape closes and keeps focus, hover opens after the delay and closes after leaving, card text ≥ 4.5:1 in light and dark, at 360px the open card stays inside the viewport in LTR and RTL, 0 console errors. Main's code fails it.
- At 900px the open card is pixel-identical to main in light and dark.
- Screenshots: `before-after-360-light.png`, `before-after-360-dark.png`.

## Not verified
- Screen readers (VoiceOver, NVDA), Safari and Firefox, touch devices.
