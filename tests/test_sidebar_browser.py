"""Optional browser regression for Sidebar; requires Playwright Python and Chromium."""
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
class SidebarBrowser(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close); self.addCleanup(self.server.shutdown)
        self.url = f'http://127.0.0.1:{self.server.server_port}/tests/sidebar-multi.html'

    def test_names_current_toggle_rtl_rail_and_text(self):
        from playwright.sync_api import sync_playwright
        from tools.verify_button import text_contrast
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 900, 'height': 1000}, device_scale_factor=2)
                errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.on('console', lambda m: m.type == 'error' and errors.append(m.text))
                page.goto(self.url)  # the page loads sidebar.js twice
                cdp = page.context.new_cdp_session(page); cdp.send('Accessibility.enable')
                nodes = [n for n in cdp.send('Accessibility.getFullAXTree')['nodes'] if not n.get('ignored')]
                role = lambda r: [n.get('name', {}).get('value') for n in nodes if n.get('role', {}).get('value') == r]
                self.assertEqual(role('navigation'), [f'{k} {i}' for i in (1, 2, 3) for k in ('Sidebar', 'Rail')])
                links = role('link')
                # Rail labels are visually hidden, so rail links keep their text names.
                for name in ('Overview', 'Reports', 'Team', 'Settings'):
                    self.assertEqual(links.count(name), 6, name)  # full sidebar and rail, three sets each
                self.assertEqual(links.count('Projects'), 3)  # rail links; the full sidebar has a group button
                self.assertEqual(links.count('Calendar'), 3)
                self.assertEqual(links.count('Calendar 3'), 3)  # the full sidebar includes the badge count
                self.assertEqual(role('button'), ['Projects'] * 3)
                self.assertEqual(page.evaluate("() => [...document.querySelectorAll('nav')].map(n => n.querySelectorAll('[aria-current=page]').length)"), [1] * 6)
                self.assertEqual(page.evaluate("() => [...document.querySelectorAll('.k-side-ava')].every(a => a.getAttribute('aria-hidden') === 'true')"), True)
                self.assertEqual(sum(1 for n in nodes if n.get('role', {}).get('value') == 'StaticText' and n.get('name', {}).get('value') == 'Aoki Ren'), 6)
                box = page.locator('.k-side.rail .k-side-t').first.bounding_box()
                self.assertLessEqual(box['width'] * box['height'], 1)
                # One click toggles once even with the script loaded twice.
                toggle = page.locator('[data-side-toggle]').first
                toggle.click()
                self.assertEqual(toggle.get_attribute('aria-expanded'), 'false')
                self.assertFalse(page.locator('.k-side-sub').first.is_visible())
                toggle.click()
                self.assertEqual(toggle.get_attribute('aria-expanded'), 'true')
                # Sub-items are indented from the inline start: left in LTR, right in RTL.
                indent = """i => { const nav = document.querySelectorAll('nav.k-side:not(.rail)')[i].getBoundingClientRect();
                    const sub = document.querySelectorAll('nav.k-side:not(.rail) .k-side-sub')[i].getBoundingClientRect();
                    return [Math.round(sub.left - nav.left), Math.round(nav.right - sub.right)] }"""
                ltr, rtl = page.evaluate(indent, 0), page.evaluate(indent, 2)
                self.assertGreater(ltr[0], ltr[1]); self.assertGreater(rtl[1], rtl[0])
                self.assertEqual(ltr, rtl[::-1])
                for theme in ('light', 'dark'):
                    page.evaluate('t => { document.documentElement.dataset.theme = t }', theme); page.wait_for_timeout(400)
                    for sel in ('.k-side-sec', '.k-side-urole', '.k-side-item:not(.on) .k-side-t', '.k-side-badge'):
                        value = text_contrast(page.locator(sel).first.screenshot())[0]
                        self.assertGreaterEqual(value, 4.5, f'{theme} {sel} {value}')
                self.assertEqual(errors, [])
            finally:
                browser.close()


if __name__ == '__main__':
    unittest.main()
