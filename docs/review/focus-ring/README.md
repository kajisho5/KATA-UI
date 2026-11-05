# Focus-ring visibility baseline (HANDOFF T2, step 1)

Main base: `1ec074ee3198580444fa92945e1c3f9b03d42bac`, after merged PR #31 (T1 done).
This PR adds a measurement only. No component, token or checker rule changes.

## Method

`python3 -m tools.verify_focus_ring [part ...]` renders each registry part
(components, blocks, templates; themes excluded) with its dependency CSS and JS,
the way `tools/check-browser.cjs` does, at 1100×900 with `--k-mscale: 0`. Focus
starts on a sentinel button; Tab walks up to 24 stops inside the part. For each
stop it captures the control box plus 8px, focused and then blurred, and compares
pixel by pixel:

- **changed**: a channel differs by more than 8.
- **3:1 pixels**: the focused and blurred colors of a pixel reach 3:1 contrast
  (the WCAG non-text contrast threshold used for focus indicators).
- **level**: `visible` at 12 or more 3:1 pixels, `weak` when only lower-contrast
  pixels change, `none` when nothing changes.
- **clipped**: the computed outline (width + offset) or box-shadow extent leaves
  the control box, and an ancestor with non-visible overflow or a clip-path cuts
  it. The report names that ancestor and the cut in px.

Light and dark are measured separately. `tests/test_focus_ring.py` proves the four
verdicts on fixtures (none, weak 12% ring, visible 3:1 ring, clipped ring).

## Results (`results.json`)

98 of 164 parts have Tab stops reachable from the default preview; 66 have none
(closed overlays, static display parts). 444 stops per theme.

| | Light | Dark |
|---|---:|---:|
| visible (3:1) | 64 | 288 |
| weak (changes, below 3:1) | 370 | 147 |
| none (no change) | 10 | 9 |
| parts with a weak or invisible stop | 85 | 58 |
| clipped stops (parts) | 49 (8) | 49 (8) |

By mechanism in light: the global `:where(:focus-visible)` accent outline is weak
on 235 stops and visible on 18; components' `box-shadow: var(--k-ring)` is weak on
129 stops and visible on 44 (where the component adds its own border change).
Dark inverts the outline result (238 visible, 15 weak), but `var(--k-ring)` box-shadows
stay weak on 128 stops in dark too.

### Why light is weak

- The global fallback outline uses `--k-accent` `#33a6b8`, **2.88:1** against white.
- `--k-ring` is `0 0 0 3px rgba(24,24,27,.12)`: a 12% tint, about 1.3:1 on white.

HANDOFF T2 step 2 asks to apply `box-shadow: var(--k-ring)` everywhere. With the
current `--k-ring` value that would make every ring weak in light theme. Fixing it
needs a ring color/width decision and a `--k-ring` value change (moldVersion bump),
so it is an owner decision before step 2.

### No change on focus (light)

Rating (one radio), Speed Dial actions ×3, Dropdown menu items ×4, Comparison
Slider range, Magnet button. The Dropdown and Speed Dial stops are inside closed
or collapsed menus that are still in the Tab order, which is its own defect.

### Clipped rings

Time Picker (`.k-tp-col`, 4px, 22 stops), Wagara (`.k-wag-bar`, 1px, 11),
Navigation Menu (`.k-navm-bar`, 4–17px, 8), List (`.k-list`, 3px, 3), Product Page
(`.k-tpl-pd-qty`, 3px, 2), Split Panel (`.k-split`, 2px), Comparison Slider
(`.k-cmp`, 3px), Inbox (`.k-tpl3`, 4px).

## Limits

Only stops reachable from the default preview are measured; menus, dialogs and
popovers are not opened, so their contents are not covered. Calendar, Time Picker,
Wagara and Landing hit the 24-stop limit. Pixel contrast is measured against the
crop's own blurred state, not against the page background. Animated parts are
measured with `--k-mscale: 0`. Chromium only.
