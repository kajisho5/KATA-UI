"""The home page prints the Stable / Beta split counted from meta.json."""
import json
import unittest
from pathlib import Path

import build

ROOT = Path(__file__).resolve().parents[1]


class HomeStatusSplit(unittest.TestCase):
    def test_counts_match_meta_and_reach_the_hero(self):
        comps = build.load_components()
        statuses = [json.loads(p.read_text(encoding='utf-8')).get('status')
                    for p in sorted((ROOT / 'components').glob('*/meta.json'))]
        stable = statuses.count('stable')
        self.assertEqual(build.status_split(comps), (stable, len(comps) - stable))
        self.assertEqual(len(comps), len(statuses))
        html = build.landing(comps, build.load_blocks(), 0, build.load_templates())
        self.assertIn(f'<a href="/components/?status=stable">{stable} stable</a>', html)
        self.assertIn(f'<a href="/components/?status=beta">{len(comps) - stable} beta</a>', html)

    def test_stable_needs_a_recorded_screen_reader_pass(self):
        # Phase 1: a part is Stable only after the checks and a recorded screen-reader pass,
        # kept at docs/review/<slug>/screen-reader.md.
        missing = [p.parent.name for p in sorted((ROOT / 'components').glob('*/meta.json'))
                   if json.loads(p.read_text(encoding='utf-8')).get('status') == 'stable'
                   and not (ROOT / 'docs' / 'review' / p.parent.name / 'screen-reader.md').exists()]
        self.assertEqual(missing, [], 'stable parts without docs/review/<slug>/screen-reader.md')


if __name__ == '__main__':
    unittest.main()
