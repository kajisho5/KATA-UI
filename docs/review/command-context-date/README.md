# Command / Context Menu / Date Picker instance batch

Base: main `839b05d` (after PR #24). The first three failing entries in the requested
priority order were Command, Context Menu and Date Picker. All three had both JS
checks failing. Their release status remains **Beta**.

## Audit

| Result | Before | After |
|---|---:|---:|
| Mold Verified | 97 / 164 | 100 / 164 |
| UI | 64 / 121 | 67 / 121 |
| Lab | 33 / 43 | 33 / 43 |
| js-single-instance findings | 19 | 14 |
| js-global-bindings findings | 52 | 37 |
| token-values | 0 | 0 |
| focus-visible findings | 132 | 125 |
| accessible-label findings | 1 | 0 |

The checker and shared tokens are unchanged. Newly working keyboard targets use
`var(--k-ring)`. Date Picker gains a visible label, automatically linked by JS,
and an accessible-name fallback before JS runs. Its icon/padding use logical
properties. No shared tokens were added. All three pass static failure checks;
existing spacing/type warnings remain. This does not make them Stable.

## Source and distribution

`build.py` reads each component's CSS, JS, preview, metadata and optional examples;
it emits the component pages, downloadable files, registry and model-facing data.
It does not rewrite these component originals. Regenerate instead of editing the
registry, llms, MCP payloads or generated pages by hand.

Each copied script is standalone: IIFE, all-instance initialization, ready guard,
collision-checked generated IDs, preserved application IDs, and per-instance state.
Existing data hooks and classes remain. Samples contain no fixed id/for/controls.
All keyboard selection handlers guard composition events, `isComposing`, keyCode
229 and the event turn immediately following compositionend.

## Behavior differences

- Command retains a native modal dialog. Arrow movement now wraps, filtering
  reports counts and zero results, and the input owns listbox active-descendant
  state. `kata-command-select` reports the selected item; the app supplies the
  action. Escape uses native cancel/close and honors application preventDefault.
  Cmd/Ctrl+K targets the associated focused trigger, then the first palette.
- Context Menu adds roving focus, Up/Down/Home/End, prefix search and edge flipping.
  Escape, Tab and selection close and return focus to the trigger; outside
  pointer/focus departure closes without stealing the user's new focus. Window blur closes all open menus through one guarded window listener; null
  focusout does not close it. Keyboard access still mirrors
  right-click; applications must keep visible alternatives to these actions.
- Date Picker adds the implemented grid keyboard model, polite month names,
  full date labels, selection/current-date states, month-end clamping, and a
  complete six-row calendar. Horizontal arrows follow visual direction: in RTL, Left advances one day
  and Right goes back one day. Native non-modal behavior is retained.
- These panels had no exit animation in main. The close helper supports end
  events, duration/delay/iteration-based timeout fallback and immediate zero
  duration completion. Reopen cancels the old listeners/timer. Native Command
  Escape has no exit animation and retains native cancel behavior.

## Evidence

Run:

```sh
python3 -m tools.verify_command_context_date
python3 -m unittest discover -s tests -p 'test_*.py'
node --check components/command/command.js
node --check components/context-menu/context-menu.js
node --check components/date-picker/date-picker.js
python3 check.py --json mold-results.json
python3 -W error::SyntaxWarning build.py
python3 -m tools.mold_ratchet --report mold-results.json
python3 -m tools.mold_publish --check
python3 -m tools.verify_mold_distribution
```

`results.json` records nine Chromium cases: three copied instances, one RTL,
script loaded twice, normal motion, multiplier zero and OS reduced motion.
The tests cover paragraphs, null relatedTarget, per-component window-blur policy, internal focus,
keyboard navigation and selection, IME event guards, unique/pre-existing IDs,
edge positioning, RTL screen coordinates and next-day movement, single window
blur listener and dismissal, native cancel veto, month-end clamping, timeout fallback and
reopening during a pending exit. Console errors: zero. Screenshots show each
case; `*-light/dark-before/after.png` compare a single instance against main.
Date Picker's visible label and keyboard focus treatment intentionally change;
its colors, radii, shadows and timing tokens are unchanged.

Real Japanese IME, screen readers, Firefox and Safari remain unverified.
Synthetic composition events do not replace real IME testing.

## Remaining JS failures (12 targets)

In requested priority order: tag-input, input-otp, data-table, file-upload,
color-picker, carousel, split-panel, reorder, follow-frame, blocks/pricing,
blocks/site-header, blocks/use-cases. Input OTP and Use Cases fail global bindings
only; the other ten fail both JS checks.
