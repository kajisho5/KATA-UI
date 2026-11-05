# T3: raw font sizes → text tokens in UI parts

Main base: `0c318c138c8dccdd15f4feebef8e2b816e182040`, after #39 (T3 spacing).
Mapping: docs/token-migration.md (T3, font size; owner decision 2026-11-06): snap
to the existing text steps plus the 15px `--k-text-lead` step added in mold v4.

`python3 -m tools.t3_migrate font-size` rewrote 433 declarations in 148 files: each
UI-profile font-size finding that check.py reports, in the CSS file or inline style
it names. Lab parts are untouched (their font sizes stay a warning).

| | Before | After |
|---|---:|---:|
| type-values findings (all) | 638 | 205 |
| — UI font-size | 435 | 2 |
| — UI line-height | 84 | 84 |
| — Lab | 119 | 119 |
| Parts with warnings | 206 | 141 |
| Mold Verified | 164 / 164 | 164 / 164 |
| Focus stops below 3:1 / clipped (light, dark) | 0 / 0 | 0 / 0 |

The 2 remaining UI font-size findings are `.86em` on inline `code` in Typeset and
Blog Article. The size follows the surrounding text (body, heading or list), so a
fixed px token would change it inside headings. They are left for the final T3
promotion PR, which decides how the checker treats em-relative inline sizes.

`before-after-light.png` / `before-after-dark.png`: the twelve main parts
(Button, Input, Field, Textarea, Select, Checkbox, Radio, Switch, Modal, Dropdown,
Popover, Tooltip), before on the left and after on the right. Pixel comparison:
Button, Select, Checkbox, Switch, Modal, Dropdown, Popover and Tooltip are
identical; Input and Textarea hint/error text 12px → 12.5px; Field label 13px →
13.5px and help/error text 12px → 12.5px (the part is 2px taller); Radio's "−20%"
badge 12px → 12.5px. Inputs at 640px and below go from 16px to 16.5px
(`--k-text-lg`), which stays at or above the 16px size that keeps iOS Safari from
zooming on focus.

Not verified: Safari/Firefox, real phones, every non-main part by eye (the
measurement covers focus only, not general layout).
