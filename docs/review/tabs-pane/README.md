# Tabs panel width (Torture Test follow-up)

## Change
`.tabpane` had `width:100%` with `padding` and a 1px border on the default content-box, so every panel was 34px wider than its container (474px in a 440px column in `tests/tabs-multi.html`; 9px past its stage in `tests/torture.html`). It now sets `box-sizing:border-box`, and `margin-top` became `margin-block-start`.

## Evidence
- `python3 -m tools.verify_torture`: check C (part overflow) for Tabs drops from 8/8 conditions to 0; all six checks are now 0 in all 8 conditions. `docs/review/torture/results.json` no longer lists Tabs, so the CI ratchet now fails if the overflow returns.
- `tests/tabs-multi.html`: panel width 474px → 440px, container 440px, light and dark.
- Screenshots: `before-after-light.png`, `before-after-dark.png` (the right edge of the panel was cut off before).

## Not verified
- Screen readers, Safari and Firefox.
