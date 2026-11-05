"""Exercise independently initialized command, context-menu and date-picker samples."""
import http.server
import json
import threading
from functools import partial
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SPECS = {
    'command': ('[data-command]', '[data-command-open]'),
    'context-menu': ('[data-ctx]', '[data-ctx-zone]'),
    'date-picker': ('[data-dp-panel]', '[data-dp-input]'),
}


def run(output=ROOT/'docs/review/command-context-date'):
    output = Path(output); output.mkdir(parents=True, exist_ok=True)
    facts, errors = [], []
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
            for slug, (panel_selector, trigger_selector) in SPECS.items():
                for case, theme, scale, reduced in [('normal', 'light', 1, 'no-preference'), ('zero', 'dark', 0, 'no-preference'), ('reduce', 'dark', 2, 'reduce')]:
                    page = browser.new_page(viewport={'width': 1100, 'height': 1000}, reduced_motion=reduced)
                    page.on('pageerror', lambda error: errors.append(str(error)))
                    page.on('console', lambda message: errors.append(message.text) if message.type == 'error' else None)
                    page.goto(f'http://127.0.0.1:{server.server_port}/tests/{slug}-multi.html')
                    page.evaluate('([theme,scale])=>{document.documentElement.dataset.theme=theme;document.documentElement.style.setProperty("--k-mscale",scale)}', [theme, scale])
                    panels, triggers = page.locator(panel_selector), page.locator(trigger_selector)
                    assert panels.count() == 3 and triggers.count() == 3
                    def opened(index):
                        panel = panels.nth(index)
                        return panel.evaluate('(e)=>e.tagName==="DIALOG"?e.open:!e.hidden')
                    def open_at(index):
                        if slug == 'context-menu': triggers.nth(index).focus(); page.keyboard.press('Shift+F10')
                        else: triggers.nth(index).click()
                        assert opened(index)
                    def closed(index):
                        page.wait_for_function('(e)=>e.tagName==="DIALOG"?!e.open:e.hidden', arg=panels.nth(index).element_handle())
                    for index in range(3):
                        open_at(index)
                        assert all(not opened(other) for other in range(3) if other != index)
                        panel = panels.nth(index)
                        panel.locator('[data-probe]').click()
                        assert opened(index)
                        panel.evaluate('(e)=>{window.dispatchEvent(new Event("blur"));e.dispatchEvent(new FocusEvent("focusout",{bubbles:true,relatedTarget:null}))}')
                        assert opened(index)
                        if slug == 'context-menu':
                            buttons = panel.locator('[role="menuitem"]')
                            buttons.nth(0).focus(); page.keyboard.press('Tab'); closed(index)
                            open_at(index); buttons.nth(0).focus(); page.keyboard.press('ArrowDown')
                            assert buttons.nth(1).evaluate('(e)=>e===document.activeElement')
                            page.keyboard.press('End'); assert buttons.last.evaluate('(e)=>e===document.activeElement')
                            page.keyboard.press('Home'); assert buttons.first.evaluate('(e)=>e===document.activeElement')
                            page.keyboard.press('d'); assert buttons.nth(1).evaluate('(e)=>e===document.activeElement')
                            page.keyboard.press('d'); assert buttons.nth(3).evaluate('(e)=>e===document.activeElement')
                            buttons.nth(0).focus(); buttons.nth(1).focus(); assert opened(index)
                        else:
                            panel.locator('[data-probe-a]').focus(); page.keyboard.press('Tab')
                            assert panel.locator('[data-probe-b]').evaluate('(e)=>e===document.activeElement')
                            assert opened(index)
                        if slug == 'command':
                            input_ = panel.locator('[data-command-input]'); options = panel.locator('[data-cmd-item]')
                            input_.focus(); page.keyboard.press('ArrowUp')
                            assert input_.get_attribute('aria-activedescendant') == options.last.get_attribute('id')
                            page.keyboard.press('ArrowDown'); assert input_.get_attribute('aria-activedescendant') == options.first.get_attribute('id')
                            input_.fill('no-such-command'); assert panel.locator('[data-command-empty]').is_visible()
                            assert panel.locator('[role="status"]').inner_text() == '0 results.'
                            page.keyboard.press('Enter'); assert opened(index)
                            input_.fill('file'); assert panel.locator('[role="status"]').inner_text() == '1 result.'
                            input_.dispatch_event('compositionstart'); page.keyboard.press('Enter'); assert opened(index)
                            input_.dispatch_event('compositionend')
                            input_.evaluate('(e)=>{e.dispatchEvent(new CompositionEvent("compositionstart",{bubbles:true}));e.dispatchEvent(new CompositionEvent("compositionend",{bubbles:true}));e.dispatchEvent(new KeyboardEvent("keydown",{key:"Enter",bubbles:true}))}'); assert opened(index)
                            input_.evaluate('(e)=>e.dispatchEvent(new KeyboardEvent("keydown",{key:"Enter",keyCode:229,bubbles:true}))'); assert opened(index)
                            input_.evaluate('(e)=>e.dispatchEvent(new KeyboardEvent("keydown",{key:"Enter",isComposing:true,bubbles:true}))'); assert opened(index)
                            page.evaluate('()=>{window.selections=0;if(!window.selectionProbe){document.addEventListener("kata-command-select",()=>window.selections++);window.selectionProbe=true}}')
                            page.keyboard.press('Enter'); closed(index); assert page.evaluate('window.selections') == 1
                            assert triggers.nth(index).evaluate('(e)=>e===document.activeElement')
                            assert input_.get_attribute('aria-activedescendant') is None
                            open_at(index); input_.focus()
                        elif slug == 'date-picker':
                            grid = panel.locator('[role="grid"]'); day = grid.locator('[data-d][tabindex="0"]'); day.focus()
                            original = day.get_attribute('data-d')
                            page.keyboard.press('ArrowRight'); next_day = grid.locator('[tabindex="0"]').get_attribute('data-d')
                            from datetime import date, timedelta
                            assert date.fromisoformat(next_day) == date.fromisoformat(original) + timedelta(days=1)
                            page.keyboard.press('ArrowDown'); assert date.fromisoformat(grid.locator('[tabindex="0"]').get_attribute('data-d')) == date.fromisoformat(original) + timedelta(days=8)
                            page.keyboard.press('ArrowUp'); page.keyboard.press('ArrowLeft'); assert grid.locator('[tabindex="0"]').get_attribute('data-d') == original
                            page.keyboard.press('Home'); assert date.fromisoformat(grid.locator('[tabindex="0"]').get_attribute('data-d')).weekday() == 6
                            page.keyboard.press('End'); assert date.fromisoformat(grid.locator('[tabindex="0"]').get_attribute('data-d')).weekday() == 5
                            before_year = int(grid.locator('[tabindex="0"]').get_attribute('data-d')[:4]); page.keyboard.press('Shift+PageDown')
                            assert int(grid.locator('[tabindex="0"]').get_attribute('data-d')[:4]) == before_year + 1
                            page.keyboard.press('Shift+PageUp'); page.keyboard.press('PageDown'); page.keyboard.press('PageUp')
                            # Navigate to January 31 without changing the application's clock.
                            current = date.fromisoformat(grid.locator('[tabindex="0"]').get_attribute('data-d'))
                            while current.month != 1:
                                page.keyboard.press('PageUp'); current = date.fromisoformat(grid.locator('[tabindex="0"]').get_attribute('data-d'))
                            while current.day < 31:
                                page.keyboard.press('ArrowRight'); current = date.fromisoformat(grid.locator('[tabindex="0"]').get_attribute('data-d'))
                            page.keyboard.press('PageDown')
                            february = date.fromisoformat(grid.locator('[tabindex="0"]').get_attribute('data-d'))
                            import calendar
                            assert february.month == 2 and february.day == calendar.monthrange(february.year, 2)[1]
                            assert panel.locator('[data-dp-title]').get_attribute('aria-live') == 'polite'
                            grid.dispatch_event('compositionstart'); page.keyboard.press('Enter'); assert opened(index)
                            grid.dispatch_event('compositionend'); grid.evaluate('(e)=>e.dispatchEvent(new KeyboardEvent("keydown",{key:"Enter",keyCode:229,bubbles:true}))'); assert opened(index)
                            grid.locator('[tabindex="0"]').focus(); page.keyboard.press('Enter'); closed(index)
                            assert triggers.nth(index).input_value()
                            assert all(not triggers.nth(other).input_value() for other in range(index+1, 3))
                            assert triggers.nth(index).evaluate('(e)=>e===document.activeElement')
                            open_at(index)
                        page.keyboard.press('Escape'); closed(index)
                        assert triggers.nth(index).evaluate('(e)=>e===document.activeElement')
                    # Existing IDs survive; pre-existing generated-looking IDs are not reused.
                    original_id = triggers.first.get_attribute('id')
                    page.add_script_tag(content=(ROOT/f'components/{slug}/{slug}.js').read_text())
                    assert triggers.first.get_attribute('id') == original_id
                    assert panels.nth(1).get_attribute('id') == 'existing-'+slug+'-panel'
                    assert triggers.nth(1).get_attribute('id') == 'existing-'+slug+'-trigger'
                    ids = page.evaluate('()=>[...document.querySelectorAll("[id]")].map(e=>e.id)'); assert len(ids) == len(set(ids))
                    assert page.locator('section').nth(2).evaluate('(e)=>getComputedStyle(e).direction') == 'rtl'
                    open_at(2)
                    if slug == 'context-menu':
                        page.keyboard.press('Escape'); closed(2)
                        triggers.nth(2).dispatch_event('contextmenu', {'clientX':1095,'clientY':995})
                        rect = panels.nth(2).bounding_box(); assert rect['x'] >= 0 and rect['x']+rect['width'] <= 1100 and rect['y']+rect['height'] <= 1000
                    page.screenshot(path=str(output/f'{slug}-{case}.png'), full_page=True)
                    if slug != 'command':
                        page.locator('[data-outside]').click(); closed(2)
                        # End events may never fire; the duration-based fallback must still close.
                        open_at(2)
                        panels.nth(2).evaluate('(e)=>{e.style.transition="opacity 30ms linear";e.style.opacity="0.9"}')
                        page.locator('[data-outside]').click(); closed(2)
                        # Reopening cancels a pending close.
                        open_at(2); panels.nth(2).evaluate('(e)=>e.style.transition="opacity 100ms linear"')
                        panels.nth(2).dispatch_event('focusout', {'relatedTarget':None}); assert opened(2)
                        page.keyboard.press('Escape')
                        if slug == 'context-menu': triggers.nth(2).dispatch_event('contextmenu', {'clientX':100,'clientY':100})
                        else: triggers.nth(2).evaluate('(e)=>e.click()')
                        page.wait_for_timeout(180); assert opened(2)
                    else:
                        page.keyboard.press('Escape'); closed(2)
                        triggers.nth(1).focus(); page.keyboard.press('Control+k'); assert opened(1) and not opened(0)
                        panels.nth(1).evaluate('(e)=>e.addEventListener("cancel",event=>event.preventDefault(),{once:true})')
                        page.keyboard.press('Escape'); assert opened(1)
                        page.keyboard.press('Escape'); closed(1)
                    facts.append({'component':slug,'case':case,'threeIndependent':True,'doubleLoad':True,'rtl':True,'idsUnique':True,'existingIdsPreserved':True,'monthEndClamped':slug == 'date-picker','nullFocusoutKeepsOpen':True,'paragraphKeepsOpen':True,'keyboard':True,'syntheticIme':slug != 'context-menu','consoleErrors':0})
                    page.close()
            browser.close()
    finally:
        server.shutdown(); server.server_close()
    assert not errors, errors
    (output/'results.json').write_text(json.dumps({'cases':facts,'consoleErrors':errors,'manualNotVerified':['Real Japanese IME','Screen readers','Firefox','Safari']},indent=2)+'\n')
    print('3 components × normal/zero/reduce, triple instances, double load, keyboard and null focusout: passed; console errors 0')
    return facts

if __name__ == '__main__': run()
