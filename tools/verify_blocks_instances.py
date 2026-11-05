"""Independent Pricing, Site Header and Use Cases blocks in real Chromium."""
import http.server
import json
import threading
from functools import partial
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SPECS = {'pricing':'.pricing', 'site-header':'.k-hdr', 'use-cases':'.k-uc'}
CASES = [('normal','light',1,'no-preference'),('zero','dark',0,'no-preference'),('reduce','dark',2,'reduce')]
EVENTS = ['kata-use-cases-change']
MONTHLY, YEARLY = ['$9','$29','$79'], ['$7','$23','$63']


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def count(page, root, kind):
    return page.evaluate('([id,type])=>window.events.filter(e=>e.root===id&&e.type===type).length',[root.get_attribute('id'),kind])


def active(locator):
    return locator.evaluate('e=>e===document.activeElement')


def kfocus(page, locator):
    """Focus after a key press, so :focus-visible follows keyboard modality after earlier clicks."""
    page.keyboard.press('Shift');locator.focus();assert active(locator)


def quiet_outside(root):
    """Null-relatedTarget focusout and window blur must not change a part."""
    root.evaluate('e=>{e.dispatchEvent(new FocusEvent("focusout",{bubbles:true,relatedTarget:null}));window.dispatchEvent(new Event("blur"))}')


def prices(root):
    return [a.inner_text() for a in root.locator('[data-m]').all()]


def pricing(page, root, index):
    toggle=root.locator('[data-billing]');status=root.locator('[role=status]')
    assert prices(root)==MONTHLY and status.count()==1
    assert page.get_by_role('checkbox',name='Yearly billing').count()==3
    root.evaluate('e=>{window.changes=0;e.addEventListener("change",()=>window.changes++)}')
    kfocus(page,toggle);assert root.locator('.tr').evaluate('e=>getComputedStyle(e).boxShadow')!='none'
    page.keyboard.press('Space')
    assert toggle.is_checked() and prices(root)==YEARLY and status.inner_text()=='Showing yearly prices.'
    assert page.evaluate('window.changes')==1
    root.locator('.switch').click();assert prices(root)==MONTHLY and status.inner_text()=='Showing monthly prices.'
    root.locator('.switch').click();assert prices(root)==YEARLY
    page.locator('section[data-instance]').nth(index).locator('[data-probe]').click();quiet_outside(root)
    assert prices(root)==YEARLY


def site_header(page, root, index):
    button=root.locator('[data-hdr-btn]');panel=root.locator('[data-hdr-panel]');expanded=lambda:button.get_attribute('aria-expanded')
    assert button.get_attribute('aria-controls')==panel.get_attribute('id') and expanded()=='false' and not panel.is_visible()
    kfocus(page,button);assert button.evaluate('e=>getComputedStyle(e).boxShadow')!='none'
    page.keyboard.press('Enter');assert expanded()=='true' and panel.is_visible()
    page.keyboard.press('Tab');assert active(panel.locator('a').first)
    assert panel.locator('a').first.evaluate('e=>getComputedStyle(e).boxShadow')!='none'
    quiet_outside(root);assert expanded()=='true'
    root.evaluate('e=>e.dispatchEvent(new KeyboardEvent("keydown",{key:"Escape",keyCode:229,bubbles:true}))');assert expanded()=='true'
    page.keyboard.press('Escape');assert expanded()=='false' and not panel.is_visible() and active(button)
    button.click();assert expanded()=='true'
    page.locator('section[data-instance]').nth(index).locator('[data-probe]').click();assert expanded()=='false'
    button.click();panel.locator('a').nth(1).click();assert expanded()=='false'
    # Opening another header's menu is an outside press for this one.
    # A press inside another header is outside this one. (Closing this panel shifts the
    # layout, so the press and the other header's own click are checked separately.)
    button.click();other=page.locator('.k-hdr').nth((index+1)%3).locator('[data-hdr-btn]')
    other.dispatch_event('pointerdown');assert expanded()=='false' and other.get_attribute('aria-expanded')=='false'
    other.click();assert other.get_attribute('aria-expanded')=='true' and expanded()=='false'
    other.click();assert other.get_attribute('aria-expanded')=='false'


def use_cases(page, root, index):
    rows=root.locator('[data-uc-row]');scenes=root.locator('[data-uc-scene]')
    state=lambda:([r.get_attribute('aria-expanded') for r in rows.all()],[not s.is_hidden() for s in scenes.all()])
    assert state()==(['true','false','false','false'],[True,False,False,False])
    assert all(rows.nth(i).get_attribute('aria-controls')==scenes.nth(i).get_attribute('id') for i in range(4))
    kfocus(page,rows.first);assert rows.first.evaluate('e=>getComputedStyle(e).outlineStyle')=='solid'
    rows.first.evaluate('e=>e.dispatchEvent(new KeyboardEvent("keydown",{key:"ArrowDown",keyCode:229,bubbles:true}))');assert active(rows.first)
    page.keyboard.press('ArrowDown');assert active(rows.nth(1)) and state()[0][0]=='true'
    page.keyboard.press('Enter');assert state()==(['false','true','false','false'],[False,True,False,False])
    page.keyboard.press('End');assert active(rows.nth(3));page.keyboard.press('ArrowDown');assert active(rows.first)
    page.keyboard.press('ArrowUp');assert active(rows.nth(3));page.keyboard.press('Home');assert active(rows.first)
    rows.nth(2).click();assert state()==(['false','false','true','false'],[False,False,True,False])
    rows.nth(2).click();assert count(page,root,'kata-use-cases-change')==2
    page.locator('section[data-instance]').nth(index).locator('[data-probe]').click();quiet_outside(root)
    assert state()[0]==['false','false','true','false']


def snapshot(page, roots, index, slug):
    out=[]
    for other in range(index+1,3):
        root=roots.nth(other)
        if slug=='pricing':out.append(prices(root))
        elif slug=='site-header':out.append(root.locator('[data-hdr-btn]').get_attribute('aria-expanded'))
        else:out.append([r.get_attribute('aria-expanded') for r in root.locator('[data-uc-row]').all()])
    return out


def run(output=ROOT/'docs/review/blocks-instances'):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    facts,errors=[],[]
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
            for slug,selector in SPECS.items():
                for case,theme,scale,reduce in CASES:
                    width=600 if slug=='site-header' else 1100
                    page=browser.new_page(viewport={'width':width,'height':1000},reduced_motion=reduce)
                    page.add_init_script('''window.globalRegistrations=[];
                        for(const target of [document,window]){
                            const original=target.addEventListener;
                            target.addEventListener=function(type,...args){
                                // Playwright installs its own pointer hit-target interceptor.
                                const stack=new Error().stack;
                                if(['keydown','blur','resize','pointerdown','click','scroll'].includes(type)&&!stack.includes('InjectedScript'))window.globalRegistrations.push({type,target:target===document?'document':'window'});
                                return original.call(this,type,...args);
                            };
                        }''')
                    page.on('pageerror',lambda error:errors.append(str(error)))
                    page.on('console',lambda message:errors.append(message.text) if message.type=='error' else None)
                    page.goto(f'http://127.0.0.1:{server.server_port}/tests/{slug}-multi.html')
                    page.evaluate('([theme,scale])=>{document.documentElement.dataset.theme=theme;document.documentElement.style.setProperty("--k-mscale",scale)}',[theme,scale])
                    page.evaluate('(types)=>{window.events=[];for(const type of types)document.addEventListener(type,event=>window.events.push({type,root:event.target.id,detail:event.detail}))}',EVENTS)
                    roots=page.locator(selector);assert roots.count()==3
                    expected=[{'type':'pointerdown','target':'document'}] if slug=='site-header' else []
                    # Only Site Header needs a document listener, and only one for every header.
                    assert page.evaluate('window.globalRegistrations')==expected,page.evaluate('window.globalRegistrations')
                    for index in range(3):
                        root=roots.nth(index);before=snapshot(page,roots,index,slug)
                        if slug=='pricing':pricing(page,root,index)
                        elif slug=='site-header':site_header(page,root,index)
                        else:use_cases(page,root,index)
                        # No operation may leave an untouched later copy changed.
                        assert snapshot(page,roots,index,slug)==before
                    page.add_script_tag(content=(ROOT/f'blocks/{slug}/{slug}.js').read_text())
                    assert roots.nth(1).get_attribute('id')=='existing-'+slug+'-root'
                    ids=page.evaluate('()=>[...document.querySelectorAll("[id]")].map(e=>e.id)');assert len(ids)==len(set(ids))
                    assert page.evaluate('window.globalRegistrations')==expected
                    page.wait_for_timeout(400)
                    page.screenshot(path=str(output/f'{slug}-{case}.png'),full_page=True)
                    facts.append({'component':slug,'case':case,'theme':theme,'mscale':scale,'reducedMotion':reduce,'viewportWidth':width,'threeIndependent':True,'doubleLoad':True,'rtl':True,'uniqueIds':True,'existingIdsPreserved':True,'nullFocusoutAndBlurSafe':True,'keyboard':True,'documentListeners':len(expected)})
                    page.close()
            browser.close()
    finally:server.shutdown();server.server_close()
    assert not errors,errors
    (output/'results.json').write_text(json.dumps({'cases':facts,'consoleErrors':errors,'unverified':['Real Japanese IME','Screen readers','Firefox','Safari','Touch on real devices']},indent=2)+'\n')
    print('Pricing / Site Header / Use Cases: 9 Chromium cases; independent triple instances, RTL, double load and keyboard passed; console errors 0')
    return facts

if __name__=='__main__':run()
