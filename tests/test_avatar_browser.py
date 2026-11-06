"""Optional browser regression for Avatar; requires Playwright Python and Chromium."""
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
class AvatarBrowser(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close); self.addCleanup(self.server.shutdown)
        self.url = f'http://127.0.0.1:{self.server.server_port}/tests/avatar-multi.html'

    def test_names_rtl_status_and_contrast(self):
        from playwright.sync_api import sync_playwright
        from tools.verify_button import text_contrast
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 600, 'height': 900}, device_scale_factor=2)
                page.goto(self.url)
                cdp = page.context.new_cdp_session(page); cdp.send('Accessibility.enable')
                nodes = [n for n in cdp.send('Accessibility.getFullAXTree')['nodes'] if not n.get('ignored')]
                images = [n.get('name', {}).get('value') for n in nodes if n.get('role', {}).get('value') == 'image']
                self.assertEqual(images, ['Aki Morita, online', 'Ren A., Mio T., Jun O. and 3 more'] * 3)
                # Decorative avatars (initials next to nothing that names them) are out of the accessibility tree.
                cdp.send('DOM.enable'); root = cdp.send('DOM.getDocument')['root']['nodeId']
                hidden = cdp.send('DOM.querySelectorAll', {'nodeId': root, 'selector': '.k-avatar[aria-hidden="true"]'})['nodeIds']
                self.assertEqual(len(hidden), 9)
                for node in hidden:
                    tree = cdp.send('Accessibility.getPartialAXTree', {'nodeId': node, 'fetchRelatives': False})['nodes']
                    self.assertTrue(tree[0].get('ignored'), tree[0])
                # The status dot sits at the inline end: right in LTR, left in RTL.
                for i, rtl in ((0, False), (2, True)):
                    a = page.locator('section').nth(i).locator('[data-status]')
                    dot = a.evaluate('e => { const s = getComputedStyle(e, "::after"); return [s.left, s.right] }')
                    box_w = a.bounding_box()['width']
                    left = float(dot[0].rstrip('px'))
                    self.assertEqual(left < box_w / 2, rtl, f'{i} {dot}')
                for theme in ('light', 'dark'):
                    page.evaluate('t => { document.documentElement.dataset.theme = t }', theme); page.wait_for_timeout(50)
                    value = text_contrast(page.locator('.k-avatar[data-size="lg"]').first.screenshot())[0]
                    self.assertGreaterEqual(value, 4.5, f'{theme} {value}')
            finally:
                browser.close()


if __name__ == '__main__':
    unittest.main()
