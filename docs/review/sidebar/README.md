# Sidebar review (T4)

## Changes
- **Double load (bug).** `sidebar.js` bound a click listener per toggle with no guard; loaded twice, each click flipped the group twice. It is now an IIFE with `data-kata-ready`.
- **Rail names (bug).** The rail hid `.k-side-t` with `display:none`, which removes the text from the accessibility tree; meta.json said "hidden visually, never removed". Labels and the user name are now clipped to 1px. In `tests/sidebar-multi.html`, "Overview" link names: 3 → 6 (rail links included).
- **Current page.** The `.on` link also carries `aria-current="page"`; CSS styles both.
- **RTL.** `.k-side-sub` used a physical left margin, so sub-items were indented from the wrong side in RTL. Now `margin-inline-start`; `.k-side-user` uses `margin-block-start` / `border-block-start`.
- Avatar initials are `aria-hidden`; the rail example gets the visually hidden user name.
- `meta.json`: status stable → beta until a screen-reader pass (as for the other T4 parts); accessibility text rewritten.

## Evidence
- `tests/test_sidebar_browser.py` over `tests/sidebar-multi.html` (three sets of full sidebar + rail, third `dir="rtl"`, script loaded twice): navigation names, link and button names, one `aria-current` per nav, toggle flips once per click, RTL indent mirrors LTR, text ≥ 4.5:1, 0 console errors. With main's CSS it fails (`3 != 6`); with main's JS it fails (`'true' != 'false'`).
- Text contrast (device scale 2), light / dark: item 7.73 / 6.91, section label 7.73 / 6.91, badge 7.22 / 5.81, user role 4.83 / 5.60.
- Screenshots: LTR identical to main in light and dark; `before-after-rtl-light.png`, `before-after-rtl-dark.png` show the sub-item indent move to the right.

## Not verified
- Screen readers (VoiceOver, NVDA), Safari and Firefox, touch devices.
