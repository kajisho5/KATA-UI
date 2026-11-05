# T4 Card: release procedure (KATA.md contract items 14–16)

CSS only. There was no three-instance page before this pass.

## What changed

- **Unnamed progress bars.** The combo's two `role="progressbar"` elements had
  no accessible name (Chromium: `""`), so a screen reader heard "progress bar,
  62%" with no subject. They now carry `aria-label="Build minutes"` and
  `aria-label="API calls"`, matching the visible labels.
- **Inline styles in examples (item 14).** The examples restated body text
  styles inline on every `<b>` and `<p>`, one with a duplicated
  `letter-spacing`. card.css adds two optional classes, `.k-card-t` (title)
  and `.k-card-p` (text), with `.k-card-t + .k-card-p` spacing. The examples
  render pixel-identically in light and dark (Chromium, 2x). No existing class
  changed; blocks and templates that use Card are unaffected.
- meta.json: usage names the new classes; accessibility text records the
  measured footer contrast. Status stays beta.
- `tests/card-multi.html` (preview ×3 with the third RTL, examples, combo) and
  `tests/test_card_browser.py` (CI after Chromium installs).

## Browser test (Chromium, headless, 320px wide)

Progress bars named "Build minutes" and "API calls" (the old combo fails here
with `['', '']`). No horizontal page overflow at 320px. In RTL the header badge
sits at the left (inline end). The whole-card link shows a 2px focus outline.
0 console errors.

Text contrast (2x pixels; matches the computed token pairs):

| Theme | Header detail | Body | Footer note |
|---|---:|---:|---:|
| light | 4.83:1 | 7.73:1 | 4.51:1 |
| dark | 5.60:1 | 6.91:1 | 4.71:1 |

The light footer pair (`--k-ink-3` #71717a on `--k-bg-soft` #f7f7f7) is
4.51:1, 0.01 above the AA minimum. Any change to either token must re-check it.

## Not verified

Screen readers (VoiceOver, NVDA), Safari and Firefox, touch devices. Beta until
a recorded screen-reader pass. No visual change, so no before/after images.
