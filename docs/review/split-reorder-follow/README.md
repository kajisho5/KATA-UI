# Split Panel / Reorder / Follow Frame

Main base: `47298c57dde8a6a61272c6180c90dc077a7f8647`, after merged PR #29.
These are the first three JS-failing parts in the HANDOFF T1 order. Split Panel
is a UI part; Reorder and Follow Frame are Lab (Motion) parts. All three failed
both JS rules; Reorder also failed focus-visible.
Their release status stays **Beta**. No shared tokens or checker rules change.

| Audit | Before | After |
|---|---:|---:|
| Mold Verified | 106 / 164 | 109 / 164 |
| UI | 73 / 121 | 74 / 121 |
| Lab | 33 / 43 | 35 / 43 |
| js-single-instance findings | 7 | 3 |
| js-global-bindings findings | 18 | 5 |
| focus-visible findings | 112 | 111 |
| spacing-values / type-values (warn) | 891 / 638 | 891 / 638 |
| token-values | 0 | 0 |

## Source and behavior

Each script is an IIFE that initializes every root once (`data-kata-ready`),
checks generated IDs for collisions and keeps IDs the application supplied.
None registers a document or window listener; Follow Frame's old window
`resize` listener became one ResizeObserver per zone. Existing classes and
data hooks keep working; nothing is renamed.

- **Split Panel.** The handle stays a focusable `role=separator`, now with
  `aria-controls` for the first pane and `aria-valuemin/max` read from the
  markup (default 20–80). Left/Right move the handle in the arrow's visual
  direction, so in RTL (first pane on the right) ArrowLeft grows that pane.
  Shift moves 10, Home/End jump to the limits. `aria-orientation="horizontal"`
  on the handle stacks the panes (`.k-split-v`, added by the script) and uses
  Up/Down. Dragging uses pointer capture and RTL-aware math; one
  `kata-split-panel-change` fires per keyboard step and per finished drag.
  The first pane now uses `box-sizing:border-box`: before, its 30px padding
  was added to the percentage, so a dragged handle landed 30px away from the
  pointer and 38% rendered as 43%. The focused handle also gets `--k-ring`.
- **Reorder.** HANDOFF described a drag-to-sort list (Space lifts, Escape
  cancels, pointer capture). The actual part is an auto re-ranking leaderboard
  with sample scores and no dragging, so that spec was not applied; turning it
  into a sortable list would be a different part. Instead: autoplay pauses
  while a pointer or keyboard focus is inside, a new Pause toggle
  (`data-rank-pause`, aria-pressed) stops it (WCAG 2.2.2), and it never starts
  with reduced motion. `data-rank-autoplay="off"` starts paused. Manual
  re-ranks are announced in a status region; autoplay is not. FLIP duration
  scales with `--k-mscale` and uses `--k-ease-in-out`; zero or reduced motion
  creates no animations. `kata-reorder-change` reports the order and source.
- **Follow Frame.** Each zone follows its own pointer. The animation loop runs
  only while the frame travels and stops when it arrives (before, every page
  ran a permanent requestAnimationFrame loop). Reduced motion keeps the frame
  parked in the center; `--k-mscale: 0` jumps without easing. The hint uses
  `inset-inline-start`.

## Verification

```sh
node --check components/split-panel/split-panel.js
node --check components/reorder/reorder.js
node --check components/follow-frame/follow-frame.js
python3 check.py --json mold-results.json
python3 -m tools.verify_split_reorder_follow
python3 -m unittest discover -s tests -p 'test_*.py'
python3 -W error::SyntaxWarning build.py
python3 -m tools.mold_ratchet --report mold-results.json --reference-ref <main SHA>
python3 -m tools.verify_mold_distribution
python3 -m tools.mold_publish --check
NODE_PATH=<axe-core and playwright> node tools/check-browser.cjs split-panel reorder follow-frame
```

`results.json` and the screenshots cover nine Chromium cases: three copies, one
RTL, the script loaded twice (then again), light with normal motion, dark with a
zero multiplier, and dark with reduced motion. Split Panel also adds a late
stacked copy. Reorder runs on Playwright's virtual clock with a seeded
Math.random, so autoplay timing and scores are reproducible. Checks include
independent state, unique and preserved IDs, synthetic composition keys
(keyCode 229), body clicks, null-relatedTarget focusout and window blur, visual
handle movement, drag results, event counts and animation counts. Console
errors: zero. The browser audit reports the same results as before the change:
Follow Frame 0; Split Panel `heading-order` (h5 pane titles) and Reorder
`color-contrast` (dim score digits on the glass panel) both predate it.

Real Japanese IME, screen readers, Firefox/Safari and touch dragging on real
devices are not verified. No part is promoted to Stable.

## Remaining JS failures (3 targets)

blocks/pricing, blocks/site-header, blocks/use-cases. Use Cases fails only global
bindings; the other two fail both JS rules.
