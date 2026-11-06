"""Optional browser regression for Spinner; requires Playwright Python and Chromium."""
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
class SpinnerBrowser(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close); self.addCleanup(self.server.shutdown)
        self.url = f'http://127.0.0.1:{self.server.server_port}/tests/spinner-multi.html'

    def test_names_sizes_contrast_and_motion(self):
        from playwright.sync_api import sync_playwright
        rgb = lambda s: [int(float(x)) for x in s[s.index('(') + 1:s.index(')')].split(',')[:3]]

        def lum(c):
            c = [x / 255 for x in c]
            c = [x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4 for x in c]
            return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]

        def ratio(a, b):
            a, b = sorted((lum(a), lum(b)), reverse=True)
            return (a + .05) / (b + .05)

        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 600, 'height': 900})
                errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.on('console', lambda m: m.type == 'error' and errors.append(m.text))
                page.goto(self.url)
                cdp = page.context.new_cdp_session(page); cdp.send('Accessibility.enable')
                nodes = cdp.send('Accessibility.getFullAXTree')['nodes']
                status = [n.get('name', {}).get('value') for n in nodes if n.get('role', {}).get('value') == 'status']
                self.assertEqual(status, ['Loading'] * 9)
                buttons = [n.get('name', {}).get('value') for n in nodes if n.get('role', {}).get('value') == 'button']
                self.assertEqual(buttons, ['Saving…'] * 3)
                sizes = page.evaluate("() => [...document.querySelectorAll('section:first-of-type .k-spinner')].map(e => e.offsetWidth)")
                # content-box: the 2px/3px ring adds to the 14/18/26px width.
                self.assertEqual(sizes, [18, 22, 32, 18])
                heights = page.evaluate("""() => {
                  const b = document.querySelector('section button'), plain = b.cloneNode(false);
                  plain.textContent = 'Saving…'; b.after(plain);
                  const h = [b.offsetHeight, plain.offsetHeight]; plain.remove(); return h }""")
                self.assertEqual(heights[0], heights[1])
                for theme in ('light', 'dark'):
                    page.evaluate('t => { document.documentElement.dataset.theme = t }', theme); page.wait_for_timeout(50)
                    edge, bg = map(rgb, page.evaluate("() => [getComputedStyle(document.querySelector('.k-spinner')).borderTopColor, getComputedStyle(document.body).backgroundColor]"))
                    # WCAG 1.4.11: the moving edge is the graphic that conveys activity.
                    self.assertGreaterEqual(ratio(edge, bg), 3, theme)
                running = page.evaluate("() => [...document.querySelectorAll('.k-spinner')].map(e => getComputedStyle(e).animationName)")
                self.assertEqual(set(running), {'k-spin'})
                page.emulate_media(reduced_motion='reduce')
                still = page.evaluate("() => [...document.querySelectorAll('.k-spinner')].map(e => getComputedStyle(e).animationName)")
                self.assertEqual(set(still), {'none'})
                self.assertEqual(errors, [])
            finally:
                browser.close()


if __name__ == '__main__':
    unittest.main()
