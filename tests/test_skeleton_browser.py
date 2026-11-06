"""Optional browser regression for Skeleton; requires Playwright Python and Chromium."""
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
class SkeletonBrowser(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close); self.addCleanup(self.server.shutdown)
        self.url = f'http://127.0.0.1:{self.server.server_port}/tests/skeleton-multi.html'

    def test_status_hidden_shapes_rtl_and_motion(self):
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 600, 'height': 900})
                errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.on('console', lambda m: m.type == 'error' and errors.append(m.text))
                page.goto(self.url)
                cdp = page.context.new_cdp_session(page); cdp.send('Accessibility.enable')
                nodes = cdp.send('Accessibility.getFullAXTree')['nodes']
                self.assertEqual(sum(n.get('role', {}).get('value') == 'status' for n in nodes), 3)
                texts = [n.get('name', {}).get('value') for n in nodes if n.get('role', {}).get('value') == 'StaticText']
                self.assertEqual(texts.count('Loading profile'), 3)
                # Placeholder shapes sit inside aria-hidden; the label is clipped to 1px.
                self.assertTrue(page.evaluate("() => [...document.querySelectorAll('.k-sk')].every(e => e.closest('[aria-hidden=true]'))"))
                box = page.locator('.k-sk-status').first.bounding_box()
                self.assertLessEqual(box['width'] * box['height'], 1)
                directions = page.evaluate("() => [...document.querySelectorAll('section')].map(s => getComputedStyle(s.querySelector('.k-sk')).animationDirection)")
                self.assertEqual(directions, ['normal', 'normal', 'reverse'])
                page.emulate_media(reduced_motion='reduce')
                names = page.evaluate("() => [...document.querySelectorAll('.k-sk')].map(e => getComputedStyle(e).animationName)")
                self.assertEqual(set(names), {'none'})
                self.assertEqual(errors, [])
            finally:
                browser.close()


if __name__ == '__main__':
    unittest.main()
