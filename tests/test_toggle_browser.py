"""Optional browser regression for Toggle; requires Playwright Python and Chromium."""
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
class ToggleBrowser(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close); self.addCleanup(self.server.shutdown)
        self.url = f'http://127.0.0.1:{self.server.server_port}/tests/toggle-multi.html'

    def test_names_double_load_disabled_and_contrast(self):
        from playwright.sync_api import sync_playwright
        from tools.verify_button import text_contrast
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 600, 'height': 900}, device_scale_factor=2); errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.goto(self.url)
                page.evaluate('document.documentElement.style.setProperty("--k-mscale","0")')
                cdp = page.context.new_cdp_session(page); cdp.send('Accessibility.enable')
                buttons = [n.get('name', {}).get('value') for n in cdp.send('Accessibility.getFullAXTree')['nodes'] if n.get('role', {}).get('value') == 'button']
                self.assertEqual(sorted(buttons), sorted(['Pinned', 'Bold', 'Italic', 'Underline'] * 3))
                # The script is loaded twice; one click still flips the state once (two listeners would undo it).
                for t in page.locator('.k-tgl').all():
                    before = t.get_attribute('aria-pressed'); t.click()
                    self.assertNotEqual(t.get_attribute('aria-pressed'), before)
                    page.keyboard.press('Space')
                    self.assertEqual(t.get_attribute('aria-pressed'), before)
                # A disabled toggle does not change and is dimmed.
                first = page.locator('.k-tgl').first
                first.evaluate('b => b.disabled = true'); state = first.get_attribute('aria-pressed')
                first.click(force=True); self.assertEqual(first.get_attribute('aria-pressed'), state)
                self.assertLess(float(first.evaluate('b => getComputedStyle(b).opacity')), 1)
                first.evaluate('b => b.disabled = false')
                page.mouse.move(1, 1); page.locator('h1').click()
                for theme in ('light', 'dark'):
                    page.evaluate('t => { document.documentElement.dataset.theme = t }', theme); page.wait_for_timeout(50)
                    for k in (1, 2):  # pressed Bold, unpressed Italic
                        value = text_contrast(page.locator('.k-tgl').nth(k).screenshot())[0]
                        self.assertGreaterEqual(value, 4.5, f'{theme} {k} {value}')
                self.assertEqual(errors, [])
            finally:
                browser.close()


if __name__ == '__main__':
    unittest.main()
