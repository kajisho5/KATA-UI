"""Optional browser regression for Textarea; requires Playwright Python and Chromium."""
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
class TextareaBrowser(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close); self.addCleanup(self.server.shutdown)
        self.url = f'http://127.0.0.1:{self.server.server_port}/tests/textarea-multi.html'

    def test_three_sets_labels_states_and_size(self):
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 1100, 'height': 1400}); errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
                page.goto(self.url)
                self.assertEqual(page.locator('section').count(), 3)
                self.assertEqual(page.locator('section [id], section [for]').count(), 0)
                names = page.locator('section textarea').evaluate_all('(es)=>es.map(e=>e.labels.length===1?e.labels[0].firstChild.textContent.trim():"")')
                self.assertEqual(names, ['Release notes', 'Reason for the refund', 'Archived note', 'Webhook payload'] * 3)
                for i in range(3):
                    s = page.locator('section').nth(i)
                    notes, invalid = s.locator('textarea').nth(0), s.locator('textarea[aria-invalid="true"]')
                    disabled, readonly = s.locator('textarea[disabled]'), s.locator('textarea[readonly]')
                    s.locator('label').first.click(position={'x': 4, 'y': 6})
                    self.assertTrue(notes.evaluate('(e)=>e===document.activeElement'))
                    page.keyboard.press('Control+End'); page.keyboard.type(' 日本語も入る。')
                    self.assertTrue(notes.input_value().endswith(' 日本語も入る。'))
                    self.assertNotEqual(notes.evaluate('(e)=>getComputedStyle(e).boxShadow'), 'none')
                    self.assertNotEqual(invalid.evaluate('(e)=>getComputedStyle(e).borderTopColor'), notes.evaluate('(e)=>{e.blur();return getComputedStyle(e).borderTopColor}'))
                    self.assertEqual(disabled.evaluate('(e)=>getComputedStyle(e).cursor'), 'not-allowed')
                    invalid.focus(); page.keyboard.press('Tab')
                    self.assertTrue(readonly.evaluate('(e)=>e===document.activeElement'), 'Tab skips the disabled field')
                    self.assertNotEqual(readonly.evaluate('(e)=>getComputedStyle(e).boxShadow'), 'none')
                    # The field fits its label and is the declared 92px tall at rest.
                    box, lab = notes.bounding_box(), notes.locator('xpath=..').bounding_box()
                    self.assertLessEqual(box['x'] + box['width'], lab['x'] + lab['width'] + 0.5)
                    self.assertEqual(round(invalid.bounding_box()['height']), 92)
                self.assertEqual(page.locator('section').nth(2).locator('textarea').first.evaluate('(e)=>getComputedStyle(e).direction'), 'rtl')
                page.set_viewport_size({'width': 375, 'height': 812})
                self.assertGreaterEqual(page.locator('section textarea').first.evaluate('(e)=>parseFloat(getComputedStyle(e).fontSize)'), 16)
                self.assertTrue(page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
                self.assertEqual(errors, [])
            finally:
                browser.close()

    def test_text_contrast(self):
        from playwright.sync_api import sync_playwright
        from tools.verify_button import text_contrast
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 1100, 'height': 1400}, device_scale_factor=2)
                page.goto(self.url)
                for theme in ('light', 'dark'):
                    page.evaluate('(t)=>document.documentElement.dataset.theme=t', theme)
                    s = page.locator('section').first
                    for name, el in [('value', s.locator('textarea').nth(0)), ('read-only', s.locator('textarea[readonly]'))]:
                        with self.subTest(theme=theme, text=name):
                            self.assertGreaterEqual(text_contrast(el.screenshot())[0], 4.5)
                    el = s.locator('textarea').nth(0)
                    el.evaluate('(e)=>{e.value=""}')
                    with self.subTest(theme=theme, text='placeholder'):
                        self.assertGreaterEqual(text_contrast(el.screenshot())[0], 4.5)
            finally:
                browser.close()
