"""The home page body stays within the Phase 2 prose budget (docs/ROADMAP.md)."""
import subprocess
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUDGET = 185  # half of the 369-word body measured before the cut


class BodyWords(HTMLParser):
    """Count whitespace-delimited words from the hero header to the last section."""

    def __init__(self):
        super().__init__()
        self.depth = 0      # nesting inside <div class="wrap lp">
        self.skip = 0
        self.words = 0

    def handle_starttag(self, tag, attrs):
        classes = (dict(attrs).get('class') or '').split()
        if self.depth:
            if tag not in ('br', 'img', 'input', 'meta', 'link', 'hr', 'source', 'wbr'):
                self.depth += 1
        elif tag == 'div' and 'wrap' in classes and 'lp' in classes:
            self.depth = 1
        if tag in ('script', 'style'):
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip -= 1
        if self.depth and tag not in ('br', 'img', 'input', 'meta', 'link', 'hr', 'source', 'wbr'):
            self.depth -= 1

    def handle_data(self, data):
        if self.depth and not self.skip:
            self.words += len(data.split())


def body_words(html):
    parser = BodyWords()
    parser.feed(html)
    return parser.words


class HomeProse(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        page = ROOT / 'dist' / 'index.html'
        if not page.exists():
            subprocess.run([sys.executable, 'build.py'], cwd=ROOT, check=True, capture_output=True)
        cls.html = page.read_text(encoding='utf-8')

    def test_counter_reads_only_the_body(self):
        sample = ('<nav>Docs Components</nav><div class="wrap lp"><h1>Two words</h1>'
                  '<script>var ignored = 1;</script><p>three more words<br>here</p></div><footer>x y</footer>')
        self.assertEqual(body_words(sample), 6)

    def test_home_body_within_budget(self):
        words = body_words(self.html)
        self.assertGreater(words, 0)
        self.assertLessEqual(words, BUDGET, f'home body has {words} words; budget is {BUDGET}')


if __name__ == '__main__':
    unittest.main()
