"""Optional browser regression for Separator; requires Playwright Python and Chromium."""
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
class SeparatorBrowser(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close); self.addCleanup(self.server.shutdown)
        self.url = f'http://127.0.0.1:{self.server.server_port}/tests/separator-multi.html'

    def test_width_forced_colors_roles_and_text(self):
        from playwright.sync_api import sync_playwright
        from tools.verify_button import text_contrast
        widths = """() => [...document.querySelectorAll('hr.k-sep')].map(h => {
            const p = h.parentElement, s = getComputedStyle(p);
            return [Math.round(h.getBoundingClientRect().width), Math.round(p.clientWidth - parseFloat(s.paddingLeft) - parseFloat(s.paddingRight))] })"""
        lines = """() => {
            const v = getComputedStyle(document.querySelector('.k-sep-v'));
            const a = getComputedStyle(document.querySelector('.k-sep-label'), '::before');
            const h = getComputedStyle(document.querySelector('hr.k-sep'));
            return [[v.borderInlineStartWidth, v.borderInlineStartColor], [a.borderTopWidth, a.borderTopColor], [h.borderTopWidth, h.borderTopColor], getComputedStyle(document.body).backgroundColor] }"""
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 600, 'height': 900}, device_scale_factor=2)
                errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.on('console', lambda m: m.type == 'error' and errors.append(m.text))
                page.goto(self.url)
                # The UA hr margin is auto; inside the grid preview it shrank the rule to 0px.
                for hr, parent in page.evaluate(widths):
                    self.assertEqual(hr, parent)
                    self.assertGreater(hr, 0)
                cdp = page.context.new_cdp_session(page); cdp.send('Accessibility.enable')
                nodes = [n for n in cdp.send('Accessibility.getFullAXTree')['nodes'] if not n.get('ignored')]
                self.assertEqual(sum(n.get('role', {}).get('value') == 'separator' for n in nodes), 3)
                self.assertTrue(page.evaluate("() => [...document.querySelectorAll('.k-sep-v')].every(e => e.getAttribute('aria-hidden') === 'true')"))
                for theme in ('light', 'dark'):
                    page.evaluate('t => { document.documentElement.dataset.theme = t }', theme); page.wait_for_timeout(50)
                    value = text_contrast(page.locator('.k-sep-label').first.screenshot())[0]
                    self.assertGreaterEqual(value, 4.5, f'{theme} OR {value}')
                self.assertEqual(errors, [])
                # Forced colors drop backgrounds; every line is a 1px border in the system text color.
                forced = browser.new_page(viewport={'width': 600, 'height': 900}, forced_colors='active')
                forced.goto(self.url)
                *borders, bg = forced.evaluate(lines)
                for width, color in borders:
                    self.assertEqual(width, '1px')
                    self.assertNotEqual(color, bg)
            finally:
                browser.close()


if __name__ == '__main__':
    unittest.main()
