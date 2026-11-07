# AI integration test: Claude Code

Run on 2026-11-07 in a Linux cloud container. Claude Code 2.1.319, Node v22.23.4, headless
mode (`claude -p`). Each run started from an empty folder with no project files, so only the
named KATA surface was available. The agent's final answer is quoted unedited; its
transcripts are not published because they carry environment details.

Cursor: **not tested.** Cursor cannot run in this environment. The commands below are the
Claude Code ones; a Cursor run needs a person with Cursor installed.

## 1. MCP server

```bash
curl -fsSL https://kata-ui.dev/mcp/kata-ui-mcp.mjs -o kata-ui-mcp.mjs
# mcp.json — the configuration from /docs/mcp-server/
claude -p "Using the kata-ui MCP server, find the KATA UI Switch component and give me its HTML markup exactly as the server returns it, plus the one-line usage note. Do not write any files." \
  --mcp-config mcp.json --strict-mcp-config \
  --allowedTools "mcp__kata-ui__list_components,mcp__kata-ui__search_components,mcp__kata-ui__get_component,mcp__kata-ui__get_audit" \
  --output-format json --max-turns 6
```

Protocol check before the run (JSON-RPC over stdio): `initialize` returned serverInfo
kata-ui 1.0.0, protocol 2024-11-05; `tools/list` returned get_audit, list_components,
search_components, get_component; `get_component` for button returned 6498 characters.

Result: success, 4 turns, 11.2 s. Answer:

> Here's the KATA UI **Switch** (`switch`, version 1.1.0) as the kata-ui server returned it from `get_component`. I didn't write any files.
>
> **HTML markup** (`components/switch/example.html`), exactly as returned:
>
> ```html
> <!-- KATA switch 1.1.0 — kata-ui.dev/components/switch — requires mold >= 3 -->
> <label class="switchrow"><span class="switch"><input role="switch" type="checkbox" checked><span class="tr"></span></span>Notifications</label>
> <label class="switchrow"><span class="switch asagi"><input role="switch" type="checkbox" checked><span class="tr"></span></span>Auto-save</label>
> <label class="switchrow"><span class="switch"><input role="switch" type="checkbox"><span class="tr"></span></span>Public</label>
> ```
>
> **One-line usage note:** the server has no field called "usage note." The closest thing is the component's description, which is one line:
>
> > A real checkbox underneath, so it works with no JS at all. Asagi variant included.
>
> - **Mold version:** the part needs mold 3 or newer (`requiresMold: 3`), and the server is on mold 5. Before you use it, check the version in the header of your `tokens.css`.
> - **Stylesheet:** the markup only renders correctly with the part's stylesheet, `components/switch/switch.css`. The server returned that file too, and I can paste it if you want it.

Finding: the server returns the markup and the description but no usage or accessibility
text, so the agent reported that no usage note exists.

## 2. AI Skill (SKILL.md)

```bash
mkdir -p .claude/skills/kata-ui
curl -fsSL https://kata-ui.dev/skill/SKILL.md -o .claude/skills/kata-ui/SKILL.md
claude -p "I want a KATA UI toggle switch for a settings row in plain HTML. Which files do I need and what is the markup? Do not write files." \
  --output-format stream-json --verbose --max-turns 8 --allowedTools "Skill,WebFetch,Read"
```

Result: success, 8 turns, 40.8 s. The agent loaded the `kata-ui` skill without being told
to, then fetched llms.txt and the Switch page (two shell calls were refused because Bash was
not allowed). Answer, first 1600 characters (the rest lists the CSS and the markup):

> You need two pieces of CSS and no JavaScript. The Switch part is a native checkbox, so it works without a script.
>
> ## Files
>
> 1. **`tokens.css`**: load it once, before any part. The switch's CSS reads its colors, spacing, radius and motion values from these tokens. If you'd rather use one file, the `kata-ui.css` bundle from the [Installation doc](https://kata-ui.dev/docs/installation/) covers both of these.
> 2. **The Switch CSS**: copy it from the CSS tab at https://kata-ui.dev/components/switch/, or run `npx @kajisho5/kataui add switch`, which fetches it along with its dependencies.
>
> ```html
> <link rel="stylesheet" href="tokens.css">
> <link rel="stylesheet" href="switch.css"> <!-- your copy of the Switch CSS -->
> ```
>
> ## Markup
>
> This is the part's basic row:
>
> ```html
> <label class="switchrow">
>   <span class="switch">
>     <input role="switch" type="checkbox" checked>
>     <span class="tr"></span>
>   </span>
>   Notifications
> </label>
> ```
>
> - **Accent colour:** add `asagi` to the switch span (`<span class="switch asagi">`).
> - **Disabled:** add `disabled` to the `<input>`.
> - **Off by default:** leave out `checked`.
>
> **If the label text sits outside the `<label>`**, as it often does in a settings row with a description underneath, the input has no name. Give it one with `aria-label`, or point `aria-labelledby` at the text's id:
>
> ```html
> <span class="switch">
>   <input role="switch" type="checkbox" aria-label="Weekly summary" checked>
>   <span class="tr"></span>
> </span>
> ```
>
> The page's "Settings list" example stacks several `.switchrow` labels in a grid with `gap: var(--k-space-3)` and `max

## 3. llms.txt

```bash
claude -p "Read https://kata-ui.dev/llms.txt. From it alone, tell me: how many components KATA UI has, the CLI command to add the Button component, and the URL of the registry file. Quote the lines you used." \
  --output-format stream-json --verbose --max-turns 12 --allowedTools "WebFetch"
```

A first run with `--max-turns 5` stopped at the turn limit. Second run: success, 6 turns,
29.1 s. Answer:

> KATA UI has **164 components**, the command to add Button is `npx @kajisho5/kataui add button`, and the registry is at `https://kata-ui.dev/registry.json`. I couldn't read the file's raw text: fetching it with `curl` needed your approval, and the web-fetch tool I used instead passes the page through a summarizing model. The lines below are what that tool returned as exact quotes, so they could be slightly off. If you approve `curl`, I can check them against the raw file.
>
> **Number of components: 164**
> > "164 parts. Static checks only. Updated 2026-11-07 (Asia/Tokyo)."
>
> The file calls them "parts", not "components". Its audit badges split the 164 into two groups: "UI 121/121" and "Lab 43/43". If you only want stable components and the Lab parts are experimental, the number would be **121**. The file doesn't say what "Lab" means, so that's my guess.
>
> **CLI command to add Button:**
> > "npx @kajisho5/kataui add button"
>
> **Registry file URL:**
> > "https://kata-ui.dev/registry.json"

Finding: the answer says 164 components. The catalog has 136 components, 21 blocks and 7
templates (164 checked parts in total). llms.txt opens with the audit line "164 parts" and
does not state the component count on its own line.

## Findings to fix (separate PRs)

1. llms.txt: state 136 components, 21 blocks and 7 templates near the top, apart from the
   164-part audit line. Fixed in PR #105; a rerun with the new file (Read on a local copy) answered "136 components" and explained the 164.
2. MCP `get_component`: include the part's usage and accessibility text from meta.json.
3. registry.json: no item carries tokens.css; agents fetch it separately (also seen in the
   ten-screen comparison, PR #96).
