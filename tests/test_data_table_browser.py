"""Optional browser regression for DataTable; requires Playwright Python and Chromium."""
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
class DataTableBrowser(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close); self.addCleanup(self.server.shutdown)
        self.url = f'http://127.0.0.1:{self.server.server_port}/tests/data-table-multi.html'

    def test_scroll_region_sort_select_and_text(self):
        from playwright.sync_api import sync_playwright
        from tools.verify_button import text_contrast
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 900, 'height': 1400}, device_scale_factor=2)
                errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.on('console', lambda m: m.type == 'error' and errors.append(m.text))
                page.goto(self.url)  # data-table.js loaded twice
                cdp = page.context.new_cdp_session(page); cdp.send('Accessibility.enable')
                nodes = [n for n in cdp.send('Accessibility.getFullAXTree')['nodes'] if not n.get('ignored')]
                self.assertEqual([n.get('name', {}).get('value') for n in nodes if n.get('role', {}).get('value') == 'region'], ['Members 1', 'Members 2', 'Members 3'])
                # Sorting one table once flips its header once (script loaded twice) and leaves the others alone.
                page.locator('.k-dt-sort').first.click()
                self.assertEqual(page.evaluate("() => [...document.querySelectorAll('.k-dt-sort')].filter((b, i) => i % 2 === 0).map(b => b.closest('th').getAttribute('aria-sort'))"), ['ascending', 'none', 'none'])
                for theme in ('light', 'dark'):
                    page.evaluate('t => { document.documentElement.dataset.theme = t }', theme); page.wait_for_timeout(400)
                    value = text_contrast(page.locator('.k-dt-t th .k-dt-sort').first.screenshot())[0]
                    self.assertGreaterEqual(value, 4.5, f'{theme} header {value}')
                # 360px: the table scrolls inside its region instead of being clipped by .k-dt.
                page.set_viewport_size({'width': 360, 'height': 800}); page.wait_for_timeout(100)
                region = page.locator('.k-dt-scroll').first
                widths = region.evaluate('r => [r.clientWidth, r.scrollWidth, r.closest(".k-dt").clientWidth]')
                self.assertGreater(widths[1], widths[0])
                self.assertEqual(widths[0], widths[2])
                region.focus(); page.keyboard.press('ArrowRight'); page.wait_for_timeout(100)
                self.assertGreater(region.evaluate('r => r.scrollLeft'), 0)
                self.assertLessEqual(page.evaluate('document.documentElement.scrollWidth'), 360)
                self.assertEqual(errors, [])
            finally:
                browser.close()


if __name__ == '__main__':
    unittest.main()
