"""Closed Dropdown menus and collapsed Speed Dial actions must not be Tab stops."""
import http.server
import threading
import unittest
from functools import partial
from pathlib import Path
try:
    from playwright.sync_api import sync_playwright
    from tools.verify_focus_ring import Quiet, load, registry_pages
except ImportError:
    sync_playwright=None


@unittest.skipIf(sync_playwright is None or not Path('/usr/bin/chromium').exists() or not Path('dist/registry.json').exists(),'Playwright/Chromium or built registry unavailable')
class ClosedMenuTabOrder(unittest.TestCase):
    def test_closed_items_skipped_open_items_reachable(self):
        root=Path(__file__).resolve().parents[1]
        server=http.server.ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(root)))
        threading.Thread(target=server.serve_forever,daemon=True).start()
        pages={item['name']:(html,scripts) for item,html,scripts in registry_pages(['dropdown','speed-dial'])}
        active='()=>(document.activeElement.textContent||"").trim()'
        try:
            with sync_playwright() as p:
                browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
                for scale in ('1','0'):
                    page=browser.new_page();page.goto(f'http://127.0.0.1:{server.server_port}/tokens.css')
                    load(page,*pages['dropdown']);page.evaluate('(s)=>document.documentElement.style.setProperty("--k-mscale",s)',scale)
                    page.focus('#kata-focus-start');page.keyboard.press('Tab');self.assertEqual(page.evaluate(active),'Actions')
                    page.keyboard.press('Tab');self.assertNotIn(page.evaluate(active),['Edit','Duplicate','Copy share link','Delete'])
                    page.click('[data-dd-trigger]');page.keyboard.press('Tab');self.assertEqual(page.evaluate(active),'Edit')
                    page.keyboard.press('Escape');page.wait_for_timeout(300)
                    self.assertEqual(page.locator('[data-dd-menu]').evaluate('e=>getComputedStyle(e).visibility'),'hidden')
                    load(page,*pages['speed-dial'])
                    page.focus('#kata-focus-start');page.keyboard.press('Tab');self.assertEqual(page.evaluate('()=>document.activeElement.getAttribute("aria-label")'),'Create')
                    page.keyboard.press('Enter');page.keyboard.press('Shift+Tab');self.assertEqual(page.evaluate(active),'Invite people')
                    page.keyboard.press('Escape');page.wait_for_timeout(300)
                    self.assertEqual(page.locator('.k-dial .acts').evaluate('e=>getComputedStyle(e).visibility'),'hidden')
                    page.close()
                browser.close()
        finally:
            server.shutdown();server.server_close()
