# T4 Date Picker: release procedure (KATA.md contract item 11)

The part already had its three-instance page and keyboard/RTL/motion coverage
(`tests/test_command_context_date.py`, #26).

## What changed

- date-picker.js: every instance added its own `document` pointerdown
  listener. One listener per script load now closes every instance the press
  is outside of (contract item 11: register document listeners once per part
  type, not per instance).
- `tests/test_date_picker_browser.py` (CI after Chromium installs): on the
  three-instance page with the script loaded a second time, the document has
  one pointerdown listener (the old script has three), and an outside press
  closes each open calendar.
- meta.json: the accessibility text mentions the outside-press behaviour.

## Found, not fixed here

At 320px the page scrolls sideways by 44px: `.input` is content-box, so
`width:100%` plus its padding overflows the 300px picker. This is the Input
box-sizing follow-up already recorded in HANDOFF; it touches about ten parts
and gets its own PR with screenshots.

## Not verified

Screen readers (VoiceOver, NVDA), Safari and Firefox, touch devices. Status
stays beta. No visual change.
