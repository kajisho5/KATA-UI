# Focus rule: shared-floor cancellation instead of per-part restatement (HANDOFF T2, step 4–5)

Main base: `5fcba9ea2e18344926a20d285160c42dac60736d`, after #36.
**Checker policy change: owner review required before merge** (AGENTS.md workflow).

## Rule change (tools/mold_rules.py, check.config.json)

Before: every interactive control needed a matching `:focus-visible` selector in its
own or dependency CSS, or a `:where(...):focus-visible{box-shadow:var(--k-ring)}`
shared rule. The real tokens.css floor (an outline) never qualified, and any
matching `:focus-visible` rule counted, even `outline:none` alone.

After (KATA.md, Focus):

1. **Own ring:** a matching `:focus-visible` / `:focus` rule that draws a ring
   (box-shadow, visible outline or outline color), or a `.host:has(x:focus-visible)`
   rule on an ancestor host. A rule that only removes the outline is not evidence.
2. **Shared floor:** the tokens.css floor (`outline` with `var(--k-ink)`, new
   `global_focus_outline_tokens`) covers a control unless a part rule that applies
   at rest or on focus removes the outline for it.

Why this does not weaken inspection: the floor's visibility is measured, not
assumed. `tools/verify_focus_ring.py --check` now runs in CI (mold.yml installs
Playwright Chromium from tools/agent-requirements.txt) and fails on any Tab stop
below 3:1 or clipped, in light and dark. The tool now measures a visually hidden
radio/checkbox through its label (Rating), so there are no unmeasured stops.

Fixtures: 9 per-element cases keep their meaning with `no_focus_floor` (the harness
strips the generated floor); 8 new cases cover the floor, cancellation, a
cancel-only focus rule, cancel + replacement, `:focus`, hover-only removal and
`:has()` host matching. `tests/test_focus_ring.py` adds the label case.

## Before / after

| | Before (main 5fcba9e) | After |
|---|---:|---:|
| Mold Verified | 120 / 164 | **164 / 164** |
| UI / Lab | 81 / 39 | 121 / 43 |
| focus-visible findings | 93 | 0 |
| spacing-values / type-values (warn) | 891 / 638 | 891 / 638 |
| Browser: Tab stops below 3:1 (light / dark) | 1 / 1 (Rating, unmeasured) | **0 / 0** |
| Browser: clipped stops | 0 | 0 |

No component CSS changes in this PR. The 44 parts that now pass were already
measured visible in the browser; they failed only because they did not restate
the floor. Measured T2 history: below 3:1 in light 380 (#32) → 20 (#34) → 1 (#35)
→ 0 (this PR); clipped 49 → 52 → 52 → 0 (#36).

Parts whose focus ring was not visible at the start of T2 are listed in
docs/review/focus-ring/results.json (#32 baseline); each was fixed in #33–#36.

## Limits

Chromium only. Only Tab stops reachable from each default preview are measured;
closed menus, dialogs and popovers are not opened. The static rule follows
selector text, not the computed cascade. Spacing and type values are still
warnings (T3). Mold Verified covers static checks; it is not a Stable label.
