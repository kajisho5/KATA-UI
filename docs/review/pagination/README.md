# T4 Pagination: release procedure (KATA.md contract items 12, 14–16)

CSS only. There was no three-set page before this pass.

## What changed

- **RTL arrows.** The prev/next chevrons and the compact form's ← → pointed
  the same way in RTL, so "previous" (now on the right) pointed left. They
  mirror under `:dir(rtl)` (KATA.md "Keyboard direction": visual arrows follow
  the reading direction).
- **Disabled state.** `.disabled` only set `pointer-events:none`; a disabled
  link stayed a Tab stop and Enter still followed it. The documented pattern is
  now an `<a>` without `href` plus `aria-disabled="true"` (shown in a new
  "first page" sample). `.disabled` stays as a deprecated alias.
- **Current page on hover.** `a.k-page:hover` outranked the current-page
  fill, so hovering page 2 turned it light. Hover and the new `:active` style
  skip `aria-current="page"`.
- **Names.** The compact form's text arrows read as "left arrow Prev"; they are
  now `aria-hidden` spans (`.k-page-arrow`). Chevron SVGs and the ellipsis are
  `aria-hidden`. The inline style on "Page 3 of 12" became `.k-page-pos`.
- `.k-page` gets `gap: var(--k-space-1)` so the arrow and word keep their space
  inside the flex item.
- `tests/pagination-multi.html` (three sets, the third RTL) and
  `tests/test_pagination_browser.py` (CI after Chromium installs).

## Browser test (Chromium, headless)

Link names per set: Previous page, 1, 2, 3, 4, 18, Next page / 1, 2, 3, Next
page / Prev, Next; the disabled Previous is skipped by Tab and has no href;
the current page keeps its background on hover (the old CSS fails here);
arrows mirrored only in RTL. 0 console errors.

| Text | Light | Dark |
|---|---:|---:|
| Page number | 7.73:1 | 6.91:1 |
| Current page | 17.72:1 | 16.12:1 |
| "Page 3 of 12" | 7.73:1 | 6.91:1 |

`before-after-{light,dark}.png`: LTR and RTL, old (left) and new (right).

## Not verified

Screen readers (VoiceOver, NVDA), Safari and Firefox, touch devices. Beta until
a recorded screen-reader pass.
