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

## Safe installs (1.1.0)

Existing files are protected by default. Resolve the entire plan before changing any files:

```sh
kataui add button --dry-run
kataui add button --force --backup
```

`--backup` requires `--force`; backups are `.bak`, `.bak.1`, etc., so earlier backups are kept. `--dry-run` creates no files, directories or backups and can preview protected destinations. The CLI refuses symlink roots/ancestors/targets, traversal and absolute registry paths, and non-file destinations. Use a physical directory path for `--dir`.

`add` never overwrites an existing `tokens.css`, even with `--force`. It reads the first mold header, treats an unversioned readable file as legacy v1, and compares against the highest `requiresMold` among the selected parts and dependencies. An older mold produces one stderr warning linking to [Update your mold](https://kata-ui.dev/docs/update-mold/). An unreadable file or malformed mold header stops the install; the version is not guessed. A header does not validate custom theme edits.

Review and back up custom changes before explicitly replacing the mold:

```sh
kataui init --dry-run --force --backup
kataui init --force --backup
```

Downloaded tokens must satisfy selected requirements. Installs stage all contents before replacing target files. A failure before replacement leaves target bytes unchanged; a commit failure attempts rollback. Created empty directories or safety backups may remain after a failed install. No atomic filesystem guarantee against a concurrently hostile process is claimed.

Tests: `npm test --prefix cli` from the repository root (no npm dependencies needed). The package remains `@kajisho5/kataui`; publishing and any namespace migration are owner actions.
