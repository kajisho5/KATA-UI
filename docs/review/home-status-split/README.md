# Home page Stable / Beta split

## Change
- `build.py`: `status_split(comps)` counts `meta.json` status values; the hero line now reads `136 components (0 stable · 136 beta) · 21 blocks · 7 templates`, with each count linking to the filtered catalog. No number is typed by hand.
- The components index accepts `?status=stable|beta` and selects that filter on load.
- 13 parts carried a legacy `stable` label without the Phase 1 release procedure (checks plus a recorded screen-reader pass): bottom-navigation, button-group, calendar, collapsible, descriptions, input-group, navigation-menu, result, scrollspy, shine-text, time-picker, transfer, typeset. They are now `beta`, as earlier legacy labels were in T4 (owner decision, option A).
- `tests/test_home_status_split.py`: the hero counts equal the meta.json counts, and any `stable` part must have `docs/review/<slug>/screen-reader.md`.

## Evidence
- Built site: hero line before `136 components · 21 blocks · 7 templates`, after `136 components (0 stable · 136 beta) · 21 blocks · 7 templates` (light and dark).
- Clicking "136 beta" opens `/components/?status=beta` with the Beta filter selected: 136 cards shown, 0 non-beta. `/components/?status=stable` selects Stable and shows the empty-result message. 0 page errors.
- Screenshots: `before-after-light.png`, `before-after-dark.png`.

## Not verified
- Screen readers, Safari, Firefox and real devices.
