#!/usr/bin/env python3
"""KATA UI — static site generator. Registry (components/) is the source of truth."""
import hashlib, html, json, re, shutil
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / 'dist'
CATS = ['Form & Input', 'Layout & Navigation', 'Overlays & Dialogs', 'Feedback & Status', 'Display & Media', 'Motion', 'KATAYABURI', 'Japan']

STARTER_HTML = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>KATA Starter — your first page</title>\n<link rel="stylesheet" href="kata-ui.css">\n<style>\n  body{font-family:var(--k-font);background:var(--k-bg-soft);color:var(--k-ink);margin:0;padding:36px 18px}\n  main{max-width:520px;margin:0 auto;display:grid;gap:14px}\n  h1{font-size:21px;letter-spacing:-.02em}\n  p.lead{color:var(--k-ink-2);font-size:14px;line-height:1.75}\n</style>\n</head>\n<body>\n<main>\n  <h1>It works. This page is KATA parts, unmodified.</h1>\n  <p class="lead">Everything below comes from kata-ui.css and kata-ui.js in this folder. Copy a part from kata-ui.dev, paste it here, and it matches — same mold, same tokens.</p>\n  <div class="k-card">\n    <div class="k-card-h">Create your account</div>\n    <div class="k-card-b" style="display:grid;gap:12px">\n      <span class="field" style="display:grid;gap:6px"><label for="em">Email</label><input class="input" id="em" type="email" placeholder="you@company.com"></span>\n      <label class="switchrow" style="display:flex;align-items:center;gap:10px;font-size:13.5px"><span class="switch"><input type="checkbox" checked><span class="tr"></span></span>Email me product updates</label>\n      <div style="display:flex;gap:9px;align-items:center">\n        <button class="btn btn-pri btn-md">Create account</button>\n        <span class="badge teal"><i></i>Free for 30 days</span>\n      </div>\n    </div>\n  </div>\n  <p class="lead">Next: browse the catalog at kata-ui.dev/components — each part carries its own CSS tab, so you can drop the bundle and keep only what you use.</p>\n</main>\n<script src="kata-ui.js"></script>\n</body>\n</html>\n'
STARTER_README = "# KATA Starter\n\nA working first page built only from KATA UI parts.\n\n## Use it\n\n1. Unzip. Open `index.html` in a browser — no server, no build step.\n2. Edit the HTML. Every class on the page comes from `kata-ui.css`.\n3. When you settle, slim down: each part at kata-ui.dev carries just its own\n   CSS/JS, so production pages can load only what they use.\n\n## Files\n\n- `index.html` — the demo page (Card, Input, Switch, Button, Badge)\n- `kata-ui.css` — design tokens + every component and block style\n- `kata-ui.js` — every part's behavior, each in its own scope\n\nMIT licensed. KATA UI — parts, cast from a single mold.\n"


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
        ex_file = d / 'examples.html'
        examples = []
        if ex_file.exists():
            parts = re.split(r'<!--\s*example:\s*(.+?)\s*-->', ex_file.read_text(encoding='utf-8'))
            for i in range(1, len(parts) - 1, 2):
                examples.append((parts[i], parts[i + 1].strip()))
        comps.append(dict(slug=slug, meta=meta, preview=preview, css=css, js=js, deps=deps, examples=examples))
    order = {c: i for i, c in enumerate(CATS)}
    comps.sort(key=lambda c: (order.get(c['meta']['category'], 99), c['meta']['title']))
    return comps

def esc(s):
    return html.escape(s)

HEADER = """<header class="top"><div class="wrap top-in">
  <a class="logo" href="/"><svg width="27" height="27" viewBox="0 0 48 48" aria-hidden="true"><rect x="7" y="7" width="16.6" height="16.6" fill="#18181b"/><rect x="32.95" y="7" width="8.05" height="8.05" fill="#18181b"/><rect x="24.4" y="15.55" width="8.05" height="8.05" fill="#18181b"/><rect x="7" y="24.4" width="16.6" height="16.6" fill="#d4d4d8"/><rect x="24.4" y="24.4" width="16.6" height="16.6" fill="#eb471f"/></svg>KATA UI<small>preview</small></a>
  <button class="menubtn" id="menubtn" type="button" aria-label="Open menu">☰<span>Menu</span></button>
  <nav><a href="/docs/">Docs</a><a href="/components/">Components</a><a href="/blocks/">Blocks</a><a href="/templates/">Templates</a><a href="/icons/">Icons</a><a href="/themes/">Themes</a><a href="/design-system/">Design System</a><a href="/pricing/">Pricing</a></nav>
  <button class="hsearch" type="button" data-site-search aria-label="Search the catalog"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.5-4.5"/></svg><span class="hst">Search</span><span class="k-kbd">\u2318K</span></button>
  <a class="gh" href="https://github.com/kajisho5/KATA-UI" rel="noopener" aria-label="KATA UI on GitHub"><svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.8a9.2 9.2 0 0 0-9.2 9.2c0 4.1 2.7 7.6 6.4 9 .5.1.6-.2.6-.4v-1.4c-2.6.6-3.1-1.2-3.1-1.2-.4-1.1-1-1.3-1-1.3-.9-.6.1-.6.1-.6.9.1 1.4.9 1.4.9.9 1.4 2.2 1 2.7.8.1-.6.3-1.1.6-1.3-2.1-.2-4.2-1-4.2-4.6 0-1 .4-1.8.9-2.5-.1-.2-.4-1.1.1-2.3 0 0 .8-.2 2.5.9a8.6 8.6 0 0 1 4.5 0c1.7-1.1 2.5-.9 2.5-.9.5 1.2.2 2.1.1 2.3.5.7.9 1.5.9 2.5 0 3.6-2.2 4.4-4.2 4.6.3.3.6.9.6 1.8v2.6c0 .2.2.5.6.4a9.2 9.2 0 0 0 6.4-9A9.2 9.2 0 0 0 12 2.8z"/></svg></a>
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
<nav class="drawer" id="drawer" aria-label="Site menu">
  <div class="dhead"><span>Menu</span><button class="dclose" id="dclose" type="button" aria-label="Close menu">✕</button></div>
  <div class="dlinks"><a href="/components/">Components</a><a href="/blocks/">Blocks</a><a href="/templates/">Templates</a><a href="/icons/">Icons</a><a href="/themes/">Themes</a><a href="/docs/">Docs</a><a href="/design-system/">Design System</a></div>
  <input class="dfilter" id="dfilter" type="search" placeholder="Filter parts, blocks, pages…" aria-label="Filter the menu">
  {''.join(tree_sections(comps, active, None))}
  <p class="dnone" id="dnone" hidden>No matches.</p>
  <div class="dlinks dgh-row"><a href="https://github.com/kajisho5/KATA-UI" rel="noopener"><svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.8a9.2 9.2 0 0 0-9.2 9.2c0 4.1 2.7 7.6 6.4 9 .5.1.6-.2.6-.4v-1.4c-2.6.6-3.1-1.2-3.1-1.2-.4-1.1-1-1.3-1-1.3-.9-.6.1-.6.1-.6.9.1 1.4.9 1.4.9.9 1.4 2.2 1 2.7.8.1-.6.3-1.1.6-1.3-2.1-.2-4.2-1-4.2-4.6 0-1 .4-1.8.9-2.5-.1-.2-.4-1.1.1-2.3 0 0 .8-.2 2.5.9a8.6 8.6 0 0 1 4.5 0c1.7-1.1 2.5-.9 2.5-.9.5 1.2.2 2.1.1 2.3.5.7.9 1.5.9 2.5 0 3.6-2.2 4.4-4.2 4.6.3.3.6.9.6 1.8v2.6c0 .2.2.5.6.4a9.2 9.2 0 0 0 6.4-9A9.2 9.2 0 0 0 12 2.8z"/></svg>GitHub</a></div>
</nav>"""


def drawer_extra():
    bl = _all_blocks()
    blinks = ''.join('<a href="/blocks/' + b['slug'] + '/">' + esc(b['meta']['title']) + '</a>' for b in bl)
    tlinks = ''
    try:
        tpls = load_templates()
        tlinks = ''.join('<a href="/templates/' + t['slug'] + '/">' + esc(t['meta']['title']) + '</a>' for t in tpls)
    except Exception:
        tlinks = ''
    elinks = ''.join('<a href="' + u + '">' + n + '</a>' for u, n in [
        ('/icons/', 'Icons'), ('/themes/', 'Themes'), ('/design-system/', 'Design System'),
        ('/docs/', 'Docs — all guides'), ('/docs/installation/', 'Installation'),
        ('/docs/changelog/', 'Changelog'), ('/skill/SKILL.md', 'AI Skill (SKILL.md)')])
    return ('<nav class="side dextra"><h4>Blocks</h4>' + blinks
            + '<h4>Templates</h4>' + tlinks
            + '<h4>Explore</h4>' + elinks + '</nav>')

DRAWER_JS = """<script>
(function(){var mb=document.getElementById('menubtn');if(!mb)return;
function setD(o){document.body.classList.toggle('dopen',o);}
mb.addEventListener('click',function(){setD(true);});
var dc=document.getElementById('dclose');if(dc)dc.addEventListener('click',function(){setD(false);});
var sc=document.getElementById('scrim');if(sc)sc.addEventListener('click',function(){setD(false);});
document.addEventListener('keydown',function(e){if(e.key==='Escape')setD(false);});
var df=document.getElementById('dfilter');
if(df){df.addEventListener('input',function(){
  var q=df.value.trim().toLowerCase();var total=0;
  df.closest('.drawer').querySelectorAll('.side').forEach(function(side){
  var kids=Array.prototype.slice.call(side.children);var curH=null;var curVis=false;
  function flush(){if(curH)curH.style.display=curVis?'':'none';}
  kids.forEach(function(el){
    if(el.tagName==='H4'){flush();curH=el;curVis=false;}
    else if(el.tagName==='A'){var hit=!q||el.textContent.toLowerCase().indexOf(q)>-1;el.style.display=hit?'':'none';if(hit){curVis=true;total++;}}
  });flush();
  });
  var dn=document.getElementById('dnone');if(dn)dn.hidden=total>0;
});}
document.querySelectorAll('.side a.on').forEach(function(a){var c=a.closest('.drawer')||a.parentElement;if(c){try{c.scrollTop=Math.max(0,a.offsetTop-80);}catch(e){}}});
})();
</script>"""

_BLOCKS_FULL = None

def _all_blocks():
    global _BLOCKS_FULL
    if _BLOCKS_FULL is None:
        _BLOCKS_FULL = load_blocks()
    return _BLOCKS_FULL

_BLOCK_CACHE = None

def _block_search_items():
    global _BLOCK_CACHE
    if _BLOCK_CACHE is None:
        _BLOCK_CACHE = [{'t': b['meta']['title'], 'u': '/blocks/' + b['slug'] + '/', 'k': 'Block'} for b in load_blocks()] + [{'t': t['meta']['title'], 'u': '/templates/' + t['slug'] + '/', 'k': 'Template'} for t in load_templates()]
    return _BLOCK_CACHE

SEARCH_TMPL = """<dialog class="kcmd" data-site-dialog aria-label="Search KATA UI">
  <div class="kcmd-input-row">
    <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.5-4.5"/></svg>
    <input class="kcmd-input" data-site-input type="text" placeholder="Search components, blocks, docs\u2026" aria-label="Search KATA UI">
  </div>
  <ul class="kcmd-list" data-site-list></ul>
  <div class="kcmd-empty" data-site-empty style="display:none">No results.</div>
</dialog>
<script>
const KIDX = __KATA_INDEX__;
const sDlg = document.querySelector('[data-site-dialog]');
const sIn = sDlg.querySelector('[data-site-input]');
const sList = sDlg.querySelector('[data-site-list]');
const sEmpty = sDlg.querySelector('[data-site-empty]');
let sAct = 0, sShown = [];
function sRender(q) {
  const query = (q || '').trim().toLowerCase();
  sShown = KIDX.filter(it => !query || it.t.toLowerCase().includes(query) || it.k.toLowerCase().includes(query)).slice(0, 14);
  sAct = 0;
  sList.innerHTML = sShown.map((it, i) => '<li><button type="button" class="kcmd-item' + (i === sAct ? ' active' : '') + '" data-su="' + it.u + '"><span>' + it.t + '</span><span class="kcmd-hint">' + it.k + '</span></button></li>').join('');
  sEmpty.style.display = sShown.length ? 'none' : '';
  sList.querySelectorAll('[data-su]').forEach(b => b.addEventListener('click', () => { location.href = b.dataset.su; }));
}
function sOpen() { if (!sDlg.open) { sIn.value = ''; sRender(''); sDlg.showModal(); sIn.focus(); } }
function sMove(d) { if (!sShown.length) return; sAct = (sAct + d + sShown.length) % sShown.length; sList.querySelectorAll('.kcmd-item').forEach((el, i) => el.classList.toggle('active', i === sAct)); }
document.querySelectorAll('[data-site-search]').forEach(b => b.addEventListener('click', sOpen));
document.addEventListener('keydown', e => { if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); sOpen(); } });
sIn.addEventListener('input', () => sRender(sIn.value));
sIn.addEventListener('keydown', e => {
  if (e.key === 'ArrowDown') { e.preventDefault(); sMove(1); }
  if (e.key === 'ArrowUp') { e.preventDefault(); sMove(-1); }
  if (e.key === 'Enter' && sShown[sAct]) { location.href = sShown[sAct].u; }
});
sDlg.addEventListener('click', e => { if (e.target === sDlg) sDlg.close(); });
</script>"""

def search_html(comps):
    import json as _json
    items = [{'t': c['meta']['title'], 'u': '/components/' + c['slug'] + '/', 'k': 'Component'} for c in comps]
    items += _block_search_items()
    items += [{'t': d[1], 'u': '/docs/' + d[0] + '/', 'k': 'Docs'} for d in DOCS]
    items += [{'t': t, 'u': u, 'k': 'Page'} for t, u in [('Components', '/components/'), ('Blocks', '/blocks/'), ('Templates', '/templates/'), ('Icons', '/icons/'), ('Themes', '/themes/'), ('Design System', '/design-system/'), ('Docs', '/docs/'), ('Pricing', '/pricing/'), ('Showcase', '/showcase/')]]
    return SEARCH_TMPL.replace('__KATA_INDEX__', _json.dumps(items, ensure_ascii=False))

def emit(page, comps, active, current=None, tree=False):
    if tree:
        import re as _re
        page = _re.sub(r'<div class="(wrap|wrap dc|wrap ds|wrap bk|wrap tk)">',
                       lambda m: m.group(0) + '<div class="layout">' + nav_tree(comps, active, current) + '<div class="lmain">',
                       page, count=1)
        page = page.replace('<div class="wrap"><footer class="site">', '</div></div><div class="wrap"><footer class="site">', 1)
    return page.replace('</body>', drawer_html(comps, active) + DRAWER_JS + search_html(comps) + '</body>', 1)

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
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/manifest.webmanifest">
<meta name="theme-color" media="(prefers-color-scheme: light)" content="#ffffff">
<meta name="theme-color" media="(prefers-color-scheme: dark)" content="#18181b">
<link rel="stylesheet" href="/tokens.css?v={_v((ROOT / 'tokens.css').read_text(encoding='utf-8'))}">
<link rel="stylesheet" href="/site.css?v={_v((ROOT / 'site.css').read_text(encoding='utf-8'))}">
<link rel="stylesheet" href="/components/command/command.css?v={_v((ROOT / 'components/command/command.css').read_text(encoding='utf-8'))}">
<link rel="stylesheet" href="/components/kbd/kbd.css?v={_v((ROOT / 'components/kbd/kbd.css').read_text(encoding='utf-8'))}">
{extra}
</head>
<body>
{HEADER}
"""

def card(c):
    m = c['meta']
    tags = ''.join(f'<span class="tag">{esc(t)}</span>' for t in m.get('tags', []))
    q = esc((m['title'] + ' ' + c['slug'] + ' ' + ' '.join(m.get('tags', [])) + ' ' + m['category']).lower())
    return f"""<a class="card" data-q="{q}" href="/components/{c['slug']}/">
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
.lpsec .sub{margin-top:7px;color:var(--ink2);font-size:14px;line-height:1.8;max-width:62ch;letter-spacing:.012em}
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
.showband{margin-top:64px;background:#101013;border-radius:18px;padding:30px 26px}
.showband h2{font-size:22px;font-weight:600;letter-spacing:-.02em;color:#f4f4f5}
.showband .sub{margin-top:7px;color:#a1a1aa;font-size:14px;line-height:1.8;max-width:62ch;letter-spacing:.012em}
.showgrid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:20px}
@media (max-width:720px){.showgrid{grid-template-columns:1fr}}
.showtile{border:1px solid #26262b;border-radius:14px;padding:16px;background:#17171a;overflow:hidden}
.showtile.wide{grid-column:1/-1}
.showtile .cap{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;font-family:var(--mono);font-size:11px;letter-spacing:.07em;color:#a1a1aa}
.showtile .cap a{color:#f4f4f5;text-decoration:none;letter-spacing:0;font-size:12px}
.hero2{position:relative;border-radius:22px;overflow:hidden;background:#0b0b0f;border:1px solid #26262b;margin-top:24px;padding:58px 26px 30px;text-align:center}
.hero2 .eyebrow{display:inline-flex;align-items:center;gap:8px}
.hero2 .stats div{display:flex;flex-direction:column;align-items:center;gap:1px}
.hero2::before{content:"";position:absolute;inset:0;background:radial-gradient(620px 300px at 50% -60px,rgba(255,255,255,.07),transparent 65%)}
.hero2 .hwag{position:absolute;inset:0;width:100%;height:100%;-webkit-mask-image:linear-gradient(180deg,#000 25%,transparent 88%);mask-image:linear-gradient(180deg,#000 25%,transparent 88%)}
.hero2 .hkanji{position:absolute;right:-38px;top:50%;transform:translateY(-54%);font-family:"Hiragino Mincho ProN","Hiragino Mincho Pro","Yu Mincho",YuMincho,"Noto Serif JP",serif;font-size:400px;line-height:1;color:rgba(244,244,245,.05);pointer-events:none;user-select:none}
@media (max-width:720px){.hero2 .hkanji{font-size:250px;right:-24px}}
.hero2 .eyebrow i{background:var(--k-core)}
.hero2-in{position:relative}
.hero2 h1{font-size:45px;line-height:1.12;color:#f4f4f5;letter-spacing:-.025em;font-weight:650}
.hero2 h1 .dim{color:#d4d4d8}
.hero2-in>p{max-width:62ch;margin:17px auto 0;font-size:15px;line-height:1.85;color:#a1a1aa}
.hero2 .eyebrow{border-color:#3f3f46;color:#d4d4d8;background:rgba(255,255,255,.05)}
.hero2 .eyebrow{white-space:nowrap}
.hero2-in p{color:#d4d4d8}
@media (max-width:560px){.hero2 .eyebrow{font-size:11px;padding:5px 10px}.hero2 .stats{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}.hero2 .stats b{font-size:19px}.hero2 .stats span{font-size:10.5px}}
.hero2 .stats{border-color:#26262b;display:flex;gap:15px 38px;flex-wrap:wrap;justify-content:center;margin-top:34px;padding-top:22px;border-top:1px solid #26262b}
.hero2 .stats b{color:#f4f4f5}
.hero2 .stats span{color:#a1a1aa}
.hero2 .browser{box-shadow:0 34px 90px -24px rgba(0,0,0,.65);margin-top:40px;text-align:left;position:relative;z-index:1}
.hero2 .framecap{color:#a1a1aa;position:relative;z-index:1}
.hero2 .framecap a{color:#e4e4e7}
@media (max-width:720px){.hero2{padding:42px 16px 22px}.hero2 h1{font-size:31px}}
.collage-sec{margin-top:64px}
.collage-sec h2{font-size:22px;font-weight:600;letter-spacing:-.02em}
.collage-sec .sub{margin-top:7px;color:var(--ink2);font-size:14px;line-height:1.8;max-width:62ch;letter-spacing:.012em}
.collage{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:18px}
.collage-cell{border:1px solid var(--hair);border-radius:14px;padding:18px;background:#fff;overflow:hidden;min-width:0}
.collage-cell.wide{grid-column:1/-1}
.collage-cell .cap{display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;font-family:var(--mono);font-size:10.5px;letter-spacing:.08em;color:var(--ink3)}
.collage-cell .cap a{color:var(--acc);text-decoration:none;font-family:inherit}
.collage-cell div.k-dt{overflow-x:auto;max-width:none!important}
.collage-cell table.k-dt-t{min-width:500px}
@media (max-width:720px){.collage{grid-template-columns:1fr}}
.cmptable{width:100%;min-width:600px;border-collapse:collapse;margin-top:18px;font-size:13.5px;background:#fff;border:1px solid var(--hair);border-radius:12px;overflow:hidden}
.cmptable th,.cmptable td{padding:11px 14px;border-bottom:1px solid var(--hair);text-align:left;vertical-align:top}
.cmptable thead th{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink3);background:var(--soft);font-weight:600}
.cmptable tbody th{font-weight:550;color:var(--ink2);white-space:nowrap}
.cmptable td{color:var(--ink2)}
.cmptable td.me{color:var(--ink);font-weight:550}
.cmptable tr:last-child td,.cmptable tr:last-child th{border-bottom:none}
.cmpnote{margin-top:9px;font-size:12px;color:var(--ink3)}
@media (max-width:720px){.cmptable{font-size:12px}.cmptable th,.cmptable td{padding:9px 9px}}
.compat{margin-top:20px;border:1px solid var(--hair);border-radius:12px;background:var(--soft);padding:18px;font-size:13.5px;line-height:1.9;color:var(--ink2)}
.compat b{color:var(--ink);font-weight:600}
.compat a{color:var(--ink);font-weight:550}
@media (max-width:720px){.lp .hero h1{font-size:33px}.browser .shell-side{display:none}}
</style>"""

def landing(comps, blocks, n_icons, templates=None):
    n = len(comps)
    nb = len(blocks)
    nt = len(templates or [])
    shell = next((b for b in blocks if b['slug'] == 'app-shell'), None)
    shell_html = shell['preview'] if shell else ''
    pv = {c['slug']: c for c in comps}
    def tile(slug, label, wide=False):
        c = pv.get(slug)
        if not c:
            return ''
        return ('<div class="showtile' + (' wide' if wide else '') + '"><div class="cap"><span>' + label.upper() + '</span><a href="/components/' + slug + '/">Open part</a></div>' + c['preview'] + '</div>')
    show_scripts = ''.join(f'<script src="/components/{sl}/{sl}.js?v={_v(pv[sl]["js"])}"></script>' for sl in ('counter', 'spotlight', 'text-reveal', 'follow-frame', 'reorder') if pv.get(sl) and pv[sl]['js'])
    faq_b = next((b for b in blocks if b['slug'] == 'faq'), None)
    principles = ('<section class="lpsec"><h2>Three rules, cast into every part</h2><div class="steps">'
      '<div class="step"><span class="no">RULE 1</span><h3>One mold</h3><p>Every part is checked by a program before it ships — tokens only, classes covered, icons on the grid. Two parts built months apart look built on the same day. <a href="/docs/the-mold/" style="color:var(--acc)">How the mold works</a></p></div>'
      '<div class="step"><span class="no">RULE 2</span><h3>Yours, not rented</h3><p>Copied code has no roadmap and no breaking changes. Nobody can sunset it, reprice it, or deprecate it under you. <a href="/docs/why-vanilla/" style="color:var(--acc)">Why vanilla</a></p></div>'
      '<div class="step"><span class="no">RULE 3</span><h3>Native first</h3><p>Where the platform has the element — dialog, details, real inputs — the part is the element. Scripts layer behavior on markup; they never generate it.</p></div>'
      '</div></section>')
    compare = ('<section class="lpsec"><h2>How KATA compares</h2>'
      '<div style="overflow-x:auto"><table class="cmptable"><thead><tr><th></th><th>KATA UI</th><th>shadcn/ui</th><th>MUI</th><th>Flux UI</th></tr></thead><tbody>'
      '<tr><th>Framework</th><td class="me">None — plain HTML</td><td>React</td><td>React</td><td>Laravel + Livewire</td></tr>'
      '<tr><th>Distribution</th><td class="me">Copy-paste, CLI & registry</td><td>Copy-paste + CLI</td><td>npm package</td><td>Composer package</td></tr>'
      '<tr><th>Runtime required</th><td class="me">None</td><td>React</td><td>React</td><td>Livewire + Alpine</td></tr>'
      '<tr><th>Theming</th><td class="me">CSS tokens</td><td>Tailwind + variables</td><td>Theme object</td><td>Tailwind</td></tr>'
      '<tr><th>Price</th><td class="me">Parts free (MIT) · Blocks + Templates lifetime</td><td>Free</td><td>Free + paid extras</td><td>One-time, per project tier</td></tr>'
      '</tbody></table></div>'
      '<p class="cmpnote">From each project’s public pages, November 2026. The honest summary: the others are excellent inside their framework. KATA is for everywhere else.</p></section>')
    wlband = ('<section class="lpsec"><div class="wl-band"><h2>Pro opens soon</h2>'
      '<p>The blocks and templates — 21 sections and 7 whole pages — go on sale at $129, once, lifetime. The parts stay free either way. Leave an email and the launch is the only message you will ever get.</p>'
      + waitlist_form(dark=True) + '</div></section>')
    lp_faq = ('<section class="k-faqb" style="max-width:640px"><div class="acc">' + '<details class="k-acc" open><summary>Is it really free?<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="square" stroke-linejoin="bevel" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg></summary><div class="k-acc-body">Yes. Every component — all 136, with the code on its page — is MIT-licensed, free for personal and commercial work. Pro adds the assembled blocks and templates; the parts themselves are never paywalled.</div></details><details class="k-acc"><summary>Which frameworks does it work with?<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="square" stroke-linejoin="bevel" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg></summary><div class="k-acc-body">All of them, and none. Parts are plain HTML, CSS and JS, so they paste into Astro, Laravel, Rails, WordPress, a static page, or the corner of a legacy app. There is no runtime and no build step unless you bring your own.</div></details><details class="k-acc"><summary>How do I install a part?<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="square" stroke-linejoin="bevel" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg></summary><div class="k-acc-body">Open its page and copy the three files — or take the starter kit and pull parts with the CLI. The registry is machine-readable JSON, so your AI tools can fetch parts for you, too.</div></details><details class="k-acc"><summary>What does Pro add?<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="square" stroke-linejoin="bevel" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg></summary><div class="k-acc-body">21 blocks and 7 page templates — whole sections, already assembled — plus every future block. One payment of $129, lifetime. Sales open soon; the waitlist on the pricing page gets exactly one email when they do.</div></details><details class="k-acc"><summary>Can I use it in client work?<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="square" stroke-linejoin="bevel" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg></summary><div class="k-acc-body">Yes — the MIT license covers components in client projects, and the Pro license covers blocks and templates the same way. Ship it, invoice it, keep the code.</div></details>' + '</div>'
              '<p class="more">Still stuck? <a href="/docs/">Read the docs</a> — or check the <a href="/docs/faq/">full FAQ</a>.</p></section>'
              '<link rel="stylesheet" href="/components/accordion/accordion.css">')
    faqsec = ('<section class="lpsec"><h2>Questions</h2><div style="margin-top:16px">' + lp_faq + '</div></section>')
    sc_block = next((b for b in blocks if b['slug'] == 'stat-cards'), None)
    def ccell(href, label, html, wide=False):
        return ('<div class="collage-cell' + (' wide' if wide else '') + '"><div class="cap"><span>' + label.upper() + '</span><a href="' + href + '">Open part</a></div>' + html + '</div>')
    collage = ('<section class="collage-sec"><h2>Assembled, not illustrated.</h2>'
               '<p class="sub">This dashboard is not a screenshot. Every panel here is a live part from the catalog — the same code the copy button hands you, running on this page.</p>'
               '<div class="collage">'
               + (ccell('/blocks/stat-cards/', 'Stat Cards — Block', sc_block['preview'], True) if sc_block else '')
               + ccell('/components/data-table/', 'Data Table', pv['data-table']['preview'], True)
               + ccell('/components/line-chart/', 'Line Chart', pv['line-chart']['preview'])
               + ccell('/components/donut-chart/', 'Donut Chart', pv['donut-chart']['preview'])
               + '</div></section>')
    showcase = ('<section class="showband"><h2>The showy shelf</h2><p class="sub">The Motion line and the ambient pieces — live on this page, in the dark they were designed for. Built to be stared at a little.</p>'
                '<div data-theme="dark"><div class="showgrid">'
                + tile('aurora', 'Aurora') + tile('converge', 'Converge') + tile('spotlight', 'Spotlight') + tile('beam-border', 'Beam Border') + tile('glass-panel', 'Glass Panel') + tile('follow-frame', 'Follow Frame')
                + tile('text-reveal', 'Text Reveal', True) + tile('reorder', 'Reorder', True) + tile('counter', 'Counter') + tile('marquee', 'Marquee')
                + '</div></div>' + show_scripts + '</section>')
    body = f"""
<div class="wrap lp">
  <div class="hero2">
    <svg class="hwag" aria-hidden="true" preserveAspectRatio="none"><defs><pattern id="hw" width="56" height="28" patternUnits="userSpaceOnUse"><g fill="none" stroke="rgba(244,244,245,.06)" stroke-width="1"><path d="M-28 28A28 28 0 0 1 28 28"/><path d="M-18.7 28A18.7 18.7 0 0 1 18.7 28"/><path d="M-9.3 28A9.3 9.3 0 0 1 9.3 28"/><path d="M28 28A28 28 0 0 1 84 28"/><path d="M37.3 28A18.7 18.7 0 0 1 74.7 28"/><path d="M46.7 28A9.3 9.3 0 0 1 65.3 28"/><path d="M0 14A28 28 0 0 1 56 14"/><path d="M9.3 14A18.7 18.7 0 0 1 46.7 14"/><path d="M18.7 14A9.3 9.3 0 0 1 37.3 14"/><path d="M-56 14A28 28 0 0 1 0 14"/><path d="M56 14A28 28 0 0 1 112 14"/></g></pattern></defs><rect width="100%" height="100%" fill="url(#hw)"/></svg>
    <span class="hkanji" aria-hidden="true">型</span>
    <div class="hero2-in">
    <span class="eyebrow"><i></i>Vanilla components — no framework, no build step</span>
    <h1>Parts, cast from a single mold.<br><span class="dim">Copy the code. Own the design.</span></h1>
    <p>From buttons to app shells — practical components in plain HTML, CSS and JS, each with a live preview and copy-ready code. Every part is cast from a single mold — kata, the Japanese discipline of the form.</p>
    <div class="cta">
      <a class="kbtn-primary" href="/components/" style="display:inline-flex;align-items:center;height:42px;padding:0 20px;border-radius:9px;background:#f4f4f5;color:#18181b;font-weight:550;font-size:14px;text-decoration:none">Browse components</a>
      <a href="/blocks/" style="display:inline-flex;align-items:center;height:42px;padding:0 20px;border-radius:9px;border:1px solid #71717a;font-weight:500;font-size:14px;text-decoration:none;background:rgba(255,255,255,.08);color:#f4f4f5">See blocks</a>
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
  </div>
  <section class="lpsec">
    <h2>How it works</h2>
    <div class="steps">
      <div class="step"><span class="no">STEP 1</span><h3>Take the tokens</h3><p>Load <code>tokens.css</code> once. Every part reads its color, spacing, radius and motion from it — that file is the mold.</p></div>
      <div class="step"><span class="no">STEP 2</span><h3>Paste the part</h3><p>Copy the HTML, the CSS and the JS from the part's page. No install, no package, nothing phoning home.</p></div>
      <div class="step"><span class="no">STEP 3</span><h3>Make it yours</h3><p>Adjust the tokens, not the parts. One change in the mold re-casts everything on the page.</p></div>
    </div>
  </section>
  <section class="lpsec">
    <h2>Five genres, one mold</h2>
    <div class="genres">
      <a class="genre" href="/components/"><span class="gn">{n} PARTS</span><h3>Components</h3><p>The single parts: forms, overlays, feedback, display — and a Motion line other libraries do not carry.</p></a>
      <a class="genre" href="/blocks/"><span class="gn">{nb} SECTIONS</span><h3>Blocks</h3><p>Whole sections composed from the parts — sign-in, pricing, settings, an app shell. Start here, take apart later.</p></a>
      <a class="genre" href="/templates/"><span class="gn">{nt} PAGES</span><h3>Templates</h3><p>Whole pages, already assembled — a dashboard, an inbox, a landing. The parts and blocks in their places, ready to take apart.</p></a>
      <a class="genre" href="/icons/"><span class="gn">{n_icons} GLYPHS</span><h3>Icons</h3><p>One mold: a 24 grid, a 1.7 stroke cut square, three shapes only. Click to copy the SVG.</p></a>
      <a class="genre" href="/design-system/"><span class="gn">TOKENS.JSON</span><h3>Design System</h3><p>The foundation every part is cast from — color, type, spacing, radius, motion. Download it, diff it, fork it.</p></a>
    </div>
    <div class="compat">
      <b>Drops into</b> plain HTML, Astro, Laravel, Django, Rails and WordPress themes — anywhere that renders HTML, with no React island required.<br>
      <b>For AI tools</b>, KATA speaks their formats: <a href="/registry.json">registry.json</a> for installers and agents, <a href="/llms.txt">llms.txt</a> for models that read the web.
    </div>
  </section>
  {principles}
  {compare}
  {faqsec}
  {wlband}
  {showcase}
  {collage}
  <div id="catalog">
{catalog_sections(comps)}
  </div>
</div>
{FOOTER}
</body>
</html>"""
    extra = ('<link rel="stylesheet" href="/blocks/app-shell/app-shell.css">'
             + ''.join(f'<link rel="stylesheet" href="/components/{sl}/{sl}.css?v={_v(pv[sl]["css"])}">' for sl in ('aurora', 'follow-frame', 'spotlight', 'beam-border', 'marquee', 'text-reveal', 'counter', 'glass-panel', 'converge', 'reorder', 'line-chart', 'donut-chart', 'data-table') if pv.get(sl)) + (f'<link rel="stylesheet" href="/blocks/stat-cards/stat-cards.css?v={_v(sc_block["css"])}">' if sc_block else '') + (f'<link rel="stylesheet" href="/blocks/faq/faq.css?v={_v(faq_b["css"])}">' if faq_b else ''))
    return head('KATA UI — UI Components & Code', 'Vanilla UI components with live previews and copy-ready code. No framework, no build step.', LP_STYLE + extra) + body

def registry_json(comps, blocks, templates=None):
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
    for t in (templates or []):
        m = t['meta']
        files = [{'path': f"templates/{t['slug']}/{t['slug']}.css", 'type': 'registry:page', 'content': t['css']}]
        if t['js']:
            files.append({'path': f"templates/{t['slug']}/{t['slug']}.js", 'type': 'registry:page', 'content': t['js']})
        example = re.sub(r'\s*<link rel="stylesheet"[^>]*>', '', t['preview']).strip()
        files.append({'path': f"templates/{t['slug']}/example.html", 'type': 'registry:page', 'content': example})
        items.append({'name': t['slug'], 'type': 'registry:page', 'title': m['title'],
                      'description': m['description'], 'categories': ['Templates'],
                      'dependencies': m.get('blocks', []) + m.get('uses', []), 'files': files})
    for t in load_themes():
        items.append({'name': 'theme-' + t['name'], 'type': 'registry:theme', 'title': 'Theme: ' + t['label'],
                      'description': t['note'], 'categories': ['Themes'],
                      'files': [{'path': 'themes/' + t['name'] + '.css', 'type': 'registry:theme', 'content': theme_css(t)}]})
    return json.dumps({'$schema': 'https://ui.shadcn.com/schema/registry.json', 'name': 'kata-ui', 'version': '1.0.0',
                       'homepage': 'https://kata-ui.dev', 'items': items}, ensure_ascii=False, indent=1)

def llms_txt(comps, blocks, n_icons, templates=None):
    lines = ['# KATA UI', '',
             '> Practical UI components in plain HTML, CSS and JavaScript. No framework, no build step. Every part is cast from a single design-token mold; copy the code and own it.', '',
             'KATA is framework-free: parts drop into plain HTML, Astro, Laravel, Django, Rails and templates unchanged. Components depend on tokens.css (design tokens) being loaded once.', '',
             '## Docs', '',
             '- [Design System](https://kata-ui.dev/design-system/): the tokens every part is cast from (tokens.json is downloadable there)',
             f'- [Icons](https://kata-ui.dev/icons/): {n_icons} icons on one mold (24 grid, 1.7 stroke, square caps); click to copy the SVG',
             '- [Registry](https://kata-ui.dev/registry.json): every component and block with its full CSS/JS/HTML, in the shadcn registry format',
             '- [Themes](https://kata-ui.dev/themes/): accent presets as small CSS files; a theme redefines the five accent tokens only. The page also offers 50 traditional Japanese colors (dentou) as click-to-cast accent sources',
             '- [Getting Started](https://kata-ui.dev/docs/getting-started/): load tokens.css once, then copy parts',
             '- [Skill for AI assistants](https://kata-ui.dev/skill/SKILL.md): a packaged SKILL.md that teaches an assistant to build with KATA correctly',
             '- [CLI](https://kata-ui.dev/docs/cli/): a zero-dependency Node script that installs parts from the registry — node kata-ui.mjs add button',
             '- [Installation](https://kata-ui.dev/docs/installation/): four ways in, plus per-stack guides for Plain HTML (https://kata-ui.dev/docs/install-html/), Astro (https://kata-ui.dev/docs/install-astro/) and Laravel (https://kata-ui.dev/docs/install-laravel/)',
             '- [Theming](https://kata-ui.dev/docs/theming/) / [Dark Mode](https://kata-ui.dev/docs/dark-mode/): dark mode is data-theme="dark" on any container', '',
             '## Components', '']
    for c in comps:
        lines.append(f"- [{c['meta']['title']}](https://kata-ui.dev/components/{c['slug']}/): {c['meta']['description']}")
    lines += ['', '## Blocks', '']
    for b in blocks:
        lines.append(f"- [{b['meta']['title']}](https://kata-ui.dev/blocks/{b['slug']}/): {b['meta']['description']}")
    lines += ['', '## Templates', '']
    for t in (templates or []):
        lines.append(f"- [{t['meta']['title']}](https://kata-ui.dev/templates/{t['slug']}/): {t['meta']['description']}")
    lines.append('')
    return '\n'.join(lines)

def llms_full(comps, blocks, templates=None):
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
    for t in (templates or []):
        m = t['meta']
        example = re.sub(r'\s*<link rel="stylesheet"[^>]*>', '', t['preview']).strip()
        out += [f"## Template: {m['title']} ({t['slug']})", '', m['description'], '',
                'Built from: ' + ', '.join(m.get('blocks', []) + m.get('uses', [])), '', '### HTML', '', '```html', example, '```', '',
                '### CSS (glue)', '', '```css', t['css'].strip(), '```', '']
        if t['js']:
            out += ['### JS', '', '```js', t['js'].strip(), '```', '']
    return '\n'.join(out)


CATALOG_SCRIPT = "<script>\nconst catq = document.getElementById('catq');\ncatq.addEventListener('input', () => {\n  const q = catq.value.trim().toLowerCase();\n  let any = false;\n  document.querySelectorAll('.catsec').forEach(sec => {\n    let vis = 0;\n    sec.querySelectorAll('.card').forEach(cd => { const hit = !q || (cd.dataset.q || '').includes(q); cd.style.display = hit ? '' : 'none'; if (hit) vis++; });\n    sec.style.display = vis ? '' : 'none';\n    if (vis) any = true;\n  });\n  document.getElementById('catnone').style.display = any ? 'none' : '';\n});\n</script>"


def components_index(comps):
    body = f"""
<div class="wrap">
  <div class="hero" style="padding-bottom:0">
    <h1 style="font-size:36px">Components</h1>
    <p>Every part is a folder in the registry — preview, CSS and JS are the same files you copy.</p>
  </div>
  <div class="catsearch"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.5-4.5"/></svg><input id="catq" type="text" placeholder="Filter parts — try \u201cchart\u201d, \u201cdate\u201d, \u201cmenu\u201d\u2026" aria-label="Filter components"></div>
  <p class="catnone" id="catnone" style="display:none">No parts match that word. Try something shorter.</p>
{catalog_sections(comps)}
{CATALOG_SCRIPT}
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

def _doc_title(slug):
    for d in DOCS:
        if d[0] == slug:
            return d[1]
    return slug


def _nav_link(url, label, current):
    on = ' class="on"' if current == url else ''
    return f'<a href="{url}"{on}>{esc(label)}</a>'


def _sec(title, links_html):
    return '<nav class="side"><h4>' + esc(title) + '</h4>' + links_html + '</nav>'


def tree_sections(comps, active, current):
    gs = ['introduction', 'getting-started', 'installation', 'install-html', 'install-astro', 'install-laravel', 'cli', 'registry', 'mcp', 'theming', 'dark-mode', 'accessibility', 'rtl', 'changelog']
    concepts = ['why-vanilla', 'the-mold', 'anatomy', 'forms', 'from-tailwind', 'vs-shadcn']
    guides = [d[0] for d in DOCS if d[0].startswith('guide-')]
    doc = lambda slugs: ''.join(_nav_link('/docs/' + x + '/', _doc_title(x), current) for x in slugs)
    return [
        _sec('Getting Started', doc(gs)),
        _sec('Concepts', doc(concepts)),
        _sec('Guides', doc(guides)),
        sidebar(comps, active),
        _sec('Blocks', ''.join(_nav_link('/blocks/' + b['slug'] + '/', b['meta']['title'], current) for b in _all_blocks())),
        _sec('Templates', ''.join(_nav_link('/templates/' + t['slug'] + '/', t['meta']['title'], current) for t in load_templates())),
        _sec('Resources', ''.join(_nav_link(u, n, current) for u, n in [('/icons/', 'Icons'), ('/themes/', 'Themes'), ('/design-system/', 'Design System'), ('/pricing/', 'Pricing'), ('/skill/SKILL.md', 'AI Skill (SKILL.md)')])),
    ]


def nav_tree(comps, active, current):
    return '<div class="sidenav">' + ''.join(tree_sections(comps, active, current)) + '</div>'


DETAIL_JS = """<script>
  const stage = document.getElementById('stage');
  document.querySelectorAll('[data-seg]').forEach(seg => {
    seg.querySelectorAll('button').forEach(btn => btn.addEventListener('click', () => {
      seg.querySelectorAll('button').forEach(b => b.classList.remove('on'));
      btn.classList.add('on');
      const v = btn.dataset.v;
      if (seg.dataset.seg === 'theme') { v === 'dark' ? stage.setAttribute('data-theme','dark') : stage.removeAttribute('data-theme'); }
      if (seg.dataset.seg === 'width') { stage.classList.toggle('narrow', v === 'mobile'); }
      window.dispatchEvent(new Event('resize'));
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
    examples_html = ''
    if c.get('examples'):
        blocks_out = []
        for title, html_ex in c['examples']:
            blocks_out.append(f'<h3 class="exh">{esc(title)}</h3><div class="stage col exstage">{html_ex}</div>'
                              f'<div class="codebox"><div class="pane on"><pre>{esc(html_ex)}</pre><div class="copyrow"><button class="copybtn">Copy</button></div></div></div>')
        examples_html = '<section class="doc"><h2>Examples</h2>' + ''.join(blocks_out) + '</section>'
    js_tag = f'<script src="/components/{slug}/{slug}.js?v={_v(c["js"])}"></script>' if c['js'] else ''
    dep_cli = ' Dependencies are resolved and written with it.' if c['deps'] else ''
    js_step = ' The part has a script — include it after the markup; it initializes itself.' if c['js'] else ''
    install_html = f'''<section class="doc"><h2>Installation</h2>
      <h3 class="insth">CLI</h3>
      <div class="codebox"><div class="pane on"><pre>node kata-ui.mjs add {slug}</pre><div class="copyrow"><button class="copybtn">Copy</button></div></div></div>
      <p class="anote">Writes the part\u2019s CSS{(' and JS' if c['js'] else '')} into your project.{dep_cli} New to the CLI? See the <a href="/docs/cli/">CLI doc</a>.</p>
      <h3 class="insth">Manual</h3>
      <ol class="instol">
        <li>Load <code>tokens.css</code> once, before any part.</li>
        <li>Copy the CSS tab into your stylesheet.</li>
        <li>Copy the HTML where it belongs.{js_step}</li>
      </ol></section>'''
    cls_seen = []
    for mm in re.finditer(r'\.([a-zA-Z][\w-]*)', c['css']):
        if mm.group(1) not in cls_seen:
            cls_seen.append(mm.group(1))
    hooks = []
    for src in (c['preview'], c['js'] or ''):
        for mm in re.finditer(r'data-[a-z0-9-]+', src):
            if mm.group(0) not in hooks:
                hooks.append(mm.group(0))
    arias = []
    for mm in re.finditer(r'aria-[a-z]+', c['preview']):
        if mm.group(0) not in arias:
            arias.append(mm.group(0))
    rows = ''
    for n in cls_seen[:14]:
        rows += f'<tr><td><code>.{esc(n)}</code></td><td>class</td></tr>'
    if len(cls_seen) > 14:
        rows += f'<tr><td><code>+{len(cls_seen) - 14} more</code></td><td>classes \u2014 see the CSS tab</td></tr>'
    for h in hooks[:10]:
        rows += f'<tr><td><code>{esc(h)}</code></td><td>data hook</td></tr>'
    for a in arias[:8]:
        rows += f'<tr><td><code>{esc(a)}</code></td><td>ARIA</td></tr>'
    anatomy_html = ''
    if rows:
        anatomy_html = ('<section class="doc"><h2>Anatomy</h2>'
                        '<p class="anote">The public surface of this part, read from its own source. Class names are the API \u2014 the CSS tab above is the full contract.</p>'
                        f'<table class="anatomy"><tbody>{rows}</tbody></table></section>')
    siblings = [x for x in comps if x['meta']['category'] == m['category'] and x['slug'] != slug][:4]
    related = ''
    if siblings:
        related = '<section class="doc"><h2>Related parts</h2><div class="cards">' + ''.join(card(x) for x in siblings) + '</div></section>'
    used_in_blocks = [b for b in _all_blocks() if slug in b['meta'].get('uses', [])]
    used_in = ''
    if used_in_blocks:
        links = ''.join(f'<a class="card" href="/blocks/{b["slug"]}/"><h3>{esc(b["meta"]["title"])}</h3><p>{esc(b["meta"]["description"])}</p></a>' for b in used_in_blocks)
        used_in = f'<section class="doc"><h2>Used in these blocks</h2><div class="cards">{links}</div></section>'
    body = f"""
<div class="wrap">
  <div class="layout">
    {nav_tree(comps, slug, '/components/' + slug + '/')}
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
      {install_html}
      {examples_html}
      <section class="doc"><h2>Usage</h2><p>{esc(m.get('usage',''))}</p></section>
      <section class="doc"><h2>Accessibility</h2><p>{esc(m.get('a11y',''))}</p></section>
      {anatomy_html}
      {used_in}
      {related}
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
.ds .lead{margin-top:10px;color:var(--ink2);font-size:15px;line-height:1.85;max-width:64ch;letter-spacing:.012em}
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
.ic .lead{margin-top:10px;color:var(--ink2);font-size:15px;line-height:1.85;max-width:64ch;letter-spacing:.012em}
.icgrid{margin-top:26px;display:grid;grid-template-columns:repeat(auto-fill,minmax(104px,1fr));gap:9px}
.iccell{border:1px solid var(--hair);border-radius:12px;background:#fff;padding:16px 6px 11px;display:grid;justify-items:center;gap:9px;cursor:pointer;font:inherit;color:var(--ink)}
.iccell:hover{border-color:var(--ink3)}
.iccell .nm{font-family:var(--mono);font-size:10.5px;color:var(--ink2)}
.icstat{margin-top:14px;font-size:13px;color:var(--ink2);min-height:20px}
.icstat b{color:var(--acc);font-weight:600}
</style>"""

BRAND_GENRES = [
    ('Social & messaging', ['x', 'instagram', 'facebook', 'threads', 'tiktok', 'linkedin', 'slack', 'discord', 'telegram', 'whatsapp', 'line', 'messenger', 'reddit', 'bluesky', 'meta']),
    ('Video & audio', ['youtube', 'twitch', 'netflix', 'spotify', 'soundcloud']),
    ('AI', ['claude', 'gemini', 'openai', 'perplexity', 'mistral']),
    ('Development', ['github', 'gitlab', 'bitbucket', 'stackoverflow', 'codepen', 'docker', 'npm']),
    ('Frameworks & site tools', ['react', 'vue', 'tailwind', 'wordpress', 'figma', 'notion', 'framer', 'linear']),
    ('Commerce & payments', ['shopify', 'stripe', 'paypal', 'mastercard']),
    ('Platforms & browsers', ['apple', 'google', 'microsoft', 'android', 'chrome', 'safari', 'firefox']),
    ('Cloud & hosting', ['vercel', 'netlify', 'cloudflare', 'supabase', 'firebase']),
]

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
    bfiles = sorted((ROOT / 'icons' / 'brands').glob('*.svg')) if (ROOT / 'icons' / 'brands').exists() else []
    bmap = {}
    for f in bfiles:
        raw = f.read_text(encoding='utf-8').strip()
        data[f.stem] = raw
        inline = raw.replace('<svg ', '<svg width="22" height="22" aria-hidden="true" ', 1)
        bmap[f.stem.replace('brand-', '')] = '<button class="iccell" type="button" data-icon="' + f.stem + '">' + inline + '<span class="nm">' + f.stem.replace('brand-', '') + '</span></button>'
    brand_section = ''
    if bmap:
        used = set()
        groups = []
        for gname, members in BRAND_GENRES:
            cells = ''.join(bmap[m] for m in members if m in bmap)
            for m in members:
                if m in bmap:
                    used.add(m)
            if cells:
                groups.append('<h3 style="font-size:15px;font-weight:600;letter-spacing:-.01em;margin:28px 0 0">' + gname + '</h3><div class="icgrid" style="margin-top:12px">' + cells + '</div>')
        rest = ''.join(bmap[k] for k in sorted(bmap) if k not in used)
        if rest:
            groups.append('<h3 style="font-size:15px;font-weight:600;letter-spacing:-.01em;margin:28px 0 0">More marks</h3><div class="icgrid" style="margin-top:12px">' + rest + '</div>')
        brand_section = ('<h2 style="font-size:21px;font-weight:600;letter-spacing:-.02em;margin-top:38px">Brand marks</h2>'
          '<p style="margin-top:8px;color:var(--ink2);font-size:13.5px;line-height:1.8;max-width:64ch">' + str(len(bmap)) + ' marks, grouped by the job they do on a site: social links, sign-in buttons, integration grids, logo clouds. Brand marks belong to their owners and are here for nominative use only — using one does not imply endorsement, and they are never part of the KATA identity. They are also the one exception to the three-shape mold: a mark keeps its owner’s geometry.</p>'
          + ''.join(groups))
    script = "<script>var ICONS=__DATA__;\ndocument.querySelectorAll('[data-icon]').forEach(function(b){b.addEventListener('click',function(){var n=b.dataset.icon;var done=function(){document.getElementById('icstat').innerHTML='<b>'+n+'</b> copied.';};if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(ICONS[n]).then(done,done);}else{done();}});});\n</script>".replace('__DATA__', _json.dumps(data))
    body = "\n<div class=\"wrap ic\">\n  <h1>Icons</h1>\n  <p class=\"lead\">One mold for icons, too: a 24 grid, a 1.7 stroke, square caps and bevel joins — a sharper cut than the usual round line icon. Every glyph is drawn from three shapes only — the circle, the 45° line, and the r2 corner — so the whole set reads as cut from one block. A few carry the KATA signature: a solid core at the center — the same vermillion that sits inside the Switch and the Radio. Click any icon to copy its SVG. For anything beyond this set, Lucide is the nearest kin (24 grid, round) and sits comfortably alongside.</p>\n  <p class=\"icstat\" id=\"icstat\">" + str(len(files)) + " icons. Every one is a single file in the registry.</p>\n  <div class=\"icgrid\">" + ''.join(cells) + "</div>" + brand_section + "\n</div>\n" + FOOTER + "\n" + script + "\n</body>\n</html>"
    return head('Icons — KATA UI', 'The KATA icon set: 24 grid, 1.7 stroke, square caps, click to copy the SVG.', ICONS_STYLE) + body



PRICING_STYLE = """<style>
.pr .tiers{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:30px}
.pr .tier{border:1px solid var(--hair);border-radius:16px;padding:26px;background:#fff}
.pr .tier.pro{border-color:var(--ink);box-shadow:0 24px 50px -30px rgba(16,24,40,.35)}
.pr .tier h2{font-size:19px;display:flex;align-items:baseline;gap:10px}
.pr .price{font-size:34px;font-weight:700;letter-spacing:-.03em;margin:12px 0 2px}
.pr .per{color:var(--ink3);font-size:13px}
.pr .tier ul{list-style:none;margin:18px 0 0;padding:0;display:grid;gap:9px}
.pr .tier li{font-size:13.5px;color:var(--ink2);display:flex;gap:9px;line-height:1.6}
.pr .tier li::before{content:"";flex:none;width:7px;height:7px;border-radius:50%;background:var(--ink);margin-top:7px}
.pr .tier.pro li::before{background:#eb471f}
.pr .cta{display:inline-flex;margin-top:22px;padding:10px 18px;border-radius:9px;background:var(--ink);color:#fff;font-weight:550;font-size:14px;text-decoration:none}
.pr .cta.ghost{background:#fff;color:var(--ink2);border:1px solid var(--hair);cursor:default}
.pr .note{margin-top:14px;font-size:12.5px;color:var(--ink3);line-height:1.7}
.pr .qa{margin-top:44px;display:grid;gap:0}
.pr .qa div{border-top:1px solid var(--hair);padding:18px 2px}
.pr .qa h3{font-size:15px;margin-bottom:6px}
.pr .qa p{font-size:13.5px;color:var(--ink2);line-height:1.8;max-width:640px}
@media (max-width:720px){.pr .tiers{grid-template-columns:1fr}}
</style>"""

def waitlist_form(label='Get one email when Pro sales open', button='Notify me',
                  note='One email, on launch day. No newsletter, no list for sale — addresses land in the maker\'s inbox and nowhere else.',
                  done='You\'re on the list. One email, when the doors open.',
                  fail='That didn\'t go through — email kajiyama@seventh-well.com and you will be added by hand.',
                  dark=False):
    cls = 'wl wl-dark' if dark else 'wl'
    import json as _json
    fail_js = _json.dumps(fail)
    button_js = _json.dumps(button)
    return f'''<form class="{cls}" data-wl novalidate>
  <label class="wl-label">{label}</label>
  <div class="wl-row">
    <input type="email" required placeholder="you@studio.com" autocomplete="email" aria-label="Email address">
    <button type="submit">{button}</button>
  </div>
  <p class="wl-note">{note}</p>
  <p class="wl-done" hidden>{done}</p>
</form>
<script>
document.querySelectorAll('[data-wl]').forEach(function(f){{ if(f.__wl) return; f.__wl = 1;
  f.addEventListener('submit', function(e){{ e.preventDefault();
    var input = f.querySelector('input'), btn = f.querySelector('button');
    if(!input.checkValidity()){{ input.reportValidity(); return; }}
    btn.disabled = true; btn.textContent = '…';
    fetch('https://formsubmit.co/ajax/kajiyama@seventh-well.com', {{method:'POST',
      headers:{{'Content-Type':'application/json','Accept':'application/json'}},
      body: JSON.stringify({{email: input.value, _subject:'KATA UI — Pro waitlist', _template:'table', _captcha:'false'}})
    }}).then(function(r){{ if(!r.ok) throw 0;
      f.querySelector('.wl-row').hidden = true; f.querySelector('.wl-note').hidden = true;
      f.querySelector('.wl-label').hidden = true; f.querySelector('.wl-done').hidden = false;
    }}).catch(function(){{ btn.disabled = false; btn.textContent = {button_js};
      f.querySelector('.wl-note').textContent = {fail_js}; }});
  }});
}});
</script>'''

def pricing_page():
    body = """
<div class="wrap pr">
  <h1>Pricing</h1>
  <p class="lead">The parts are free, forever. What Pro sells is the assembled work — the blocks and templates — for one payment, once.</p>
  <div class="tiers">
    <div class="tier">
      <h2>Free</h2>
      <p class="price">$0</p>
      <p class="per">MIT licensed. No account, no catch.</p>
      <ul>
        <li>All 136 components, with live previews and examples</li>
        <li>150 icons and 56 brand marks</li>
        <li>5 themes and the full design-token system</li>
        <li>The CLI, the registry, the MCP server and the AI Skill</li>
        <li>All documentation and guides</li>
      </ul>
      <a class="cta" href="/components/">Browse the parts</a>
      <p class="note">The parts are the commons: they stay free whatever Pro does. A library nobody can afford to start with helps nobody.</p>
    </div>
    <div class="tier pro">
      <h2>Pro</h2>
      <p class="price">$129</p>
      <p class="per">One payment. Lifetime. Every future block and template included.</p>
      <ul>
        <li>All blocks — page chrome, marketing and product sections</li>
        <li>All templates — whole pages, assembled and styled</li>
        <li>Key-gated downloads of the composed work</li>
        <li>Every block and template added later, at no extra cost</li>
        <li>No seats, no per-project fees, no subscription</li>
      </ul>
      <span class="cta ghost">Sales open soon</span>
      __WAITLIST__
      <p class="note">Not on sale yet: the blocks and templates are still open on this site while Pro is being prepared. When sales open, $129 is the price — once, and the code is yours either way.</p>
    </div>
  </div>
  <div class="qa">
    <div><h3>Why charge for blocks and not parts?</h3><p>A single part is an afternoon of work and, honestly, an AI can draft one. A set of blocks that compose without friction — same tokens, same spacing, same voice — is the accumulated discipline of the whole catalog. That is what Pro prices.</p></div>
    <div><h3>What happens to code I already copied?</h3><p>Nothing, ever. Copied code is yours under its license; there is no activation, no telemetry, no kill switch. Pro changes what new downloads cost, not what your files do.</p></div>
    <div><h3>Will the parts go paid later?</h3><p>No. The line is permanent: components, icons, themes and the tooling are free; the composed work is Pro. If that line ever moved, the trust the catalog runs on would go with it.</p></div>
  </div>
</div>
""" + FOOTER + """
</body>
</html>"""
    return (head('Pricing — KATA UI', 'KATA UI pricing: every component free forever under MIT; Pro is the blocks and templates, $129 once, lifetime.', PRICING_STYLE) + body).replace('__WAITLIST__', waitlist_form())

JA_STYLE = """<style>
.ja-hero{padding:34px 0 6px}
.ja-hero h1{font-size:34px;line-height:1.35;letter-spacing:.05em}
.ja-hero .lead{margin-top:14px;letter-spacing:.04em}
.ja-stats{display:flex;gap:15px 34px;flex-wrap:wrap;margin-top:26px;padding-top:20px;border-top:1px solid var(--hair)}
.ja-stats div b{display:block;font-size:23px;font-weight:650;letter-spacing:-.01em}
.ja-stats div span{font-size:12px;color:var(--ink3)}
.ja-sec{margin-top:44px}
.ja-sec h2{font-size:20px;font-weight:650;letter-spacing:.05em}
.ja-sec p{font-size:14px;line-height:1.9;color:var(--ink2);margin-top:9px;max-width:640px;letter-spacing:.04em}
.ja-steps{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:16px}
.ja-step{border:1px solid var(--hair);border-radius:13px;padding:17px;background:#fff}
.ja-step .no{font-size:11px;font-weight:650;letter-spacing:.14em;color:var(--acc)}
.ja-step h3{font-size:14.5px;margin:7px 0 5px;letter-spacing:.04em}
.ja-step p{font-size:13px;line-height:1.8;color:var(--ink2);letter-spacing:.04em}
.ja-cards{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:16px}
.ja-card{border:1px solid var(--hair);border-radius:13px;padding:19px;background:#fff;text-decoration:none;color:inherit;display:block}
.ja-card h3{font-size:15.5px;letter-spacing:.04em}
.ja-card p{font-size:13px;line-height:1.8;color:var(--ink2);margin-top:6px;letter-spacing:.04em}
.ja-card .go{font-size:12.5px;font-weight:600;color:var(--acc);margin-top:10px;display:inline-block}
.ja-wl{margin-top:44px;background:#101013;border-radius:16px;padding:26px;color:#f4f4f5}
.ja-wl h2{color:#f4f4f5}
.ja-wl p{color:#c9c9ce}
@media (max-width:720px){.ja-steps,.ja-cards{grid-template-columns:1fr}.ja-hero h1{font-size:27px}.ja-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:16px 18px}}
</style>"""

def ja_page():
    body = """
<div class="wrap ja">
  <div class="ja-hero">
    <h1>型から生まれる、UI部品。</h1>
    <p class="lead">KATA UIは、素のHTML・CSS・JavaScriptだけでできた実用コンポーネント集です。フレームワークなし、ビルドなし、依存なし。部品をコピーして貼れば、そのコードはあなたのものになります。</p>
    <div class="ja-stats">
      <div><b>136</b><span>コンポーネント</span></div>
      <div><b>21</b><span>ブロック</span></div>
      <div><b>7</b><span>テンプレート</span></div>
      <div><b>150</b><span>アイコン</span></div>
      <div><b>0</b><span>依存</span></div>
    </div>
  </div>
  <section class="ja-sec">
    <h2>使い方</h2>
    <div class="ja-steps">
      <div class="ja-step"><span class="no">STEP 1</span><h3>トークンを読み込む</h3><p>tokens.cssを一度読み込むだけ。色・余白・角丸・動きはすべてそこから来ます。それが「型」です。</p></div>
      <div class="ja-step"><span class="no">STEP 2</span><h3>部品を貼る</h3><p>部品ページからHTML・CSS・JSをコピー。インストールもパッケージもありません。</p></div>
      <div class="ja-step"><span class="no">STEP 3</span><h3>型を調整する</h3><p>変えるのは部品ではなくトークン。型をひとつ変えれば、ページ全体が鋳直されます。</p></div>
    </div>
  </section>
  <section class="ja-sec">
    <h2>棚の紹介</h2>
    <p>実務の部品が中心ですが、他にはない棚もあります。動きの部品を集めた Motion、型破りを自称する KATAYABURI、そして和柄を幾何から作図する Wagara、朱色の判子、 金継ぎのカード、暖簾、縦書きを収めた Japan ジャンル。</p>
    <div class="ja-cards">
      <a class="ja-card" href="/components/"><h3>カタログを見る</h3><p>全136部品にライブプレビューとコピーできるコード付き。カタログとドキュメントは英語です（部品名とコードはそのまま使えます）。</p><span class="go">Components →</span></a>
      <a class="ja-card" href="/components/wagara/"><h3>Japanジャンル</h3><p>青海波・麻の葉・七宝・市松を貼り絵ではなく作図で。判子は到着すると自分で押されます。</p><span class="go">Wagara →</span></a>
    </div>
  </section>
  <section class="ja-sec">
    <h2>料金</h2>
    <p>コンポーネントとアイコンは永久無料（MIT）。有料の Pro は、組み上げ済みのブロックとテンプレートで、$129の買い切り・買い切り後の追加料金なし。販売は近日開始です。</p>
  </section>
  <div class="ja-wl">
    <h2>販売開始の通知</h2>
    <p>Proの販売が始まった日に、1通だけメールします。それ以外の連絡はしません。</p>
    """ + waitlist_form(label='販売開始日に1通だけ受け取る', button='通知する',
                        note='販売開始日の1通だけ。ニュースレターも、第三者への提供もありません。',
                        done='登録しました。販売開始日に1通だけ送ります。',
                        fail='送信できませんでした — kajiyama@seventh-well.com 宛にご連絡いただければ手動で追加します。',
                        dark=True) + """
  </div>
</div>
""" + FOOTER + """
</body>
</html>"""
    return (head('KATA UI — 日本語', 'KATA UIの日本語案内。素のHTML/CSS/JSのUIコンポーネント集、136部品・21ブロック・7テンプレート。フレームワークなし、依存なし。', JA_STYLE) + body).replace('<html lang="en">', '<html lang="ja">', 1)

SC_STYLE = """<style>
.sc-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:22px}
.sc-card{border:1px solid var(--hair);border-radius:14px;padding:20px;background:#fff;text-decoration:none;color:inherit;display:block}
.sc-card:hover{border-color:var(--ink3)}
.sc-card .k{font-size:11px;font-weight:650;letter-spacing:.14em;color:var(--acc);text-transform:uppercase}
.sc-card h3{font-size:16px;margin:7px 0 5px}
.sc-card p{font-size:13px;line-height:1.75;color:var(--ink2)}
.sc-card .go{font-size:12.5px;font-weight:600;margin-top:10px;display:inline-block}
@media (max-width:720px){.sc-grid{grid-template-columns:1fr}}
</style>"""

def showcase_page(templates, blocks):
    cards = ''.join(
        f'<a class="sc-card" href="/templates/{esc(tp["slug"])}/"><span class="k">Template — live page</span><h3>{esc(tp["meta"]["title"])}</h3><p>{esc(tp["meta"]["description"])}</p><span class="go">Open the live page →</span></a>'
        for tp in templates)
    body = """
<div class="wrap sc">
  <h1>Showcase</h1>
  <p class="lead">No mockups. Every page below is assembled from the catalog itself — the same parts, blocks and tokens the copy button hands you — and rendered live. Take any of them apart to see.</p>
  <div class="sc-grid">
    <a class="sc-card" href="/"><span class="k">This site</span><h3>kata-ui.dev itself</h3><p>The landing page's showcase and collage are not screenshots: the dashboard in the hero window, the stat cards and the charts are live parts running on the page.</p><span class="go">See it on the home page →</span></a>
    <a class="sc-card" href="/starter/kata-starter.zip"><span class="k">Starter kit</span><h3>The starter project</h3><p>Tokens, the one-file bundle and a first page, zipped. The fastest honest test of the mold: unzip, open, and everything on screen is a part.</p><span class="go">Download the starter →</span></a>
""" + cards + """
  </div>
  <p class="note" style="margin-top:20px;font-size:13px;color:var(--ink3);line-height:1.8">Building something with KATA? The maker reads every issue on the repository — a link there is how a project joins this page.</p>
</div>
""" + FOOTER + """
</body>
</html>"""
    return head('Showcase — KATA UI', 'Live pages assembled from the KATA UI catalog itself: templates, the starter kit, and this site.', SC_STYLE) + body

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
  <section><h2>Typography</h2><p class="note">Sans: {esc(tokens['font']['sans'])}<br>Mono: {esc(tokens['font']['mono'])}<br>Tracking: {esc(tokens['font']['tracking'])}<br>Leading: {esc(tokens['font']['leading'])}</p><div class="spec">{specs}</div></section>
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
.bk .lead{margin-top:10px;color:var(--ink2);font-size:15px;line-height:1.85;max-width:64ch;letter-spacing:.012em}
.bcards{margin-top:26px;display:grid;grid-template-columns:repeat(auto-fill,minmax(264px,1fr));gap:12px}
.bcard{border:1px solid var(--hair);border-radius:14px;background:#fff;padding:18px;text-decoration:none;color:var(--ink);display:block}
.bcard:hover{border-color:var(--ink3)}
.bcard h3{font-size:15.5px;font-weight:600;display:flex;align-items:center;gap:8px}
.bcard p{margin-top:7px;font-size:13px;color:var(--ink2);line-height:1.75}
.bcard .uses{margin-top:12px;display:flex;gap:5px;flex-wrap:wrap}
.bcard .uses span{font-family:var(--mono);font-size:10.5px;color:var(--ink2);border:1px solid var(--hair);border-radius:99px;padding:2px 8px}
</style>"""

BLOCK_CATS = [('Page chrome', ['app-shell', 'site-header', 'site-footer', 'cookie-consent']),
              ('Marketing', ['pricing', 'use-cases', 'integrations', 'testimonials', 'logo-cloud', 'faq', 'cta-band', 'team', 'plan-compare']),
              ('Product', ['login', 'settings', 'stat-cards', 'kanban', 'roadmap', 'invoice', 'order-confirmation', 'filter-toolbar'])]

def blocks_index(blocks):
    def card(b):
        m = b['meta']
        uses = ''.join(f'<span>{esc(u)}</span>' for u in m.get('uses', []))
        return f"""<a class="bcard" href="/blocks/{b['slug']}/">
  <h3>{esc(m['title'])} <span class="st st-{esc(m.get('status','beta'))}">{esc(m.get('status','beta'))}</span> <span class="st st-pro">Pro</span></h3>
  <p>{esc(m['description'])}</p>
  <span class="uses">{uses}</span>
</a>"""
    by_slug = {b['slug']: b for b in blocks}
    seen = set()
    secs = []
    for cat, slugs in BLOCK_CATS:
        group = [by_slug[s] for s in slugs if s in by_slug]
        seen.update(b['slug'] for b in group)
        if group:
            secs.append(f'<section class="catsec"><h2>{esc(cat)}</h2><div class="bcards">' + ''.join(card(b) for b in group) + '</div></section>')
    rest = [b for b in blocks if b['slug'] not in seen]
    if rest:
        secs.append('<section class="catsec"><h2>More blocks</h2><div class="bcards">' + ''.join(card(b) for b in rest) + '</div></section>')
    body = f"""
<div class="wrap bk">
  <h1>Blocks</h1>
  <p class="lead">Components, composed into whole sections. A block is copied the same way as a component — HTML, CSS and JS — and every part inside it stays a part you already own. Start from a block, then take it apart with the catalog.</p>
{''.join(secs)}
</div>
{FOOTER}
</body>
</html>"""
    return head('Blocks — KATA UI', 'Whole sections composed from KATA components: sign-in, pricing, settings, app shells.', BLOCK_STYLE) + body

def install_section(slug, noun, has_js, dep_note=''):
    js_bit = ' and JS' if has_js else ''
    js_step = ' The page has scripts — include them after the markup; they initialize themselves.' if has_js else ''
    return f'''<section class="doc"><h2>Installation</h2>
      <h3 class="insth">CLI</h3>
      <div class="codebox"><div class="pane on"><pre>node kata-ui.mjs add {slug}</pre><div class="copyrow"><button class="copybtn">Copy</button></div></div></div>
      <p class="anote">Writes the {noun}\u2019s CSS{js_bit} into your project.{dep_note} New to the CLI? See the <a href="/docs/cli/">CLI doc</a>.</p>
      <h3 class="insth">Manual</h3>
      <ol class="instol">
        <li>Load <code>tokens.css</code> once, before any part.</li>
        <li>Copy the CSS tab into your stylesheet, with the CSS of everything listed under \u201cBuilt from\u201d above.</li>
        <li>Copy the HTML where it belongs.{js_step}</li>
      </ol></section>'''

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
    install_html = install_section(slug, 'block', bool(b['js']), ' Everything it is built from comes with it.' if links else '')
    body = f"""
<div class="wrap">
  <main class="detail">
    <p class="crumb"><a href="/blocks/">Blocks</a> / {esc(m['title'])}</p>
    <h1>{esc(m['title'])} <span class="st st-{esc(m.get('status','beta'))}">{esc(m.get('status','beta'))}</span> <span class="st st-pro">Pro</span></h1>
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
    {install_html}
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


def load_templates():
    templates = []
    tdir = ROOT / 'templates'
    if not tdir.exists():
        return templates
    for d in sorted(tdir.iterdir()):
        if not d.is_dir():
            continue
        meta = json.loads((d / 'meta.json').read_text(encoding='utf-8'))
        slug = d.name
        preview = (d / 'preview.html').read_text(encoding='utf-8')
        css = (d / f'{slug}.css').read_text(encoding='utf-8')
        js_file = d / f'{slug}.js'
        js = js_file.read_text(encoding='utf-8') if js_file.exists() else None
        templates.append(dict(slug=slug, meta=meta, preview=preview, css=css, js=js))
    templates.sort(key=lambda t: t['meta']['title'])
    return templates

TPL_STYLE = """<style>
.tk h1{font-size:32px;font-weight:600;letter-spacing:-.025em;margin-top:26px}
.tk .lead{margin-top:10px;color:var(--ink2);font-size:15px;line-height:1.85;max-width:64ch;letter-spacing:.012em}
.tplcards{margin-top:26px;display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:14px}
.tplcard{border:1px solid var(--hair);border-radius:14px;background:#fff;color:var(--ink);display:block;overflow:hidden;position:relative}
.tplcard .tplmeta h3 a{color:inherit;text-decoration:none}
.tplcard .tplmeta h3 a::after{content:"";position:absolute;inset:0}
.tplcard:hover{border-color:var(--ink3)}
.tplthumb{height:190px;overflow:hidden;border-bottom:1px solid var(--hair);position:relative;background:var(--soft)}
.tplscale{width:1080px;transform:scale(.306);transform-origin:top left;pointer-events:none}
.tplmeta{padding:16px 18px 18px}
.tplmeta h3{font-size:15.5px;font-weight:600;display:flex;align-items:center;gap:8px}
.tplmeta p{margin-top:7px;font-size:13px;color:var(--ink2);line-height:1.75}
.tplmeta .uses{margin-top:12px;display:flex;gap:5px;flex-wrap:wrap}
.tplmeta .uses span{font-family:var(--mono);font-size:10.5px;color:var(--ink2);border:1px solid var(--hair);border-radius:99px;padding:2px 8px}
.tplframe{border:1px solid var(--hair);border-radius:14px;overflow:hidden;background:#fff}
.tplbar{display:flex;align-items:center;gap:10px;padding:9px 12px;border-bottom:1px solid var(--hair);background:var(--soft)}
.tpldots{display:flex;gap:6px}
.tpldots i{width:10px;height:10px;border-radius:50%;background:var(--hair);display:block}
.tplurl{font-family:var(--mono);font-size:11.5px;color:var(--ink2);background:#fff;border:1px solid var(--hair);border-radius:7px;padding:3px 12px}
.tplstage{border:0;border-radius:0;max-height:none}
</style>"""

def templates_index(templates):
    cards = []
    for t in templates:
        m = t['meta']
        uses = ''.join(f'<span>{esc(u)}</span>' for u in m.get('blocks', []) + m.get('uses', []))
        cards.append(f"""<article class="tplcard">
  <div class="tplthumb"><div class="tplscale">{t['preview']}</div></div>
  <div class="tplmeta">
  <h3><a href="/templates/{t['slug']}/">{esc(m['title'])}</a> <span class="st st-{esc(m.get('status','beta'))}">{esc(m.get('status','beta'))}</span> <span class="st st-pro">Pro</span></h3>
  <p>{esc(m['description'])}</p>
  <span class="uses">{uses}</span>
  </div>
</article>""")
    body = f"""
<div class="wrap tk">
  <h1>Templates</h1>
  <p class="lead">Whole pages, assembled. A template is a block that kept going — the app shell, the stats, the chart and the table already in their places. Copy the page the same way you copy a part, then take it apart with the catalog.</p>
  <div class="tplcards">
{''.join(cards)}
  </div>
</div>
{FOOTER}
</body>
</html>"""
    extra = TPL_STYLE + ''.join(f'<link rel="stylesheet" href="/templates/{t["slug"]}/{t["slug"]}.css?v={_v(t["css"])}">' for t in templates)
    return head('Templates — KATA UI', 'Full pages composed from KATA parts and blocks: dashboards, inboxes, landing pages.', extra) + body

def template_detail(templates, idx, comps, blocks):
    t = templates[idx]
    m = t['meta']
    slug = t['slug']
    display_html = re.sub(r'\s*<link rel="stylesheet"[^>]*>', '', t['preview']).strip()
    tabs = [('HTML', display_html), ('CSS', t['css'])]
    if t['js']:
        tabs.append(('JS', t['js']))
    def tab_btn(i, name):
        on = ' class="on"' if i == 0 else ''
        return f'<button data-tab="{name}"{on}>{name}</button>'
    tab_btns = ''.join(tab_btn(i, name) for i, (name, _) in enumerate(tabs))
    panes = ''.join(
        f'<div class="pane{" on" if i == 0 else ""}" data-pane="{name}"><pre>{esc(code)}</pre><div class="copyrow"><button class="copybtn">Copy</button></div></div>'
        for i, (name, code) in enumerate(tabs))
    by_slug = {x['slug']: x for x in comps}
    blk_by_slug = {x['slug']: x for x in blocks}
    bits = []
    if m.get('blocks'):
        bits.append('Blocks: ' + ', '.join(f'<a href="/blocks/{u}/">{esc(blk_by_slug[u]["meta"]["title"])}</a>' for u in m['blocks'] if u in blk_by_slug))
    if m.get('uses'):
        bits.append('Parts: ' + ', '.join(f'<a href="/components/{u}/">{esc(by_slug[u]["meta"]["title"])}</a>' for u in m['uses'] if u in by_slug))
    deps_html = f'<p class="deps">Built from: {" &middot; ".join(bits)} — include their CSS alongside this template.</p>' if bits else ''
    prev_html = next_html = '<span style="flex:1"></span>'
    if idx > 0:
        pb = templates[idx - 1]
        prev_html = f'<a href="/templates/{pb["slug"]}/"><span class="dir">Previous</span><div class="nm">{esc(pb["meta"]["title"])}</div></a>'
    if idx < len(templates) - 1:
        nb = templates[idx + 1]
        next_html = f'<a class="next" href="/templates/{nb["slug"]}/"><span class="dir">Next</span><div class="nm">{esc(nb["meta"]["title"])}</div></a>'
    install_html = install_section(slug, 'template', bool(t['js']), ' Everything it is built from comes with it.' if bits else '')
    scripts = ''
    for u in m.get('uses', []):
        cj = next((x['js'] for x in comps if x['slug'] == u), None)
        if cj:
            scripts += f'<script src="/components/{u}/{u}.js?v={_v(cj)}"></script>'
    for u in m.get('blocks', []):
        bj = next((x['js'] for x in blocks if x['slug'] == u), None)
        if bj:
            scripts += f'<script src="/blocks/{u}/{u}.js?v={_v(bj)}"></script>'
    if t['js']:
        scripts += f'<script src="/templates/{slug}/{slug}.js?v={_v(t["js"])}"></script>'
    body = f"""
<div class="wrap">
  <main class="detail">
    <p class="crumb"><a href="/templates/">Templates</a> / {esc(m['title'])}</p>
    <h1>{esc(m['title'])} <span class="st st-{esc(m.get('status','beta'))}">{esc(m.get('status','beta'))}</span> <span class="st st-pro">Pro</span></h1>
    <p class="desc">{esc(m['description'])}</p>
    <div class="stagebar">
      <span class="lbl">Preview</span>
      <span class="seg" data-seg="width"><button data-v="desktop" class="on">Desktop</button><button data-v="mobile">Mobile</button></span>
      <span class="seg" data-seg="theme"><button data-v="light" class="on">Light</button><button data-v="dark">Dark</button></span>
    </div>
    <div class="tplframe">
      <div class="tplbar"><span class="tpldots"><i></i><i></i><i></i></span><span class="tplurl">{esc(m.get('url','example.com'))}</span></div>
      <div class="stage col tplstage" id="stage">
{t['preview']}
      </div>
    </div>
    {deps_html}
    <div class="codebox">
      <div class="codetabs">{tab_btns}</div>
      {panes}
    </div>
    {install_html}
    <section class="doc"><h2>Usage</h2><p>{esc(m.get('usage',''))}</p></section>
    <div class="prevnext">{prev_html}{next_html}</div>
  </main>
</div>
{FOOTER}
{scripts}
{DETAIL_JS}
</body>
</html>"""
    extra = f'<link rel="stylesheet" href="/templates/{slug}/{slug}.css?v={_v(t["css"])}">' + TPL_STYLE
    return head(f"{m['title']} — Templates — KATA UI", m['description'], extra) + body


def load_themes():
    return json.loads((ROOT / 'system' / 'themes.json').read_text(encoding='utf-8'))

def load_dentou():
    return json.loads((ROOT / 'system' / 'dentou.json').read_text(encoding='utf-8'))

def theme_css(t):
    return ('/* KATA UI theme: ' + t['label'] + ' — load AFTER tokens.css.\n'
            '   A theme moves the accent only. Neutrals, motion and the vermillion core never change. */\n'
            ':root{\n'
            '  --k-accent:' + t['accent'] + ';\n'
            '  --k-accent-ink:' + t['ink'] + ';\n'
            '  --k-accent-bg:rgba(' + t['rgb'] + ',.08);\n'
            '  --k-accent-bg-strong:rgba(' + t['rgb'] + ',.1);\n'
            '  --k-accent-line:rgba(' + t['rgb'] + ',.18);\n'
            '}\n'
            '[data-theme="dark"]{\n'
            '  --k-accent-ink:' + t['darkInk'] + ';\n'
            '}\n')

THEME_STYLE = """<style>
.th h1{font-size:32px;font-weight:600;letter-spacing:-.025em;margin-top:26px}
.th .lead{margin-top:10px;color:var(--ink2);font-size:15px;line-height:1.85;max-width:64ch;letter-spacing:.012em}
.thgrid{margin-top:24px;display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:10px}
.thcard{border:1px solid var(--hair);border-radius:12px;background:#fff;padding:14px;text-align:left;cursor:pointer;font:inherit;color:var(--ink)}
.thcard:hover{border-color:var(--ink3)}
.thcard.on{border-color:var(--ink);box-shadow:0 0 0 1px var(--ink)}
.thcard .sw{display:flex;gap:5px;margin-bottom:11px}
.thcard .sw i{width:22px;height:22px;border-radius:7px;display:block;border:1px solid var(--hair)}
.thcard .nm{font-size:14px;font-weight:600}
.thcard .nt{font-size:12px;color:var(--ink2);margin-top:3px;line-height:1.6}
.thdemo{margin-top:22px;border:1px solid var(--hair);border-radius:14px;background:#fff;padding:22px;display:flex;gap:22px;align-items:center;flex-wrap:wrap}
.thdemo .lbl{font-family:var(--mono);font-size:11px;color:var(--ink3);letter-spacing:.06em;width:100%}
.thcode{margin-top:16px;border:1px solid var(--hair);border-radius:12px;overflow:hidden}
.thcode pre{margin:0;padding:16px;overflow:auto;font-family:var(--mono);font-size:12px;line-height:1.75;background:var(--soft)}
.thcode .bar{display:flex;gap:8px;align-items:center;padding:9px 12px;border-bottom:1px solid var(--hair);background:#fff}
.thcode .bar b{font-size:12.5px;margin-right:auto}
.thcode .bar a,.thcode .bar button{font:inherit;font-size:12px;border:1px solid var(--hair);background:#fff;border-radius:7px;padding:5px 11px;cursor:pointer;color:var(--ink);text-decoration:none}
</style>"""

BUILDER_STYLE = """<style>
.thbuild{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin:18px 0 0;padding:16px;border:1px solid var(--hair);border-radius:14px;background:var(--paper)}
.thbuild input[type=color]{width:46px;height:46px;border:1px solid var(--hair);border-radius:10px;background:none;padding:3px;cursor:pointer;flex:none}
.thbuild .hb{font-weight:600;font-size:13.5px;color:var(--ink)}
.thbuild .hn{font-size:12.5px;color:var(--ink3);margin-top:2px;max-width:52ch}
.thbuild code{font-family:var(--mono);font-size:12.5px;color:var(--ink2);margin-left:auto}
</style>"""

DENTOU_STYLE = """<style>
.dentou{margin-top:52px;border-top:1px solid var(--hair);padding-top:34px}
.dentou .dtk{font-family:"Yuji Syuku","Hiragino Mincho ProN","Yu Mincho",serif;font-size:15px;letter-spacing:.4em;color:var(--ink3)}
.dentou h2{font-size:24px;font-weight:600;letter-spacing:-.01em;margin-top:8px}
.dtpv{margin-top:18px;border:1px solid var(--hair);border-radius:14px;background:#fff;padding:16px 18px;display:flex;gap:14px;align-items:center;flex-wrap:wrap}
.dtpv .lbl{font-family:var(--mono);font-size:11px;color:var(--ink3);letter-spacing:.06em;width:100%}
.dtpv .dtstatus{font-size:12.5px;color:var(--ink2)}
.dtfam{font-size:12.5px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:var(--ink2);margin:28px 0 10px;display:flex;gap:12px;align-items:baseline}
.dtfam span{font-family:"Yuji Syuku","Hiragino Mincho ProN","Yu Mincho",serif;letter-spacing:.25em;color:var(--ink3);font-size:13px;text-transform:none;font-weight:400}
.dtgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(148px,1fr));gap:10px}
.dtcard{border:1px solid var(--hair);border-radius:12px;background:#fff;padding:0;text-align:left;cursor:pointer;overflow:hidden;font:inherit;color:var(--ink);display:flex;flex-direction:column;width:100%}
.dtcard .dsw{height:58px;display:block;border-bottom:1px solid var(--hair);flex:none}
.dtcard:hover{border-color:var(--ink3)}
.dtcard.on{border-color:var(--ink);box-shadow:0 0 0 1px var(--ink)}
.dtcard .dsw{height:58px;display:block;border-bottom:1px solid var(--hair)}
.dtcard .dbd{display:block;padding:10px 12px 11px}
.dtcard .dkj{font-family:"Yuji Syuku","Hiragino Mincho ProN","Yu Mincho",serif;font-size:21px;line-height:1.3;display:block;letter-spacing:.06em}
.dtcard .drm{font-size:12.5px;font-weight:600;margin-top:3px;display:flex;flex-wrap:wrap;column-gap:6px;align-items:baseline;letter-spacing:.01em}
.dtcard .drm i{font-style:normal;font-weight:400;color:var(--ink3);font-size:11.5px;letter-spacing:.05em;white-space:nowrap}
.dtcard .dhx{font-family:var(--mono);font-size:11.5px;color:var(--ink2);margin-top:5px;display:flex;justify-content:space-between;align-items:center;letter-spacing:.03em}
.dtcard .dhx .cp{font-size:10.5px;color:var(--ink3);border:1px solid var(--hair);border-radius:6px;padding:2px 7px}
.dtcard .dnt{font-size:11.5px;color:var(--ink2);line-height:1.65;margin-top:6px;display:block;letter-spacing:.01em}
.dtcard.core{cursor:default;background:var(--soft)}
.dtcard .core-tag{font-family:var(--mono);font-size:9.5px;letter-spacing:.08em;color:var(--ink3);border:1px solid var(--hair);border-radius:99px;padding:2px 7px}
</style>"""

def themes_page(themes):
    import json as _json
    cards = []
    for i, t in enumerate(themes):
        cards.append('<button class="thcard' + (' on' if i == 0 else '') + '" type="button" data-theme-card="' + t['name'] + '">'
                     '<span class="sw"><i style="background:' + t['accent'] + '"></i><i style="background:' + t['ink'] + '"></i><i style="background:rgba(' + t['rgb'] + ',.12)"></i></span>'
                     '<span class="nm">' + t['label'] + '</span><div class="nt">' + t['note'] + '</div></button>')
    demo = """<div class="thdemo" id="thdemo">
    <span class="lbl">LIVE — THE SAME PARTS, RE-CAST</span>
    <button class="btn btn-teal btn-md">Accent button</button>
    <span class="switchrow"><label class="switch teal"><input type="checkbox" checked><span class="tr"></span></label>Notifications</span>
    <span class="badge teal"><i></i>Live</span>
    <span class="badge">Neutral stays neutral</span>
  </div>"""
    builder = """<div class="thbuild">
    <input type="color" id="thcolor" value="#0e9594" aria-label="Pick an accent color">
    <div><div class="hb">Make your own</div><div class="hn">Pick any accent — the ink shade, the dark-mode ink and the washes are derived for you, and the code below becomes your theme.</div></div>
    <code id="thhex">#0e9594</code>
  </div>"""
    dentou = load_dentou()
    core_card = ('<div class="dtcard core"><span class="dsw" style="background:#eb471f"></span><span class="dbd">'
                 '<span class="dkj">型の朱</span><span class="drm">Kata vermilion<i>かたのしゅ</i></span>'
                 '<span class="dhx">#EB471F<span class="core-tag">THE CORE</span></span>'
                 '<span class="dnt">KATA\u2019s own vermilion \u2014 inside every switch and radio. It is not a theme: no color moves it.</span></span></div>')
    fams = []
    for f in dentou:
        dcards = []
        if f['family'] == 'Vermilion & reds':
            dcards.append(core_card)
        for col in f['colors']:
            slug = col['romaji'].lower().replace('\u016b', 'u').replace('\u014d', 'o')
            dcards.append('<button class="dtcard" type="button" data-dentou data-hex="' + col['hex'] + '" data-name="' + col['romaji'] + '" data-slug="' + slug + '" data-kanji="' + col['kanji'] + '">'
                          '<span class="dsw" style="background:' + col['hex'].lower() + '"></span><span class="dbd">'
                          '<span class="dkj">' + col['kanji'] + '</span>'
                          '<span class="drm">' + col['romaji'] + '<i>' + col['kana'] + '</i></span>'
                          '<span class="dhx">' + col['hex'] + '<span class="cp" data-copy="' + col['hex'] + '">Copy</span></span>'
                          '<span class="dnt">' + col['note'] + '</span></span></button>')
        fams.append('<h3 class="dtfam">' + f['family'] + '<span>' + f['family_jp'] + '</span></h3><div class="dtgrid">' + ''.join(dcards) + '</div>')
    palette = """
<section class="dentou" id="dentou">
  <span class="dtk">伝統色</span>
  <h2>Traditional colors of Japan</h2>
  <p class="lead" style="margin-top:8px">Fifty colors that began as dyes, pigments and plants \u2014 indigo, safflower, gardenia, pine soot. Click one and it is cast into the same demo and the same CSS as any theme above: the button, the switch and the badge take the color, under its own name (ai.css, yamabuki.css). The hex values follow the common references (NIPPON COLORS and the JIS customary color names); colors older than hex itself are faithful approximations, not measurements.</p>
  <div class="dtpv" id="dtpv">
    <span class="lbl">CASTING \u2014 TRADITIONAL COLORS</span>
    <button class="btn btn-teal btn-md" type="button">Accent button</button>
    <span class="badge teal"><i></i><span id="dtpvname">Teal</span></span>
    <span class="dtstatus" id="dtstatus">Pick a color below \u2014 it lands here, in the demo above, and in the CSS.</span>
  </div>
""" + ''.join(fams) + """
</section>
"""
    dentou_script = r"""<script>
function applyDentou(hex,romaji,slug,kanji){
  var rgb=h2r(hex);var hsl=rgbToHsl(rgb[0],rgb[1],rgb[2]);
  var ink=hslToHex(hsl[0],hsl[1],hsl[2]*0.84);
  var dink=hslToHex(hsl[0],Math.max(hsl[1]-8,0),hsl[2]+(100-hsl[2])*0.55);
  [demo,document.getElementById('dtpv')].forEach(function(el){
    el.style.setProperty('--k-accent',hex);
    el.style.setProperty('--k-accent-ink',ink);
    el.style.setProperty('--k-accent-bg','rgba('+rgb.join(',')+',.08)');
    el.style.setProperty('--k-accent-bg-strong','rgba('+rgb.join(',')+',.1)');
    el.style.setProperty('--k-accent-line','rgba('+rgb.join(',')+',.18)');
  });
  var css='/* KATA UI theme: '+romaji+' ('+kanji+') \u2014 a traditional color of Japan.\n   Load AFTER tokens.css. A theme moves the accent only.\n   Neutrals, motion and the vermillion core never change. */\n:root{\n  --k-accent:'+hex+';\n  --k-accent-ink:'+ink+';\n  --k-accent-bg:rgba('+rgb.join(',')+',.08);\n  --k-accent-bg-strong:rgba('+rgb.join(',')+',.1);\n  --k-accent-line:rgba('+rgb.join(',')+',.18);\n}\n[data-theme="dark"]{\n  --k-accent-ink:'+dink+';\n}\n';
  document.getElementById('thcss').textContent=css;
  document.getElementById('thname').textContent=slug+'.css';
  if(blobUrl)URL.revokeObjectURL(blobUrl);
  blobUrl=URL.createObjectURL(new Blob([css],{type:'text/css'}));
  var dl=document.getElementById('thdl');dl.href=blobUrl;dl.setAttribute('download',slug+'.css');
  document.getElementById('thhex').textContent=hex;
  document.getElementById('thcolor').value=hex.toLowerCase();
  document.getElementById('dtpvname').textContent=romaji;
  document.getElementById('dtstatus').textContent=kanji+' '+romaji+' \u2014 '+hex.toUpperCase()+' is cast. The theme CSS above is now '+slug+'.css.';
  document.querySelectorAll('[data-theme-card]').forEach(function(c){c.classList.remove('on');});
}
document.querySelectorAll('[data-dentou]').forEach(function(card){
  card.addEventListener('click',function(){
    document.querySelectorAll('[data-dentou]').forEach(function(c){c.classList.remove('on');});
    card.classList.add('on');
    applyDentou(card.dataset.hex,card.dataset.name,card.dataset.slug,card.dataset.kanji);
  });
  var cp=card.querySelector('[data-copy]');
  if(cp)cp.addEventListener('click',function(e){e.stopPropagation();if(navigator.clipboard)navigator.clipboard.writeText(cp.dataset.copy);cp.textContent='Copied';setTimeout(function(){cp.textContent='Copy';},1400);});
});
</script>"""
    script = '<script>var THEMES=' + _json.dumps(themes) + """;
var CODES={};
""" + ''.join('CODES["' + t['name'] + '"]=' + _json.dumps(theme_css(t)) + ';\n' for t in themes) + """
var demo=document.getElementById('thdemo');
function applyTheme(name){
  var t=THEMES.find(function(x){return x.name===name;});if(!t)return;
  demo.style.setProperty('--k-accent',t.accent);
  demo.style.setProperty('--k-accent-ink',t.ink);
  demo.style.setProperty('--k-accent-bg','rgba('+t.rgb+',.08)');
  demo.style.setProperty('--k-accent-bg-strong','rgba('+t.rgb+',.1)');
  demo.style.setProperty('--k-accent-line','rgba('+t.rgb+',.18)');
  document.getElementById('thcss').textContent=CODES[name];
  document.getElementById('thdl').href='/themes/'+name+'.css';
  document.getElementById('thname').textContent=name+'.css';
  document.querySelectorAll('[data-theme-card]').forEach(function(c){c.classList.toggle('on',c.dataset.themeCard===name);});
}
document.querySelectorAll('[data-theme-card]').forEach(function(c){c.addEventListener('click',function(){applyTheme(c.dataset.themeCard);});});
document.getElementById('thcopy').addEventListener('click',function(){var b=this;if(navigator.clipboard)navigator.clipboard.writeText(document.getElementById('thcss').textContent);b.textContent='Copied';setTimeout(function(){b.textContent='Copy CSS';},1600);});
function h2r(h){return [parseInt(h.slice(1,3),16),parseInt(h.slice(3,5),16),parseInt(h.slice(5,7),16)];}
function rgbToHsl(r,g,b){r/=255;g/=255;b/=255;var mx=Math.max(r,g,b),mn=Math.min(r,g,b),h=0,s=0,l=(mx+mn)/2;if(mx!==mn){var d=mx-mn;s=l>0.5?d/(2-mx-mn):d/(mx+mn);if(mx===r)h=(g-b)/d+(g<b?6:0);else if(mx===g)h=(b-r)/d+2;else h=(r-g)/d+4;h*=60;}return [h,s*100,l*100];}
function hslToHex(h,s,l){s/=100;l/=100;var a=s*Math.min(l,1-l);function f(n){var k=(n+h/30)%12;return l-a*Math.max(-1,Math.min(k-3,Math.min(9-k,1)));}function to(x){var s2=Math.round(x*255).toString(16);return s2.length<2?('0'+s2):s2;}return '#'+to(f(0))+to(f(8))+to(f(4));}
var blobUrl=null;
function applyCustom(hex){
  var rgb=h2r(hex);var hsl=rgbToHsl(rgb[0],rgb[1],rgb[2]);
  var ink=hslToHex(hsl[0],hsl[1],hsl[2]*0.84);
  var dink=hslToHex(hsl[0],Math.max(hsl[1]-8,0),hsl[2]+(100-hsl[2])*0.55);
  demo.style.setProperty('--k-accent',hex);
  demo.style.setProperty('--k-accent-ink',ink);
  demo.style.setProperty('--k-accent-bg','rgba('+rgb.join(',')+',.08)');
  demo.style.setProperty('--k-accent-bg-strong','rgba('+rgb.join(',')+',.1)');
  demo.style.setProperty('--k-accent-line','rgba('+rgb.join(',')+',.18)');
  var css='/* KATA UI theme: Custom \u2014 load AFTER tokens.css.\\n   A theme moves the accent only. Neutrals, motion and the vermillion core never change. */\\n:root{\\n  --k-accent:'+hex+';\\n  --k-accent-ink:'+ink+';\\n  --k-accent-bg:rgba('+rgb.join(',')+',.08);\\n  --k-accent-bg-strong:rgba('+rgb.join(',')+',.1);\\n  --k-accent-line:rgba('+rgb.join(',')+',.18);\\n}\\n[data-theme="dark"]{\\n  --k-accent-ink:'+dink+';\\n}\\n';
  document.getElementById('thcss').textContent=css;
  document.getElementById('thname').textContent='custom.css';
  if(blobUrl)URL.revokeObjectURL(blobUrl);
  blobUrl=URL.createObjectURL(new Blob([css],{type:'text/css'}));
  document.getElementById('thdl').href=blobUrl;
  document.getElementById('thdl').setAttribute('download','custom.css');
  document.getElementById('thhex').textContent=hex;
  document.querySelectorAll('[data-theme-card]').forEach(function(c){c.classList.remove('on');});
}
document.getElementById('thcolor').addEventListener('input',function(){applyCustom(this.value);});
applyTheme('teal');
</script>"""
    body = """
<div class="wrap th">
  <h1>Themes</h1>
  <p class="lead">A theme moves one thing: the accent. Neutrals stay zinc, motion stays measured, and the vermillion core — the mark inside the Switch and the Radio — never changes. Pick a preset to see the same parts re-cast, then take the CSS. Or skip the presets \u2014 <a href="#dentou">fifty traditional colors of Japan</a> wait below, each ready to cast.</p>
  <div class="thgrid">""" + ''.join(cards) + """
  </div>
""" + demo + builder + """
  <div class="thcode">
    <div class="bar"><b id="thname">teal.css</b><button id="thcopy" type="button">Copy CSS</button><a id="thdl" href="/themes/teal.css" download>Download</a></div>
    <pre id="thcss"></pre>
  </div>
  <p class="lead" style="margin-top:18px">Making your own is the same move by hand: redefine the five accent tokens after <span style="font-family:var(--mono);font-size:13px">tokens.css</span>. See <a href="/docs/theming/">Theming</a>.</p>
""" + palette + """</div>
""" + FOOTER + '\n' + script + dentou_script + """
</body>
</html>"""
    extra = (THEME_STYLE + BUILDER_STYLE + DENTOU_STYLE + '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Yuji+Syuku&display=swap" rel="stylesheet">' + '<link rel="stylesheet" href="/components/button/button.css">'
             '<link rel="stylesheet" href="/components/switch/switch.css">'
             '<link rel="stylesheet" href="/components/badge/badge.css">')
    return head('Themes — KATA UI', 'Accent presets for KATA UI: one token family changes, everything else holds.', extra) + body

DOCS = [
  ('introduction', 'Introduction', 'What KATA UI is, how it is made, and where to go next.',
   [('A library you copy, not a dependency you rent', 'KATA UI is a catalog of interface parts — components, assembled blocks, and whole page templates — written in plain HTML, CSS and JavaScript. You take the code: by copy-paste from any part\u2019s page, or with the CLI. There is no framework to adopt, no build step to configure and no runtime to ship. After the copy, the code is yours; nothing updates itself and nothing phones home.', None, 'The catalog today: 96 parts, 13 blocks, 4 templates, 150 icons and 56 brand marks, 5 themes — every one free under MIT.'),
    ('Cast from a single mold', 'Every part is built to one written standard (the mold) and machine-checked against it before it ships: the same design tokens, the same spacing rhythm, the same states and focus rings, the same icon geometry. That sameness — not any single part — is the product. It is also why the parts compose: a Modal, a Command palette and a form built months apart sit together like they were made in one afternoon, because in the ways that show, they were.', None, 'The word kata is the Japanese discipline of the form: a pattern practiced until it disappears into the work.'),
    ('Three ways in', 'Copy-paste from the site is the front door — every part page shows its HTML, CSS and JS with a live preview. The CLI is the same catalog from a terminal. And because AI tools increasingly write the first draft, the whole catalog is published in machine-readable forms (registry.json, llms.txt, an installable Skill) so a model can fetch real parts instead of improvising lookalikes:', 'node kata-ui.mjs add sidebar calendar qr-code', 'Start at Getting Started for the three-step version, or open Components and take what you need.'),
    ('What it is not', 'Not a framework: there is no KATA way to fetch data, route pages or manage state — your stack keeps those jobs. Not a hosted service: the site is a catalog, not a platform. And not a React library: the parts are deliberately framework-free, which is what lets them drop into Astro, Laravel, Rails, Django, WordPress or a single HTML file unchanged.', None, None)]),
  ('getting-started', 'Getting Started', 'From zero to a working part in three steps.',
   [('Start with the tokens', 'Every part reads its color, spacing, radius and motion from one file. Load it once, before anything else:', '<link rel="stylesheet" href="https://kata-ui.dev/tokens.css">', 'That file is the mold. Parts never hard-code a color, so this one link is what makes the whole catalog look like one product.'),
    ('Copy a part', 'Open the part in Components and copy its three files: the HTML from the preview, the CSS, and the JS when it has one. Paste them into your project as they are. There is no install step and no package to keep updated — the code becomes yours, which is the point.', None, 'If the part says "Uses:" under its preview, it builds on another part (a Modal on Buttons, a Command palette on Kbd). Include that part\u2019s CSS too; the page names it.'),
    ('Works anywhere HTML does', 'Plain HTML files, Astro, Laravel Blade, Django and Rails templates, WordPress themes. If it renders HTML, KATA parts drop in unchanged — no framework island, no build plugin, no runtime.', None, 'For AI tools and installers, the whole catalog is also published as registry.json in the shadcn registry format, and as llms.txt for models that read the web.')]),
  ('cli', 'CLI', 'Install parts from your terminal instead of copy-pasting.',
   [('Get the CLI', 'The CLI is a single Node file with no dependencies (Node 18+). Download it once and keep it anywhere:', 'curl -fsSL https://kata-ui.dev/cli/kata-ui.mjs -o kata-ui.mjs\nnode kata-ui.mjs list', 'It reads the same registry.json this site publishes for AI tools — the CLI is a friendlier reader of the same catalog. An npm package is on the way; the single file is the whole thing either way.'),
    ('Add parts', 'init writes the design tokens. add writes a part — and everything it depends on — into ./kata by default:', 'node kata-ui.mjs init\nnode kata-ui.mjs add button select\nnode kata-ui.mjs add login', 'Blocks and templates install the same way: add dashboard writes the whole page. Theme presets too — add indigo writes the theme CSS. Pass --dir to choose another folder.'),
    ('Then load the files', 'Link tokens.css first, then the part CSS, and paste the HTML in as it is:', '<link rel="stylesheet" href="kata/tokens.css">\n<link rel="stylesheet" href="kata/components/button/button.css">', 'Nothing phones home and nothing updates itself afterwards: the files are yours, like a copy-paste that typed itself.')]),
  ('theming', 'Theming', 'Change the tokens, not the parts.',
   [('One surface', 'Parts reference only var(--k-…) tokens. To restyle everything, redefine tokens after tokens.css loads — never edit a part\u2019s CSS. An accent change is five lines:', ':root{ --k-accent:#4f46e5; --k-accent-ink:#4338ca; --k-accent-bg:rgba(79,70,229,.08); --k-accent-bg-strong:rgba(79,70,229,.1); --k-accent-line:rgba(79,70,229,.18); }', 'The Themes page ships five presets in exactly this form, each as a small CSS file you can download or copy.'),
    ('Shape and motion are tokens too', 'Radius (--k-radius, --k-radius-lg), durations (--k-dur-1…3) and the easing curve are tokens. Tighten the whole product by tightening the mold; loosen one part and it stops matching its siblings.', None, 'One token is off-limits by design: --k-core, the vermillion at the center of active controls. It is the signature, not a setting.')]),
  ('dark-mode', 'Dark Mode', 'One attribute flips every part.',
   [('The attribute', 'Put data-theme="dark" on the root element — or on any container — and every part inside flips. The tokens carry both themes; parts do not know which one they are in:', '<section data-theme="dark"> …parts… </section>', 'The Light/Dark toggle on every component page is this attribute, applied to the preview stage.'),
    ('What flips, what holds', 'Backgrounds, ink, lines, tracks and the accent ink (brighter in the dark) are theme tokens. The zinc scale underneath stays the same family, so a dark page still reads as the same product.', None, 'There is no automatic prefers-color-scheme switch built in: which theme a page wears is the page\u2019s decision. Setting the attribute from a media query in your own CSS is one line.')]),
  ('accessibility', 'Accessibility', 'What the parts guarantee, and what stays yours.',
   [('Native first', 'Where the platform has the element, the part is the element: dialog for Modal and Drawer, details for Accordion, real radio inputs for Segmented and Radio. Focus traps, Escape handling and screen-reader semantics come from the browser, not from scripts re-implementing them.', None, 'Interactive parts document their keyboard behavior on their own page, under Accessibility.'),
    ('Focus, motion, contrast', 'Focus rings are a token (--k-ring), visible in both themes, and never removed without a replacement. The Motion line and the Drawer honor prefers-reduced-motion. Text colors come from the zinc scale at weights chosen to stay readable on their backgrounds.', None, 'Parts are a starting point, not a certification: labels, heading order and the meaning of the page remain the page\u2019s responsibility. Test with a keyboard and a screen reader before shipping.')]),
  ('installation', 'Installation', 'Four ways in — from a single part to the whole set.',
   [('Copy a part — the default', 'Every part is three files at most: HTML, CSS, and JS when it needs behavior. Copy them from the part’s page into your project and they are yours — no dependency to update, no version to pin. Load the design tokens once, first:', '<link rel="stylesheet" href="https://kata-ui.dev/tokens.css">', 'Parts that build on other parts say "Uses:" on their page; include those parts’ CSS as well. That is the entire install for most pages.'),
    ('The one-file bundle', 'To evaluate everything at once, download the full bundle — every component and block, styles and behavior:', '<link rel="stylesheet" href="https://kata-ui.dev/kata-ui.css">\n<script src="https://kata-ui.dev/kata-ui.js"></script>', 'The CSS is the tokens plus all parts in catalog order. The JS runs each part in its own scope; parts whose markup is not on the page stay inert. When you settle on the parts you use, swap the bundle for their individual files and the page gets leaner.'),
    ('The starter kit', 'kata-starter.zip is a working first page — Card, Input, Switch, Button and Badge already composed — with the bundle beside it. Unzip, open index.html in a browser, and edit. No server, no build step:', 'https://kata-ui.dev/starter/kata-starter.zip', 'The README inside explains how to slim the starter down to per-part files when you are ready.'),
    ('For AI tools and installers', 'The catalog is published in machine-readable forms: registry.json in the shadcn registry format (every part and block with its files inline), llms.txt as a short index, and llms-full.txt with the full text and code.', 'https://kata-ui.dev/registry.json\nhttps://kata-ui.dev/llms.txt\nhttps://kata-ui.dev/llms-full.txt', 'Point your assistant at llms.txt and it can fetch the exact part it needs instead of inventing one.')]),
  ('install-html', 'Plain HTML', 'A static page is the simplest host there is: two links, then paste parts.',
   [('Link the bundle', 'The fastest way in is the hosted one-file bundle — every part’s CSS and JS, plus the tokens that make them one product:', '<link rel="stylesheet" href="https://kata-ui.dev/tokens.css">\n<link rel="stylesheet" href="https://kata-ui.dev/kata-ui.css">\n<script src="https://kata-ui.dev/kata-ui.js" defer></script>', 'Parts with behavior initialize themselves on load. Nothing to configure, nothing to build.'),
    ('Or take the starter', 'The starter kit is a working index.html with the tokens and a first set of parts already wired, ready to edit:', 'curl -O https://kata-ui.dev/starter/kata-starter.zip', 'Unzip it anywhere and open index.html. It is plain files all the way down — host it on any static host, or none.'),
    ('Then paste parts', 'Open any part in the catalog, copy its HTML, and paste it into your page. For production, swap the bundle for just the parts you use — each part page lists its own CSS and JS files, and the page stays as lean as what is on it.', None, 'Because the code is yours, there is no upgrade treadmill: a part you pasted last year keeps working exactly as it does today.')]),
  ('install-astro', 'Astro', 'Astro renders HTML and asks for nothing else. KATA parts paste into .astro files unchanged.',
   [('Fetch the parts with the CLI', 'Run the CLI into public/ so Astro serves the files as static assets:', 'curl -fsSL https://kata-ui.dev/cli/kata-ui.mjs -o kata-ui.mjs\nnode kata-ui.mjs init --dir public/kata\nnode kata-ui.mjs add button switch card --dir public/kata', 'init writes tokens.css; add writes each part’s CSS and JS next to it, dependencies included.'),
    ('Link them in your layout', 'In src/layouts/Layout.astro, load the tokens first, then the parts you use — once, for every page:', '<link rel="stylesheet" href="/kata/tokens.css">\n<link rel="stylesheet" href="/kata/button.css">\n<link rel="stylesheet" href="/kata/switch.css">', 'KATA CSS is global by design, which suits Astro: load it in the layout instead of a component’s scoped style block, and every page shares the same mold.'),
    ('Paste parts into pages', 'Copy a part’s HTML into any .astro file — frontmatter expressions work inside it like anywhere else. A part’s JS is a plain script: paste it into a script tag at the end of the page, or serve the file and reference it.', None, 'No island, no hydration, no client framework. The parts were never components in the framework sense; Astro’s HTML-first model is exactly the ground they were cast for.')]),
  ('install-laravel', 'Laravel', 'Blade templates are HTML with echoes — KATA parts drop in unchanged.',
   [('Fetch the parts with the CLI', 'Run the CLI into public/ so the files are served as static assets:', 'curl -fsSL https://kata-ui.dev/cli/kata-ui.mjs -o kata-ui.mjs\nnode kata-ui.mjs init --dir public/kata\nnode kata-ui.mjs add button switch data-table --dir public/kata', 'init writes tokens.css; add writes each part’s CSS and JS next to it, dependencies included.'),
    ('Link them in your layout Blade', 'In resources/views/layouts/app.blade.php, load the tokens first, then the parts — once, for every view:', '<link rel="stylesheet" href="{{ asset(\'kata/tokens.css\') }}">\n<link rel="stylesheet" href="{{ asset(\'kata/button.css\') }}">', 'Serve a part’s JS the same way, with the defer attribute, at the end of the layout.'),
    ('Paste parts into views', 'Copy a part’s HTML into any Blade view. Echoes and directives work inside the markup as usual — a @foreach over your models can stamp out cards, rows and list items from a single pasted part.', None, 'If the project builds front-end assets with Vite instead, the same files can live under resources/ and be imported unchanged; they are plain CSS and JS either way.')]),
  ('javascript', 'JavaScript', 'What the scripts do — and what still works without them.',
   [('Plain scripts, data hooks', 'A part’s JS is a single plain script: no imports, no framework, no build. It finds its root by a data attribute (data-dp, data-combo, data-tags…) and keeps its state in the DOM — classes and ARIA attributes you can inspect. Copy it next to the HTML and it runs.', None, 'In the one-file bundle each script is wrapped in its own function scope, so parts never collide with each other or with your code.'),
    ('What works with no JavaScript', 'More than you might expect. Accordion is native details. Rating and Segmented are radio inputs. Switch and Checkbox are checkboxes. Marquee, Aurora, Beam Border and the charts are CSS and SVG. These parts are complete with the script tag deleted.', None, 'Parts that do need JS say so by having a JS tab — and the honest ones degrade: Tag Input falls back to a plain text field, Combobox to a text input, the Date Picker to a text input.'),
    ('Behavior contracts', 'Interactive parts document their keyboard behavior on their own page, under Accessibility. The shared rules: Escape closes what is open and returns focus, arrows move within a part, and nothing ever traps the pointer. Motion parts check prefers-reduced-motion once and honor it.', None, 'If a part’s script fails to load, the page still renders — behavior is layered on markup, never generated by it (the Date Picker calendar grid is the one exception, and it is labelled as such).')]),
  ('guide-dashboard', 'Guide: Building a Dashboard', 'The parts, in the order a reader’s eyes take them.',
   [('Start with the frame', 'A dashboard is the App Shell block and then restraint. Sidebar navigation, a top bar, and a content column — the shell is already composed from the catalog’s own parts, so the page inherits the mold for free. Resist adding a second navigation pattern inside the content; one way to move is a feature.', None, 'Below 720px the shell hides its sidebar. Whatever your page adds must survive that: if a control only exists in the sidebar, it needs a second home.'),
    ('Numbers before charts', 'The first row is Stat Cards — three or four numbers with deltas, because most visits answer one question: is it up or down? Charts come second, and one chart per question. The Line Chart shows change, the Donut shows share, the Bar Chart compares. A dashboard with six charts answers nothing; it performs analysis instead of providing it.', None, 'Every chart in the catalog states its conclusion in its accessible label. Keep that habit in your own charts: the sentence first, the picture second.'),
    ('Tables carry the work', 'Below the fold, a Data Table with sortable columns and row selection does the actual job of the page. Keep rows to the fields people compare, put the row’s main action first, and let the footer paginate honestly. If a table needs fourteen columns, the answer is a detail page, not a wider table.', None, None)]),
  ('guide-settings', 'Guide: Building a Settings Page', 'Grouped switches, honest saves, and no settings that do nothing.',
   [('Group by consequence', 'Order groups by how much damage a wrong toggle does: profile, notifications, billing, danger. The Settings block ships this shape — a rail of groups on the left, forms on the right, and the destructive group last, in red, far from the save button it does not belong to.', None, 'A setting that takes effect immediately gets a Switch. A setting that needs a save gets inputs and a button. Mixing the two in one group teaches users that saving is optional, and they will believe you at the worst moment.'),
    ('The save contract', 'If the page has a Save button, it saves everything on the page or it says exactly what it did not save. Show the saved state — a Toast, a timestamp, a disabled button that wakes on the next edit. Never let a user wonder whether the click landed.', None, 'Validation belongs to the Field part: label, hint, error, in that order, with the error replacing the hint rather than pushing the layout down the page.'),
    ('Danger gets its own room', 'Delete-account, revoke-keys, cancel-plan: these live in their own group, behind an Alert Dialog that names the consequence in the button itself — “Delete workspace”, not “Yes”. The dialog is not friction; it is the feature.', None, None)]),
  ('guide-pricing', 'Guide: Building a Pricing Page', 'Three plans, one switch, and prices that survive the toggle.',
   [('The toggle is a Switch', 'Monthly/yearly is the Pricing block’s own composition: a Switch flips data attributes on the prices, so the numbers in the page are the numbers that were checked. Never compute prices in the browser from a formula nobody audited — write both prices down, in the markup, where a reviewer can diff them.', None, 'Yearly shows the monthly-equivalent price with the saving stated once, plainly. “Save 17%” is a claim; make sure it is arithmetically true on every plan, including the free one.'),
    ('One plan is the answer', 'Three plans, the middle one marked — not because it is the most profitable, but because it is the right default for the reader the page is for. The block’s .plan-hot and its badge exist for exactly one plan. Two highlighted plans is a page that refuses to recommend, and readers can tell.', None, 'Feature lists compare downward: every plan lists what it adds over the one before. A grid of forty checkmarks and crosses is a spreadsheet wearing a costume.'),
    ('Under the plans', 'The FAQ block answers the five questions pricing always raises — switching, refunds, seats, taxes, cancellation — and after it, one CTA Band. A pricing page that ends at the table assumes the reader decided; most have not, and the questions are the decision.', None, None)]),
  ('guide-auth', 'Guide: Sign-in & Account Pages', 'The smallest pages in the product, held to the highest standard.',
   [('One card, one job', 'The Login block is a Card with two fields and one primary button, and that is the whole page’s ambition. Every element added to a sign-in page — a banner, a testimonial, a “what’s new” — is measured against the only metric that matters here: does the person get in?', None, 'Errors on auth pages are written for someone who is already frustrated: say what failed and what to try, never which half of the credential was wrong. “Email or password did not match” is both kinder and safer.'),
    ('Password rules, stated before typing', 'If the account-creation form rejects passwords, the rules sit in the Field hint before the first keystroke, not in an error after the third attempt. Length is the rule that matters; composition rules mostly manufacture Post-it notes.', None, 'Offer the platform’s help: autocomplete attributes (email, current-password, new-password, one-time-code) and the Input OTP part for codes. The browser and the password manager are part of your interface whether you design for them or not.'),
    ('After the door', 'Sign-in succeeds into the App Shell, not into a celebration. If the session was heading somewhere — a deep link, an invite — it lands there. The welcome-back toast is the most that should mark the occasion.', None, None)]),
  ('why-vanilla', 'Why Vanilla', 'An honest account of what copy-paste gives you, and what it costs.',
   [('What you get', 'No runtime. A KATA page ships the HTML, CSS and JS you can read in the tab next to this one — nothing transpiles, nothing hydrates, and the dependency list is empty, so there is nothing to audit, patch or be broken by. The code is yours in the plainest sense: fork a part, rename its classes, delete the half you do not need. It will still be running, unchanged, in ten years, because nothing underneath it can be deprecated.', None, 'This is also why AI tools are good at KATA: a part is a complete, self-contained answer in one context window. The registry and llms.txt exist so the model copies the mold instead of improvising one.'),
    ('What it costs', 'No components in the framework sense: no props, no reactivity, no tree-shaking. State that spans many parts — a cart, a multi-step wizard with shared data — is yours to wire, and past a certain size a framework earns its keep. KATA’s bet is that most pages are not that size: they are forms, tables, dashboards and marketing sections, and for those the framework was never the point.', None, 'The honest line: if your app is a document with behavior, vanilla wins. If it is a program with a document attached, use the framework — and KATA’s tokens and CSS still drop into it unchanged.'),
    ('Why copy-paste, not a package', 'A package makes the library’s roadmap your roadmap: upgrades, breaking changes, abandonment. Copied code has no roadmap. shadcn proved the model for React; the trade is the same in vanilla — you own the code, including its bugs, and in exchange nobody can take it away, sunset it, or put it behind a pricing page.', None, None)]),
  ('the-mold', 'The Mold', 'How every part is made, and the checks it has to pass before it exists.',
   [('One mold', 'Kata — 型 — is the Japanese discipline of the form: the pattern from which things are cast, and the practice that keeps the casting true. Every KATA part is built to one production standard: same file layout, same tokens, same class grammar, same accessibility contract. The consistency is not a style guide people try to remember; it is a checklist a program enforces.', None, 'Two parts built months apart should look like they were built on the same day, by the same hand. The mold is how a library with one author keeps that promise.'),
    ('The checks', 'Before a part ships, a checker reads its files the way a casting inspector reads a mold. Required files present. Metadata complete. No raw color anywhere — tokens only, because a hard-coded hex is a part that will not survive a theme. Every class used in the preview actually defined. Icons drawn on the 24-grid at stroke 2, from three shapes: circle, 45-degree line, rounded corner. A part that fails does not ship; the count on the homepage only ever counts parts that passed.', None, 'The checker is in the repository (check.py) and the standard is written down (KATA.md), so the mold is inspectable, not vibes.'),
    ('The signature', 'One color is reserved: a vermillion core, #EB471F, that appears only at the center of active controls — the dot inside a checked radio, the core of an on switch, the end point of a line chart, and one quarter of the logo itself. Never on a surface, never as text, never changed by a theme. It is how you can tell a KATA part at a glance, and how the parts tell you where the action is.', None, None)]),
  ('anatomy', 'Anatomy of a Part', 'What is inside every folder in the catalog.',
   [('The files', 'A part is a folder: preview.html (the markup, exactly as you copy it), the part’s CSS, a JS file when the part behaves, and meta.json. Examples, when a part has them, live in examples.html and render on the part’s page under the preview. What you see on the site is not a rendering of the part — it is the part, loaded live.', 'components/button/\n  preview.html   the markup\n  button.css     the styles\n  button.js      the behavior (when any)\n  examples.html  variations (when any)\n  meta.json      title, category, usage, accessibility', 'Blocks are folders too, with one addition: meta.json names the parts they use, and their previews load those parts’ CSS — a block is a composition, never a re-implementation.'),
    ('The contract', 'Every part reads color, spacing, radius and motion from the tokens and nothing else. Classes follow one grammar. Interactive parts state their keyboard behavior and their no-JavaScript fallback in their metadata, and the part’s page prints both. If two parts disagree about anything, that is a bug in one of them, and the mold decides which.', None, 'Status is printed on every part: stable means the contract is settled; beta means the shape is right but the edges are still being filed. The catalog counts both, and labels both.')]),
  ('from-tailwind', 'Coming from Tailwind', 'For the largest group of visitors: what changes, what does not.',
   [('The mental shift', 'Tailwind puts the design system in your class attributes; KATA puts it in tokens and part CSS. You will write longer stylesheets and shorter markup. A card stops being eleven utilities and becomes .k-card — which means the design can be retuned in one place, and the HTML reads as structure instead of as styling.', None, 'They coexist fine: Tailwind for layout glue in a page, KATA parts for the components. The tokens are plain CSS variables, so a Tailwind config can point at the same values and the two systems stop arguing.'),
    ('Rough translations', 'A few mappings to start: bg-zinc-900 text-white becomes a part on a dark section (data-theme="dark" does the whole subtree). rounded-xl is --k-radius-lg. The accent button is .btn-pri or .btn-teal, not a recipe of bg-, hover: and focus: classes — hover and focus are in the part, tested once, everywhere. Arbitrary values like w-[340px] stay inline styles in KATA too; the mold is strict about color, relaxed about one-off geometry.', None, 'What you give up: the utility for the one weird case, answered inline. What you get back: a page whose markup a new hire (or a model) can read at a glance, and parts that look related because they are.')]),
  ('vs-shadcn', 'KATA vs shadcn/ui', 'The honest comparison, written by the side with more to gain from flattery.',
   [('The short version', 'shadcn/ui and KATA start from the same conviction: you should own the code — copy it into your project, change it, never rent it back from a package. shadcn casts that idea for React. KATA casts it for everywhere else HTML renders: plain files, Astro, Laravel, Django, Rails, WordPress, email templates, the admin page nobody frameworks. If your product is a React app, shadcn is excellent and this page will tell you so twice. If your stack is anything else, the React door is simply not your door.', None, None),
    ('Where shadcn wins', 'The React ecosystem, first: thousands of projects, snippets, and answers already exist, and a team hiring React developers hires people who know it. Its primitives stand on Radix, whose accessibility engineering — focus management, aria patterns, edge cases in dialogs and menus — is deep and battle-tested. It is TypeScript-first in a way KATA, being plain files, does not try to be. And its design language is the current default for a reason: it is tasteful, consistent, and safe to choose in a meeting.', None, None),
    ('Where KATA wins', 'Adoption cost outside React: a KATA part is three files and no toolchain, so it lands in a ten-year-old Laravel app as easily as in a fresh Astro site. Range: the catalog carries shelves shadcn does not — a Motion line, the KATAYABURI shelf of deliberate showpieces, a Japan genre (wagara patterns constructed from their geometry, a hanko seal, a kintsugi card), charts, and 150 icons cut to one spec. Composed work: blocks and templates are first-class citizens here, not community links. And the machine surface: registry.json, an MCP server, and an installable AI Skill are published by the catalog itself, so an assistant asked for a sidebar installs this Sidebar instead of improvising one.', None, None),
    ('The honest summary', 'Framework: React and Tailwind, versus none at all. Runtime: React, versus nothing. Distribution: a CLI and registry, versus copy-paste, a CLI and a registry. License: MIT, versus MIT for every part (blocks and templates are the paid line here). Community: enormous, versus one maker and a mold. Neither list is an embarrassment — they are answers to different questions. Choose by the stack you actually ship, not by the loudest timeline.', None, 'A fair number of teams will run both: shadcn inside the product, KATA on the marketing site, the docs, and the pages that were never going to be React.')]),
  ('site-faq', 'FAQ', 'About the library itself — licensing, the Pro line, and what is not planned.',
   [('Licensing and Pro', 'Every component and icon in this catalog is MIT-licensed: copy it, ship it, sell what you build with it. Blocks and full templates are the commercial line — sold once, lifetime, no subscription — because composed screens are where the hours actually go. The parts will never move behind the paywall retroactively; a part that is free is free in every future version.', None, None),
    ('Is there a React version?', 'Not today. The parts paste into any stack that renders HTML, including inside React as plain markup for static sections. A native React port, in the shadcn registry format, is the most-requested item on the list and is being considered honestly — the registry file already published is the first step, since it describes every part in that format.', None, None),
    ('Why no npm package?', 'Because the package would become the product, and the product is the code in your repo. The one-file bundle and the starter kit cover the “just give me everything” case without a dependency. If a package ever ships, it will be a mirror of these files, never the source of truth.', None, None),
    ('Who makes this?', 'One person, in the open, with the mold as the second pair of hands. The repository holds the parts, the checker, and the standard they are built to — issues and corrections are welcome there.', None, None)]),
  ('registry', 'Registry', 'The whole catalog as one machine-readable file — what reads it, and how to mirror it.',
   [('One file, the whole catalog', 'registry.json, served at /registry.json, describes every part, block, template and theme in the shadcn registry format: its name, its type, its dependencies, and the complete contents of its files. Anything that can read JSON can install KATA UI — the file is the API.', None, 'It is regenerated on every build from the same sources as this site, so it can never drift from the pages you are reading.'),
    ('An item, up close', 'A trimmed excerpt of one entry. The files carry their full contents (the CSS below is shortened here for print); dependencies name other registry items the installer must bring along:', '{\n  "name": "sidebar",\n  "type": "registry:component",\n  "title": "Sidebar",\n  "dependencies": [],\n  "files": [\n    { "path": "components/sidebar/sidebar.css", "type": "registry:component", "content": "/* KATA Sidebar … */" },\n    { "path": "components/sidebar/sidebar.js", "type": "registry:component", "content": "// KATA Sidebar …" }\n  ]\n}', 'Types are registry:component for parts, registry:block for blocks, registry:page for templates and registry:theme for themes.'),
    ('Who reads it', 'Three readers ship today. The CLI (node kata-ui.mjs add …) resolves dependencies and writes files into your project. The AI Skill teaches coding models the catalog\u2019s shape, so an assistant asked for "a sidebar" installs this Sidebar instead of inventing one. And your own scripts are welcome to it — a generator, a company-internal installer, an audit that diffs the catalog against your codebase.', None, 'For language models that read prose rather than JSON, llms.txt and llms-full.txt mirror the same catalog as text.'),
    ('Mirror it', 'The registry is a static file and the parts inside it are complete, so a mirror works offline and forever: download /registry.json once, serve it anywhere, and point the CLI at it:', 'KATA_BASE=https://your-mirror.example node kata-ui.mjs add button', 'Pinning a mirror is also how a team freezes a catalog version while the public one moves on.')]),
  ('forms', 'Forms', 'How forms compose in KATA: the field wrapper, honest errors, and which part takes which job.',
   [('The shape of a field', 'Every control wears the same wrapper — the Field part: a label above, the control, then a hint or an error below, in that order, always. The wrapper is what makes a column of different controls read as one form:', '<div class="field" data-field>\n  <label for="email">Email</label>\n  <input class="input" id="email" type="email" autocomplete="email">\n  <p class="hint">The receipt goes here.</p>\n</div>', 'Labels are text, never placeholders doing double duty: a placeholder disappears exactly when the reader needs it most.'),
    ('Errors that say something', 'An error replaces the hint, in the danger color and in words: what is wrong and how to fix it ("Enter the address the receipt should go to", not "Invalid"). Three wirings make it real rather than decorative: the control carries aria-invalid="true"; the error paragraph has an id the control names in aria-describedby; and on submit, focus moves to a summary at the top listing the problems, each linked to its field.', '<div class="field" data-field>\n  <label for="email">Email</label>\n  <input class="input errb" id="email" type="email" aria-invalid="true" aria-describedby="email-err">\n  <p class="err" id="email-err">Enter the address the receipt should go to.</p>\n</div>', 'Never let color be the only signal: the words carry the error for everyone, the red just helps find them.'),
    ('Grouping and choosing', 'Choices that belong together get a fieldset with a legend — the Radio and Checkbox groups are built that way — because "how did you hear about us" is the label for the whole set, not for any one option. Which control takes the job: one short line is an Input, a paragraph is a Textarea, one of two-to-five visible options is Radio or Segmented, one of many is a Select or a Combobox, a date is a Date Picker, a time is a Time Picker, several values are a Tag Input, a path down a tree is a Cascader, and assigning many things at once is a Transfer.', None, 'Attached pieces stay attached: money gets an Input Group (the ¥ is part of the control, not a caption), and the form\u2019s actions are a right-aligned row of Buttons — the primary one once, at the end.'),
    ('Required, honestly', 'Mark required fields in the label text ("Email (required)") or mark the optional ones — pick one convention per form and keep it. Star-only marking fails everyone who cannot see the star\u2019s legend, and there is always a legend nobody reads.', None, None)]),
  ('mcp', 'MCP Server', 'The catalog as an MCP server, so AI tools can browse and fetch real parts.',
   [('Why an MCP server', 'Models improvise interfaces when they cannot see real ones. The MCP server gives a connected AI tool the actual catalog — it can list what exists, search it, and fetch a part\u2019s real files (HTML, CSS, JS) with its dependencies, then write them into your project as they are. It is the registry, served over the Model Context Protocol, from one zero-dependency Node file.', None, None),
    ('Connect it', 'Download the server once, then point your MCP client at it. The configuration most clients accept:', 'curl -fsSL https://kata-ui.dev/mcp/kata-ui-mcp.mjs -o kata-ui-mcp.mjs', '{\n  "mcpServers": {\n    "kata-ui": {\n      "command": "node",\n      "args": ["/path/to/kata-ui-mcp.mjs"]\n    }\n  }\n}'),
    ('The tools', 'Three, deliberately. list_components returns the catalog (optionally one type: parts, blocks, templates, themes). search_components finds candidates by name, title and description. get_component returns one item complete — every file\u2019s full contents and the dependencies to bring along — which is the difference between a model describing a sidebar and installing this one.', None, 'The server is read-only: it serves the catalog and writes nothing, anywhere.'),
    ('Point it elsewhere', 'By default the server reads https://kata-ui.dev/registry.json at first use. Set KATA_BASE to a mirror, or pass --registry with a local file path, to serve a pinned or offline copy — the same mirror story as the CLI:', 'node kata-ui-mcp.mjs --registry ./registry.json', None)]),
  ('rtl', 'RTL', 'Right-to-left is a direction, not a stylesheet: set dir and the catalog follows.',
   [('One attribute', 'There is no RTL build, no .rtl variant and nothing to download twice. Write direction into the document and the same files lay out right-to-left:', '<html lang="ar" dir="rtl">', 'It works on any container, too — dir="rtl" on a section flips that section only, which is how mixed-direction pages are usually built.'),
    ('What mirrors', 'The site chrome and the structural parts are written with logical properties — inline-start and inline-end instead of left and right — so sidebars trade sides, menus open from their other edge, panels anchor to the new start, form groups and button seams join in the new direction, and breadcrumbs, pagination and navigation follow. Flex and grid layouts follow direction on their own; the Switch knob, which moves on a physical track, carries an explicit flip rule.', None, 'Text alignment follows too: start-aligned in LTR is start-aligned in RTL, and numeric columns align to the end in both.'),
    ('What deliberately does not', 'The showpieces keyed to physical coordinates stay physical: the Spotlight beam follows a cursor, the Comparison seam divides a picture, the Aurora washes drift where they drift, and the Drawer slides from the side it was built for. Direction is about reading order, not about re-choreographing effects. Directional icons — arrows, chevrons, the little plane on a send button — are glyphs, and flipping a glyph is a design decision left to the page.', None, 'The vermillion core sits at the center of active controls. Centers have no direction, so the signature survives the flip untouched.')]),
  ('changelog', 'Changelog', 'What shipped, newest first.',
   [('November 2, 2026 \u2014 Type, templated', '<p>Letter-spacing and line-height are fixed values now, not taste: a tracking table lives in the mold (KATA.md \u00a70.5), as --k-ls-* and --k-lh-* tokens, and on the Design System page. Body text takes +0.012em, CJK display +0.06em, CJK never goes negative, and kana readings wrap as whole words. The table exists because the traditional-colors section shipped with body tracking at zero \u2014 the kind of basic a mold is supposed to make impossible to forget. Applied site-wide the same day: every page lead, the docs body, the landing sub-texts and the Japanese page (CJK body +0.04em, headings +0.05em) now follow the table, and an audit of all 164 part stylesheets found their tracking already sitting inside the ramps \u2014 card titles, micro labels, vertical text \u2014 that the table now records explicitly.</p>', None, None),
    ('November 2, 2026 \u2014 Traditional colors of Japan', '<p>The Themes page gains \u4f1d\u7d71\u8272: fifty traditional Japanese colors in seven families \u2014 pine-soot inks, safflower reds, indigo blues, gardenia yellows \u2014 each with its kanji name, its reading and the dye or pigment it came from. Clicking one casts it into the live demo and writes the theme CSS under its own name (ai.css, yamabuki.css), so a button can wear a thousand-year-old color in one click. At the head of the reds sits \u578b\u306e\u6731, KATA\u2019s own vermilion core, labeled as what it is: the one color no theme moves.</p>', None, None),
    ('November 2, 2026 — The zoom pass', '<p>Every one of the 201 pages and all 136 part previews was re-examined at full phone size. The pass caught and fixed a collapsed Accordion Gallery and Speed Dial stage, a Hover Card whose markup invalidly nested blocks inside a paragraph, clipped Radar Chart labels, a nearly invisible Skeleton, label collisions in Steps and List, tables that broke out of their stages, and readouts that shrank instead of stretching. The landing page Questions section now answers questions about this library instead of a generic SaaS. Nothing new was added; everything already here simply holds up better under a magnifying glass.</p>', None, None),
 ('November 2, 2026 — Ten patterns on the loom', 'The Wagara instrument grows from four patterns to ten, each still drawn from its construction: Kikko (nested tortoiseshell hexagons), Uroko (the triangle scale tiling), Samekomon (dots riding the scale arcs, sharkskin-fine), Yagasuri (the arrow-feather silhouette), Kanoko (staggered shibori fawn-spots) and Hishi (the diamond lattice, studded at its crossings). Same three tones, same tokens — the loom is bigger, the discipline is not.', None, None),
    ('November 2, 2026 — Retina, at last', 'A bug report from a phone: the canvas parts were drawing at 1x and being stretched on retina screens — the shippo circles gave it away, soft where they should be cut. All nine canvas parts (Wagara, Kintsugi Card, Particle Net, Particle Word, Fireworks, Kata Rain, Kaleidoscope, Confetti Cannon, Burst Button) now back their canvases at device pixel ratio, up to 3x, and draw through the transform in CSS pixels as before. Same pictures, drawn at the resolution your screen actually has.', None, None),
    ('November 2, 2026 — v1.0.0', 'The catalog gets a version number and a front door for the sale to come. v1.0.0 is now stamped where machines look: registry.json carries it, the CLI answers --version with it, and the MCP server already spoke it. The pricing page and the landing page both take waitlist emails for the Pro launch — one email on the day, promised in writing next to the form. Three new pages: an honest KATA vs shadcn/ui comparison in the docs (it recommends shadcn twice, for React teams), a Showcase that assembles the evidence — every template is a live page built from the parts it lists — and a Japanese landing at /ja/, one page, for the home market. The README finally counts what is actually in the catalog: 136 parts in eight categories, 21 blocks, 7 templates.', None, None),
    ('November 2, 2026 — Japan, a genre', 'A new eighth category: Japan — built with patience, not souvenir. Wagara constructs four classical patterns from their real geometry (seigaiha\u2019s half-offset arcs, asanoha\u2019s six-fold hemp, shippo\u2019s equal circles, ichimatsu with the nested mini-checker the mark wears) and plays them in three house tones; Hanko is a vermillion seal that stamps itself on arrival and again on click; the Kintsugi Card reports an incident honestly, its cracks gilded and re-drawn on arrival; Noren hangs a three-panel curtain as a section divider that sways and parts on hover; and Tategaki sets vertical text properly — shuhari, obey the form, break the form, leave the form, the discipline this whole library runs on. The landing hero was re-dressed in the same pass: compact eyebrow, a brighter second line, stats four-across, and a ghost button that survives its gradient. The catalog stands at 136 parts.', None, None),
    ('November 2, 2026 — Effects, on duty', 'Six effect parts, all of them working parts first: a Burst Button that answers clicks with sparks, a Liquid Button that pours on hover, Goo Tabs whose indicator travels like liquid over real tab panels, a Glow Button in a rotating ring of light (with the same ring as a search-field treatment), a Particle Net quiet enough to carry a hero, and a Torn Ticket with mask-cut perforations and a stub that keeps the code. The catalog stands at 131 parts.', None, None),
    ('November 2, 2026 — Back to work', 'A practical round, on request: the toys stay on their shelf and this one is all tools. A Dual Range slider for price filters; four working blocks — Invoice, Order Confirmation, Filter Toolbar and a Cookie Consent with no dark patterns; and two full templates, a Product Page (gallery, options, accordions) and a Blog Article (prose rhythm, contents rail, author card). The catalog stands at 125 parts, 21 blocks and 7 templates.', None, None),
    ('November 2, 2026 — More weather, and the Pro line grows teeth', 'Seven more parts: KATAYABURI gains Fireworks (click the sky), Newton\u2019s Cradle in pure CSS, a 3D Carousel Ring and Bounce Letters; Motion gains Stacking Cards, an Accordion Gallery and a Horizontal Reel. Blocks and templates — the Pro line — now wear a Pro pill on their cards and pages, and the line itself grew: Team Grid, Roadmap and Plan Compare blocks, and a full Checkout template composing steps, forms and a sticky summary. The catalog stands at 124 parts, 17 blocks and 5 templates.', None, None),
    ('November 2, 2026 — KATAYABURI', 'Every mold deserves a shelf where it is broken on purpose. KATAYABURI (型破り, "breaking the form") is a new seventh category: eight parts with no business case — a word made of a thousand spring-loaded particles, katakana rain, a confetti cannon in the token palette, the catalog itself dropped under gravity, a kaleidoscope that draws alone until you take the pen, a goo cursor with surface tension, a warp tunnel in pure CSS, and jelly buttons. The joke the shelf is built on: every rebel still passes the mold — tokens, class coverage, reduced-motion manners and all. The catalog stands at 117 parts.', None, None),
    ('November 2, 2026 — Weather, gravity, light', 'The Motion shelf more than doubled, ten parts to twenty-three. New weather: Meteors seeding a night sky, Sparkles twinkling in the container\u2019s own color. New gravity: a macOS-style Dock whose tiles swell by proximity, and Magnet, a button that leans a third of the way toward the cursor. New light: Glow Cards whose borders warm where the pointer passes, a Tilt Card with a real floating layer, Shine Text, and a Tracing Beam that fills the rail as you read. New voices: Typewriter, Scramble decoding itself, Word Rotate stepping its stack, Blur In sharpening word by word, and Orbit — two rings, two speeds, every glyph upright. Every one honors prefers-reduced-motion, and the showpieces were verified in motion, in screenshots, mid-flight.', None, None),
    ('November 2, 2026 — The machine room', 'The docs grew the pages that explain the machinery: Introduction, Registry, Forms, MCP Server and RTL (24 doc pages in all). The MCP server ships as a single zero-dependency file at /mcp/kata-ui-mcp.mjs — list, search and get, read-only, straight from the registry. A Pricing page states the line in public: parts free forever, Pro is blocks and templates at $129 once, not yet on sale. Blocks are grouped by kind (Page chrome / Marketing / Product) and gained a Kanban board whose cards really drag. And the catalog learned direction: chrome and structural parts now use logical properties throughout, so dir="rtl" mirrors them — verified part by part, with the physical showpieces honestly exempted.', None, None),
    ('November 2, 2026 — The missing sixteen', 'A second gap hunt — the current catalogs of six libraries against our own, example by example — found sixteen genres the mold had never cast. All sixteen are parts now: Button Group and Input Group (the seams were missing even as examples), Collapsible, Descriptions, Result, Bottom Navigation, Calendar (freed from inside the Date Picker), Comparison Slider, Speed Dial, Scrollspy, Navigation Menu, Menubar, Time Picker, Cascader, Transfer — and a QR Code whose encoder is written from the spec, zero-dependency, and verified module-for-module against a reference implementation across versions 1–6. The catalog stands at 96 parts.', None, None),
    ('November 2, 2026 — Structure, and the furniture', 'Every part, block and template page now opens with an Installation section (CLI or manual) and closes with an Anatomy table read from the part\u2019s own source. New part: Sidebar, with sections, collapsible groups and an icon rail. Spotlight was rebuilt as a flashlight — a dark panel, a resting beam, and words that light only where the beam reaches. The site itself grew its furniture: a full favicon set and PWA icons drawn from the new mark, a web manifest and service worker (documents network-first, so deploys are never stale), Open Graph and Twitter cards on every page with a proper social image, and canonical URLs throughout. The comparison table now says what is true: distribution is copy-paste, CLI & registry.', None, None),
    ('November 2, 2026 — A sharper cut, a new mark', 'The icon set was re-cut on the user’s call: a 1.7 stroke, square caps and bevel joins replace the round 2px line, in all 150 glyphs and every inline copy. The logo changed too — the framed mold mark gave way to a frameless four-part square with a small ichimatsu checker nested in its top-right quarter, a mold inside the mold. New part: Typeset, long-form text as one cast piece. Every chart part gained Examples (two-series lines, a six-axis radar, four-segment donuts and more), the Themes page learned to build a custom theme from any color, and the docs grew per-stack install guides for Plain HTML, Astro and Laravel.', None, None),
   ('November 2, 2026 — CLI, brand marks, wagara', 'The catalog is installable from a terminal now: a zero-dependency Node CLI (node kata-ui.mjs add button) reads registry.json and writes parts, blocks, templates and themes — dependencies included — into your project. Brand marks grew from 12 to 56, grouped by job (social, AI, development, commerce, platforms, cloud) on the Icons page, and the Integrations block grew to 18 tiles. Aurora learned three wagara textures — Seigaiha, Asanoha and Ichimatsu — as drifting line patterns under the wash, in its Examples. The site menu is labeled Menu and lists blocks, templates and docs next to the components.', None, None),
    ('November 2, 2026 — Templates arrive', 'The catalog grows a third shelf: Templates — whole pages composed from parts and blocks, starting with a Dashboard page (sidebar, stat row, revenue chart, sortable orders table). The site navigation, search and registry now carry templates as first-class items (registry:page), and the landing page counts five genres.', None, None),
   ('November 2, 2026 — The catalog fills in', 'Seventy-six components and thirteen blocks. New: Date Picker, Combobox, File Upload, Tag Input, Context Menu, Tree, Data Table, Color Picker, Split Panel, Scroll Area, Aspect Ratio, Toggle, and the Scatter, Radar and Funnel charts plus Sparkline. Blocks gained FAQ, Site Header, Site Footer, Testimonials, CTA Band and Logo Cloud. Installation becomes a real thing: the one-file bundle (kata-ui.css / kata-ui.js), the starter kit, and an Installation doc. The landing page now assembles its showcase from live parts, and the mobile overflow bugs reported on day one are fixed.', None, None),
    ('November 1, 2026 — Launch', 'KATA UI opens with 46 components in six groups, 5 blocks, 150 icons and 12 brand marks, the design-system tokens with light and dark themes, five accent themes, and the AI distribution files (registry.json, llms.txt). Every part is checked against the mold before it ships: required files, token-only colors, class coverage, icon geometry.', None, None)]),

]

DOC_STYLE = """<style>
.dc h1{font-size:32px;font-weight:600;letter-spacing:-.025em;margin-top:26px}
.dc .lead{margin-top:10px;color:var(--ink2);font-size:15px;line-height:1.85;max-width:64ch;letter-spacing:.012em}
.dc section{margin-top:36px;max-width:68ch}
.dc h2{font-size:18px;font-weight:600;letter-spacing:-.015em}
.dc p{margin-top:9px;font-size:14px;line-height:1.9;color:var(--ink2);letter-spacing:.012em}
.dc pre{margin-top:12px;border:1px solid var(--hair);border-radius:10px;background:var(--soft);padding:13px 15px;font-family:var(--mono);font-size:12px;line-height:1.75;overflow:auto;color:var(--ink)}
.dcgrid{margin-top:24px;display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px}
.dccard{border:1px solid var(--hair);border-radius:12px;background:#fff;padding:17px;text-decoration:none;color:var(--ink);display:block}
.dccard:hover{border-color:var(--ink3)}
.dccard h3{font-size:15px;font-weight:600}
.dccard p{margin-top:6px;font-size:13px;color:var(--ink2);line-height:1.7}
</style>"""

def docs_index():
    cards = ''.join(f'<a class="dccard" href="/docs/{s}/"><h3>{esc(t)}</h3><p>{esc(d)}</p></a>' for s, t, d, _ in DOCS)
    body = f"""
<div class="wrap dc">
  <h1>Docs</h1>
  <p class="lead">The short version of everything: how to start, how to theme, how dark mode works, and what the parts promise about accessibility. The long version lives on each part's own page.</p>
  <div class="dcgrid">{cards}</div>
</div>
{FOOTER}
</body>
</html>"""
    return head('Docs — KATA UI', 'Getting started, theming, dark mode and accessibility for KATA UI.', DOC_STYLE) + body

def doc_page(slug):
    entry = next(d for d in DOCS if d[0] == slug)
    _, title, desc, sections = entry
    secs = []
    for h, p1, code, p2 in sections:
        chunk = f'<section><h2>{esc(h)}</h2><p>{esc(p1)}</p>'
        if code:
            chunk += f'<pre>{esc(code)}</pre>'
        if p2:
            chunk += f'<p>{esc(p2)}</p>'
        secs.append(chunk + '</section>')
    others = ' · '.join(f'<a href="/docs/{s}/">{esc(t)}</a>' for s, t, _, _ in DOCS if s != slug)
    body = f"""
<div class="wrap dc">
  <p class="crumb" style="margin-top:22px"><a href="/docs/">Docs</a> / {esc(title)}</p>
  <h1>{esc(title)}</h1>
  <p class="lead">{esc(desc)}</p>
  {''.join(secs)}
  <section><h2>More docs</h2><p>{others}</p></section>
</div>
{FOOTER}
</body>
</html>"""
    return head(f'{title} — Docs — KATA UI', desc, DOC_STYLE) + body


def main():
    comps = load_components()
    blocks = load_blocks()
    templates = load_templates()
    n_icons = len(list((ROOT / 'icons').glob('*.svg')))
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    _cl = ROOT / 'cli'
    if _cl.exists():
        (DIST / 'cli').mkdir(exist_ok=True)
        for _f in _cl.iterdir():
            if _f.is_file():
                shutil.copy(_f, DIST / 'cli' / _f.name)
    _mc = ROOT / 'mcp'
    if _mc.exists():
        (DIST / 'mcp').mkdir(exist_ok=True)
        for _f in _mc.iterdir():
            if _f.is_file():
                shutil.copy(_f, DIST / 'mcp' / _f.name)
    shutil.copy(ROOT / 'tokens.css', DIST / 'tokens.css')
    _sk = ROOT / 'skill'
    if _sk.exists():
        (DIST / 'skill').mkdir(exist_ok=True)
        for _f in _sk.iterdir():
            if _f.is_file():
                shutil.copy(_f, DIST / 'skill' / _f.name)
    shutil.copy(ROOT / 'logo' / 'favicon.svg', DIST / 'favicon.svg')
    shutil.copy(ROOT / 'logo' / 'logo.svg', DIST / 'logo.svg')
    for _a in ('favicon.ico', 'apple-touch-icon.png', 'icon-192.png', 'icon-512.png', 'icon-maskable-512.png', 'ogp.png'):
        shutil.copy(ROOT / 'logo' / _a, DIST / _a)
    shutil.copy(ROOT / 'manifest.webmanifest', DIST / 'manifest.webmanifest')
    shutil.copy(ROOT / 'sw.js', DIST / 'sw.js')
    shutil.copy(ROOT / 'site.css', DIST / 'site.css')
    (DIST / 'index.html').write_text(emit(landing(comps, blocks, n_icons, templates), comps, None), encoding='utf-8')
    cdir = DIST / 'components'
    cdir.mkdir()
    (cdir / 'index.html').write_text(emit(components_index(comps), comps, None, '/components/', True), encoding='utf-8')
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
    (dsdir / 'index.html').write_text(emit(design_system_page(tokens), comps, None, '/design-system/', True), encoding='utf-8')
    prdir = DIST / 'pricing'
    prdir.mkdir()
    (prdir / 'index.html').write_text(emit(pricing_page(), comps, None, '/pricing/', True), encoding='utf-8')
    jadir = DIST / 'ja'
    jadir.mkdir()
    (jadir / 'index.html').write_text(emit(ja_page(), comps, None, '/ja/', True), encoding='utf-8')
    scdir = DIST / 'showcase'
    scdir.mkdir()
    (scdir / 'index.html').write_text(emit(showcase_page(templates, blocks), comps, None, '/showcase/', True), encoding='utf-8')
    shutil.copy(ROOT / 'system' / 'tokens.json', dsdir / 'tokens.json')
    idir = DIST / 'icons'
    idir.mkdir(exist_ok=True)
    (idir / 'index.html').write_text(emit(icons_page(), comps, None, '/icons/', True), encoding='utf-8')
    for f in (ROOT / 'icons').glob('*.svg'):
        shutil.copy(f, idir / f.name)
    bdir2 = ROOT / 'icons' / 'brands'
    if bdir2.exists():
        (idir / 'brands').mkdir(exist_ok=True)
        for f in bdir2.glob('*.svg'):
            shutil.copy(f, idir / 'brands' / f.name)
    bkdir = DIST / 'blocks'
    bkdir.mkdir(exist_ok=True)
    (bkdir / 'index.html').write_text(emit(blocks_index(blocks), comps, None, '/blocks/', True), encoding='utf-8')
    for i, b in enumerate(blocks):
        src = ROOT / 'blocks' / b['slug']
        dst = bkdir / b['slug']
        dst.mkdir(exist_ok=True)
        for f in src.iterdir():
            if f.is_file():
                shutil.copy(f, dst / f.name)
        (dst / 'index.html').write_text(emit(block_detail(blocks, i, comps), comps, None, '/blocks/' + blocks[i]['slug'] + '/', True), encoding='utf-8')
    tpdir = DIST / 'templates'
    tpdir.mkdir(exist_ok=True)
    (tpdir / 'index.html').write_text(emit(templates_index(templates), comps, None, '/templates/', True), encoding='utf-8')
    for i, t in enumerate(templates):
        src = ROOT / 'templates' / t['slug']
        dst = tpdir / t['slug']
        dst.mkdir(exist_ok=True)
        for f in src.iterdir():
            if f.is_file():
                shutil.copy(f, dst / f.name)
        (dst / 'index.html').write_text(emit(template_detail(templates, i, comps, blocks), comps, None, '/templates/' + templates[i]['slug'] + '/', True), encoding='utf-8')
    (DIST / 'registry.json').write_text(registry_json(comps, blocks, templates), encoding='utf-8')
    (DIST / 'llms.txt').write_text(llms_txt(comps, blocks, n_icons, templates), encoding='utf-8')
    (DIST / 'llms-full.txt').write_text(llms_full(comps, blocks, templates), encoding='utf-8')
    themes = load_themes()
    tdir = DIST / 'themes'
    tdir.mkdir(exist_ok=True)
    (tdir / 'index.html').write_text(emit(themes_page(themes), comps, None, '/themes/', True), encoding='utf-8')
    for t in themes:
        (tdir / (t['name'] + '.css')).write_text(theme_css(t), encoding='utf-8')
    ddir = DIST / 'docs'
    ddir.mkdir(exist_ok=True)
    (ddir / 'index.html').write_text(emit(docs_index(), comps, None, '/docs/', True), encoding='utf-8')
    for dslug, *_ in DOCS:
        dp = ddir / dslug
        dp.mkdir(exist_ok=True)
        (dp / 'index.html').write_text(emit(doc_page(dslug), comps, None, '/docs/' + dslug + '/', True), encoding='utf-8')
    # --- install artifacts: full bundles + starter zip ---
    _base = Path(__file__).parent
    _css = ['/* KATA UI full bundle - tokens + every component and block. For production, per-part copies are leaner; this is the fast start. */\n' + (_base / 'tokens.css').read_text(encoding='utf-8')]
    for _c in comps:
        if _c.get('css'):
            _css.append('\n/* ===== component: ' + _c['slug'] + ' ===== */\n' + _c['css'])
    for _b in blocks:
        if _b.get('css'):
            _css.append('\n/* ===== block: ' + _b['slug'] + ' ===== */\n' + _b['css'])
    for _t in templates:
        if _t.get('css'):
            _css.append('\n/* ===== template: ' + _t['slug'] + ' ===== */\n' + _t['css'])
    bundle_css = '\n'.join(_css)
    (DIST / 'kata-ui.css').write_text(bundle_css, encoding='utf-8')
    _js = ['/* KATA UI behavior bundle - each part in its own scope. Load at the end of <body>. Parts whose markup is absent stay inert. */']
    for _c in comps:
        if _c.get('js'):
            _js.append('\n/* ===== component: ' + _c['slug'] + ' ===== */\n(function(){\n' + _c['js'] + '\n})();')
    for _b in blocks:
        if _b.get('js'):
            _js.append('\n/* ===== block: ' + _b['slug'] + ' ===== */\n(function(){\n' + _b['js'] + '\n})();')
    for _t in templates:
        if _t.get('js'):
            _js.append('\n/* ===== template: ' + _t['slug'] + ' ===== */\n(function(){\n' + _t['js'] + '\n})();')
    bundle_js = '\n'.join(_js)
    (DIST / 'kata-ui.js').write_text(bundle_js, encoding='utf-8')
    import zipfile as _zf
    _sdir = DIST / 'starter'
    _sdir.mkdir(exist_ok=True)
    with _zf.ZipFile(_sdir / 'kata-starter.zip', 'w', _zf.ZIP_DEFLATED) as _z:
        _z.writestr('kata-starter/index.html', STARTER_HTML)
        _z.writestr('kata-starter/kata-ui.css', bundle_css)
        _z.writestr('kata-starter/kata-ui.js', bundle_js)
        _z.writestr('kata-starter/README.md', STARTER_README)
    # --- 404 + robots ---
    nf = head('Page not found — KATA UI', 'That page is not in the catalog.', '') + """
<div class="wrap">
  <div class="hero" style="text-align:center;padding:80px 0 30px">
    <span class="eyebrow"><i></i>404</span>
    <h1 style="font-size:40px;letter-spacing:-.025em">This part is not in the catalog.</h1>
    <p style="margin:14px auto 0;max-width:52ch;color:var(--ink2);line-height:1.85">The page moved, or it never existed. The catalog search is the fastest way back — press the search button above, or start from a genre:</p>
    <div class="cta" style="justify-content:center;margin-top:22px;display:flex;gap:10px;flex-wrap:wrap">
      <a class="btn-p" href="/components/" style="display:inline-flex;align-items:center;height:42px;padding:0 20px;border-radius:9px;background:#18181b;color:#fff;font-weight:500;font-size:14px;text-decoration:none">Browse components</a>
      <a href="/blocks/" style="display:inline-flex;align-items:center;height:42px;padding:0 20px;border-radius:9px;border:1px solid var(--hair);font-weight:500;font-size:14px;text-decoration:none;background:#fff">See blocks</a>
      <a href="/docs/" style="display:inline-flex;align-items:center;height:42px;padding:0 20px;border-radius:9px;border:1px solid var(--hair);font-weight:500;font-size:14px;text-decoration:none;background:#fff">Read the docs</a>
    </div>
  </div>
</div>
""" + FOOTER + """
</body>
</html>"""
    (DIST / '404.html').write_text(emit(nf, comps, None), encoding='utf-8')
    (DIST / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://kata-ui.dev/sitemap.xml\n', encoding='utf-8')
    urls = ['/', '/components/', '/design-system/', '/icons/', '/blocks/', '/templates/', '/themes/', '/docs/', '/pricing/', '/ja/', '/showcase/'] + [f"/components/{c['slug']}/" for c in comps] + [f"/blocks/{b['slug']}/" for b in blocks] + [f"/templates/{t['slug']}/" for t in templates] + [f"/docs/{d[0]}/" for d in DOCS]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
         '\n'.join(f'<url><loc>https://kata-ui.dev{u}</loc></url>' for u in urls) + '\n</urlset>\n'
    (DIST / 'sitemap.xml').write_text(sm, encoding='utf-8')
    # --- furniture post-pass: canonical, social meta, service worker ---
    import html as _html
    _sw = "<script>if('serviceWorker' in navigator){navigator.serviceWorker.register('/sw.js')}</script>"
    for _p in sorted(DIST.rglob('*.html')):
        _t = _p.read_text(encoding='utf-8')
        if '</body>' in _t and _sw not in _t:
            _t = _t.replace('</body>', _sw + '\n</body>', 1)
        if _p.name != '404.html' and 'og:title' not in _t:
            _rel = _p.relative_to(DIST)
            if _p.name == 'index.html':
                _url = '/' + '/'.join(_rel.parts[:-1]) + ('/' if _rel.parts[:-1] else '')
            else:
                _url = '/' + '/'.join(_rel.parts)
            _mt = re.search(r'<title>(.*?)</title>', _t, re.S)
            _md = re.search(r'<meta name="description" content="(.*?)"', _t, re.S)
            _title = _html.unescape(_mt.group(1)) if _mt else 'KATA UI'
            _desc = _html.unescape(_md.group(1)) if _md else ''
            _abs = 'https://kata-ui.dev' + _url
            _meta = ('<link rel="canonical" href="' + _abs + '">'
                     '<meta property="og:type" content="website">'
                     '<meta property="og:site_name" content="KATA UI">'
                     '<meta property="og:title" content="' + esc(_title) + '">'
                     '<meta property="og:description" content="' + esc(_desc) + '">'
                     '<meta property="og:url" content="' + _abs + '">'
                     '<meta property="og:image" content="https://kata-ui.dev/ogp.png">'
                     '<meta property="og:image:width" content="1200">'
                     '<meta property="og:image:height" content="630">'
                     '<meta name="twitter:card" content="summary_large_image">'
                     '<meta name="twitter:title" content="' + esc(_title) + '">'
                     '<meta name="twitter:description" content="' + esc(_desc) + '">'
                     '<meta name="twitter:image" content="https://kata-ui.dev/ogp.png">')
            _t = _t.replace('</head>', _meta + '\n</head>', 1)
        _p.write_text(_t, encoding='utf-8')
    print(f'built {len(comps)} components -> {DIST}')

if __name__ == '__main__':
    main()
