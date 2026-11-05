"""Optional browser regression for Table; requires Playwright Python and Chromium."""
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
class TableBrowser(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close); self.addCleanup(self.server.shutdown)
        self.url = f'http://127.0.0.1:{self.server.server_port}/tests/table-multi.html'

    def test_headers_names_scroll_alignment_and_contrast(self):
        from playwright.sync_api import sync_playwright
        from tools.verify_button import text_contrast
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 360, 'height': 1200}, device_scale_factor=2); errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
                page.goto(self.url)
                cdp = page.context.new_cdp_session(page); cdp.send('Accessibility.enable')
                nodes = cdp.send('Accessibility.getFullAXTree')['nodes']
                role = lambda r: [n.get('name', {}).get('value') for n in nodes if n.get('role', {}).get('value') == r and not n.get('ignored')]
                # Column headers, a named scroll region, and owner cells without the avatar initials.
                self.assertEqual(role('columnheader'), ['Project', 'Owner', 'Status', 'Amount'] * 3)
                self.assertEqual(role('region'), ['Projects'] * 3)
                self.assertEqual(role('cell')[1], 'Yamada')
                # At 360px the table scrolls inside its region; the region takes focus and arrow keys scroll it.
                wrap = page.locator('.ktable-wrap').first
                self.assertGreater(wrap.evaluate('w => w.scrollWidth - w.clientWidth'), 0)
                self.assertLessEqual(page.evaluate('document.documentElement.scrollWidth'), 360)
                wrap.focus(); page.keyboard.press('Shift+Tab'); page.keyboard.press('Tab')
                self.assertTrue(wrap.evaluate('w => document.activeElement === w'))
                self.assertNotEqual(wrap.evaluate('w => getComputedStyle(w).outlineStyle'), 'none')
                page.keyboard.press('ArrowRight'); page.wait_for_timeout(100)
                self.assertGreater(wrap.evaluate('w => w.scrollLeft'), 0)
                # Amounts align to the inline end of their column (left edge in RTL).
                page.set_viewport_size({'width': 900, 'height': 1200})
                for i, rtl in ((0, False), (2, True)):
                    cell = page.locator('.ktable').nth(i).locator('td.num').first
                    box = cell.bounding_box()
                    text = cell.evaluate('c => { const r = document.createRange(); r.selectNodeContents(c); const b = r.getBoundingClientRect(); return [b.left, b.right] }')
                    if rtl: self.assertLess(text[0] - box['x'], 16)
                    else: self.assertLess(box['x'] + box['width'] - text[1], 16)
                # Header and cell text contrast in both themes.
                table = page.locator('.ktable').first
                for theme in ('light', 'dark'):
                    page.evaluate('t => { document.documentElement.dataset.theme = t }', theme); page.wait_for_timeout(50)
                    for sel in ('th', 'tbody td:first-child', 'tbody td.num'):
                        value = text_contrast(table.locator(sel).first.screenshot())[0]
                        self.assertGreaterEqual(value, 4.5, f'{theme} {sel} {value}')
                self.assertEqual(errors, [])
            finally:
                browser.close()


if __name__ == '__main__':
    unittest.main()
