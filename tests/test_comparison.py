"""The ten-screen comparison is complete and its recorded numbers match the drafts."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / 'comparison'
SCREENS = ['sign-in', 'sign-up', 'settings', 'pricing', 'dashboard',
           'data-table', 'checkout', 'inbox', 'empty-state', 'delete-confirm']
B_LINE = 'Fetch each part from kata-ui.dev/registry.json and use it unmodified.'
KEYS = {'bytes', 'buttonNoType', 'consoleErrors', 'colors', 'spacings', 'lowContrast',
        'lowContrastDark', 'unnamed', 'focusInvisible', 'tabStops', 'overflow'}


class Comparison(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = json.loads((DIR / 'results.json').read_text(encoding='utf-8'))

    def test_every_screen_has_prompt_drafts_and_shots(self):
        for screen in SCREENS:
            for name in ('prompt.md', 'direct.html', 'kata.html'):
                self.assertTrue((DIR / screen / name).is_file(), f'{screen}/{name}')
            for draft in ('direct', 'kata'):
                for theme in ('light', 'dark'):
                    self.assertTrue((DIR / 'shots' / f'{screen}-{draft}-{theme}.png').is_file())

    def test_prompt_b_is_prompt_a_plus_one_fixed_sentence(self):
        for screen in SCREENS:
            text = (DIR / screen / 'prompt.md').read_text(encoding='utf-8')
            a = re.search(r'## Prompt A \(direct\)\n\n(.+?)\n', text).group(1)
            b = re.search(r'## Prompt B \(KATA\)\n\n(.+?)\n', text).group(1)
            self.assertEqual(b, a + ' ' + B_LINE, screen)

    def test_results_cover_every_screen_and_match_file_sizes(self):
        self.assertEqual([s['slug'] for s in self.results['screens']], SCREENS)
        for s in self.results['screens']:
            for draft, name in (('direct', 'direct.html'), ('kata', 'kata.html')):
                self.assertEqual(set(s[draft]), KEYS, s['slug'])
                self.assertEqual(s[draft]['bytes'], (DIR / s['slug'] / name).stat().st_size, s['slug'])

    def test_button_type_count_matches_source(self):
        for s in self.results['screens']:
            for draft, name in (('direct', 'direct.html'), ('kata', 'kata.html')):
                html = (DIR / s['slug'] / name).read_text(encoding='utf-8')
                tags = re.findall(r'<button\b[^>]*>', html, re.I)
                missing = [t for t in tags if not re.search(r'\btype\s*=', t, re.I)]
                self.assertEqual(s[draft]['buttonNoType'], len(missing), s['slug'] + ' ' + draft)


if __name__ == '__main__':
    unittest.main()
