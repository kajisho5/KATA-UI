"""Independent Split Panel, Reorder and Follow Frame behavior in real Chromium."""
import http.server
import json
import threading
from functools import partial
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SPECS = {'split-panel':'[data-split]', 'reorder':'[data-rank]', 'follow-frame':'[data-follow]'}
CASES = [('normal','light',1,'no-preference'),('zero','dark',0,'no-preference'),('reduce','dark',2,'reduce')]
EVENTS = ['kata-split-panel-change','kata-reorder-change']
# A seeded Math.random keeps re-rank scores reproducible between runs.
SEED = '''(()=>{let s=7;Math.random=()=>{s=(s*1103515245+12345)%2147483648;return s/2147483648};})();'''


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def count(page, root, kind, source=None):
    return page.evaluate('([id,type,source])=>window.events.filter(e=>e.root===id&&e.type===type&&(!source||e.detail.source===source)).length',[root.get_attribute('id'),kind,source])


def active(locator):
    return locator.evaluate('e=>e===document.activeElement')


def kfocus(page, locator):
    """Focus after a key press, so :focus-visible follows keyboard modality after earlier clicks."""
    page.keyboard.press('Shift');locator.focus();assert active(locator)


def outside(page, index, root):
    """Body clicks, null-relatedTarget focusout and window blur must not change a part."""
    page.locator('section').nth(index).locator('[data-probe]').click()
    root.evaluate('e=>{e.dispatchEvent(new FocusEvent("focusout",{bubbles:true,relatedTarget:null}));window.dispatchEvent(new Event("blur"))}')


def center(locator):
    box=locator.bounding_box();return box['x']+box['width']/2,box['y']+box['height']/2


def split_panel(page, root, index, facts):
    handle=root.locator('[data-split-h]');pane=root.locator('.k-split-a');now=lambda:handle.get_attribute('aria-valuenow')
    assert handle.get_attribute('role')=='separator' and handle.get_attribute('aria-controls')==pane.get_attribute('id')
    assert now()=='38' and abs(pane.evaluate('e=>e.getBoundingClientRect().width/e.parentElement.getBoundingClientRect().width*100')-38)<1.5
    kfocus(page,handle);assert handle.evaluate('e=>getComputedStyle(e).boxShadow')!='none'
    handle.evaluate('e=>e.dispatchEvent(new KeyboardEvent("keydown",{key:"ArrowRight",keyCode:229,bubbles:true}))');assert now()=='38'
    forward='ArrowLeft' if index==2 else 'ArrowRight'
    before=center(handle)[0];page.keyboard.press(forward);after=center(handle)[0]
    # The handle travels in the arrow's direction: right for ArrowRight, left for ArrowLeft in RTL.
    assert now()=='40' and ((after<before) if index==2 else (after>before))
    facts.append({'component':'split-panel','instance':index,'key':forward,'handleXBefore':before,'handleXAfter':after})
    page.keyboard.press('Shift+'+forward);assert now()=='50'
    page.keyboard.press('Home');assert now()=='20'
    page.keyboard.press('End');assert now()=='80'
    page.keyboard.press('ArrowUp');assert now()=='80'
    assert count(page,root,'kata-split-panel-change')==4
    box=root.bounding_box();x,y=center(handle)
    target=box['x']+box['width']*(0.7 if index==2 else 0.3)
    page.mouse.move(x,y);page.mouse.down();page.mouse.move((x+target)/2,y);page.mouse.move(target,y+40);page.mouse.up()
    assert abs(int(now())-30)<=2,now()
    assert count(page,root,'kata-split-panel-change')==5
    outside(page,index,root);assert abs(int(now())-30)<=2


def stacked(page):
    """A late-added copy with a horizontal handle stacks its panes and uses Up/Down."""
    page.evaluate('''()=>{const s=document.createElement('section');s.dataset.instance='stacked';s.innerHTML=document.querySelector('section[data-instance="0"]').innerHTML;
        s.querySelector('[data-split]').removeAttribute('data-kata-ready');s.querySelector('[data-split]').removeAttribute('id');s.querySelector('.k-split-a').removeAttribute('id');s.querySelector('.k-split-a').style.width='';
        s.querySelector('[data-split-h]').setAttribute('aria-orientation','horizontal');s.querySelector('[data-split-h]').setAttribute('aria-valuenow','38');s.querySelector('[data-split-h]').removeAttribute('aria-controls');document.body.append(s)}''')
    page.add_script_tag(content=(ROOT/'components/split-panel/split-panel.js').read_text())
    root=page.locator('section[data-instance="stacked"] [data-split]');handle=root.locator('[data-split-h]')
    assert 'k-split-v' in root.get_attribute('class') and root.evaluate('e=>getComputedStyle(e).flexDirection')=='column'
    kfocus(page,handle);page.keyboard.press('ArrowRight');assert handle.get_attribute('aria-valuenow')=='38'
    before=center(handle)[1];page.keyboard.press('ArrowDown');after=center(handle)[1]
    assert handle.get_attribute('aria-valuenow')=='40' and after>before
    page.keyboard.press('ArrowUp');page.keyboard.press('ArrowUp');assert handle.get_attribute('aria-valuenow')=='36'
    pane=root.locator('.k-split-a');assert abs(pane.evaluate('e=>e.getBoundingClientRect().height/e.parentElement.getBoundingClientRect().height*100')-36)<2


def rows(root):
    return root.evaluate('e=>[...e.children].map(li=>[li.querySelector(".no").textContent,[...li.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent).join("").trim(),li.querySelector(".val").textContent,li.dataset.score])')


def reorder(page, root, index, facts, reduce, scale):
    panel=root.locator('xpath=ancestor::*[contains(@class,"k-glass")][1]');button=panel.locator('[data-rank-btn]');pause=panel.locator('[data-rank-pause]')
    status=panel.locator('[role=status]');assert status.count()==1
    assert button.get_attribute('aria-controls')==root.get_attribute('id')==pause.get_attribute('aria-controls')
    kfocus(page,button);assert button.evaluate('e=>getComputedStyle(e).boxShadow')!='none'
    # Keyboard focus inside the panel pauses autoplay for this list only.
    autos=count(page,root,'kata-reorder-change','auto');page.clock.run_for(6100);assert count(page,root,'kata-reorder-change','auto')==autos
    page.keyboard.press('Enter');result=rows(root)
    assert [r[0] for r in result]==['1','2','3','4'] and all(r[2]==r[3] for r in result)
    assert [int(r[3]) for r in result]==sorted((int(r[3]) for r in result),reverse=True)
    assert status.inner_text()=='Re-ranked. First: '+result[0][1]+'.' and count(page,root,'kata-reorder-change','button')==1
    animations=page.evaluate('()=>document.getAnimations().filter(a=>a.effect&&a.effect.target&&a.effect.target.closest&&a.effect.target.closest("[data-rank]")).length')
    if scale==0 or reduce=='reduce':assert animations==0,animations
    facts.append({'component':'reorder','instance':index,'case':(scale,reduce),'animationsAfterManualRerank':animations})
    pause.click();assert pause.get_attribute('aria-pressed')=='true'
    outside(page,index,root);page.mouse.move(1,1)
    autos=count(page,root,'kata-reorder-change','auto');page.clock.run_for(6100);assert count(page,root,'kata-reorder-change','auto')==autos
    kfocus(page,pause);page.keyboard.press('Space');assert pause.get_attribute('aria-pressed')=='false'
    outside(page,index,root);page.mouse.move(1,1)
    autos=count(page,root,'kata-reorder-change','auto');page.clock.run_for(6100)
    assert count(page,root,'kata-reorder-change','auto')==(autos if reduce=='reduce' else autos+2)


def follow_frame(page, root, index, reduce, scale):
    frame=root.locator('[data-frame]');tag=root.locator('[data-frame-tag]')
    pos=lambda:frame.evaluate('e=>[parseFloat(e.style.left),parseFloat(e.style.top)]')
    mid=root.evaluate('e=>[e.clientWidth/2,e.clientHeight/2]');assert pos()==mid
    box=root.bounding_box();page.mouse.move(box['x']+100,box['y']+60)
    if reduce=='reduce':page.wait_for_timeout(200);assert pos()==mid
    elif scale==0:assert pos()==[100,60]
    else:
        page.wait_for_function('(e)=>parseFloat(e.querySelector("[data-frame]").style.left)===100&&parseFloat(e.querySelector("[data-frame]").style.top)===60',arg=root.element_handle(),timeout=4000)
        settled=pos();page.wait_for_timeout(100);assert pos()==settled
    assert tag.evaluate('e=>[parseFloat(e.style.left),parseFloat(e.style.top)]')==pos()
    others=[i for i in range(3) if i!=index]
    for other in others:
        zone=page.locator('[data-follow]').nth(other)
        assert zone.locator('[data-frame]').evaluate('e=>[parseFloat(e.style.left),parseFloat(e.style.top)]')==zone.evaluate('e=>[e.clientWidth/2,e.clientHeight/2]')
    page.mouse.move(1,1)
    if scale==0 or reduce=='reduce':assert pos()==mid
    else:page.wait_for_function('([e,m])=>parseFloat(e.querySelector("[data-frame]").style.left)===m[0]',arg=[root.element_handle(),mid],timeout=4000)
    root.evaluate('e=>e.style.maxWidth="300px"');page.wait_for_function('(e)=>parseFloat(e.querySelector("[data-frame]").style.left)===e.clientWidth/2',arg=root.element_handle(),timeout=2000)
    root.evaluate('e=>e.style.maxWidth="430px"')


def run(output=ROOT/'docs/review/split-reorder-follow'):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    facts,errors,arrows=[],[],[]
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
            for slug,selector in SPECS.items():
                for case,theme,scale,reduce in CASES:
                    page=browser.new_page(viewport={'width':1100,'height':1000},reduced_motion=reduce)
                    if slug=='reorder':page.clock.install()
                    page.add_init_script(SEED+'''window.globalRegistrations=[];
                        for(const target of [document,window]){
                            const original=target.addEventListener;
                            target.addEventListener=function(type,...args){
                                // Playwright installs its own pointer hit-target interceptor.
                                const stack=new Error().stack;
                                if(['keydown','blur','resize','pointerdown','pointermove','scroll'].includes(type)&&!stack.includes('InjectedScript'))window.globalRegistrations.push({type,source:document.currentScript?.src||null});
                                return original.call(this,type,...args);
                            };
                        }''')
                    page.on('pageerror',lambda error:errors.append(str(error)))
                    page.on('console',lambda message:errors.append(message.text) if message.type=='error' else None)
                    page.goto(f'http://127.0.0.1:{server.server_port}/tests/{slug}-multi.html')
                    page.evaluate('([theme,scale])=>{document.documentElement.dataset.theme=theme;document.documentElement.style.setProperty("--k-mscale",scale)}',[theme,scale])
                    page.evaluate('(types)=>{window.events=[];for(const type of types)document.addEventListener(type,event=>window.events.push({type,root:event.target.id,detail:event.detail}))}',EVENTS)
                    roots=page.locator(selector);assert roots.count()==3
                    if slug=='reorder':
                        # Autoplay runs independently in every copy, and never with reduced motion.
                        page.mouse.move(1,1);page.clock.run_for(3100)
                        autos=[count(page,roots.nth(i),'kata-reorder-change','auto') for i in range(3)]
                        assert autos==([0,0,0] if reduce=='reduce' else [1,1,1]),autos
                    for index in range(3):
                        root=roots.nth(index)
                        before=[roots.nth(o).evaluate('e=>e.outerHTML') for o in range(index+1,3)] if slug!='reorder' else None
                        if slug=='split-panel':split_panel(page,root,index,arrows)
                        elif slug=='reorder':reorder(page,root,index,arrows,reduce,scale)
                        else:follow_frame(page,root,index,reduce,scale)
                        # No operation may mutate an untouched later copy (Reorder copies autoplay on their own).
                        if before is not None:
                            assert before==[roots.nth(o).evaluate('e=>e.outerHTML') for o in range(index+1,3)]
                    if slug=='split-panel':stacked(page)
                    page.add_script_tag(content=(ROOT/f'components/{slug}/{slug}.js').read_text())
                    assert roots.nth(1).get_attribute('id')=='existing-'+slug+'-root'
                    if slug=='reorder':assert page.locator('.k-rank-status').count()==3
                    ids=page.evaluate('()=>[...document.querySelectorAll("[id]")].map(e=>e.id)');assert len(ids)==len(set(ids))
                    registrations=page.evaluate('window.globalRegistrations');assert not registrations,registrations
                    if slug=='reorder':page.clock.run_for(1000)
                    else:page.wait_for_timeout(400)
                    page.screenshot(path=str(output/f'{slug}-{case}.png'),full_page=True)
                    facts.append({'component':slug,'case':case,'theme':theme,'mscale':scale,'reducedMotion':reduce,'threeIndependent':True,'doubleLoad':True,'rtl':True,'uniqueIds':True,'existingIdsPreserved':True,'nullFocusoutAndBodyClickSafe':True,'keyboard':slug!='follow-frame','globalListeners':0})
                    page.close()
            browser.close()
    finally:server.shutdown();server.server_close()
    assert not errors,errors
    (output/'results.json').write_text(json.dumps({'cases':facts,'positions':arrows,'consoleErrors':errors,'unverified':['Real Japanese IME','Screen readers','Firefox','Safari','Touch dragging on real devices']},indent=2)+'\n')
    print('Split Panel / Reorder / Follow Frame: 9 Chromium cases; independent triple instances, RTL, double load, events and keyboard passed; console errors 0')
    return facts

if __name__=='__main__':run()
