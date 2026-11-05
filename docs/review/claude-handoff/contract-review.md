# Approved decisions versus main

Base: 2c057fb, measured 2026-11-05 (Asia/Tokyo). Documentation review only.
No component, token or checker code was changed to make this table appear complete.
The contract is normative; the status below describes present evidence.

| KATA contract item | Evidence and present status |
|---|---|
| 1 Canonical tokens | Implemented: build.py invokes tools/sync_shape_tokens.py on system/tokens.json. |
| 2 Shared/local ownership | shared-token-scope reports zero findings. Toast-local values live in .k-toast. The static rule does not certify every possible local override. |
| 3 Profiles | check.config.json and tools/mold_rules.py implement ui/lab categories and paint-versus-geometry provenance; no rule changed here. |
| 4 Geometry | Configured border widths/circle/layout primitives and radius-full classification match the precision fixtures already in tests/mold. |
| 5 Scales | Finite radius steps follow the base, while full stays fixed at 999px. Shadow/backdrop roles exist. --k-glow is absent; optional --k-shadow-edge is absent. No missing token was added by this task. |
| 6 Rings | Distinct shared names exist. Product Page uses a focus shadow that replaces the selected shadow. Whether both states remain distinguishable needs browser evidence. |
| 7 Contrast roles | Role definitions and prior 40-part artifacts exist; no new full-catalog/state contrast certification was performed. The 4.5:1 rule is a target, not a claim that every part is verified. |
| 8 Fixed palette | Canonical fixed paint and root definitions keep zinc/asagi/yamabuki/tsutsuji independent of theme. Existing highlight repairs are retained, not re-applied. |
| 9 Motion | Shared multiplier, durations/curves and scoped reduced-motion token changes are present. Prior migration/regression artifacts exist; this handoff does not re-certify every legacy JS timing path. |
| 10 Mold compatibility | Mold v2/header/requirements/pages exist. CLI warning/safe add is in open #25, not main. Main is CLI1.0.0, engines>=18, with no npm test script. |
| 11 JS contract | Incomplete. Current JSON lists remaining failures. Combobox and Popover still use per-instance document click listeners. Passing lexical JS checks does not certify this stronger contract. |
| 12 Keyboard | Date Picker visual RTL direction is merged. Tag/OTP corrections remain in open #27. Numeric LTR/IME/completion behavior is not yet main. |
| 13 Dialogs | Alert Dialog/Drawer have reviewed native behavior. Modal has showModal/Escape but no backdrop-click close handler. |
| 14 Samples | Explicit button-type/accessible-label static checks have no findings, but inline styles and fixed IDs remain in legacy samples. Static label evidence is not a full accessible-name audit. |
| 15 Metadata | Existing descriptions still need per-part review. No real IME, screen-reader or device claims were added. |
| 16 Stable | Existing labels predate the full evidence gate. Modal/Dropdown/Tabs/Tooltip lack multi-instance pages. JSON currently fails Modal/Dropdown/Tabs; Tooltip passes. Do not infer manual verification from a label. |

Additional handoff corrections:

- The supplied assumption that #25 is merged is false at this snapshot; #26 is
  merged and #27 remains open. Main's score stays 100/164 rather than #27's 103.
- The supplied aria-sort-on-button wording is corrected to the column header,
  following WAI-ARIA; a native button still performs the sort.
- :where(targets):focus-visible has a specificity contribution outside :where.
  The future zero-specificity example wraps the entire focus selector instead.
- Spacing/type scales already exist. T3 must fill gaps/preserve aliases rather
  than assume the scales are absent and duplicate them.
- A deliberate stricter-check score drop will trip the trusted-main ratchet.
  An owner-reviewed transition is required; no automatic bypass is introduced.
- No mold.yml install/CLI steps exist in this main. The setup helper supplements
  browser dependencies without modifying the workflow. Some tools require the
  hard-coded /usr/bin/chromium path even when a managed browser is installed.

Real IME, screen readers, mobile autofill and fresh Firefox/Safari verification
were not performed in this documentation task. No visual changes were made, so
no new before/after component screenshots were produced.
