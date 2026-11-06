# Skeleton review (T4)

## Changes
- `components/skeleton/preview.html`: the outer container is `role="status"` with a visually hidden "Loading profile" label; the shapes moved into an inner `aria-hidden` wrapper. Before, the preview was fully `aria-hidden`, so nothing announced loading although meta.json asked for a status container.
- `components/skeleton/skeleton.css`:
  - `.k-sk-status` visually hidden label (1px box, `clip-path:inset(50%)`);
  - `.k-sk:dir(rtl){animation-direction:reverse}` so the shimmer follows the reading direction.
- `components/skeleton/meta.json`: accessibility text describes the above.

## Evidence
- `tests/test_skeleton_browser.py` over `tests/skeleton-multi.html` (three sets, third `dir="rtl"`): 3 status nodes, 3 "Loading profile" texts, every `.k-sk` inside `aria-hidden`, label box ≤ 1px², animation direction normal/normal/reverse, animation `none` under reduced motion, 0 console errors. With main's CSS the test fails (label box 7600px²).
- Screenshots of main and this branch with reduced motion: pixel-identical in light and dark (`ImageChops.difference(...).getbbox()` is `None`).

## Not verified
- Screen readers (VoiceOver, NVDA), Safari and Firefox.
- Replacing the skeleton with content: the preview is static.
