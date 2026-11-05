# Tag Input / Input OTP / Data Table

Main base: `2c057fb48157fe5fa03ae3f58a892087ff044d4d`, after merged PR #26.
These are the first three JS-failing parts in the requested order. Tag Input and
Data Table failed both JS rules; Input OTP failed global bindings only.
Their release status remains **Beta**. No shared tokens or checker rules change.

| Audit | Before | After |
|---|---:|---:|
| Mold Verified | 100 / 164 | 103 / 164 |
| UI | 67 / 121 | 70 / 121 |
| Lab | 33 / 43 | 33 / 43 |
| js-single-instance findings | 14 | 12 |
| js-global-bindings findings | 37 | 31 |
| focus-visible findings | 125 | 119 |
| token-values | 0 | 0 |

## Source and behavior

`build.py` reads originals and generates downloadable files, component pages,
registry and model-facing data. It does not rewrite these component originals;
regenerate instead of editing those generated copies. Each JS script is an IIFE,
initializes all roots once, checks ID collisions and preserves supplied IDs.
None needs a document/window listener. No overlays, exit animations or dragging
exist in these three parts, so popup dismissal/exit timing are not applicable.
Existing data hooks and classes stay available.

- Tags commit on Enter/comma, not blur. Duplicate matching is case-insensitive.
  Typed draft text remains on body click, null focusout or window blur. Empty
  Backspace removes the final chip. Visual arrows navigate removal buttons;
  RTL Left moves forward. Delete/Backspace remove focused chips. Named native
  buttons, live status and `kata-tag-input-add/remove` report changes. Tag text
  uses textContent/attributes, never interpolation into HTML.
- OTP stays explicitly LTR inside RTL pages, advances after a digit, clears and
  moves back on Backspace, and distributes paste/autofill over that instance's
  digits. The first input supports one-time-code; each digit is labelled and
  numeric. Composition events/keys are guarded. Completed changed codes emit
  bubbling native `change` on `[data-otp]` with `data-value`; ordinary native
  per-digit changes still bubble, so applications distinguish the event target.
- Table has a Members caption. Text/numeric sorting uses native buttons and
  stable sort; selection stays on its row. Select-all and indeterminate state
  work per table. `aria-sort` is correctly on **th**, not the button: ARIA permits
  it on column/row headers, not button roles. Buttons control their own table.
  Sorting emits `kata-data-table-sort` with column/direction; checkbox changes
  are native. Status announces sort and selection counts. Initial unsorted rows
  are no longer falsely labelled ascending. Pagination remains application work.

All three add necessary `var(--k-ring)` focus-visible styles. Tags no longer get
both a surrounding focus-within ring and an input ring. Existing CSS motion is
border/focus/sort-indicator transition only; no completion event waits exist.
Metadata states only implemented behavior, with event-listening usage examples.
Existing spacing/type warnings remain; a static pass does not make a part Stable.

## Verification

```sh
node --check components/tag-input/tag-input.js
node --check components/input-otp/input-otp.js
node --check components/data-table/data-table.js
python3 check.py --json mold-results.json
python3 -m tools.verify_tag_otp_table
python3 -m unittest discover -s tests -p 'test_*.py'
python3 -W error::SyntaxWarning build.py
python3 -m tools.mold_ratchet --report mold-results.json
python3 -m tools.verify_mold_distribution
python3 -m tools.mold_publish --check
```

`results.json` and screenshots cover nine Chromium cases: three copies, one RTL,
script loaded twice (then again), normal/zero/reduced motion, independent state,
unique/application IDs, composition events, duplicate/XSS-safe tags, event counts,
visual tag movement, LTR OTP coordinates, paste and completion, native keyboard
sorting, mixed/select-all checkboxes, table names and preserved row selection.
Console errors: zero. No part registers global shortcuts/blur/resize/pointerdown;
the test excludes Playwright's own hit-target interceptor from that count.

Real Japanese IME, screen readers, Firefox/Safari, SMS/password-manager autofill
and mobile soft keyboards remain unverified. Synthetic composition/autofill
behavior does not replace device checks. No Stable promotion is made.

## Remaining JS failures (9 targets)

In priority order: file-upload, color-picker, carousel, split-panel, reorder,
follow-frame, blocks/pricing, blocks/site-header, blocks/use-cases. Use Cases fails
only global bindings; the other eight fail both JS rules.
