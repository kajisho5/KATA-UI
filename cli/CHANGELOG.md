# CLI changelog

## 1.1.0 — 2026-11-05

- Reject unsafe registry paths, symlinks and non-file destinations before writing.
- Protect existing output by default; add --dry-run, --force and --backup. Backups use unique .bak suffixes; existing file modes are preserved.
- Resolve and validate the complete dependency/file plan before staging. Attempt rollback if a commit fails.
- Compare the installed mold header with the maximum requirement of selected parts and dependencies. Warn on stderr for legacy/older versions; unreadable and malformed headers are errors.
- Keep existing tokens.css unchanged during add, including add --force. Explicit init --force --backup is required to replace a customized mold.
- Add zero-dependency Node integration tests for filesystem and version boundaries.
- Require Node 20 or newer; test Node 20 and 22 in CI.

## 1.0.0

Initial CLI version in the repository. No historical npm publication date is asserted here.
