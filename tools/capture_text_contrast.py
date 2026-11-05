"""Measure shared-theme text contrast in real component previews (not Mold pass/fail)."""
import argparse,json,re
from pathlib import Path
from playwright.sync_api import sync_playwright
try:
    from tools.capture_shape_migration import Source,content,open_state,CONTRAST_METRICS,sheet,pixel_diff
    from tools.capture_toast_tokens import contrast
except ModuleNotFoundError:
    from capture_shape_migration import Source,content,open_state,CONTRAST_METRICS,sheet,pixel_diff
    from capture_toast_tokens import contrast

ROOT=Path(__file__).resolve().parents[1]
CORE=['button','input','select','card','badge','modal','drawer','dropdown','popover','tabs','toast','tooltip']
MORE=['field','textarea','checkbox','radio','switch','accordion','alert','table','pagination','breadcrumbs','combobox','input-otp','tag-input','file-upload','slider','dual-range','segmented','toggle','button-group','input-group','alert-dialog','command','context-menu','hover-card','navigation-menu','menubar','copy-field','collapsible']


PROPOSAL_TOKENS=':root,[data-theme="light"]{--k-accent:#247c8c;--k-on-accent:#fff;--k-danger-hover:#b7282e}[data-theme="dark"]{--k-accent:#33a6b8;--k-on-accent:#18181b;--k-danger-hover:#b7282e}'


def proposed_roles(css):
    """Diagnostic common-role migration, not an applied component patch."""
    css=re.sub(r'(?<![\w-])color:\s*var\(--k-danger\)', 'color:var(--k-danger-ink)',css)
    css=re.sub(r'(?<![\w-])background:\s*var\(--k-danger-ink\)', 'background:var(--k-danger-hover)',css)
    def role_block(m):
        body=m[2]
        if re.search(r'(?<![\w-])background:\s*var\(--k-accent\)',body):body=body.replace('color:var(--k-on-color)','color:var(--k-on-accent)')
        return m[1]+'{'+body+'}'
    return re.sub(r'([^{}]+)\{([^{}]*)\}',role_block,css)


class RoleProposal(Source):
    def read(self,path):
        value=super().read(path)
        return value+PROPOSAL_TOKENS if str(path)=='tokens.css' else value
    def css(self,target,seen=None):return proposed_roles(super().css(target,seen))


def rows(page):
    # Opacity-zero ancestors paint no visible text; do not count hidden menus as 1:1.
    script=CONTRAST_METRICS.replace('const result=[];', 'function disabled(e){const label=e.closest(\'label\');return !!(e.matches(\':disabled\')||e.closest(\'button:disabled,fieldset:disabled,[aria-disabled="true"]\')||label?.control?.disabled)}\n const result=[];')
    script=script.replace("const own=[...e.childNodes]", "if([...function*(n){while(n){yield n;n=n.parentElement}}(e)].some(n=>+getComputedStyle(n).opacity===0))continue;\n  if(e.matches('input')&&['checkbox','radio','range','file','color','hidden','image'].includes(e.type))continue;\n  const own=[...e.childNodes]")
    script=script.replace('disabled:!!e.disabled','disabled:disabled(e)')
    data=page.evaluate(script)
    for row in data:
        fg='rgb('+','.join(str(n) for n in row['foreground'])+')';bg='rgb('+','.join(str(n) for n in row['background'])+')'
        row['ratio']=contrast(fg,bg)
    return data


def extra_state(page,slug):
    if slug=='alert-dialog':page.locator('[data-alert-open]').click()
    if slug=='command':page.locator('[data-command-open]').click()
    if slug=='context-menu':page.locator('[data-ctx-zone]').click(button='right')
    if slug=='hover-card':page.locator('[data-hover] a').first.focus()
    if slug=='navigation-menu':page.locator('.k-navm-btn').first.click()
    if slug=='menubar':page.locator('.k-mbar-btn').first.click()
    if slug=='combobox':page.locator('[role=combobox]').click()


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--phase',choices=('before','after','proposal'),required=True);parser.add_argument('--ref');parser.add_argument('--only',nargs='+');parser.add_argument('--limit',type=int,default=40);args=parser.parse_args()
    out=ROOT/'docs/review/text-contrast';out.mkdir(parents=True,exist_ok=True);source=RoleProposal() if args.phase=='proposal' else Source(args.ref);errors=[];facts={}
    slugs=(CORE+MORE)[:args.limit]
    if args.only and (out/(args.phase+'.json')).exists():facts=json.loads((out/(args.phase+'.json')).read_text())['facts']
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
        for theme in ('light','dark'):
            facts.setdefault(theme,{})
            for slug in slugs:
                if args.only and slug not in args.only:continue
                page=browser.new_page(viewport={'width':900,'height':600},reduced_motion='reduce');page.on('pageerror',lambda e:errors.append(str(e)))
                page.set_content(content(source,'components/'+slug,theme));js=source.read('components/'+slug+'/'+slug+'.js')
                if js:page.add_script_tag(content=js)
                if slug in CORE:open_state(page,slug)
                else:extra_state(page,slug)
                page.evaluate('() => new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')
                facts[theme][slug]={'default':rows(page)}
                page.screenshot(path=str(out/f'{args.phase}-{theme}-{slug}.png'))
                if slug in ('button','dropdown','context-menu','tabs','pagination'):
                    selectors={'button':['.btn-accent','.btn-danger'], 'dropdown':['.menu a:not(.danger)','.menu a.danger'], 'context-menu':['.k-ctx button:not(.danger)','.k-ctx button.danger'], 'tabs':['.tabs button.on','.tabs button:not(.on)'], 'pagination':['a.k-page[aria-current="page"]','a.k-page:not([aria-current]):not(.disabled)']}
                    for selector in selectors[slug]:
                        candidates=page.locator(selector)
                        if slug=='pagination':candidates=candidates.filter(has_text=re.compile(r'^\d+$'))
                        target=candidates.first
                        if not target.count():continue
                        for state in ('hover','active','focus'):
                            print(theme,slug,selector,state,flush=True)
                            if slug=='dropdown' and not page.locator('.menu').evaluate('(e)=>e.classList.contains("open")'):open_state(page,slug)
                            if slug=='context-menu' and page.locator('.k-ctx').evaluate('(e)=>e.hidden'):extra_state(page,slug)
                            page.mouse.move(895,595)
                            if state=='focus':
                                # Keyboard Tab gives :focus-visible, unlike a synthetic click.
                                target.evaluate('(e)=>{e.setAttribute("data-contrast-target","")}')
                                page.keyboard.press('Tab');target.focus()
                            else:
                                target.hover()
                                if state=='active':page.mouse.down()
                            key=selector+' / '+state
                            indices=target.evaluate('(e)=>[...document.body.querySelectorAll("*")].flatMap((node,i)=>e.contains(node)?[i]:[])')
                            facts[theme][slug][key]=[row for row in rows(page) if row['index'] in indices]
                            if state=='active':page.mouse.up()
                            target.evaluate('(e)=>e.blur()')
                if slug=='button':
                    for name in ('accent','danger'):
                        page.locator('.btn-'+name).hover();facts[theme][slug][name+'-hover']=rows(page)
                        page.screenshot(path=str(out/f'{args.phase}-{theme}-button-{name}-hover.png'))
                page.close()
            sheet([(slug,out/f'{args.phase}-{theme}-{slug}.png') for slug in slugs],out/f'{args.phase}-{theme}-overview.png',columns=4,tile=(225,150))
        browser.close()
    result={'ref':args.ref or 'worktree','phase':args.phase,'targets':slugs,'facts':facts,'errors':errors,'method':'Computed colors + ancestor alpha/opacity composition; same WCAG luminance function as Toast; fully transparent ancestor content excluded as unpainted.'}
    (out/(args.phase+'.json')).write_text(json.dumps(result,indent=2)+'\n')
    assert not errors,errors
    print(args.phase,len(slugs),'components, 2 themes, default/open + accent/danger hover; no page errors')

if __name__=='__main__':main()
