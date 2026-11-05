# T4 Toast: release procedure (KATA.md contract items 11, 14–16)

## What changed

- **Not announced (bug).** meta.json said toasts announce "via a polite live
  region", but no element had `role="status"` or `aria-live`, so screen
  readers were not told about new toasts (WCAG 4.1.3 status messages).
  toast.js now gives each `[data-toasts]` stack `role="status"` and
  `aria-live="polite"` at load, before any toast is added (a region created
  together with its content is often not announced). Author values are kept.
- **Markup from text.** The title and detail were concatenated into
  `innerHTML`. They are now inserted with `textContent`.
- **Hard-coded colour.** The check icon carried `stroke="#5dac81"` and an
  inline style in the JS, which the mold checker does not read. It is now
  `stroke="currentColor"` with `.toast-icon { color: var(--k-success) }`
  (the same value) and `aria-hidden="true"`. The 1px offset uses
  `--k-space-px`. Rendering is pixel-identical (`before-after-*.png`).
- meta.json: `stable` → `beta`; the accessibility text lists what is and is
  not implemented.
- `tests/toast-multi.html` (three instances, the third RTL, script loaded
  twice) and `tests/test_toast_browser.py` (CI after Chromium installs).

## Browser test (Chromium, headless, --k-mscale 0, fake clock)

Each stack is a polite status region before any toast; one click adds one
toast to that instance's stack (double load binds once) and focus stays on the
button; the icon is aria-hidden and the toast has no inline styles; after
4.1 s every toast is removed. 0 console errors. The old toast.js fails at the
first check (no `role`).

Text contrast on the toast (2x pixels):

| Theme | Title | Detail |
|---|---:|---:|
| light | 17.72:1 | 16.54:1 |
| dark | 16.12:1 | 13.55:1 |

## Not implemented / not verified

- Pausing on hover or focus, and a dismiss button. Toasts are for
  confirmations only (meta usage); errors that need action do not belong here.
- The script has no public `toast()` API; only `[data-toast-demo]` triggers it.
  Adding an API is a separate change.
- Screen readers (VoiceOver, NVDA) actually announcing the toast, Safari and
  Firefox, touch devices. Beta until a recorded screen-reader pass.
