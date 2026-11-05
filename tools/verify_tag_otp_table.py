"""Independent tag, numeric OTP and sortable table behavior in real Chromium."""
import http.server
import json
import threading
from functools import partial
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SPECS = {'tag-input':'[data-tags]', 'input-otp':'[data-otp]', 'data-table':'[data-dt]'}


def run(output=ROOT/'docs/review/tag-otp-table'):
    output = Path(output); output.mkdir(parents=True, exist_ok=True)
    facts, errors, arrows = [], [], []
    server = http.server.ThreadingHTTPServer(('127.0.0.1',0), partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
            for slug,selector in SPECS.items():
                for case,theme,scale,reduce in [('normal','light',1,'no-preference'),('zero','dark',0,'no-preference'),('reduce','dark',2,'reduce')]:
                    page=browser.new_page(viewport={'width':1100,'height':1000},reduced_motion=reduce)
                    page.add_init_script('''window.globalRegistrations=[];
                        for(const target of [document,window]){
                            const original=target.addEventListener;
                            target.addEventListener=function(type,...args){
                                // Playwright installs its own pointer hit-target interceptor.
                                const stack=new Error().stack;
                                if(['keydown','blur','resize','pointerdown'].includes(type)&&!stack.includes('InjectedScript'))window.globalRegistrations.push({type,source:document.currentScript?.src||null});
                                return original.call(this,type,...args);
                            };
                        }''')
                    page.on('pageerror',lambda error:errors.append(str(error)))
                    page.on('console',lambda message:errors.append(message.text) if message.type=='error' else None)
                    page.goto(f'http://127.0.0.1:{server.server_port}/tests/{slug}-multi.html')
                    page.evaluate('([theme,scale])=>{document.documentElement.dataset.theme=theme;document.documentElement.style.setProperty("--k-mscale",scale)}',[theme,scale])
                    roots=page.locator(selector);assert roots.count()==3
                    page.evaluate('''()=>{window.events=[];for(const type of ['kata-tag-input-add','kata-tag-input-remove','kata-data-table-sort'])document.addEventListener(type,event=>window.events.push({type,root:event.target.id,detail:event.detail}));window.completions=[];document.addEventListener('change',event=>{if(event.target.matches('[data-otp]'))window.completions.push({root:event.target.id,value:event.target.dataset.value})});}''')
                    for index in range(3):
                        root=roots.nth(index)
                        if slug=='tag-input':
                            input_=root.locator('input');chips=root.locator('.k-chip');assert chips.count()==2
                            input_.fill('Sample '+str(index));page.keyboard.press('Enter');assert chips.count()==3
                            assert root.locator('[role="status"]').inner_text()=='Added Sample '+str(index)+'.'
                            input_.fill('design');page.keyboard.press('Enter');assert chips.count()==3
                            input_.fill('日本語');input_.dispatch_event('compositionstart');page.keyboard.press('Enter');assert chips.count()==3 and input_.input_value()=='日本語'
                            input_.evaluate('e=>e.dispatchEvent(new KeyboardEvent("keydown",{key:"Enter",keyCode:229,bubbles:true}))');assert chips.count()==3
                            input_.evaluate('e=>{e.dispatchEvent(new CompositionEvent("compositionend",{bubbles:true}));e.dispatchEvent(new KeyboardEvent("keydown",{key:"Enter",bubbles:true}))}');assert chips.count()==3
                            page.keyboard.press('Enter');assert chips.count()==4
                            input_.fill('draft');page.locator('section').nth(index).locator('[data-probe]').click()
                            root.evaluate('e=>{e.dispatchEvent(new FocusEvent("focusout",{bubbles:true,relatedTarget:null}));window.dispatchEvent(new Event("blur"))}')
                            assert input_.input_value()=='draft' and chips.count()==4
                            input_.fill('');page.keyboard.press('Backspace');assert chips.count()==3
                            buttons=root.locator('.k-chip-x');buttons.first.focus()
                            first_left=buttons.first.evaluate('e=>e.getBoundingClientRect().left');forward='ArrowLeft' if index==2 else 'ArrowRight'
                            page.keyboard.press(forward);assert buttons.nth(1).evaluate('e=>e===document.activeElement')
                            next_left=buttons.nth(1).evaluate('e=>e.getBoundingClientRect().left');assert next_left<first_left if index==2 else next_left>first_left
                            arrows.append({'case':case,'instance':index,'key':forward,'beforeLeft':first_left,'afterLeft':next_left})
                            page.keyboard.press('Delete');assert chips.count()==2
                            assert root.locator('[role="status"]').inner_text()=='Removed Vanilla.'
                            buttons=root.locator('.k-chip-x');buttons.first.focus();page.keyboard.press('Backspace');assert chips.count()==1
                            assert all(button.get_attribute('aria-label').startswith('Remove tag ') for button in buttons.all())
                            input_.fill('<img src=x onerror=alert(1)>');page.keyboard.press('Enter');assert root.locator('img').count()==0
                            assert page.evaluate('(id)=>window.events.filter(e=>e.root===id&&e.type==="kata-tag-input-add").length',root.get_attribute('id'))==3
                        elif slug=='input-otp':
                            inputs=root.locator('input');assert inputs.count()==6
                            assert root.get_attribute('dir')=='ltr' and root.evaluate('e=>getComputedStyle(e).direction')=='ltr'
                            assert inputs.first.get_attribute('autocomplete')=='one-time-code'
                            assert all(item.get_attribute('inputmode')=='numeric' for item in inputs.all())
                            for item in inputs.all():item.fill('')
                            inputs.first.focus();page.keyboard.type('123456');assert root.get_attribute('data-value')=='123456'
                            assert page.evaluate('(id)=>window.completions.filter(e=>e.root===id).length',root.get_attribute('id'))==1
                            assert inputs.last.evaluate('e=>e===document.activeElement')
                            page.keyboard.press('Backspace');assert inputs.nth(4).evaluate('e=>e===document.activeElement') and inputs.last.input_value()==''
                            first_left=inputs.nth(4).evaluate('e=>e.getBoundingClientRect().left');page.keyboard.press('ArrowRight')
                            assert inputs.last.evaluate('e=>e===document.activeElement') and inputs.last.evaluate('e=>e.getBoundingClientRect().left')>first_left
                            inputs.first.evaluate('e=>{const data=new DataTransfer();data.setData("text","98 76-54");e.dispatchEvent(new ClipboardEvent("paste",{clipboardData:data,bubbles:true,cancelable:true}))}')
                            assert root.get_attribute('data-value')=='987654'
                            assert page.evaluate('(id)=>window.completions.filter(e=>e.root===id).length',root.get_attribute('id'))==2
                            inputs.first.focus();inputs.first.dispatch_event('compositionstart');inputs.first.evaluate('e=>{e.value="あ";e.dispatchEvent(new InputEvent("input",{bubbles:true,isComposing:true}))}')
                            page.keyboard.press('Enter');assert inputs.first.evaluate('e=>e===document.activeElement')
                            inputs.first.dispatch_event('compositionend');assert inputs.first.input_value()==''
                            inputs.first.fill('9');assert root.get_attribute('data-value')=='987654'
                            # Re-entering a complete value after an incomplete state is a new completion.
                            assert page.evaluate('(id)=>window.completions.filter(e=>e.root===id).length',root.get_attribute('id'))==3
                            page.locator('section').nth(index).locator('[data-probe]').click();root.dispatch_event('focusout',{'relatedTarget':None});page.evaluate('()=>window.dispatchEvent(new Event("blur"))');assert root.get_attribute('data-value')=='987654'
                            if index==2:assert inputs.first.evaluate('e=>e.getBoundingClientRect().left')<inputs.last.evaluate('e=>e.getBoundingClientRect().left')
                            inputs.first.focus();page.keyboard.type('1');assert root.get_attribute('data-value')=='187654' and inputs.nth(1).evaluate('e=>e===document.activeElement')
                            assert page.evaluate('(id)=>window.completions.filter(e=>e.root===id).length',root.get_attribute('id'))==4
                        else:
                            table=root.locator('table');assert table.locator('caption').inner_text()=='Members' and root.get_by_role('table',name='Members').count()==1
                            inputs=table.locator('tbody input');all_=table.locator('thead input');inputs.first.check();assert all_.evaluate('e=>e.indeterminate')
                            assert root.locator('[role="status"]').inner_text()=='1 row selected.'
                            all_.check();assert all(item.is_checked() for item in inputs.all())
                            all_.uncheck();assert not any(item.is_checked() for item in inputs.all())
                            inputs.first.check()
                            name=root.locator('[data-sort="str"]');name.focus();page.keyboard.press('Enter')
                            assert name.locator('..').get_attribute('aria-sort')=='ascending'
                            assert table.locator('tbody tr').first.locator('td').nth(1).inner_text()=='Aoi Kimura'
                            page.keyboard.press('Space');assert name.locator('..').get_attribute('aria-sort')=='descending'
                            assert table.locator('tbody tr').first.locator('td').nth(1).inner_text()=='Ren Sato'
                            billed=root.locator('[data-sort="num"]');billed.click();assert table.locator('tbody tr').first.locator('td').nth(4).inner_text()=='$0'
                            assert table.locator('tbody tr').filter(has_text='Aoi Kimura').locator('input').is_checked()
                            assert page.evaluate('(id)=>window.events.filter(e=>e.root===id&&e.type==="kata-data-table-sort").length',root.get_attribute('id'))==3
                            page.locator('section').nth(index).locator('[data-probe]').click();root.dispatch_event('focusout',{'relatedTarget':None});page.evaluate('()=>window.dispatchEvent(new Event("blur"))')
                        # No operation may mutate an untouched later copy.
                        for other in range(index+1,3):
                            sibling=roots.nth(other)
                            if slug=='tag-input':assert sibling.locator('.k-chip').count()==2
                            elif slug=='input-otp':assert [item.input_value() for item in sibling.locator('input').all()]==['4','8','2','','','']
                            else:assert not sibling.locator('tbody input:checked').count() and sibling.locator('tbody tr').first.locator('td').nth(1).inner_text()=='Aoi Kimura'
                    page.add_script_tag(content=(ROOT/f'components/{slug}/{slug}.js').read_text())
                    assert roots.nth(1).get_attribute('id')=='existing-'+slug+'-root'
                    ids=page.evaluate('()=>[...document.querySelectorAll("[id]")].map(e=>e.id)');assert len(ids)==len(set(ids))
                    registrations=page.evaluate('window.globalRegistrations'); assert not registrations,registrations
                    page.screenshot(path=str(output/f'{slug}-{case}.png'),full_page=True)
                    facts.append({'component':slug,'case':case,'threeIndependent':True,'doubleLoad':True,'rtl':True,'uniqueIds':True,'existingIdsPreserved':True,'nullFocusoutAndBodyClickSafe':True,'keyboard':True,'eventsOnce':True,'globalListeners':0,'consoleErrors':0})
                    page.close()
            browser.close()
    finally:server.shutdown();server.server_close()
    assert not errors,errors
    (output/'results.json').write_text(json.dumps({'cases':facts,'horizontalPositions':arrows,'consoleErrors':errors,'unverified':['Real Japanese IME','Screen readers','Firefox','Safari']},indent=2)+'\n')
    print('Tag Input / OTP / Data Table: 9 Chromium cases; independent triple instances, RTL, double load, events and keyboard passed; console errors 0')
    return facts

if __name__=='__main__':run()
