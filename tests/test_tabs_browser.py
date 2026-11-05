"""Optional browser regression for Tabs; requires Playwright Python and Chromium."""
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
class TabsBrowser(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close); self.addCleanup(self.server.shutdown)
        self.url = f'http://127.0.0.1:{self.server.server_port}/tests/tabs-multi.html'

    def test_roles_keyboard_panels_rtl_and_contrast(self):
        from playwright.sync_api import sync_playwright
        from tools.verify_button import text_contrast
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 900, 'height': 1400}, device_scale_factor=2); errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
                page.goto(self.url)
                page.evaluate('document.documentElement.style.setProperty("--k-mscale","0")')
                lists = page.locator('[data-tabs]')
                self.assertEqual(lists.count(), 4)
                self.assertEqual(page.locator('[data-kata-ready]').count(), 4)
                ids = page.evaluate('[...document.querySelectorAll("[id]")].map(e => e.id)')
                self.assertEqual(len(ids), len(set(ids)))
                selected = lambda lst: [t.get_attribute('aria-selected') for t in lst.locator('[role=tab]').all()]
                visible = lambda lst: lst.evaluate('l => [...l.querySelectorAll("[role=tab]")].map(t => !document.getElementById(t.getAttribute("aria-controls")).hidden)')
                for i in range(4):
                    lst = lists.nth(i); tabs = lst.locator('[role=tab]')
                    self.assertEqual(lst.get_attribute('role'), 'tablist')
                    self.assertEqual(tabs.count(), 3)
                    self.assertEqual(selected(lst), ['true', 'false', 'false'])
                    self.assertEqual(visible(lst), [True, False, False])
                    self.assertEqual([t.evaluate('e => e.tabIndex') for t in tabs.all()], [0, -1, -1])
                    for t in tabs.all():
                        panel = page.locator('#' + t.get_attribute('aria-controls'))
                        self.assertEqual(panel.get_attribute('role'), 'tabpanel')
                        self.assertEqual(panel.get_attribute('aria-labelledby'), t.get_attribute('id'))
                    # Keyboard: arrows follow the visual direction, wrap, Home/End; selection follows focus.
                    rtl = lst.evaluate('l => getComputedStyle(l).direction') == 'rtl'
                    forward, back = ('ArrowLeft', 'ArrowRight') if rtl else ('ArrowRight', 'ArrowLeft')
                    tabs.first.focus()
                    page.keyboard.press(forward); self.assertEqual(selected(lst), ['false', 'true', 'false']); self.assertEqual(visible(lst), [False, True, False])
                    self.assertTrue(tabs.nth(1).evaluate('e => document.activeElement === e'))
                    page.keyboard.press(forward); page.keyboard.press(forward); self.assertEqual(selected(lst), ['true', 'false', 'false'])
                    page.keyboard.press(back); self.assertEqual(selected(lst), ['false', 'false', 'true'])
                    page.keyboard.press('Home'); self.assertEqual(selected(lst), ['true', 'false', 'false'])
                    page.keyboard.press('End'); self.assertEqual(selected(lst), ['false', 'false', 'true'])
                    # Click selects; the thumb sits under the selected tab.
                    tabs.nth(1).click(); self.assertEqual(selected(lst), ['false', 'true', 'false'])
                    t, th = tabs.nth(1).bounding_box(), lst.locator('.thumb').bounding_box()
                    self.assertAlmostEqual(t['x'], th['x'], delta=1); self.assertAlmostEqual(t['width'], th['width'], delta=1)
                # Tab from the selected tab moves into its panel (text-only panels take focus).
                first = lists.first.locator('[role=tab]').nth(1); first.focus(); page.keyboard.press('Tab')
                self.assertEqual(page.evaluate('document.activeElement.getAttribute("role")'), 'tabpanel')
                # The combo's hidden panels stay hidden despite their inline display:grid.
                combo = lists.nth(3)
                self.assertEqual(combo.evaluate('l => [...l.querySelectorAll("[role=tab]")].map(t => getComputedStyle(document.getElementById(t.getAttribute("aria-controls"))).display)'), ['none', 'grid', 'none'])
                # Unselected and selected tab text contrast on the segment background.
                for theme in ('light', 'dark'):
                    page.evaluate('t => { document.documentElement.dataset.theme = t }', theme); page.wait_for_timeout(50)
                    for k in (0, 1):
                        tab = lists.first.locator('[role=tab]').nth(k)
                        value = text_contrast(tab.screenshot())[0]
                        self.assertGreaterEqual(value, 4.5, f'{theme} tab {k} {value}')
                self.assertEqual(errors, [])
            finally:
                browser.close()


if __name__ == '__main__':
    unittest.main()
