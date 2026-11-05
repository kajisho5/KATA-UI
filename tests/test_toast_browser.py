"""Optional browser regression for Toast; requires Playwright Python and Chromium."""
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
class ToastBrowser(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close); self.addCleanup(self.server.shutdown)
        self.url = f'http://127.0.0.1:{self.server.server_port}/tests/toast-multi.html'

    def test_live_region_stack_contrast_and_dismissal(self):
        from playwright.sync_api import sync_playwright
        from tools.verify_button import text_contrast
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 900, 'height': 900}, device_scale_factor=2); errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
                page.clock.install()
                page.goto(self.url)
                page.evaluate('document.documentElement.style.setProperty("--k-mscale","0")')
                stacks = page.locator('[data-toasts]'); buttons = page.locator('[data-toast-demo]')
                # Every stack is a polite status region before any toast exists (4.1.3 status messages).
                for i in range(3):
                    self.assertEqual(stacks.nth(i).get_attribute('role'), 'status')
                    self.assertEqual(stacks.nth(i).get_attribute('aria-live'), 'polite')
                    self.assertEqual(stacks.nth(i).locator('.toast').count(), 0)
                # Loading the script twice binds each button once: one click, one toast, in that instance's stack.
                for i in range(3):
                    buttons.nth(i).click()
                    self.assertEqual(stacks.nth(i).locator('.toast').count(), 1, f'instance {i}')
                    self.assertTrue(buttons.nth(i).evaluate('e => document.activeElement === e'))  # focus is not stolen
                toast = stacks.first.locator('.toast').first
                self.assertEqual(toast.locator('b').inner_text(), 'Saved')
                self.assertEqual(toast.locator('svg').get_attribute('aria-hidden'), 'true')
                self.assertEqual(toast.locator('[style]').count(), 0)
                for theme in ('light', 'dark'):
                    page.evaluate('t => { document.documentElement.dataset.theme = t }', theme); page.wait_for_timeout(50)
                    for part in ('b', 'small'):
                        value = text_contrast(toast.locator(part).screenshot())[0]
                        self.assertGreaterEqual(value, 4.5, f'{theme} {part} {value}')
                # Toasts leave after 4 s; at zero motion they are removed at once.
                page.clock.run_for(4100)
                self.assertEqual(page.locator('.toast').count(), 0)
                self.assertEqual(errors, [])
            finally:
                browser.close()


if __name__ == '__main__':
    unittest.main()
