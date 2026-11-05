"""Optional browser regression for Field; requires Playwright Python and Chromium."""
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
class FieldBrowser(unittest.TestCase):
    def test_three_sets_ids_descriptions_and_errors(self):
        from playwright.sync_api import sync_playwright
        root = Path(__file__).resolve().parents[1]
        server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.server_close); self.addCleanup(server.shutdown)
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 1100, 'height': 1200}); errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
                page.goto(f'http://127.0.0.1:{server.server_port}/tests/field-multi.html')
                # The script ran once per field even though it is loaded twice; IDs are unique.
                self.assertEqual(page.locator('.k-field[data-kata-ready]').count(), 7)
                ids = page.evaluate('[...document.querySelectorAll("[id]")].map(e=>e.id)')
                self.assertEqual(len(ids), len(set(ids)))
                for i in range(3):
                    s = page.locator('section').nth(i)
                    name, mail = s.locator('input').nth(0), s.locator('input').nth(1)
                    self.assertEqual(name.evaluate('(e)=>e.labels[0].firstChild.textContent.trim()'), 'Workspace name')
                    self.assertEqual(name.evaluate('(e)=>document.getElementById(e.getAttribute("aria-describedby")).textContent.trim()'), 'Shown in menus and the sidebar. You can change it later.')
                    self.assertIsNone(name.get_attribute('aria-invalid'))
                    self.assertEqual(mail.get_attribute('aria-invalid'), 'true')
                    self.assertEqual(mail.evaluate('(e)=>document.getElementById(e.getAttribute("aria-describedby")).textContent.trim()'), 'That address is missing its domain.')
                    # The error present at load is not an alert; one added later (submit) is, once.
                    err = s.locator('.err')
                    self.assertIsNone(err.get_attribute('role'))
                    field = s.locator('.k-field').nth(1)
                    field.evaluate('(e)=>e.removeAttribute("data-invalid")'); page.wait_for_timeout(20)
                    self.assertIsNone(mail.get_attribute('aria-invalid'))
                    self.assertNotIn(err.get_attribute('id'), mail.get_attribute('aria-describedby') or '')
                    field.evaluate('(e)=>e.setAttribute("data-invalid","")'); page.wait_for_timeout(20)
                    self.assertEqual(err.get_attribute('role'), 'alert')
                    self.assertEqual(mail.get_attribute('aria-invalid'), 'true')
                    self.assertIn(err.get_attribute('id'), mail.get_attribute('aria-describedby'))
                    # Typing does not change the error state.
                    mail.fill('accounts@acme.example'); self.assertEqual(err.get_attribute('role'), 'alert')
                    # The control fits its field and sits under the label text in both directions.
                    fb, ib, lb = field.bounding_box(), mail.bounding_box(), s.locator('.k-field').nth(1).locator('.lab').bounding_box()
                    self.assertLessEqual(ib['x'] + ib['width'], fb['x'] + fb['width'] + 0.5)
                    self.assertGreaterEqual(ib['x'], fb['x'] - 0.5)
                    self.assertGreater(ib['y'], lb['y'] + 10)
                self.assertEqual(page.locator('section').nth(2).evaluate('(e)=>getComputedStyle(e.querySelector(".lab")).direction'), 'rtl')
                # Existing IDs are kept and the author's own description stays first.
                own = page.locator('#own-name')
                self.assertEqual(own.get_attribute('aria-describedby'), 'own-extra own-hint')
                self.assertEqual(page.locator('label[for="own-name"]').count(), 1)
                page.set_viewport_size({'width': 375, 'height': 812})
                self.assertTrue(page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
                self.assertEqual(errors, [])
            finally:
                browser.close()

    def test_text_contrast(self):
        """Label, badges, hint and error text reach 4.5:1 in light and dark (pixels; see tools/verify_button)."""
        from playwright.sync_api import sync_playwright
        from tools.verify_button import text_contrast
        root = Path(__file__).resolve().parents[1]
        server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.server_close); self.addCleanup(server.shutdown)
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 1100, 'height': 1200}, device_scale_factor=2)
                page.goto(f'http://127.0.0.1:{server.server_port}/tests/field-multi.html')
                for theme in ('light', 'dark'):
                    page.evaluate('(t)=>document.documentElement.dataset.theme=t', theme)
                    s = page.locator('section').first
                    for name, el in [('optional', s.locator('.opt')), ('required', s.locator('.req')), ('hint', s.locator('.hint')), ('error', s.locator('.err'))]:
                        value = text_contrast(el.screenshot())[0]
                        with self.subTest(theme=theme, text=name):
                            self.assertGreaterEqual(value, 4.5)
                    box = s.locator('.lab').first.bounding_box()
                    value = text_contrast(page.screenshot(clip={'x': box['x'], 'y': box['y'], 'width': 110, 'height': 18}))[0]
                    with self.subTest(theme=theme, text='label'):
                        self.assertGreaterEqual(value, 4.5)
            finally:
                browser.close()
