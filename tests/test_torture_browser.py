"""Torture Test matrix: 8 conditions over tests/torture.html; fails on failures not in results.json."""
import importlib.util
import json
import os
import shutil
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHROMIUM = os.environ.get('CHROMIUM_PATH') or shutil.which('chromium') or '/usr/bin/chromium'
AVAILABLE = importlib.util.find_spec('playwright') is not None and Path(CHROMIUM).exists()


@unittest.skipUnless(AVAILABLE, 'Requires Playwright Python and Chromium')
class TortureBrowser(unittest.TestCase):
    def test_no_new_failures(self):
        from tools import verify_torture
        results = verify_torture.run()
        known = json.loads((verify_torture.OUT / 'results.json').read_text(encoding='utf-8'))['results']
        self.assertEqual(sorted(results), sorted(verify_torture.CONDITIONS))
        new = sorted(verify_torture.keys(results) - verify_torture.keys(known))
        self.assertEqual(new, [], 'new Torture Test failures; fix them or explain in the PR')
        # Every condition walks the whole page and the three instances stay in step.
        for condition, result in results.items():
            self.assertGreater(result['tab_stops'], 120, condition)

    def test_toolbar_sets_direction_and_theme(self):
        import functools, http.server, threading
        from playwright.sync_api import sync_playwright
        from tools.verify_torture import Quiet
        server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(ROOT)))
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.server_close); self.addCleanup(server.shutdown)
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 1280, 'height': 900})
                page.goto(f'http://127.0.0.1:{server.server_port}/tests/torture.html?dir=rtl')
                state = "() => [document.documentElement.dir, document.documentElement.dataset.theme]"
                self.assertEqual(page.evaluate(state), ['rtl', 'light'])
                page.get_by_role('radio', name='Dark').click()
                self.assertEqual(page.evaluate(state), ['rtl', 'dark'])
                self.assertIn('theme=dark', page.url)
                page.get_by_role('radio', name='LTR').click()
                self.assertEqual(page.evaluate(state), ['ltr', 'dark'])
                page.select_option('#tt-jump', 'part-tabs')
                self.assertEqual(page.evaluate('() => document.activeElement.id'), 'h-tabs')
            finally:
                browser.close()


if __name__ == '__main__':
    unittest.main()
