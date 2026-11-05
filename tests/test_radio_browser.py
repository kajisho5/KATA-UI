"""Optional browser regression for Radio (.k-radio); requires Playwright Python and Chromium."""
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
class RadioBrowser(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close); self.addCleanup(self.server.shutdown)
        self.url = f'http://127.0.0.1:{self.server.server_port}/tests/radio-multi.html'

    def test_three_sets_keyboard_states(self):
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 1100, 'height': 1200}); errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
                page.goto(self.url)
                page.evaluate('document.documentElement.style.setProperty("--k-mscale","0")')
                self.assertEqual(page.locator('section input').evaluate_all('(es)=>es.filter(e=>e.labels.length!==1).length'), 0)
                self.assertEqual(page.locator('fieldset').evaluate_all('(fs)=>fs.filter(f=>!f.querySelector("legend")).length'), 0)
                for i in range(3):
                    s = page.locator('section').nth(i)
                    cycle = s.locator('input[name^="cycle"]')
                    cycle.nth(0).focus(); page.keyboard.press('ArrowDown')
                    self.assertTrue(cycle.nth(1).is_checked(), 'arrow keys move the selection')
                    self.assertNotEqual(cycle.nth(1).evaluate('(e)=>getComputedStyle(e).boxShadow'), 'none')
                    page.keyboard.press('ArrowDown')
                    self.assertTrue(cycle.nth(0).is_checked(), 'the disabled option is skipped')
                    disabled = s.locator('input[disabled]')
                    self.assertEqual(disabled.evaluate('(e)=>getComputedStyle(e).cursor'), 'not-allowed')
                    disabled.click(force=True); self.assertFalse(disabled.is_checked())
                    invalid = s.locator('input[aria-invalid="true"]').first
                    self.assertNotEqual(invalid.evaluate('(e)=>getComputedStyle(e).borderTopColor'), cycle.nth(1).evaluate('(e)=>getComputedStyle(e).borderTopColor'))
                    s.locator('label', has_text='Express').click()
                    self.assertTrue(s.locator('input[name^="ship"]').nth(1).is_checked())
                    if i == 1:
                        self.assertTrue(page.locator('section').nth(0).locator('input[name^="cycle"]').nth(0).is_checked(), 'set 2 does not change set 1')
                self.assertEqual(page.locator('section').nth(2).evaluate('(e)=>getComputedStyle(e.querySelector(".k-radio")).direction'), 'rtl')
                self.assertEqual(errors, [])
            finally:
                browser.close()

    def test_boundary_and_label_contrast(self):
        from playwright.sync_api import sync_playwright
        from tools.verify_button import text_contrast
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 1100, 'height': 1200}, device_scale_factor=2)
                page.goto(self.url)
                page.evaluate('document.documentElement.style.setProperty("--k-mscale","0")')
                for theme in ('light', 'dark'):
                    page.evaluate('(t)=>document.documentElement.dataset.theme=t', theme); page.wait_for_timeout(50)
                    s = page.locator('section').first
                    with self.subTest(theme=theme, part='unchecked boundary'):
                        self.assertGreaterEqual(text_contrast(s.locator('input[name^="cycle"]').nth(1).screenshot())[0], 3.0)
                    label = s.locator('.k-radio').first.bounding_box()
                    with self.subTest(theme=theme, part='label'):
                        self.assertGreaterEqual(text_contrast(page.screenshot(clip={'x': label['x'] + 26, 'y': label['y'], 'width': 60, 'height': label['height']}))[0], 4.5)
            finally:
                browser.close()
