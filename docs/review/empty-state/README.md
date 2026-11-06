# Empty State review (T4)

## Changes
- `components/empty-state/preview.html`: the decorative SVG icon gets `aria-hidden="true"`. Before, Chromium exposed it as an unnamed image (3 in `tests/empty-state-multi.html`).
- `components/empty-state/empty-state.css`: `margin-bottom` → `margin-block-end`, `margin-top` → `margin-block-start`, `max-width` → `max-inline-size` (AGENTS.md rule 7).
- `components/empty-state/meta.json`: accessibility text records the decorative icon and logical spacing.

## Evidence
- `tests/test_empty_state_browser.py` over `tests/empty-state-multi.html` (three sets, third `dir="rtl"`): 3 headings "No exports yet", 3 buttons "Create export", 0 exposed images, heading and body text ≥ 4.5:1 in light and dark, no horizontal scroll at 360px, 0 console errors.
- Text contrast (device scale 2): heading 17.72 light / 16.12 dark, body 7.73 / 6.91. Icon (`--k-ink-3` on `--k-bg-soft`): 4.51 / 4.71.
- Full-page screenshots of main's CSS and this branch are pixel-identical in light and dark (after a 1s wait for the theme transition).

## Not verified
- Screen readers (VoiceOver, NVDA), Safari and Firefox.
