"""Optional browser regression for Input; requires Playwright Python and Chromium."""
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
class InputBrowser(unittest.TestCase):
    def test_three_sets_labels_states_and_rtl(self):
        from playwright.sync_api import sync_playwright
        root = Path(__file__).resolve().parents[1]
        server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.server_close); self.addCleanup(server.shutdown)
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 1100, 'height': 1400}); errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
                page.goto(f'http://127.0.0.1:{server.server_port}/tests/input-multi.html')
                sections = page.locator('section')
                self.assertEqual(sections.count(), 3)
                self.assertEqual(sections.nth(2).evaluate('(e)=>getComputedStyle(e).direction'), 'rtl')
                # Samples carry no id/for, and every input is named by the label that wraps it.
                self.assertEqual(page.locator('section [id], section [for]').count(), 0)
                names = page.locator('section input').evaluate_all('(es)=>es.map(e=>e.labels.length===1?e.labels[0].firstChild.textContent.trim():"")')
                self.assertEqual(len(names), 15); self.assertNotIn('', names)
                self.assertEqual(names[:5], ['Email', 'Full name', 'Search', 'Billing email', 'Account ID'])
                for i in range(3):
                    s = sections.nth(i)
                    email = s.locator('input[placeholder="you@example.com"]')
                    # Clicking the label text focuses its own input, not another set's.
                    s.get_by_text('Email', exact=True).click()
                    self.assertTrue(email.evaluate('(e)=>e===document.activeElement'))
                    page.keyboard.type('a@b.example')
                    self.assertEqual(email.input_value(), 'a@b.example')
                    self.assertNotEqual(email.evaluate('(e)=>getComputedStyle(e).boxShadow'), 'none')
                    invalid = s.locator('input[aria-invalid="true"]')
                    danger = invalid.evaluate('(e)=>getComputedStyle(e).borderTopColor')
                    self.assertNotEqual(danger, email.evaluate('(e)=>{e.blur();return getComputedStyle(e).borderTopColor}'))
                    disabled = s.locator('input[disabled]'); readonly = s.locator('input[readonly]')
                    self.assertEqual(disabled.evaluate('(e)=>getComputedStyle(e).cursor'), 'not-allowed')
                    self.assertNotEqual(disabled.evaluate('(e)=>getComputedStyle(e).color'), email.evaluate('(e)=>getComputedStyle(e).color'))
                    # Tab skips the disabled input and reaches the read-only one.
                    s.locator('input[placeholder^="Search"]').focus(); page.keyboard.press('Tab')
                    self.assertTrue(readonly.evaluate('(e)=>e===document.activeElement'))
                    self.assertNotEqual(readonly.evaluate('(e)=>getComputedStyle(e).boxShadow'), 'none')
                    # The search icon sits at the inline start: left in LTR, right in RTL.
                    icon = s.locator('.searchwrap svg').bounding_box(); field = s.locator('.searchwrap .input').bounding_box()
                    centre = field['x'] + field['width'] / 2
                    self.assertTrue(icon['x'] > centre if i == 2 else icon['x'] < centre)
                page.set_viewport_size({'width': 375, 'height': 812})
                self.assertGreaterEqual(float(page.locator('section input').first.evaluate('(e)=>parseFloat(getComputedStyle(e).fontSize)')), 16)
                self.assertTrue(page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
                self.assertEqual(errors, [])
            finally:
                browser.close()

    def test_text_contrast(self):
        from tools.verify_input import run, problems
        result = run()
        self.assertEqual(len(result['rows']), 6)
        self.assertEqual(problems(result), [])
