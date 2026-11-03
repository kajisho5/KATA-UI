# Changelog

The full, entry-by-entry changelog lives on the site: https://kata-ui.dev/docs/changelog/
This file marks the versioned releases.

## v1.1.0 — Unreleased

- **CLI safety**: existing files are protected by default; `--force` is required to overwrite, `--dry-run` previews changes, and `--backup` saves replaced files.
- **Path safety**: registry paths that escape the output directory and symlink destinations are rejected.
- **Batch writes**: files are staged before installation and already-replaced destinations are rolled back if a later replacement fails.
- **Quality checks**: added CLI regression tests, representative Chromium browser tests, automated axe-core checks, responsive overflow checks, and a GitHub Actions quality workflow.
- **Reporting**: clarified that 164 refers to catalog items covered by static checks, not 164 independent test cases.

## v1.0.0 — 2026-11-02

First versioned release of KATA UI.

- **Catalog**: 136 components in eight categories (Form & Input, Layout & Navigation,
  Overlays & Dialogs, Feedback & Status, Display & Media, Motion, KATAYABURI, Japan),
  21 blocks, 7 templates, 150 icons and 56 brand marks.
- **Distribution**: copy-paste from the site, a zero-dependency CLI, registry.json in
  the shadcn registry format, an MCP server, and an installable AI Skill.
- **Versioning**: 1.0.0 is stamped into registry.json ("version"), the CLI
  (`node kata-ui.mjs --version`) and the MCP server.
- **Pro**: blocks and templates will be sold once, lifetime, at $129. Not on sale yet —
  a waitlist is open on the pricing page. Components, icons, themes and tooling are
  MIT and stay free.
