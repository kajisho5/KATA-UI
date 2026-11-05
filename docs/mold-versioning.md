# Mold v2 compatibility

The owner identifies the November 1 release as mold v1; current shared tokens are v2. The git repository starts on November 2. Its earliest tokens.css (a8bc6fa) is evidence, **not a verified November 1 copy**. The generated changelog lists every recorded addition, removal and value change since that snapshot, including transient combo/toast additions and their later removal. Exact changes between the November 1 publication and the earliest surviving snapshot cannot be reconstructed.

`system/tokens.json` owns moldVersion and moldDate. `system/mold-history.json` freezes git-linked declaration events, first appearances, semantic changes and deprecations. `tools/mold_history.py --ref <commit>` regenerates that ledger; a normal website build consumes the committed ledger without needing git history. Values contain all light/dark/conditional alternatives.

Distribution requirements are computed from each component's shared-token references, its CSS/HTML/JS and recursive component/block dependencies. Local custom properties are not mold API. Numbered duration semantics require v2 even though the names existed before. Since the exact v1 snapshot is unavailable, shared-token consumers conservatively require v2 instead of making an unsupported v1 compatibility claim. The algorithm supports lower requirements once verified v1 evidence exists; token-free components do not need a newer mold. No component appearance or static checker rule changes.

## CLI overlap: implementation deferred

Open PR #1 changes `put` / `ensureTokens`, safe paths and overwrite behavior in cli/kata-ui.mjs. Open PR #3 changes the same installation flow to `addTokens` / `commitFiles`, adds readFile, and changes registry loading. A warning needs those exact import/registry/token-installation call sites; implementing it here would conflict with both pending safety designs. The CLI source/package is therefore unchanged, as requested.

After those safety PRs merge, add a read-only check before installing any files:

1. Read the installed `tokens.css` through the merged safe-destination and symlink checks. Read only; never silently overwrite a customized mold.
2. Parse `/^\/\* KATA mold v(\d+)\b/`; a readable unversioned file is legacy v1. Report an unreadable file as an error, not as a guessed version. A missing file follows the merged init policy.
3. Take the maximum `requiresMold` across the requested items and the resolved dependency closure; compare it with the installed version. The registry also exposes `moldVersion`.
4. If older, print one stderr warning: `Installed mold v1; selected parts require mold >= 2. Review https://kata-ui.dev/docs/update-mold/ before updating tokens.css.` Preserve all merged dry-run/force/backup/transaction behavior.
5. Test missing, unversioned, v1, v2, malformed, unreadable, customized and symlink cases against a local registry; verify the warning never writes or updates a file.

Until that follow-up is merged, the current CLI does **not** issue this warning. The registry, component headers, llms and Skill/MCP instructions ask consumers to check manually.
