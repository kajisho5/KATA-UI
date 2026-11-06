"""Optional browser regression for ContextMenu; requires Playwright Python and Chromium."""
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
class ContextMenuBrowser(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close); self.addCleanup(self.server.shutdown)
        self.url = f'http://127.0.0.1:{self.server.server_port}/tests/context-menu-multi.html'

    def test_shared_outside_press_listener(self):
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 900, 'height': 1200})
                errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.on('console', lambda m: m.type == 'error' and errors.append(m.text))
                page.goto(self.url)  # several menus, context-menu.js loaded twice
                cdp = page.context.new_cdp_session(page)
                doc = cdp.send('Runtime.evaluate', {'expression': 'document'})['result']['objectId']
                types = [l['type'] for l in cdp.send('DOMDebugger.getEventListeners', {'objectId': doc})['listeners']]
                # Contract item 11: one document listener per script load, not one per menu.
                self.assertEqual(types.count('pointerdown'), 1)
                zones = page.locator('[data-ctx-zone]')
                expanded = "() => [...document.querySelectorAll('[data-ctx-zone]')].map(z => z.getAttribute('aria-expanded'))"
                count = zones.count()
                zones.nth(1).click(button='right')
                self.assertEqual(page.evaluate(expanded), ['false', 'true'] + ['false'] * (count - 2))
                # A press outside every zone and menu closes the open one.
                page.mouse.move(2, 2); page.mouse.down(); page.mouse.up(); page.wait_for_timeout(300)
                self.assertEqual(page.evaluate(expanded), ['false'] * count)
                # A press inside the open menu does not close it.
                zones.nth(0).click(button='right')
                menu = page.locator('[data-ctx]').nth(0)
                box = menu.bounding_box()
                page.mouse.move(box['x'] + 2, box['y'] + 2); page.mouse.down(); page.mouse.up()
                self.assertEqual(page.evaluate(expanded)[0], 'true')
                self.assertEqual(errors, [])
            finally:
                browser.close()


if __name__ == '__main__':
    unittest.main()
