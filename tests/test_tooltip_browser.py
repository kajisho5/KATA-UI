"""Optional browser regression for Tooltip; requires Playwright Python and Chromium."""
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
NAMES = ['Copy', 'Settings', 'Save']


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


@unittest.skipUnless(AVAILABLE, 'Requires Playwright Python and Chromium')
class TooltipBrowser(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close); self.addCleanup(self.server.shutdown)
        self.url = f'http://127.0.0.1:{self.server.server_port}/tests/tooltip-multi.html'

    def test_names_focus_display_and_contrast(self):
        from playwright.sync_api import sync_playwright
        from tools.verify_button import text_contrast
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 900, 'height': 900}, device_scale_factor=2); errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
                page.goto(self.url)
                page.evaluate('document.documentElement.style.setProperty("--k-mscale","0")')
                # The tip text must not join the button's accessible name ("Copy Copy link" before).
                cdp = page.context.new_cdp_session(page); cdp.send('Accessibility.enable')
                names = [n.get('name', {}).get('value') for n in cdp.send('Accessibility.getFullAXTree')['nodes'] if n.get('role', {}).get('value') == 'button']
                self.assertEqual(names, NAMES * 3)
                tips = page.locator('.k-tip')
                self.assertEqual(tips.count(), 9)
                after = 'e => getComputedStyle(e, "::after").opacity'
                for i in range(9):
                    tip = tips.nth(i)
                    self.assertEqual(tip.evaluate(after), '0')
                    tip.focus(); page.keyboard.press('Shift+Tab'); page.keyboard.press('Tab')
                    self.assertEqual(tip.evaluate(after), '1', f'focus {i}')
                    page.mouse.move(1, 1); tip.evaluate('e => e.blur()')
                    tip.hover(); self.assertEqual(tip.evaluate(after), '1', f'hover {i}')
                    page.mouse.move(1, 1)
                # The rendered tip is centred on its trigger, above it (or below with data-side="bottom"), in LTR and RTL.
                for theme in ('light', 'dark'):
                    page.evaluate('t => { document.documentElement.dataset.theme = t }', theme); page.wait_for_timeout(50)
                    for i in (0, 2, 6):
                        tip = tips.nth(i); tip.hover(); box = tip.bounding_box()
                        below = tip.get_attribute('data-side') == 'bottom'
                        # A 40x12 window inside the tip's box: 9px beyond the 7px gap, centred on the trigger.
                        cx = box['x'] + box['width'] / 2
                        clip = {'x': cx - 20, 'width': 40, 'height': 12,
                                'y': box['y'] + box['height'] + 10 if below else box['y'] - 22}
                        value = text_contrast(page.screenshot(clip=clip))[0]
                        self.assertGreaterEqual(value, 4.5, f'{theme} tip {i} {value}')
                        page.mouse.move(1, 1)
                self.assertEqual(errors, [])
            finally:
                browser.close()


if __name__ == '__main__':
    unittest.main()
