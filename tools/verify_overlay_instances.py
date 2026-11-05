"""Exercise three real overlay instances, RTL, double load, native focus and zero motion."""
import json,http.server,threading,re
from functools import partial
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
SPECS={'alert-dialog':('data-alert-dialog','data-alert-open','data-alert-close'),'drawer':('data-drawer','data-drawer-open','data-drawer-close'),'popover':('data-popover','data-popover-btn','data-popover-panel')}


def run(output=ROOT/'docs/review/overlay-instances'):
 output=Path(output);output.mkdir(parents=True,exist_ok=True);errors=[];facts=[]
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start()
 try:
  with sync_playwright() as p:
   browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
   for slug,(root_attr,open_attr,last_attr) in SPECS.items():
    for case,preference,scale,theme in [('normal','no-preference',1,'light'),('zero','no-preference',0,'dark'),('reduce','reduce',2,'light')]:
     page=browser.new_page(viewport={'width':1000,'height':800},reduced_motion=preference)
     page.on('pageerror',lambda e:errors.append(str(e)));page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
     page.goto(f'http://127.0.0.1:{server.server_port}/tests/{slug}-multi.html',wait_until='networkidle')
     page.evaluate('([scale,theme])=>{document.documentElement.style.setProperty("--k-mscale",scale);document.documentElement.dataset.theme=theme}',[str(scale),theme])
     roots=page.locator(f'[{root_attr}]');triggers=page.locator(f'[{open_attr}]');assert roots.count()==3 and page.locator('[data-kata-ready]').count()==3
     ids=page.evaluate('()=>[...document.querySelectorAll("[id]")].map(e=>e.id)');assert len(ids)==len(set(ids))
     for index in range(3):
      root=roots.nth(index);trigger=triggers.nth(index);assert trigger.get_attribute('aria-controls')==(root.get_attribute('id') if slug!='popover' else root.locator(f'[{last_attr}]').get_attribute('id'))
      trigger.click()
      if slug!='popover':
       assert root.evaluate('(e)=>e.open');assert page.locator('dialog[open]').count()==1
       buttons=root.locator('button');buttons.last.focus();page.keyboard.press('Tab');assert buttons.first.evaluate('(e)=>document.activeElement===e')
       page.keyboard.press('Shift+Tab');assert buttons.last.evaluate('(e)=>document.activeElement===e')
       root.dispatch_event('compositionstart');page.keyboard.press('Escape');assert root.evaluate('(e)=>e.open');root.dispatch_event('compositionend')
       page.keyboard.press('Escape');page.wait_for_function('(e)=>!e.open',arg=root.element_handle());assert trigger.evaluate('(e)=>document.activeElement===e')
       trigger.click();page.mouse.click(5,5);page.wait_for_function('(e)=>!e.open',arg=root.element_handle())
       assert trigger.evaluate('(e)=>document.activeElement===e')
       trigger.click();root.locator(f'[{last_attr}]').first.click();assert not root.evaluate('(e)=>e.open')
      else:
       panel=root.locator(f'[{last_attr}]');assert trigger.get_attribute('aria-expanded')=='true' and not panel.evaluate('(e)=>e.hidden')
       root.dispatch_event('compositionstart');page.keyboard.press('Escape');assert trigger.get_attribute('aria-expanded')=='true';root.dispatch_event('compositionend')
       root.evaluate('(e)=>e.dispatchEvent(new KeyboardEvent("keydown",{key:"Escape",keyCode:229,bubbles:true}))');assert trigger.get_attribute('aria-expanded')=='true'
       page.keyboard.press('Escape');page.wait_for_function('(e)=>e.hidden',arg=panel.element_handle());assert trigger.evaluate('(e)=>document.activeElement===e')
       trigger.click();panel.locator('button').last.focus();page.keyboard.press('Tab');page.wait_for_function('(e)=>e.hidden',arg=panel.element_handle());assert not root.evaluate('(e)=>e.contains(document.activeElement)')
       trigger.click();root.evaluate('(e)=>{e.dispatchEvent(new FocusEvent("focusout",{bubbles:true,relatedTarget:document.querySelector("[data-outside]")}));e.querySelector("[data-popover-panel]").getAnimations().forEach(a=>a.pause())}');page.wait_for_function('(e)=>e.hidden',arg=panel.element_handle())
       trigger.click();page.locator('[data-outside]').click();panel.evaluate('(e)=>e.getAnimations().forEach(a=>a.pause())');page.wait_for_function('(e)=>e.hidden',arg=panel.element_handle());assert page.locator('[data-outside]').evaluate('(e)=>document.activeElement===e')
     assert roots.nth(2).evaluate('(e)=>getComputedStyle(e).direction')=='rtl'
     triggers.nth(2).click();page.screenshot(path=str(output/f'{slug}-{case}.png'));page.keyboard.press('Escape')
     # An appended instance with application-provided IDs also initializes on a subsequent load.
     preview=re.sub(r'<link[^>]*>','',(ROOT/f'components/{slug}/preview.html').read_text())
     page.evaluate('''([html,rootAttr,openAttr,slug])=>{const section=document.createElement('section');section.innerHTML=html;section.querySelector('['+rootAttr+']').id='existing-'+slug;section.querySelector('['+openAttr+']').id='existing-trigger-'+slug;document.body.append(section)}''',[preview,root_attr,open_attr,slug])
     page.add_script_tag(content=(ROOT/f'components/{slug}/{slug}.js').read_text());assert page.locator(f'[{root_attr}]').last.get_attribute('id')=='existing-'+slug
     page.locator(f'[{open_attr}]').last.click()
     if slug!='popover':assert page.locator(f'[{root_attr}]').last.evaluate('(e)=>e.open')
     else:assert page.locator(f'[{open_attr}]').last.get_attribute('aria-expanded')=='true'
     page.keyboard.press('Escape');assert page.locator(f'[{open_attr}]').last.get_attribute('id')=='existing-trigger-'+slug
     ids=page.evaluate('()=>[...document.querySelectorAll("[id]")].map(e=>e.id)');assert len(ids)==len(set(ids))
     facts.append({'component':slug,'case':case,'theme':theme,'inlineMultiplier':scale,'threeIndependent':True,'doubleLoad':True,'rtl':True,'uniqueIds':True,'existingIdsPreserved':True,'escapeAndOutside':True,'focusBehavior':True,'syntheticImeGuard':True})
     page.close()
   browser.close()
 finally:server.shutdown();server.server_close()
 assert not errors,errors
 (output/'results.json').write_text(json.dumps({'facts':facts,'errors':errors},indent=2)+'\n');print('3 components × 3 motion cases × 3 instances; focus/RTL/double load/IDs verified; no console errors')

if __name__=='__main__':run()
