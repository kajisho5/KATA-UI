# 10 — Gap hunt, second sweep (2026-11-02, user: 探せ)

Method: KATA's current 80 slugs mapped against (a) shadcn/ui's catalog fetched
fresh today (llms.txt), (b) the 6-library union from 07-genre-audit.md
(shadcn / Radix / MUI / Ant Design / Web Awesome / Flux), (c) direct greps of
KATA's own examples to verify "covered at example level" claims — two of those
claims turned out stale (see Button Group / Input Group).

## Verified missing as parts

| # | Genre | Who carries it | Note |
|---|---|---|---|
| 1 | Button Group | shadcn, MUI, AntD, WA, Flux | Not even an example in Button (examples are Variants/Sizes/Icons/States/Loading — grep-verified). |
| 2 | Input Group | shadcn, AntD, WA | Addons (prefix/suffix/attached button) — no addon example in Input either (grep-verified). |
| 3 | Navigation Menu | shadcn, Radix, MUI | Header nav with dropdown panels. Site Header block has plain links only. |
| 4 | Menubar | shadcn, Radix | Desktop-app menu bar (File/Edit/View…). |
| 5 | Collapsible | shadcn, Radix, MUI | Single disclosure unit; Accordion is the group pattern. |
| 6 | Calendar | shadcn, MUI, AntD, WA, Flux | Standalone month grid; today it exists only inside Date Picker (its JS is 50 lines — extractable). |
| 7 | Comparison Slider | WA (image-comparer), AntD-adjacent | Before/after drag — a Motion-shaped showpiece. |
| 8 | Float Button / Speed Dial | MUI, AntD | FAB + expanding action fan. |
| 9 | Anchor / Scrollspy | AntD | In-page nav tracking scroll position; docs sites need it. |
| 10 | Bottom Navigation | MUI | Mobile app tab bar — squarely the app-factory audience. |
| 11 | Descriptions | AntD | Definition-list display; Stat covers numbers only (07 partial, still open). |
| 12 | Result | AntD | Success/error outcome panel; Empty State is adjacent, not this (07 partial, still open). |
| 13 | Time Picker | AntD, Flux | The Date Picker's missing other half. |
| 14 | Cascader | AntD | Multi-level select (region trees etc.). Hard. |
| 15 | QR Code | WA, AntD | 07 said skip (encoder lib breaks zero-dep). A hand-rolled byte-mode encoder keeps zero-dep — re-opened as possible. |
| 16 | Transfer | AntD, MUI | Dual listbox. Real but rare; low priority. |

## Block-level, not a part
- Kanban board (Flux Pro genre) → Blocks backlog (would make 14 blocks).

## Skip, with reasons (checked, not overlooked)
- Rich Text Editor — a product, not a part; every serious one is an engine.
- Mentions — too app-specific; belongs to the app, not the mold.
- Watermark — one CSS trick; a doc recipe at most.
- Phone Input — the hard part is locale data, not the widget.
- Video Player — the vanilla answer is the <video> element itself; WA ships
  one, but skinning native controls is a recipe, not a part.
- TreeSelect — Tree + Select composition; revisit after Cascader.

## Build order (folds into the P2 queue)
Cheap first: Button Group, Input Group, Collapsible, Descriptions, Result,
Bottom Navigation. Then: Calendar (extract), Comparison Slider, Speed Dial,
Scrollspy, Navigation Menu, Menubar, Time Picker. Last: Cascader, QR Code,
Transfer. Kanban to the Blocks backlog.
