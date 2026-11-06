# File Upload review (T4)

## Changes
- **Hover/drag contrast (bug).** The hint ("PNG, JPG or PDF — up to 10 MB each") is `--k-ink-3`; on the tinted `--k-accent-bg` hover and drag background it measured 4.48:1 in light. It now uses `--k-ink-2` in those states: 7.16:1 light, 6.24:1 dark. At rest it stays `--k-ink-3` (4.83 / 5.60).
- **States (contract item 5).** Added `:active` for the zone and for the remove button, and a disabled zone (`:has(input:disabled)`: opacity .45 like Toggle, `not-allowed`, no hover tint).
- `.k-up-list` top margin → `margin-block-start`.
- `meta.json`: accessibility text records the above.

## Evidence
- `tests/test_file_upload_browser.py` over the existing `tests/file-upload-multi.html` (three sets, third `dir="rtl"`, script loaded twice): hint ≥ 4.5:1 at rest, on hover and while dragging in light and dark; remove button rest, hover and active backgrounds differ; disabled zone is dimmed with no hover tint; list spacing equal in LTR and RTL; 0 console errors. With main's CSS it fails (`light hover hint 4.48`).
- `tests.test_upload_color_carousel` (existing interaction checks) still passes.
- At rest the page is pixel-identical to main in light and dark. Screenshots of the hover state: `before-after-hover-light.png`, `before-after-hover-dark.png`.

## Not verified
- Real drag and drop from the desktop, the native picker per browser, screen readers (VoiceOver, NVDA), Safari and Firefox.
