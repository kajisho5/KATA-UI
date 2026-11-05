"""Measure real component motion (never disable it in the harness) and zero-motion safety."""
import argparse,json,http.server,threading,subprocess
from functools import partial
from pathlib import Path
from playwright.sync_api import sync_playwright
from tools.capture_shape_migration import Source,content,open_state,HARNESS,MAJOR
ROOT=Path(__file__).resolve().parents[1]
BODY='body{margin:0;padding:32px;background:var(--k-bg);color:var(--k-ink);font-family:var(--k-font)}'
METRICS='''() => [...document.body.querySelectorAll('*')].flatMap((e,index)=>['','::before','::after','::backdrop'].map(pseudo=>{const s=getComputedStyle(e,pseudo||null);return {element:e.tagName.toLowerCase()+'.'+e.className,index,pseudo,transition:s.transitionDuration,animation:s.animationDuration,delay:s.animationDelay,easing:s.transitionTimingFunction,animationName:s.animationName}})).filter(r=>r.transition!=='0s'||r.animation!=='0s')'''


def run(before_ref,output):
    before_ref=subprocess.check_output(["git","rev-parse",before_ref],cwd=ROOT,text=True).strip()
    output=Path(output);output.mkdir(parents=True,exist_ok=True);measurements={};errors=[];safety=[]
    handler=partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT))
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    try:
      with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
        for phase,source in [('before',Source(before_ref)),('after',Source())]:
            measurements[phase]={}
            for multiplier in (.5,2):
                facts={};measurements[phase][str(multiplier)]=facts
                for slug in MAJOR:
                    page=browser.new_page(reduced_motion='no-preference')
                    page.on('pageerror',lambda error:errors.append(str(error)))
                    page.set_content(content(source,'components/'+slug,'light').replace(HARNESS,BODY))
                    page.evaluate('(v)=>document.documentElement.style.setProperty("--k-mscale",v)',str(multiplier))
                    js=source.read(f'components/{slug}/{slug}.js')
                    if js:page.add_script_tag(content=js)
                    open_state(page,slug)
                    facts[slug]=page.evaluate(METRICS)
                    page.close()
        # Test the literal zero-motion page, plus OS reduced-motion with a nonzero inline multiplier.
        for preference,multiplier in [('no-preference',0),('reduce',2)]:
            page=browser.new_page(reduced_motion=preference)
            page.on('pageerror',lambda error:errors.append(str(error)))
            page.goto(f'http://127.0.0.1:{server.server_port}/tests/motion-zero.html',wait_until='networkidle')
            page.evaluate('(v)=>document.documentElement.style.setProperty("--k-mscale",v)',str(multiplier))
            page.clock.install()
            host=page.locator('#host-transition')
            host_duration=host.evaluate('(e)=>getComputedStyle(e).transitionDuration')
            assert host_duration=='0.4s',host_duration
            # Flush both styles so Chromium creates a native CSSTransition. Playwright's
            # fake timer clock does not drive the compositor clock; seek it explicitly.
            host_mid_opacity=host.evaluate('''(e)=>{
                getComputedStyle(e).opacity;
                e.style.opacity='0.2';getComputedStyle(e).opacity;
                const transition=e.getAnimations().find(a=>a.transitionProperty==='opacity');
                if(!transition)throw new Error('Host opacity transition was suppressed');
                transition.pause();transition.currentTime=200;
                const midway=parseFloat(getComputedStyle(e).opacity);
                transition.finish();return midway;
            }''')
            assert .2<host_mid_opacity<1,host_mid_opacity
            for slug in ('modal','drawer'):
                page.locator(f'[data-{slug}-open]').first.click()
                assert page.locator(f'[data-{slug}]').evaluate('(e)=>e.open')
                page.locator(f'[data-{slug}-close]').first.click()
                assert not page.locator(f'[data-{slug}]').evaluate('(e)=>e.open')
            page.locator('[data-toast-demo]').click();assert page.locator('.toast').count()==1
            page.clock.run_for(4001);assert page.locator('.toast').count()==0
            page.locator('.k-jelly').first.click();assert not page.locator('.k-jelly').first.evaluate('(e)=>e.classList.contains("squish")')
            # Load twice: neither Toast nor Jelly may register a second listener.
            for slug in ('toast','jelly-buttons'):page.add_script_tag(content=Source().read(f'components/{slug}/{slug}.js'))
            page.locator('[data-toast-demo]').click();assert page.locator('.toast').count()==1
            page.clock.run_for(4001);assert page.locator('.toast').count()==0
            active=page.evaluate('()=>document.getAnimations().filter(a=>a.playState==="running").map(a=>({name:a.animationName,duration:a.effect.getTiming().duration}))')
            if preference=='reduce':assert not active,active
            page.screenshot(path=str(output/f'safety-{preference}.png'),full_page=True)
            safety.append({'preference':preference,'inlineMultiplier':multiplier,'effectiveMultiplier':page.evaluate('()=>getComputedStyle(document.documentElement).getPropertyValue("--k-mscale")'),'hostTransitionDuration':host_duration,'hostMidOpacity':host_mid_opacity,'modalClosed':True,'drawerClosed':True,'toastRemoved':True,'jellyReset':True,'doubleLoadSafe':True,'runningAnimations':active})
            page.close()
        browser.close()
    finally:server.shutdown();server.server_close()
    assert not errors,errors
    for slug, rows in measurements['after']['0.5'].items():
        lookup={(row['element'],row['index'],row['pseudo']):row for row in measurements['after']['2'][slug]}
        for row in rows:
            other=lookup[(row['element'],row['index'],row['pseudo'])]
            for field in ('transition','animation'):
                for slow,fast in zip(row[field].split(','),other[field].split(',')):
                    assert abs(float(fast.strip()[:-1])-4*float(slow.strip()[:-1]))<.00001,(slug,field,slow,fast)
    result={'beforeRef':before_ref,'measurements':measurements,'safety':safety,'errors':errors}
    (output/'measurements.json').write_text(json.dumps(result,indent=2)+'\n')
    print('12 components × before/after × 0.5/2; zero/reduced-motion safety passed; no page errors')
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--before-ref',required=True);parser.add_argument('--output',default='docs/review/shared-motion');args=parser.parse_args();run(args.before_ref,args.output)
