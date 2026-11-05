# Implementation handoff

## Status

Snapshot: 2026-11-06 (Asia/Tokyo), branch `fix/t3-line-height` on main
`77d926e926229c88567766c820eb2724c477e9ea` (after #40). Counts become main's when this PR merges.
Regenerated with `python3 check.py --json mold-results.json`; all counts below
come from that JSON.

**Mold Verified 164 / 164 · UI 121 / 121 · Lab 43 / 43**.
No target fails a check. The JSON reports 91 warning-bearing
checks; warning findings are counted separately below. This is static evidence,
not browser or screen-reader certification.

| Check | Remaining findings | Level |
|---|---:|---|
| accessible-label | 0 | fail |
| button-type | 0 | fail |
| focus-visible | 0 | fail |
| js-global-bindings | 0 | fail |
| js-single-instance | 0 | fail |
| legacy-contract | 0 | fail |
| reduced-motion | 0 | fail |
| shared-token-scope | 0 | fail |
| spacing-values | 140 | warn |
| token-values | 0 | fail |
| type-values | 121 | warn |
| variant-hover | 0 | fail |

Focus-visible has no findings under the T2 step 4 rule (shared floor plus
cancellation detection, KATA.md Focus); the browser measurement in CI finds
0 Tab stops below 3:1 or clipped. spacing-values has 140 warning findings (UI 12, Lab 128);
type-values has 121 (UI: font-size 2, line-height 0; Lab 119). token-values has no remaining findings.

### Remaining JS failures

None. js-single-instance and js-global-bindings reached 0 with #31
(Pricing, Site Header, Use Cases). #27 took main to 103, #29 to 106, #30 to 109,
and #31 to 112. Evidence: docs/review/tag-otp-table/,
docs/review/upload-color-carousel/, docs/review/split-reorder-follow/ and
docs/review/blocks-instances/. The JS checker is lexical; a pass is not proof of
every contract item (see Contract implementation gaps, item 11).

### Merged work, PR #11 through #40

The following one-line summaries are based on main's first-parent git log.
Missing number #12 is open, not silently assumed merged.

| PR | Main commit | Summary |
|---|---|---|
| #11 | a582ad2 | Mechanical button-type and reduced-motion repairs. |
| #13 | 95d4c11 | Token migration investigation and proposal. |
| #14 | 704f0ad | Audit failure combinations and token-migration analysis. |
| #15 | b97d4b4 | Profile-aware rules, local-token provenance and checker fixtures. |
| #16 | 6140cbf | CI ratchet, audit surfaces, measured claims, template and roadmap. |
| #17 | 1db2d12 | Semantic checker precision and Toast-local text colors. |
| #18 | 9efb97d | Inverse theme pairs restore readable Toast text. |
| #19 | ee7d179 | Shared shape/elevation migration, preserved Lab glows and distinct rings. |
| #20 | c6982b8 | Shared text roles and Foundry accent contrast behavior. |
| #21 | fd010dc | Scaled durations/easings, scoped reduced motion and zero-duration safety. |
| #22 | 2fa7cdc | Remaining paint/border token migration and fixed-palette hue preservation. |
| #23 | deb88d2 | Mold versioning, compatibility headers and upgrade/changelog pages. |
| #24 | 839b05d | Alert Dialog, Drawer and Popover multi-instance behavior. |
| #26 | 2c057fb | Command, Context Menu and Date Picker instances, RTL visual arrows and menu blur. |
| #25 | dcbd287 | CLI safe installs, mold-version warnings, Node 20/22 CLI tests in CI. |
| #27 | 30f67ab | Tag Input, Input OTP and Data Table instances and keyboard behavior. |
| #28 | 20ca626 | This handoff, CLAUDE.md and the opt-in session setup helper. |
| #29 | 47298c5 | File Upload, Color Picker and Carousel instances and keyboard behavior. |
| #30 | 9c003f3 | Split Panel, Reorder and Follow Frame instances, stacked split and pausable autoplay. |
| #31 | 1ec074e | Pricing, Site Header and Use Cases block instances; JS findings reach 0. |
| #32 | 69b5a86 | Focus-ring visibility measurement and baseline (T2 step 1). |
| #33 | 4dddb8a | Closed Dropdown menus and collapsed Speed Dial actions leave the Tab order. |
| #34 | 0b8f5f6 | Mold v3: --k-ring and the focus floor become a 2px ink ring. |
| #35 | 9b3ecf9 | Part-owned weak focus rings replaced; 112 → 116. |
| #36 | 5fcba9e | Clipped focus rings drawn inside; Navigation Menu panel visible; 116 → 120. |
| #38 | f6f7bc5 | Mold v4: spacing, text and leading scales generated from tokens.json (T3 step 1). |
| #39 | 0c318c1 | T3 spacing: 762 raw declarations → tokens; UI spacing findings 763 → 12. |
| #40 | 77d926e | T3 font size: 433 raw declarations → text tokens; UI font-size findings 435 → 2. |
| #37 | 7d7b562 | Focus rule: shared floor plus cancellation detection; browser focus measurement in CI; 120 → 164. The owner approved this checker change in chat on 2026-11-06. |

#25, #27 and #28 were squash-merged on 2026-11-05 by the Claude Code session,
in that order, on the owner's explicit chat instruction to do the merging. Each
PR's CI was green. #25 shared no files with the others and was based on main.
#27 and #28 were each merged locally onto the updated main first and checked
(check, ratchet, unittest, build, distribution; CLI tests for #27).
#29–#40 were squash-merged the same way after green CI. The owner then asked the
session to keep going: after each batch PR's CI is green, merge it and start
the next task. That instruction applies to this session; record it again if a
later session is given the same permission.

Evidence commands: `git log --first-parent --oneline origin/main` and
`gh pr list --state merged --limit 50 --json number,title,mergedAt,url`.

### Open PRs and owner actions

Snapshot checked through GitHub on 2026-11-05. Refresh before selecting work.

| PR | Handling |
|---|---|
| [#1](https://github.com/kajisho5/KATA-UI/pull/1) | Old CLI safety patch. #25 is now merged, so the owner may close it. Do not merge the stale branch wholesale. |
| [#3](https://github.com/kajisho5/KATA-UI/pull/3) | CLI consolidation landed in #25. Preserve its useful UI remainder as owner-created issues using #25's paste-ready list, then owner decides closure. |
| [#12](https://github.com/kajisho5/KATA-UI/pull/12) | Not wholly duplicated: Button combos id/for, Input focus-visible and a triple/RTL test remain. Revisit during T4; do not discard the remainder. |
| This PR (fix/t3-line-height) | T3: 84 raw line heights → leading tokens; UI line-height findings 84 → 0. |

### npm and environment

Read-only `npm view @kajisho5/kataui version dist-tags time --json` (2026-11-05)
returned latest **1.0.0**, published 2026-11-03. main's cli/package.json is now
1.1.0 (from #25) and requires Node >=20; 1.1.0 is **not** published. No npm
publish/deprecate or ownership changes were made. The owner alone may use the
manual publish workflow after reviewing its version and provenance requirements.
Do not trigger it as an implementation agent.

Ubuntu setup target: Python >=3.11 and Node >=20. This session (cloud container)
reports Python 3.13.18, Node 22.23.4, Playwright 1.62.0 (from
tools/agent-setup.sh) and Pillow 12.3.0. Node 20 is not installed here, so CLI
tests ran on Node 22 only; CI runs the Node 20/22 matrix. The container's
browser is /opt/pw-browsers/chromium, not /usr/bin/chromium. This session linked
/usr/bin/chromium to it by hand before running the setup helper, which then
reported "Chromium already available"; a fresh container without that link gets
the helper's /usr/bin/chromium warning, and the browser tests skip.
mold.yml installs no Playwright, so the browser regression tests (including
tests/test_upload_color_carousel.py) skip in CI; run them locally and report it.
Python Playwright does not install a Node playwright module for legacy Node browser tools.
Some existing browser tests hard-code /usr/bin/chromium and skip if it is missing;
a Playwright-managed browser alone does not satisfy those paths. Inspect setup
output and report skips rather than claiming headless verification happened.

## Pitfalls (do not repeat)

- Toast (#18): fixed light text on an inverting surface gave 1:1 in dark. Use inverted pairs.
- Combobox: filtering on focus hid every option except the current value.
- #19: generic shadows destroyed Lab glows; focus rings must not replace persistent selection rings.
- #21: a reduced-motion rule on * would disable host-app transitions. The old ease-out token was an in-out curve.
- #22: replacing Converge pink with gray lost the hue. Use a fixed palette color.
- #24: an instruction asked Alert Dialog to close on backdrop click; platform/APG convention wins, so it stays open.
- #26: RTL horizontal keys must follow screen direction, not an unconditional date increment.
- The old 164/164 badge counted files rather than completed checks. The badge never runs ahead of checker JSON.
- Two simultaneous branches from one main require a later rebase. One implementation PR at a time.
- aria-sort belongs to a column/row header, not a button role. Use a native button in the header.
- :where(targets):focus-visible is not zero specificity: the outside pseudo-class still counts. Wrap the whole focus selector in :where when zero specificity is intended.
- A stricter-check rollout can reduce the score and fail the trusted-main ratchet even after updating a local baseline. The owner must review that deliberate transition; never hide it with a permissive exception.
- Carousel (batch 4): announcing on every scroll index change reported the slides a smooth jump passed. Update dots live, announce and dispatch once on scrollend (with a timeout fallback).
- A sample root with role=region and a fixed aria-label repeats the same landmark when pasted twice (axe landmark-unique). Use role=group for carousel-like widgets.
- File inputs: `hidden` removes them from the tab order. Hide visually, keep focusable, and show the ring on the visible zone with :has(). Chromium opens the picker on Space; Enter was not reliable.
- Reorder (batch 5): the queue described a drag-to-sort list, but the part is an auto re-ranking leaderboard. Check the real part before applying a per-part spec; changing its purpose is a new part, not a fix.
- Split Panel (batch 5): a padded content-box pane made the percentage and the handle disagree by the padding. Use border-box when a percentage positions a handle.
- Site Header (batch 6): closing one stacked header's menu on pointerdown shifts the layout, so a click that started on another header's button can land elsewhere. Test the outside press and the other button's click separately.
- Use Cases axe color-contrast comes and goes (2, 1, 1 violations on unchanged code): the scene fades in over 0.45s and axe can measure mid-fade. Do not treat it as a palette change.
- Playwright: expect_file_chooser was flaky; use page.on('filechooser') and close each chooser. After a mouse click, a programmatic focus() is not :focus-visible; press a key first.

## Task queue

Execute top to bottom. One task = one PR. Update Status and this queue in the same
PR. Do not start while the previous task's PR is open. **Current blocker: the T3 line-height PR must be merged before the promotion PR.**
Never merge, publish, deprecate or close PRs/issues as the implementation agent
unless the owner explicitly asks in that session (see Merged work above).

### T1 — done

JS multi-instance batches 1–6 (#24, #26, #27, #29, #30 and #31) left no
js-single-instance or js-global-bindings findings. For new JS parts, reuse the
pattern in tools/verify_blocks_instances.py and the Common rules kept in KATA.md
contract items 11, 12 and 14. Follow-up found during T1, for T4 or a separate PR:
Use Cases rows are buttons that contain headings and lists, so their accessible
names are very long; splitting the row into a button plus a sibling body changes
markup and CSS selectors.

### T2 — done

#32 measurement tool and baseline; #33 closed menus out of the Tab order; #34
mold v3 2px ink ring (owner chose option 1); #35 part-owned weak rings; #36
clipped rings and the Navigation Menu panel; #37: static rule = shared
floor + cancellation detection, `verify_focus_ring --check` in CI, Rating measured
through its label. Below 3:1 in light: 380 → 0; clipped: 49 → 0; Mold Verified
120 → 164. Evidence: docs/review/focus-ring*/ and docs/review/focus-rule/.
Open follow-ups: `--k-ring-danger` is unused; Navigation Menu and Dropdown do not
return focus on Escape (T4); only default-preview Tab stops are measured.

### T3 — spacing-values and type-values become failures for ui (in progress)

Owner decisions (2026-11-06): spacing ties go to the smaller 4px step; 1px and
2px get tokens; font sizes snap to existing steps plus a new 15px step; leading
follows KATA.md §0.5. Mappings with counts: docs/token-migration.md (T3 section).
Order changed with reason: replace spacing, then font size, then line height
while the checks are warnings, and promote both to fail for UI last, at 0 UI
findings, so the pass count and trusted-main ratchet never drop. Step 1 (scales,
mold v4) is #38. #39 replaced 762 declarations (UI 763 → 12;
the 12 are `* -1` negatives, one `env(safe-area-inset-bottom)` and one `12vh`,
to settle with the checker change in the final promotion PR). #40 replaced 433
font sizes (UI 435 → 2; the 2 are `.86em` on inline code, also for the promotion
PR). The line-height PR replaced 84 (UI 84 → 0). Next: the promotion PR (checker
change; the owner reviews it before merge). It must settle the 14 remaining UI
findings: 10 `calc(token * -1)`, Bottom Navigation's `env(safe-area-inset-bottom)`,
Command's `12vh` and Typeset/Blog Article's `.86em` inline code.
Lab parts keep warnings.

1. Complete the common 4px spacing and text/leading scales in tokens.json. Existing --k-space-* / --k-text-* / --k-lh-* already exist; reuse them and preserve names/aliases rather than adding duplicate scales. Propose --k-leading-* only if a missing shared role needs it. Bump moldVersion for changes and write counted mappings in docs/token-migration.md.
2. Promote both checks to fail for ui only; record the lower baseline and explain the stricter-check transition, including the trusted-main CI ratchet effect. The owner must review the baseline-policy transition; never use an allowlist to conceal the drop.
3. Replace one category per PR: spacing, then font-size, then line-height, until both checks have zero UI findings. Capture before/after light/dark screenshots for the main twelve parts.

### T4 — Phase 1: Stable, one part per PR

Order: button, input, field, textarea, select, checkbox, radio, switch, modal,
dropdown-menu, popover, tooltip, toast, card, tabs, accordion, badge, alert, table,
pagination, breadcrumbs, then the rest of the forty most-used parts.
Repository mapping: dropdown-menu is components/dropdown; confirm other folder
names before editing. Modal/Dropdown/Tabs currently fail static checks, while
Tooltip passes. None of these four has a multi-instance page in current main.
The supplied brief's claim that all four already passed was not confirmed.

Per part: every check passes, JS follows item 11, tests/<slug>-multi.html exists,
metadata follows item 15. Mark Stable only after item 16, including recorded
manual IME/screen-reader checks; otherwise retain Beta with a reason. Existing
legacy Stable labels do not bypass this procedure.
Button also reconciles the unmerged #12 remainder (combos id/for, explicit
focus-visible and triple/RTL test). Verify the existing btn-accent and deprecated
btn-asagi alias instead of recreating them; include the variant × state table.

Then build one Torture Test page: each part ×3, RTL, dark, 200% zoom, keyboard only.
Show a measured N stable / M beta split on the home page.

### T5 — Phase 2 onward

Follow docs/ROADMAP.md. Keep one purpose per PR and update measured Status and the
queue. Do not add catalog components before Phase 1 is complete.

## Review protocol

The owner pastes each PR URL to a reviewer. Every PR uses the AGENTS.md template;
the reviewer checks before/after numbers, screenshots and the unverified list.
The agent writes owner steps for merge/publication/closure instead of doing them.

## Contract implementation gaps (documentation review only)

The contract is a target. No code is changed to conceal these differences:

- Item 5: finite radius steps follow --k-radius but full is intentionally fixed 999px; --k-glow is absent. No --k-shadow-edge exists (it is optional).
- Item 6: templates/product-page/product-page.css replaces the selected swatch box-shadow with an offset focus shadow; preservation of both states needs a browser test.
- Item 7: prior 40-part contrast artifacts exist under docs/review; no complete fresh 164-part/state contrast certification was performed for this handoff.
- Item 10: #25 is merged, so main's CLI (1.1.0 in cli/package.json) has the mold-header warnings and safe forced-add behavior. npm still serves 1.0.0 until the owner publishes. Explicit owner init --force is an intentional update, not automatic add overwrite.
- Item 11: Combobox and Popover still install per-instance document click listeners, rather than one pointerdown listener per part type. The JS checker does not detect every contract violation; the measured remaining JS failures are listed above.
- Item 12: Date Picker's RTL correction is merged in #26; Tag/OTP behavior (including OTP LTR/IME/completion) is merged in #27. Color Picker and Carousel visual arrows are in #29; Split Panel visual arrows are in #30.
- Item 13: main Modal uses native showModal/Escape but has no backdrop-click close handler. Drawer/Alert Dialog have the reviewed #24 behavior. Do not silently call Modal complete.
- Item 14: inline sample styles and fixed IDs remain across legacy parts; the static inline-data-color allowance is not proof of full sample compliance.
- Items 15/16: metadata and existing Stable labels predate the full manual release gate. No new manual IME/SR certification was performed. Missing multi-instance pages for Modal/Dropdown/Tabs/Tooltip are confirmed above.
- Setup/CI: #25 added the CLI regression script and the Node 20/22 matrix to mold.yml. There is still no Python browser dependency-install step, so browser tests skip in CI. CLAUDE.md's "Pending PR #25" section predates that merge. Managed Chromium paths may not satisfy scripts hard-coded to /usr/bin/chromium.
