"""Optional browser regression for Pagination; requires Playwright Python and Chromium."""
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
class PaginationBrowser(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close); self.addCleanup(self.server.shutdown)
        self.url = f'http://127.0.0.1:{self.server.server_port}/tests/pagination-multi.html'

    def test_names_disabled_current_rtl_and_contrast(self):
        from playwright.sync_api import sync_playwright
        from tools.verify_button import text_contrast
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 700, 'height': 1200}, device_scale_factor=2); errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
                page.goto(self.url)
                page.evaluate('document.documentElement.style.setProperty("--k-mscale","0")')
                # Link names: arrows and the ellipsis are not read.
                cdp = page.context.new_cdp_session(page); cdp.send('Accessibility.enable')
                nodes = cdp.send('Accessibility.getFullAXTree')['nodes']
                links = [n.get('name', {}).get('value') for n in nodes if n.get('role', {}).get('value') == 'link']
                first = ['Previous page', '1', '2', '3', '4', '18', 'Next page', '1', '2', '3', 'Next page', 'Prev', 'Next']
                self.assertEqual(links, first * 3)
                # The disabled Previous is not a link and not a Tab stop.
                nav = page.locator('section').first.locator('nav').nth(1)
                page.locator('section').first.locator('nav').first.locator('a').last.focus()
                page.keyboard.press('Tab')
                self.assertEqual(page.evaluate('document.activeElement.textContent.trim()'), '1')
                self.assertEqual(nav.locator('[aria-disabled="true"]').evaluate('e => e.hasAttribute("href")'), False)
                # Hovering the current page keeps its filled state.
                current = page.locator('[aria-current="page"]').first
                before = current.evaluate('e => getComputedStyle(e).backgroundColor')
                current.hover(); self.assertEqual(current.evaluate('e => getComputedStyle(e).backgroundColor'), before)
                page.mouse.move(1, 1)
                # RTL: arrows are mirrored so they point in the reading direction.
                for i, mirrored in ((0, False), (2, True)):
                    sec = page.locator('section').nth(i)
                    for sel in ('.k-page svg', '.k-page-arrow'):
                        transform = sec.locator(sel).first.evaluate('e => getComputedStyle(e).transform')
                        self.assertEqual(transform.startswith('matrix(-1'), mirrored, f'{i} {sel} {transform}')
                # Number, current page and position text contrast.
                sec = page.locator('section').first
                for theme in ('light', 'dark'):
                    page.evaluate('t => { document.documentElement.dataset.theme = t }', theme); page.wait_for_timeout(50)
                    for sel in ('a.k-page:not([aria-current])', '[aria-current="page"]', '.k-page-pos'):
                        value = text_contrast(sec.locator(sel).nth(1 if sel.startswith('a.k-page') else 0).screenshot())[0]
                        self.assertGreaterEqual(value, 4.5, f'{theme} {sel} {value}')
                self.assertEqual(errors, [])
            finally:
                browser.close()


if __name__ == '__main__':
    unittest.main()
