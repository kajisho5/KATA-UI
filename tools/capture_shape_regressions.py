"""Compare restored effects and semantic rings against pre-PR19 and PR19 sources."""
import argparse
import json
from pathlib import Path
import re
from PIL import Image
from playwright.sync_api import sync_playwright
try:
    from tools.capture_shape_migration import Source,content,HARNESS,METRICS,sheet,pixel_diff
except ModuleNotFoundError:
    from capture_shape_migration import Source,content,HARNESS,METRICS,sheet,pixel_diff

ROOT=Path(__file__).resolve().parents[1]
LAB=['comparison-slider','converge','glow-button','meteors','newtons-cradle','orbit','tracing-beam']
TARGETS=['components/'+name for name in LAB+['color-picker','tour']]+['templates/product-page']
SEED='''(()=>{let n=918273;Math.random=()=>{n=(1664525*n+1013904223)>>>0;return n/4294967296}})()'''
FREEZE='body{margin:0;padding:32px;background:var(--k-bg);color:var(--k-ink);font-family:var(--k-font);font-size:14px}*,*::before,*::after{transition:none!important;caret-color:transparent!important;animation-play-state:paused!important}'


def freeze(page):
    page.evaluate('''() => {document.querySelectorAll('svg').forEach(s=>{s.pauseAnimations();s.setCurrentTime(.8)});document.getAnimations().forEach(a=>{a.pause();const t=a.effect.getTiming();a.currentTime=Number(t.delay||0)+Number(t.duration||1000)*.35})}''')
    page.evaluate('() => new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--before-ref',default='9efb97d');parser.add_argument('--pr19-ref',default='0a486dd');args=parser.parse_args()
    out=ROOT/'docs/review/shape-regressions';out.mkdir(parents=True,exist_ok=True);facts={};errors=[];edges={}
    phases={'before19':Source(args.before_ref),'initial19':Source(args.pr19_ref),'restored':Source()}
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
        for phase,source in phases.items():
            facts[phase]={}
            for theme in ('light','dark'):
                facts[phase][theme]={}
                for target in TARGETS:
                    slug=target.split('/')[-1];page=browser.new_page(viewport={'width':1100,'height':900},reduced_motion='no-preference')
                    page.on('pageerror',lambda error:errors.append(str(error)))
                    html=content(source,target,theme).replace(HARNESS,FREEZE)
                    page.set_content(html);page.add_script_tag(content=SEED)
                    js=source.read(target+'/'+slug+'.js')
                    if js:page.add_script_tag(content=js)
                    if slug=='glow-button':page.locator('.k-glowbtn button').hover();page.locator('.k-glowfield input').focus()
                    if slug=='tracing-beam':page.locator('.k-beam-body').evaluate('(e)=>{e.scrollTop=110;e.dispatchEvent(new Event("scroll"))}')
                    freeze(page)
                    facts[phase][theme][slug]=page.evaluate(METRICS)
                    page.screenshot(path=str(out/f'{phase}-{theme}-{slug}.png'),animations='allow')
                    if slug=='product-page':
                        page.locator('.k-tpl-pd-sw input').nth(1).focus();freeze(page)
                        page.screenshot(path=str(out/f'{phase}-{theme}-product-focus.png'))
                    page.close()
                for side in ('right','left'):
                    page=browser.new_page(viewport={'width':1000,'height':700},reduced_motion='reduce');html=content(source,'components/drawer',theme)
                    if side=='left':html=html.replace('</style>','.kdrawer{margin:0 auto 0 0;inset:0 auto 0 0}</style>')
                    page.set_content(html);page.add_script_tag(content=source.read('components/drawer/drawer.js'));page.locator('[data-drawer-open]').click()
                    enabled=out/f'{phase}-{theme}-drawer-{side}.png';page.screenshot(path=str(enabled))
                    if phase=='restored':
                        rect=page.locator('dialog').bounding_box();page.locator('dialog').evaluate('(e)=>e.style.boxShadow="none"')
                        disabled=out/f'restored-{theme}-drawer-{side}-no-shadow.png';page.screenshot(path=str(disabled))
                        a=Image.open(enabled).convert('RGB');b=Image.open(disabled).convert('RGB');profile=[]
                        for distance in range(1,81):
                            x=int(rect['x']-distance) if side=='right' else int(rect['x']+rect['width']+distance-1)
                            deltas=sorted(max(abs(c-d) for c,d in zip(a.getpixel((x,y)),b.getpixel((x,y)))) for y in range(175,525))
                            profile.append(deltas[len(deltas)//2])
                        edges.setdefault(theme,{})[side]={'visible_width_at_delta2':max((n+1 for n,v in enumerate(profile) if v>=2),default=0),'at8':profile[7],'profile':profile}
                        assert edges[theme][side]['visible_width_at_delta2']>=8
                    page.close()
        # Verify fixed light palette paint and semantic rings across theme/Foundry changes.
        page=browser.new_page();page.set_content('<style>'+Source().read('tokens.css')+'</style><div id="ring" style="box-shadow:var(--k-ring-offset)"></div>')
        rings={}
        for theme in ('light','dark'):
            page.evaluate('(theme)=>document.documentElement.dataset.theme=theme',theme)
            page.evaluate("() => document.documentElement.style.setProperty('--k-accent','#745399')")
            rings[theme]=page.locator('#ring').evaluate('(e)=>getComputedStyle(e).boxShadow')
            assert '116, 83, 153' in rings[theme]
        page.close();browser.close()
    diffs={};geometry=[]
    for theme in ('light','dark'):
        diffs[theme]={}
        for target in TARGETS:
            slug=target.split('/')[-1]
            diffs[theme][slug]=pixel_diff(out/f'before19-{theme}-{slug}.png',out/f'restored-{theme}-{slug}.png',out/f'restored-diff-{theme}-{slug}.png')
            if slug in LAB:
                before={v['key']:v for v in facts['before19'][theme][slug]};restored={v['key']:v for v in facts['restored'][theme][slug]}
                for key in sorted(before.keys()&restored.keys()):
                    a=before[key]['shadow'];b=restored[key]['shadow']
                    if a!='none' or b!='none':
                        ga=re.findall(r'[-+]?(?:\d*\.\d+|\d+)px',a);gb=re.findall(r'[-+]?(?:\d*\.\d+|\d+)px',b)
                        geometry.append({'target':slug,'theme':theme,'element':before[key]['element']+before[key]['pseudo'],'before':a,'restored':b,'same_geometry':ga==gb})
                        assert ga==gb,(slug,a,b)
        for phase in phases:sheet([(target.split('/')[-1],out/f'{phase}-{theme}-{target.split("/")[-1]}.png') for target in TARGETS],out/f'{phase}-{theme}-overview.png',columns=2,tile=(440,360))
    result={'before_ref':args.before_ref,'initial19_ref':args.pr19_ref,'geometry':geometry,'pixel_diffs_from_before19':diffs,'rings_follow_foundry_accent':rings,'errors':errors,'drawer_edges':edges,'method':'Seeded JS randomness; paused CSS/SMIL at identical animation progress; actual preview sources; left Drawer positioned only in harness.'}
    (out/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    assert not errors,errors
    print('Restored',len(geometry),'computed shadow geometries; no page errors; rings follow theme/accent')

if __name__=='__main__':main()
