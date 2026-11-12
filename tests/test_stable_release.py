"""A part may carry status "stable" only after the full release procedure (KATA.md contract item 16).

Evidence required per part, all read from the repository:
  static     every failure check passes in mold-results.json
  multi      tests/<slug>-multi.html with an RTL instance, and the part's script
             loaded twice when it has one
  browser    a test or verify tool that opens that page (it asserts the three
             instances; page layouts differ, so the count is not parsed here)
  reader     a recorded screen-reader pass at docs/review/<slug>/screen-reader.md
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def release_gaps(slug):
    """Names of the release steps that have no evidence for components/<slug>."""
    gaps = []
    results = json.loads((ROOT / 'mold-results.json').read_text(encoding='utf-8'))
    item = next((i for i in results['items'] if i['id'] == 'components/' + slug), None)
    if not item or not item['passed']:
        gaps.append('static')
    page = ROOT / 'tests' / f'{slug}-multi.html'
    if not page.exists():
        gaps.append('multi')
    else:
        html = page.read_text(encoding='utf-8')
        scripts = re.findall(rf'<script\b[^>]*src="[^"]*components/{re.escape(slug)}/{re.escape(slug)}\.js"', html)
        has_js = (ROOT / 'components' / slug / f'{slug}.js').exists()
        if not re.search(r'\bdir\s*=\s*"rtl"', html) or (has_js and len(scripts) < 2):
            gaps.append('multi')

    def opens_page(text):
        # A literal path, or a loop over slugs that builds f'{slug}-multi.html'.
        return f'{slug}-multi.html' in text or (re.search(r'\{\w+\}-multi\.html', text) and f"'{slug}'" in text)

    users = [p for p in [*ROOT.glob('tests/test_*.py'), *ROOT.glob('tools/verify_*.py')]
             if p.name != Path(__file__).name and opens_page(p.read_text(encoding='utf-8'))]
    if not users:
        gaps.append('browser')
    if not (ROOT / 'docs' / 'review' / slug / 'screen-reader.md').exists():
        gaps.append('reader')
    return gaps


class StableRelease(unittest.TestCase):
    def test_every_stable_part_has_the_full_release_evidence(self):
        stable = [p.parent.name for p in sorted((ROOT / 'components').glob('*/meta.json'))
                  if json.loads(p.read_text(encoding='utf-8')).get('status') == 'stable']
        self.assertIn('button', stable)
        self.assertEqual({slug: release_gaps(slug) for slug in stable if release_gaps(slug)}, {})

    def test_gaps_name_the_missing_steps(self):
        # Passing case: Button has every step.
        self.assertEqual(release_gaps('button'), [])
        # Failing cases: these beta parts lack a recorded screen-reader pass, and
        # Glow Button has no three-instance page or browser test at all.
        self.assertEqual(release_gaps('pixel-switch'), ['reader'])
        self.assertEqual(release_gaps('glow-button'), ['multi', 'browser', 'reader'])
        self.assertEqual(release_gaps('no-such-part'), ['static', 'multi', 'browser', 'reader'])


if __name__ == '__main__':
    unittest.main()
