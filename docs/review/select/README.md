# T4 Select: release procedure (KATA.md contract items 11, 14–16)

Main base: `d2046dbb29bc1714f1fb0db02f4b4b4a38a4139c` (after #47, Textarea). No JavaScript.

## What changed

- **RTL overlap.** The chevron uses `inset-inline-end`, so in RTL it sits on the
  left, but the select's padding was physical (`0 32px 0 12px`): the 32px room
  stayed on the right and long text ran under the chevron. Padding is now
  `padding-inline: 12px 32px`. LTR rendering is pixel-identical
  (`rtl-before-after-{light,dark}.png` shows RTL).
- **Global side effect removed.** select.css set `color-scheme` on `:root`, so any
  page that loaded it (and the one-file bundle kata-ui.css) switched scrollbars and
  native controls for the whole page. It is now set on `.k-select select` only.
  site.css sets the KATA site's own `color-scheme`, so the site keeps its dark
  scrollbars. Pages that relied on the old side effect set their own
  `color-scheme` (the docs already say the page decides its theme).
- Hover no longer changes a disabled select; `aria-invalid="true"` draws the
  danger border, as in Input and Textarea.
- `tests/select-multi.html` (three sets, set 3 RTL, invalid and long-option
  examples) and `tests/test_select_browser.py`, run in CI after Chromium installs.
  The test fails on the old CSS (`:root` color-scheme) and passes on the new.

## Browser test

15 selects named by their wrapping labels; `:root` color-scheme is `normal`;
keyboard focus ring; ArrowDown changes the value; invalid border differs; disabled
is not-allowed, keeps its border on hover and is skipped by Tab; the chevron sits
inside the inline-end padding in LTR and RTL. 16px or more and no sideways scroll
at 375px. Console clean. Text contrast (pixels at 2x): light: value 17.72, disabled 4.83; dark: value 16.12, disabled 5.6.

## Not verified

Screen readers, the native option list on iOS/Android, Safari, Firefox, real
devices, 200% zoom. IME does not apply.
