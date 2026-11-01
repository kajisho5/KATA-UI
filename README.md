# KATA UI

**Every part is cast from a single mold — kata, the Japanese discipline of the form.**

Practical UI components in plain HTML, CSS and JavaScript. No framework, no build step, no runtime. Copy a part, paste it into your project, and the code is yours.

**Live site: [kata-ui.dev](https://kata-ui.dev)** — previews, code and docs for every part.

## What's inside

- **76 components** in six groups — Form & Input, Layout & Navigation, Overlays & Dialogs, Feedback & Status, Display & Media, and a Motion line you will not find in other libraries
- **150 icons** drawn on one mold: a 24 grid, a 2px stroke, round caps — and fully compatible with [Lucide](https://lucide.dev), which follows the same spec, for anything beyond the set
- **56 brand marks** (X, GitHub, OpenAI, Figma, Stripe, LINE and more), grouped by job: social, AI, development, commerce, platforms, cloud
- **A CLI** — `node kata-ui.mjs add button` installs parts, blocks, templates and themes from the registry, dependencies included (zero dependencies itself)
- **A design system** (`system/tokens.json`) — color, type, spacing, radius and motion scales that every part is cast from
- **13 blocks** — components composed into whole sections (sign-in, pricing, settings, app shells, integrations)
- **4 templates** — whole pages composed from parts and blocks (dashboard, settings, inbox, landing)

## Use a part

1. Take `tokens.css` once — every part reads its color, spacing and motion from it.
2. Copy the part's HTML from its page on [kata-ui.dev](https://kata-ui.dev/components/), plus its CSS (and JS, when it has one).
3. Adjust the tokens, not the parts. One change in `tokens.css` re-casts everything.

Works in plain HTML, Astro, Laravel, Django, Rails — anywhere that renders HTML.

## The mold

Every part in this repository passes one check before it ships. `KATA.md` is the production standard: folder shape, token discipline, motion limits (130–220ms, no bounce), and the icon rules. `check.py` enforces it.

```bash
python3 check.py   # verify every component against the mold
python3 build.py   # build the site into dist/
```

## Repository layout

| Path | What it is |
|---|---|
| `components/` | The registry — one folder per component (meta, preview, CSS, JS) |
| `icons/` | The icon set, one SVG per icon (brand marks in `icons/brands/`) |
| `blocks/`, `templates/` | Composed sections and whole pages |
| `cli/` | The kata-ui CLI (a single zero-dependency Node file) |
| `skill/` | SKILL.md that teaches AI assistants to build with KATA |
| `system/` | `tokens.json`, the design-system source of truth |
| `template/` | The skeleton every new component starts from |
| `KATA.md` | The production mold (how parts are made) |
| `DESIGN.md` | Positioning, design language and decisions |

## License

MIT. The components, icons and tokens are free to use, including commercially. Blocks and templates will be sold separately as a one-time purchase; everything in this repository stays MIT.
