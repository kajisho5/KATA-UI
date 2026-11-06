# Input box-sizing follow-up (recorded in HANDOFF during T4 Input/Field)

## What changed

`.input` was content-box with `width:100%` and 12px inline padding plus a 1px
border, so outside a `.k-field` it was 26px wider than its container and
40px tall. It is now `box-sizing:border-box`: it fits its container and is 38px
tall, the same as `.btn-md`.

Measured at 360px on every registry part whose sample uses `.input`
(17 parts; only those that changed are listed):

| Part | Inputs wider than their container, before → after | Height | Page scroll width |
|---|---|---|---|
| checkout | 7 (26px each) → 0 | 40 → 38 | 576 → 571 |
| date-picker | 1 (56px) → 0 | 40 → 38 | 384 → 360 |
| input | 3 (26, 26, 46px) → 0 | 40 → 38 | 374 → 360 |
| login | 2 (26px) → 0 | 40 → 38 | 360 → 360 |
| settings | 2 (26px) → 0 | 40 → 38 | 379 → 378 |
| time-picker | 1 (54px) → 0 | 40 → 38 | 360 → 360 |
| input-group, landing, site-footer | 0 → 0 | 40 → 38 | unchanged |

Checkout (571) and Settings (378) still scroll sideways at 360px for other
reasons; they are not part of this change. The Dashboard template's search
input has an explicit `width:210px` (140px under 560px), which now includes its
padding, so it is 26px narrower than before.

`tests/test_input_box_sizing.py` (CI after Chromium installs): on the Input,
Date Picker and Field three-instance pages at 360px, no `.input` is wider than
its parent, the page does not scroll sideways and every input is 38px tall. On
the old CSS it fails (15 inputs overflow on the Input page).

`input-{light,dark}.png`, `login-{light,dark}.png`: 360px, old (left) and new
(right).

## Not verified

Safari and Firefox, every block and template at every width (only the 360px
registry previews were measured).
