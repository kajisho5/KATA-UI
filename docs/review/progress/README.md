# Progress review (T4)

## Changes
- `components/progress/preview.html`: both progress bars now carry `aria-label` ("Uploading footage", "Verifying files"). Before, Chromium exposed both as unnamed progressbars.
- `components/progress/meta.json`: accessibility text names the label requirement and the RTL fill direction.
- No other `role="progressbar"` without a name exists in components, blocks or templates (searched).

## Evidence
- `tests/test_progress_browser.py` over `tests/progress-multi.html` (three sets, the third `dir="rtl"`):
  - accessible names `['Uploading footage', 'Verifying files'] × 3` (before: six empty names);
  - values 68 and 92;
  - LTR fill starts at the left edge, RTL fill at the right edge (±1px);
  - percentage text contrast ≥ 4.5:1 in light and dark.
- Measured text contrast (device scale 2): task name 17.72 light / 16.12 dark, percentage 7.73 / 6.91.

## Not verified
- Screen readers (VoiceOver, NVDA), Safari and Firefox.
- Live updates: the preview is static; announcing changes depends on the user's own script.
