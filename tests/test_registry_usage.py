"""registry.json (and so the MCP server) carries each part's status, usage and accessibility text."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RegistryUsage(unittest.TestCase):
    def test_meta_matches_source(self):
        path = ROOT / 'dist' / 'registry.json'
        if not path.exists():
            subprocess.run([sys.executable, 'build.py'], cwd=ROOT, check=True, capture_output=True)
        items = json.loads(path.read_text(encoding='utf-8'))['items']
        folders = {'registry:component': 'components', 'registry:block': 'blocks', 'registry:page': 'templates'}
        checked = 0
        for item in items:
            folder = folders.get(item['type'])
            if not folder:
                continue
            meta = json.loads((ROOT / folder / item['name'] / 'meta.json').read_text(encoding='utf-8'))
            self.assertEqual(item['meta'], {'status': meta.get('status', 'stable'), 'usage': meta.get('usage', ''),
                                            'accessibility': meta.get('a11y', '')}, item['name'])
            checked += 1
        self.assertGreater(checked, 0)


if __name__ == '__main__':
    unittest.main()
