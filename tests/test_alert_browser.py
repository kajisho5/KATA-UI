"""Optional browser regression for Alert; requires Playwright Python and Chromium."""
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
TONES = [None, 'success', 'warning', 'danger']


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


@unittest.skipUnless(AVAILABLE, 'Requires Playwright Python and Chromium')
class AlertBrowser(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close); self.addCleanup(self.server.shutdown)
        self.url = f'http://127.0.0.1:{self.server.server_port}/tests/alert-multi.html'

    def test_icons_hidden_tones_rtl_and_contrast(self):
        from playwright.sync_api import sync_playwright
        from tools.verify_button import text_contrast
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 700, 'height': 1400}, device_scale_factor=2); errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
                page.goto(self.url)
                alerts = page.locator('.k-alert')
                self.assertEqual([a.get_attribute('data-tone') for a in alerts.all()], TONES * 3)
                # Decorative icons are not announced as unnamed images (the title states the tone).
                cdp = page.context.new_cdp_session(page); cdp.send('Accessibility.enable')
                images = [n for n in cdp.send('Accessibility.getFullAXTree')['nodes'] if n.get('role', {}).get('value') == 'image' and not n.get('ignored')]
                self.assertEqual(images, [])
                # RTL: the icon sits at the inline start (right edge).
                rtl = alerts.nth(8); icon, box = rtl.locator('svg').bounding_box(), rtl.bounding_box()
                self.assertGreater(icon['x'] - box['x'], box['width'] / 2)
                # Title and body text keep 4.5:1; the decorative icon keeps 3:1 in every tone and theme.
                for theme in ('light', 'dark'):
                    page.evaluate('t => { document.documentElement.dataset.theme = t }', theme); page.wait_for_timeout(50)
                    for k, tone in enumerate(TONES):
                        alert = alerts.nth(k)
                        for part, minimum in (('b', 4.5), ('p', 4.5), ('svg', 3.0)):
                            value = text_contrast(alert.locator(part).screenshot())[0]
                            self.assertGreaterEqual(value, minimum, f'{theme} {tone} {part} {value}')
                self.assertEqual(errors, [])
            finally:
                browser.close()


if __name__ == '__main__':
    unittest.main()
