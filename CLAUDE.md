@AGENTS.md

# Claude Code supplements

At the start of every session read `docs/HANDOFF.md` (current state and task
queue), then `docs/ROADMAP.md` and `KATA.md`. The handoff records facts and open
work; a design requirement is not proof that every existing part implements it.

Environment: Ubuntu, Python >=3.11, Node >=20. Run `bash tools/agent-setup.sh`
once per session. SessionStart runs it automatically; reuse that output unless a retry is needed. It is idempotent and reports available tools. Installation
requires `CLAUDE_CODE_REMOTE=true` or `AGENT_SETUP=1`; otherwise it only inspects.
If it reports a local virtual environment, run `source .agent/venv/bin/activate`
before manual commands. A SessionStart hook cannot activate its parent shell.
Setup failure must not stop the session; do the checks that remain available and
report missing tools. Current main has no dependency-install step in mold.yml;
the helper supplements CI with Playwright/Pillow for the existing browser tools.

Use `fix/<topic>` or `docs/<topic>`, branch from main and target main. If the
previous task's PR remains open, stop and report before starting the next task.
Do not ask the owner to repeat decisions already in AGENTS.md, KATA.md or
HANDOFF.md. If blocked, finish the safe authorized portion and describe the rest
in the PR. Never merge, publish to npm, deprecate, or close PRs/issues; write the
owner's steps instead. Do not trigger the npm publish workflow.

## Manual verification

These run blocks are copied from `.github/workflows/mold.yml` at main 2c057fb.
Read that workflow again after rebasing: it is the command source, not this copy.
The owner must fetch main first; then use its full SHA for the trusted ratchet.

```bash
MOLD_BASE_SHA=$(git rev-parse origin/main)
result=0
python3 -W error::SyntaxWarning check.py --json /tmp/mold-results.json || result=$?
if [ "$result" -gt 1 ]; then exit "$result"; fi
test -s /tmp/mold-results.json
python3 -W error::SyntaxWarning -m tools.mold_ratchet --report /tmp/mold-results.json --reference-ref "$MOLD_BASE_SHA"
python3 -W error::SyntaxWarning -m unittest discover -s tests -p 'test_*.py'
python3 -W error::SyntaxWarning -m tools.verify_template --json /tmp/mold-template-result.json
python3 -W error::SyntaxWarning build.py
python3 -W error::SyntaxWarning -m tools.mold_publish --check
python3 -W error::SyntaxWarning -m tools.verify_mold_distribution
```

`check.py` exits 1 for known failing parts. Do not hide an exception, parse error
or missing report as that expected failure. The ratchet compares individual
passing parts as well as the total. Build refreshes the root mold-results.json.

**Pending PR #25:** current main has neither a CLI npm test script nor the
Node20/22 matrix. Do not claim those steps exist in this workflow or have passed.
After the owner merges #25, copy its updated workflow and run its exact CLI steps:

```bash
npm test --prefix cli
# Working directory: cli
npm pack --dry-run
```

Run CLI tests under both Node20 and Node22, matching the pending matrix. Until
then `node --check cli/kata-ui.mjs` checks syntax only, not CLI regression tests.
`tools.mold_publish --check` above is the existing pre-publish consistency check;
`npm pack --dry-run` inspects a package and never publishes it.
