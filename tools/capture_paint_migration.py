"""Capture every paint-migrated component and reuse PR #20's text-contrast metric."""
import argparse,json,subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright
from tools.capture_shape_migration import Source,content,open_state,sheet,pixel_diff,HARNESS
from tools.capture_text_contrast import rows
ROOT=Path(__file__).resolve().parents[1]
PARTS=['chip','color-picker','comparison-slider','converge','meteors','meter','spotlight','tilt-card','tooltip']
SEED='''Math.random=(()=>{let state=123456;return ()=>{state=(state*1664525+1013904223)>>>0;return state/4294967296}})();'''


def run(ref,output):
    ref=subprocess.check_output(['git','rev-parse',ref],cwd=ROOT,text=True).strip();output=Path(output);output.mkdir(parents=True,exist_ok=True);facts={};errors=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
        for phase,source in [('before',Source(ref)),('after',Source())]:
            facts[phase]={}
            for theme in ('light','dark'):
                facts[phase][theme]={}
                for slug in PARTS:
                    page=browser.new_page(viewport={'width':900,'height':600},reduced_motion='reduce');page.on('pageerror',lambda error:errors.append(str(error)))
                    page.set_content(content(source,'components/'+slug,theme));page.evaluate(SEED)
                    js=source.read(f'components/{slug}/{slug}.js')
                    if js:page.add_script_tag(content=js)
                    if slug=='tooltip':open_state(page,slug)
                    page.evaluate('()=>document.querySelectorAll("svg").forEach(e=>{e.pauseAnimations();e.setCurrentTime(1)})')
                    page.screenshot(path=str(output/f'{phase}-{theme}-{slug}.png'))
                    facts[phase][theme][slug]=rows(page)
                    if slug=='tooltip':
                        for side in ('top','bottom'):
                            page.locator('[data-tip]').first.evaluate('(e,side)=>e.dataset.side=side',side)
                            page.locator('[data-tip]').first.hover()
                            page.screenshot(path=str(output/f'{phase}-{theme}-tooltip-{side}.png'))
                    if slug=='meteors':
                        # Reduced motion hides meteors. Capture a reproducible paused visible phase too.
                        page.emulate_media(reduced_motion='no-preference')
                        page.set_content(content(source,'components/'+slug,theme).replace(HARNESS,'body{margin:0;padding:32px;background:var(--k-bg);color:var(--k-ink);font-family:var(--k-font)}'))
                        page.evaluate(SEED);page.add_script_tag(content=js)
                        page.evaluate('()=>document.getAnimations().forEach(a=>{a.pause();const t=a.effect.getTiming();a.currentTime=t.delay+t.duration*.35})')
                        page.screenshot(path=str(output/f'{phase}-{theme}-meteors-visible.png'))
                    page.close()
                sheet([(f'{phase} {slug}',output/f'{phase}-{theme}-{slug}.png') for slug in PARTS],output/f'{phase}-{theme}-overview.png',columns=3,tile=(300,200))
        browser.close()
    diffs={}
    for theme in ('light','dark'):
        diffs[theme]={slug:pixel_diff(output/f'before-{theme}-{slug}.png',output/f'after-{theme}-{slug}.png',output/f'diff-{theme}-{slug}.png') for slug in PARTS}
        sheet([(f'{phase} {slug}',output/f'{phase}-{theme}-{slug}.png') for slug in PARTS for phase in ('before','after')],output/f'comparison-{theme}.png',columns=2,tile=(450,300))
    assert not errors,errors
    (output/'measurements.json').write_text(json.dumps({'beforeRef':ref,'parts':PARTS,'facts':facts,'pixelDiffs':diffs,'errors':errors},indent=2)+'\n')
    print('9 changed parts × before/after × light/dark; no page errors')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--before-ref',required=True);parser.add_argument('--output',default='docs/review/shared-paint');args=parser.parse_args();run(args.before_ref,args.output)
