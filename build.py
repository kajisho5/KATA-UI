#!/usr/bin/env python3
"""KATA UI — static site generator. Registry (components/) is the source of truth."""
import hashlib, html, json, re, shutil
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / 'dist'
CATS = ['Form & Input', 'Layout & Navigation', 'Overlays & Dialogs', 'Feedback & Status', 'Display & Media', 'Motion']

def load_components():
    comps = []
    for d in sorted((ROOT / 'components').iterdir()):
        if not d.is_dir():
            continue
        meta = json.loads((d / 'meta.json').read_text(encoding='utf-8'))
        slug = d.name
        preview = (d / 'preview.html').read_text(encoding='utf-8')
        css = (d / f'{slug}.css').read_text(encoding='utf-8')
        js_file = d / f'{slug}.js'
        js = js_file.read_text(encoding='utf-8') if js_file.exists() else None
        deps = sorted(set(re.findall(r'/components/([a-z0-9-]+)/\1\.css', preview))) 
        deps = [x for x in deps if x != slug]
        comps.append(dict(slug=slug, meta=meta, preview=preview, css=css, js=js, deps=deps))
    order = {c: i for i, c in enumerate(CATS)}
    comps.sort(key=lambda c: (order.get(c['meta']['category'], 99), c['meta']['title']))
    return comps

def esc(s):
    return html.escape(s)

HEADER = """<header class="top"><div class="wrap top-in">
  <a class="logo" href="/"><svg width="27" height="27" viewBox="0 0 48 48" aria-hidden="true"><rect x="6" y="6" width="36" height="36" rx="9" fill="none" stroke="#18181b" stroke-width="4"/><rect x="19" y="19" width="10" height="10" rx="3" fill="#eb471f"/></svg>KATA UI<small>preview</small></a>
  <button class="menubtn" id="menubtn" type="button" aria-label="Open component menu">☰<span>Components</span></button>
  <nav><a href="/components/">Components</a><a href="/blocks/">Blocks</a><a href="/design-system/">Design System</a><a href="/icons/">Icons</a><a href="/#catalog">Categories</a><a href="#">Pricing</a></nav>
  <a class="gh" href="https://github.com/kajisho5/KATA-UI" rel="noopener">GitHub</a>
</div></header>"""

FOOTER = """<div class="wrap"><footer class="site">
  <span>KATA UI (working title) — a store of UI parts &amp; code.</span>
  <span style="margin-left:auto">Every part runs on vanilla HTML, CSS &amp; JS</span>
</footer></div>"""


def _v(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()[:8]

def drawer_html(comps, active):
    return f"""
<div class="scrim" id="scrim"></div>
<nav class="drawer" id="drawer" aria-label="All components">
  <div class="dhead"><span>Components</span><button class="dclose" id="dclose" type="button" aria-label="Close menu">✕</button></div>
  {sidebar(comps, active)}
</nav>"""

DRAWER_JS = """<script>
(function(){var mb=document.getElementById('menubtn');if(!mb)return;
function setD(o){document.body.classList.toggle('dopen',o);}
mb.addEventListener('click',function(){setD(true);});
var dc=document.getElementById('dclose');if(dc)dc.addEventListener('click',function(){setD(false);});
var sc=document.getElementById('scrim');if(sc)sc.addEventListener('click',function(){setD(false);});
document.addEventListener('keydown',function(e){if(e.key==='Escape')setD(false);});
document.querySelectorAll('.side a.on').forEach(function(a){var c=a.closest('.drawer')||a.parentElement;if(c){try{c.scrollTop=Math.max(0,a.offsetTop-80);}catch(e){}}});
})();
</script>"""

def emit(page, comps, active):
    return page.replace('</body>', drawer_html(comps, active) + DRAWER_JS + '</body>', 1)

def head(title, desc, extra=''):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="stylesheet" href="/tokens.css?v={_v((ROOT / 'tokens.css').read_text(encoding='utf-8'))}">
<link rel="stylesheet" href="/site.css?v={_v((ROOT / 'site.css').read_text(encoding='utf-8'))}">
{extra}
</head>
<body>
{HEADER}
"""

def card(c):
    m = c['meta']
    tags = ''.join(f'<span class="tag">{esc(t)}</span>' for t in m.get('tags', []))
    return f"""<a class="card" href="/components/{c['slug']}/">
  <h3>{esc(m['title'])} <span class="st st-{esc(m.get('status','stable'))}">{esc(m.get('status','stable'))}</span></h3>
  <p>{esc(m['description'])}</p>
  <span class="tags">{tags}</span>
</a>"""

def catalog_sections(comps):
    out = []
    for cat in CATS:
        group = [c for c in comps if c['meta']['category'] == cat]
        if not group:
            continue
        cards = '\n'.join(card(c) for c in group)
        out.append(f'<section class="catsec"><h2>{esc(cat)}</h2><div class="cards">\n{cards}\n</div></section>')
    return '\n'.join(out)

LP_STYLE = """<style>
.lp .hero{padding:64px 0 8px;text-align:center}
.lp .hero h1{font-size:44px;line-height:1.12}
.lp .hero p{margin-left:auto;margin-right:auto}
.lp .cta{justify-content:center}
.lp .stats{justify-content:center}
.browser{margin:38px auto 0;max-width:880px;border:1px solid var(--hair);border-radius:14px;overflow:hidden;background:#fff;box-shadow:0 30px 70px -30px rgba(16,24,40,.25);text-align:left}
.browser-bar{display:flex;align-items:center;gap:7px;padding:10px 14px;border-bottom:1px solid var(--hair);background:var(--soft)}
.browser-bar i{width:10px;height:10px;border-radius:50%;background:var(--hair);display:block}
.browser-bar .url{margin-left:8px;font-family:var(--mono);font-size:11px;color:var(--ink3);border:1px solid var(--hair);border-radius:6px;padding:3px 10px;background:#fff}
.browser .shell{border:0;border-radius:0}
.framecap{max-width:880px;margin:10px auto 0;text-align:right;font-size:12px;color:var(--ink3)}
.framecap a{color:var(--ink2)}
.lpsec{margin-top:64px}
.lpsec h2{font-size:22px;font-weight:600;letter-spacing:-.02em}
.lpsec .sub{margin-top:7px;color:var(--ink2);font-size:14px;line-height:1.8;max-width:62ch}
.steps{margin-top:20px;display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px}
.step{border:1px solid var(--hair);border-radius:12px;background:#fff;padding:18px}
.step .no{font-family:var(--mono);font-size:11px;color:var(--acc);font-weight:600;letter-spacing:.08em}
.step h3{margin-top:8px;font-size:15px;font-weight:600}
.step p{margin-top:6px;font-size:13px;color:var(--ink2);line-height:1.75}
.step code{font-family:var(--mono);font-size:12px;background:var(--soft);border-radius:5px;padding:1px 5px}
.genres{margin-top:20px;display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px}
.genre{border:1px solid var(--hair);border-radius:12px;background:#fff;padding:18px;text-decoration:none;color:var(--ink);display:block}
.genre:hover{border-color:var(--ink3)}
.genre .gn{font-family:var(--mono);font-size:11px;color:var(--ink3);letter-spacing:.06em}
.genre h3{margin-top:7px;font-size:15.5px;font-weight:600}
.genre p{margin-top:6px;font-size:13px;color:var(--ink2);line-height:1.75}
.compat{margin-top:20px;border:1px solid var(--hair);border-radius:12px;background:var(--soft);padding:18px;font-size:13.5px;line-height:1.9;color:var(--ink2)}
.compat b{color:var(--ink);font-weight:600}
.compat a{color:var(--ink);font-weight:550}
@media (max-width:720px){.lp .hero h1{font-size:33px}.browser .shell-side{display:none}}
</style>"""

def landing(comps, blocks, n_icons):
    n = len(comps)
    nb = len(blocks)
    shell = next((b for b in blocks if b['slug'] == 'app-shell'), None)
    shell_html = shell['preview'] if shell else ''
    body = f"""
<div class="wrap lp">
  <div class="hero">
    <span class="eyebrow"><i></i>Vanilla components — no framework, no build step</span>
    <h1>Parts, cast from a single mold.<br><span class="dim">Copy the code. Own the design.</span></h1>
    <p>From buttons to app shells — practical components in plain HTML, CSS and JS, each with a live preview and copy-ready code. Every part is cast from a single mold — kata, the Japanese discipline of the form.</p>
    <div class="cta">
      <a class="kbtn-primary" href="/components/" style="display:inline-flex;align-items:center;height:42px;padding:0 20px;border-radius:9px;background:#18181b;color:#fff;font-weight:500;font-size:14px;text-decoration:none">Browse components</a>
      <a href="/blocks/" style="display:inline-flex;align-items:center;height:42px;padding:0 20px;border-radius:9px;border:1px solid var(--hair);font-weight:500;font-size:14px;text-decoration:none;background:#fff">See blocks</a>
    </div>
    <div class="stats">
      <div><b>{n}</b><span>components</span></div>
      <div><b>{nb}</b><span>blocks</span></div>
      <div><b>{n_icons}</b><span>icons</span></div>
      <div><b>0</b><span>dependencies</span></div>
    </div>
  </div>
  <div class="browser" aria-hidden="true">
    <div class="browser-bar"><i></i><i></i><i></i><span class="url">your-app.com</span></div>
{shell_html}
  </div>
  <p class="framecap">A working screen built only from KATA parts — the <a href="/blocks/app-shell/">App Shell</a> block.</p>
  <section class="lpsec">
    <h2>How it works</h2>
    <div class="steps">
      <div class="step"><span class="no">STEP 1</span><h3>Take the tokens</h3><p>Load <code>tokens.css</code> once. Every part reads its color, spacing, radius and motion from it — that file is the mold.</p></div>
      <div class="step"><span class="no">STEP 2</span><h3>Paste the part</h3><p>Copy the HTML, the CSS and the JS from the part's page. No install, no package, nothing phoning home.</p></div>
      <div class="step"><span class="no">STEP 3</span><h3>Make it yours</h3><p>Adjust the tokens, not the parts. One change in the mold re-casts everything on the page.</p></div>
    </div>
  </section>
  <section class="lpsec">
    <h2>Four genres, one mold</h2>
    <div class="genres">
      <a class="genre" href="/components/"><span class="gn">{n} PARTS</span><h3>Components</h3><p>The single parts: forms, overlays, feedback, display — and a Motion line other libraries do not carry.</p></a>
      <a class="genre" href="/blocks/"><span class="gn">{nb} SECTIONS</span><h3>Blocks</h3><p>Whole sections composed from the parts — sign-in, pricing, settings, an app shell. Start here, take apart later.</p></a>
      <a class="genre" href="/icons/"><span class="gn">{n_icons} GLYPHS</span><h3>Icons</h3><p>One mold: a 24 grid, a 2px stroke, three shapes only. Click to copy, and Lucide mixes in without a seam.</p></a>
      <a class="genre" href="/design-system/"><span class="gn">TOKENS.JSON</span><h3>Design System</h3><p>The foundation every part is cast from — color, type, spacing, radius, motion. Download it, diff it, fork it.</p></a>
    </div>
    <div class="compat">
      <b>Drops into</b> plain HTML, Astro, Laravel, Django, Rails and WordPress themes — anywhere that renders HTML, with no React island required.<br>
      <b>For AI tools</b>, KATA speaks their formats: <a href="/registry.json">registry.json</a> for installers and agents, <a href="/llms.txt">llms.txt</a> for models that read the web.
    </div>
  </section>
  <div id="catalog">
{catalog_sections(comps)}
  </div>
</div>
{FOOTER}
</body>
</html>"""
    extra = '<link rel="stylesheet" href="/blocks/app-shell/app-shell.css">'
    return head('KATA UI — UI Components & Code', 'Vanilla UI components with live previews and copy-ready code. No framework, no build step.', LP_STYLE + extra) + body

def registry_json(comps, blocks):
    items = []
    for c in comps:
        m = c['meta']
        files = [{'path': f"components/{c['slug']}/{c['slug']}.css", 'type': 'registry:component', 'content': c['css']}]
        if c['js']:
            files.append({'path': f"components/{c['slug']}/{c['slug']}.js", 'type': 'registry:component', 'content': c['js']})
        example = re.sub(r'\s*<link rel="stylesheet"[^>]*>', '', c['preview']).strip()
        files.append({'path': f"components/{c['slug']}/example.html", 'type': 'registry:component', 'content': example})
        items.append({'name': c['slug'], 'type': 'registry:component', 'title': m['title'],
                      'description': m['description'], 'categories': [m['category']],
                      'dependencies': c['deps'], 'files': files})
    for b in blocks:
        m = b['meta']
        files = [{'path': f"blocks/{b['slug']}/{b['slug']}.css", 'type': 'registry:block', 'content': b['css']}]
        if b['js']:
            files.append({'path': f"blocks/{b['slug']}/{b['slug']}.js", 'type': 'registry:block', 'content': b['js']})
        example = re.sub(r'\s*<link rel="stylesheet"[^>]*>', '', b['preview']).strip()
        files.append({'path': f"blocks/{b['slug']}/example.html", 'type': 'registry:block', 'content': example})
        items.append({'name': b['slug'], 'type': 'registry:block', 'title': m['title'],
                      'description': m['description'], 'categories': ['Blocks'],
                      'dependencies': m.get('uses', []), 'files': files})
    return json.dumps({'$schema': 'https://ui.shadcn.com/schema/registry.json', 'name': 'kata-ui',
                       'homepage': 'https://kata-ui.dev', 'items': items}, ensure_ascii=False, indent=1)

def llms_txt(comps, blocks, n_icons):
    lines = ['# KATA UI', '',
             '> Practical UI components in plain HTML, CSS and JavaScript. No framework, no build step. Every part is cast from a single design-token mold; copy the code and own it.', '',
             'KATA is framework-free: parts drop into plain HTML, Astro, Laravel, Django, Rails and templates unchanged. Components depend on tokens.css (design tokens) being loaded once.', '',
             '## Docs', '',
             '- [Design System](https://kata-ui.dev/design-system/): the tokens every part is cast from (tokens.json is downloadable there)',
             f'- [Icons](https://kata-ui.dev/icons/): {n_icons} icons on one mold (24 grid, 2px stroke); click to copy the SVG',
             '- [Registry](https://kata-ui.dev/registry.json): every component and block with its full CSS/JS/HTML, in the shadcn registry format', '',
             '## Components', '']
    for c in comps:
        lines.append(f"- [{c['meta']['title']}](https://kata-ui.dev/components/{c['slug']}/): {c['meta']['description']}")
    lines += ['', '## Blocks', '']
    for b in blocks:
        lines.append(f"- [{b['meta']['title']}](https://kata-ui.dev/blocks/{b['slug']}/): {b['meta']['description']}")
    lines.append('')
    return '\n'.join(lines)

def llms_full(comps, blocks):
    out = ['# KATA UI — full text', '',
           'Vanilla UI components: HTML, CSS and JS for every part, plus the design tokens.', '',
           '## Design tokens (tokens.css)', '', '```css', (ROOT / 'tokens.css').read_text(encoding='utf-8').strip(), '```', '']
    for c in comps:
        m = c['meta']
        example = re.sub(r'\s*<link rel="stylesheet"[^>]*>', '', c['preview']).strip()
        out += [f"## Component: {m['title']} ({c['slug']})", '', m['description'], '',
                f"Usage: {m.get('usage','')}", '', '### HTML', '', '```html', example, '```', '',
                '### CSS', '', '```css', c['css'].strip(), '```', '']
        if c['js']:
            out += ['### JS', '', '```js', c['js'].strip(), '```', '']
    for b in blocks:
        m = b['meta']
        example = re.sub(r'\s*<link rel="stylesheet"[^>]*>', '', b['preview']).strip()
        out += [f"## Block: {m['title']} ({b['slug']})", '', m['description'], '',
                'Built from: ' + ', '.join(m.get('uses', [])), '', '### HTML', '', '```html', example, '```', '',
                '### CSS (glue)', '', '```css', b['css'].strip(), '```', '']
        if b['js']:
            out += ['### JS', '', '```js', b['js'].strip(), '```', '']
    return '\n'.join(out)


def components_index(comps):
    body = f"""
<div class="wrap">
  <div class="hero" style="padding-bottom:0">
    <h1 style="font-size:36px">Components</h1>
    <p>Every part is a folder in the registry — preview, CSS and JS are the same files you copy.</p>
  </div>
{catalog_sections(comps)}
</div>
{FOOTER}
</body>
</html>"""
    return head('Components — KATA UI', 'All KATA UI components.', '') + body

def sidebar(comps, active):
    out = []
    for cat in CATS:
        group = [c for c in comps if c['meta']['category'] == cat]
        if not group:
            continue
        out.append(f'<h4>{esc(cat)}</h4>')
        for c in group:
            on = ' class="on"' if c['slug'] == active else ''
            out.append(f'<a href="/components/{c["slug"]}/"{on}>{esc(c["meta"]["title"])}</a>')
    return '<aside class="side">' + '\n'.join(out) + '</aside>'

DETAIL_JS = """<script>
  const stage = document.getElementById('stage');
  document.querySelectorAll('[data-seg]').forEach(seg => {
    seg.querySelectorAll('button').forEach(btn => btn.addEventListener('click', () => {
      seg.querySelectorAll('button').forEach(b => b.classList.remove('on'));
      btn.classList.add('on');
      const v = btn.dataset.v;
      if (seg.dataset.seg === 'theme') { v === 'dark' ? stage.setAttribute('data-theme','dark') : stage.removeAttribute('data-theme'); }
      if (seg.dataset.seg === 'width') { stage.classList.toggle('narrow', v === 'mobile'); }
    }));
  });
  document.querySelectorAll('.codetabs button').forEach(btn => btn.addEventListener('click', () => {
    const box = btn.closest('.codebox');
    box.querySelectorAll('.codetabs button').forEach(b => b.classList.remove('on'));
    box.querySelectorAll('.pane').forEach(p => p.classList.remove('on'));
    btn.classList.add('on');
    box.querySelector('.pane[data-pane="' + btn.dataset.tab + '"]').classList.add('on');
  }));
  document.querySelectorAll('.copybtn').forEach(btn => btn.addEventListener('click', () => {
    const pre = btn.closest('.pane').querySelector('pre');
    if (navigator.clipboard) navigator.clipboard.writeText(pre.innerText);
    btn.textContent = 'Copied';
    setTimeout(() => btn.textContent = 'Copy', 1600);
  }));
</script>"""

def detail(comps, idx):
    c = comps[idx]
    m = c['meta']
    slug = c['slug']
    display_html = re.sub(r'\s*<link rel="stylesheet"[^>]*>', '', c['preview']).strip()
    tabs = [('HTML', display_html), ('CSS', c['css'])]
    if c['js']:
        tabs.append(('JS', c['js']))
    def tab_btn(i, name):
        on = ' class="on"' if i == 0 else ''
        return f'<button data-tab="{name}"{on}>{name}</button>'
    tab_btns = ''.join(tab_btn(i, name) for i, (name, _) in enumerate(tabs))
    panes = ''.join(
        f'<div class="pane{" on" if i == 0 else ""}" data-pane="{name}"><pre>{esc(code)}</pre><div class="copyrow"><button class="copybtn">Copy</button></div></div>'
        for i, (name, code) in enumerate(tabs))
    deps_html = ''
    if c['deps']:
        by_slug = {x['slug']: x for x in comps}
        links = ', '.join(f'<a href="/components/{d}/">{esc(by_slug[d]["meta"]["title"])}</a>' for d in c['deps'] if d in by_slug)
        deps_html = f'<p class="deps">Uses: {links} — include its CSS alongside this one.</p>'
    prev_html = next_html = '<span style="flex:1"></span>'
    if idx > 0:
        p = comps[idx - 1]
        prev_html = f'<a href="/components/{p["slug"]}/"><span class="dir">Previous</span><div class="nm">{esc(p["meta"]["title"])}</div></a>'
    if idx < len(comps) - 1:
        nx = comps[idx + 1]
        next_html = f'<a class="next" href="/components/{nx["slug"]}/"><span class="dir">Next</span><div class="nm">{esc(nx["meta"]["title"])}</div></a>'
    stage_cls = 'stage col' if m.get('stage') == 'col' else 'stage'
    js_tag = f'<script src="/components/{slug}/{slug}.js?v={_v(c["js"])}"></script>' if c['js'] else ''
    body = f"""
<div class="wrap">
  <div class="layout">
    {sidebar(comps, slug)}
    <main class="detail">
      <p class="crumb"><a href="/components/">Components</a> / {esc(m['category'])} / {esc(m['title'])}</p>
      <h1>{esc(m['title'])} <span class="st st-{esc(m.get('status','stable'))}">{esc(m.get('status','stable'))}</span></h1>
      <p class="desc">{esc(m['description'])}</p>
      <div class="stagebar">
        <span class="lbl">Preview</span>
        <span class="seg" data-seg="width"><button data-v="desktop" class="on">Desktop</button><button data-v="mobile">Mobile</button></span>
        <span class="seg" data-seg="theme"><button data-v="light" class="on">Light</button><button data-v="dark">Dark</button></span>
      </div>
      <div class="{stage_cls}" id="stage">
{c['preview']}
      </div>
      {deps_html}
      <div class="codebox">
        <div class="codetabs">{tab_btns}</div>
        {panes}
      </div>
      <section class="doc"><h2>Usage</h2><p>{esc(m.get('usage',''))}</p></section>
      <section class="doc"><h2>Accessibility</h2><p>{esc(m.get('a11y',''))}</p></section>
      <div class="prevnext">{prev_html}{next_html}</div>
    </main>
  </div>
</div>
{FOOTER}
{js_tag}
{DETAIL_JS}
</body>
</html>"""
    extra = f'<link rel="stylesheet" href="/components/{slug}/{slug}.css?v={_v(c["css"])}">'
    return head(f"{m['title']} — KATA UI", m['description'], extra) + body


DS_STYLE = """<style>
.ds h1{font-size:32px;font-weight:600;letter-spacing:-.025em;margin-top:26px}
.ds .lead{margin-top:10px;color:var(--ink2);font-size:15px;line-height:1.85;max-width:64ch}
.ds section{margin-top:46px}
.ds h2{font-size:19px;font-weight:600;letter-spacing:-.015em}
.ds .note{margin-top:7px;color:var(--ink2);font-size:13.5px;line-height:1.8;max-width:66ch}
.swatches{margin-top:16px;display:grid;grid-template-columns:repeat(auto-fill,minmax(96px,1fr));gap:9px}
.sw{border:1px solid var(--hair);border-radius:10px;overflow:hidden;background:#fff}
.sw .fill{height:44px}
.sw .meta{padding:7px 9px;font-family:var(--mono);font-size:10.5px;color:var(--ink2);line-height:1.6}
.sw .meta b{color:var(--ink);font-weight:600}
.roles{margin-top:14px;display:grid;gap:7px;font-size:13.5px;color:var(--ink2)}
.roles b{color:var(--ink);font-family:var(--mono);font-size:12px;font-weight:600}
.spec{margin-top:14px;border-top:1px solid var(--hair)}
.spec .row{display:flex;align-items:baseline;gap:18px;padding:11px 2px;border-bottom:1px solid #f0f0f2}
.spec .tag{font-family:var(--mono);font-size:11px;color:var(--ink3);width:74px;flex:none}
.spec .sample{font-weight:600;letter-spacing:-.02em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.bars{margin-top:14px;display:grid;gap:9px}
.bars .row{display:flex;align-items:center;gap:14px;font-family:var(--mono);font-size:11.5px;color:var(--ink2)}
.bars .bar{height:14px;background:var(--ink);border-radius:4px}
.radii{margin-top:14px;display:flex;gap:12px;flex-wrap:wrap}
.radii .box{width:74px;height:56px;border:1.5px solid var(--ink);display:flex;align-items:flex-end;justify-content:center;padding-bottom:6px;font-family:var(--mono);font-size:10.5px;color:var(--ink2)}
.motions{margin-top:14px;display:flex;gap:12px;flex-wrap:wrap}
.motions .m{flex:1;min-width:150px;border:1px solid var(--hair);border-radius:12px;padding:14px;background:#fff;font-size:12.5px;color:var(--ink2)}
.motions .dot{width:16px;height:16px;border-radius:50%;background:var(--ink);margin-top:10px;transition:transform var(--dur) cubic-bezier(.3,.7,.3,1)}
.motions .m:hover .dot{transform:translateX(56px)}
.dl{margin-top:16px;display:flex;gap:9px;flex-wrap:wrap}
.dl a{border:1px solid var(--hair);border-radius:8px;padding:9px 14px;font-size:13px;font-weight:500;text-decoration:none;background:#fff}
.dl a:hover{background:var(--soft)}
</style>"""


ICONS_STYLE = """<style>
.ic h1{font-size:32px;font-weight:600;letter-spacing:-.025em;margin-top:26px}
.ic .lead{margin-top:10px;color:var(--ink2);font-size:15px;line-height:1.85;max-width:64ch}
.icgrid{margin-top:26px;display:grid;grid-template-columns:repeat(auto-fill,minmax(104px,1fr));gap:9px}
.iccell{border:1px solid var(--hair);border-radius:12px;background:#fff;padding:16px 6px 11px;display:grid;justify-items:center;gap:9px;cursor:pointer;font:inherit;color:var(--ink)}
.iccell:hover{border-color:var(--ink3)}
.iccell .nm{font-family:var(--mono);font-size:10.5px;color:var(--ink2)}
.icstat{margin-top:14px;font-size:13px;color:var(--ink2);min-height:20px}
.icstat b{color:var(--acc);font-weight:600}
</style>"""

def icons_page():
    import json as _json
    files = sorted((ROOT / 'icons').glob('*.svg'))
    data = {}
    cells = []
    for f in files:
        raw = f.read_text(encoding='utf-8').strip()
        data[f.stem] = raw
        inline = raw.replace('<svg ', '<svg width="22" height="22" aria-hidden="true" ', 1)
        cells.append('<button class="iccell" type="button" data-icon="' + f.stem + '">' + inline + '<span class="nm">' + f.stem + '</span></button>')
    script = "<script>var ICONS=__DATA__;\ndocument.querySelectorAll('[data-icon]').forEach(function(b){b.addEventListener('click',function(){var n=b.dataset.icon;var done=function(){document.getElementById('icstat').innerHTML='<b>'+n+'</b> copied.';};if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(ICONS[n]).then(done,done);}else{done();}});});\n</script>".replace('__DATA__', _json.dumps(data))
    body = "\n<div class=\"wrap ic\">\n  <h1>Icons</h1>\n  <p class=\"lead\">One mold for icons, too: a 24 grid, a 2px stroke, round caps and joins. Every glyph is drawn from three shapes only — the circle, the 45° line, and the r2 corner — so the whole set reads as cut from one block. A few carry the KATA signature: a solid core at the center, the same mark that sits inside the Switch, the Radio and the logo. Click any icon to copy its SVG. For anything beyond this set, Lucide speaks the same mold (24 / 2 / round) and mixes in without a seam.</p>\n  <p class=\"icstat\" id=\"icstat\">" + str(len(files)) + " icons. Every one is a single file in the registry.</p>\n  <div class=\"icgrid\">" + ''.join(cells) + "</div>\n</div>\n" + FOOTER + "\n" + script + "\n</body>\n</html>"
    return head('Icons — KATA UI', 'The KATA icon set: 24 grid, 2px stroke, click to copy the SVG.', ICONS_STYLE) + body

def design_system_page(tokens):
    def swatches(scale_name, scale):
        cells = ''.join(
            f'<div class="sw"><div class="fill" style="background:{v}"></div><div class="meta"><b>{scale_name}-{k}</b><br>{v}</div></div>'
            for k, v in scale.items())
        return f'<div class="swatches">{cells}</div>'
    roles = ''.join(f'<div><b>--{k}</b> — {esc(v)}</div>' for k, v in tokens['color']['roles'].items())
    specs = ''.join(
        f'<div class="row"><span class="tag">{k} · {v}px</span><span class="sample" style="font-size:{v}px">Design, cast in a mold</span></div>'
        for k, v in tokens['typeScalePx'].items())
    bars = ''.join(
        f'<div class="row"><span style="width:64px">space-{k}</span><span class="bar" style="width:{v}px"></span><span>{v}px</span></div>'
        for k, v in tokens['spacePx'].items())
    radii = ''.join(
        f'<div class="box" style="border-radius:{v}px">{k} · {v}</div>' for k, v in tokens['radiusPx'].items())
    body = f"""
<div class="wrap ds">
  <h1>Design System</h1>
  <p class="lead">The foundation every KATA component is cast from: color, type, spacing, radius, motion. One accent, hairline borders, flat surfaces — and tokens for everything, so the system survives every theme.</p>
  <div class="dl">
    <a href="/tokens.css">tokens.css</a>
    <a href="/design-system/tokens.json">tokens.json</a>
    <a href="/components/">Browse components</a>
  </div>
  <section><h2>Color — Zinc</h2><p class="note">The dominant scale. Interfaces are built from zinc first; color is the exception.</p>{swatches('zinc', tokens['color']['zinc'])}</section>
  <section><h2>Color — Teal (the one accent)</h2><p class="note">A single accent, used sparingly: links, highlights, the core of the mark. If everything is teal, nothing is.</p>{swatches('teal', tokens['color']['teal'])}</section>
  <section><h2>Color — Roles</h2><div class="roles">{roles}</div></section>
  <section><h2>Typography</h2><p class="note">Sans: {esc(tokens['font']['sans'])}<br>Mono: {esc(tokens['font']['mono'])}<br>Tracking: {esc(tokens['font']['tracking'])}</p><div class="spec">{specs}</div></section>
  <section><h2>Spacing</h2><p class="note">A 4px base. If a gap is not on this scale, it is a mistake.</p><div class="bars">{bars}</div></section>
  <section><h2>Radius</h2><div class="radii">{radii}</div></section>
  <section><h2>Heights</h2><p class="note">Controls come in three heights — 32 / 38 / 44px. Shared heights are what make separate components look like one system.</p></section>
  <section><h2>Motion</h2><p class="note">{esc(tokens['motion']['rule'])} Hover the cards:</p>
    <div class="motions">
      <div class="m" style="--dur:130ms">fast · 130ms<div class="dot"></div></div>
      <div class="m" style="--dur:180ms">base · 180ms<div class="dot"></div></div>
      <div class="m" style="--dur:220ms">slow · 220ms<div class="dot"></div></div>
    </div></section>
  <section><h2>Elevation</h2><p class="note">{esc(tokens['elevation']['rule'])}</p></section>
</div>
{FOOTER}
</body>
</html>"""
    return head('Design System — KATA UI', 'The KATA design system: color, type, spacing, radius and motion tokens.', DS_STYLE) + body


def load_blocks():
    blocks = []
    bdir = ROOT / 'blocks'
    if not bdir.exists():
        return blocks
    for d in sorted(bdir.iterdir()):
        if not d.is_dir():
            continue
        meta = json.loads((d / 'meta.json').read_text(encoding='utf-8'))
        slug = d.name
        preview = (d / 'preview.html').read_text(encoding='utf-8')
        css = (d / f'{slug}.css').read_text(encoding='utf-8')
        js_file = d / f'{slug}.js'
        js = js_file.read_text(encoding='utf-8') if js_file.exists() else None
        blocks.append(dict(slug=slug, meta=meta, preview=preview, css=css, js=js))
    blocks.sort(key=lambda b: b['meta']['title'])
    return blocks

BLOCK_STYLE = """<style>
.bk h1{font-size:32px;font-weight:600;letter-spacing:-.025em;margin-top:26px}
.bk .lead{margin-top:10px;color:var(--ink2);font-size:15px;line-height:1.85;max-width:64ch}
.bcards{margin-top:26px;display:grid;grid-template-columns:repeat(auto-fill,minmax(264px,1fr));gap:12px}
.bcard{border:1px solid var(--hair);border-radius:14px;background:#fff;padding:18px;text-decoration:none;color:var(--ink);display:block}
.bcard:hover{border-color:var(--ink3)}
.bcard h3{font-size:15.5px;font-weight:600;display:flex;align-items:center;gap:8px}
.bcard p{margin-top:7px;font-size:13px;color:var(--ink2);line-height:1.75}
.bcard .uses{margin-top:12px;display:flex;gap:5px;flex-wrap:wrap}
.bcard .uses span{font-family:var(--mono);font-size:10.5px;color:var(--ink2);border:1px solid var(--hair);border-radius:99px;padding:2px 8px}
</style>"""

def blocks_index(blocks):
    cards = []
    for b in blocks:
        m = b['meta']
        uses = ''.join(f'<span>{esc(u)}</span>' for u in m.get('uses', []))
        cards.append(f"""<a class="bcard" href="/blocks/{b['slug']}/">
  <h3>{esc(m['title'])} <span class="st st-{esc(m.get('status','beta'))}">{esc(m.get('status','beta'))}</span></h3>
  <p>{esc(m['description'])}</p>
  <span class="uses">{uses}</span>
</a>""")
    body = f"""
<div class="wrap bk">
  <h1>Blocks</h1>
  <p class="lead">Components, composed into whole sections. A block is copied the same way as a component — HTML, CSS and JS — and every part inside it stays a part you already own. Start from a block, then take it apart with the catalog.</p>
  <div class="bcards">
{''.join(cards)}
  </div>
</div>
{FOOTER}
</body>
</html>"""
    return head('Blocks — KATA UI', 'Whole sections composed from KATA components: sign-in, pricing, settings, app shells.', BLOCK_STYLE) + body

def block_detail(blocks, idx, comps):
    b = blocks[idx]
    m = b['meta']
    slug = b['slug']
    display_html = re.sub(r'\s*<link rel="stylesheet"[^>]*>', '', b['preview']).strip()
    tabs = [('HTML', display_html), ('CSS', b['css'])]
    if b['js']:
        tabs.append(('JS', b['js']))
    def tab_btn(i, name):
        on = ' class="on"' if i == 0 else ''
        return f'<button data-tab="{name}"{on}>{name}</button>'
    tab_btns = ''.join(tab_btn(i, name) for i, (name, _) in enumerate(tabs))
    panes = ''.join(
        f'<div class="pane{" on" if i == 0 else ""}" data-pane="{name}"><pre>{esc(code)}</pre><div class="copyrow"><button class="copybtn">Copy</button></div></div>'
        for i, (name, code) in enumerate(tabs))
    by_slug = {x['slug']: x for x in comps}
    links = ', '.join(f'<a href="/components/{u}/">{esc(by_slug[u]["meta"]["title"])}</a>' for u in m.get('uses', []) if u in by_slug)
    deps_html = f'<p class="deps">Built from: {links} — include their CSS alongside this block.</p>' if links else ''
    prev_html = next_html = '<span style="flex:1"></span>'
    if idx > 0:
        pb = blocks[idx - 1]
        prev_html = f'<a href="/blocks/{pb["slug"]}/"><span class="dir">Previous</span><div class="nm">{esc(pb["meta"]["title"])}</div></a>'
    if idx < len(blocks) - 1:
        nb = blocks[idx + 1]
        next_html = f'<a class="next" href="/blocks/{nb["slug"]}/"><span class="dir">Next</span><div class="nm">{esc(nb["meta"]["title"])}</div></a>'
    js_tag = f'<script src="/blocks/{slug}/{slug}.js?v={_v(b["js"])}"></script>' if b['js'] else ''
    body = f"""
<div class="wrap">
  <main class="detail">
    <p class="crumb"><a href="/blocks/">Blocks</a> / {esc(m['title'])}</p>
    <h1>{esc(m['title'])} <span class="st st-{esc(m.get('status','beta'))}">{esc(m.get('status','beta'))}</span></h1>
    <p class="desc">{esc(m['description'])}</p>
    <div class="stagebar">
      <span class="lbl">Preview</span>
      <span class="seg" data-seg="width"><button data-v="desktop" class="on">Desktop</button><button data-v="mobile">Mobile</button></span>
      <span class="seg" data-seg="theme"><button data-v="light" class="on">Light</button><button data-v="dark">Dark</button></span>
    </div>
    <div class="stage col" id="stage">
{b['preview']}
    </div>
    {deps_html}
    <div class="codebox">
      <div class="codetabs">{tab_btns}</div>
      {panes}
    </div>
    <section class="doc"><h2>Usage</h2><p>{esc(m.get('usage',''))}</p></section>
    <div class="prevnext">{prev_html}{next_html}</div>
  </main>
</div>
{FOOTER}
{js_tag}
{DETAIL_JS}
</body>
</html>"""
    extra = f'<link rel="stylesheet" href="/blocks/{slug}/{slug}.css?v={_v(b["css"])}">'
    return head(f"{m['title']} — Blocks — KATA UI", m['description'], extra) + body

def main():
    comps = load_components()
    blocks = load_blocks()
    n_icons = len(list((ROOT / 'icons').glob('*.svg')))
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    shutil.copy(ROOT / 'tokens.css', DIST / 'tokens.css')
    shutil.copy(ROOT / 'logo' / 'favicon.svg', DIST / 'favicon.svg')
    shutil.copy(ROOT / 'logo' / 'logo.svg', DIST / 'logo.svg')
    shutil.copy(ROOT / 'site.css', DIST / 'site.css')
    (DIST / 'index.html').write_text(emit(landing(comps, blocks, n_icons), comps, None), encoding='utf-8')
    cdir = DIST / 'components'
    cdir.mkdir()
    (cdir / 'index.html').write_text(emit(components_index(comps), comps, None), encoding='utf-8')
    for i, c in enumerate(comps):
        src = ROOT / 'components' / c['slug']
        dst = cdir / c['slug']
        dst.mkdir()
        for f in src.iterdir():
            if f.is_file():
                shutil.copy(f, dst / f.name)
        (dst / 'index.html').write_text(emit(detail(comps, i), comps, comps[i]['slug']), encoding='utf-8')
    tokens = json.loads((ROOT / 'system' / 'tokens.json').read_text(encoding='utf-8'))
    dsdir = DIST / 'design-system'
    dsdir.mkdir()
    (dsdir / 'index.html').write_text(emit(design_system_page(tokens), comps, None), encoding='utf-8')
    shutil.copy(ROOT / 'system' / 'tokens.json', dsdir / 'tokens.json')
    idir = DIST / 'icons'
    idir.mkdir(exist_ok=True)
    (idir / 'index.html').write_text(emit(icons_page(), comps, None), encoding='utf-8')
    for f in (ROOT / 'icons').glob('*.svg'):
        shutil.copy(f, idir / f.name)
    bkdir = DIST / 'blocks'
    bkdir.mkdir(exist_ok=True)
    (bkdir / 'index.html').write_text(emit(blocks_index(blocks), comps, None), encoding='utf-8')
    for i, b in enumerate(blocks):
        src = ROOT / 'blocks' / b['slug']
        dst = bkdir / b['slug']
        dst.mkdir(exist_ok=True)
        for f in src.iterdir():
            if f.is_file():
                shutil.copy(f, dst / f.name)
        (dst / 'index.html').write_text(emit(block_detail(blocks, i, comps), comps, None), encoding='utf-8')
    (DIST / 'registry.json').write_text(registry_json(comps, blocks), encoding='utf-8')
    (DIST / 'llms.txt').write_text(llms_txt(comps, blocks, n_icons), encoding='utf-8')
    (DIST / 'llms-full.txt').write_text(llms_full(comps, blocks), encoding='utf-8')
    urls = ['/', '/components/', '/design-system/', '/icons/', '/blocks/'] + [f"/components/{c['slug']}/" for c in comps] + [f"/blocks/{b['slug']}/" for b in blocks]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
         '\n'.join(f'<url><loc>https://kata-ui.dev{u}</loc></url>' for u in urls) + '\n</urlset>\n'
    (DIST / 'sitemap.xml').write_text(sm, encoding='utf-8')
    print(f'built {len(comps)} components -> {DIST}')

if __name__ == '__main__':
    main()
