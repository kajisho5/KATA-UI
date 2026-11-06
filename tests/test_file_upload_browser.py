"""Optional browser regression for FileUpload; requires Playwright Python and Chromium."""
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
class FileUploadBrowser(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close); self.addCleanup(self.server.shutdown)
        self.url = f'http://127.0.0.1:{self.server.server_port}/tests/file-upload-multi.html'

    def test_hint_contrast_states_and_rtl_spacing(self):
        from playwright.sync_api import sync_playwright
        from tools.verify_button import text_contrast
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 900, 'height': 1200}, device_scale_factor=2, reduced_motion='reduce')
                errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.on('console', lambda m: m.type == 'error' and errors.append(m.text))
                page.goto(self.url)
                zone = page.locator('.k-up-zone').first
                hint = zone.locator(':scope > span:not(.ic)')
                for theme in ('light', 'dark'):
                    page.evaluate('t => { document.documentElement.dataset.theme = t }', theme)
                    page.mouse.move(1, 1); page.wait_for_timeout(300)
                    rest = text_contrast(hint.screenshot())[0]
                    zone.hover(); page.wait_for_timeout(300)
                    hover = text_contrast(hint.screenshot())[0]
                    page.mouse.move(1, 1)
                    zone.evaluate("z => z.classList.add('drag')"); page.wait_for_timeout(300)
                    drag = text_contrast(hint.screenshot())[0]
                    zone.evaluate("z => z.classList.remove('drag')")
                    for label, value in (('rest', rest), ('hover', hover), ('drag', drag)):
                        self.assertGreaterEqual(value, 4.5, f'{theme} {label} hint {value}')
                # Remove button: hover and active differ from rest.
                rm = page.locator('.k-up-item .rm').first
                bg = lambda: rm.evaluate('b => getComputedStyle(b).backgroundColor')
                rest_bg = bg(); rm.hover(); hover_bg = bg()
                page.mouse.down(); active_bg = bg(); page.mouse.up()
                self.assertNotEqual(rest_bg, hover_bg); self.assertNotEqual(hover_bg, active_bg)
                # Disabled input: the zone dims, shows not-allowed and drops the hover tint.
                zone.evaluate("z => { z.querySelector('input').disabled = true }")
                page.mouse.move(1, 1); before = zone.evaluate('z => getComputedStyle(z).backgroundColor')
                zone.hover(); page.wait_for_timeout(100)
                style = zone.evaluate('z => { const s = getComputedStyle(z); return [s.opacity, s.cursor, s.backgroundColor] }')
                self.assertEqual(style[:2], ['0.45', 'not-allowed']); self.assertEqual(style[2], before)
                # The list gap sits on the block start in LTR and RTL alike.
                margins = page.evaluate("() => [...document.querySelectorAll('.k-up-list')].map(l => getComputedStyle(l).marginTop)")
                self.assertEqual(len(set(margins)), 1)
                self.assertEqual(errors, [])
            finally:
                browser.close()


if __name__ == '__main__':
    unittest.main()
