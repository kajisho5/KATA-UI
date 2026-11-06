"""Optional browser regression for Slider; requires Playwright Python and Chromium."""
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
class SliderBrowser(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close); self.addCleanup(self.server.shutdown)
        self.url = f'http://127.0.0.1:{self.server.server_port}/tests/slider-multi.html'

    def test_names_sync_and_rtl_fill(self):
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 600, 'height': 900}, device_scale_factor=2); errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.goto(self.url)
                self.assertEqual(page.locator('[data-kata-ready]').count(), 6)
                self.assertEqual(page.locator('[id]').count(), 0)
                cdp = page.context.new_cdp_session(page); cdp.send('Accessibility.enable')
                names = [n.get('name', {}).get('value') for n in cdp.send('Accessibility.getFullAXTree')['nodes'] if n.get('role', {}).get('value') == 'slider']
                self.assertEqual(names, ['Volume', 'Brightness'] * 3)
                # Keys move the value once per press (double load does not double-bind) and the readout follows.
                for i in (0, 4):
                    s = page.locator('.k-slider').nth(i); s.focus(); start = int(s.input_value())
                    page.keyboard.press('ArrowUp')
                    self.assertEqual(int(s.input_value()), start + 1)
                    self.assertEqual(page.locator('[data-slider-val]').nth(i).inner_text(), str(start + 1))
                    self.assertEqual(s.evaluate('e => e.style.getPropertyValue("--p")'), f'{start + 1}%')
                # The fill starts at the inline start: left in LTR, right in RTL.
                for i, rtl in ((0, False), (4, True)):
                    s = page.locator('.k-slider').nth(i); s.evaluate('e => { e.value = 20; e.dispatchEvent(new Event("input")) }')
                    page.mouse.move(1, 1); page.locator('h1').focus(); page.wait_for_timeout(50)
                    b = s.bounding_box()
                    shot = s.screenshot()
                    from PIL import Image; import io
                    img = Image.open(io.BytesIO(shot)).convert('RGB'); w, h = img.size
                    left, right = img.getpixel((int(w * 0.04), h // 2)), img.getpixel((int(w * 0.9), h // 2))
                    dark = lambda px: sum(px) < 200
                    self.assertEqual((dark(left), dark(right)), ((False, True) if rtl else (True, False)), f'rtl={rtl} {left} {right}')
                self.assertEqual(errors, [])
            finally:
                browser.close()


if __name__ == '__main__':
    unittest.main()
