"""Run with python3 -m unittest discover -s tests -p test_combobox_browser.py."""
import importlib.util
from pathlib import Path
import shutil
import functools
import http.server
import threading
import unittest

AVAILABLE = importlib.util.find_spec('playwright') is not None and shutil.which('chromium') is not None

@unittest.skipUnless(AVAILABLE, 'Requires Playwright Python and Chromium')
class ComboboxBrowser(unittest.TestCase):
    def test_copied_markup_and_interaction(self):
        from playwright.sync_api import sync_playwright
        root=Path(__file__).resolve().parents[1]
        handler=functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(root))
        server=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler)
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        self.addCleanup(server.server_close);self.addCleanup(server.shutdown)
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
            try:
                page=browser.new_page();errors=[]
                page.on('pageerror',lambda error:errors.append(str(error)))
                page.goto(f'http://127.0.0.1:{server.server_port}/tests/combobox-multi.html')
                combos=page.locator('[data-combo]');self.assertEqual(combos.count(),3)
                self.assertEqual(page.locator('[data-kata-ready]').count(),3)
                self.assertTrue(page.evaluate('()=>{const ids=[...document.querySelectorAll("[id]")].map(x=>x.id);return ids.length===new Set(ids).size}'))
                for i in range(3):
                    combo=combos.nth(i);field=combo.locator('input');status=combo.locator('[role=status]')
                    field.click();self.assertEqual(field.input_value(),'Astro')
                    self.assertEqual(combo.locator('[data-val]:visible').count(),16)
                    self.assertEqual(status.inner_text(),'')
                    field.press('Escape');field.press('Alt+ArrowDown')
                    self.assertEqual(combo.locator('[data-val]:visible').count(),16)
                    self.assertEqual(status.inner_text(),'')
                    field.fill('Django');self.assertEqual(combo.locator('[data-val]:visible').count(),1)
                    self.assertEqual(status.inner_text(),'1 result available.')
                    field.click();self.assertEqual(combo.locator('[data-val]:visible').count(),16)
                    self.assertEqual(status.inner_text(),'')
                    combo.evaluate('(e)=>e.dataset.comboResultMany="{count} choices"')
                    field.fill('zzz');self.assertEqual(status.inner_text(),'0 choices')
                    self.assertTrue(combo.locator('.none').is_visible())
                    field.fill('');field.press('ArrowDown')
                    field.dispatch_event('keydown',{'key':'Enter','isComposing':True})
                    self.assertEqual(field.input_value(),'')
                    field.press('Enter');self.assertEqual(field.input_value(),'Astro')
                    self.assertIsNone(field.get_attribute('aria-activedescendant'))
                    field.press('Tab');self.assertEqual(field.get_attribute('aria-expanded'),'false')
                # Zero enabled options must produce the same empty result as zero matches.
                combo=combos.first;combo.locator('[data-val]').evaluate_all('(es)=>es.forEach(e=>e.setAttribute("aria-disabled","true"))')
                combo.locator('input').click();self.assertTrue(combo.locator('.none').is_visible())
                self.assertEqual(combo.locator('[role=status]').inner_text(),'')
                self.assertEqual(errors,[])
            finally:browser.close()
