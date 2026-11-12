"""Optional browser regression for Pixel Switch; requires Playwright Python and Chromium."""
import functools
import http.server
import importlib.util
import os
import re
import shutil
import threading
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHROMIUM = os.environ.get('CHROMIUM_PATH') or shutil.which('chromium')
AVAILABLE = importlib.util.find_spec('playwright') is not None and bool(CHROMIUM) and Path(CHROMIUM).exists()
JS = (ROOT / 'components' / 'pixel-switch' / 'pixel-switch.js').read_text(encoding='utf-8')
# The same maps the part draws, read from its source: name -> (unchecked cells, checked cells).
MAPS = {}
for name, off, on in re.findall(r"(\w+): \[\s*\[([^\]]+)\],\s*\[([^\]]+)\]\]", JS):
    MAPS[name] = tuple({(x, y) for y, row in enumerate(re.findall(r"'([.#]{11})'", rows)) for x, c in enumerate(row) if c == '#'}
                       for rows in (off, on))
VARIANTS = ['theme', 'sound', 'bell', 'power', 'theme', 'bell']
CHECKED = [False, True, False, True, True, False]

# Lit dots of one part, as integer cells read from layout (dot offset / cell size).
LIT = '''root => {
  const box = root.querySelector('.k-pxs-dots').getBoundingClientRect();
  return [...root.querySelectorAll('.k-pxs-dots > span')].filter(d => getComputedStyle(d).opacity === '1').map(d => {
    const r = d.getBoundingClientRect();
    return [(r.left - box.left) / r.width, (r.top - box.top) / r.height];
  });
}'''


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


@unittest.skipUnless(AVAILABLE, 'Requires Playwright Python and Chromium')
class PixelSwitchBrowser(unittest.TestCase):
    def setUp(self):
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(ROOT)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close); self.addCleanup(self.server.shutdown)
        self.url = f'http://127.0.0.1:{self.server.server_port}/tests/pixel-switch-multi.html'

    def cells(self, root):
        points = root.evaluate(LIT)
        for x, y in points:
            self.assertAlmostEqual(x, round(x), delta=0.02)
            self.assertAlmostEqual(y, round(y), delta=0.02)
        return {(round(x), round(y)) for x, y in points}

    def test_icons_toggle_interrupt_rtl_focus_and_twice_loaded(self):
        from playwright.sync_api import sync_playwright
        self.assertEqual(set(MAPS), {'theme', 'sound', 'bell', 'power'})
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 1200, 'height': 1400}); errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.on('console', lambda m: errors.append(m.text) if m.type == 'error' and 'favicon' not in m.text else None)
                page.goto(self.url)
                roots = page.locator('[data-pxs]')
                self.assertEqual(roots.count(), 18)
                for k in range(18):
                    root = roots.nth(k); name = VARIANTS[k % 6]
                    self.assertEqual(root.get_attribute('data-kata-ready'), 'true')
                    # Loading the script twice adds no second set of dots.
                    self.assertEqual(root.locator('.k-pxs-dots > span').count(), max(len(m) for m in MAPS[name]))
                    self.assertEqual(root.locator('input').is_checked(), CHECKED[k % 6])
                    self.assertEqual(self.cells(root), MAPS[name][CHECKED[k % 6]], f'{k} {name}')

                # Animated toggle: dots leave the grid mid-flight and land on the checked icon.
                root = roots.nth(0)
                root.locator('input').click()
                page.wait_for_timeout(200)
                mid = root.evaluate(LIT)
                off_grid = [pt for pt in root.evaluate('''root => [...root.querySelectorAll('.k-pxs-dots > span')].map(d => {
                    const b = root.querySelector('.k-pxs-dots').getBoundingClientRect(), r = d.getBoundingClientRect();
                    return [(r.left - b.left) / r.width, (r.top - b.top) / r.height]; })''') if abs(pt[0] - round(pt[0])) > 0.05]
                self.assertTrue(off_grid or len(mid) < len(MAPS['theme'][1]), 'no motion observed')
                page.wait_for_timeout(1200)
                self.assertTrue(root.locator('input').is_checked())
                self.assertEqual(self.cells(root), MAPS['theme'][1])

                # An interrupted morph still lands on the final state.
                root.locator('input').click(); page.wait_for_timeout(120); root.locator('input').click()
                page.wait_for_timeout(1300)
                self.assertEqual(self.cells(root), MAPS['theme'][1])

                # Keyboard: Space toggles; multiplier zero changes the icon at once.
                page.evaluate('document.documentElement.style.setProperty("--k-mscale","0")')
                sound = roots.nth(1)
                sound.locator('input').focus(); page.keyboard.press('Space')
                self.assertFalse(sound.locator('input').is_checked())
                self.assertEqual(self.cells(sound), MAPS['sound'][0])

                # Focus draws the ring on the track.
                track = sound.locator('.k-pxs-track')
                focused = track.evaluate('e => getComputedStyle(e).boxShadow')
                page.locator('[data-outside]').focus()
                self.assertNotEqual(focused, track.evaluate('e => getComputedStyle(e).boxShadow'))

                # Disabled parts ignore clicks.
                disabled = roots.nth(5)
                disabled.click(force=True)
                self.assertFalse(disabled.locator('input').is_checked())

                # RTL: off sits at the inline start (right), on at the inline end (left).
                for k, on in ((12, False), (13, True)):
                    knob = roots.nth(k).locator('.k-pxs-knob').bounding_box(); box = roots.nth(k).bounding_box()
                    centre = knob['x'] + knob['width'] / 2 - box['x']
                    self.assertEqual(centre < box['width'] / 2, on, k)
                # The icon keeps its drawing in RTL.
                self.assertEqual(self.cells(roots.nth(13)), MAPS['sound'][1])
                self.assertEqual(errors, [])
            finally:
                browser.close()

    def test_reduced_motion_changes_icon_without_animation(self):
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                page = browser.new_page(viewport={'width': 1200, 'height': 900}, reduced_motion='reduce')
                page.goto(self.url)
                root = page.locator('[data-pxs]').nth(3)
                root.locator('input').click()
                self.assertEqual(root.evaluate('r => r.querySelectorAll(".k-pxs-dots > span")[0].getAnimations().length'), 0)
                self.assertEqual(self.cells(root), MAPS['power'][0])
            finally:
                browser.close()


if __name__ == '__main__':
    unittest.main()
