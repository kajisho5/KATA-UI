# T4 Input: release procedure (KATA.md contract items 11, 14–16)

Main base: `c04cf6015dbb5c638e8b4ef87ba95e0178e3979d` (after #44, Button).
Input has no JavaScript.

## What changed

- **Samples without fixed IDs** (`preview.html`, `examples.html`, `combos.html`):
  each `<label for>` + `<input id>` pair became a label that wraps its input, so
  a pasted sample can appear twice (item 14). A new rule
  `.field label:has(> .input,> .searchwrap)` stacks the text above the field with
  the same 4px gap; rendered label/field layout is pixel-identical. Labels that do
  not wrap an Input (Select's inline samples, `<label for>` in other parts) are
  unaffected.
- **Error state:** sample errors carry `aria-invalid="true"`; the CSS styles it
  like `.errb` (kept, not renamed).
- **Focus:** `.input:focus` → `.input:focus-visible` (the #12 remainder). Text
  inputs match `:focus-visible` on every focus, including a click.
- **Disabled was indistinguishable** from enabled (same text and background).
  Now: soft background, muted text, no shadow, `not-allowed` cursor. Read-only
  gets the soft background and keeps its focus ring (the browser test caught a
  first version that removed it).
- **Search icon:** `left:10px` → `inset-inline-start: var(--k-space-3)` (12px,
  RTL-aware), `pointer-events:none`, and `aria-hidden="true"` in samples.
- `tests/input-multi.html` (three sets, set 3 RTL), `tests/test_input_browser.py`
  and `tools/verify_input.py`; CI runs the browser test after Chromium installs.
- `meta.json`: **beta** (was a legacy stable label) with the measured behavior
  and the missing manual checks.

## Text contrast (Chromium, `input-text.json`)

Set 1; sets 2 and 3 (RTL) match within 0.05. Enabled text must reach 4.5:1.

| Text | Light | Dark |
|---|---:|---:|
| label | 17.72 | 16.12 |
| value | 17.72 | 16.12 |
| placeholder | 4.83 | 5.6 |
| hint | 4.83 | 5.6 |
| error | 6.26 | 7.48 |
| focused value | 17.72 | 16.12 |
| read-only value | 16.54 | 13.55 |
| disabled value | 4.51 | 4.71 |

Keyboard focus: `verify_focus_ring --check` measures the Input stops at 3:1 or
more in both themes, none clipped.

## Browser test (`tests/test_input_browser.py`)

Per set: no `id`/`for`; all 15 inputs named by their own label; clicking a
label focuses its own input; typing works; focus draws a ring; the invalid
border differs from the normal one; disabled is muted, `not-allowed` and skipped
by Tab while read-only is reached and shows the ring; the search icon is left of
centre in LTR and right of centre in RTL. At 375px the field is at least 16px and
the page does not scroll sideways. Console clean.

## Before / after

`before-after-{light,dark}.png`: top, the preview (only the search icon moves
2px); bottom, the disabled and read-only example.

## Why beta / not verified

The hint and error text are not linked with `aria-describedby`, because that
needs unique IDs; the meta text tells users to add them. Item 16 needs recorded
manual checks that this container cannot run: a screen reader and real IME
input (Japanese conversion with Enter to confirm). Also not verified: Safari,
Firefox, real devices, 200% zoom.
