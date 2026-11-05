"""Optional browser regression for Accordion; requires Playwright Python and Chromium."""
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
NAMES = ['Is there a build step?', 'Does it work in dark mode?', 'Can I change the radius?']


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


@unittest.skipUnless(AVAILABLE, 'Requires Playwright Python and Chromium')
class AccordionBrowser(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close); self.addCleanup(self.server.shutdown)
        self.url = f'http://127.0.0.1:{self.server.server_port}/tests/accordion-multi.html'

    def test_names_state_keyboard_rtl_and_contrast(self):
        from playwright.sync_api import sync_playwright
        from tools.verify_button import text_contrast
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 600, 'height': 1600}, device_scale_factor=2); errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
                page.goto(self.url)
                page.evaluate('document.documentElement.style.setProperty("--k-mscale","0")')
                # Each summary is exposed with its question as the name and its open state.
                cdp = page.context.new_cdp_session(page); cdp.send('Accessibility.enable')
                nodes = [n for n in cdp.send('Accessibility.getFullAXTree')['nodes'] if n.get('role', {}).get('value') == 'DisclosureTriangle']
                self.assertEqual([n.get('name', {}).get('value') for n in nodes], NAMES * 3)
                expanded = [next((pr['value']['value'] for pr in n.get('properties', []) if pr['name'] == 'expanded'), None) for n in nodes]
                self.assertEqual(expanded, [True, False, False] * 3)
                details = page.locator('details.k-acc')
                summaries = page.locator('details.k-acc > summary')
                # Enter and Space toggle; sets are independent.
                summaries.nth(1).focus(); page.keyboard.press('Enter')
                self.assertTrue(details.nth(1).evaluate('d => d.open'))
                self.assertFalse(details.nth(4).evaluate('d => d.open'))
                page.keyboard.press('Space'); self.assertFalse(details.nth(1).evaluate('d => d.open'))
                # The focus ring is visible (box-shadow) and the chevron flips when open.
                self.assertNotEqual(summaries.nth(1).evaluate('s => getComputedStyle(s).boxShadow'), 'none')
                self.assertIn('matrix(-1', details.nth(0).locator('svg').evaluate('s => getComputedStyle(s).transform'))
                # Collapsed content stays in the document text, which is what find-in-page searches.
                self.assertIn('Every color comes from a token', details.nth(1).evaluate('d => d.textContent'))
                # RTL: the chevron sits at the inline end (left edge in RTL).
                ltr = summaries.nth(0).locator('svg').bounding_box(); rtl = summaries.nth(6).locator('svg').bounding_box()
                s_ltr = summaries.nth(0).bounding_box(); s_rtl = summaries.nth(6).bounding_box()
                self.assertGreater(ltr['x'] - s_ltr['x'], s_ltr['width'] / 2)
                self.assertLess(rtl['x'] - s_rtl['x'], s_rtl['width'] / 2)
                page.mouse.move(1, 1); summaries.nth(1).evaluate('s => s.blur()')
                for theme in ('light', 'dark'):
                    page.evaluate('t => { document.documentElement.dataset.theme = t }', theme); page.wait_for_timeout(50)
                    q = text_contrast(summaries.nth(0).screenshot())[0]
                    a = text_contrast(details.nth(0).locator('.k-acc-body').screenshot())[0]
                    self.assertGreaterEqual(q, 4.5, f'{theme} question {q}'); self.assertGreaterEqual(a, 4.5, f'{theme} answer {a}')
                self.assertEqual(errors, [])
            finally:
                browser.close()


if __name__ == '__main__':
    unittest.main()
