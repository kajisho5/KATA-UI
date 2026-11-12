# Show HN draft

## Title (80 characters max)

Show HN: KATA UI – copy-paste components in plain HTML, CSS and JS

## URL

https://kata-ui.dev

## First comment

I built KATA UI, a catalog of 137 UI components (plus 21 blocks and 7 page templates) written in plain HTML, CSS and JavaScript. You copy a part's files into your project, by hand or with a one-file CLI (npx @kajisho5/kataui add button), and the code is yours. MIT.

Every part reads its colors, radii, shadows and durations from one tokens.css. A static checker (check.py, in the repo) fails a part that uses raw values, lacks :focus-visible, leaves a <button> without a type, or breaks when its script loads twice. All 165 parts, blocks and templates pass it today.

A static check reads code and cannot tell whether a screen reader can use a part, so "Stable" has a separate bar: a three-instance test page with an RTL copy, a browser regression test, and a recorded screen-reader pass. Only Button meets it so far; the other 136 parts are labeled Beta.

There is also a registry.json in the shadcn registry format, llms.txt, an MCP server and an AI Skill. I asked Claude Code to build the same ten screens twice, once from a plain prompt and once with "use the parts from registry.json" added. Across the ten, elements overflowing a 390px RTL viewport went from 43 to 0 and dark-mode text below 4.5:1 from 6 to 0, while the files grew from 109 KB to 287 KB. Prompts and unedited outputs: https://kata-ui.dev/compare/

Feedback on the checker rules and on parts that fall short is very welcome.
