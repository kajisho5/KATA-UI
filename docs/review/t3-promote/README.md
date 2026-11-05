# T3 promotion: spacing and type checks fail for UI parts (mold v5)

Main base: `5d4163d417eb6e69a1fa79c794ae6c4fafb180e2`, after #41 (T3 line height).
This is a checker change; the owner reviews it before merge (AGENTS.md workflow).

## What changes

| Remaining UI finding | Count | Resolution |
|---|---:|---|
| `calc(var(--k-space-*) * -1)` (Avatar, Button Group, Input Group, Noren, Slider, Split Panel, Tour) | 10 | Lexer fix: `-1` is a number (CSS Syntax 3); `* 2` already passed. No allowance added. |
| Bottom Navigation `env(safe-area-inset-bottom)` | 1 | `env()` accepted in spacing for the four safe-area insets only (`environment_spacing_variables`). |
| Command `margin: 12vh auto auto` | 1 | Owner choice: `var(--k-space-16)` (64px). |
| Typeset, Blog Article inline code `font-size: .86em` | 2 | Owner choice: new shared token `--k-text-code: .86em` (mold v5). |

Then `spacing-values` and `type-values` report `fail` for UI parts and `warn` for
Lab parts (`tools/mold_rules.py`).

| | Before | After |
|---|---:|---:|
| UI spacing / type findings | 12 / 2 | 0 / 0 |
| Lab spacing / type findings (warn) | 128 / 119 | 128 / 119 |
| Parts with warnings | 91 | 80 |
| Mold Verified | 164 / 164 | 164 / 164 |

Because the promotion happens at 0 UI findings, the pass count and the
trusted-main ratchet do not drop; `mold-baseline.json` is unchanged.

## Visual evidence

- `command-before-after-{light,dark}.png`: open Command palette on a 900×900
  viewport; the dialog top moves from 108px (12vh) to 64px. At 600px tall it
  moves from 72px to 64px.
- Typeset, Blog Article and Command default previews: pixel-identical before and
  after in light and dark (`tools/capture_parts`).

## Fixtures

tests/mold/cases.json: UI raw gap/margin/padding/inset/font-size/line-height and
font shorthand now `fail`; Lab spacing and type stay `warn`; negated token passes;
raw `-4px` and `calc(4px * -1)` fail; safe-area inset passes alone, in `calc()`
and with a token fallback; a raw fallback and other `env()` names fail; `env()`
is not a type value.

Not verified: Safari/Firefox, real phones (the safe-area inset is only non-zero
on devices with a notch or home indicator).
