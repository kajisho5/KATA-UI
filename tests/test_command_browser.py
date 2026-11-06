"""Optional browser regression for Command; requires Playwright Python and Chromium."""
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
class CommandBrowser(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close); self.addCleanup(self.server.shutdown)
        self.url = f'http://127.0.0.1:{self.server.server_port}/tests/command-multi.html'

    def test_shared_shortcut_listener(self):
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 900, 'height': 900})
                errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.on('console', lambda m: m.type == 'error' and errors.append(m.text))
                page.goto(self.url)  # three palettes, command.js loaded twice
                cdp = page.context.new_cdp_session(page)
                doc = cdp.send('Runtime.evaluate', {'expression': 'document'})['result']['objectId']
                types = [l['type'] for l in cdp.send('DOMDebugger.getEventListeners', {'objectId': doc})['listeners']]
                # Contract item 11: one document listener per script load, not one per palette.
                self.assertEqual(types.count('keydown'), 1)
                is_open = "() => [...document.querySelectorAll('[data-command]')].map(d => d.open)"
                # Composing keystrokes are ignored.
                page.evaluate("() => document.dispatchEvent(new KeyboardEvent('keydown', { key: 'k', ctrlKey: true, isComposing: true, bubbles: true }))")
                self.assertEqual(page.evaluate(is_open), [False] * 3)
                # Nothing focused: the first palette opens; a second press keeps one palette open.
                page.keyboard.press('Control+k')
                self.assertEqual(page.evaluate(is_open), [True, False, False])
                page.keyboard.press('Control+k')
                self.assertEqual(page.evaluate(is_open), [True, False, False])
                page.keyboard.press('Escape'); page.wait_for_timeout(300)
                self.assertEqual(page.evaluate(is_open), [False] * 3)
                # Focused trigger: its own palette opens, and Escape returns focus to it.
                trigger = page.locator('[data-command-open]').nth(1)
                trigger.focus()
                page.keyboard.press('Control+k')
                self.assertEqual(page.evaluate(is_open), [False, True, False])
                page.keyboard.press('Escape'); page.wait_for_timeout(300)
                self.assertEqual(page.evaluate('() => document.activeElement === document.querySelectorAll("[data-command-open]")[1]'), True)
                self.assertEqual(errors, [])
            finally:
                browser.close()


if __name__ == '__main__':
    unittest.main()
