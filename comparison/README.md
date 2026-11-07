# Ten screens, two ways — raw drafts

Design: `docs/design/ai-comparison.md` (owner-approved 2026-11-07).

- Agent: Claude (Anthropic) via Claude Code, 2026-11-07. Each draft set was written by a
  separate agent started with no prior conversation: A could read only the prompts;
  B could read the prompts and fetch from kata-ui.dev.
- `prompt.md`: prompt A, and prompt B = prompt A plus one fixed sentence
  ("Fetch each part from kata-ui.dev/registry.json and use it unmodified.").
- `direct.html` (A) and `kata.html` (B): the first output, unedited. Nothing was rendered,
  retried or picked before measuring.
- `results.json` and `shots/`: written by `python3 -m tools.measure_comparison`.
  `--check` re-measures and reports any number that differs.

Observed while drafting B: registry.json has no item for tokens.css, so the B agent fetched
`https://kata-ui.dev/tokens.css` separately and inlined it.

Measured in Chromium only. Not verified: other agents or dates, screen readers, Safari,
Firefox, real devices.
