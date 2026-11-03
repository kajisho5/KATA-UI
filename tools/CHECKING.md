# Mold checks

Run `python3 check.py --json /tmp/mold-results.json`. Exit 1 means real violations; 2 or an exception means the checker failed. `--json -` writes JSON only. Optional positional slugs select components. Every item contains independent pass/fail/warn records; warnings do not inflate the passing count. Build runs the full check and publishes `dist/mold-results.json`, using its exact summary and per-component verdicts. A broken checker aborts the build; failed components do not prevent publication.

`check.config.json` holds exceptions. Entries in `raw_value_allowlist` require exact `path`, `property`, `value`, and a nonempty `reason`. The list starts empty. The only built-in numeric exception is the repository's explicit allowance for a 1px border. Shared token definitions are checked for component-name and root-class prefixes: --k-<component>-* is forbidden in tokens.css. Component-root custom properties belong in the component stylesheet, and their definitions are not treated as raw property usages. Legacy prefixed definitions are reported as failures; no allowlist bypass applies to this rule.

## Browser audit

Install tooling outside the checkout:

```sh
mkdir -p /tmp/kata-audit
npm install --prefix /tmp/kata-audit playwright axe-core
NODE_PATH=/tmp/kata-audit/node_modules npx --prefix /tmp/kata-audit playwright install chromium
python3 build.py
NODE_PATH=/tmp/kata-audit/node_modules node tools/check-browser.cjs
# Optional: test only named parts
NODE_PATH=/tmp/kata-audit/node_modules node tools/check-browser.cjs button combobox
```

Set CHROMIUM_PATH to an existing Chromium executable if available. The script serves local files on 127.0.0.1, renders two unmodified copies of each preview with dependencies, runs scripts and axe, and reports duplicate IDs and JS errors separately. Exit 1 means violations, 2 means an execution failure. Results go to mold-browser-results.json. Incomplete axe findings require manual review. It does not operate every widget or open every hidden panel.

## Detection limits

Static CSS inspection uses leaf-block parsing and property/value matching, not a full CSS parser. Comments and URL fragments are excluded. It checks radius/shadow/time/color properties, shorthands, inline styles and style blocks, including var() fallbacks. Named-color detection covers common names, not the entire CSS color grammar. Cascade, specificity, escaped selectors and CSS nesting can still require manual review.

Focus checks look for relevant local/dependency selectors, rather than accepting any focus rule or the global token fallback as proof. Complex ancestor/sibling selectors can produce false positives or false negatives. Hover detection currently targets color-setting btn-* classes, excludes sizing rules, and recognizes grouped alias selectors. It cannot infer arbitrary semantic variant names.

Labels recognize explicit for/id, wrapping labels, aria-label and existing aria-labelledby targets; they do not prove the label is meaningful or visible. JS checks are warning-only lexical heuristics, not an AST; template expressions, regex literals and nested constructs may confuse them. Reduced-motion checks establish a local reduce rule, not its effective cascade. axe is not a keyboard, IME, screen-reader or full WCAG certification.

Combobox message hooks: `data-combo-result-one` and `data-combo-result-many` accept `{count}`. Focus/click/Alt+ArrowDown open all options without status announcements; only non-composing input events filter and announce. Run the browser regression with `python3 -m unittest discover -s tests -p test_combobox_browser.py` (requires Playwright Python and system Chromium; otherwise explicitly skipped).
