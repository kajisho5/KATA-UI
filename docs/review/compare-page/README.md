# /compare/ page

Built by `build.py` (`compare_page()`) from `comparison/results.json`; raw drafts and
screenshots are copied to `/compare/<screen>/` and `/compare/shots/`.
`tests/test_comparison.py` checks that every number on the page equals results.json.

Screenshots: light and dark, 1280px and 390px, top of page and the Dashboard section.
No horizontal page scroll at either width. Console: only the analytics beacon's CORS error,
which every page shows when served from 127.0.0.1.

Not verified: screen readers, Safari, Firefox, real devices.
