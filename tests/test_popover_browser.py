"""Optional browser regression for Popover; requires Playwright Python and Chromium."""
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
class PopoverBrowser(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close); self.addCleanup(self.server.shutdown)
        self.url = f'http://127.0.0.1:{self.server.server_port}/tests/popover-multi.html'

    def test_panel_stays_in_narrow_viewport_and_text_contrast(self):
        from playwright.sync_api import sync_playwright
        from tools.verify_button import text_contrast
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 360, 'height': 800}, device_scale_factor=2); errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
                page.goto(self.url)
                # Triggers at the inline start of a phone-width page: the LTR left edge and the RTL right edge.
                page.add_style_tag(content='body{padding:var(--k-space-2)}section{justify-items:start}')
                page.evaluate('document.documentElement.style.setProperty("--k-mscale","0")')
                triggers = page.locator('[data-popover-btn]'); panels = page.locator('[data-popover-panel]')
                for i in range(3):
                    triggers.nth(i).scroll_into_view_if_needed(); triggers.nth(i).click()
                    box = panels.nth(i).bounding_box()
                    self.assertGreaterEqual(box['x'], 16 - 0.5, f'instance {i} left {box}')
                    self.assertLessEqual(box['x'] + box['width'], 360 - 16 + 0.5, f'instance {i} right {box}')
                    for theme in ('light', 'dark'):
                        page.evaluate('t => { document.documentElement.dataset.theme = t }', theme); page.wait_for_timeout(50)
                        for part, minimum in (('.kpop-h', 4.5), ('.kpop-p', 4.5)):
                            value = text_contrast(panels.nth(i).locator(part).screenshot())[0]
                            self.assertGreaterEqual(value, minimum, f'{theme} {part} {value}')
                    # An outside press closes it; one shared listener serves every instance.
                    page.mouse.click(350, 5)
                    self.assertEqual(triggers.nth(i).get_attribute('aria-expanded'), 'false')
                    page.evaluate('() => { document.documentElement.dataset.theme = "light" }')
                # A wide viewport keeps the panel centred under its trigger (no shift).
                page.set_viewport_size({'width': 1100, 'height': 800})
                page.add_style_tag(content='section{justify-items:center}')
                triggers.first.click()
                t, b = triggers.first.bounding_box(), panels.first.bounding_box()
                self.assertAlmostEqual(t['x'] + t['width'] / 2, b['x'] + b['width'] / 2, delta=1)
                self.assertEqual(errors, [])
            finally:
                browser.close()


if __name__ == '__main__':
    unittest.main()
