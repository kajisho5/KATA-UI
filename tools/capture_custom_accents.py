"""Exercise real Foundry controls, static exports and manual CSS accent edits in Chromium."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from tools.capture_text_contrast import rows
from tools.color_roles import theme_css
ROOT=Path(__file__).resolve().parents[1]


def main():
    output=ROOT/'docs/review/text-contrast';result=[];errors=[]
    config=json.loads((ROOT/'system/tokens.json').read_text())['contrast']
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
        page=browser.new_page(viewport={'width':1100,'height':800})
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.route('https://**/*',lambda route:route.abort())
        page.goto('http://127.0.0.1:8765/components/button/',wait_until='networkidle')
        # Isolated preview uses the actual shipped component CSS and the live root palette.
        page.evaluate('''()=>{const demo=document.createElement('div');demo.id='contrast-demo';demo.innerHTML='<button type="button" class="btn btn-accent btn-md">Palette test button</button>';demo.style.cssText='position:fixed;inset:80px auto auto 30px;z-index:99999;padding:24px;background:var(--k-bg)';document.body.append(demo)}''')
        page.add_style_tag(content=(ROOT/'components/button/button.css').read_text()+' *{transition:none!important;animation:none!important}')
        page.locator('#fdfab').click()
        for mode in ('light','dark'):
            page.locator('#fd-'+mode).click()
            for accent in ('#1f3a5f','#ffd166'):
                page.locator('#fd-accent').fill(accent)
                page.locator('#fd-accent').dispatch_event('input')
                page.wait_for_timeout(50)
                button=page.locator('#contrast-demo button')
                for state in ('default','hover','active','focus'):
                    page.mouse.move(1080,780)
                    if state=='hover':button.hover()
                    if state=='active':button.hover();page.mouse.down()
                    if state=='focus':page.keyboard.press('Tab');button.focus()
                    measured=next(row for row in rows(page) if row['text']=='Palette test button')
                    result.append({'theme':mode,'accent':accent,'source':'Foundry','state':state,**measured})
                    assert measured['ratio']>=4.5,result[-1]
                    if state=='active':page.mouse.up()
                    button.evaluate('(e)=>e.blur()')
                page.locator('#contrast-demo').screenshot(path=str(output/f'custom-{mode}-{accent[1:]}.png'))
                with page.expect_download() as download:page.locator('[data-export-theme]').click()
                path=output/f'export-{mode}-{accent[1:]}.css';download.value.save_as(path)
                expected=theme_css(accent,config)
                assert path.read_text()==expected,'Python/build and browser export diverged'
                # Prove a downloaded theme needs no relative-color implementation.
                legacy=browser.new_page()
                base=(ROOT/'tokens.css').read_text();start=base.index('/* relative-color-roles:start */');end=base.index('/* relative-color-roles:end */')+len('/* relative-color-roles:end */')
                base=base[:start]+base[end:]
                legacy.set_content('<html data-theme="'+mode+'"><style>'+base+expected+(ROOT/'components/button/button.css').read_text()+'</style><button type="button" class="btn btn-accent">Export fallback</button>')
                measured=rows(legacy)[0];result.append({'theme':mode,'accent':accent,'source':'static-export', 'state':'default',**measured});assert measured['ratio']>=4.5
                legacy.close()
                # No Foundry JS: hand editing the shared accent must recompute roles in CSS.
                manual=browser.new_page();manual.set_content('<html data-theme="'+mode+'"><style>'+(ROOT/'tokens.css').read_text()+(ROOT/'components/button/button.css').read_text()+'</style><button type="button" class="btn btn-accent">Manual CSS</button>')
                manual.evaluate('(accent)=>document.documentElement.style.setProperty("--k-accent",accent)',accent)
                measured=rows(manual)[0];result.append({'theme':mode,'accent':accent,'source':'manual-css','state':'default',**measured});assert measured['ratio']>=4.5
                manual.close()
        # Existing Themes custom palette must export the same roles as Foundry.
        page.goto('http://127.0.0.1:8765/themes/',wait_until='networkidle')
        for accent in ('#1f3a5f','#ffd166'):
            page.locator('#thcolor').fill(accent);page.locator('#thcolor').dispatch_event('input')
            assert page.locator('#thcss').text_content()==theme_css(accent,config)
        browser.close()
    assert not errors,errors
    (output/'custom-accents.json').write_text(json.dumps({'measurements':result,'errors':errors},indent=2)+'\n')
    print(len(result),'custom accent/state/export/manual-CSS measurements passed; no page errors')

if __name__=='__main__':main()
