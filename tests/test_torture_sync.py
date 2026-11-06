"""tests/torture.html must match tools/build_torture.py output (no browser needed)."""
import unittest
from pathlib import Path

from tools import build_torture


class TortureSync(unittest.TestCase):
    def test_page_is_generated_output(self):
        self.assertEqual(build_torture.OUT.read_text(encoding='utf-8'), build_torture.build(),
                         'run python3 -m tools.build_torture')

    def test_forty_distinct_parts_with_previews(self):
        self.assertEqual(len(build_torture.PARTS), 40)
        self.assertEqual(len(set(build_torture.PARTS)), 40)
        for slug in build_torture.PARTS:
            self.assertTrue((build_torture.ROOT / 'components' / slug / 'preview.html').exists(), slug)

    def test_three_instances_and_independent_radio_groups(self):
        page = build_torture.build()
        self.assertEqual(page.count('class="tt-stage"'), 40 * 3)
        for name in ('kpay', 'cycle', 'range', 'density'):
            self.assertNotIn(f'name="{name}"', page)
            for n in (1, 2, 3):
                self.assertIn(f'name="{name}-{n}"', page)


if __name__ == '__main__':
    unittest.main()
