# npm package name: check and migration plan

Checked on 2026-11-12 with read-only `npm view` (no login, no publish, no deprecate).
ROADMAP Phase 3: "Check npm name availability and migrate to `kata-ui` or `@kata-ui/cli`
with a compatibility plan."

## What the registry says

| Name | State on 2026-11-12 |
|---|---|
| `kata-ui` | **Taken.** Published by a different npm account (version 1.0.0, created 2024-11-16). It is not this project. |
| `kataui` | Not in the registry. npm compares a new unscoped name with existing names after removing punctuation ([npm blog, "new package moniker rules"](https://blog.npmjs.org/post/168978377570/new-package-moniker-rules)), so `kataui` matches `kata-ui` and is expected to be refused. The exact rule is not published ([package name guidelines](https://docs.npmjs.com/package-name-guidelines)). |
| `@kata-ui/cli` | Not in the registry. It needs an npm organization named `kata-ui`; the organization name is also its scope ([Creating an organization](https://docs.npmjs.com/creating-an-organization)). Whether the name is free can only be seen by trying to create it while signed in. |
| `@kajisho5/kataui` | The current package: 1.0.0 on npm (2026-11-03). main's `cli/package.json` is 1.1.0, not published. |

**Target: `@kata-ui/cli`**, the roadmap's second option, because `kata-ui` is taken.
The command name stays `kataui` (the `bin` entry), so `npx @kata-ui/cli add button` and an
installed `kataui add button` both work.

## Compatibility plan

1. **One code base, two names for a while.** The same `cli/kata-ui.mjs` is published as
   `@kata-ui/cli`. `@kajisho5/kataui` stays on npm, so every command already written in
   blog posts, chats and scripts (`npx @kajisho5/kataui …`) keeps working.
2. **Docs switch after the first publish is confirmed.** The site, README, Skill and
   llms.txt change to `npx @kata-ui/cli` only after `npm view @kata-ui/cli version`
   returns the published version.
3. **The old name is not deprecated by an agent.** Deprecation prints a message on install
   and removes the package from npm search
   ([npm docs](https://docs.npmjs.com/deprecating-and-undeprecating-packages-or-package-versions)).
   Whether and when to do it is the owner's decision; the suggested message is
   `Moved to @kata-ui/cli. Same CLI, same commands.`
4. **One place for the name.** The package name and the Node requirement are read from
   `cli/package.json`. `tests/test_cli_package_name.py` fails if an install command in the
   README, the CLI README, the Skill, the publish workflow or the built site names any
   other package, or if the site states a different Node version. Switching is then a
   one-line change in `cli/package.json` plus the places that test lists.

## Owner steps (iPhone)

1. Open https://www.npmjs.com/org/create while signed in to npm.
2. Name: `kata-ui`. Plan: **Unlimited public packages** (free). Press **Create**.
3. If npm says the name is taken, tell me; the plan then needs another scope.
4. Tell me it is created. I will open a PR that changes the package name and the publish
   workflow. Publishing stays your action (GitHub → Actions → "Publish kataui to npm" →
   Run workflow), and the npm token used by that workflow must be allowed to publish to
   the new `@kata-ui` scope.

## Not verified

- Whether the `kata-ui` organization name is free (needs a signed-in attempt).
- Whether npm would actually refuse `kataui` (the rule is described, not specified).
