"""llms.txt states the component count on its own, apart from the audit's part total (docs/review/ai-integration)."""
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class LlmsCounts(unittest.TestCase):
    def test_catalog_line_matches_the_folders(self):
        page = ROOT / 'dist' / 'llms.txt'
        if not page.exists():
            subprocess.run([sys.executable, 'build.py'], cwd=ROOT, check=True, capture_output=True)
        text = page.read_text(encoding='utf-8')
        head = text.split('[Mold Verified', 1)[0]
        match = re.search(r'Catalog: (\d+) components, (\d+) blocks, (\d+) templates', head)
        self.assertIsNotNone(match, 'llms.txt must state the counts before the audit line')
        counts = [int(n) for n in match.groups()]
        expected = [len([p for p in (ROOT / d).iterdir() if (p / 'meta.json').exists()])
                    for d in ('components', 'blocks', 'templates')]
        self.assertEqual(counts, expected)


if __name__ == '__main__':
    unittest.main()
