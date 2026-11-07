"""Japanese docs stay in step with the English meta.json they translate (docs/design/ja-docs.md)."""
import ast
import hashlib
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JA = ROOT / 'ja' / 'components'
SOURCE_KEYS = ('description', 'usage', 'a11y')


def sha1(text):
    return hashlib.sha1(text.encode('utf-8')).hexdigest()


class JaDocs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(ROOT))
        source = (ROOT / 'build.py').read_text(encoding='utf-8')
        cls.planned = re.search(r"^JA_DOCS = (\[.*?\])", source, re.M).group(1)
        cls.docs = {p.stem: json.loads(p.read_text(encoding='utf-8')) for p in sorted(JA.glob('*.json'))}
        if not (ROOT / 'dist' / 'ja' / 'components').exists():
            subprocess.run([sys.executable, 'build.py'], cwd=ROOT, check=True, capture_output=True)

    def test_only_planned_parts_are_translated(self):
        planned = ast.literal_eval(self.planned)
        self.assertEqual(len(planned), 10)
        self.assertTrue(set(self.docs) <= set(planned), set(self.docs) - set(planned))

    def test_translations_match_current_english(self):
        for slug, doc in self.docs.items():
            meta = json.loads((ROOT / 'components' / slug / 'meta.json').read_text(encoding='utf-8'))
            for key in SOURCE_KEYS:
                self.assertEqual(doc['source']['sha1'][key], sha1(meta[key]),
                                 f'{slug}.{key}: the English text changed; update ja/components/{slug}.json and its sha1')

    def test_entries_are_complete_japanese(self):
        for slug, doc in self.docs.items():
            self.assertEqual(doc['slug'], slug)
            for key in ('name_ja', 'description', 'usage', 'a11y'):
                self.assertRegex(doc[key], r'[぀-ヿ一-鿿]', f'{slug}.{key}')
            self.assertRegex(doc['source']['date'], r'^\d{4}-\d{2}-\d{2}$')

    def test_pages_link_both_ways_and_show_the_same_code(self):
        for slug, doc in self.docs.items():
            ja = (ROOT / 'dist' / 'ja' / 'components' / slug / 'index.html').read_text(encoding='utf-8')
            en = (ROOT / 'dist' / 'components' / slug / 'index.html').read_text(encoding='utf-8')
            self.assertIn('<html lang="ja">', ja)
            self.assertIn(f'href="/components/{slug}/" hreflang="en"', ja)
            self.assertIn(f'href="/ja/components/{slug}/" hreflang="ja"', en)
            self.assertIn(doc['usage'].replace('"', '&quot;').split('。')[0], ja.replace('&#x27;', "'"))
            preview = (ROOT / 'components' / slug / 'preview.html').read_text(encoding='utf-8').strip()
            self.assertIn(preview, ja)


if __name__ == '__main__':
    unittest.main()
