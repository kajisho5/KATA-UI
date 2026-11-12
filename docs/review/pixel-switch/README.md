# Pixel Switch — visual and contrast evidence (2026-11-12)

Page: `tests/pixel-switch-multi.html`, first instance set, Chromium headless
(Playwright), `data-theme` set to light and dark on the root.

- `light.png`, `dark.png`: the six preview switches at rest, device scale 2.
- `morph-frames.png`: the theme switch at 0, 120, 260, 420 and 900 ms after a click
  (multiplier 1). Dots leave the sun, scatter, and land on the moon; the rim arc
  turns once and changes from yamabuki to asagi.

## Contrast (WCAG 1.4.11, non-text, 3:1)

Colors are the computed values, painted to a 1×1 canvas and read back as sRGB.
The rim is the 1px `--k-pxs-rim` line on the track edge; it carries the track
boundary, as the 1px outline does in Switch.

| Theme | State | Dots / knob | Rim / page | Knob / track | Track / page |
|---|---|---:|---:|---:|---:|
| light | theme off | 16.97 | 4.83 | 1.22 | 1.27 |
| light | theme on | 14.27 | 4.83 | 1.34 | 19.90 |
| light | other pairs off | 7.73 | 4.83 | 1.07 | 1.07 |
| light | other pairs on | 17.72 | 4.83 | 1.07 | 1.07 |
| dark | theme off | 16.97 | 3.67 | 1.22 | 13.96 |
| dark | theme on | 14.27 | 3.67 | 1.34 | 1.12 |
| dark | other pairs off | 6.91 | 5.60 | 1.19 | 1.19 |
| dark | other pairs on | 16.12 | 5.60 | 1.19 | 1.19 |

The state is shown by the icon (at least 6.91:1) and by the knob position. The
knob fill itself is close to the track fill (1.07–1.34); the knob is identified by
its icon and its drop shadow. The glow is decoration and is not measured.

Keyboard focus (`python3 -m tools.verify_focus_ring --check`, whole catalog):
448 focus stops in 100 / 165 parts, 0 below 3:1 and 0 clipped in light and dark.

Not verified: screen readers, Safari, Firefox, real devices.
