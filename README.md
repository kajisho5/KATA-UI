<img src="logo/logo.svg" width="64" height="64" alt="KATA UI">

# KATA UI

**Every part is cast from a single mold — kata, the Japanese discipline of the form.**

Practical UI components in plain HTML, CSS and JavaScript. No framework, no build step, no runtime. Copy a part, paste it into your project, and the code is yours.

**Live site: [kata-ui.dev](https://kata-ui.dev)** — previews, code and docs for every part.

**Current release: v1.0.0** — see [CHANGELOG.md](CHANGELOG.md).

## What's inside

- **136 components** in eight groups — Form & Input, Layout & Navigation, Overlays & Dialogs, Feedback & Status, Display & Media, Motion, KATAYABURI (型破り, deliberate showpieces) and Japan (wagara, hanko, kintsugi, noren, tategaki)
- **150 icons** drawn on one mold: a 24 grid, a 1.7px stroke, square caps and bevel joins — the nearest kin is [Lucide](https://lucide.dev) (24 grid, round), which sits comfortably alongside for anything beyond the set
- **220 brand marks** (X, GitHub, OpenAI, Figma, Stripe, LINE and more), grouped by job: social, AI, development, commerce, platforms, cloud
- **A CLI** — `npx kataui add button` installs parts, blocks, templates and themes from the registry, dependencies included (zero dependencies itself)
- **A design system** (`system/tokens.json`) — color, type, spacing, radius and motion scales that every part is cast from
- **21 blocks** — components composed into whole sections (sign-in, pricing, settings, app shells, kanban, invoices)
- **7 templates** — whole pages composed from parts and blocks (dashboard, settings, inbox, landing, checkout, product, blog)

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
