"""Render actual previews, measure shape changes, and exercise the Foundry slider."""
import argparse
from functools import partial
import http.server
import json
from pathlib import Path
import re
import subprocess
import threading
from PIL import Image, ImageChops, ImageDraw
from playwright.sync_api import sync_playwright
try:
    from tools.capture_toast_tokens import contrast
except ModuleNotFoundError:
    from capture_toast_tokens import contrast

ROOT=Path(__file__).resolve().parents[1]
MAJOR=['button','input','select','card','badge','modal','drawer','dropdown','popover','tabs','toast','tooltip']
HARNESS='body{margin:0;padding:32px;background:var(--k-bg);color:var(--k-ink);font-family:var(--k-font);font-size:14px}*,*::before,*::after{animation:none!important;transition:none!important;caret-color:transparent!important}'
METRICS='''() => [...document.body.querySelectorAll('*')].flatMap((e,index)=>['','::before','::after','::backdrop'].map(pseudo=>{const s=getComputedStyle(e,pseudo||null);const r=e.getBoundingClientRect();return {key:index+':'+pseudo,element:e.tagName.toLowerCase()+'.'+e.className,pseudo,radius:[s.borderTopLeftRadius,s.borderTopRightRadius,s.borderBottomRightRadius,s.borderBottomLeftRadius],shadow:s.boxShadow,background:s.backgroundColor,rect:[r.x,r.y,r.width,r.height]}}))'''


CONTRAST_METRICS='() => {\n const canvas=document.createElement(\'canvas\');canvas.width=canvas.height=1;const ctx=canvas.getContext(\'2d\',{willReadFrequently:true});\n function rgba(color){ctx.clearRect(0,0,1,1);ctx.fillStyle=color;ctx.fillRect(0,0,1,1);return [...ctx.getImageData(0,0,1,1).data].map((v,i)=>i===3?v/255:v)}\n function over(a,b){const alpha=a[3]+b[3]*(1-a[3]);return alpha?[0,1,2].map(i=>(a[i]*a[3]+b[i]*b[3]*(1-a[3]))/alpha).concat(alpha):[0,0,0,0]}\n function colors(e,style,pseudo=false){let foreground=rgba(style.color),background=rgba(style.backgroundColor);foreground=over(foreground,background);const opacity=+style.opacity;foreground[3]*=opacity;background[3]*=opacity;\n  for(let parent=(pseudo?e:e.parentElement);parent;parent=parent.parentElement){const s=getComputedStyle(parent);const bg=rgba(s.backgroundColor);foreground=over(foreground,bg);background=over(background,bg);foreground[3]*=+s.opacity;background[3]*=+s.opacity;}\n  return {foreground:over(foreground,[255,255,255,1]).slice(0,3),background:over(background,[255,255,255,1]).slice(0,3)};\n }\n const result=[];\n for(const [index,e] of [...document.body.querySelectorAll(\'*\')].entries()){\n  const s=getComputedStyle(e),rect=e.getBoundingClientRect();if(!rect.width||!rect.height||s.visibility===\'hidden\'||s.display===\'none\')continue;\n  const own=[...e.childNodes].filter(n=>n.nodeType===Node.TEXT_NODE).map(n=>n.textContent.trim()).filter(Boolean).join(\' \');\n  let text=own,style=s,kind=\'text\';\n  if(e.matches(\'input,textarea\')){text=e.value||e.getAttribute(\'placeholder\')||\'\';if(!e.value&&text){style=getComputedStyle(e,\'::placeholder\');kind=\'placeholder\'}}\n  if(e.matches(\'select\'))text=e.selectedOptions[0]?.textContent||\'\';\n  if(text&&!e.matches(\'option\')){\n   // For ordinary text, begin compositing with the element\'s own background only once.\n   const color=colors(e,style,kind===\'placeholder\');result.push({element:e.tagName.toLowerCase()+\'.\'+e.className,index,text,kind,disabled:!!e.disabled,opacity:s.opacity,...color});\n  }\n  for(const pseudo of [\'::before\',\'::after\']){const ps=getComputedStyle(e,pseudo);if(!ps.content||[\'none\',\'normal\',\'""\'].includes(ps.content)||+ps.opacity===0)continue;\n   result.push({element:e.tagName.toLowerCase()+\'.\'+e.className,index,text:ps.content,kind:pseudo,disabled:!!e.disabled,opacity:ps.opacity,...colors(e,ps,true)});\n  }\n }\n return result;\n}\n'

class Source:
    def __init__(self,ref=None):self.ref=ref;self.cache={}
    def read(self,path):
        path=str(path)
        if path not in self.cache:
            if self.ref:
                r=subprocess.run(['git','show',self.ref+':'+path],cwd=ROOT,text=True,capture_output=True)
                self.cache[path]=r.stdout if r.returncode==0 else ''
            else:
                p=ROOT/path;self.cache[path]=p.read_text() if p.is_file() else ''
        return self.cache[path]
    def css(self,target,seen=None):
        seen=set() if seen is None else seen
        if target in seen:return ''
        seen.add(target);html=self.read(target+'/preview.html');meta=json.loads(self.read(target+'/meta.json') or '{}');out=''
        names=set(meta.get('deps',[])+meta.get('uses',[]))
        for href in re.findall(r'<link[^>]*href=["\']([^"\']+)',html):
            if href.startswith('/components/'):
                names.add(href.split('/')[2])
        for name in sorted(names):out+=self.css('components/'+name,seen)
        for name in meta.get('blocks',[]):out+=self.css('blocks/'+name,seen)
        return out+self.read(target+'/'+target.split('/')[-1]+'.css')


def content(source,target,theme,radius=None):
    html=source.read(target+'/preview.html')
    html=re.sub(r'<link\b[^>]*>|<script\b[^>]*>.*?</script>','',html,flags=re.S|re.I)
    base='' if radius is None else f' style="--k-radius:{radius}px"'
    stage='body{display:flex;justify-content:center}' if target=='components/popover' else ''
    return f'<!doctype html><html lang="en" data-theme="{theme}"{base}><head><title>KATA {target}</title><style>'+source.read('tokens.css')+source.css(target)+HARNESS+stage+'</style></head><body>'+html+'</body></html>'


def open_state(page,slug):
    triggers={'modal':'[data-modal-open]','drawer':'[data-drawer-open]','dropdown':'[data-dd-trigger]','popover':'[data-popover-btn]','toast':'[data-toast-demo]'}
    if slug in triggers:page.locator(triggers[slug]).first.click()
    if slug=='tooltip':page.locator('[data-tip]').first.hover()
    states={'modal':'dialog[open]','drawer':'dialog[open]','dropdown':'[data-dd-menu].open','popover':'[data-popover-panel].open','toast':'.toast'}
    if slug in states:assert page.locator(states[slug]).count()>0,slug+' failed to open'
    if slug=='tabs':
        page.locator('[data-tabs] button').nth(1).click()
        assert 'Details' in page.locator('[data-tabpane]').inner_text()
        page.locator('[data-tabs] button').first.click()


def pixel_diff(before,after,destination):
    a=Image.open(before).convert('RGB');b=Image.open(after).convert('RGB');diff=ImageChops.difference(a,b)
    mask=diff.convert('L').point(lambda n:255 if n else 0)
    # RGB max avoids missing a one-channel change whose grayscale rounds to zero.
    mask=ImageChops.lighter(ImageChops.lighter(diff.getchannel('R'),diff.getchannel('G')),diff.getchannel('B')).point(lambda n:255 if n else 0)
    heat=Image.new('RGB',a.size,'white');heat.paste((220,40,40),mask=mask);heat.save(destination)
    return {'changed_pixels':sum(mask.histogram()[1:]),'bounds':mask.getbbox()}


def sheet(paths,destination,columns=3,tile=(300,200)):
    canvas=Image.new('RGB',(columns*tile[0],((len(paths)+columns-1)//columns)*(tile[1]+24)), '#eee')
    draw=ImageDraw.Draw(canvas)
    for i,(label,path) in enumerate(paths):
        image=Image.open(path).convert('RGB');image.thumbnail(tile)
        x=i%columns*tile[0];y=i//columns*(tile[1]+24)
        draw.text((x+6,y+4),label,fill='black');canvas.paste(image,(x,y+24))
    canvas.save(destination)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--before-ref',required=True);parser.add_argument('--output',default='docs/review/shared-shape');parser.add_argument('--chromium',default='/usr/bin/chromium');args=parser.parse_args()
    out=ROOT/args.output;out.mkdir(parents=True,exist_ok=True);sources={'before':Source(args.before_ref),'after':Source()};facts={};errors=[];contrasts={};mobile={}
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=args.chromium,args=['--no-sandbox'])
        for phase,source in sources.items():
            facts[phase]={}
            for theme in ('light','dark'):
                facts[phase][theme]={}
                for slug in MAJOR:
                    page=browser.new_page(viewport={'width':900,'height':600},reduced_motion='reduce')
                    page.on('pageerror',lambda e:errors.append(str(e)))
                    page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
                    page.set_content(content(source,'components/'+slug,theme))
                    js=source.read('components/'+slug+'/'+slug+'.js')
                    if js:page.add_script_tag(content=js)
                    open_state(page,slug);page.evaluate('() => new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))')
                    assert page.title()=='KATA components/'+slug
                    assert page.locator('body').inner_text().strip()
                    facts[phase][theme][slug]=page.evaluate(METRICS)
                    if phase=='after' and theme=='dark':
                        measured=page.evaluate(CONTRAST_METRICS)
                        for row in measured:
                            fg='rgb('+','.join(str(n) for n in row['foreground'])+')'
                            bg='rgb('+','.join(str(n) for n in row['background'])+')'
                            row['ratio']=contrast(fg,bg)
                        contrasts[slug]=measured
                    page.screenshot(path=str(out/f'{phase}-{theme}-{slug}.png'),animations='disabled')
                    if theme=='light':
                        page.set_viewport_size({'width':360,'height':760})
                        if slug=='tooltip':page.locator('[data-tip]').first.hover()
                        mobile.setdefault(phase,{})[slug]=page.evaluate('() => ({viewport:innerWidth,scrollWidth:document.documentElement.scrollWidth})')
                        page.screenshot(path=str(out/f'{phase}-mobile-{slug}.png'),animations='disabled')
                    page.close()
        diffs={}
        for theme in ('light','dark'):
            diffs[theme]={}
            for slug in MAJOR:
                a={r['key']:r for r in facts['before'][theme][slug]};b={r['key']:r for r in facts['after'][theme][slug]}
                changes=[]
                for key in sorted(a.keys()&b.keys()):
                    changed={prop:{'before':a[key][prop],'after':b[key][prop]} for prop in ('radius','shadow','background','rect') if a[key][prop]!=b[key][prop]}
                    if changed:changes.append({'element':a[key]['element'],'pseudo':a[key]['pseudo'],'changes':changed})
                diffs[theme][slug]={**pixel_diff(out/f'before-{theme}-{slug}.png',out/f'after-{theme}-{slug}.png',out/f'diff-{theme}-{slug}.png'),'styles':changes}
            for phase in ('before','after','diff'):
                sheet([(slug,out/f'{phase}-{theme}-{slug}.png') for slug in MAJOR],out/f'{phase}-{theme}-overview.png')
        # Every UI target, including blocks/templates, is rendered with its real source CSS.
        ui=[]
        for group in ('components','blocks','templates'):
            for meta in sorted((ROOT/group).glob('*/meta.json')):
                if json.loads(meta.read_text()).get('category') not in ('Motion','KATAYABURI'):ui.append(str(meta.parent.relative_to(ROOT)))
        scale_facts={};gallery={0:[],16:[]}
        scratch=out/'radius-previews';scratch.mkdir(exist_ok=True)
        for target in ui:
            page=browser.new_page(viewport={'width':600,'height':320},reduced_motion='reduce');scale_facts[target]={}
            for radius in (0,16):
                page.set_content(content(sources['after'],target,'light',radius))
                # Open native dialogs for visible shape proof; no component JS is rewritten.
                page.evaluate("() => document.querySelectorAll('dialog').forEach(d=>{if(!d.open)d.show()})")
                metrics=page.evaluate(METRICS);scale_facts[target][str(radius)]=metrics
                path=scratch/(target.replace('/','-')+f'-{radius}.png');page.screenshot(path=str(path),animations='disabled');gallery[radius].append((target,path))
            page.close()
        for radius in (0,16):sheet(gallery[radius],out/f'all-ui-radius-{radius}.png',columns=4,tile=(240,128))
        # Individual tiles are intermediate; keep the galleries and measured data.
        for path in scratch.glob('*.png'):path.unlink()
        scratch.rmdir()
        # Exercise the actual built Foundry deck, including persisted zero on reload.
        class Quiet(http.server.SimpleHTTPRequestHandler):
            def log_message(self,*args):pass
        server=http.server.ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT/'dist')))
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        foundry={};page=browser.new_page(viewport={'width':1280,'height':900},reduced_motion='reduce')
        page.route('**/*',lambda route:route.continue_() if route.request.url.startswith('http://127.0.0.1:') else route.fulfill(status=200,body=''))
        url=f'http://127.0.0.1:{server.server_port}/design-system/'
        page.goto(url,wait_until='load')
        for radius in (0,16):
            page.locator('#fd-radius').evaluate('(e,v)=>{e.value=v;e.dispatchEvent(new Event("input",{bubbles:true}))}',str(radius))
            page.reload(wait_until='load')
            page.locator('#fdfab').click()
            assert page.locator('#fdeck').is_visible()
            foundry[str(radius)]=page.evaluate("() => Object.fromEntries(['xs','sm','md','lg','xl','full'].map(name=>{const e=document.createElement('div');e.style.borderRadius='var(--k-radius-'+name+')';document.body.append(e);const value=getComputedStyle(e).borderRadius;e.remove();return[name,value]}))")
            expected={'xs':radius*.375,'sm':radius*.75,'md':radius,'lg':radius*1.5,'xl':radius*2,'full':999}
            assert all(foundry[str(radius)][name]==f'{value:g}px' for name,value in expected.items()),foundry
            page.screenshot(path=str(out/f'foundry-radius-{radius}.png'),full_page=True)
        page.close();server.shutdown();server.server_close();browser.close()
    # Compact full metrics into radius changes, while preserving the pre/post numeric corners.
    scale_summary={}
    for target,by_scale in scale_facts.items():
        a={m['key']:m for m in by_scale['0']};b={m['key']:m for m in by_scale['16']}
        scale_summary[target]=[{'element':a[key]['element'],'pseudo':a[key]['pseudo'],'at0':a[key]['radius'],'at16':b[key]['radius']} for key in sorted(a.keys()&b.keys()) if a[key]['radius']!=b[key]['radius']]
    result={'before_ref':args.before_ref,'browser':'Chromium','viewport':[900,600],'browser_plugin':'not available; Python Playwright used','errors':errors,'diffs':diffs,'foundry':foundry,'ui_targets':len(ui),'radius_changes':scale_summary,'dark_contrast':contrasts,'mobile':mobile}
    (out/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    assert not errors,errors
    print('Captured 12 × 2 themes × before/after; rendered',len(ui),'UI targets; Foundry persistence verified; no console/page errors')

if __name__=='__main__':main()
