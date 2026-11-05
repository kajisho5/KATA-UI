# T4 Table: release procedure (KATA.md contract items 14–16)

CSS only. There was no three-instance page before this pass.

## What changed

- **Header markup.** The header row sat in the implicit `<tbody>` with bare
  `<th>`. It is now `<thead>` with `scope="col"`; the rows are in `<tbody>`.
- **Keyboard scrolling (WCAG 2.1.1).** At 360px the table is wider than its
  `.ktable-wrap`, which scrolls. The wrapper now has `role="region"`,
  `aria-label="Projects"` and `tabindex="0"`, so it takes focus (shared focus
  outline) and the arrow keys scroll it. Browsers that do not make scroll
  containers focusable on their own need this.
- **Avatar initials.** "YM Yamada" was read as the owner; `.ava` is now
  `aria-hidden`, so the cell reads "Yamada".
- **Numbers.** meta.json said "right-align numbers", but the Amount column was
  start-aligned. New `.num` class (`text-align:end`, tabular digits) on the
  header and cells. In RTL it aligns to the left.
- **Avatar alignment.** `vertical-align:-8px` left the name above the avatar's
  centre; `vertical-align:middle` aligns them (rows are 3px shorter).
- meta.json: `stable` → `beta`; usage and accessibility text updated.
- `tests/table-multi.html` (three instances, the third RTL) and
  `tests/test_table_browser.py` (CI after Chromium installs).

## Browser test (Chromium, headless)

Column headers Project/Owner/Status/Amount; three regions named "Projects";
owner cell named "Yamada"; at 360px the region overflows, takes focus with an
outline and scrolls on ArrowRight, and the page itself does not overflow;
amounts end-aligned in LTR and RTL. 0 console errors. The old markup fails
(no region).

| Text | Light | Dark |
|---|---:|---:|
| Header (ink-3 on bg-soft) | 4.51:1 | 4.71:1 |
| First column | 17.72:1 | 16.12:1 |
| Amount | 7.73:1 | 6.91:1 |

`before-after-{light,dark}.png`: old (top) and new (bottom).

## Not verified

Screen readers (VoiceOver, NVDA) table navigation, Safari and Firefox, touch
scrolling. Beta until a recorded screen-reader pass.
