# Mold checks

Run `python3 check.py --json /tmp/mold-results.json`. Exit 1 means real violations; 2 or an exception means the checker failed. `--json -` writes JSON only. Optional positional slugs select components. Every item contains independent pass/fail/warn records; warnings do not inflate the passing count. Build runs the full check and publishes `dist/mold-results.json`, using its exact summary and per-component verdicts. A broken checker aborts the build; failed components do not prevent publication.

`check.config.json` holds exceptions. Entries in `raw_value_allowlist` require exact `path`, `property`, `value`, and a nonempty `reason`. The list starts empty. Allowed primitives and the 1px border-width exception are specified in the config, not hidden in code. Shared token definitions are checked for folder-slug and explicit meta.prefix namespaces: --k-<component>-* is forbidden in tokens.css. Component-root custom properties belong in the component stylesheet, and their definitions are not treated as raw property usages. Legacy prefixed definitions are reported as failures; no allowlist bypass applies to this rule.

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

Static CSS inspection uses leaf-block parsing and property/value matching, not a full CSS parser. Comments and URL fragments are excluded. It checks radius/shadow/time/color properties, shorthands, inline styles and style blocks, including var() fallbacks. Color identifiers outside configured grammar are rejected; unknown functions and unresolved values produce findings. Cascade, specificity, escaped selectors and CSS nesting can still require manual review.

Focus checks accept a matching local/dependency rule that draws a ring (`:focus-visible`, `:focus`, or a `:has()` host), or the tokens.css focus floor when no part rule removes the outline for that control (KATA.md, Focus). Run `python3 -m tools.verify_focus_ring --check` for the browser measurement (3:1 pixels in light and dark, clipping); CI runs it after the build with Playwright Chromium (`CHROMIUM_PATH`). Complex ancestor/sibling selectors can produce false positives or false negatives. Hover detection currently targets color-setting btn-* classes, excludes sizing rules, and recognizes grouped alias selectors. It cannot infer arbitrary semantic variant names.

Labels recognize explicit for/id, wrapping labels, aria-label and existing aria-labelledby targets; they do not prove the label is meaningful or visible. JS checks are error-level lexical heuristics, not an AST; template expressions, regex literals and nested constructs may confuse them. Reduced-motion checks establish a local reduce rule, not its effective cascade. axe is not a keyboard, IME, screen-reader or full WCAG certification.

Combobox message hooks: `data-combo-result-one` and `data-combo-result-many` accept `{count}`. Focus/click/Alt+ArrowDown open all options without status announcements; only non-composing input events filter and announce. Run the browser regression with `python3 -m unittest discover -s tests -p test_combobox_browser.py` (requires Playwright Python and system Chromium; otherwise explicitly skipped).

## Profile policy (KATA.md A–F)

UI requires shared token provenance for radius, duration/delay, shadow, color and
border. Motion/KATAYABURI use Lab: color, duration, shadow and easing require
tokens; literal radius/border/dimension/position geometry is permitted. Spacing
and type checks are advisory in both profiles, including Lab. Local aliases are
followed at use sites; a private variable name alone never proves provenance.
All candidate definitions are inspected conservatively, including dependencies.
Namespaces come from slug and explicit meta.prefix, never the first CSS class.
JS single-instance and global-binding findings are errors, not warnings.
Primitives and grammar allowances are in check.config.json.

Run `python3 -m unittest discover -s tests -p 'test_mold*.py'` for policy fixtures.
JSON v2 publishes profile, details/by_kind, summary.findings (finding counts),
summary.by_profile and summary.warnings (warning records, not findings).
KATA.md is authoritative for A–F; focus-visible and variant-hover retain their existing independent checks.
