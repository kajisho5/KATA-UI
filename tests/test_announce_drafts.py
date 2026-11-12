"""The unposted announcement drafts in docs/announce/ state the repository's current numbers.

A draft stops being checked once its channel has a URL in the "Posted" table of
docs/announce/README.md: a published post keeps the numbers of its day.
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / 'docs' / 'announce'
FILES = {'Zenn': 'zenn.md', 'X': 'x.md', 'Show HN': 'show-hn.md', 'Product Hunt': 'product-hunt.md'}


def facts():
    metas = [json.loads(p.read_text(encoding='utf-8')) for p in sorted((ROOT / 'components').glob('*/meta.json'))]
    stable = sum(m.get('status') == 'stable' for m in metas)
    mold = json.loads((ROOT / 'mold-results.json').read_text(encoding='utf-8'))['summary']
    screens = json.loads((ROOT / 'comparison' / 'results.json').read_text(encoding='utf-8'))['screens']
    total = lambda draft, key: sum(s[draft][key] for s in screens)
    kb = lambda draft: round(total(draft, 'bytes') / 1000)
    return {
        'components': len(metas), 'stable': stable, 'beta': len(metas) - stable,
        'blocks': sum(1 for p in (ROOT / 'blocks').glob('*/meta.json')),
        'templates': sum(1 for p in (ROOT / 'templates').glob('*/meta.json')),
        'checked': mold['total'], 'passed': mold['passed'],
        'overflow': (total('direct', 'overflow'), total('kata', 'overflow')),
        'darkContrast': (total('direct', 'lowContrastDark'), total('kata', 'lowContrastDark')),
        'spacings': (total('direct', 'spacings'), total('kata', 'spacings')),
        'kb': (kb('direct'), kb('kata')),
        'package': json.loads((ROOT / 'cli' / 'package.json').read_text(encoding='utf-8'))['name'],
    }


# (channel, pattern, fact) — each pattern's groups must equal the fact.
CLAIMS = [
    ('Zenn', r'部品 (\d+) 個、組み合わせたブロック (\d+) 個、ページの雛形 (\d+) 個', ('components', 'blocks', 'templates')),
    ('Zenn', r'今のところ (\d+) 個（部品・ブロック・雛形）すべて', ('checked',)),
    ('Zenn', r'はみ出した要素 \| (\d+) \| (\d+) \|', ('overflow',)),
    ('Zenn', r'4\.5:1 未満 \| (\d+) \| (\d+) \|', ('darkContrast',)),
    ('Zenn', r'余白の値の種類 \| (\d+) \| (\d+) \|', ('spacings',)),
    ('Zenn', r'（合計） \| (\d+) KB \| (\d+) KB \|', ('kb',)),
    ('X', r'部品(\d+)個', ('components',)),
    ('X', r'KATA UI: (\d+) UI components', ('components',)),
    ('Show HN', r'a catalog of (\d+) UI components \(plus (\d+) blocks and (\d+) page templates\)', ('components', 'blocks', 'templates')),
    ('Show HN', r'All (\d+) parts, blocks and templates pass', ('checked',)),
    ('Show HN', r'the other (\d+) parts are labeled Beta', ('beta',)),
    ('Show HN', r'viewport went from (\d+) to (\d+)', ('overflow',)),
    ('Show HN', r'below 4\.5:1 from (\d+) to (\d+)', ('darkContrast',)),
    ('Show HN', r'grew from (\d+) KB to (\d+) KB', ('kb',)),
    ('Product Hunt', r'^(\d+) components, (\d+) blocks and (\d+) page templates', ('components', 'blocks', 'templates')),
    ('Product Hunt', r'keeps all (\d+) parts, blocks and templates', ('checked',)),
]


def posted():
    text = (DIR / 'README.md').read_text(encoding='utf-8').split('## Posted', 1)[1]
    rows = [[c.strip() for c in line.strip('|').split('|')] for line in text.splitlines() if line.startswith('|')]
    return {row[0] for row in rows[2:] if len(row) > 2 and row[2]}


class AnnounceDrafts(unittest.TestCase):
    def test_numbers_match_the_repository(self):
        f, done, wrong = facts(), posted(), []
        self.assertEqual(f['passed'], f['checked'])
        for channel, pattern, keys in CLAIMS:
            if channel in done:
                continue
            match = re.search(pattern, (DIR / FILES[channel]).read_text(encoding='utf-8'), re.M)
            if not match:
                wrong.append((channel, pattern, 'missing'))
                continue
            expected = [v for k in keys for v in (f[k] if isinstance(f[k], tuple) else (f[k],))]
            if [int(g) for g in match.groups()] != expected:
                wrong.append((channel, match.group(0), expected))
        self.assertEqual(wrong, [])

    def test_stable_wording_matches_meta(self):
        if 'Zenn' not in posted():
            self.assertEqual(facts()['stable'], 1, 'zenn.md says Button is the only Stable part; update it')

    def test_install_commands_use_the_package_name(self):
        name, done = facts()['package'], posted()
        for channel, file in FILES.items():
            if channel in done:
                continue
            for found in re.findall(r'\bnpx\s+(@?[\w.-]+(?:/[\w.-]+)?)', (DIR / file).read_text(encoding='utf-8')):
                self.assertEqual(found, name, file)

    def test_length_limits(self):
        hn = (DIR / 'show-hn.md').read_text(encoding='utf-8')
        self.assertLessEqual(len(re.search(r'## Title.*?\n\n(.+?)\n', hn, re.S).group(1)), 80)
        ph = (DIR / 'product-hunt.md').read_text(encoding='utf-8')
        self.assertLessEqual(len(re.search(r'## Tagline.*?\n\n(.+?)\n', ph, re.S).group(1)), 60)
        self.assertLessEqual(len(re.search(r'## Description.*?\n\n(.+?)\n', ph, re.S).group(1)), 260)


if __name__ == '__main__':
    unittest.main()
