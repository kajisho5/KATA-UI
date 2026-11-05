"""Optional browser regression for Badge; requires Playwright Python and Chromium."""
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
class BadgeBrowser(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close); self.addCleanup(self.server.shutdown)
        self.url = f'http://127.0.0.1:{self.server.server_port}/tests/badge-multi.html'

    def test_tone_contrast_rtl_and_text_spacing(self):
        from playwright.sync_api import sync_playwright
        from tools.verify_button import text_contrast
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 700, 'height': 900}, device_scale_factor=2); errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
                page.goto(self.url)
                badges = page.locator('section[data-set] .badge')
                self.assertEqual(badges.count(), 18)
                # Every tone keeps text contrast at 4.5:1 or more in both themes.
                for theme in ('light', 'dark'):
                    page.evaluate('t => { document.documentElement.dataset.theme = t }', theme); page.wait_for_timeout(50)
                    for badge in page.locator('.badge').all():
                        value = text_contrast(badge.screenshot())[0]
                        self.assertGreaterEqual(value, 4.5, f'{theme} {badge.inner_text()} {value}')
                # RTL: the dot sits at the inline start (right of the label).
                rtl = page.locator('section[data-set]').nth(2).locator('.badge.asagi')
                dot, box = rtl.locator('i').bounding_box(), rtl.bounding_box()
                self.assertGreater(dot['x'] - box['x'], box['width'] / 2)
                # WCAG 1.4.12 text spacing: no badge clips its label.
                page.add_style_tag(content='*{line-height:1.5!important;letter-spacing:.12em!important;word-spacing:.16em!important}')
                self.assertEqual(page.evaluate('[...document.querySelectorAll(".badge")].filter(b => b.scrollHeight > b.clientHeight + 1 || b.scrollWidth > b.clientWidth + 1).length'), 0)
                self.assertEqual(errors, [])
            finally:
                browser.close()


if __name__ == '__main__':
    unittest.main()
