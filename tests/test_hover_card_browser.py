"""Optional browser regression for HoverCard; requires Playwright Python and Chromium."""
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
class HoverCardBrowser(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close); self.addCleanup(self.server.shutdown)
        self.url = f'http://127.0.0.1:{self.server.server_port}/tests/hover-card-multi.html'

    def test_hidden_when_closed_focus_escape_hover_and_fit(self):
        from playwright.sync_api import sync_playwright
        from tools.verify_button import text_contrast
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 900, 'height': 1200}, device_scale_factor=2)
                errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.on('console', lambda m: m.type == 'error' and errors.append(m.text))
                page.goto(self.url)  # hover-card.js loaded twice
                cdp = page.context.new_cdp_session(page); cdp.send('Accessibility.enable')

                def texts():
                    nodes = cdp.send('Accessibility.getFullAXTree')['nodes']
                    return [n.get('name', {}).get('value') for n in nodes if not n.get('ignored') and n.get('role', {}).get('value') == 'StaticText']

                doc = cdp.send('Runtime.evaluate', {'expression': 'document'})['result']['objectId']
                types = [l['type'] for l in cdp.send('DOMDebugger.getEventListeners', {'objectId': doc})['listeners']]
                self.assertEqual(types.count('keydown'), 1)
                # Closed cards are not read inside the sentence.
                self.assertEqual(texts().count('Product designer, Tokyo'), 0)
                trigger = page.locator('.trigger').first
                wrap = page.locator('[data-hover]').first
                trigger.focus(); page.wait_for_timeout(250)
                self.assertIn('open', wrap.get_attribute('class'))
                self.assertEqual(texts().count('Product designer, Tokyo'), 1)
                # WCAG 1.4.13: Escape dismisses without moving focus.
                page.keyboard.press('Escape')
                self.assertNotIn('open', wrap.get_attribute('class'))
                self.assertTrue(page.evaluate("() => document.activeElement.classList.contains('trigger')"))
                page.locator('h1').click()
                # Pointer: opens after the delay, closes after leaving.
                page.locator('.trigger').nth(1).hover(); page.wait_for_timeout(500)
                self.assertIn('open', page.locator('[data-hover]').nth(1).get_attribute('class'))
                page.mouse.move(5, 5); page.wait_for_timeout(500)
                self.assertNotIn('open', page.locator('[data-hover]').nth(1).get_attribute('class'))
                for theme in ('light', 'dark'):
                    page.evaluate('t => { document.documentElement.dataset.theme = t }', theme)
                    page.evaluate('() => document.activeElement.blur()')
                    trigger.focus(); page.wait_for_timeout(400)
                    box = page.locator('.card > p').first.bounding_box()
                    value = text_contrast(page.screenshot(clip=box, animations='disabled'))[0]
                    self.assertGreaterEqual(value, 4.5, f'{theme} card text {value}')
                    page.keyboard.press('Escape')
                # 360px: the open card stays inside the viewport in LTR and RTL.
                page.set_viewport_size({'width': 360, 'height': 800})
                for i in (0, 2):
                    page.evaluate('() => document.activeElement.blur()')
                    page.locator('.trigger').nth(i).focus(); page.wait_for_timeout(400)
                    self.assertIn('open', page.locator('[data-hover]').nth(i).get_attribute('class'))
                    left, right = page.evaluate("i => { const r = document.querySelectorAll('.card')[i].getBoundingClientRect(); return [r.left, r.right] }", i)
                    self.assertGreaterEqual(left, 0); self.assertLessEqual(right, 360)
                self.assertEqual(errors, [])
            finally:
                browser.close()


if __name__ == '__main__':
    unittest.main()
