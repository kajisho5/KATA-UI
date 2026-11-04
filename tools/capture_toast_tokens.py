"""Compare the Toast rendered before a ref and in the worktree (requires Playwright)."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
FILES=['tokens.css','components/button/button.css','components/toast/toast.css']


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--before-ref',required=True)
    parser.add_argument('--chromium',default='/usr/bin/chromium')
    parser.add_argument('--output',default='docs/review/toast-local-tokens')
    args=parser.parse_args();out=ROOT/args.output;out.mkdir(parents=True,exist_ok=True)
    facts={};errors=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=args.chromium,args=['--no-sandbox'])
        for phase in ('before','after'):
            def read(name):
                if phase=='after':return (ROOT/name).read_text()
                return subprocess.run(['git','show',args.before_ref+':'+name],cwd=ROOT,text=True,capture_output=True,check=True).stdout
            facts[phase]={}
            for theme in ('light','dark'):
                page=browser.new_page(viewport={'width':800,'height':400},reduced_motion='reduce')
                page.on('pageerror',lambda e:errors.append(str(e)))
                page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
                css=''.join(read(name) for name in FILES)
                html=read('components/toast/preview.html').split('<link')[0]
                page.set_content(f'<!doctype html><html lang="en" data-theme="{theme}"><head><style>'+css+'body{background:var(--k-bg);color:var(--k-ink)}</style></head><body>'+html+'</body></html>')
                page.add_script_tag(content=read('components/toast/toast.js'))
                page.locator('[data-toast-demo]').click();page.locator('.toast').wait_for()
                colors=page.locator('.toast').evaluate('(e)=>({color:getComputedStyle(e).color,background:getComputedStyle(e).backgroundColor,sub:getComputedStyle(e.querySelector("small")).color})')
                png=page.screenshot(path=str(out/f'{phase}-{theme}.png'),animations='disabled')
                facts[phase][theme]={'colors':colors,'sha256':hashlib.sha256(png).hexdigest()}
                page.close()
        version=browser.version;browser.close()
    result={'before_ref':args.before_ref,'browser':version,'viewport':[800,400],'reduced_motion':'reduce','facts':facts,'errors':errors}
    (out/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    assert facts['before']==facts['after'], 'Toast render changed'
    assert not errors,errors
    print('Toast: identical PNG bytes and computed colors in light/dark; no console/page errors')

if __name__=='__main__':main()
