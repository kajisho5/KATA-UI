---
name: kata-ui
description: Build web UI with KATA UI — practical components, blocks and full-page templates in plain HTML, CSS and JavaScript (no framework, no build step). Use when the user wants pages or interfaces built with KATA parts, or asks for vanilla / framework-free UI code.
---

# Building with KATA UI

KATA UI (https://kata-ui.dev) is a copy-paste library with a CLI and a
machine-readable registry: every part is plain HTML + CSS + (sometimes)
vanilla JS, cast from one design-token mold. There is no framework to
adopt and no runtime to install; in a terminal, `npx @kajisho5/kataui add <slug>` (see https://kata-ui.dev/docs/cli/) fetches parts and their
dependencies for you.

<!-- mold-summary:start -->
[Mold Verified 88 / 164 · UI 59 / 121 · Lab 29 / 43](https://kata-ui.dev/audit/)

164 parts. Static checks only. Updated 2026-11-05 (Asia/Tokyo).
Read the audit for each part's pass, fail and warning results. Browser behavior needs separate testing.
<!-- mold-summary:end -->

Static checks cover token provenance, markup and JavaScript patterns. Test keyboard, IME and screen-reader behavior separately.

## Sources of truth (fetch, don't guess)

- Catalog index for models: https://kata-ui.dev/llms.txt
- Everything, full text: https://kata-ui.dev/llms-full.txt
- Machine-readable registry (shadcn format, code inline):
  https://kata-ui.dev/registry.json
- Design tokens: https://kata-ui.dev/design-system/ (tokens.json is linked there)

Fetch the part's real code from the registry or its page
(https://kata-ui.dev/components/<slug>/, /blocks/<slug>/, /templates/<slug>/)
and paste it verbatim as the starting point. Never re-invent a part's markup
from memory — class names are the API.

## Assembly rules

1. Load `tokens.css` once (or the one-file bundle `kata-ui.css` /
   `kata-ui.js` from the Installation doc). UI and Lab have different token policies.
   Read each part's audit before using it.
2. A part's page lists the other parts it depends on ("Built from") —
   include their CSS too. Blocks compose parts; templates compose blocks
   and parts. Prefer composing existing parts over writing new markup.
3. Dark mode is `data-theme="dark"` on any container. Themes only change
   the five accent tokens.
4. Behavior is progressive: scripts layer onto real markup (dialog,
   details, native inputs). If a part has a JS file, include it after the
   markup.
5. Icons are SVGs on a 24 grid, stroke-width 1.7, square caps and bevel joins, `currentColor`.
   The icon set is at https://kata-ui.dev/icons/ — click-to-copy there;
   Lucide icons mix in without a seam.

## House discipline (keep the mold)

- Colors come from tokens only — no raw hex values in new CSS.
- The vermilion core color (`--k-core`, #eb471f) appears only at the
  center of active controls, the logo core and chart end points.
  Never use it for surfaces, text or decoration.
- One accent (asagi by default). Zinc carries the neutrals.
- Fictional placeholder content in examples: invented people, companies
  and numbers — never a real client's data.
