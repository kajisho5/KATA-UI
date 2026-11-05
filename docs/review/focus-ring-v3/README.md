# Mold v3: visible keyboard focus (HANDOFF T2, step 2)

Main base: `4dddb8a3df5590ff8f4c69f4b408d83aa1bb5ef1`, after #32 (measurement) and
#33 (closed menus). Owner decision after #32: a 2px ink ring (option 1).

## Change

Both values are generated from `system/tokens.json` by `tools/sync_shape_tokens.py`;
`tokens.css` is not hand-edited for them any more.

| | v2 | v3 |
|---|---|---|
| `--k-ring` (component focus rings) | `0 0 0 3px` 12% ink tint, separate light/dark values | `0 0 0 2px var(--k-bg), 0 0 0 4px var(--k-ink)` in root and both theme blocks |
| focus floor `:where(:focus-visible)` | `outline:2px solid var(--k-accent)` (#33a6b8, 2.88:1 on white) | `outline:2px solid var(--k-ink)`, offset 2px |

The floor stays an outline instead of the box-shadow suggested in HANDOFF step 2:
a zero-specificity box-shadow is replaced by any component's own box-shadow
(elevation, borders drawn as rings), while outline is independent of them and
remains in forced-colors mode. Component rules that use `var(--k-ring)` get the
same 2px-gap, 2px-ink look.

`moldVersion` 2 → 3 (`moldDate` 2026-11-06). `system/mold-history.json` was
regenerated with full git history (`tools/mold_history.py --ref HEAD`) and records
`--k-ring` as a v3 meaning change, so parts that reference it require mold v3.
The mold changelog page gains a v3 section; the update page no longer names v2 files.

## Measured before → after (`tools/verify_focus_ring.py`, Chromium)

| | v2 light | v3 light | v2 dark | v3 dark |
|---|---:|---:|---:|---:|
| Tab stops | 444 | 437 | 444 | 437 |
| below 3:1 | 380 | **20** | 156 | **4** |
| no change at all | 10 | 3 | 9 | 3 |
| clipped stops (parts) | 49 (8) | 52 (9) | 49 (8) | 52 (9) |

437 instead of 444 stops: #33 removed seven closed-menu items from the Tab order.
The ring is 1px wider, so Stepper (`.k-stepper`, 3px) joins the clipped list.

`before-after-light.png` / `before-after-dark.png`: first Tab stop of Button,
Input, Tabs, Checkbox, Combobox and Tag Input; top row v2, bottom row v3.

## Remaining (T2 step 3)

Still below 3:1 in light, all with their own accent outline that overrides the
floor: Dual Range ×2, Toggle ×4, Glow Button, Confetti Cannon, Kaleidoscope,
Particle Word ×3, Wagara search, Use Cases rows ×4. Input's error field is weak in
dark (`--k-ring-danger`). No change on focus: Rating, Chip remove button, Comparison
Slider. Clipped: Time Picker, Wagara, Navigation Menu, List, Stepper, Product Page,
Split Panel, Comparison Slider, Inbox. `results.json` has per-stop details.

Screen readers, Safari/Firefox, Windows forced-colors mode and Foundry custom
palettes are not verified.
