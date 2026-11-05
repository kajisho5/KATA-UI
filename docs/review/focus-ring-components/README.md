# Component focus rings after mold v3 (HANDOFF T2, step 3 — part 1)

Main base: `0b8f5f6659a9f5c208ccd82ef02379e1e7c225ef`, after #34 (mold v3).
#34 fixed the shared ring; this PR fixes parts that drew their own weak ring.

## Changes

| Part | Before | After |
|---|---|---|
| Toggle, Dual Range, Rating label, Wagara search, Use Cases rows | own 2px `--k-accent` outline | 2px `--k-ink` outline, same offsets |
| Confetti Cannon, Kaleidoscope, Particle Word buttons | floor outline: ink on a fixed `--k-zinc-950` stage (light theme) | 2px `--k-on-color` outline (fixed light color on the fixed dark stage) |
| Chip remove button on a selected chip | ink outline on the ink chip | outline uses `--k-bg` |
| Comparison Slider | range input has `opacity:0`, so its focus is never visible | the visible grip gets a 2px `--k-zinc-900` outline while the input has keyboard focus |
| Glow Button search field | input `outline:none`, only an accent glow | the field gets `box-shadow: var(--k-ring)` while the input has keyboard focus |
| Input / Textarea in error | `--k-ring-danger` (3px 14% red, below 3:1) | `var(--k-ring)`; the red border and message still mark the error |

`--k-ring-danger` is no longer used by any part but stays in tokens.css; removing
it would be an API change.

`system/mold-history.json` is regenerated with `--ref origin/main`, so the v3
`--k-ring` change now points at the #34 squash commit `0b8f5f6`.

## Measured (`tools/verify_focus_ring.py`, Chromium, 437 Tab stops)

| | after #34, light | now, light | after #34, dark | now, dark |
|---|---:|---:|---:|---:|
| below 3:1 | 20 | **1** | 4 | **1** |
| clipped stops (parts) | 52 (9) | 52 (9) | 52 (9) | 52 (9) |

The remaining stop is Rating: the focused element is a 1×1px radio input and the
ring is drawn on its label next to it, outside the measured crop. The tool cannot
see it; a person can. Clipped rings (Time Picker, Wagara, Navigation Menu, List,
Stepper, Product Page, Split Panel, Comparison Slider, Inbox) are the next PR.

Static checker: 112 → 116 (Chip, Confetti Cannon, Kaleidoscope, Particle Word now
pass focus-visible). Comparison Slider and Glow Button now show a 3:1 ring in the
browser but still fail the static rule, which cannot read `:has()` selectors; T2
step 4 replaces that rule and needs owner review.

`before-after-light.png` / `before-after-dark.png`: Toggle, Dual Range, selected
Chip remove, Comparison Slider grip, Glow Button field, Particle Word, Confetti
Cannon, Kaleidoscope, Use Cases row, Input in error; top row before, bottom after.

Screen readers, Safari/Firefox and forced-colors mode are not verified.
