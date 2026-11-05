"""Optional browser regression for Alert Dialog layout and contrast; requires Playwright Python and Chromium.

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
class AlertDialogBrowser(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close); self.addCleanup(self.server.shutdown)
        self.url = f'http://127.0.0.1:{self.server.server_port}/tests/alert-dialog-multi.html'

    def test_role_name_narrow_layout_and_contrast(self):
        from playwright.sync_api import sync_playwright
        from tools.verify_button import text_contrast
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 320, 'height': 700}, device_scale_factor=2); errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
                page.goto(self.url)
                page.evaluate('document.documentElement.style.setProperty("--k-mscale","0")')
                page.locator('[data-alert-open]').first.click()
                dialog = page.locator('dialog[open]')
                self.assertEqual(dialog.get_attribute('role'), 'alertdialog')
                cdp = page.context.new_cdp_session(page); cdp.send('Accessibility.enable')
                names = [n.get('name', {}).get('value') for n in cdp.send('Accessibility.getFullAXTree')['nodes'] if n.get('role', {}).get('value') == 'alertdialog']
                self.assertEqual(names, ['Delete project'])
                # At 320px both buttons stay inside the dialog's padding (they wrap instead of spilling).
                inner = dialog.locator('.kalert-in').evaluate('e => { const r = e.getBoundingClientRect(), s = getComputedStyle(e); return [r.left + parseFloat(s.paddingLeft), r.right - parseFloat(s.paddingRight)] }')
                for button in dialog.locator('button').all():
                    box = button.bounding_box()
                    self.assertGreaterEqual(box['x'], inner[0] - 0.5); self.assertLessEqual(box['x'] + box['width'], inner[1] + 0.5)
                for theme in ('light', 'dark'):
                    page.evaluate('t => { document.documentElement.dataset.theme = t }', theme); page.wait_for_timeout(50)
                    for sel in ('h3', 'p'):
                        value = text_contrast(dialog.locator(sel).screenshot())[0]
                        self.assertGreaterEqual(value, 4.5, f'{theme} {sel} {value}')
                self.assertEqual(errors, [])
            finally:
                browser.close()


if __name__ == '__main__':
    unittest.main()
