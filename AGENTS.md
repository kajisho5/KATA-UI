# AGENTS.md — KATA UI

## Project
KATA UI (https://kata-ui.dev) is a framework-free, build-free UI library. Users copy HTML/CSS/vanilla JS into their own projects (like shadcn/ui, but not React).
- tokens.css is "the mold". Every component must read only tokens.
- The site claims: a checked-component workflow and a "Mold Verified" count derived from check.py JSON. The code must actually meet these claims.
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
3. Use shared tokens.css variables for shared values. Keep component-specific custom properties on the component root; never add component-prefixed tokens to tokens.css to pass checks. List new shared tokens under "New tokens" in the PR description.
4. Follow the profile/primitive definitions in KATA.md and check.config.json (including 1–3px border geometry, circular 50% radii and layout percentages). Do not add arbitrary literals or per-part exceptions.
5. Every interactive element needs :focus-visible. Every color variant needs hover / active / disabled.
6. JS components: no globals, init all instances with querySelectorAll, safe to load twice (data-kata-ready guard), unique auto-generated IDs (respect existing IDs), ignore keys while IME is composing (e.isComposing / keyCode 229).
7. Logical properties (inset-inline, padding-inline) for RTL. Respect prefers-reduced-motion.
8. Every <button> in examples has an explicit type. Every input/select has a label.
9. Update meta.json (status, accessibility text) so it matches what the code actually does. Do not claim anything that is not implemented.
10. After changes, run build.py and make sure it succeeds. Commit regenerated outputs.

## Workflow

- One task per PR, one PR at a time. Branch from main, target main. If the previous task's PR is open, do not start the next task; report.
- Never loosen a check to raise the number. A rule change requires an English rationale in KATA.md, passing and failing fixtures in tests/mold/, and before/after counts in the PR. The allowlist never gets per-part exceptions.
- When the pass count changes, update mold-baseline.json, the header and relevant checkboxes of docs/ROADMAP.md, the Status section of docs/HANDOFF.md, and docs/token-migration.md where relevant, in the same PR.
- On rebase, take main's baseline, ROADMAP, HANDOFF and generated outputs, then regenerate with check.py and build.py. Restore only task-specific progress after reconciling it with main.
- system/tokens.json is canonical. Never hand-edit tokens.css or generated files. Token additions, value changes or meaning changes require a moldVersion bump and a mold-changelog update in the same PR. Preserve git evidence in system/mold-history.json.
- Visual changes need before/after screenshots in light and dark. Text-color changes need contrast measurements with tools/capture_* (use --min-contrast 4.5 where supported). Interaction changes need a headless run of tests/<slug>-multi.html and the console error count.
- When an instruction conflicts with WAI-ARIA APG or platform convention, follow the convention and explain the choice in the PR (Alert Dialog backdrop and visual RTL arrows are examples).
- Site copy and code comments are English. Avoid "honest", "not a render", and "X, not Y" copy; use numbers and facts.

## PR description (required, Japanese)

- Files changed and why
- New tokens, or explicitly none
- Before/after checker numbers
- Commands run and their results
- What was not verified: real IME, screen readers, Safari/Firefox and relevant device behavior
- Before/after screenshots when visual changes occur; otherwise state that the change is documentation/tooling only

Read docs/HANDOFF.md before selecting work, then docs/ROADMAP.md and KATA.md.
