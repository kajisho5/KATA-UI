# T4 Slider: release procedure (KATA.md contract items 11, 12, 14–16)

## What changed

- **RTL fill (bug).** The filled track was a fixed left-to-right gradient. A
  native range runs right to left in RTL, so the fill sat on the wrong side of
  the thumb (left image, lower half). The WebKit track now uses a `to left`
  gradient under `:dir(rtl)`; Firefox's `::-moz-range-progress` already
  followed the direction.
- **Samples without fixed IDs (item 14).** The preview used `id="sl-vol"` /
  `for`. Each `<label class="k-slider-row" data-slider>` now wraps its range;
  the readout is `aria-hidden` because the range already exposes its value.
  The inline row styles became `.k-slider-row`, `.k-slider-head`,
  `.k-slider-label` and `.k-slider-val`.
- **Thumb outline.** `--k-border-strong` (#c9c9cf) was 1.6:1 against the white
  page with a white knob; it now uses `--k-ink-3` (#71717a, 4.83:1), as
  Checkbox and Radio did in #49 and #50.
- **slider.js (item 11).** IIFE and `data-kata-ready`, so a second load does
  not bind a second listener.
- meta.json: legacy wording updated; status beta.
- `tests/slider-multi.html` (three sets, the third RTL, script loaded twice)
  and `tests/test_slider_browser.py` (CI after Chromium installs): ready
  markers, no IDs, names Volume/Brightness, one step per ArrowUp with readout
  and `--p` in sync, fill on the correct side in LTR and RTL. The old files
  fail it.

`before-after-{light,dark}.png`: LTR (top) and RTL (bottom), old (left) and new
(right).

## Not verified

Screen readers (VoiceOver, NVDA), Safari (WebKit track) and Firefox, touch
dragging. Beta until a recorded screen-reader pass.
