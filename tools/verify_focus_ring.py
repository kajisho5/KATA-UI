"""Measure whether keyboard focus is visible on every part, in light and dark.

For each registry part (components, blocks, templates), the preview is rendered
with its dependency CSS/JS, focus starts on a sentinel button and Tab walks the
part's controls. For every control reached, two crops (control box plus a margin)
are compared: focused and blurred. A control counts as visible when enough pixels
change. A ring whose outline or box-shadow extends past the control is reported
as clipped when an ancestor with non-visible overflow cuts that extent.

This is evidence for HANDOFF T2. It does not change components or checker rules.
"""
import argparse
import http.server
import io
import json
import threading
from functools import partial
from pathlib import Path
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
MARGIN = 8          # px around the control included in each crop
DELTA = 8           # per-channel difference that counts as a changed pixel
RATIO = 3.0         # focused vs blurred contrast for a pixel to count (WCAG non-text 3:1)
VISIBLE = 12        # 3:1 pixels needed to call focus visible
MAX_STOPS = 24      # Tab stops measured per part


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


GEOMETRY = r'''(el)=>{
  const cs=getComputedStyle(el), r=el.getBoundingClientRect();
  const outline=cs.outlineStyle!=='none'&&parseFloat(cs.outlineWidth)>0?Math.max(0,parseFloat(cs.outlineWidth)+(parseFloat(cs.outlineOffset)||0)):0;
  let shadow=0;
  if(cs.boxShadow&&cs.boxShadow!=='none'){
    for(const part of cs.boxShadow.split(/,(?![^(]*\))/)){
      if(/inset/.test(part))continue;
      const nums=(part.replace(/rgba?\([^)]*\)|oklch\([^)]*\)|color\([^)]*\)/g,'').match(/-?[\d.]+px/g)||[]).map(parseFloat);
      const [x=0,y=0,blur=0,spread=0]=nums;shadow=Math.max(shadow,spread+blur/2+Math.max(Math.abs(x),Math.abs(y)));
    }
  }
  const extent=Math.max(outline,shadow);
  let clipped=null;
  if(extent>0){
    const want={l:r.left-extent,t:r.top-extent,r:r.right+extent,b:r.bottom+extent};
    for(let a=el.parentElement;a&&a!==document.body;a=a.parentElement){
      const s=getComputedStyle(a);
      if(s.overflowX==='visible'&&s.overflowY==='visible'&&s.clipPath==='none')continue;
      const c=a.getBoundingClientRect();
      const cut=Math.max(c.left-want.l,c.top-want.t,want.r-c.right,want.b-c.bottom);
      if(cut>0.5){clipped={by:(a.className&&typeof a.className==='string'?'.'+a.className.trim().split(/\s+/).join('.'):a.tagName.toLowerCase()),cut:Math.round(cut*10)/10};break}
    }
  }
  const label=(el.getAttribute('aria-label')||el.textContent||el.getAttribute('placeholder')||el.value||'').trim().replace(/\s+/g,' ').slice(0,40);
  return {box:[r.left,r.top,r.width,r.height],extent:Math.round(extent*10)/10,clipped,outline:cs.outlineStyle!=='none'&&parseFloat(cs.outlineWidth)>0,shadow:cs.boxShadow!=='none',
    tag:el.tagName.toLowerCase(),cls:typeof el.className==='string'?el.className.trim():'',role:el.getAttribute('role')||'',type:el.getAttribute('type')||'',label}
}'''


def _lum(c):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = c[:3]
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def changed(a, b, box):
    """Count changed pixels, pixels whose focused/blurred colors reach 3:1, and strong pixels outside the control."""
    a, b = a.convert('RGB'), b.convert('RGB')
    pa, pb = a.load(), b.load(); w, h = a.size
    x0, y0, x1, y1 = box
    total = strong = outside = 0
    for y in range(h):
        for x in range(w):
            ca, cb = pa[x, y], pb[x, y]
            if max(abs(ca[i] - cb[i]) for i in range(3)) <= DELTA:
                continue
            total += 1
            la, lb = _lum(ca), _lum(cb)
            if (max(la, lb) + 0.05) / (min(la, lb) + 0.05) >= RATIO:
                strong += 1
                if not (x0 <= x < x1 and y0 <= y < y1):
                    outside += 1
    return total, strong, outside


def page_html(head, body):
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Focus ring audit</title>' + head +
            '<style>body{background:var(--k-bg);color:var(--k-ink);font-family:var(--k-font);padding:var(--k-space-6)}</style></head>'
            '<body><button type="button" id="kata-focus-start">Start</button><main id="kata-focus-part">' + body + '</main></body></html>')


def load(page, html, scripts=()):
    """Render one audit page and run the part's scripts once."""
    page.set_content(html)
    for script in scripts:
        page.add_script_tag(content=script)


def measure(page, theme):
    """Walk Tab stops inside #kata-focus-part of the loaded page; one record per control."""
    page.evaluate('(t)=>{document.documentElement.dataset.theme=t;document.documentElement.style.setProperty("--k-mscale","0")}', theme)
    page.wait_for_timeout(50)
    page.keyboard.press('Shift'); page.focus('#kata-focus-start')
    records, seen = [], set()
    for _ in range(MAX_STOPS):
        page.keyboard.press('Tab')
        handle = page.evaluate_handle('()=>{const a=document.activeElement;return a&&document.getElementById("kata-focus-part").contains(a)?a:null}')
        el = handle.as_element()
        if el is None:
            break
        key = el.evaluate('e=>{if(!e.dataset.kataFocusKey)e.dataset.kataFocusKey=String(Math.random());return e.dataset.kataFocusKey}')
        if key in seen:
            break
        seen.add(key)
        geo = el.evaluate(GEOMETRY)
        x, y, w, h = geo['box']
        if w < 1 or h < 1:
            records.append({**geo, 'visible': False, 'level': 'none', 'changed': 0, 'strong': 0, 'outside': 0, 'note': 'zero-size'})
            continue
        vw, vh = page.viewport_size['width'], page.viewport_size['height']
        if y + h > vh or y < 0:
            el.scroll_into_view_if_needed(); geo = el.evaluate(GEOMETRY); x, y, w, h = geo['box']
        clip = {'x': max(0, x - MARGIN), 'y': max(0, y - MARGIN)}
        clip['width'] = min(vw, x + w + MARGIN) - clip['x']; clip['height'] = min(vh, y + h + MARGIN) - clip['y']
        if clip['width'] < 1 or clip['height'] < 1:
            records.append({**geo, 'visible': False, 'level': 'none', 'changed': 0, 'strong': 0, 'outside': 0, 'note': 'off-screen'})
            continue
        page.wait_for_timeout(20)
        focused = Image.open(io.BytesIO(page.screenshot(clip=clip)))
        el.evaluate('e=>e.blur()'); page.wait_for_timeout(20)
        blurred = Image.open(io.BytesIO(page.screenshot(clip=clip)))
        inner = (round(x - clip['x']), round(y - clip['y']), round(x - clip['x'] + w), round(y - clip['y'] + h))
        total, strong, outside = changed(focused, blurred, inner)
        level = 'visible' if strong >= VISIBLE else ('weak' if total >= VISIBLE else 'none')
        records.append({**geo, 'visible': level == 'visible', 'level': level, 'changed': total, 'strong': strong, 'outside': outside})
        # Return to the same control with keyboard modality so Tab continues from it.
        page.keyboard.press('Shift'); el.focus()
    return records


def registry_pages(selected=None):
    registry = json.loads((ROOT / 'dist/registry.json').read_text())
    items = [x for x in registry['items'] if x['type'] != 'registry:theme' and (not selected or x['name'] in selected)]
    by_name = {x['name']: x for x in registry['items']}
    for item in items:
        deps, seen = [], set()
        def visit(it):
            if it['name'] in seen: return
            seen.add(it['name'])
            for name in it.get('dependencies') or []:
                if name in by_name: visit(by_name[name])
            deps.append(it)
        visit(item)
        files = [f for d in deps for f in d['files']]
        html = next(f['content'] for f in item['files'] if f['path'].endswith('.html'))
        head = '<link rel="stylesheet" href="/tokens.css">' + ''.join(f'<link rel="stylesheet" href="/{f["path"]}">' for f in files if f['path'].endswith('.css'))
        scripts = [f['content'] for f in files if f['path'].endswith('.js')]
        yield item, page_html(head, html), scripts


def run(selected=None, output=ROOT / 'docs/review/focus-ring', themes=('light', 'dark')):
    output = Path(output); output.mkdir(parents=True, exist_ok=True)
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    parts, errors = [], []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
            page = browser.new_page(viewport={'width': 1100, 'height': 900})
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.goto(f'http://127.0.0.1:{server.server_port}/tokens.css')
            for item, html, scripts in registry_pages(selected):
                entry = {'id': item['name'], 'type': item['type'].split(':')[-1], 'themes': {}}
                for theme in themes:
                    try:
                        load(page, html, scripts)
                    except Exception as error:
                        errors.append(f'{item["name"]}: {error}')
                    entry['themes'][theme] = measure(page, theme)
                parts.append(entry)
            browser.close()
    finally:
        server.shutdown(); server.server_close()
    report = summarize(parts)
    (output / 'results.json').write_text(json.dumps({'method': {'margin': MARGIN, 'delta': DELTA, 'ratio': RATIO, 'visible': VISIBLE, 'maxStops': MAX_STOPS, 'mscale': 0, 'viewport': [1100, 900]}, 'summary': report, 'parts': parts, 'pageErrors': errors}, indent=1) + '\n')
    return report, parts


def summarize(parts):
    out = {}
    for theme in ('light', 'dark'):
        stops = [r for p in parts for r in p['themes'].get(theme, [])]
        out[theme] = {
            'parts': len(parts), 'partsWithStops': sum(1 for p in parts if p['themes'].get(theme)),
            'stops': len(stops), 'invisible': sum(1 for r in stops if not r['visible']),
            'none': sum(1 for r in stops if r['level'] == 'none'), 'weak': sum(1 for r in stops if r['level'] == 'weak'),
            'clipped': sum(1 for r in stops if r['clipped']),
            'partsWithInvisible': sorted(p['id'] for p in parts if any(not r['visible'] for r in p['themes'].get(theme, []))),
            'partsWithClipped': sorted(p['id'] for p in parts if any(r['clipped'] for r in p['themes'].get(theme, []))),
        }
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('parts', nargs='*')
    args = parser.parse_args()
    report, _ = run(args.parts or None)
    for theme, s in report.items():
        print(f"{theme}: {s['stops']} focus stops in {s['partsWithStops']}/{s['parts']} parts; below 3:1 {s['invisible']} (no change {s['none']}, weak {s['weak']}; {len(s['partsWithInvisible'])} parts); clipped {s['clipped']} ({len(s['partsWithClipped'])} parts)")
