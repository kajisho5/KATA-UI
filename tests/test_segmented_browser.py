"""Optional browser regression for Segmented; requires Playwright Python and Chromium."""
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
class SegmentedBrowser(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close); self.addCleanup(self.server.shutdown)
        self.url = f'http://127.0.0.1:{self.server.server_port}/tests/segmented-multi.html'

    def test_names_keyboard_rtl_focus_and_contrast(self):
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
                nodes = cdp.send('Accessibility.getFullAXTree')['nodes']
                role = lambda r: [n.get('name', {}).get('value') for n in nodes if n.get('role', {}).get('value') == r and not n.get('ignored')]
                self.assertEqual(role('radiogroup'), ['Range', 'Density'] * 3)
                self.assertEqual(role('radio'), ['Day', 'Week', 'Month', 'Comfort', 'Compact'] * 3)
                checked = lambda sec: [r.is_checked() for r in page.locator('section').nth(sec).locator('.k-seg').first.locator('input').all()]
                # Arrow keys move the selection (native radios); in RTL the visual arrows follow the platform.
                page.locator('section').first.locator('input:checked').first.focus()
                page.keyboard.press('ArrowRight'); self.assertEqual(checked(0), [False, True, False])
                self.assertEqual(checked(1), [True, False, False])  # other sets untouched
                # The focused segment shows the ring.
                ring = page.locator('section').first.locator('input:checked + span').first.evaluate('s => getComputedStyle(s).boxShadow')
                self.assertNotEqual(ring, 'none')
                # Clicking a label selects it.
                page.locator('section').nth(2).locator('.k-seg-item', has_text='Month').click()
                self.assertEqual(checked(2), [False, False, True])
                page.locator('h1').click()
                seg = page.locator('section').nth(1).locator('.k-seg').first
                for theme in ('light', 'dark'):
                    page.evaluate('t => { document.documentElement.dataset.theme = t }', theme); page.wait_for_timeout(50)
                    for text in ('Day', 'Week'):
                        value = text_contrast(seg.locator('span', has_text=text).screenshot())[0]
                        self.assertGreaterEqual(value, 4.5, f'{theme} {text} {value}')
                self.assertEqual(errors, [])
            finally:
                browser.close()


if __name__ == '__main__':
    unittest.main()
