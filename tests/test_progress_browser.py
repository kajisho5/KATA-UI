"""Optional browser regression for Progress; requires Playwright Python and Chromium."""
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
class ProgressBrowser(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close); self.addCleanup(self.server.shutdown)
        self.url = f'http://127.0.0.1:{self.server.server_port}/tests/progress-multi.html'

    def test_names_values_rtl_and_text(self):
        from playwright.sync_api import sync_playwright
        from tools.verify_button import text_contrast
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 600, 'height': 900}, device_scale_factor=2)
                page.goto(self.url)
                cdp = page.context.new_cdp_session(page); cdp.send('Accessibility.enable')
                bars = [n for n in cdp.send('Accessibility.getFullAXTree')['nodes'] if n.get('role', {}).get('value') == 'progressbar']
                self.assertEqual([b.get('name', {}).get('value') for b in bars], ['Uploading footage', 'Verifying files'] * 3)
                values = [int(b['value']['value']) for b in bars]
                self.assertEqual(values, [68, 92] * 3)
                # The fill starts at the inline start: left edge in LTR, right edge in RTL.
                for i, rtl in ((0, False), (4, True)):
                    track = page.locator('.k-progress').nth(i).bounding_box(); fill = page.locator('.k-progress-bar').nth(i).bounding_box()
                    if rtl: self.assertAlmostEqual(fill['x'] + fill['width'], track['x'] + track['width'], delta=1)
                    else: self.assertAlmostEqual(fill['x'], track['x'], delta=1)
                for theme in ('light', 'dark'):
                    page.evaluate('t => { document.documentElement.dataset.theme = t }', theme); page.wait_for_timeout(50)
                    value = text_contrast(page.locator('section').first.locator('span').nth(1).screenshot())[0]
                    self.assertGreaterEqual(value, 4.5, f'{theme} percentage {value}')
            finally:
                browser.close()


if __name__ == '__main__':
    unittest.main()
