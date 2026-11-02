# 09 — Structure audit: KATA vs shadcn/ui (2026-11-02, second pass)

Grounded in ui.shadcn.com/llms.txt fetched fresh 2026-11-02 (their current taxonomy),
not memory. The first completion pass added pieces; this audit is about composition.

## Where KATA's structure is thinner

### A. Component detail pages (biggest multiplier — ×79 pages)
shadcn part pages carry: preview/code, **Installation (CLI + manual)**,
**Usage with code**, **API reference (props tables)**, examples, prev/next pager.
KATA pages have preview/code, prose Usage, prose Accessibility, Examples, Related
and a prev/next pager — but NO per-part Installation block and NO API/anatomy
table. (Prev/next exists — corrected on implementation, 2026-11-02.)

### B. Part genres shadcn lists today that KATA lacks
From their current catalog: **Button Group, Input Group, Collapsible,
Toggle Group, Sidebar (as a part), Navigation Menu, Calendar (standalone)**.
(KATA covers Sheet≈Drawer, Native Select≈Select, Item≈List, Field ✓.)
Earlier genre audit predates these shadcn additions.

### C. Docs architecture
- **Registry**: shadcn documents the registry in 11 pages. KATA publishes
  registry.json but explains it almost nowhere (CLI doc only). Missing:
  a Registry doc (format, item fields, how tools consume it).
- **Forms**: shadcn has a Forms section (overview + patterns). KATA has the
  Field part and an auth guide, but no Forms overview (composition,
  validation states, error summary patterns).
- **Introduction**: their Overview leads with principles. KATA's principles
  live in Why Vanilla / The Mold (Concepts) — no Introduction entry in the
  Getting Started group.
- **AI**: Skills doc ✓ equivalent exists (SKILL.md). **MCP server: missing**
  (deferred in the first pass). Their MCP doc + server is a headline feature.
- **RTL**: they have an RTL section. KATA has nothing — parts use physical
  left/right in places (tour, drawer, popover). Needs a logical-property
  pass on chrome + key parts and an honest doc note.
- components.json config doc: KATA's CLI has flags only, no config file.
  A kata.config doc is optional; skip unless the CLI grows one.

### D. Product structure
- No real **Pricing page** for the product itself (the Pricing block is a
  demo part, not KATA's own pricing). Free vs Pro Lifetime needs a page.
- Blocks index is one flat grid; shadcn categorizes. Minor.
- Homepage composition is fine (live parts, comparison, FAQ) — not a gap.

## Build order
- P1 Detail pages: Installation block (CLI + manual + deps), prev/next
  pager, Anatomy table (classes + data hooks extracted from the part itself).
- P2 Missing parts: Button Group, Input Group, Collapsible, Toggle Group,
  Sidebar, Navigation Menu, Calendar. 79 → 86 parts.
- P3 Docs: Registry, Forms overview, Introduction; llms/nav follow.
- P4 MCP server (single-file Node, stdio, serves the registry) + MCP doc.
- P5 RTL pass + note.
- P6 Pricing page; blocks index categories.

## Not gaps (checked, do not redo)
Nav tree (unified, shadcn-shaped) ✓ · ⌘K search ✓ · themes + builder ✓ ·
per-stack install guides ✓ (theirs are framework installs; ours match our
stacks) · Typeset ✓ · CLI ✓ · Skill ✓ · dark mode (one attribute, doc'd) ✓.
