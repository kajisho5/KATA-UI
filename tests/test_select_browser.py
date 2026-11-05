"""Optional browser regression for Select; requires Playwright Python and Chromium."""
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
class SelectBrowser(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close); self.addCleanup(self.server.shutdown)
        self.url = f'http://127.0.0.1:{self.server.server_port}/tests/select-multi.html'

    def test_three_sets_keyboard_states_and_rtl(self):
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 1100, 'height': 1200}); errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
                page.goto(self.url)
                page.evaluate('document.documentElement.style.setProperty("--k-mscale","0")')
                self.assertEqual(page.locator('section').count(), 3)
                names = page.locator('section select').evaluate_all('(es)=>es.map(e=>e.labels.length===1?e.labels[0].firstChild.textContent.trim():"")')
                self.assertEqual(names, ['Plan', 'Region', 'Availability', 'Shipping zone', 'Long option'] * 3)
                # The part no longer sets color-scheme on the page.
                self.assertEqual(page.evaluate('getComputedStyle(document.documentElement).colorScheme'), 'normal')
                for i in range(3):
                    s = page.locator('section').nth(i)
                    plan, disabled, invalid = s.locator('select').nth(0), s.locator('select[disabled]'), s.locator('select[aria-invalid="true"]')
                    plan.focus(); page.keyboard.press('Shift')
                    self.assertNotEqual(plan.evaluate('(e)=>getComputedStyle(e).boxShadow'), 'none')
                    self.assertEqual(plan.input_value(), 'Studio')
                    page.keyboard.press('ArrowDown')
                    self.assertEqual(plan.input_value(), 'Scale', 'arrow keys change the native select')
                    rest = plan.evaluate('(e)=>{e.blur();return getComputedStyle(e).borderTopColor}')
                    self.assertNotEqual(invalid.evaluate('(e)=>getComputedStyle(e).borderTopColor'), rest)
                    self.assertEqual(disabled.evaluate('(e)=>getComputedStyle(e).cursor'), 'not-allowed')
                    before = disabled.evaluate('(e)=>getComputedStyle(e).borderTopColor')
                    disabled.hover(force=True); page.wait_for_timeout(250)
                    self.assertEqual(disabled.evaluate('(e)=>getComputedStyle(e).borderTopColor'), before, 'hover does not change a disabled select')
                    page.mouse.move(0, 0)
                    s.locator('select').nth(1).focus(); page.keyboard.press('Tab')
                    self.assertTrue(invalid.evaluate('(e)=>e===document.activeElement'), 'Tab skips the disabled select')
                    # The chevron's room is on the inline end in both directions, so text never runs under it.
                    long = s.locator('select').nth(4)
                    chevron = long.locator('xpath=following-sibling::*[local-name()="svg"]').bounding_box()
                    box = long.bounding_box()
                    pad = long.evaluate('(e)=>{const s=getComputedStyle(e);return [parseFloat(s.paddingLeft),parseFloat(s.paddingRight)]}')
                    if i == 2:
                        self.assertLess(chevron['x'] + chevron['width'], box['x'] + pad[0])
                    else:
                        self.assertGreater(chevron['x'], box['x'] + box['width'] - pad[1])
                page.set_viewport_size({'width': 375, 'height': 812})
                self.assertGreaterEqual(page.locator('section select').first.evaluate('(e)=>parseFloat(getComputedStyle(e).fontSize)'), 16)
                self.assertTrue(page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
                self.assertEqual(errors, [])
            finally:
                browser.close()

    def test_text_contrast(self):
        from playwright.sync_api import sync_playwright
        from tools.verify_button import text_contrast
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 1100, 'height': 1200}, device_scale_factor=2)
                page.goto(self.url)
                for theme in ('light', 'dark'):
                    page.evaluate('(t)=>document.documentElement.dataset.theme=t', theme)
                    value = text_contrast(page.locator('section').first.locator('select').first.screenshot())[0]
                    with self.subTest(theme=theme):
                        self.assertGreaterEqual(value, 4.5)
            finally:
                browser.close()
