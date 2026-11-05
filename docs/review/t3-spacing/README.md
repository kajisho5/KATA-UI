# T3: raw spacing → spacing tokens in UI parts

Main base: `f6f7bc590d992baf2f15522e38c6abd2383d3678`, after #38 (mold v4 scales).
Mapping: docs/token-migration.md (T3, owner decisions 2026-11-06): 4px grid, ties
to the smaller step, `--k-space-px` 1px and `--k-space-0-5` 2px, 3px → 4px,
rare multiples via `calc(var(--k-space-1) * n)`, negatives as `calc(token * -1)`.

`python3 -m tools.t3_migrate spacing` rewrote 762 declarations in 177 files: each
UI-profile spacing finding that check.py reports, in the CSS file or inline style
it names. Part-local custom properties that carried the raw value
(`--k-btn-gap`, `--k-btn-pad-lg`, `--combo-*`) were rewritten at their definition.
Lab parts are untouched (their spacing stays a warning).

One manual change: Tour's spotlight ring moved from -5px to -8px instead of the
rule's -4px. At -4px it sat on the 4px keyboard focus ring and hid it
(`verify_focus_ring --check` flagged the anchor button); at -8px both show.

| | Before | After |
|---|---:|---:|
| spacing-values findings (all) | 891 | 140 |
| — UI | 763 | 12 |
| — Lab | 128 | 128 |
| Mold Verified | 164 / 164 | 164 / 164 |
| Focus stops below 3:1 / clipped | 0 / 0 | 0 / 0 |

The 12 remaining UI findings are not raw values in the old sense:
- 10 negative offsets written as `calc(token * -1)`: the checker cannot express a
  negative token (multiplication by -1 and subtraction are reported as raw).
- Bottom Navigation's `env(safe-area-inset-bottom)` (iPhone home indicator).
- Command's `margin: 12vh auto auto` (viewport-relative dialog offset).
Accepting `* -1` and `env(safe-area-inset-*)` is a checker change; it belongs to
the final T3 PR that promotes the checks, with owner review. The `12vh` offset
needs a decision there too.

`before-after-light.png` / `before-after-dark.png`: the twelve main parts
(Button, Input, Field, Textarea, Select, Checkbox, Radio, Switch, Modal, Dropdown,
Popover, Tooltip), before on the left and after on the right. Shifts are 1–2px.

Not verified: Safari/Firefox, real phones, every non-main part by eye (the
measurement covers focus only, not general layout).
