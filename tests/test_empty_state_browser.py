"""Optional browser regression for EmptyState; requires Playwright Python and Chromium."""
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


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


@unittest.skipUnless(AVAILABLE, 'Requires Playwright Python and Chromium')
class EmptyStateBrowser(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close); self.addCleanup(self.server.shutdown)
        self.url = f'http://127.0.0.1:{self.server.server_port}/tests/empty-state-multi.html'

    def test_names_icon_text_and_narrow_width(self):
        from playwright.sync_api import sync_playwright
        from tools.verify_button import text_contrast
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 600, 'height': 900}, device_scale_factor=2)
                errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.on('console', lambda m: m.type == 'error' and errors.append(m.text))
                page.goto(self.url)
                cdp = page.context.new_cdp_session(page); cdp.send('Accessibility.enable')
                nodes = [n for n in cdp.send('Accessibility.getFullAXTree')['nodes'] if not n.get('ignored')]
                role = lambda r: [n.get('name', {}).get('value') for n in nodes if n.get('role', {}).get('value') == r]
                self.assertEqual(role('button'), ['Create export'] * 3)
                self.assertEqual(role('heading').count('No exports yet'), 3)
                # The decorative icon is aria-hidden; before, Chromium exposed three unnamed images.
                self.assertEqual(role('image'), [])
                for theme in ('light', 'dark'):
                    page.evaluate('t => { document.documentElement.dataset.theme = t }', theme); page.wait_for_timeout(50)
                    for sel in ('h3', 'p'):
                        value = text_contrast(page.locator(f'.k-empty {sel}').first.screenshot())[0]
                        self.assertGreaterEqual(value, 4.5, f'{theme} {sel} {value}')
                page.set_viewport_size({'width': 360, 'height': 800})
                self.assertLessEqual(page.evaluate('document.documentElement.scrollWidth'), 360)
                self.assertEqual(errors, [])
            finally:
                browser.close()


if __name__ == '__main__':
    unittest.main()
