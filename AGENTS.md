# AGENTS.md — KATA UI

## Project
KATA UI (https://kata-ui.dev) is a framework-free, build-free UI library. Users copy HTML/CSS/vanilla JS into their own projects (like shadcn/ui, but not React).
- tokens.css is "the mold". Every component must read only tokens.
- The site claims: "tokens only, classes covered, every state finished" and "Mold Verified 164/164". The code must actually meet these claims.
- AI integration: registry.json / llms.txt / SKILL.md / MCP. These must stay in sync with component source.
- Foundry (theme editor) changes radius, colors, motion multiplier, etc. Components must respond to it.

## Layout
- Component source: components/<name>/ (preview.html, <name>.css, <name>.js, meta.json)
- Tokens: tokens.css (root)
- Site generator: build.py
- Before editing, check how build.py uses component files and where else the same code appears (registry.json, llms.txt, MCP data, generated site files). Regenerate with build.py instead of hand-editing generated files.

## Rules
1. Do not guess. If something is not in the repo, say so in the PR description.
2. Do not rename existing classes, data attributes, or tokens. If a rename is needed, keep the old name as a deprecated alias and explain why.
3. Use tokens.css CSS variables for all values. If a token is missing, add it to tokens.css and list it under "New tokens" in the PR description.
4. Raw values allowed only: 0, 1px borders, and percentages in layout. Anything else needs a token.
5. Every interactive element needs :focus-visible. Every color variant needs hover / active / disabled.
6. JS components: no globals, init all instances with querySelectorAll, safe to load twice (data-kata-ready guard), unique auto-generated IDs (respect existing IDs), ignore keys while IME is composing (e.isComposing / keyCode 229).
7. Logical properties (inset-inline, padding-inline) for RTL. Respect prefers-reduced-motion.
8. Every <button> in examples has an explicit type. Every input/select has a label.
9. Update meta.json (status, accessibility text) so it matches what the code actually does. Do not claim anything that is not implemented.
10. After changes, run build.py and make sure it succeeds. Commit regenerated outputs.

## PR description (required)
- Files changed and why
- New tokens (if any)
- What you verified (commands you ran and results)
- What you could NOT verify, and what I should check by hand in a browser / screen reader
- Write the PR description in Japanese. Code comments and site copy in English.
