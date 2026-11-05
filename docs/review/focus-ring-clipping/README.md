# Clipped focus rings (HANDOFF T2, step 3 — part 2)

Main base: `9b3ecf97faa8a21b0996240f564696339afa1e7b`, after #35.

## Changes

Controls flush against an ancestor that clips overflow (or scrolls) now draw the
ring inside: `outline:2px solid var(--k-ink);outline-offset:-2px`. On an ink
(selected) background the inner ring uses `--k-bg`.

| Part | Clipped by | Fix |
|---|---|---|
| Stepper buttons | `.k-stepper` | `box-shadow: inset var(--k-ring)` only insets the first layer since mold v3's two-layer ring (#34), so the ink layer leaked out and was cut; now an inner outline |
| Time Picker options | scrolling `.k-tp-col` | inner outline; selected option uses `--k-bg` |
| Navigation Menu | `.k-navm-bar` had `overflow-x:auto` | **the open panel was clipped completely** — the preview showed an empty card while its links stayed in the Tab order. The bar now wraps (`flex-wrap:wrap`) instead of scrolling; the panel renders. Phone-width screenshot included |
| Split Panel handle | `.k-split` | inner outline instead of the 4px ring |
| List rows | `.k-list` | inner outline |
| Wagara filter buttons | `.k-wag-bar` | inner outline; the active button uses `--k-bg` |
| Comparison Slider input | `.k-cmp` | the transparent input draws no ring (#35 moved focus to the grip) |
| Product Page quantity buttons | `.k-tpl-pd-qty` | inner outline |
| Inbox reply field | `.k-tpl3` | inner outline instead of the 4px ring |

Navigation Menu metadata no longer claims that Escape returns focus to the
button; the script does not do that.

## Measured (`tools/verify_focus_ring.py`, 437 Tab stops)

| | after #35 | now |
|---|---:|---:|
| clipped stops (parts), each theme | 52 (9) | **0 (0)** |
| below 3:1, each theme | 1 (Rating, not measurable) | 1 (same) |

Static checker: 116 → 120 (Comparison Slider, List, Wagara, Product Page now pass
focus-visible). `tools/verify_split_reorder_follow.py` now expects the Split Panel
handle's inner outline instead of a box-shadow.

`before-after-light.png` / `before-after-dark.png`: first focused control of
Stepper, Time Picker, Split Panel, List, Wagara, Product Page quantity and Inbox
reply (top before, bottom after). For Time Picker and Wagara the first Tab stop is
the text field; the options/buttons are covered by the measurement above.
`navigation-menu-before-after.png`: before (900px, 360px), after (900px, 360px).

Not verified: Safari/Firefox, screen readers, real phones. At 360px the open panel
(min-width 300px) reaches the card edge; a narrow-screen drawer is outside this PR.
