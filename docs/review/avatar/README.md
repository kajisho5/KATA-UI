# T4 Avatar: release procedure (KATA.md contract items 12, 14–16)

CSS only. There was no three-set page before this pass.

## What changed

- **Real name in the sample.** The preview used a real person's name; it now
  uses fictional names (Aki Morita; Ren A., Mio T., Jun O.).
- **Names.** The meta text said decorative avatars are `aria-hidden`, but no
  sample did that, so initials were read next to the visible name ("AK Aoi
  Kimura"). 31 avatars next to a visible name in blocks, templates and combos
  now carry `aria-hidden="true"`. Avatars with an `aria-label` (preview status
  avatar, Avatar combo, Dashboard topbar) get `role="img"`: a bare
  `aria-label` on a generic span is not allowed by ARIA 1.2. The preview stack
  is one `role="img"` labelled "Ren A., Mio T., Jun O. and 3 more".
- **RTL.** The status dot used `right:0`; it now uses `inset-inline-end:0`.
- `tests/test_avatar_names.py` (static, every run): every `.k-avatar` in
  components, blocks and templates is hidden or a named image. The old markup
  fails it.
- `tests/avatar-multi.html` (three sets, the third RTL) and
  `tests/test_avatar_browser.py` (CI after Chromium installs): named images,
  hidden avatars ignored by the accessibility tree, dot side in LTR/RTL,
  initials contrast.

Initials (`--k-zinc-600` on `--k-zinc-200`, not themed) measure 6.09:1 by
token value.

## Not verified

Screen readers (VoiceOver, NVDA), Safari and Firefox. The blocks and templates
were changed by markup only (one attribute per avatar); their layout is
unchanged. Beta until a recorded screen-reader pass.
