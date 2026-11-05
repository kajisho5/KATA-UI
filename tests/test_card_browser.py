"""Optional browser regression for Card; requires Playwright Python and Chromium."""
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
class CardBrowser(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close); self.addCleanup(self.server.shutdown)
        self.url = f'http://127.0.0.1:{self.server.server_port}/tests/card-multi.html'

    def test_names_layout_rtl_link_focus_and_contrast(self):
        from playwright.sync_api import sync_playwright
        from tools.verify_button import text_contrast
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 320, 'height': 900}, device_scale_factor=2); errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
                page.goto(self.url)
                page.evaluate('document.documentElement.style.setProperty("--k-mscale","0")')
                # Progress bars in the combo have names (they were announced only as "progress bar").
                cdp = page.context.new_cdp_session(page); cdp.send('Accessibility.enable')
                bars = [n.get('name', {}).get('value') for n in cdp.send('Accessibility.getFullAXTree')['nodes'] if n.get('role', {}).get('value') == 'progressbar']
                self.assertEqual(bars, ['Build minutes', 'API calls'])
                # No horizontal page overflow at 320px.
                self.assertLessEqual(page.evaluate('document.documentElement.scrollWidth'), 320)
                # RTL: the header badge sits at the inline end, which is the left edge.
                cards = page.locator('section > .k-card')
                ltr = cards.nth(0).locator('.k-card-h .sp').bounding_box(); rtl = cards.nth(2).locator('.k-card-h .sp').bounding_box()
                self.assertGreater(ltr['x'], rtl['x'])
                # The whole-card link shows a focus ring outside its box (not clipped by overflow:hidden).
                link = page.locator('a.k-card')
                link.focus(); page.keyboard.press('Shift+Tab'); page.keyboard.press('Tab')
                self.assertTrue(link.evaluate('e => document.activeElement === e'))
                outline = link.evaluate('e => { const s = getComputedStyle(e); return [s.outlineStyle, parseFloat(s.outlineWidth)] }')
                self.assertNotEqual(outline[0], 'none'); self.assertGreaterEqual(outline[1], 2)
                link.evaluate('e => e.blur()')
                # Text contrast: header detail, body, footer text (ink-3 on bg-soft is the tightest pair).
                card = cards.first
                for theme in ('light', 'dark'):
                    page.evaluate('t => { document.documentElement.dataset.theme = t }', theme); page.wait_for_timeout(50)
                    card.scroll_into_view_if_needed()
                    # The footer note is a bare text node: measure the box of that text only.
                    footer = card.locator('.k-card-f').evaluate('f => { const r = document.createRange(); r.selectNodeContents(f.firstChild); const b = r.getBoundingClientRect(); return {x: b.x, y: b.y, width: b.width, height: b.height} }')
                    values = {
                        'detail': text_contrast(card.locator('.k-card-h p').screenshot())[0],
                        'body': text_contrast(card.locator('.k-card-b').screenshot())[0],
                        'footer': text_contrast(page.screenshot(clip={'x': footer['x'] - 2, 'y': footer['y'] - 2, 'width': footer['width'] + 4, 'height': footer['height'] + 4}))[0],
                    }
                    for name, value in values.items():
                        self.assertGreaterEqual(value, 4.5, f'{theme} {name} {value}')
                self.assertEqual(errors, [])
            finally:
                browser.close()


if __name__ == '__main__':
    unittest.main()
