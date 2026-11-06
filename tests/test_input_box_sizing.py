"""Optional browser regression: .input fits its container (border-box); requires Playwright Python and Chromium."""
import functools
import http.server
import importlib.util
import os
import shutil
import threading
import unittest
from pathlib import Path

CHROMIUM = os.environ.get('CHROMIUM_PATH') or shutil.which('chromium')
AVAILABLE = importlib.util.find_spec('playwright') is not None and bool(CHROMIUM) and Path(CHROMIUM).exists()
PAGES = ['input-multi.html', 'date-picker-multi.html', 'field-multi.html']


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


@unittest.skipUnless(AVAILABLE, 'Requires Playwright Python and Chromium')
class InputBoxSizing(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close); self.addCleanup(self.server.shutdown)
        self.base = f'http://127.0.0.1:{self.server.server_port}/tests/'

    def test_inputs_fit_their_container_at_360px(self):
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 360, 'height': 900})
                for name in PAGES:
                    page.goto(self.base + name)
                    over = page.evaluate('''() => [...document.querySelectorAll('.input')].filter(i => {
                        const r = i.getBoundingClientRect(), p = i.parentElement.getBoundingClientRect();
                        return r.width && (r.right > p.right + 0.5 || r.left < p.left - 0.5);
                    }).length''')
                    self.assertEqual(over, 0, name)
                    self.assertLessEqual(page.evaluate('document.documentElement.scrollWidth'), 360, name)
                    # Border-box: the 38px height includes the border, matching .btn-md.
                    heights = set(page.evaluate("[...document.querySelectorAll('input.input')].map(i => Math.round(i.getBoundingClientRect().height))"))
                    self.assertEqual(heights, {38}, name)
            finally:
                browser.close()


if __name__ == '__main__':
    unittest.main()
