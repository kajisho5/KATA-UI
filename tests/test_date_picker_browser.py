"""Optional browser regression for Date Picker outside dismissal; requires Playwright Python and Chromium.

Keyboard, RTL and motion behaviour are covered by tests/test_command_context_date.py.
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
class DatePickerBrowser(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close); self.addCleanup(self.server.shutdown)
        self.url = f'http://127.0.0.1:{self.server.server_port}/tests/date-picker-multi.html'
        self.script = (root / 'components/date-picker/date-picker.js').read_text()

    def test_one_shared_pointerdown_listener(self):
        """Contract item 11: outside dismissal uses pointerdown, registered once per script load, not per instance."""
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 900, 'height': 900}); errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.goto(self.url)
                # A second load finds no new instance and adds nothing.
                page.add_script_tag(content=self.script)
                cdp = page.context.new_cdp_session(page)
                doc = cdp.send('Runtime.evaluate', {'expression': 'document'})['result']['objectId']
                types = [l['type'] for l in cdp.send('DOMDebugger.getEventListeners', {'objectId': doc})['listeners']]
                self.assertEqual(page.locator('[data-dp]').count(), 3)
                self.assertEqual(types.count('pointerdown'), 1)
                inputs = page.locator('[data-dp-input]')
                for i in range(3):
                    inputs.nth(i).click()
                    self.assertEqual(inputs.nth(i).get_attribute('aria-expanded'), 'true')
                    page.mouse.move(2, 2); page.mouse.down()
                    self.assertEqual(inputs.nth(i).get_attribute('aria-expanded'), 'false')
                    page.mouse.up()
                self.assertEqual(errors, [])
            finally:
                browser.close()


if __name__ == '__main__':
    unittest.main()
