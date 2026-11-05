"""Optional browser regression for Switch; requires Playwright Python and Chromium."""
import functools
import http.server
import importlib.util
import io
import os
import shutil
import threading
import unittest
from pathlib import Path

CHROMIUM = os.environ.get('CHROMIUM_PATH') or shutil.which('chromium')
AVAILABLE = importlib.util.find_spec('playwright') is not None and bool(CHROMIUM) and Path(CHROMIUM).exists()
NAMES = ['Notifications', 'Auto-save', 'Public', 'SSO (Scale plan)', 'Login alerts']


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


@unittest.skipUnless(AVAILABLE, 'Requires Playwright Python and Chromium')
class SwitchBrowser(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close); self.addCleanup(self.server.shutdown)
        self.url = f'http://127.0.0.1:{self.server.server_port}/tests/switch-multi.html'

    def test_names_keyboard_click_and_rtl(self):
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 1100, 'height': 1200}); errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
                page.goto(self.url)
                page.evaluate('document.documentElement.style.setProperty("--k-mscale","0")')
                # Chromium's accessibility tree: every switch has the role and its visible text as its name.
                cdp = page.context.new_cdp_session(page)
                nodes = [n for n in cdp.send('Accessibility.getFullAXTree')['nodes'] if (n.get('role') or {}).get('value') == 'switch']
                self.assertEqual([(n.get('name') or {}).get('value') for n in nodes], NAMES * 3)
                for i in range(3):
                    s = page.locator('section').nth(i)
                    public = s.locator('input').nth(2)
                    s.get_by_text('Public', exact=True).click()
                    self.assertTrue(public.is_checked(), 'clicking the text toggles the switch')
                    public.focus(); page.keyboard.press('Space')
                    self.assertFalse(public.is_checked(), 'Space toggles it back')
                    self.assertNotEqual(public.locator('xpath=following-sibling::span').evaluate('(e)=>getComputedStyle(e).boxShadow'), 'none')
                    disabled = s.locator('input[disabled]')
                    s.get_by_text('SSO (Scale plan)', exact=True).click(force=True)
                    self.assertFalse(disabled.is_checked(), 'a disabled switch does not toggle')
                    # The knob ends at the inline end: right in LTR, left in RTL.
                    on = s.locator('input').nth(0)
                    track = on.locator('xpath=following-sibling::span').bounding_box()
                    knob = on.locator('xpath=following-sibling::span').evaluate('(e)=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e,"::after");const m=new DOMMatrix(s.transform);return r.left+parseFloat(s.insetInlineStart||s.left)+m.m41}')
                    centre = track['x'] + track['width'] / 2
                    if i == 2:
                        self.assertLess(knob, centre)
                    else:
                        self.assertGreater(knob, centre)
                self.assertEqual(errors, [])
            finally:
                browser.close()

    def test_track_boundary_contrast(self):
        """The off track and the accent-on track keep 3:1 from the page at their outer edge (WCAG 1.4.11)."""
        from playwright.sync_api import sync_playwright
        from PIL import Image
        from tools.verify_button import ratio
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 1100, 'height': 1200}, device_scale_factor=2)
                page.goto(self.url)
                page.evaluate('document.documentElement.style.setProperty("--k-mscale","0")')
                for theme in ('light', 'dark'):
                    page.evaluate('(t)=>document.documentElement.dataset.theme=t', theme); page.wait_for_timeout(50)
                    s = page.locator('section').first
                    for name, i in [('off', 2), ('accent on', 1)]:
                        track = s.locator('input').nth(i).locator('xpath=following-sibling::span').bounding_box()
                        y = track['y'] + track['height'] / 2
                        # Edge pixel 0.5px inside the left end vs the page 4px outside it.
                        shot = Image.open(io.BytesIO(page.screenshot(clip={'x': track['x'] - 4, 'y': y - 1, 'width': 6, 'height': 2}))).convert('RGB')
                        edge, page_px = shot.getpixel((9, 2)), shot.getpixel((1, 2))
                        with self.subTest(theme=theme, state=name):
                            self.assertGreaterEqual(ratio(edge, page_px), 3.0)
            finally:
                browser.close()
