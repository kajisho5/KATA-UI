# Roadmap

Implementation agent: Claude Code (from 2026-11-05).

<!-- mold-snapshot:start -->
[Mold Verified 164 / 164 · UI 121 / 121 · Lab 43 / 43](https://kata-ui.dev/audit/)

164 parts. Static checks only. Updated 2026-11-06 (Asia/Tokyo).
Read the audit for each part's pass, fail and warning results. Browser behavior needs separate testing.

| Remaining check findings | Count |
|---|---:|
| token-values: radius | 0 |
| token-values: radius-full | 0 |
| token-values: duration | 0 |
| token-values: shadow | 0 |
| token-values: shadow-ring | 0 |
| token-values: border | 0 |
| token-values: color | 0 |
| token-values: easing | 0 |
| spacing-values (UI fail, Lab warn) | 128 |
| type-values (UI fail, Lab warn) | 119 |
| focus-visible | 0 |
| js-single-instance | 0 |
| js-global-bindings | 0 |
| shared-token-scope | 0 |
| accessible-label | 0 |
<!-- mold-snapshot:end -->

The snapshot above is generated from `mold-results.json`. It counts parts, not
individual checks. A pass is a static-check result. Beta and Stable remain
separate release statuses. The phases below are targets, not shipped features.

## Principles

1. Add no new catalog components until Phase 1 is complete.
2. Keep checker rules strict. Do not change them to improve the score.
3. Site, README and model-facing copy state only what checks establish.
4. Work on one PR at a time. Give each PR one purpose.
5. Create new components from `template/`: checks pass → Beta → a three-instance
   page plus IME and screen-reader verification → Stable.

## Phase 0 — Align claims and implementation

- [x] P1 accuracy follow-up: semantic primitive rules, ring/pill classifications, dependency-aware focus evidence and Toast-local colors ([PR #17](https://github.com/kajisho5/KATA-UI/pull/17)).
- [x] P1: Profile-aware checker and token provenance ([PR #15](https://github.com/kajisho5/KATA-UI/pull/15)).
- [x] P2: CI ratchet, audit tables, generated audit facts and a checked template ([PR #16](https://github.com/kajisho5/KATA-UI/pull/16)).
- [ ] P3: Resolve or close [PR #1](https://github.com/kajisho5/KATA-UI/pull/1) and [PR #3](https://github.com/kajisho5/KATA-UI/pull/3) after reviewing their remaining changes.
- [x] P4: Replace UI radius literals with the Foundry-linked shared scale; keep Lab geometry unchanged ([PR #19](https://github.com/kajisho5/KATA-UI/pull/19)).
- [x] PR #19 regression correction: preserve Lab glow geometry with token paint, separate selected/offset rings, and measure both Drawer edges ([PR #19](https://github.com/kajisho5/KATA-UI/pull/19)).
- [x] P5 (shadow/rings): Normalize all remaining elevation/ring findings and four backdrops ([PR #19](https://github.com/kajisho5/KATA-UI/pull/19)).
- [x] Shared text contrast: role separation, Foundry/export fallback and 40-part Chromium measurements ([PR #20](https://github.com/kajisho5/KATA-UI/pull/20)); Firefox/Safari and screen-reader checks remain manual.
- [x] P5 (duration/easing): Shared scaled timing, named curves, zero/reduced-motion safety ([PR #21](https://github.com/kajisho5/KATA-UI/pull/21)).
- [x] P5 (color/border): token-values reached **0** on **2026-11-05** ([PR #22](https://github.com/kajisho5/KATA-UI/pull/22)); fixed tsutsuji palette and highlight review included.

- [x] P6: Rebuild JS-failing components using the Combobox initialization pattern. Three components per PR; test repeated loading, generated IDs, IME and focus departure.
  - [x] First batch: Alert Dialog, Drawer and Popover JS instances, focus and zero-motion safety ([PR #24](https://github.com/kajisho5/KATA-UI/pull/24)).
  - [x] Second batch: Command, Context Menu and Date Picker: independent instances, keyboard/IME guards and zero-motion regression tests ([PR #26](https://github.com/kajisho5/KATA-UI/pull/26)).
  - [x] Third batch: Tag Input, Input OTP and Data Table: independent state, visual arrows, LTR codes and native/custom change events ([PR #27](https://github.com/kajisho5/KATA-UI/pull/27)).
  - [x] Fourth batch: File Upload, Color Picker and Carousel: keyboard-reachable file input, radio swatches with visual arrows, RTL-safe carousel with settled announcements ([PR #29](https://github.com/kajisho5/KATA-UI/pull/29)).
  - [x] Fifth batch: Split Panel, Reorder and Follow Frame: RTL-aware separator with stacked mode, pausable autoplay, per-zone pointer following that idles when settled ([PR #30](https://github.com/kajisho5/KATA-UI/pull/30)).
  - [x] Sixth batch: Pricing, Site Header and Use Cases blocks: per-section state, Escape/outside-press menu dismissal with one document listener, keyboard row focus. js-single-instance and js-global-bindings reached **0** ([PR #31](https://github.com/kajisho5/KATA-UI/pull/31)).
- [x] P7: First add Playwright checks that measure whether a focused control has a visible ring. Then resolve focus findings using those checks.
  - [x] Measurement baseline: 444 Tab stops in 98 parts; below 3:1 contrast on 380 (light) and 156 (dark); 49 clipped stops in 8 parts ([PR #32](https://github.com/kajisho5/KATA-UI/pull/32)). The current `--k-ring` and light accent outline are below 3:1, so the ring value needs an owner decision before the shared rule.
  - [x] Closed Dropdown menus and collapsed Speed Dial actions leave the Tab order (7 of 10 no-change stops) ([PR #33](https://github.com/kajisho5/KATA-UI/pull/33)).
  - [x] Mold v3: `--k-ring` and the focus floor become a 2px ink ring; below 3:1 dropped from 380 to 20 (light) and 156 to 4 (dark) ([PR #34](https://github.com/kajisho5/KATA-UI/pull/34)).
  - [x] Part-owned weak rings replaced; below 3:1 dropped to 1 stop per theme (Rating, not measurable by the tool) ([PR #35](https://github.com/kajisho5/KATA-UI/pull/35)).
  - [x] Clipped rings drawn inside their controls (52 → 0); Navigation Menu's open panel is visible again ([PR #36](https://github.com/kajisho5/KATA-UI/pull/36)).
  - [x] Static rule: shared floor plus cancellation detection; the browser measurement runs in CI with 0 stops below 3:1 or clipped (owner review: [PR #37](https://github.com/kajisho5/KATA-UI/pull/37)).
- [x] P8: Promote spacing-values and type-values to fail for UI only, then replace the failing values.
  - [x] Mold v4 completes the spacing, text and leading scales with owner-chosen mappings (docs/token-migration.md) ([PR #38](https://github.com/kajisho5/KATA-UI/pull/38)).
  - [x] Spacing: 762 raw declarations in UI parts replaced with tokens; UI spacing findings 763 → 12 ([PR #39](https://github.com/kajisho5/KATA-UI/pull/39)).
  - [x] Font size: 433 raw declarations in UI parts replaced with text tokens; UI font-size findings 435 → 2 ([PR #40](https://github.com/kajisho5/KATA-UI/pull/40)).
  - [x] Line height: 84 raw declarations in UI parts replaced with leading tokens; UI line-height findings 84 → 0 ([PR #41](https://github.com/kajisho5/KATA-UI/pull/41)).
  - [x] Promotion (mold v5): spacing-values and type-values fail for UI parts at 0 UI findings; 164 / 164 before and after (owner review: [PR #42](https://github.com/kajisho5/KATA-UI/pull/42)).

**Completion criteria:** no hard-coded audit counts; CI rejects score loss and
individual passing-target regressions; claims stay within test coverage; at
least 90% of UI-profile targets pass all checks.

## Phase 1 — Finish 40 frequently used components

- [ ] Work in this order: button, input, field, textarea, select, checkbox, radio,
  switch, dialog/modal, dropdown-menu, popover, tooltip, toast, card, tabs,
  accordion, badge, alert, table, pagination, breadcrumb, then the remaining
  components needed to reach 40. Map requested names to repository slugs in each PR.
  - [ ] Popover: release procedure run; panel kept inside narrow viewports, shared outside listener; beta until a screen-reader pass (docs/review/popover, [PR #56](https://github.com/kajisho5/KATA-UI/pull/56)).
  - [ ] Dropdown: release procedure run; menu button keyboard, ARIA state and focus return added; beta until a screen-reader pass (docs/review/dropdown, [PR #55](https://github.com/kajisho5/KATA-UI/pull/55)).
  - [ ] Modal: release procedure run; backdrop close, dialog name and opener focus fixed; beta until a screen-reader pass (docs/review/modal, [PR #54](https://github.com/kajisho5/KATA-UI/pull/54)).
  - [ ] Switch: release procedure run; accessible names and boundary fixed; beta until a screen-reader pass (docs/review/switch, [PR #51](https://github.com/kajisho5/KATA-UI/pull/51)).
  - [ ] Radio: release procedure run; boundary contrast fixed; beta until a screen-reader pass (docs/review/radio, [PR #50](https://github.com/kajisho5/KATA-UI/pull/50)).
  - [ ] Checkbox: release procedure run; boundary contrast fixed; beta until a screen-reader pass (docs/review/checkbox, [PR #49](https://github.com/kajisho5/KATA-UI/pull/49)).
  - [ ] Select: release procedure run; beta until a screen-reader pass (docs/review/select, [PR #48](https://github.com/kajisho5/KATA-UI/pull/48)).
  - [ ] Textarea: release procedure run; beta until screen-reader and IME passes (docs/review/textarea, [PR #47](https://github.com/kajisho5/KATA-UI/pull/47)).
  - [ ] Field: release procedure run; field.js links hint/error; beta until screen-reader and IME passes (docs/review/field, [PR #46](https://github.com/kajisho5/KATA-UI/pull/46)).
  - [ ] Input: release procedure run; beta until screen-reader and IME passes (docs/review/input, [PR #45](https://github.com/kajisho5/KATA-UI/pull/45)).
  - [ ] Button: release procedure run; beta until a recorded screen-reader pass (docs/review/button, [PR #44](https://github.com/kajisho5/KATA-UI/pull/44)).
- [ ] Build one Torture Test page: three instances per component, RTL, dark mode,
  200% zoom and keyboard-only operation.
- [ ] Require static checks and the release procedure before marking each part Stable.
- [ ] Show the measured Stable / Beta split on the home page.
- [ ] Keep all First five recommendations Stable and passing.

**Completion criteria:** 40 components pass every check and are Stable; the
Torture Test matrix is verified; the home page shows current Stable/Beta counts
and its First five meet those requirements.

## Phase 2 — Website and writing

- [x] Put Kanban counts, Calendar dates and chart data in initial HTML ([PR #5](https://github.com/kajisho5/KATA-UI/pull/5)).
- [x] Fix singular/plural part counts and add generated distribution headers ([PR #5](https://github.com/kajisho5/KATA-UI/pull/5)).
- [x] Move the Lab to `/lab/` and shorten home/Pricing copy ([PR #9](https://github.com/kajisho5/KATA-UI/pull/9)).
- [ ] Review remaining "X, not Y", "honest" and "not a render" phrasing.
- [ ] Write Japanese documentation for the ten most-used components; establish usage evidence before choosing them.
- [ ] Publish a ten-screen comparison: a direct AI draft and the same screen assembled from fetched KATA sources. Publish the prompts and method.
- [ ] Reduce home-page prose to half the Phase 2 baseline recorded below.

**Completion criteria:** the home page has no more than half its recorded
baseline prose length; the listed documentation and ten-screen comparison are
published; initial HTML includes the demo content and distribution metadata.
The Phase 2 word-count baseline and measurement method are recorded below before further copy changes.

<!-- home-prose-baseline:start -->
Baseline: 815 whitespace-delimited words in the generated home page before this PR. Count text nodes outside script/style, including common navigation and controls. Use the same scope for the Phase 2 comparison. This is a measured planning baseline, not an audit score.
<!-- home-prose-baseline:end -->

## Phase 3 — Prepare for release

- [ ] Document the Pro free/paid boundary. Keep everything already visible accessible.
- [ ] Add DaisyUI, Web Awesome, Basecoat, Pico CSS and Franken UI to the comparison. Include areas where KATA loses.
- [ ] Check npm name availability and migrate to `kata-ui` or `@kata-ui/cli` with a compatibility plan.
- [ ] Test llms.txt, SKILL.md and MCP in Claude Code and Cursor. Publish commands, versions, prompts and results.

**Completion criteria:** the access boundary is documented, the expanded
comparison is sourced, the npm migration is tested, and both tool integrations
have reproducible published results.

## Phase 4 — Announce

- [ ] Publish on Zenn in Japanese.
- [ ] Post on X, then Show HN, then Product Hunt.
- [ ] Reserve the announcement week for support and fixes; ship no new features.

**Completion criteria:** all four announcements are published in that order,
links are recorded, and the announcement week contains no feature releases.

## Phase 5 — Japanese form components

- [ ] IME-safe Tag Input and Input OTP.
- [ ] Postal code to address and automatic furigana entry.
- [ ] Full-/half-width and phone-number normalization with explicit data rules.
- [ ] Japanese-era Date Picker and a holiday calendar with identified data sources.
- [ ] Family/given Name Field, ruby and Japanese line-breaking support.
- [ ] Registration and shipping-address blocks.
- [ ] Publish one Zenn article per component.

**Completion criteria:** every listed component and block passes the applicable
checks, the three-instance/IME/screen-reader release matrix is verified, and each
component has a published article. Phase 1's restriction on new components still applies.

## Phase 6 — Operate

- [ ] Update the audit and changelog monthly.
- [ ] Add one Pro block per quarter after the quality gates are met.
- [ ] Track GitHub stars, npm downloads, llms.txt requests and Pro revenue using documented collection methods.

**Completion criteria:** audit/changelog updates cover each month, quarterly
block delivery is recorded, and the four metrics have dated measurements.
This is a recurring maintenance phase, not a one-time release.

## Non-goals

- No new catalog components before Phase 1 is complete.
- No score-driven exceptions or weaker checks.
- No claims of keyboard, IME or screen-reader coverage based on static checks alone.
- No parallel feature PRs or unrelated fixes in one PR.
- No Stable label before the full release matrix is verified.
- No hidden removal of already visible material when Pro launches.
- No feature work during the announcement week.
- No usage, revenue or competitor claims without measurements or sources.
