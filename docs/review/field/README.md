# T4 Field: release procedure (KATA.md contract items 11, 14–16)

Main base: `9792d5ad2ec88efd001d068991f3783d4b0d5140` (after #45, Input).

## What changed

- **Claimed but missing behavior.** meta.json said the hint and error were wired
  with aria-describedby and the error became an alert only after submit. The
  sample did it with fixed IDs and nothing did the alert. New `field.js`
  (IIFE, `data-kata-ready`, safe to load twice, one MutationObserver per field,
  no document listeners) now:
  - generates missing IDs (`kata-field-N-…`, collision-checked) and keeps existing ones;
  - adds the hint, and the error while `data-invalid` is set, to aria-describedby
    after the author's own IDs;
  - sets/removes aria-invalid with data-invalid;
  - sets role="alert" on the error only when data-invalid is added after load
    (an error already present at load is not announced; typing does not change it).
- **Sample without fixed IDs:** the label wraps its control; the text and badge
  stay on line one and the control fills line two (`flex-wrap`, 8px row gap, as
  the previous grid gap). The name works without the script.
- **Controls fit the field:** `.k-field :is(input,textarea,select)` uses
  border-box. Before, `.input` (content-box, width 100% plus 26px padding and
  border) overflowed the field by 26px, and its 38px height rendered as 40px.
  Settings Page inputs ran past the card edge; its textarea is now its declared
  92px instead of 110px.

## Evidence

- `tests/field-multi.html`: three sets (set 3 RTL), a field with author IDs, and
  the script loaded twice.
- `tests/test_field_browser.py` (CI runs it after Chromium installs): 7 fields
  initialized once, all IDs unique, label names, hint/error descriptions,
  aria-invalid sync, alert only on a later error, typing keeps it, control inside
  the field and below the label text in LTR and RTL, author IDs kept with the
  author's description first, no horizontal scroll at 375px, console clean.
  Text contrast (pixels, light / dark): label 17.72 / 16.12, Optional 4.83 / 5.6,
  Required 6.26 / 7.48, hint 4.83 / 5.6, error 6.26 / 7.48.
- `before-after-{light,dark}.png`: Field preview and the Settings Page template.

## Not verified

Screen readers (whether role="alert" is announced once), real IME input,
Safari, Firefox, real devices, 200% zoom. Status stays beta.
Follow-up (recorded in HANDOFF): `.input` itself is content-box everywhere
outside a Field.
