# T4 Breadcrumbs: release procedure (KATA.md contract items 12, 14–16)

CSS only. There was no three-set page before this pass.

## What changed

- **RTL separators.** The chevron separators pointed right in RTL too, away
  from the current page. `.k-crumbs:dir(rtl) svg` mirrors them (KATA.md
  "Keyboard direction": visual arrows follow the reading direction). This also
  applies to the App Shell block, which uses the same markup.
- meta.json: accessibility text mentions the RTL mirroring.
- `tests/breadcrumbs-multi.html` (three sets, the third RTL) and
  `tests/test_breadcrumbs_browser.py` (CI after Chromium installs).

## Browser test (Chromium, headless)

Navigation named "Breadcrumb", links Home/Projects/kata-ui, the current page is
not a link and carries `aria-current`; separators mirrored only in RTL (the old
CSS fails here); link targets are at least 24px apart (WCAG 2.5.8 spacing).
0 console errors.

Text contrast (2x pixels): links 7.73:1 light / 6.91:1 dark, current page
17.72:1 / 16.12:1.

## Not verified

Screen readers (VoiceOver, NVDA), Safari and Firefox, touch devices; long paths
on small screens (the usage text asks authors to collapse the middle; there is
no collapsing behaviour). Beta until a recorded screen-reader pass. The only
visual change is the mirrored separator in RTL.
