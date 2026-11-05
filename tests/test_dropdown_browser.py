"""Optional browser regression for Dropdown; requires Playwright Python and Chromium."""
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
ITEMS = ['Edit', 'Duplicate', 'Copy share link', 'Delete']


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


@unittest.skipUnless(AVAILABLE, 'Requires Playwright Python and Chromium')
class DropdownBrowser(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close); self.addCleanup(self.server.shutdown)
        self.url = f'http://127.0.0.1:{self.server.server_port}/tests/dropdown-multi.html'

    def test_menu_button_keyboard_pointer_and_rtl(self):
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
                roots = page.locator('.dd'); triggers = page.locator('[data-dd-trigger]'); menus = page.locator('[data-dd-menu]')
                self.assertEqual(roots.count(), 3)
                self.assertEqual(page.locator('[data-kata-ready]').count(), 3)
                ids = page.evaluate('[...document.querySelectorAll("[id]")].map(e => e.id)')
                self.assertEqual(len(ids), len(set(ids)))
                focused = lambda: page.evaluate('document.activeElement.textContent.trim()')
                for i in range(3):
                    trigger, menu = triggers.nth(i), menus.nth(i)
                    self.assertEqual(trigger.get_attribute('aria-haspopup'), 'menu')
                    self.assertEqual(trigger.get_attribute('aria-controls'), menu.get_attribute('id'))
                    self.assertEqual(trigger.get_attribute('aria-expanded'), 'false')
                    self.assertEqual(menu.get_attribute('role'), 'menu')
                    self.assertEqual([a.get_attribute('role') for a in menu.locator('a').all()], ['menuitem'] * 4)
                    # Closed items are not Tab stops.
                    self.assertTrue(menu.evaluate('m => [...m.querySelectorAll("a")].every(a => a.tabIndex === -1)'))
                    # Enter opens and focuses the first item; arrows wrap; Home/End.
                    trigger.focus(); page.keyboard.press('Enter')
                    self.assertEqual(trigger.get_attribute('aria-expanded'), 'true'); self.assertEqual(focused(), 'Edit')
                    page.keyboard.press('ArrowUp'); self.assertEqual(focused(), 'Delete')
                    page.keyboard.press('ArrowDown'); self.assertEqual(focused(), 'Edit')
                    page.keyboard.press('ArrowDown'); self.assertEqual(focused(), 'Duplicate')
                    page.keyboard.press('End'); self.assertEqual(focused(), 'Delete')
                    page.keyboard.press('Home'); self.assertEqual(focused(), 'Edit')
                    # Escape closes and returns focus to the trigger.
                    page.keyboard.press('Escape')
                    self.assertEqual(trigger.get_attribute('aria-expanded'), 'false')
                    self.assertTrue(trigger.evaluate('e => document.activeElement === e'))
                    # ArrowUp on the trigger opens on the last item.
                    page.keyboard.press('ArrowUp'); self.assertEqual(focused(), 'Delete')
                    # Opening another instance closes this one.
                    if i < 2:
                        triggers.nth(i + 1).click()
                        self.assertEqual(trigger.get_attribute('aria-expanded'), 'false')
                        self.assertEqual(triggers.nth(i + 1).get_attribute('aria-expanded'), 'true')
                        page.keyboard.press('Escape')
                    else:
                        page.keyboard.press('Escape')
                    # Tab from an item closes the menu and moves on.
                    trigger.click(); page.keyboard.press('Tab')
                    self.assertEqual(trigger.get_attribute('aria-expanded'), 'false')
                    # A null focusout keeps it open; an outside press closes it without taking focus back.
                    trigger.click()
                    menu.evaluate('m => m.dispatchEvent(new FocusEvent("focusout", {bubbles: true, relatedTarget: null}))')
                    self.assertEqual(trigger.get_attribute('aria-expanded'), 'true')
                    page.locator('[data-outside]').click()
                    self.assertEqual(trigger.get_attribute('aria-expanded'), 'false')
                    self.assertTrue(page.locator('[data-outside]').evaluate('e => document.activeElement === e'))
                    # Choosing an item closes the menu and returns focus.
                    trigger.click(); menu.locator('a').nth(1).click()
                    self.assertEqual(trigger.get_attribute('aria-expanded'), 'false')
                    self.assertTrue(trigger.evaluate('e => document.activeElement === e'))
                # A disabled item is skipped by the arrow keys.
                menus.first.locator('a').nth(1).evaluate('a => a.setAttribute("aria-disabled", "true")')
                triggers.first.focus(); page.keyboard.press('Enter'); page.keyboard.press('ArrowDown')
                self.assertEqual(focused(), 'Copy share link'); page.keyboard.press('Escape')
                # RTL: the menu opens from the inline start (right edge) of its trigger.
                triggers.nth(2).click()
                t, m = triggers.nth(2).bounding_box(), menus.nth(2).bounding_box()
                self.assertAlmostEqual(t['x'] + t['width'], m['x'] + m['width'], delta=1)
                page.keyboard.press('Escape')
                # Item text contrast on the focused (hover-coloured) background, light and dark.
                for theme in ('light', 'dark'):
                    page.evaluate('t => { document.documentElement.dataset.theme = t }', theme); page.wait_for_timeout(50)
                    triggers.first.click()
                    for name in ('Edit', 'Delete'):
                        item = menus.first.locator('a', has_text=name); item.focus(); page.wait_for_timeout(30)
                        item.evaluate('a => a.style.outline = "none"')
                        ratio = text_contrast(item.screenshot(scale='device'))[0]
                        item.evaluate('a => a.style.outline = ""')
                        self.assertGreaterEqual(ratio, 4.5, f'{theme} {name} {ratio}')
                    page.keyboard.press('Escape')
                self.assertEqual(errors, [])
            finally:
                browser.close()


if __name__ == '__main__':
    unittest.main()
