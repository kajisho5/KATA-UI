"""Optional browser regression; requires Playwright Python and system Chromium."""
import functools
import os
import http.server
import importlib.util
from pathlib import Path
import shutil
import threading
import unittest

CHROMIUM=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium')
AVAILABLE=importlib.util.find_spec('playwright') is not None and bool(CHROMIUM) and Path(CHROMIUM).exists()

@unittest.skipUnless(AVAILABLE,'Requires Playwright Python and Chromium')
class ButtonBrowser(unittest.TestCase):
    def test_three_sets_states_and_rtl(self):
        from playwright.sync_api import sync_playwright
        root=Path(__file__).resolve().parents[1]
        server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(root)))
        threading.Thread(target=server.serve_forever,daemon=True).start()
        self.addCleanup(server.server_close);self.addCleanup(server.shutdown)
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path=CHROMIUM,args=['--no-sandbox'])
            try:
                page=browser.new_page(viewport={'width':1100,'height':800});errors=[]
                page.on('pageerror',lambda error:errors.append(str(error)))
                page.on('console',lambda msg:errors.append(msg.text) if msg.type=='error' else None)
                page.goto(f'http://127.0.0.1:{server.server_port}/tests/button-multi.html')
                self.assertEqual(page.locator('section').count(),3)
                self.assertEqual(page.locator('button:not([type="button"])').count(),0)
                self.assertEqual(page.locator('section').nth(2).evaluate('(e)=>getComputedStyle(e).direction'),'rtl')
                page.evaluate('document.querySelectorAll("button").forEach(b=>b.addEventListener("click",()=>b.dataset.clicks=String(+(b.dataset.clicks||0)+1)))')
                for i in range(3):
                    section=page.locator('section').nth(i)
                    for variant in ['pri','sec','ghost','accent','danger']:
                        button=section.locator('.btn-'+variant).first
                        button.focus();self.assertNotEqual(button.evaluate('(e)=>getComputedStyle(e).boxShadow'),'none')
                        button.hover();page.mouse.down()
                        self.assertNotEqual(button.evaluate('(e)=>getComputedStyle(e).transform'),'none');page.mouse.up()
                        count=int(button.get_attribute('data-clicks') or 0)
                        button.press('Enter');button.press('Space')
                        self.assertEqual(int(button.get_attribute('data-clicks')),count+2)
                        button.evaluate('(e)=>e.disabled=true')
                        self.assertEqual(button.evaluate('(e)=>getComputedStyle(e).opacity'),'0.45')
                        button.evaluate('(e)=>e.disabled=false')
                    loading=section.locator('[aria-busy="true"]')
                    self.assertGreater(loading.count(),0)
                    self.assertTrue(loading.evaluate_all('(es)=>es.every(e=>e.disabled)'))
                self.assertEqual(page.locator('section').nth(0).locator('button').first.get_attribute('data-clicks'),page.locator('section').nth(1).locator('button').first.get_attribute('data-clicks'))
                page.locator('section').first.evaluate('(e)=>e.insertAdjacentHTML("beforeend",\'<button type="button" class="btn btn-asagi btn-md">Legacy accent</button>\')')
                alias=page.locator('.btn-asagi');accent=page.locator('.btn-accent').first
                self.assertEqual(alias.evaluate('(e)=>getComputedStyle(e).backgroundColor'),accent.evaluate('(e)=>getComputedStyle(e).backgroundColor'))
                page.emulate_media(reduced_motion='reduce')
                self.assertTrue(page.locator('.spin').evaluate_all('(es)=>es.every(e=>getComputedStyle(e).animationName==="none")'))
                page.set_viewport_size({'width':375,'height':812})
                self.assertTrue(page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
                self.assertEqual(errors,[])
            finally:browser.close()

    def test_variant_state_contrast(self):
        from tools.verify_button import run, problems
        result=run()
        self.assertEqual(len(result['rows']),30)
        self.assertEqual(problems(result),[])
