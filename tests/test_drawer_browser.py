"""Optional browser regression for Drawer placement and contrast; requires Playwright Python and Chromium.

Keyboard, focus, backdrop and IME behaviour are covered by tools/verify_overlay_instances.py.
"""
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
class DrawerBrowser(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close); self.addCleanup(self.server.shutdown)
        self.url = f'http://127.0.0.1:{self.server.server_port}/tests/drawer-multi.html'

    def open(self, browser, index, reduced='no-preference'):
        page = browser.new_page(viewport={'width': 1000, 'height': 700}, device_scale_factor=2, reduced_motion=reduced)
        page.goto(self.url)
        page.locator('[data-drawer-open]').nth(index).click(); page.mouse.move(2, 2)
        return page, page.locator('dialog[open]')

    def test_inline_end_placement_motion_and_contrast(self):
        from playwright.sync_api import sync_playwright
        from tools.verify_button import text_contrast
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                # LTR: the panel sits at the right edge; RTL (third instance): at the left edge.
                page, dialog = self.open(browser, 0)
                page.wait_for_timeout(400)
                box = dialog.bounding_box(); self.assertAlmostEqual(box['x'] + box['width'], 1000, delta=1)
                for theme in ('light', 'dark'):
                    page.evaluate('t => { document.documentElement.dataset.theme = t }', theme); page.wait_for_timeout(50)
                    for sel in ('.kdrawer-title', '[data-test-prose]'):
                        value = text_contrast(dialog.locator(sel).screenshot())[0]
                        self.assertGreaterEqual(value, 4.5, f'{theme} {sel} {value}')
                page.close()
                page, dialog = self.open(browser, 2)
                self.assertEqual(dialog.evaluate('d => getComputedStyle(d).animationName'), 'kdrawer-in-rtl')
                page.wait_for_timeout(400)
                box = dialog.bounding_box(); self.assertAlmostEqual(box['x'], 0, delta=1)
                page.close()
                # Reduced motion: no slide in either direction.
                for index in (0, 2):
                    page, dialog = self.open(browser, index, 'reduce')
                    self.assertEqual(dialog.evaluate('d => getComputedStyle(d).animationName'), 'none')
                    page.close()
            finally:
                browser.close()


if __name__ == '__main__':
    unittest.main()
