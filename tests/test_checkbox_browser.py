"""Optional browser regression for Checkbox / Radio (.check); requires Playwright Python and Chromium."""
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
class CheckboxBrowser(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close); self.addCleanup(self.server.shutdown)
        self.url = f'http://127.0.0.1:{self.server.server_port}/tests/checkbox-multi.html'

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
                self.assertEqual(page.locator('section').count(), 3)
                self.assertEqual(page.locator('section input').evaluate_all('(es)=>es.filter(e=>e.labels.length!==1).length'), 0)
                for i in range(3):
                    s = page.locator('section').nth(i)
                    box = s.locator('input[type=checkbox]').nth(1)          # "Include travel", unchecked
                    box.focus(); page.keyboard.press('Space')
                    self.assertTrue(box.is_checked(), 'Space toggles a checkbox')
                    self.assertNotEqual(box.evaluate('(e)=>getComputedStyle(e).boxShadow'), 'none')
                    s.locator('label', has_text='Include travel').click(position={'x': 60, 'y': 8})
                    self.assertFalse(box.is_checked(), 'clicking the label text toggles it back')
                    radios = s.locator('input[type=radio]:not([disabled])')
                    radios.nth(0).focus(); page.keyboard.press('ArrowDown')
                    self.assertTrue(radios.nth(1).is_checked(), 'arrow keys move the radio selection')
                    # Groups are per set (names differ), so set 1 did not change set 2.
                    if i == 1:
                        self.assertTrue(page.locator('section').nth(0).locator('input[type=radio]').nth(1).is_checked())
                    mixed = s.locator('input[data-mixed]')
                    self.assertTrue(mixed.evaluate('(e)=>e.indeterminate'))
                    self.assertEqual(mixed.evaluate('(e)=>getComputedStyle(e).backgroundColor'), s.locator('input[type=checkbox]').nth(0).evaluate('(e)=>getComputedStyle(e).backgroundColor'))
                    invalid = s.locator('input[aria-invalid="true"]')
                    self.assertNotEqual(invalid.evaluate('(e)=>getComputedStyle(e).borderTopColor'), box.evaluate('(e)=>getComputedStyle(e).borderTopColor'))
                    disabled = s.locator('input[type=checkbox][disabled]')
                    self.assertEqual(disabled.evaluate('(e)=>getComputedStyle(e).cursor'), 'not-allowed')
                    disabled.click(force=True); self.assertFalse(disabled.is_checked())
                self.assertEqual(page.locator('section').nth(2).evaluate('(e)=>getComputedStyle(e.querySelector(".check")).direction'), 'rtl')
                self.assertEqual(errors, [])
            finally:
                browser.close()

    def test_boundary_and_label_contrast(self):
        """Unchecked boundary reaches 3:1 (WCAG 1.4.11); label text 4.5:1. Pixels at 2x."""
        from playwright.sync_api import sync_playwright
        from tools.verify_button import text_contrast
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 1100, 'height': 1200}, device_scale_factor=2)
                page.goto(self.url)
                # No border-colour transition between themes: measure the settled colours.
                page.evaluate('document.documentElement.style.setProperty("--k-mscale","0")')
                for theme in ('light', 'dark'):
                    page.evaluate('(t)=>document.documentElement.dataset.theme=t', theme)
                    page.wait_for_timeout(50)
                    s = page.locator('section').first
                    for name, el in [('checkbox', s.locator('input[type=checkbox]').nth(1)), ('radio', s.locator('input[type=radio]').nth(1))]:
                        with self.subTest(theme=theme, part=name):
                            self.assertGreaterEqual(text_contrast(el.screenshot())[0], 3.0)
                    label = s.locator('label').first.bounding_box()
                    value = text_contrast(page.screenshot(clip={'x': label['x'] + 26, 'y': label['y'], 'width': 80, 'height': label['height']}))[0]
                    with self.subTest(theme=theme, part='label'):
                        self.assertGreaterEqual(value, 4.5)
            finally:
                browser.close()
