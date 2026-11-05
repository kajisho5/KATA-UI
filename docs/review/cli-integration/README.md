# CLI integration review (before implementation)

Base: main after merged PR #24, commit 839b05d. Static audit: 97/164, token-values 0. This review is published in the PR description before changing CLI code.

| Area | PR #1 | PR #3 | Main | Decision |
|---|---|---|---|---|
| Registry path validation | Reject absolute/traversal paths | Same, before planning writes | join() without validation | Consolidate one validation path, including backslash/drive paths |
| Symlink / non-file destinations | Checks installation parents/destinations | Same, preflight commit | Follows normal filesystem writes | Keep refusal for root, parent and destination links; dry-run also validates |
| Existing files | Refuse unless force | Same | Parts overwrite; existing tokens are skipped based on access() | Protect all destinations; read errors are not treated as missing |
| dry-run / force | Both flags | Both flags | Neither | Keep both; dry-run makes no directories/backups/writes |
| Backup | None | backup option, staged commit | None | Keep explicit --backup with force and preserve previous backups |
| Dependency errors / installation plan | Per-item writing can leave earlier writes | Plan before writing and commit safely | Writes dependencies/tokens before discovering an unknown part | Resolve/validate everything first; no partial install on unknown or unsafe paths |
| Registry validation | Original loader | Reject malformed items | Silently falls back to [] | Keep validation |
| Version and tests | No version bump/new tests | 1.1.0 + Node integration tests | 1.0.0, no CLI tests | New 1.1.0 and fresh main-based black-box tests |
| Root CI | None | Additional quality-gate workflow | Mold ratchet, unittest, warning-as-error build and distribution checks already merged | Extend the existing workflow with CLI tests; do not add a competing old pipeline |
| Components/tokens/FAQ/pricing/site edits | None | Several non-CLI edits from old base | Token/color/motion work already evolved in #19–#24; some unrelated UI details may remain | Exclude all non-CLI UI edits; do not reintroduce obsolete literals or change component appearance |
| Mold-version check | None | None | #23 publishes requiresMold; warning intentionally deferred | Add read-only header check to the consolidated installation plan |

No PR #1/#3 commits are cherry-picked wholesale. Any reused safety ideas are credited in commit messages. Current main already has the audit/CI and generated distribution machinery; those old changes are not re-applied.

## PR #12: keep the useful remainder

PR #12 is **not fully duplicated** in main. Button is already Stable and its main variant states, busy/disabled spinner and accent alias are present. However, main still has a fixed cb-sub id/for in Button combos; its Input dependency has :focus but no explicit :focus-visible rule, and the current checker still fails Button's combo Input focus-visible. The proposed triple/RTL Button page and its browser test are absent from main. Its old schema-1 mold-results snapshot and 20→22 totals are obsolete, and its accessibility prose largely duplicates newer main.

Do not close #12 solely as a duplicate now. Rebase/port its remaining focus, repeated-example and browser checks in the Button/Phase 1 work, then close the superseded PR. This CLI PR does not change those components. The owner will decide/perform closure.

## Closure decisions for #1 / #3

After the consolidated CLI PR merges and its tests pass, #1 can be closed as superseded. #3's CLI safety/version/test portion can also be closed as superseded; keep links to any desired non-CLI UI leftovers as separate issues/PRs instead of merging its broad stale patch. Neither old PR is closed automatically by this work.

## npm name check — 2026-11-05 (Asia/Tokyo)

Read-only npm view found kata-ui@1.0.0, so kata-ui is already published. @kata-ui/cli returned E404. That is not proof of publish eligibility: scope ownership, reserved-name policy and permissions remain unverified. No publish or deprecate is performed.

## Exact CLI diffs against main 839b05d

- [PR #1 head vs main](pr1-vs-main-cli.diff)
- [PR #3 head vs main](pr3-vs-main-cli.diff)

The new implementation adapts PR #3 staging/rollback and PR #1 overlapping path safety, fixes root/ancestor symlink checks and cross-platform traversal, preserves existing tokens during add (even force), checks required mold from the full dependency closure, keeps unique backups and file modes, and validates dry-run without writes. The old PR heads/base refs are pinned in the adjacent JSON records. No unrelated component or token patch is carried over.

## Rebase after PR #26

Rebased without conflicts onto main `2c057fb48157fe5fa03ae3f58a892087ff044d4d`.
Mold is now **100/164**, UI 67/121, Lab 33/43; token-values remains zero.
The 97/164 numbers above describe the original pre-rebase investigation.
The main baseline and roadmap are retained; distribution package headers remain
1.1.0. The CLI requires Node >=20 and CI tests Node 20 and 22 separately.

[Non-CLI remainder and paste-ready issues](UI-LEFTOVERS.md) distinguishes useful
unmerged changes from replaced token values and obsolete landing-page changes.
No issues or old PRs were closed or created automatically.
