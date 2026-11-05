"""Optional browser regression for Breadcrumbs; requires Playwright Python and Chromium."""
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
class BreadcrumbsBrowser(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close); self.addCleanup(self.server.shutdown)
        self.url = f'http://127.0.0.1:{self.server.server_port}/tests/breadcrumbs-multi.html'

    def test_structure_rtl_targets_and_contrast(self):
        from playwright.sync_api import sync_playwright
        from tools.verify_button import text_contrast
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 700, 'height': 900}, device_scale_factor=2); errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
                page.goto(self.url)
                cdp = page.context.new_cdp_session(page); cdp.send('Accessibility.enable')
                nodes = cdp.send('Accessibility.getFullAXTree')['nodes']
                role = lambda r: [n.get('name', {}).get('value') for n in nodes if n.get('role', {}).get('value') == r and not n.get('ignored')]
                self.assertEqual(role('navigation'), ['Breadcrumb'] * 3)
                self.assertEqual(role('link'), ['Home', 'Projects', 'kata-ui'] * 3)
                self.assertEqual(page.locator('ol.k-crumbs > li').count(), 12)
                self.assertEqual(page.locator('[aria-current="page"]').count(), 3)
                # Separators mirror in RTL so they point toward the current page.
                for i, mirrored in ((0, False), (2, True)):
                    t = page.locator('section').nth(i).locator('.k-crumbs svg').first.evaluate('e => getComputedStyle(e).transform')
                    self.assertEqual(t.startswith('matrix(-1'), mirrored, f'{i} {t}')
                # Links meet the WCAG 2.5.8 minimum: 24px tall, or 24px apart with the spacing exception.
                boxes = [a.bounding_box() for a in page.locator('section').first.locator('.k-crumbs a').all()]
                for a, b in zip(boxes, boxes[1:]):
                    self.assertGreaterEqual(b['x'] - a['x'], 24)
                for theme in ('light', 'dark'):
                    page.evaluate('t => { document.documentElement.dataset.theme = t }', theme); page.wait_for_timeout(50)
                    crumbs = page.locator('section').first
                    for sel in ('.k-crumbs a', '[aria-current="page"]'):
                        value = text_contrast(crumbs.locator(sel).first.screenshot())[0]
                        self.assertGreaterEqual(value, 4.5, f'{theme} {sel} {value}')
                self.assertEqual(errors, [])
            finally:
                browser.close()


if __name__ == '__main__':
    unittest.main()
