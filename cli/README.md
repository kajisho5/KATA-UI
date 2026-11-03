<p align="center">
  <img src="https://kata-ui.dev/logo/logo.svg" width="64" height="64" alt="KATA UI">
</p>

# kataui

The CLI for [KATA UI](https://kata-ui.dev) — a copy-paste library of vanilla
HTML, CSS and JS parts: 136 components, 21 blocks and 7 templates, all cast
from one design-token mold. No framework, no runtime, no build step.

`kataui` fetches parts from the same registry the site publishes and writes
them into your project, dependencies included. It has zero dependencies
itself and needs Node 18+.

## Usage

```sh
npx @kajisho5/kataui init            # write the design tokens (kata/tokens.css)
npx @kajisho5/kataui add button      # add a part — and everything it depends on
npx @kajisho5/kataui add data-table  # components, blocks, templates, themes: one verb
npx @kajisho5/kataui list            # every part in the registry
```

Files land in `./kata` by default; load `kata/tokens.css` first, then the
part CSS, and paste the example HTML in as it is. Nothing phones home and
nothing updates itself afterwards — the files are yours, like a copy-paste
that typed itself.

## Options

- `--dir <folder>` — write somewhere other than `./kata`
- `--base <url>` — read a mirrored registry instead of https://kata-ui.dev
  (the `KATA_BASE` environment variable works too)

## Links

- Catalog and live previews: https://kata-ui.dev/components/
- CLI documentation: https://kata-ui.dev/docs/cli/
- Source: https://github.com/kajisho5/KATA-UI

MIT
