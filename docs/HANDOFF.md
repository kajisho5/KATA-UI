# Implementation handoff

## Status

Snapshot: 2026-11-06 (Asia/Tokyo), branch `fix/product-page-swatch-names` on main
`adab2528eda6570b789e9a33904cd67e055d2c39` (after #51). Counts become main's when this PR merges.
Regenerated with `python3 check.py --json mold-results.json`; all counts below
come from that JSON.

**Mold Verified 164 / 164 · UI 121 / 121 · Lab 43 / 43**.
No target fails a check. The JSON reports 80 warning-bearing
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
| spacing-values | 128 | fail (UI), warn (Lab) |
| token-values | 0 | fail |
| type-values | 119 | fail (UI), warn (Lab) |
| variant-hover | 0 | fail |

Focus-visible has no findings under the T2 step 4 rule (shared floor plus
cancellation detection, KATA.md Focus); the browser measurement in CI finds
0 Tab stops below 3:1 or clipped. Since mold v5 spacing-values and type-values fail for UI parts; all 128 spacing and
119 type findings are Lab warnings (UI 0). token-values has no remaining findings.

### Remaining JS failures

None. js-single-instance and js-global-bindings reached 0 with #31
(Pricing, Site Header, Use Cases). #27 took main to 103, #29 to 106, #30 to 109,
and #31 to 112. Evidence: docs/review/tag-otp-table/,
docs/review/upload-color-carousel/, docs/review/split-reorder-follow/ and
docs/review/blocks-instances/. The JS checker is lexical; a pass is not proof of
every contract item (see Contract implementation gaps, item 11).

### Merged work, PR #11 through #51

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
| #41 | 5d4163d | T3 line height: 84 raw declarations → leading tokens; UI line-height findings 84 → 0. |
| #42 | cbc9073 | T3 promotion, mold v5: spacing/type fail for UI; `--k-text-code`; owner approved in chat on 2026-11-06 ("おすきにどうぞ"). |
| #43 | f5e2734 | Mold history regenerated against main after #42's squash merge. |
| #44 | c04cf60 | T4 Button: ID-free combo, three-set browser test in CI, variant × state contrast; beta pending a screen-reader pass. |
| #45 | 9792d5a | T4 Input: wrapped labels, aria-invalid, focus-visible, visible disabled state, RTL search icon; beta. |
| #46 | 619f119 | T4 Field: wrapped label, field.js links hint/error, alert on later errors, controls fit the field; beta. |
| #47 | d2046db | T4 Textarea: border-box, focus-visible, aria-invalid, read-only state, samples without IDs; beta. |
| #48 | 450c0fd | T4 Select: RTL chevron overlap, color-scheme scoped to the select (site.css owns the page's), disabled hover, aria-invalid; beta. |
| #49 | 7bb190b | T4 Checkbox: unchecked boundary 1.65:1 → 4.83:1, hover/mixed/invalid/disabled states; beta. |
| #50 | 1cdcbdf | T4 Radio: unchecked boundary 1.65:1 → 4.83:1, hover and aria-invalid; beta. |
| #51 | adab252 | T4 Switch: accessible names (were empty), role=switch, track boundary 3:1+, disabled; beta. |
| #52 | 2e59f45 | Product Page colour swatches: aria-label from the visible colour names, radiogroup named Color (repair before the empty-label rule). |
| #53 | 67b6759 | Checker: an empty label, label[for] or aria-labelledby target no longer names a control (owner approved); 164/164 unchanged. |
| #54 | 51baa6c | T4 Modal: backdrop click closes (item 13), dialog name/description, opener focus, IIFE with data-kata-ready; overlay browser test in CI; beta. |
| #55 | 7947de8 | T4 Dropdown: APG menu button (ARIA state, arrow keys, Escape focus return), IIFE with data-kata-ready, focused-item styles; beta. |
| #56 | f19e970 | T4 Popover: panel kept inside narrow viewports (--kpop-shift), one shared pointerdown/resize listener per script load; beta. |
| #57 | 46e4204 | T4 Tooltip: tip text kept out of the accessible name (CSS alternative text); WCAG 1.4.13 needs JS (owner decision); beta. |
| #58 | 23e2ea0 | T4 Toast: status live region (was claimed, not present), text instead of markup, tokenised icon; beta. |
| #59 | 463bdbd | T4 Card: combo progress bars named, optional .k-card-t/.k-card-p replace inline example styles; beta. |
| #60 | ce3d1ff | T4 Tabs: real panels (text was in the script), APG roles and keyboard, IIFE with data-kata-ready; beta. |
| #61 | 951d650 | T4 Accordion: three-set page and browser test; no defect found, no part file changed; beta. |
| #62 | 377ed56 | T4 Badge: three-set page and browser test; no defect found; legacy stable → beta. |
| #63 | 5205d0e | T4 Alert: decorative icons aria-hidden (were unnamed images), danger tone shown; beta. |
| #64 | 0a0ce65 | T4 Table: thead/scope, keyboard-scrollable named region, avatar initials hidden, end-aligned numbers; beta. |
| #65 | 140b679 | T4 Pagination: RTL arrows, real disabled state (no href + aria-disabled), current page keeps its fill on hover; beta. |
| #66 | 21a9515 | T4 Breadcrumbs: separators mirror in RTL (also the App Shell block); three-set page and test; beta. |
| #67 | 05a6bd1 | T4 Alert Dialog: button row wraps at 320px (ran 16px into the padding); layout/contrast test; beta. |
| #68 | 497ad98 | T4 Drawer: opens from the inline end in RTL (logical inset/margin, mirrored slide); beta. |
| #69 | 3b2f22e | T4 Combobox: one shared pointerdown listener replaces a document click listener per instance (item 11); beta. |
| #70 | ac54ccb | T4 Date Picker: one shared pointerdown listener replaces one per instance (item 11); beta. |
| #71 | 5b8291f | Input box-sizing follow-up: .input is border-box, fits its container and is 38px tall like .btn-md. |
| #72 | 5c8f50c | T4 Slider: RTL fill on the correct side, label-wrapped samples (no fixed IDs), thumb edge 4.83:1, IIFE with data-kata-ready; beta. |
| #73 | 82e041b | T4 Toggle: guarded IIFE (a second load no longer undoes every click), Bold/Italic/Underline names, active and disabled states; beta. |
| #74 | 47872f4 | T4 Segmented: hover state on unchecked segments, per-group name note, three-set page and browser test; beta. |
| #75 | 3c43aec | T4 Avatar: every avatar hidden or a named image (31 hidden next to visible names), fictional sample names, RTL status dot, dot no longer clipped; beta. |
| #76 | 763e450 | T4 Progress: both preview bars named (were unnamed progressbars), three-set page and browser test; beta. |
| #77 | 401bde0 | T4 Skeleton: role=status with a visually hidden loading label, shapes stay aria-hidden, shimmer reversed in RTL; beta. |
| #78 | 5e05ccd | T4 Spinner: no source change; browser test for names, sizes, edge contrast and reduced motion; forced-colors gap recorded; beta. |
| #79 | daf59f7 | T4 Empty State: decorative icon aria-hidden (Chromium exposed an unnamed image), logical spacing; beta. |
| #80 | dd0da8e | T4 Separator: hr no longer shrinks to 0px in grid/flex (UA auto margins), lines are borders so forced colors keep them; beta. |
| #81 | b77fe09 | T4 Sidebar: guarded script (double load toggled twice), rail labels visually hidden instead of removed, aria-current, RTL sub-item indent; stable -> beta. |
| #82 | 14f035a | T4 Command: one shared Cmd/Ctrl+K document listener per script load (was one per palette), logical CSS; beta. |
| #83 | 55b5f02 | T4 Context Menu: one shared outside-press document listener per script load (was one per menu), logical CSS; beta. |
| #84 | c7e14f4 | T4 Hover Card: closed card visibility:hidden (was read in the sentence), Escape dismisses (WCAG 1.4.13), guarded IIFE, viewport fit at 360px; beta. |
| #37 | 7d7b562 | Focus rule: shared floor plus cancellation detection; browser focus measurement in CI; 120 → 164. The owner approved this checker change in chat on 2026-11-06. |

#25, #27 and #28 were squash-merged on 2026-11-05 by the Claude Code session,
in that order, on the owner's explicit chat instruction to do the merging. Each
PR's CI was green. #25 shared no files with the others and was based on main.
#27 and #28 were each merged locally onto the updated main first and checked
(check, ratchet, unittest, build, distribution; CLI tests for #27).
#29–#84 were squash-merged the same way after green CI. The owner then asked the
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
| [#12](https://github.com/kajisho5/KATA-UI/pull/12) | Its remainder landed in T4: Button combos id/for and the three-set/RTL test in #44, Input focus-visible in #45. Nothing in #12 is left unmerged; the owner may close it. |
| [#85](https://github.com/kajisho5/KATA-UI/pull/85) | T4 Data Table: table scrolls inside a named, focusable .k-dt-scroll region (was clipped at narrow widths), inset focus outline, logical borders; beta. |

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
PR. Do not start while the previous task's PR is open. **Current blocker: #85 (T4 Data Table), then file-upload (prepared locally).**
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

### T3 — done

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
PR). #41 replaced 84 (UI 84 → 0). #42 (mold v5) settles the last 14:
the 10 `calc(token * -1)` were a lexer bug (`-1` read as an identifier), fixed;
`env(safe-area-inset-*)` is accepted in spacing only; the owner chose (chat,
2026-11-06) Command's offset `12vh` → `--k-space-16` (64px) and a shared
`--k-text-code` `.86em` for inline code. spacing-values and type-values then fail
for UI at 0 UI findings, 164 / 164 before and after. Evidence:
docs/review/t3-promote/. #42 merged with owner approval. After a squash merge, regenerate
`python3 -m tools.mold_history --ref origin/main` so token introductions point at main
commits (v5's `--k-text-code` pointed at the branch commit until this follow-up).
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

Progress: Button ([#44](https://github.com/kajisho5/KATA-UI/pull/44)) — combo sample without fixed IDs, tests/button-multi.html
and tests/test_button_browser.py (run in CI after Chromium is installed), variant ×
state contrast in docs/review/button/ (enabled minimum 5.57:1). Status changed
from the legacy `stable` label to `beta`: item 16 needs a recorded screen-reader
pass, which the container cannot run. The owner can record one with iPhone
VoiceOver on the preview (steps in docs/review/button/README.md); then a one-line
meta change marks Button stable.
Input ([#45](https://github.com/kajisho5/KATA-UI/pull/45)): samples wrap inputs in labels (no fixed IDs), errors use
aria-invalid, `:focus-visible` (the last #12 remainder), the disabled state was
indistinguishable and is now muted, the search icon is RTL-aware. Beta until a
screen-reader and real IME pass. #12 has no remaining Button/Input work; the
owner may close it.
Field ([#46](https://github.com/kajisho5/KATA-UI/pull/46)): the label wraps its control; new field.js links the hint and the
error (while data-invalid) with generated IDs, keeps author IDs, syncs
aria-invalid and sets role="alert" only when data-invalid is added after load.
The old a11y text claimed this without code. Controls in a Field use
border-box: they overflowed by 26px (Settings Page inputs ran past the card).
Follow-up for Input (done in #71): `.input` was content-box, so `width:100%`
overflowed its container by 26px and the height was 40px outside a Field.
Textarea ([#47](https://github.com/kajisho5/KATA-UI/pull/47)): border-box (it overflowed by 26px and rendered 110px for a
92px minimum; Settings block is 18px shorter), :focus-visible, aria-invalid as
an alias of data-invalid, hover skips disabled, read-only gets a soft
background, samples wrap the textarea in its label and gain error and
disabled/read-only examples. Pixel contrast here is measured at 2x scale
(placeholder 5.74:1); the Input table was at 1x and reads lower (4.83:1) for the
same colors, so treat 1x values as a floor.
Select ([#48](https://github.com/kajisho5/KATA-UI/pull/48)): in RTL the chevron moved to the left but its 32px padding
stayed on the right, so text ran under it; padding is now logical. select.css
set color-scheme on :root (every page that loaded it, including the one-file
bundle, changed scrollbars and native controls); it is now scoped to the select,
and site.css sets the site's own color-scheme. Disabled no longer reacts to
hover; aria-invalid draws the danger border.
Checkbox ([#49](https://github.com/kajisho5/KATA-UI/pull/49), `.check`): the unchecked border used --k-border-strong,
1.65:1 (light) and 2.29:1 (dark) against the page, below WCAG 1.4.11's 3:1; it
now uses --k-ink-3 (4.83:1 / 5.6:1). The token itself is unchanged because other
parts use it for hover borders. Adds hover, indeterminate, aria-invalid and
disabled styles. The Radio part (`.k-radio`) has the same 1.65:1 border: fix it
in the Radio PR. Radio names in samples are per group; pasting a radio sample
twice joins the groups (documented in meta; a native-HTML property).
Measure contrast with --k-mscale 0 after a theme switch: border transitions
otherwise catch mid-fade colours (2.89:1 was read once).
Radio ([#50](https://github.com/kajisho5/KATA-UI/pull/50), `.k-radio`): same boundary fix (--k-ink-3, 4.83:1 / 5.6:1),
hover and aria-invalid; arrow keys skip the disabled option.
Switch ([#51](https://github.com/kajisho5/KATA-UI/pull/51)): every sample put the text outside `label.switch`, so in
Chromium's accessibility tree all switches had an empty name and clicking the
text did nothing (meta.json claimed both worked). Samples now use
`label.switchrow > span.switch > input[role=switch]` + text; Settings block,
Settings Page and Landing switches get `aria-label` from their row title, and
all get role=switch. The off track (1.48:1 light, 2.29:1 dark) and the accent
track (2.88:1) get a 1px rim so their edge is 3:1+. **Checker gap for the
owner:** `accessible-label` passes any input inside a <label>, even a label with
no text; detecting empty labels is a rule change and needs owner approval.
The owner approved it in chat on 2026-11-06 ("なおしてもいいよ"). The stricter
rule (name from the control's aria-label, or aria-labelledby, label[for] or
ancestor label holding text, a child aria-label or img alt; title is still not
accepted) flags only the three Product Page colour swatches. The repair landed
first (#52); the rule is #53 (rationale in KATA.md "Accessible label").
Modal ([#54](https://github.com/kajisho5/KATA-UI/pull/54)): modal.js had no IIFE, no data-kata-ready guard and
no backdrop close (item 13); the dialog had no name link and focus did not
return to the opener. It now follows the Drawer pattern from #24. combos.html
wraps the input in its label. tests/modal-multi.html; tools/verify_overlay_instances
covers Modal and CI runs tests.test_overlay_instances after Chromium. Beta.
Dropdown ([#55](https://github.com/kajisho5/KATA-UI/pull/55)): dropdown.js was four lines with one document click
and keydown listener per instance, no ARIA state, no arrow keys and no focus
return. It now follows the APG menu button pattern (aria-haspopup/expanded/
controls, role menu/menuitem/separator, Enter/Space/ArrowDown/ArrowUp open,
arrows wrap, Home/End, aria-disabled skipped, Escape and item choice return
focus, Tab/outside pointerdown/blur close, one menu open at a time). A focused
item now gets the hover background. tests/test_closed_menu_tab_order.py now
expects opening to focus the first item (APG) instead of a Tab into the menu;
closed items are still not Tab stops. Beta.
Popover ([#56](https://github.com/kajisho5/KATA-UI/pull/56)): on a 360px page with the trigger at the inline start
the centred panel reached x=-77 (LTR) / 437 (RTL); popover.js now sets
--kpop-shift on open and resize to keep a --k-space-4 margin. One pointerdown
and one resize listener per script load replace a document click listener per
instance (item 11). Beta.
Tooltip ([#57](https://github.com/kajisho5/KATA-UI/pull/57)): the ::after tip text joined each trigger's accessible name
("Copy Copy link"); `content: attr(data-tip) / ""` keeps it out, and the tip
renders pixel-identically. **Owner decision:** WCAG 1.4.13 (Escape dismissal,
hoverable tip) cannot be met in CSS alone; it needs a small tooltip.js, which
changes the part's "Pure CSS, no JS" description. Beta until then.
Toast ([#58](https://github.com/kajisho5/KATA-UI/pull/58)): meta claimed a polite live region but none existed; each
[data-toasts] stack now gets role=status and aria-live=polite at load. Title
and detail use textContent (were innerHTML). The icon's hard-coded #5dac81 is
now --k-success via .toast-icon, aria-hidden; rendering is pixel-identical.
No public toast() API exists (only the demo button); pause-on-hover and a
dismiss button are not implemented. Beta.
Card ([#59](https://github.com/kajisho5/KATA-UI/pull/59)): the combo's progress bars had empty names; they take
aria-label from their visible labels. Optional .k-card-t/.k-card-p replace the
examples' inline text styles (pixel-identical). The light footer pair
(--k-ink-3 on --k-bg-soft) is 4.51:1: re-check it if either token changes. Beta.
Tabs ([#60](https://github.com/kajisho5/KATA-UI/pull/60)): tabs.js wrote three hard-coded sample texts into one pane;
panels are now markup (one [data-tabpane] per tab after the list). APG tabs
with automatic activation, arrows in visual direction (reversed in RTL),
Home/End, roving tabindex; text-only panels take focus. The combo card body is
split into three panels. Default-preview focus stops went 437 → 436 (roving
tabindex leaves one tab in the Tab order). Beta.
Accordion ([#61](https://github.com/kajisho5/KATA-UI/pull/61)): native details; the browser test (names, expanded
state, Enter/Space, focus ring, RTL chevron, contrast) found no defect, so no
part file changed. Beta until a screen-reader pass.
Badge ([#62](https://github.com/kajisho5/KATA-UI/pull/62)): no defect found (every tone ≥ 5.26:1 text contrast,
text-spacing overrides do not clip, RTL dot at the inline start); legacy
stable becomes beta per item 16.
Alert ([#63](https://github.com/kajisho5/KATA-UI/pull/63)): tone icons were unnamed images in the accessibility tree
(also in the Settings Page template); they take aria-hidden. The preview adds
the danger tone. The lowest pair is the dark success icon at 3.10:1. Beta.
Table ([#64](https://github.com/kajisho5/KATA-UI/pull/64)): header row in <thead> with scope="col"; the overflowing
.ktable-wrap (360px) is a named region with tabindex=0 so the keyboard can
scroll it; avatar initials aria-hidden; .num end-aligns numbers (usage already
asked for it); avatars centred on the name. Header text is 4.51:1 light. Beta.
Pagination ([#65](https://github.com/kajisho5/KATA-UI/pull/65)): prev/next chevrons and the compact text arrows
mirror in RTL; disabled prev/next is an <a> without href plus aria-disabled
(.disabled kept as a deprecated alias); hover and :active skip the current page;
text arrows, chevrons and the ellipsis are aria-hidden. Beta.
Breadcrumbs ([#66](https://github.com/kajisho5/KATA-UI/pull/66)): chevron separators pointed right in RTL; they now
mirror (App Shell uses the same markup). No other defect found. Beta.
Alert Dialog ([#67](https://github.com/kajisho5/KATA-UI/pull/67)): at 320px the button row ran 16px into the left
padding; it now wraps. Behaviour stays covered by verify_overlay_instances. Beta.
Drawer ([#68](https://github.com/kajisho5/KATA-UI/pull/68)): physical margin/inset kept the panel on the right in RTL; logical
properties put it at the inline end and kdrawer-in-rtl slides it from the left;
reduced motion removes both. verify_overlay_instances now clicks the backdrop
outside the panel. Beta.
Combobox ([#69](https://github.com/kajisho5/KATA-UI/pull/69)): each instance added a document click listener; one
pointerdown listener per script load now serves all instances (item 11).
test_combobox_browser counts the listeners over CDP and now runs in CI after
Chromium. Beta.
Date Picker ([#70](https://github.com/kajisho5/KATA-UI/pull/70)): each instance added a document pointerdown listener;
one per script load now serves all instances. At 320px the page scrolls
sideways by 44px because of the Input box-sizing follow-up (next PR). Beta.
Input box-sizing ([#71](https://github.com/kajisho5/KATA-UI/pull/71)): .input is border-box. At 360px, 16 overflowing inputs
across Checkout, Date Picker, Input, Login, Settings and Time Picker now fit;
all .input controls are 38px tall (were 40). Dashboard's fixed-width search is
26px narrower. Checkout and Settings still scroll sideways at 360px for other
reasons (not audited).
Slider ([#72](https://github.com/kajisho5/KATA-UI/pull/72)): the WebKit track gradient ran left to right in RTL, so the
fill sat on the wrong side of the thumb; :dir(rtl) fixes it. Samples wrap the
range in its label (no fixed id/for), the readout is aria-hidden, the thumb
outline is --k-ink-3 (4.83:1, was 1.6:1). Beta.
Toggle ([#73](https://github.com/kajisho5/KATA-UI/pull/73)): toggle.js bound one click listener per button with no
guard, so a second script load flipped aria-pressed twice per click. It is now
an IIFE with data-kata-ready and a kata-toggle-change event. The formatting
toggles are named Bold, Italic and Underline (were B, I, U); :active and
:disabled styles added. Beta.
Segmented ([#74](https://github.com/kajisho5/KATA-UI/pull/74)): CSS only on native radios. Unchecked segments had no
hover state; they now darken on hover. meta.json records that each group needs
its own name. Contrast: selected 17.72/16.12, unchecked 6.55/5.81. Beta.
Avatar ([#75](https://github.com/kajisho5/KATA-UI/pull/75)): initials were read next to the visible name. 31 avatars in
blocks, templates and combos are aria-hidden; labelled avatars are role=img.
The preview uses fictional names. The status dot uses inset-inline-end.
tests/test_avatar_names.py checks every .k-avatar statically. Beta.
Progress ([#76](https://github.com/kajisho5/KATA-UI/pull/76)): both preview progressbars had no accessible name; they now
carry aria-label matching the visible task. No other unnamed progressbar exists
in components, blocks or templates. The fill starts at the inline start in RTL.
Contrast: task 17.72/16.12, percentage 7.73/6.91. Beta.
Skeleton ([#77](https://github.com/kajisho5/KATA-UI/pull/77)): the preview was entirely aria-hidden, so nothing announced
loading although meta.json asked for a status container. The container is now
role=status with a visually hidden "Loading profile" label; the shapes stay
aria-hidden. The shimmer runs in reverse under dir=rtl. Pixel-identical at rest. Beta.
Spinner ([#78](https://github.com/kajisho5/KATA-UI/pull/78)): no defect found; tests only. Rendered sizes are 18/22/32px
(content-box ring), the button keeps its height with a spinner, and the moving
edge is 17.72/16.12:1. In Chromium forced-colors emulation edge and track both
become black, so the ring shows no moving edge; no part handles forced colors
yet (separate decision). Beta.
Empty State ([#79](https://github.com/kajisho5/KATA-UI/pull/79)): the decorative SVG icon had no aria-hidden, so Chromium
exposed an unnamed image; it is now hidden. Spacing uses logical properties.
Pixel-identical in light and dark. Text 17.72/16.12 and 7.73/6.91, icon 4.51/4.71. Beta.
Separator ([#80](https://github.com/kajisho5/KATA-UI/pull/80)): the UA hr margin is 0.5em auto, so in grid and flex
containers .k-sep shrank to 0px (component preview; Inbox template demo 0 -> 702px).
.k-sep sets margin-inline:0. The vertical and labelled lines were background
fills that forced colors drop; they are now 1px borders. Other pages keep their
widths. Beta.
Sidebar ([#81](https://github.com/kajisho5/KATA-UI/pull/81)): sidebar.js had no guard, so a second load flipped each
group twice per click; it is now an IIFE with data-kata-ready. The rail hid labels
with display:none, removing link names; they are now clipped to 1px. The current
link carries aria-current=page. Sub-items used a physical left margin; now
margin-inline-start. Avatar initials aria-hidden. LTR pixel-identical. stable -> beta.
Command ([#82](https://github.com/kajisho5/KATA-UI/pull/82)): command.js added one document keydown listener per palette
(3 on the three-palette page); it now adds one per script load and keeps the
same target rule (open palette, focused trigger's palette, else first).
Logical CSS; pixel-identical. Item 11 audit: Command now uses a shared listener. Beta.
Context Menu ([#83](https://github.com/kajisho5/KATA-UI/pull/83)): context-menu.js added one document pointerdown listener
per menu (3 on the three-menu page); it now adds one per script load. The window
blur listener already had a guard. Logical CSS; pixel-identical. Beta.
Hover Card ([#84](https://github.com/kajisho5/KATA-UI/pull/84)): a closed card was only opacity:0, so its heading, initials
and paragraphs stayed in the accessibility tree after the link; closed cards are
now visibility:hidden. Escape closes open cards (one shared keydown listener).
hover-card.js is a guarded IIFE. At 360px the card started at x=-73px; a
--khover-shift clamp (as Popover #56) keeps it 16px inside. 900px pixel-identical. Beta.
Data Table ([#85](https://github.com/kajisho5/KATA-UI/pull/85)): .k-dt has overflow:hidden for its corners, so at 360px
the preview (381px in 292px), combo, Dashboard demo and listing preview were
clipped and could not scroll. Tables now sit in .k-dt-scroll (role=region,
aria-label, tabindex=0, overflow-x:auto) like Table #64, with a 2px inset outline
(an outer ring would be clipped). New class .k-dt-scroll. 1280px pixel-identical. Beta.
Next: file-upload.

Remaining 19 of the forty (chosen by the session on 2026-11-06 from parts most
UI libraries ship; the queue names only 21; the owner may reorder or swap):
alert-dialog, drawer, combobox, date-picker, slider, toggle, segmented, avatar,
progress, skeleton, spinner, empty-state, separator, sidebar, command,
context-menu, hover-card, data-table, file-upload.

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
- Item 11: Combobox, Popover and Dropdown now register one outside-press listener per script load (#69, #56, #55). Date Picker since #70. Other parts were not audited for this. The JS checker does not detect every contract violation; the measured remaining JS failures are listed above.
- Item 12: Date Picker's RTL correction is merged in #26; Tag/OTP behavior (including OTP LTR/IME/completion) is merged in #27. Color Picker and Carousel visual arrows are in #29; Split Panel visual arrows are in #30.
- Item 13: Modal closes on backdrop click since #54 (browser-tested with Drawer and Alert Dialog in tools/verify_overlay_instances). Modal remains Beta until a recorded screen-reader pass.
- Item 14: inline sample styles and fixed IDs remain across legacy parts; the static inline-data-color allowance is not proof of full sample compliance.
- Items 15/16: metadata and existing Stable labels predate the full manual release gate. No new manual IME/SR certification was performed. Missing multi-instance pages for Dropdown/Tabs/Tooltip are confirmed above (Modal added in #54).
- Setup/CI: #25 added the CLI regression script and the Node 20/22 matrix to mold.yml. There is still no Python browser dependency-install step, so browser tests skip in CI. CLAUDE.md's "Pending PR #25" section predates that merge. Managed Chromium paths may not satisfy scripts hard-coded to /usr/bin/chromium.
