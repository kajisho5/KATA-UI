# Pricing / Site Header / Use Cases blocks

Main base: `9c003f3f61139d1e82247ee40e6f06211a08280c`, after merged PR #30.
These are the last three JS-failing targets in the HANDOFF T1 order. Pricing and
Site Header failed both JS rules; Use Cases failed global bindings only. Site
Header and Use Cases also failed focus-visible. All are UI-profile blocks.
Their release status stays **Beta**. No shared tokens or checker rules change.

| Audit | Before | After |
|---|---:|---:|
| Mold Verified | 109 / 164 | 112 / 164 |
| UI | 74 / 121 | 77 / 121 |
| Lab | 35 / 43 | 35 / 43 |
| js-single-instance findings | 3 | **0** |
| js-global-bindings findings | 5 | **0** |
| focus-visible findings | 111 | 104 |
| spacing-values / type-values (warn) | 891 / 638 | 891 / 638 |
| token-values | 0 | 0 |

## Source and behavior

Each script is an IIFE, initializes every block once (`data-kata-ready`), checks
generated IDs for collisions and keeps IDs the application supplied. Existing
classes and data hooks (`data-billing`, `data-m`, `data-y`, `data-hdr-btn`,
`data-hdr-panel`, `data-uc-row`, `data-uc-scene`) keep working.

- **Pricing.** The switch rewrites `data-m`/`data-y` amounts only inside its
  own `.pricing` section; before, one switch rewrote every price on the page.
  The checkbox gets the name "Yearly billing" (axe `label` violation fixed). A
  status region announces monthly/yearly prices, and a checked state restored
  by the browser shows matching prices. The badge uses `inset-inline-start`.
  The home page embeds this block with the same script, so scoping matters there.
- **Site Header.** The menu button gets `aria-controls`. Escape closes an open
  menu and returns focus to the button; a pointer press outside the header or
  following a panel link closes it. Focus leaving the header, window blur and
  null-relatedTarget focusout do not. Outside presses use **one** document
  `pointerdown` listener for all headers, registered once even when the script
  loads twice (KATA.md item 11). Links and the button show `--k-ring`.
- **Use Cases.** Rows and scenes are grouped per `.k-uc` section; before, the
  script collected every row and scene on the page into one switcher. Each row
  controls its scene (`aria-controls`). Up/Down/Home/End move focus between rows
  (accordion pattern), Enter/Space opens one. Rows show a 2px inner accent
  outline because the list clips outer rings. `kata-use-cases-change` reports a
  new choice. Rows still contain their headings and lists inside the button, so
  the accessible name is long; that markup split is listed as follow-up work.

## Verification

```sh
node --check blocks/pricing/pricing.js
node --check blocks/site-header/site-header.js
node --check blocks/use-cases/use-cases.js
python3 check.py --json mold-results.json
python3 -m tools.verify_blocks_instances
python3 -m unittest discover -s tests -p 'test_*.py'
python3 -W error::SyntaxWarning build.py
python3 -m tools.mold_ratchet --report mold-results.json --reference-ref <main SHA>
python3 -m tools.verify_mold_distribution
python3 -m tools.mold_publish --check
NODE_PATH=<axe-core and playwright> node tools/check-browser.cjs pricing site-header use-cases
```

`results.json` and the screenshots cover nine Chromium cases (three copies, one
RTL, the script loaded twice, light/normal, dark/zero multiplier, dark/reduced
motion). Site Header runs at 600px so the menu button is visible. Checks include
independent state, unique and preserved IDs, synthetic composition keys,
null-relatedTarget focusout, window blur, focus rings, keyboard operation and
the exact set of document/window listeners. Console errors: zero.

Browser audit, before → after: Pricing `heading-order` + `label` → `heading-order`;
Site Header `landmark-unique` (two copies of the same Primary nav in the audit
page) unchanged; Use Cases `heading-order` unchanged. Use Cases `color-contrast`
appears intermittently on both old and new code (2, 1, 1 violations in three
runs of the old code): the scene fades in over 0.45s and axe can measure mid-fade.

Real Japanese IME, screen readers, Firefox/Safari and touch on real devices are
not verified. No block is promoted to Stable.
