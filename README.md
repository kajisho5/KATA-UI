<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="logo/logo-white.svg">
    <img src="logo/logo.svg" width="96" alt="KATA UI">
  </picture>
</p>

<h1 align="center">KATA UI</h1>

<p align="center"><b>Vanilla HTML, CSS and JS. Copy the code. Own the design.</b><br>
136 components, 21 blocks and 7 templates — every part cast from a single design-token mold.<br>
No framework · No build step · No runtime</p>

<p align="center">
  <a href="#quick-start"><b>Quick start</b></a> ·
  <a href="https://kata-ui.dev/components/">Components</a> ·
  <a href="https://kata-ui.dev/blocks/">Blocks</a> ·
  <a href="https://kata-ui.dev/templates/">Templates</a> ·
  <a href="https://kata-ui.dev/docs/">Docs</a> ·
  <a href="https://www.npmjs.com/package/@kajisho5/kataui">npm</a>
</p>

<p align="center">
  <a href="https://www.npmjs.com/package/@kajisho5/kataui"><img src="https://img.shields.io/npm/v/@kajisho5%2Fkataui" alt="npm"></a>
  <a href="https://github.com/kajisho5/KATA-UI"><img src="https://img.shields.io/github/stars/kajisho5/KATA-UI" alt="GitHub stars"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green" alt="MIT"></a>
  <a href="https://kata-ui.dev/docs/why-vanilla/"><img src="https://img.shields.io/badge/vanilla-only-18181b" alt="Vanilla only"></a>
</p>

```bash
npx @kajisho5/kataui add button
```

<p align="center">
  <img src="https://kata-ui.dev/ogp.png" alt="KATA UI — the four-quadrant mark on an Asanoha lattice">
</p>

Browse component previews and full-page [dashboard](https://kata-ui.dev/templates/dashboard/demo/), [inbox](https://kata-ui.dev/templates/inbox/demo/) and [checkout](https://kata-ui.dev/templates/checkout/demo/) examples. Each template lists its dependencies.

Copy a button, form or table into your project. Edit the files yourself. No framework, no build step.

A zero-dependency CLI ([`@kajisho5/kataui`](https://www.npmjs.com/package/@kajisho5/kataui)) installs parts and their dependencies. AI tools can fetch the source from the registry.

If it renders HTML, it works: plain files, Astro, Laravel Blade, Django and Rails templates, WordPress themes, or one island inside a React app.

<!-- mold-summary:start -->
[Mold Verified 103 / 164 · UI 70 / 121 · Lab 33 / 43](https://kata-ui.dev/audit/)

164 parts. Static checks only. Updated 2026-11-05 (Asia/Tokyo).
Read the audit for each part's pass, fail and warning results. Browser behavior needs separate testing.
<!-- mold-summary:end -->

---

## Quick start

```bash
# 1. write the design tokens into ./kata (every part reads them)

<!-- mold-version:start -->
moldVersion: 2. Before copying a part, check the tokens.css mold header against requiresMold; update the mold before using newer parts. Unversioned tokens.css is legacy v1.
<!-- mold-version:end -->
npx @kajisho5/kataui init

# 2. add parts — dependencies come along on their own
npx @kajisho5/kataui add button
npx @kajisho5/kataui add data-table        # pulls in badge + button first
npx @kajisho5/kataui add login             # blocks and templates install the same way

# 3. load the files, tokens first, and paste the example HTML in as it is
```

```html
<link rel="stylesheet" href="kata/tokens.css">
<link rel="stylesheet" href="kata/components/button/button.css">
```

Prefer no terminal at all? Open the part on [kata-ui.dev](https://kata-ui.dev/components/) and copy its three files from the page. Same code, same mold — the CLI is a faster pair of hands, not a different product.

## What's inside

**136 components** in eight groups:

| Group | Parts | What lives there |
|---|---:|---|
| Form & Input | 27 | Button, Input, Select, Combobox, Date Picker, OTP Field, Tag Input, File Upload, Switch, Slider |
| Display & Media | 26 | Card, Data Table, the charts (line, bar, donut, radar, funnel…), Avatar, QR Code, Calendar |
| Motion | 31 | Aurora, Spotlight, Text Reveal, Marquee, Counter, Converge — the ambient line |
| Layout & Navigation | 16 | Sidebar, Command Menu, Tabs, Breadcrumb, Pagination, Dock |
| KATAYABURI | 12 | 型破り — deliberate mold-breakers: Newton's Cradle, Warp Tunnel, Noren, Goo Tabs |
| Overlays & Dialogs | 10 | Modal, Drawer, Popover, Tooltip, Context Menu |
| Feedback & Status | 9 | Toast, Alert, Progress, Skeleton, Empty State |
| Japan | 5 | Wagara (100 tiling patterns), Hanko, Kintsugi Card, Tategaki |

**21 blocks** — whole sections composed from the parts: App Shell, Cookie Consent, CTA Band, FAQ, Filter Toolbar, Integrations, Invoice, Kanban, Login, Logo Cloud, Order Confirmation, Plan Compare, Pricing, Roadmap, Settings, Site Footer, Site Header, Stat Cards, Team Grid, Testimonials, Use Cases.

**7 templates** — whole pages: Blog Article, Checkout, Dashboard, Inbox, Landing Page, Product Page, Settings. Every template has a [live full-page demo](https://kata-ui.dev/templates/) built from the parts it lists.

**370 glyphs** — 150 UI icons drawn on one mold (24 grid, 1.7 stroke, square caps, bevel joins — nearest kin is [Lucide](https://lucide.dev), which sits comfortably alongside) and 220 brand marks in official artwork, grouped by job: social, AI, development, commerce, platforms, cloud.

## The mold

`KATA.md` defines the UI and Lab policies. `check.py` runs static checks.
Read each part's pass, fail and warning results before using it.

```bash
python3 check.py --json mold-results.json
python3 build.py
```

## Theming and dark mode

Load `tokens.css` before component styles. `data-theme="dark"` selects dark theme values. UI and Lab use different token policies; inspect the audit for literal values and other open findings.

## Built for machines

The catalog is published for tools as well as people, all generated from the same source folders as the site:

- **Registry** — [`registry.json`](https://kata-ui.dev/registry.json) in the shadcn registry format: names, files, dependencies.
- **CLI** — [`@kajisho5/kataui`](https://www.npmjs.com/package/@kajisho5/kataui) on npm, or the same single file [downloaded directly](https://kata-ui.dev/cli/kata-ui.mjs). Zero dependencies, Node 18+.
- **MCP server** — a read-only, zero-dependency server (`mcp/kata-ui-mcp.mjs`) that lists, searches and fetches parts from the registry.
- **AI Skill** — [`skill/SKILL.md`](skill/SKILL.md) teaches coding models the catalog's shape, so an assistant asked for "a sidebar" installs this Sidebar instead of inventing one.
- **llms.txt** — the catalog as prose for models that read the web: [llms.txt](https://kata-ui.dev/llms.txt) and [llms-full.txt](https://kata-ui.dev/llms-full.txt).

## Repository layout

| Path | What it is |
|---|---|
| `components/` | The registry — one folder per component (meta, preview, CSS, JS) |
| `icons/` | The icon set, one SVG per icon (brand marks in `icons/brands/`) |
| `blocks/`, `templates/` | Composed sections and whole pages |
| `cli/` | The kataui CLI (a single zero-dependency Node file) |
| `mcp/` | The read-only MCP server |
| `skill/` | SKILL.md that teaches AI assistants to build with KATA |
| `system/` | `tokens.json`, the design-system source of truth |
| `template/` | The skeleton every new component starts from |
| `KATA.md` | The production mold (how parts are made) |
| `DESIGN.md` | Positioning, design language and decisions |

## Docs

Start at [kata-ui.dev/docs](https://kata-ui.dev/docs/): Getting Started, Installation, Theming, Dark Mode, the CLI, the Registry, framework guides (React, Next.js, Astro and more), and the changelog — which is also kept here as [CHANGELOG.md](CHANGELOG.md). Current release: **v1.0.0**.

## License

MIT. The components, icons and tokens are free to use, including commercially. Blocks and templates will be sold separately as a one-time purchase (Pro, $129 lifetime — [pricing](https://kata-ui.dev/pricing/)); everything in this repository stays MIT.

[Development roadmap](docs/ROADMAP.md)
