"""Regression: the multiplier applies once; reduced/zero motion cannot strand a wobble."""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright=None


@unittest.skipIf(sync_playwright is None or not Path('/usr/bin/chromium').exists(),'Playwright/Chromium unavailable')
class MotionTokens(unittest.TestCase):
    def test_multiplier_aliases_and_zero_completion(self):
        config=json.loads((ROOT/'system/tokens.json').read_text())['motion']
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
            for preference,scale in [('no-preference',.5),('no-preference',2),('no-preference',0),('reduce',2)]:
                page=browser.new_page(reduced_motion=preference)
                page.set_content('<style>'+(ROOT/'tokens.css').read_text()+(ROOT/'components/jelly-buttons/jelly-buttons.css').read_text()+'</style><button type="button" class="k-jelly">Press</button><div id="host" style="transition:opacity 400ms linear">Host application</div>')
                self.assertEqual(page.locator('#host').evaluate('(e)=>getComputedStyle(e).transitionDuration'),'0.4s')
                page.evaluate('(v)=>document.documentElement.style.setProperty("--k-mscale",v)',str(scale))
                for index,(name,milliseconds) in enumerate(config['durationsMs'].items(),1):
                    for token in (name,str(index)):
                        page.locator('button').evaluate('(e,token)=>e.style.transition="opacity var(--k-dur-"+token+")"',token)
                        actual=page.locator('button').evaluate('(e)=>parseFloat(getComputedStyle(e).transitionDuration)')
                        self.assertAlmostEqual(actual,0 if preference=='reduce' else milliseconds/1000*scale)
                script=(ROOT/'components/jelly-buttons/jelly-buttons.js').read_text()
                page.add_script_tag(content=script);page.add_script_tag(content=script)
                page.clock.install();page.locator('button').click()
                if scale==0 or preference=='reduce':self.assertFalse(page.locator('button').evaluate('(e)=>e.classList.contains("squish")'))
                else:
                    # Suppress the end event: timeout must still complete the effect.
                    page.locator('button').evaluate('(e)=>e.getAnimations().forEach(a=>a.pause())')
                    page.clock.run_for(1200)
                    self.assertFalse(page.locator('button').evaluate('(e)=>e.classList.contains("squish")'))
                page.close()
            browser.close()
