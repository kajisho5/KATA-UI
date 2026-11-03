# Toast local-token verification

Run from the repository root:

```sh
python3 tools/capture_toast_tokens.py --before-ref 6140cbfe9a3b2f86eec8053067b148b2e1c1c3b6
```

Requires Python Playwright and Chromium (`--chromium` overrides its executable).
The harness loads the actual Button/Toast sources, clicks Show toast, and captures
an 800×400 viewport in light and dark themes with reduced motion. It asserts
identical PNG hashes and computed text/background/subtext colors and no console
or page errors. See `verification.json` for browser/version and hashes.

| Theme | Before | After |
|---|---|---|
| Light | ![Light before](before-light.png) | ![Light after](after-light.png) |
| Dark | ![Dark before](before-dark.png) | ![Dark after](after-dark.png) |

Both themes are byte-identical before/after. The existing dark Toast has very
poor contrast: text and background both resolve to rgb(244,244,245). This scoped
variable move preserves that existing behavior; it does not establish
accessibility. Manual screen-reader and other-browser checks were not performed.

`audit-summary.json` records the complete checker summaries before/after this
revision. Rule effects count removed findings; reclassified findings remain errors.
