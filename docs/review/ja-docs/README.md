# Japanese docs: ten parts

Pages `/ja/components/button/` and `/ja/components/input/`, built by `ja_detail()` in
build.py from `ja/components/<slug>.json`. Full-page screenshots: light and dark, 1280px
and 390px. No horizontal page scroll at either width; no console errors other than the
analytics beacon's CORS error on 127.0.0.1.

`tests/test_ja_docs.py` stores the SHA-1 of the English description, usage and a11y the
translation was made from. Changing `components/button/meta.json` usage made the test
fail (checked once, then reverted).

Not verified: translation reviewed by a native speaker, screen readers reading Japanese,
Safari, Firefox, real devices.

Field, Textarea, Select, Checkbox, Radio, Switch, Modal and Dropdown (PR #100): full-page
screenshots at 1280px light and 390px dark. No console errors other than the beacon, no
horizontal page scroll. Modal opens and Dropdown expands from the Japanese page's stage.
