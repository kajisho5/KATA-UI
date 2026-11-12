# Metrics (ROADMAP Phase 6)

One JSON file per calendar month, written by `python3 -m tools.collect_metrics`.
The four metrics named in the roadmap and how each is collected:

| Metric | How | Notes |
|---|---|---|
| GitHub stars (and forks) | `https://api.github.com/repos/kajisho5/KATA-UI`, unauthenticated | The count at the moment of measurement. |
| npm downloads | `https://api.npmjs.org/downloads/range/<start>:<end>/<package>` for the package name in `cli/package.json` | npm counts every tarball download, including CI, mirrors, bots and this project's own test runs. It is a download count, not a user count. npm's data trails by about a day; the file records the `start`/`end` npm returned. |
| llms.txt requests | Entered by the owner: the request count for `/llms.txt` in the Cloudflare dashboard for the month, with `--llms-source` naming the view used | No public API; the exact dashboard menu path was not verified from this repository. `null` until entered. |
| Pro revenue | Entered by the owner with `--pro-revenue-usd` | Pro is not on sale; the file says `"state": "not on sale"` until a value is given. |

## Monthly routine

In the first days of each month, for the month that just ended:

1. `python3 -m tools.collect_metrics --month YYYY-MM` (add `--llms-requests N --llms-source "…"` once the owner has the number).
2. `python3 check.py --json mold-results.json` and `python3 build.py`: the audit page and the Mold Verified header are regenerated from the checker.
3. Add a dated changelog entry in build.py for anything that shipped that month.
4. Commit the month's file, the regenerated outputs and the changelog in one PR.

A month measured before it ends has `"complete": false` and is re-measured after it ends.

## Recorded

| Month | Stars | npm downloads | llms.txt requests | Pro revenue |
|---|---:|---:|---:|---|
| 2026-11 (to 2026-11-12) | 0 | 244 | not entered | not on sale |
