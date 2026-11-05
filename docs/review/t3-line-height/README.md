# T3: raw line heights → leading tokens in UI parts

Main base: `77d926e926229c88567766c820eb2724c477e9ea`, after #40 (T3 font size).
Mapping: docs/token-migration.md (T3, line height), following the KATA.md §0.5
leading table and the mold v4 `--k-lh-*` scale.

`python3 -m tools.t3_migrate line-height` rewrote 84 declarations in 58 files: each
UI-profile line-height finding that check.py reports. 45 of them keep their value
(the token equals the raw number); 39 move by 0.05–0.1 (for example 1.75 → 1.7,
1.8 → 1.85, 1.5 → 1.6, 1.12 → 1.1). Lab parts are untouched.

| | Before | After |
|---|---:|---:|
| type-values findings (all) | 205 | 121 |
| — UI line-height | 84 | 0 |
| — UI font-size | 2 | 2 |
| — Lab | 119 | 119 |
| Parts with warnings | 141 | 91 |
| Mold Verified | 164 / 164 | 164 / 164 |
| Focus stops below 3:1 / clipped (light, dark) | 0 / 0 | 0 / 0 |

The twelve main parts (Button through Tooltip) are pixel-identical before and
after in both themes: their line heights either already matched a token or sit
in closed overlays (Modal, Popover) that the default preview does not open. The
images therefore show ten parts whose values moved: Accordion, Alert, Card,
Typeset, Tabs, Timeline, Descriptions, Result, Kanban and CTA Band
(`before-after-light.png`, `before-after-dark.png`; before left, after right).
Height changes are 1–8 CSS px per part (Kanban's tallest column +8px, Typeset
−6px, Alert +5px).

Not verified: Safari/Firefox, real phones, open Modal/Popover panels by eye, and
other changed parts not in the images (list in the PR description).
