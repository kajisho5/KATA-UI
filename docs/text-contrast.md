# Text contrast follow-up

PR #19 was corrected, passed Checks and merged. This follow-up is based on main ee7d179. The current app changes only shared token values for muted text and light yellow text; the role correction below is a diagnostic proposal, not applied component code.

## Causes

| Text | Foreground token | Background | Original dark contrast |
|---|---|---|---:|
| Accent button | --k-on-color (#fff) | --k-accent (#33a6b8) | 2.88:1 |
| Input error / Dropdown danger | --k-danger (#c9171e) | --k-bg (#18181b) | 3.06:1 |
| Placeholder / hint / card note / menu heading | --k-ink-3 (#71717a) | --k-bg (#18181b) | 3.67:1 |
| Card footer | --k-ink-3 (#71717a) | --k-bg-soft (#27272a) | 3.08:1 |

Input errors and danger actions consume a paint token also used as the filled danger-button background. The existing --k-danger-ink is already the intended bright dark-theme text color, but these consumers do not use it. --k-on-color is also used on fixed dark Lab surfaces, so changing it globally to dark text would break those surfaces. Core vermilion is unrelated and unchanged.

## Safe value changes already applied

| Existing token | Light before → after | Dark before → after | Reason |
|---|---|---|---|
| --k-ink-3 | #a1a1aa → #71717a | #71717a → #90909a | Placeholders/hints/notes; light was already 2.56:1 (footer 2.39:1), so a light correction is necessary too |
| --k-yamabuki-ink | #9b6e23 → #876019 | #f6c555 (unchanged) | Light Badge text was already 4.20:1 |

All values are canonical in system/tokens.json, generated into tokens.css, and rendered on design-system. Mode switches use those same semantic definitions. No component CSS or JS is changed in the applied patch.

## Why danger needs a decision

At the current #18181b background, a danger text color needs relative luminance ≥0.2167 for 4.5:1. A background carrying white text needs luminance ≤0.1833. These intervals do not overlap. One --k-danger value cannot satisfy both roles on the existing background.

A pure token-only alternative would require changing the basic dark background to black: #e12b32 would give 4.59:1 as text on black and 4.57:1 with white text on it. That changes the theme and still requires resolving existing hover-role conflicts. It is not silently applied.

## Accent alternatives

| Candidate | Pair | Contrast |
|---|---|---:|
| Dark text on current accent | #18181b / #33a6b8 | 6.15:1 |
| Darkened accent with white text | #fff / #247c8c | 4.84:1 |
| Current white text on accent | #fff / #33a6b8 | 2.88:1 |

The role proposal uses a separate common --k-on-accent (light white / dark ink), keeps generic --k-on-color white for other filled/dark surfaces, and darkens the light accent because its original white-text pair was already below 4.5:1. It also separates the danger hover surface from danger-ink text. Current body background and core stay unchanged.

The exact generic role patch is [shared-role-proposal.patch](review/text-contrast/shared-role-proposal.patch). It maps all color:var(--k-danger) text uses to --k-danger-ink, all danger-ink background uses to a common hover surface, and accent-surface text to --k-on-accent. It contains no per-component RGB values. It is **not applied**. Its default-color preview passes the 12 core components and the two button hover states. Foundry custom-palette behavior still needs implementation/verification if this option is selected.

## Core 12: before / safe values / proposed roles

Eligible minima exclude actual disabled controls, which are listed separately. All numbers are from actual rendered computed colors and ancestor alpha composition; no Mold checker or allowlist is changed.

| Component | Light before | Light safe changes | Light role proposal | Dark before | Dark safe changes | Dark role proposal |
|---|---:|---:|---:|---:|---:|---:|
| button | 2.88:1 | 2.88:1 | 4.84:1 | 2.88:1 | 2.88:1 | 5.79:1 |
| input | 2.56:1 | 4.83:1 | 4.83:1 | 3.06:1 | 3.06:1 | 5.60:1 |
| select | 17.72:1 | 17.72:1 | 17.72:1 | 16.12:1 | 16.12:1 | 16.12:1 |
| card | 2.39:1 | 4.51:1 | 4.51:1 | 3.08:1 | 4.71:1 | 4.71:1 |
| badge | 4.20:1 | 5.26:1 | 5.26:1 | 5.81:1 | 5.81:1 | 5.81:1 |
| modal | 7.73:1 | 7.73:1 | 7.73:1 | 6.91:1 | 6.91:1 | 6.91:1 |
| drawer | 7.73:1 | 7.73:1 | 7.73:1 | 6.91:1 | 6.91:1 | 6.91:1 |
| dropdown | 2.56:1 | 4.83:1 | 4.83:1 | 3.06:1 | 3.06:1 | 5.60:1 |
| popover | 7.73:1 | 7.73:1 | 7.73:1 | 6.91:1 | 6.91:1 | 6.91:1 |
| tabs | 6.55:1 | 6.55:1 | 6.55:1 | 5.81:1 | 5.81:1 | 5.81:1 |
| toast | 16.54:1 | 16.54:1 | 16.54:1 | 13.55:1 | 13.55:1 | 13.55:1 |
| tooltip | 16.54:1 | 16.54:1 | 16.54:1 | 13.55:1 | 13.55:1 | 13.55:1 |

## Button hover pairs

| Theme | State | Text | Before | Safe changes | Role proposal |
|---|---|---|---:|---:|
| light | accent-hover | Accent | 7.09:1 | 7.09:1 | 7.09:1 |
| light | danger-hover | Delete | 6.26:1 | 6.26:1 | 6.26:1 |
| dark | accent-hover | Accent | 1.90:1 | 1.90:1 | 9.33:1 |
| dark | danger-hover | Delete | 2.14:1 | 2.14:1 | 6.26:1 |

## Remaining visible text below 4.5:1 after safe values (40 components)

| Theme | Component | Text | Contrast |
|---|---|---|---:|
| light | button | Accent | 2.88:1 |
| light | hover-card | Aoi Kimura | 2.88:1 |
| dark | button | Accent | 2.88:1 |
| dark | input | Please enter your full name | 3.06:1 |
| dark | dropdown | Delete | 3.06:1 |
| dark | field | Required | 3.06:1 |
| dark | field | That address is missing its domain. | 3.06:1 |
| dark | context-menu | Delete | 3.06:1 |

## Disabled controls (excluded from threshold, numbers retained)

| Theme | Component | Text | Before | Safe changes |
|---|---|---|---:|---:|
| light | button | Disabled | 2.92:1 | 2.92:1 |
| light | button | Saving… | 2.92:1 | 2.92:1 |
| light | select | Availability | 17.72:1 | 17.72:1 |
| light | select | Locked | 3.38:1 | 3.38:1 |
| light | radio | Lifetime (sold out) | 2.56:1 | 4.83:1 |
| dark | button | Disabled | 4.19:1 | 4.19:1 |
| dark | button | Saving… | 4.19:1 | 4.19:1 |
| dark | select | Availability | 16.12:1 | 16.12:1 |
| dark | select | Locked | 4.88:1 | 4.88:1 |
| dark | radio | Lifetime (sold out) | 3.67:1 | 5.60:1 |


[Images, JSON, precise method and un-applied proposal patch](review/text-contrast/README.md).
