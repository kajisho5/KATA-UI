"""Independent File Upload, Color Picker and Carousel behavior in real Chromium."""
import http.server
import json
import threading
from functools import partial
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SPECS = {'file-upload':'[data-upload]', 'color-picker':'[data-cp]', 'carousel':'.k-car'}
CASES = [('normal','light',1,'no-preference'),('zero','dark',0,'no-preference'),('reduce','dark',2,'reduce')]
CHOOSERS = []
EVENTS = ['kata-file-upload-add','kata-file-upload-remove','kata-color-picker-change','kata-carousel-change']


def count(page, root, kind):
    return page.evaluate('([id,type])=>window.events.filter(e=>e.root===id&&e.type===type).length',[root.get_attribute('id'),kind])


def active(locator):
    return locator.evaluate('e=>e===document.activeElement')


def kfocus(page, locator):
    """Focus after a key press, so :focus-visible follows keyboard modality after earlier clicks."""
    page.keyboard.press('Shift');locator.focus();assert active(locator)


def outside(page, index, root):
    """Body clicks, null-relatedTarget focusout and window blur must not change a part."""
    page.locator('section').nth(index).locator('[data-probe]').click()
    root.evaluate('e=>{e.dispatchEvent(new FocusEvent("focusout",{bubbles:true,relatedTarget:null}));window.dispatchEvent(new Event("blur"))}')


def file_upload(page, root, index, facts):
    zone=root.locator('.k-up-zone');input_=root.locator('input[type=file]');items=root.locator('.k-up-item')
    assert items.count()==1 and root.locator('[role=status]').count()==1
    assert input_.get_attribute('hidden') is None and input_.evaluate('e=>e.tabIndex')==0
    kfocus(page,input_)
    assert zone.evaluate('e=>getComputedStyle(e).boxShadow')!='none'
    # Space on the focused input must open a multiple-file chooser (handled and closed in run()).
    opened=len(CHOOSERS);page.keyboard.press('Space')
    for _ in range(40):
        if len(CHOOSERS)>opened:break
        page.wait_for_timeout(50)
    assert CHOOSERS[opened:]==[True] and items.count()==1
    assert root.locator('.rm').first.get_attribute('aria-label')=='Remove q3-board-deck.pdf'
    input_.set_input_files([{'name':'brief.pdf','mimeType':'application/pdf','buffer':b'x'*2048},{'name':'<img src=x onerror=alert(1)>.png','mimeType':'image/png','buffer':b'y'*3000000}])
    assert items.count()==3 and root.locator('img').count()==0
    assert root.locator('[role=status]').inner_text()=='Added 2 files: brief.pdf, <img src=x onerror=alert(1)>.png.'
    assert items.nth(1).locator('.sz').inner_text()=='2 KB' and items.nth(2).locator('.sz').inner_text()=='2.9 MB'
    assert items.nth(1).locator('.rm').get_attribute('aria-label')=='Remove brief.pdf'
    assert items.nth(1).locator('.rm svg').count()==1
    assert count(page,root,'kata-file-upload-add')==1
    root.locator('.rm').first.click()
    assert items.count()==2 and active(items.first.locator('.rm'))
    assert root.locator('[role=status]').inner_text()=='Removed q3-board-deck.pdf.'
    items.first.locator('.rm').focus();page.keyboard.press('Enter');page.keyboard.press('Enter')
    assert items.count()==0 and active(input_) and count(page,root,'kata-file-upload-remove')==3
    # Drag state belongs to one zone and survives entering a child element.
    zone.dispatch_event('dragenter');zone.locator('.ic').dispatch_event('dragenter');zone.dispatch_event('dragleave')
    assert 'drag' in zone.get_attribute('class')
    assert page.evaluate('()=>document.querySelectorAll(".k-up-zone.drag").length')==1
    zone.evaluate('e=>{const data=new DataTransfer();data.items.add(new File(["z"],"dropped.txt"));e.dispatchEvent(new DragEvent("drop",{bubbles:true,cancelable:true,dataTransfer:data}))}')
    assert 'drag' not in zone.get_attribute('class') and items.count()==1 and items.first.locator('.nm').inner_text()=='dropped.txt'
    assert count(page,root,'kata-file-upload-add')==2
    outside(page,index,root);assert items.count()==1


def color_picker(page, root, index, facts):
    swatches=root.locator('.k-cp-sw');value=lambda:root.get_attribute('data-value')
    assert root.get_by_role('radiogroup',name='Brand color').count()==1
    assert [s.get_attribute('tabindex') for s in swatches.all()]==['0']+['-1']*7
    assert value()=='#30A3BB' and root.locator('[data-cp-hex]').inner_text()=='#30A3BB'
    kfocus(page,swatches.first)
    style=swatches.first.evaluate('e=>[getComputedStyle(e).outlineStyle,getComputedStyle(e).boxShadow]')
    assert style[0]=='solid' and style[1]!='none',style
    swatches.first.evaluate('e=>e.dispatchEvent(new KeyboardEvent("keydown",{key:"ArrowRight",keyCode:229,bubbles:true}))')
    assert value()=='#30A3BB'
    forward='ArrowLeft' if index==2 else 'ArrowRight'
    before=swatches.first.evaluate('e=>e.getBoundingClientRect().left');page.keyboard.press(forward)
    after=swatches.nth(1).evaluate('e=>e.getBoundingClientRect().left')
    assert active(swatches.nth(1)) and swatches.nth(1).get_attribute('aria-checked')=='true' and swatches.first.get_attribute('aria-checked')=='false'
    assert (after<before) if index==2 else (after>before)
    facts.append({'component':'color-picker','instance':index,'key':forward,'beforeLeft':before,'afterLeft':after})
    assert value()=='#1F54A3' and [s.get_attribute('tabindex') for s in swatches.all()].count('0')==1
    page.keyboard.press('ArrowUp');assert active(swatches.first) and value()=='#30A3BB'
    page.keyboard.press('End');assert active(swatches.last) and value()=='#1C1C1C'
    page.keyboard.press('Home');assert active(swatches.first)
    page.keyboard.press('ArrowUp');assert active(swatches.last)
    assert count(page,root,'kata-color-picker-change')==5
    swatches.nth(3).click();swatches.nth(3).click();page.keyboard.press('Space')
    assert swatches.nth(3).get_attribute('aria-checked')=='true' and count(page,root,'kata-color-picker-change')==6
    custom=root.locator('[data-cp-custom]')
    custom.evaluate('e=>{e.value="#12ab34";e.dispatchEvent(new Event("input",{bubbles:true}))}')
    assert value()=='#12AB34' and count(page,root,'kata-color-picker-change')==6
    custom.evaluate('e=>e.dispatchEvent(new Event("change",{bubbles:true}))')
    assert count(page,root,'kata-color-picker-change')==7 and root.locator('[aria-checked=true]').count()==0
    assert [s.get_attribute('tabindex') for s in swatches.all()]==['0']+['-1']*7
    kfocus(page,custom);assert root.locator('.k-cp-custom').evaluate('e=>getComputedStyle(e).boxShadow')!='none'
    outside(page,index,root);assert value()=='#12AB34'


def carousel(page, root, index, facts, scale, reduce):
    track=root.locator('[data-car-track]');slides=track.locator('.k-car-slide');dots=root.locator('[data-car-dot]')
    instant=scale==0 or reduce=='reduce'
    assert root.get_attribute('role')=='group' and root.get_attribute('aria-label')=='Highlights'
    assert [s.get_attribute('aria-label') for s in slides.all()]==['1 of 3','2 of 3','3 of 3']
    current=lambda:[d.get_attribute('aria-current') for d in dots.all()].index('true')
    def at(i):
        page.wait_for_function('([id,i])=>{const r=document.getElementById(id),d=r.querySelectorAll("[data-car-dot]");return d[i].getAttribute("aria-current")==="true"}',arg=[root.get_attribute('id'),i],timeout=4000)
    if index==2:assert root.locator('.k-car-btn svg').first.evaluate('e=>getComputedStyle(e).transform')!='none'
    kfocus(page,track);assert track.evaluate('e=>getComputedStyle(e).boxShadow')!='none'
    forward='ArrowLeft' if index==2 else 'ArrowRight'
    before=slides.nth(1).evaluate('e=>e.getBoundingClientRect().left');page.keyboard.press(forward)
    if instant:assert track.evaluate('e=>e.scrollLeft')!=0,'zero motion must move at once'
    at(1)
    # Wait for smooth scrolling to settle: slide 2's inline-start edge meets the track's.
    page.wait_for_function('''(id)=>{const t=document.getElementById(id).querySelector("[data-car-track]"),s=t.children[1],side=getComputedStyle(t).direction==="rtl"?"right":"left";return Math.abs(t.getBoundingClientRect()[side]-s.getBoundingClientRect()[side])<2}''',arg=root.get_attribute('id'),timeout=4000)
    after=slides.nth(1).evaluate('e=>e.getBoundingClientRect().left')
    assert (after>before) if index==2 else (after<before)
    facts.append({'component':'carousel','instance':index,'key':forward,'slide2LeftBefore':before,'slide2LeftAfter':after})
    settled=lambda n:page.wait_for_function('([id,n])=>window.events.filter(e=>e.root===id&&e.type==="kata-carousel-change").length===n',arg=[root.get_attribute('id'),n],timeout=4000)
    settled(1);assert root.locator('[role=status]').inner_text()=='Slide 2 of 3'
    root.locator('[data-car-next]').click();at(2);settled(2)
    root.locator('[data-car-prev]').click();at(1);settled(3)
    dots.first.click();at(0);settled(4)
    track.focus();page.keyboard.press('End');at(2);settled(5);page.keyboard.press('Home');at(0)
    track.evaluate('e=>e.dispatchEvent(new KeyboardEvent("keydown",{key:"ArrowRight",keyCode:229,bubbles:true}))');page.wait_for_timeout(50);assert current()==0
    # One settled change per move: 1, 2, 1, 0, 2, 0 (no reports for slides passed on the way).
    page.wait_for_function('(id)=>window.events.filter(e=>e.root===id&&e.type==="kata-carousel-change").length>=6',arg=root.get_attribute('id'),timeout=4000)
    page.wait_for_timeout(300)
    assert page.evaluate('(id)=>window.events.filter(e=>e.root===id&&e.type==="kata-carousel-change").map(e=>e.detail.index)',root.get_attribute('id'))==[1,2,1,0,2,0]
    outside(page,index,root);page.wait_for_timeout(50);assert current()==0


def run(output=ROOT/'docs/review/upload-color-carousel'):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    facts,errors,arrows=[],[],[]
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
            for slug,selector in SPECS.items():
                for case,theme,scale,reduce in CASES:
                    page=browser.new_page(viewport={'width':1100,'height':1000},reduced_motion=reduce)
                    page.add_init_script('''window.globalRegistrations=[];
                        for(const target of [document,window]){
                            const original=target.addEventListener;
                            target.addEventListener=function(type,...args){
                                // Playwright installs its own pointer hit-target interceptor.
                                const stack=new Error().stack;
                                if(['keydown','blur','resize','pointerdown','scroll','dragover','drop'].includes(type)&&!stack.includes('InjectedScript'))window.globalRegistrations.push({type,source:document.currentScript?.src||null});
                                return original.call(this,type,...args);
                            };
                        }''')
                    page.on('pageerror',lambda error:errors.append(str(error)))
                    page.on('console',lambda message:errors.append(message.text) if message.type=='error' else None)
                    page.on('filechooser',lambda chooser:(CHOOSERS.append(chooser.is_multiple()),chooser.set_files([])))
                    page.on('dialog',lambda dialog:(errors.append('dialog: '+dialog.message),dialog.dismiss()))
                    page.goto(f'http://127.0.0.1:{server.server_port}/tests/{slug}-multi.html')
                    page.evaluate('([theme,scale])=>{document.documentElement.dataset.theme=theme;document.documentElement.style.setProperty("--k-mscale",scale)}',[theme,scale])
                    page.evaluate('(types)=>{window.events=[];for(const type of types)document.addEventListener(type,event=>window.events.push({type,root:event.target.id,detail:event.detail}))}',EVENTS)
                    roots=page.locator(selector);assert roots.count()==3
                    for index in range(3):
                        root=roots.nth(index)
                        if slug=='file-upload':file_upload(page,root,index,arrows)
                        elif slug=='color-picker':color_picker(page,root,index,arrows)
                        else:carousel(page,root,index,arrows,scale,reduce)
                        # No operation may mutate an untouched later copy.
                        for other in range(index+1,3):
                            sibling=roots.nth(other)
                            if slug=='file-upload':assert sibling.locator('.k-up-item').count()==1
                            elif slug=='color-picker':assert sibling.get_attribute('data-value')=='#30A3BB'
                            else:assert sibling.locator('[data-car-dot]').first.get_attribute('aria-current')=='true' and sibling.locator('[data-car-track]').evaluate('e=>e.scrollLeft')==0
                    page.add_script_tag(content=(ROOT/f'components/{slug}/{slug}.js').read_text())
                    assert roots.nth(1).get_attribute('id')=='existing-'+slug+'-root'
                    assert all(roots.nth(i).locator('[role=status]').count()<=1 for i in range(3))
                    ids=page.evaluate('()=>[...document.querySelectorAll("[id]")].map(e=>e.id)');assert len(ids)==len(set(ids))
                    registrations=page.evaluate('window.globalRegistrations');assert not registrations,registrations
                    page.wait_for_timeout(400)  # let state transitions finish before capture
                    page.screenshot(path=str(output/f'{slug}-{case}.png'),full_page=True)
                    facts.append({'component':slug,'case':case,'theme':theme,'mscale':scale,'reducedMotion':reduce,'threeIndependent':True,'doubleLoad':True,'rtl':True,'uniqueIds':True,'existingIdsPreserved':True,'nullFocusoutAndBodyClickSafe':True,'keyboard':True,'eventsCounted':True,'globalListeners':0})
                    page.close()
            browser.close()
    finally:server.shutdown();server.server_close()
    assert not errors,errors
    (output/'results.json').write_text(json.dumps({'cases':facts,'horizontalPositions':arrows,'consoleErrors':errors,'unverified':['Real Japanese IME','Screen readers','Firefox','Safari','Native file and color pickers on mobile','Real drag and drop from the operating system']},indent=2)+'\n')
    print('File Upload / Color Picker / Carousel: 9 Chromium cases; independent triple instances, RTL, double load, events and keyboard passed; console errors 0')
    return facts

if __name__=='__main__':run()
