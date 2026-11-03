# Roadmap

<!-- mold-snapshot:start -->
[Mold Verified 29 / 164 · UI 19 / 121 · Lab 10 / 43](https://kata-ui.dev/audit/)

164 parts. Static checks only. Updated 2026-11-04 (Asia/Tokyo).
Read the audit for each part's pass, fail and warning results. Browser behavior needs separate testing.

| Remaining check findings | Count |
|---|---:|
| token-values: radius | 157 |
| token-values: radius-full | 11 |
| token-values: duration | 107 |
| token-values: shadow | 37 |
| token-values: shadow-ring | 12 |
| token-values: border | 1 |
| token-values: color | 23 |
| token-values: easing | 10 |
| spacing-values (warn) | 892 |
| type-values (warn) | 638 |
| focus-visible | 132 |
| js-single-instance | 24 |
| js-global-bindings | 57 |
| shared-token-scope | 0 |
| accessible-label | 1 |
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
- [ ] P4: Replace the open UI radius literals listed in the snapshot. Keep Lab geometry under its own policy.
- [ ] P5: Replace duration, shadow, border, color and easing literals. One value kind per PR.
- [ ] P6: Rebuild JS-failing components using the Combobox initialization pattern. Three components per PR; test repeated loading, generated IDs, IME and focus departure.
- [ ] P7: First add Playwright checks that measure whether a focused control has a visible ring. Then resolve focus findings using those checks.
- [ ] P8: Promote spacing-values and type-values to fail for UI only, then replace the failing values.

**Completion criteria:** no hard-coded audit counts; CI rejects score loss and
individual passing-target regressions; claims stay within test coverage; at
least 90% of UI-profile targets pass all checks.

## Phase 1 — Finish 40 frequently used components

- [ ] Work in this order: button, input, field, textarea, select, checkbox, radio,
  switch, dialog/modal, dropdown-menu, popover, tooltip, toast, card, tabs,
  accordion, badge, alert, table, pagination, breadcrumb, then the remaining
  components needed to reach 40. Map requested names to repository slugs in each PR.
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
