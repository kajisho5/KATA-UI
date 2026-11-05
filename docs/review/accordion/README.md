# T4 Accordion: release procedure (KATA.md contract items 14–16)

Native `<details>`/`<summary>`, CSS only. There was no three-set page before
this pass. The browser test found no defect, so no part file changed.

## Browser test (Chromium, headless, --k-mscale 0)

`tests/accordion-multi.html` (three sets, the third RTL) and
`tests/test_accordion_browser.py` (CI after Chromium installs):

- Each summary is exposed as a disclosure with its question as the name and
  the right expanded state (open, closed, closed per set).
- Enter opens and Space closes the focused item; other sets do not change.
- The focus ring (`--k-ring` box-shadow) is drawn on the summary; the chevron
  rotates when open.
- Collapsed answers stay in the document text (find-in-page can reach them).
- In RTL the chevron sits at the inline end (left half of the summary).
- 0 console errors.

Text contrast (2x pixels): question 17.72:1 light / 16.12:1 dark, answer
7.73:1 / 6.91:1.

## Not verified

Screen readers (VoiceOver, NVDA), Safari and Firefox (the summary marker reset
and find-in-page auto-expansion differ by browser), touch devices. Status stays
beta until a recorded screen-reader pass. No visual change, so no images.
