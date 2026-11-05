# Mold compatibility (v2–v4)

## v4 — complete spacing, text and leading scales (2026-11-06)

T3 replaces raw spacing and type values in UI parts with tokens. v4 adds the missing scale steps, generated from `system/tokens.json` into the `scale-tokens` region of tokens.css: `--k-space-px` 1px, `--k-space-0-5` 2px, `--k-space-5` 20px, `--k-space-7` 28px, `--k-space-10` 40px, `--k-text-md` 14px and `--k-text-display` 44px (already canonical, now exported), `--k-text-lead` 15px, `--k-lh-tight` 1, `--k-lh-card` 1.35, `--k-lh-small` 1.6. No existing token changes value or meaning. Mappings and counts: docs/token-migration.md.

## v3 — focus visibility (2026-11-06)

`tools/verify_focus_ring.py` measured 444 Tab stops in 98 parts: 380 were below 3:1 contrast in light and 156 in dark (docs/review/focus-ring/). The owner chose a 2px ink ring. v3 changes the meaning and width of one token and one tokens.css rule, both generated from `system/tokens.json` by `tools/sync_shape_tokens.py`:

- `--k-ring`: `0 0 0 3px` 12% tint (theme-specific) → `0 0 0 2px var(--k-bg), 0 0 0 4px var(--k-ink)`, declared in the root and both theme blocks so nested `[data-theme]` sections resolve their own colors. The ring is 4px wide instead of 3px.
- The focus floor `:where(:focus-visible)`: 2px `--k-accent` outline (#33a6b8, 2.88:1 on white) → 2px `--k-ink` outline, 2px offset.

`system/mold-history.json` records `--k-ring` as a v3 meaning change, so parts that reference it declare `requires mold >= 3` and the CLI warns on an older installed tokens.css. Parts that only inherit the floor need no newer mold: an old tokens.css keeps its weaker floor.

## v2

The owner identifies the November 1 release as mold v1; current shared tokens are v2. The git repository starts on November 2. Its earliest tokens.css (a8bc6fa) is evidence, **not a verified November 1 copy**. The generated changelog lists every recorded addition, removal and value change since that snapshot, including transient combo/toast additions and their later removal. Exact changes between the November 1 publication and the earliest surviving snapshot cannot be reconstructed.

`system/tokens.json` owns moldVersion and moldDate. `system/mold-history.json` freezes git-linked declaration events, first appearances, semantic changes and deprecations. `tools/mold_history.py --ref <commit>` regenerates that ledger; a normal website build consumes the committed ledger without needing git history. Values contain all light/dark/conditional alternatives.

Distribution requirements are computed from each component's shared-token references, its CSS/HTML/JS and recursive component/block dependencies. Local custom properties are not mold API. Numbered duration semantics require v2 even though the names existed before. Since the exact v1 snapshot is unavailable, shared-token consumers conservatively require v2 instead of making an unsupported v1 compatibility claim. The algorithm supports lower requirements once verified v1 evidence exists; token-free components do not need a newer mold. No component appearance or static checker rule changes.

## CLI overlap resolved by the consolidated safety PR

PR #1 and PR #3 overlapped in the CLI import, registry loading and token installation flow. The consolidated safety PR reviews and combines the required changes rather than merging their stale non-CLI patches. Exact CLI diffs and closure recommendations are in [the integration review](review/cli-integration/README.md); owner-only publication and namespace migration are in [PUBLISH.md](review/cli-integration/PUBLISH.md).

CLI 1.1.0 now performs a read-only check before installing any files:

1. Read the installed `tokens.css` through the merged safe-destination and symlink checks. Read only; never silently overwrite a customized mold.
2. Parse `/^\/\* KATA mold v(\d+)\b/`; a readable unversioned file is legacy v1. Report an unreadable file as an error, not as a guessed version. A missing file follows the merged init policy.
3. Take the maximum `requiresMold` across the requested items and the resolved dependency closure; compare it with the installed version. The registry also exposes `moldVersion`.
4. If older, print one stderr warning: `Installed mold v1; selected parts require mold >= 2. Review https://kata-ui.dev/docs/update-mold/ before updating tokens.css.` Preserve all merged dry-run/force/backup/transaction behavior.
5. Test missing, unversioned, v1, v2, malformed, unreadable, customized and symlink cases against a local registry; verify the warning never writes or updates a file.

The source now issues the warning, but npm publication remains a separate owner action. Older installed CLI versions still need the manual header check. add --force never replaces tokens.css; updating it requires an explicit init --force operation after diff review.
