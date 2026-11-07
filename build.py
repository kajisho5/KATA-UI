#!/usr/bin/env python3
"""KATA UI — static site generator. Registry (components/) is the source of truth."""
import glob, hashlib, html, json, re, shutil
from tools.sync_shape_tokens import sync as sync_shape_tokens
from tools.anatomy import css_surface, aria_surface
from tools.mold_publish import label as audit_label, metadata as audit_metadata, summary_block, sync as sync_audit_docs
from tools.mold_view import audit as render_audit, checks as render_checks
from pathlib import Path

ROOT = Path(__file__).parent
sync_shape_tokens(ROOT)
from tools.mold_release import config as mold_config, requires_component, version_line, sync_docs as sync_mold_docs, changelog_html, history as mold_history
sync_mold_docs(ROOT)
MOLD_CONFIG = mold_config(ROOT)
DIST = ROOT / 'dist'
RELEASE_VERSION = json.loads((ROOT / 'cli' / 'package.json').read_text())['version']


def distribution_header(path, content):
    parts = Path(path).parts
    if len(parts) < 3 or parts[0] not in ('components', 'blocks', 'templates'):
        return content
    kind, name = parts[:2]
    meta = json.loads((ROOT / kind / name / 'meta.json').read_text())
    version = meta.get('version', RELEASE_VERSION)
    requirement=requires_component(kind,name,ROOT)
    stamp = f'KATA {name} {version} — kata-ui.dev/{kind}/{name} — requires mold >= {requirement}'
    if Path(path).suffix in ('.css', '.js'):
        return f'/* {stamp} */\n' + content
    if Path(path).suffix == '.html':
        return f'<!-- {stamp} -->\n' + content
    return content

CATS = ['Form & Input', 'Layout & Navigation', 'Overlays & Dialogs', 'Feedback & Status', 'Display & Media', 'Motion', 'KATAYABURI', 'Japan']

STARTER_HTML = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>KATA Starter — your first page</title>\n<link rel="stylesheet" href="kata-ui.css">\n<style>\n  body{font-family:var(--k-font);background:var(--k-bg-soft);color:var(--k-ink);margin:0;padding:36px 18px}\n  main{max-width:520px;margin:0 auto;display:grid;gap:14px}\n  h1{font-size:21px;letter-spacing:-.02em}\n  p.lead{color:var(--k-ink-2);font-size:14px;line-height:1.75;letter-spacing:.012em}\n</style>\n</head>\n<body>\n<main>\n  <h1>It works. This page is KATA parts, unmodified.</h1>\n  <p class="lead">Everything below comes from kata-ui.css and kata-ui.js in this folder. Copy a part from kata-ui.dev, paste it here, and it matches — same mold, same tokens.</p>\n  <div class="k-card">\n    <div class="k-card-h">Create your account</div>\n    <div class="k-card-b" style="display:grid;gap:12px">\n      <span class="field" style="display:grid;gap:6px"><label for="em">Email</label><input class="input" id="em" type="email" placeholder="you@company.com"></span>\n      <label class="switchrow" style="display:flex;align-items:center;gap:10px;font-size:13.5px"><span class="switch"><input type="checkbox" checked><span class="tr"></span></span>Email me product updates</label>\n      <div style="display:flex;gap:9px;align-items:center">\n        <button class="btn btn-pri btn-md">Create account</button>\n        <span class="badge asagi"><i></i>Free for 30 days</span>\n      </div>\n    </div>\n  </div>\n  <p class="lead">Next: browse the catalog at kata-ui.dev/components — each part carries its own CSS tab, so you can drop the bundle and keep only what you use.</p>\n</main>\n<script src="kata-ui.js"></script>\n</body>\n</html>\n'
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
        cb_file = d / 'combos.html'
        combos = []
        if cb_file.exists():
            raw = cb_file.read_text(encoding='utf-8')
            pm = re.search(r'<!--\s*parts:\s*(.+?)\s*-->', raw)
            cparts = [x.strip() for x in pm.group(1).split(',')] if pm else []
            chunks = re.split(r'<!--\s*combo:\s*(.+?)\s*-->', raw)
            for i in range(1, len(chunks) - 1, 2):
                seg = chunks[i + 1]
                nm = re.search(r'<!--\s*note:\s*(.+?)\s*-->', seg)
                note = nm.group(1) if nm else ''
                if nm:
                    seg = seg.replace(nm.group(0), '', 1)
                combos.append((chunks[i], note, cparts, seg.strip()))
        comps.append(dict(slug=slug, meta=meta, preview=preview, css=css, js=js, deps=deps, examples=examples, combos=combos))
    order = {c: i for i, c in enumerate(CATS)}
    comps.sort(key=lambda c: (order.get(c['meta']['category'], 99), c['meta']['title']))
    return comps

def esc(s):
    return html.escape(s)

HEADER = """<header class="top"><div class="wrap top-in">
  <a class="logo" href="/"><svg width="27" height="27" viewBox="0 0 48 48" aria-hidden="true"><rect x="7" y="7" width="16.6" height="16.6" fill="currentColor"/><rect x="32.95" y="7" width="8.05" height="8.05" fill="currentColor"/><rect x="24.4" y="15.55" width="8.05" height="8.05" fill="currentColor"/><rect x="7" y="24.4" width="16.6" height="16.6" fill="#d4d4d8"/><rect x="24.4" y="24.4" width="16.6" height="16.6" fill="#eb471f"/></svg>KATA UI<small>preview</small></a>
  <button class="menubtn" id="menubtn" type="button" aria-label="Open menu">☰<span>Menu</span></button>
  <nav><a href="/docs/">Docs</a><a href="/components/">Components</a><a href="/blocks/">Blocks</a><a href="/templates/">Templates</a><a href="/icons/">Icons</a><a href="/themes/">Themes</a><a href="/design-system/">Design System</a><a href="/pricing/">Pricing</a></nav>
  <button class="hsearch" type="button" data-site-search aria-label="Search the catalog"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.5-4.5"/></svg><span class="hst">Search</span><span class="k-kbd">\u2318K</span></button>
  <a class="gh" href="https://github.com/kajisho5/KATA-UI" rel="noopener" aria-label="KATA UI on GitHub"><svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.8a9.2 9.2 0 0 0-9.2 9.2c0 4.1 2.7 7.6 6.4 9 .5.1.6-.2.6-.4v-1.4c-2.6.6-3.1-1.2-3.1-1.2-.4-1.1-1-1.3-1-1.3-.9-.6.1-.6.1-.6.9.1 1.4.9 1.4.9.9 1.4 2.2 1 2.7.8.1-.6.3-1.1.6-1.3-2.1-.2-4.2-1-4.2-4.6 0-1 .4-1.8.9-2.5-.1-.2-.4-1.1.1-2.3 0 0 .8-.2 2.5.9a8.6 8.6 0 0 1 4.5 0c1.7-1.1 2.5-.9 2.5-.9.5 1.2.2 2.1.1 2.3.5.7.9 1.5.9 2.5 0 3.6-2.2 4.4-4.2 4.6.3.3.6.9.6 1.8v2.6c0 .2.2.5.6.4a9.2 9.2 0 0 0 6.4-9A9.2 9.2 0 0 0 12 2.8z"/></svg></a>
</div></header>"""

FOOTER = """<div class="wrap"><footer class="site">
  <span><b>KATA UI</b> — parts, cast from a single mold.</span>
  <span class="fprin">One mold · Tokens first · Three shapes only · Flat before fancy · The vermillion core never moves</span>
  <span class="fmold">__MOLD__</span>
  <span style="margin-left:auto"><a href="https://github.com/kajisho5/KATA-UI" rel="noopener">GitHub</a> · <a href="/docs/">Docs</a> · <a href="/design-system/">Design System</a> · <a href="/themes/">Themes</a></span>
</footer></div>"""

import subprocess as _sp, sys as _sys
_r = _sp.run([_sys.executable, str(ROOT / 'check.py'), '--json', '-'], capture_output=True, text=True, timeout=90)
if _r.returncode not in (0, 1):
    raise RuntimeError('Mold checker failed: ' + _r.stderr)
MOLD_REPORT = json.loads(_r.stdout)
_summary = MOLD_REPORT['summary']
_ms = audit_label(MOLD_REPORT)
(ROOT / 'mold-results.json').write_text(json.dumps(MOLD_REPORT, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
sync_audit_docs(ROOT, MOLD_REPORT)
MOLD_ITEMS = {item['id']: item for item in MOLD_REPORT['items']}
MOLD_STATUS = _ms
FOOTER = FOOTER.replace('__MOLD__', '<a href="/audit/">' + _ms + '</a>')


def render_usage(text):
    """Render escaped usage prose and optional fenced JavaScript examples."""
    segments = re.split(r'```(?:js|javascript)\n(.*?)\n```', text, flags=re.S)
    return ''.join('<pre><code class="language-javascript">' + esc(part) + '</code></pre>'
                   if index % 2 else '<p>' + esc(part.strip()) + '</p>'
                   for index, part in enumerate(segments) if part.strip())


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
  <div class="kcmd-body">
    <div class="kcmd-left">
      <ul class="kcmd-list" data-site-list></ul>
      <div class="kcmd-empty" data-site-empty style="display:none">No results.</div>
    </div>
    <div class="kcmd-pv" data-site-pv><div class="kcmd-pv-note">Highlight a part to see it live.</div></div>
  </div>
</dialog>
<script>
const KIDX = __KATA_INDEX__;
const sDlg = document.querySelector('[data-site-dialog]');
const sIn = sDlg.querySelector('[data-site-input]');
const sList = sDlg.querySelector('[data-site-list]');
const sEmpty = sDlg.querySelector('[data-site-empty]');
const sPv = sDlg.querySelector('[data-site-pv]');
const sCache = {}, sCssDone = {};
let sPvSeq = 0;
function sPreview() {
  const it = sShown[sAct];
  if (!it || !sPv) return;
  const m = it.u.match(/^[/](components|blocks|templates)[/]([a-z0-9-]+)[/]$/);
  if (!m) { sPv.innerHTML = '<div class="kcmd-pv-note"><b>' + it.t + '</b><span>' + it.k + ' \u2014 Enter opens the page.</span></div>'; return; }
  const seq = ++sPvSeq;
  const show = html => { if (seq === sPvSeq) sPv.innerHTML = '<div class="kcmd-pv-stage">' + html + '</div><p class="kcmd-pv-cap">' + it.t + ' \u2014 live from its page</p>'; };
  if (sCache[it.u]) { show(sCache[it.u]); return; }
  sPv.innerHTML = '<div class="kcmd-pv-note">Casting a preview\u2026</div>';
  fetch(it.u).then(r => r.text()).then(txt => {
    const doc = new DOMParser().parseFromString(txt, 'text/html');
    doc.querySelectorAll('link[rel="stylesheet"]').forEach(l => {
      const href = l.getAttribute('href');
      if (href && !sCssDone[href] && /[/](components|blocks|templates)[/]/.test(href)) { sCssDone[href] = 1; const nl = document.createElement('link'); nl.rel = 'stylesheet'; nl.href = href; document.head.appendChild(nl); }
    });
    const st = doc.querySelector('#stage') || doc.querySelector('.stage');
    const html = st ? st.innerHTML : '<div class="kcmd-pv-note">No preview stage on that page.</div>';
    sCache[it.u] = html; show(html);
  }).catch(() => { if (seq === sPvSeq) sPv.innerHTML = '<div class="kcmd-pv-note">Preview unavailable.</div>'; });
}
let sAct = 0, sShown = [];
function sRender(q) {
  const query = (q || '').trim().toLowerCase();
  sShown = KIDX.filter(it => !query || it.t.toLowerCase().includes(query) || it.k.toLowerCase().includes(query)).slice(0, 14);
  sAct = 0;
  sList.innerHTML = sShown.map((it, i) => '<li><button type="button" class="kcmd-item' + (i === sAct ? ' active' : '') + '" data-su="' + it.u + '"><span>' + it.t + '</span><span class="kcmd-hint">' + it.k + '</span></button></li>').join('');
  sEmpty.style.display = sShown.length ? 'none' : '';
  sList.querySelectorAll('[data-su]').forEach((b, i) => {
    b.addEventListener('click', () => { location.href = b.dataset.su; });
    b.addEventListener('mouseenter', () => { if (sAct !== i) { sAct = i; sList.querySelectorAll('.kcmd-item').forEach((el, j) => el.classList.toggle('active', j === sAct)); sPreview(); } });
  });
  sPreview();
}
function sOpen() { if (!sDlg.open) { sIn.value = ''; sRender(''); sDlg.showModal(); sIn.focus(); } }
function sMove(d) { if (!sShown.length) return; sAct = (sAct + d + sShown.length) % sShown.length; sList.querySelectorAll('.kcmd-item').forEach((el, i) => el.classList.toggle('active', i === sAct));  sPreview(); }
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
    items += [{'t': t, 'u': u, 'k': 'Page'} for t, u in [('Components', '/components/'), ('Blocks', '/blocks/'), ('Templates', '/templates/'), ('Icons', '/icons/'), ('Themes', '/themes/'), ('Design System', '/design-system/'), ('Docs', '/docs/'), ('Pricing', '/pricing/'), ('Showcase', '/showcase/'), ('Comparison', '/compare/')]]
    return SEARCH_TMPL.replace('__KATA_INDEX__', _json.dumps(items, ensure_ascii=False))


FOUNDRY_HTML = """<button class="fdeck-fab" id="fdfab" type="button" aria-expanded="false" aria-controls="fdeck"><span class="fdot"></span>Foundry</button>
<div class="fdeck" id="fdeck" role="dialog" aria-label="Foundry — recast this page">
  <h3><span class="fdot"></span>The Foundry<span style="margin-left:auto;font-weight:500;color:var(--ink3);font-size:11.5px">one change recasts everything</span></h3>
  <div class="frow"><label>Radius <output id="fd-rv">8px</output></label><input type="range" id="fd-radius" min="0" max="20" step="1" value="8"></div>
  <div class="frow"><label for="fd-accent">Custom accent</label><input id="fd-accent" type="color" value="#33a6b8"></div>
  <div class="frow"><label>Accent — a traditional color</label><div class="sws" id="fd-sws"></div></div>
  <div class="frow"><span style="background:var(--k-accent);color:var(--k-on-accent)">Text on accent</span> · <span style="color:var(--k-accent-ink)">Accent text</span></div>
  <div class="frow"><label>Mode</label><div class="fseg"><button type="button" id="fd-light">Light (washi)</button><button type="button" id="fd-dark">Dark (sumi)</button></div></div>
  <div class="frow"><label>Backdrop \u2014 wagara</label><div class="fseg" id="fd-wgs"><button type="button" data-wg="">None</button><button type="button" data-wg="seigaiha">Seigaiha</button><button type="button" data-wg="asanoha">Asanoha</button><button type="button" data-wg="ichimatsu">Ichimatsu</button></div></div>
  <div class="frow"><label>Motion <output id="fd-mv">1.0&times;</output></label><input type="range" id="fd-motion" min="0" max="2" step="0.1" value="1"></div>
  <div class="frow"><output id="fd-times" aria-label="Effective transition durations"></output><small>Curves: ease · in-out · spring · bounce</small></div>
  <div class="fcore"><i></i><span>The vermillion core — \u578b\u306e\u6731 — is not on the deck. It never moves; that is the point of a mold.</span></div>
  <div class="flog" id="fd-log"></div>
  <button class="freset" type="button" data-export-theme>Export theme CSS</button>
  <button class="freset" id="fd-reset" type="button">Reset to the mold</button>
</div>"""
FOUNDRY_JS = """<script>
(function(){var fab=document.getElementById('fdfab'),deck=document.getElementById('fdeck');if(!fab||!deck)return;
var PRESETS=[["Asagi","#33A6B8","#165E83","#81C7D4"],["Ruri","#1E50A2","#223A70","#58B2DC"],["Edomurasaki","#745399","#592C63","#8B81C3"],["Suo","#8E354A","#64363C","#DC9FB4"],["Kaki","#ED6D3D","#95483F","#E2943B"]];
PRESETS=PRESETS.concat(Object.entries(__KATA_FIXED_PALETTE__).map(function(pair){return [pair[0],pair[1]]}));
var S={};try{S=JSON.parse(localStorage.getItem('kata-fdeck')||'{}')}catch(e){}
var root=document.documentElement,logEl=document.getElementById('fd-log');
function save(){try{localStorage.setItem('kata-fdeck',JSON.stringify(S))}catch(e){}}
function log(msg){var d=document.createElement('div');var now=new Date();d.textContent=now.toTimeString().slice(0,5)+'  '+msg;logEl.prepend(d);while(logEl.children.length>4)logEl.lastChild.remove();}
function dark(){return root.getAttribute('data-theme')==='dark'}
function applyAccent(p,quiet){document.getElementById('fd-accent').value=p[1];S.accent=p[1];S.accentInk=p[2];S.darkInk=p[3];S.accentName=p[0];root.style.setProperty('--k-accent',p[1]);root.style.setProperty('--acc',p[1]);root.style.removeProperty("--k-accent-ink");document.querySelectorAll('#fd-sws .sw').forEach(function(b){b.classList.toggle('on',b.dataset.n===p[0])});if(!quiet)log('Accent \u2192 '+p[0]);save();}
function applyRadius(v,quiet){S.radius=+v;root.style.setProperty('--k-radius',v+'px');document.getElementById('fd-rv').textContent=v+'px';if(!quiet)log('Radius \u2192 '+v+'px');save();}
function applyMode(d,quiet){S.dark=d;if(d)root.setAttribute('data-theme','dark');else root.removeAttribute('data-theme');if(S.accent){var p=PRESETS.filter(function(x){return x[0]===S.accentName})[0];if(p)root.style.removeProperty("--k-accent-ink");}document.getElementById('fd-light').classList.toggle('on',!d);document.getElementById('fd-dark').classList.toggle('on',d);if(!quiet)log(d?'Mode \u2192 Dark (sumi)':'Mode \u2192 Light (washi)');document.querySelectorAll('#stage').forEach(function(st){st.setAttribute('data-theme',d?'dark':'light');});document.querySelectorAll('[data-seg="theme"]').forEach(function(sg){sg.querySelectorAll('button').forEach(function(b){b.classList.toggle('on',(b.dataset.v==='dark')===!!d);});});save();}
function applyMotion(v,quiet){var reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;document.getElementById('fd-times').textContent=Object.entries(__KATA_MOTION_DURATIONS__).map(function(pair){return pair[0]+' '+Math.round(pair[1]*(reduced?0:+v))+'ms'}).join(' · ');S.mscale=+v;root.style.setProperty('--k-mscale',v);document.getElementById('fd-mv').textContent=(+v).toFixed(1)+'\u00d7';if(!quiet)log('Motion \u2192 '+(+v).toFixed(1)+'\u00d7');save();}
var sws=document.getElementById('fd-sws');PRESETS.forEach(function(p){var b=document.createElement('button');b.type='button';b.className='sw';b.dataset.n=p[0];b.title=p[0];b.style.background=p[1];b.setAttribute('aria-label','Accent '+p[0]);b.addEventListener('click',function(){applyAccent(p)});sws.appendChild(b);});
document.getElementById('fd-accent').addEventListener('input',function(){applyAccent(['Custom',this.value])});
fab.addEventListener('click',function(){var open=deck.classList.toggle('open');fab.setAttribute('aria-expanded',open)});
document.getElementById('fd-radius').addEventListener('input',function(e){applyRadius(e.target.value)});
document.getElementById('fd-motion').addEventListener('input',function(e){applyMotion(e.target.value)});
function applyBg(w,quiet){S.wg=w;if(w)root.setAttribute('data-wg',w);else root.removeAttribute('data-wg');document.querySelectorAll('#fd-wgs button').forEach(function(b){b.classList.toggle('on',b.dataset.wg===w)});if(!quiet)log('Backdrop \u2192 '+(w||'none'));save();}
document.querySelectorAll('#fd-wgs button').forEach(function(b){b.addEventListener('click',function(){applyBg(b.dataset.wg)})});
document.getElementById('fd-light').addEventListener('click',function(){applyMode(false)});
document.getElementById('fd-dark').addEventListener('click',function(){applyMode(true)});
document.getElementById('fd-reset').addEventListener('click',function(){S={};save();root.removeAttribute('data-theme');['--k-radius','--k-radius-sm','--k-radius-lg','--k-accent','--k-accent-ink','--acc','--k-mscale'].forEach(function(k){root.style.removeProperty(k)});document.getElementById('fd-radius').value=8;document.getElementById('fd-motion').value=1;applyRadius(8,true);applyMotion(1,true);applyMode(false,true);document.querySelectorAll('#fd-sws .sw').forEach(function(b){b.classList.remove('on')});applyBg('',true);log('Reset to the mold');});
if(S.radius!==undefined){document.getElementById('fd-radius').value=S.radius;applyRadius(S.radius,true);}
document.getElementById('fd-motion').value=S.mscale===undefined?1:S.mscale;applyMotion(S.mscale===undefined?1:S.mscale,true);
matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change',function(){applyMotion(S.mscale,true)});
if(S.accentName){var p0=PRESETS.filter(function(x){return x[0]===S.accentName})[0];if(p0)applyAccent(p0,true);else if(S.accent)applyAccent(['Custom',S.accent],true);}
applyBg(S.wg||'',true);
applyMode(dark(),true);
})();
</script>""".replace("__KATA_MOTION_DURATIONS__", json.dumps(json.loads((ROOT / "system/tokens.json").read_text())["motion"]["durationsMs"])).replace("__KATA_FIXED_PALETTE__",json.dumps(json.loads((ROOT / "system/tokens.json").read_text())["color"].get("fixed",{})))


def emit(page, comps, active, current=None, tree=False):
    if tree:
        import re as _re
        page = _re.sub(r'<div class="(wrap|wrap dc|wrap ds|wrap bk|wrap tk)">',
                       lambda m: m.group(0) + '<div class="layout">' + nav_tree(comps, active, current) + '<div class="lmain">',
                       page, count=1)
        page = page.replace('<div class="wrap"><footer class="site">', '</div></div><div class="wrap"><footer class="site">', 1)
    return page.replace('</body>', drawer_html(comps, active) + DRAWER_JS + search_html(comps) + FOUNDRY_HTML + FOUNDRY_JS + '</body>', 1)

WA_TOKEN = 'ea804ab11ad24ba099ed62f14cf32bcf'
WA_BEACON = ''
if WA_TOKEN:
    WA_BEACON = '<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon=\'{"token": "' + WA_TOKEN + '"}\'></script>'

def head(title, desc, extra=''):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<script>(function(){{try{{var s=JSON.parse(localStorage.getItem("kata-fdeck")||"{{}}");var r=document.documentElement;if(s.dark||(!("dark" in s)&&window.matchMedia&&matchMedia("(prefers-color-scheme: dark)").matches))r.setAttribute("data-theme","dark");if(s.radius!==undefined){{r.style.setProperty("--k-radius",s.radius+"px");}}if(s.accent){{r.style.setProperty("--k-accent",s.accent);r.style.setProperty("--acc",s.accent);r.style.removeProperty("--k-accent-ink");if(s.wg)r.setAttribute(\"data-wg\",s.wg);}}}}catch(e){{}}}})();</script>
<script src="/color-roles.js"></script>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/manifest.webmanifest">
{WA_BEACON}
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

def card(c, gallery=False, compact=False):
    m = c['meta']
    tags = ''.join(f'<span class="tag">{esc(t)}</span>' for t in m.get('tags', []))
    q = esc((m['title'] + ' ' + c['slug'] + ' ' + ' '.join(m.get('tags', [])) + ' ' + m['category']).lower())
    stage = ''
    if gallery and '<canvas' not in c['preview']:
        pv_html = re.sub(r'\s*<link rel="stylesheet"[^>]*>', '', c['preview']).strip()
        # The card itself is an <a>; a preview containing anchors would make the
        # HTML parser close the card early and scatter its body (nested-<a> rule).
        # The stage is inert (aria-hidden, pointer-events off), so preview links
        # become spans that keep their classes and look.
        pv_html = re.sub(r'<a(\s[^>]*?)?>', lambda m: '<span' + re.sub(r'\s+href="[^"]*"', '', m.group(1) or '') + '>', pv_html)
        pv_html = pv_html.replace('</a>', '</span>')
        assert '<a ' not in pv_html and '</a>' not in pv_html, c['slug']
        stage = f'<span class="gstage" aria-hidden="true"><span class="gscale">{pv_html}</span></span>'
    return f"""<a class="card{' gcard' if gallery else ''}" data-q="{q}" data-status="{esc(m.get('status','stable'))}" href="/components/{c['slug']}/">
  {stage}<h3>{esc(m['title'])} <span class="st st-{esc(m.get('status','stable'))}">{esc(m.get('status','stable'))}</span></h3>
  {'' if compact else f'<p>{esc(m["description"])}</p>'}
  {'' if compact else f'<span class="tags">{tags}</span>'}
</a>"""

def catalog_sections(comps):
    out = []
    for cat in CATS:
        group = [c for c in comps if c['meta']['category'] == cat]
        if not group:
            continue
        cards = '\n'.join(card(c, gallery=True) for c in group)
        kb = ' kburi' if cat == 'KATAYABURI' else ''
        _exp = '<p class="expnote">The experimental line \u2014 showpieces. The production shelf carries the same mold without the performance.</p>' if cat in ('Motion', 'KATAYABURI') else ''
        out.append(f'<section class="catsec{kb}"><h2>{esc(cat)}</h2>{_exp}<div class="cards">\n{cards}\n</div></section>')
    return '\n'.join(out)

LP_STYLE = """<style>
.lp .hero{padding:64px 0 8px;text-align:center}
.lp .hero h1{font-size:44px;line-height:1.12}
.lp .hero p{margin-left:auto;margin-right:auto}
.lp .cta{justify-content:center}
.lp .stats{justify-content:center}
.browser{margin:38px auto 0;max-width:880px;border:1px solid var(--hair);border-radius:12px;overflow:hidden;background:var(--paper);box-shadow:0 18px 44px -24px rgba(16,24,40,.22);text-align:left}
.browser-bar{display:flex;align-items:center;gap:7px;padding:10px 14px;border-bottom:1px solid var(--hair);background:var(--soft)}
.browser-bar i{width:10px;height:10px;border-radius:50%;background:var(--hair);display:block}
.browser-bar .url{margin-left:8px;font-family:var(--mono);font-size:11px;color:var(--ink3);border:1px solid var(--hair);border-radius:6px;padding:3px 10px;background:var(--paper)}
.browser .shell{border:0;border-radius:0}
.livechip{display:inline-flex;align-items:center;gap:8px;font-family:var(--mono);font-size:11px;letter-spacing:.05em;color:var(--ink2)}
.livechip i{width:7px;height:7px;border-radius:50%;background:var(--acc);flex:none}
.livechip.on-dark{color:#d4d4d8}
.browser{position:relative}
.framelive{position:absolute;top:12px;left:14px;z-index:4;background:rgba(11,11,15,.78);padding:5px 10px;border-radius:99px}
.fann{position:absolute;z-index:4;font-family:var(--mono);font-size:11px;font-weight:600;background:rgba(11,11,15,.85);color:#f4f4f5;padding:5px 10px;border-radius:99px;opacity:0;transition:opacity .18s ease;pointer-events:none;white-space:nowrap}
.browser:hover .fann,.browser:focus-within .fann{opacity:1}
@media (hover:none){.fann{display:none}}
.moldface{font-size:29px;font-weight:600;letter-spacing:-.022em;line-height:1.25;margin-top:12px;max-width:26em}
.lpc{margin-top:16px;border-top:1px solid var(--k-line);padding-top:14px;display:grid;gap:10px}
.lpc-cap{font-family:var(--mono);font-size:11px;letter-spacing:.06em;color:var(--k-ink-2)}
.lpc-row{display:flex;align-items:center;gap:12px;font-size:12.5px;color:var(--k-ink-2)}
.lpc-row>span:first-child{width:52px;flex:none;font-weight:550}
.lpc-note{font-size:12.5px;color:var(--k-ink-2)}
.lpc .ds-btns button{background:var(--k-bg);border-color:var(--k-border-strong);color:var(--k-ink-2)}
.lpc .ds-btns button.on{background:var(--k-ink);border-color:var(--k-ink);color:var(--k-bg)}
.lpc .ds-sws button.on{border-color:var(--k-ink)}
.tokcode{font-family:var(--mono);font-size:12px;line-height:1.75;background:var(--soft);border:1px solid var(--hair);border-radius:10px;padding:12px 14px;overflow-x:auto;text-align:left;margin-top:12px;white-space:pre}
.sctabs{display:flex;gap:6px;margin-top:18px;overflow-x:auto;padding-bottom:2px}
.sctab-btn{flex:none;font:inherit;font-size:13.5px;font-weight:550;padding:8px 16px;border-radius:99px;border:1px solid var(--hair);background:var(--paper);color:var(--ink2);cursor:pointer}
.sctab-btn.on{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.scframe{position:relative;margin-top:14px;border:1px solid var(--hair);border-radius:12px;overflow:hidden;background:var(--paper)}
.scframe iframe{width:100%;height:600px;border:0;display:block}
@media (max-width:720px){.scframe iframe{height:540px}}
.framelive{pointer-events:none}
.sccap{margin-top:12px;font-size:13.5px;color:var(--ink2)}
.scmeta{margin-top:6px;font-family:var(--mono);font-size:11.5px;color:var(--ink2);display:flex;gap:14px;flex-wrap:wrap}
.scmeta a{color:var(--acc)}
.motiongrid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:18px}
@media (max-width:720px){.motiongrid{grid-template-columns:1fr}}
.billboard{font-size:34px;font-weight:650;letter-spacing:-.022em;margin-top:28px;line-height:1.2}
.cmpcta{margin-top:18px;display:flex;gap:10px;flex-wrap:wrap}
.cmpsum{display:none}
@media (max-width:720px){.cmpsum{display:grid;gap:8px;margin-top:16px}.cmpsum>div{display:flex;gap:12px;align-items:baseline;font-size:13px;border:1px solid var(--hair);border-radius:10px;padding:9px 12px}.cmpsum b{font-family:var(--mono);font-size:10.5px;letter-spacing:.05em;color:var(--ink3);flex:none;width:86px}.cmpsum .k{font-weight:600}.billboard{font-size:27px}}
.pronums{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:24px}
.pronums b{display:block;font-size:42px;font-weight:650;letter-spacing:-.025em;line-height:1.05}
.pronums span{font-size:13px;color:var(--ink2)}
@media (max-width:720px){.pronums{grid-template-columns:1fr}.pronums b{font-size:34px}}
.probars{margin-top:26px;display:grid;gap:12px;max-width:660px}
.proster{margin-top:28px;border-top:1px solid var(--hair);padding-top:2px}
.proster-h{font-family:var(--mono);font-size:11px;letter-spacing:.08em;color:var(--ink3);margin:16px 0 10px}
.prochips{display:flex;flex-wrap:wrap;gap:8px}
.prochip{border:1px solid var(--hair);border-radius:8px;padding:7px 12px;font-size:13px;color:var(--ink);text-decoration:none}
.prochip:hover{border-color:var(--ink3)}
.probar{display:grid;grid-template-columns:150px 1fr 64px;align-items:center;gap:12px;font-size:13px}
.probar .track{height:10px;background:var(--soft);border-radius:99px;overflow:hidden}
.probar .track i{display:block;height:100%;border-radius:99px}
.probar b{text-align:right;font-weight:600}
@media (max-width:560px){.probar{grid-template-columns:104px 1fr 52px;font-size:12px}}
.finalcta{text-align:center}
.fc-cta{margin-top:22px;display:flex;gap:10px;justify-content:center;flex-wrap:wrap}
.hero3{text-align:center;padding:76px 0 6px}
.hero3-eyebrow{font-family:var(--mono);font-size:11.5px;letter-spacing:.05em;color:var(--ink2)}
.hero3-eyebrow a{color:inherit;text-decoration:underline;text-underline-offset:2px}
.hero3 h1{font-size:64px;line-height:1.06;letter-spacing:-.028em;font-weight:650;margin-top:24px}
.hero3 h1 .dim{color:var(--ink2)}
.hero3-sub{max-width:60ch;margin:24px auto 0;font-size:15.5px;line-height:1.85;color:var(--ink2);letter-spacing:.012em}
.hero3 .cta{margin-top:30px;display:flex;gap:10px;justify-content:center;flex-wrap:wrap}
.hero3 .herotrust{margin-top:24px;color:var(--ink3)}
.hero3 .herotrust .fmold{color:var(--ink2)}
@media (max-width:720px){.hero3{padding:52px 0 2px}.hero3 h1{font-size:34px}.hero3 .cta{flex-direction:column;align-items:stretch}.hero3 .cta a{justify-content:center}}
#one-mold .castlive{max-width:920px;margin-left:0}
.cl-grid2{display:grid;grid-template-columns:1fr 1fr;gap:8px 28px;margin-top:12px}
.cl-grid2 figure{margin:0}
@media (max-width:760px){.cl-grid2{grid-template-columns:1fr}}
.speccap{font-family:var(--mono);font-size:10.5px;letter-spacing:.04em;color:var(--k-ink-2);margin-top:8px}
.term{font-family:var(--mono);font-size:12px;line-height:1.75;background:var(--soft);border:1px solid var(--hair);border-radius:10px;padding:12px 14px;overflow-x:auto;text-align:left;margin-top:12px;white-space:pre;color:var(--ink)}
.term .dim{color:var(--ink3)}
.proofstrip{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:16px}
.proofstrip>div{border:1px solid var(--hair);border-radius:12px;padding:16px 18px}
.proofstrip h3{font-size:14.5px;font-weight:600;margin-bottom:6px}
.proofstrip p{font-size:13.5px;color:var(--ink2);line-height:1.75}
.proofstrip .vs{font-family:var(--mono);font-size:10.5px;letter-spacing:.05em;color:var(--ink3);display:block;margin-bottom:8px}
@media (max-width:720px){.proofstrip{grid-template-columns:1fr}}
.proofline{margin-top:14px;font-size:14.5px;line-height:1.8;max-width:68ch}
.psframe{max-width:1080px}
.pscreen{display:grid;grid-template-columns:224px 1fr;min-height:520px}
.ps-side{border-right:1px solid var(--hair);background:var(--k-bg-soft)}
.ps-side .k-side{height:100%}
.ps-main{padding:18px;display:grid;gap:16px;align-content:start;min-width:0}
.ps-row{display:grid;grid-template-columns:1.15fr .85fr;gap:16px;align-items:start}
.ps-chart figure{margin:0}
.ps-table{overflow-x:auto}
.psmani{display:flex;gap:7px;flex-wrap:wrap;margin-top:14px;align-items:center}
.psmani .pm{font-size:12px;font-weight:550;border:1px solid var(--hair);border-radius:99px;padding:4px 12px;color:var(--ink2);text-decoration:none}
.psmani .pm:hover{color:var(--ink);border-color:var(--ink3)}
.psmani .pm i{font-style:normal;font-family:var(--mono);font-size:9.5px;color:var(--k-yamabuki-ink,#8a5a00);margin-left:5px}
.psmani .lead{font-family:var(--mono);font-size:10.5px;letter-spacing:.05em;color:var(--ink3);margin-right:2px}
.tplrow{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:14px}
.tplrow a{display:block;border:1px solid var(--hair);border-radius:12px;padding:13px 15px;text-decoration:none;color:var(--ink)}
.tplrow b{font-size:14px;font-weight:600;display:block}
.tplrow span{font-size:12px;color:var(--ink2)}
@media (max-width:900px){.pscreen{grid-template-columns:190px 1fr}.ps-row{grid-template-columns:1fr}}
@media (max-width:720px){.pscreen{grid-template-columns:1fr}.ps-side{display:none}.tplrow{grid-template-columns:1fr 1fr}}
.framecap{max-width:880px;margin:10px auto 0;text-align:right;font-size:12px;color:var(--ink3)}
.framecap a{color:var(--ink2)}
.lpsec{margin-top:64px}
.lpsec.proof{margin-top:96px}
.lpsec h2{font-size:27px;font-weight:600;letter-spacing:-.02em}
.lpsec .sub{margin-top:7px;color:var(--ink2);font-size:14px;line-height:1.8;max-width:62ch;letter-spacing:.012em}
.steps{margin-top:20px;display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px}
.step{border:1px solid var(--hair);border-radius:12px;background:var(--paper);padding:18px}
.step .no{font-family:var(--mono);font-size:11px;color:var(--acc);font-weight:600;letter-spacing:.08em}
.step h3{margin-top:8px;font-size:15px;font-weight:600}
.step p{margin-top:6px;font-size:13px;color:var(--ink2);line-height:1.75;letter-spacing:.01em}
.step code{font-family:var(--mono);font-size:12px;background:var(--soft);border-radius:5px;padding:1px 5px}
.genres{margin-top:20px;display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px}
.genre{border:1px solid var(--hair);border-radius:12px;background:var(--paper);padding:18px;text-decoration:none;color:var(--ink);display:block}
.genre:hover{border-color:var(--ink3)}
.genre .gn{font-family:var(--mono);font-size:11px;color:var(--ink3);letter-spacing:.06em}
.genre h3{margin-top:7px;font-size:15.5px;font-weight:600}
.genre p{margin-top:6px;font-size:13px;color:var(--ink2);line-height:1.75;letter-spacing:.01em}
.showband{margin-top:64px;background:#0b0b0f;border-radius:12px;padding:30px 26px}
.showband h2{font-size:22px;font-weight:600;letter-spacing:-.02em;color:#f4f4f5}
.showband .sub{margin-top:7px;color:#a1a1aa;font-size:14px;line-height:1.8;max-width:62ch;letter-spacing:.012em}
.showgrid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:20px}
@media (max-width:720px){.showgrid{grid-template-columns:1fr}}
.showtile{border:1px solid #26262b;border-radius:14px;padding:16px;background:#17171a;overflow:hidden;color:var(--k-ink)}
.showtile.wide{grid-column:1/-1}
.showtile .cap{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;font-family:var(--mono);font-size:11px;letter-spacing:.07em;color:#a1a1aa}
.showtile .cap a{color:#f4f4f5;text-decoration:none;letter-spacing:0;font-size:12px}
.hero2 .eyebrow{display:inline-flex;align-items:center;gap:8px}
.hero2 .stats div{display:flex;flex-direction:column;align-items:center;gap:1px}
.hero2 .eyebrow i{background:var(--k-core)}
.hero2-in{position:relative}
.hero2 h1{font-size:64px;line-height:1.05;color:#f4f4f5;letter-spacing:-.028em;font-weight:650}
.hero2 h1 .dim{color:#d4d4d8}
.hero2-in>p{max-width:62ch;margin:17px auto 0;font-size:15px;line-height:1.85;color:#a1a1aa;letter-spacing:.012em}
.hero2 .eyebrow{border-color:#3f3f46;color:#d4d4d8;background:rgba(255,255,255,.05)}
.hero2 .eyebrow{white-space:nowrap}
.hero2-in p{color:#d4d4d8}
@media (max-width:560px){.hero2 .eyebrow{font-size:11px;padding:5px 10px}.hero2 .stats{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}.hero2 .stats b{font-size:19px}.hero2 .stats span{font-size:10.5px}}
.hero2 .stats{border-color:#26262b;display:flex;gap:15px 38px;flex-wrap:wrap;justify-content:center;margin-top:34px;padding-top:22px;border-top:1px solid #26262b}
.hero2 .stats b{color:#f4f4f5}
.hero2 .stats span{color:#a1a1aa}
.hero2 .framecap{color:#a1a1aa;position:relative;z-index:1}
.hero2 .framecap a{color:#e4e4e7}
@media (max-width:720px){.hero2{padding:42px 16px 22px}.hero2 h1{font-size:34px}}
@media (max-width:720px){.hero2 .cta{flex-direction:column;align-items:stretch}.hero2 .cta a{flex:none;justify-content:center}}
@media (max-width:560px){.hero2 .eyebrow{white-space:normal;line-height:1.6;text-align:center}}
.collage-sec{margin-top:64px}
.collage-sec h2{font-size:22px;font-weight:600;letter-spacing:-.02em}
.collage-sec .sub{margin-top:7px;color:var(--ink2);font-size:14px;line-height:1.8;max-width:62ch;letter-spacing:.012em}
.collage{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:18px}
.collage-cell{border:1px solid var(--hair);border-radius:14px;padding:18px;background:var(--paper);overflow:hidden;min-width:0}
.collage-cell.wide{grid-column:1/-1}
.collage-cell .cap{display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;font-family:var(--mono);font-size:10.5px;letter-spacing:.08em;color:var(--ink3)}
.collage-cell .cap a{color:var(--acc);text-decoration:none;font-family:inherit}
.collage-cell div.k-dt{overflow-x:auto;max-width:none!important}
.collage-cell table.k-dt-t{min-width:500px}
@media (max-width:720px){.collage{grid-template-columns:1fr}}
.cmptable{width:100%;min-width:600px;border-collapse:collapse;margin-top:18px;font-size:13.5px;background:var(--paper);border:1px solid var(--hair);border-radius:12px;overflow:hidden}
.cmptable th,.cmptable td{padding:11px 14px;border-bottom:1px solid var(--hair);text-align:left;vertical-align:top}
.cmptable thead th{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink3);background:var(--soft);font-weight:600}
.cmptable tbody th{font-weight:550;color:var(--ink2);white-space:nowrap}
.cmptable td{color:var(--ink2)}
.cmptable td.me{color:var(--ink);font-weight:550}
.cmptable tr:last-child td,.cmptable tr:last-child th{border-bottom:none}
.cmpnote{margin-top:9px;font-size:12px;color:var(--ink3)}
@media (max-width:720px){.cmptable{font-size:12px}.cmptable th,.cmptable td{padding:9px 9px}}
.compat{margin-top:20px;border:1px solid var(--hair);border-radius:12px;background:var(--soft);padding:18px;font-size:13.5px;line-height:1.9;color:var(--ink2);letter-spacing:.012em}
.compat b{color:var(--ink);font-weight:600}
.compat a{color:var(--ink);font-weight:550}
@media (max-width:720px){.lp .hero h1{font-size:33px}.browser .shell-side{display:none}}
</style>"""

def audit_page():
    return head('Audit — KATA UI', 'Current static check results.') + render_audit(MOLD_REPORT, ROOT) + plain_footer() + '</body></html>'


def plain_footer():
    return '<div class="wrap"><footer class="site"><b>KATA UI</b><a href="/audit/">' + MOLD_STATUS + '</a><a href="/docs/">Docs</a><a href="/lab/">Lab</a><a href="https://github.com/kajisho5/KATA-UI">GitHub</a></footer></div>'


def status_split(comps):
    """Count meta.json status values; the home page prints these, never a typed number."""
    stable = sum(1 for c in comps if c['meta'].get('status') == 'stable')
    return stable, len(comps) - stable


def landing(comps, blocks, n_icons, templates=None):
    n = len(comps)
    nb = len(blocks)
    nt = len(templates or [])
    _nbrands = len(list((ROOT / 'icons' / 'brands').glob('*.svg')))
    LIVECHIP = '<span class="livechip"><i></i>LIVE \u2014 this code is copyable</span>'
    shell = next((b for b in blocks if b['slug'] == 'app-shell'), None)
    shell_html = shell['preview'] if shell else ''
    pv = {c['slug']: c for c in comps}
    def tile(slug, label, wide=False):
        c = pv.get(slug)
        if not c:
            return ''
        return ('<div data-theme="dark" class="showtile' + (' wide' if wide else '') + '"><div class="cap"><span>' + label.upper() + '</span><a href="/components/' + slug + '/">Open part</a></div>' + c['preview'] + '</div>')
    show_scripts = ''.join(f'<script src="/components/{sl}/{sl}.js?v={_v(pv[sl]["js"])}"></script>' for sl in ('counter', 'spotlight', 'text-reveal', 'follow-frame', 'reorder', 'word-rotate', 'goo-tabs', 'dock', 'jelly-buttons', 'scramble', 'bounce-letters', 'tilt-card', 'marquee') if pv.get(sl) and pv[sl]['js'])
    faq_b = next((b for b in blocks if b['slug'] == 'faq'), None)
    principles = ('<section class="lpsec"><h2>Two more rules, cast into every part</h2><div class="steps">'
      '<div class="step"><span class="no">OWNERSHIP</span><h3>Yours to keep</h3><p>Copied code has no roadmap and no breaking changes. Nobody can sunset it, reprice it, or deprecate it under you. <a href="/docs/why-vanilla/" style="color:var(--acc)">Why vanilla</a></p></div>'
      '<div class="step"><span class="no">PLATFORM</span><h3>Native first</h3><p>Where the platform has the element \u2014 dialog, details, real inputs \u2014 the part is the element. Scripts layer behavior on markup; they never generate it.</p></div>'
      '</div></section>')
    compare = ('<section class="lpsec"><h2>How KATA compares</h2>'
      '<div class="cmpsum"><div><b>FRAMEWORK</b><span class="k">KATA: none</span><span>shadcn/ui: React</span></div><div><b>RUNTIME</b><span class="k">KATA: none</span><span>shadcn/ui: React</span></div><div><b>DISTRIBUTION</b><span class="k">KATA: copy-paste</span><span>shadcn/ui: CLI + copy</span></div></div>'
      '<div style="overflow-x:auto"><table class="cmptable"><thead><tr><th></th><th>KATA UI</th><th>shadcn/ui</th><th>Others</th></tr></thead><tbody>'
      '<tr><th>Framework</th><td class="me">None \u2014 plain HTML</td><td>React</td><td>React, Laravel, or another stack</td></tr>'
      '<tr><th>Runtime</th><td class="me">None</td><td>React</td><td>The framework\u2019s runtime</td></tr>'
      '<tr><th>Distribution</th><td class="me">Copy-paste, CLI &amp; registry</td><td>Copy-paste + CLI</td><td>npm or Composer package</td></tr>'
      '<tr><th>Theming</th><td class="me">CSS tokens \u2014 one file is the mold</td><td>Tailwind + variables</td><td>Theme object or utility config</td></tr>'
      '<tr><th>Ownership</th><td class="me">Yours outright \u2014 MIT, no upstream</td><td>Yours, inside a React codebase</td><td>Rented \u2014 a package, their roadmap</td></tr>'
      '<tr><th>AI friendliness</th><td class="me">Registry + Skill: the AI fetches checked parts</td><td>Files an AI can copy \u2014 React-bound</td><td>APIs the AI must already know</td></tr>'
      '<tr><th>Quality without React</th><td class="me">The whole shelf, framework-free</td><td>None \u2014 React required</td><td>Partial \u2014 tied to their stack</td></tr>'
      '</tbody></table></div>'
      '<p class="cmpnote">From each project\u2019s public pages, November 2026. In summary: the others are excellent inside their framework.</p>'
      '<p class="billboard">KATA is for everywhere else.</p>'
      '<p class="cmpcta"><a class="btn btn-pri btn-md" href="/components/">Browse the catalog</a><a class="btn btn-ghost btn-md" href="/docs/react/">Read the React guide</a></p></section>')
    _mt = ''
    for _slug, _label in [('aurora', 'Aurora'), ('spotlight', 'Spotlight'), ('text-reveal', 'Text Reveal'), ('converge', 'Converge')]:
        _c = pv.get(_slug)
        if _c:
            _mt += ('<div class="showtile"><div class="cap"><span>' + _label.upper() + '</span><span class="livechip"><i></i>LIVE</span><a href="/components/' + _slug + '/">Open part</a></div>' + _c['preview'] + '</div>')
    motionband = ('<section class="lpsec proof"><h2>Motion, on duty</h2>'
      '<p class="sub">Motion is not decoration here. It points at what changed, confirms what you did, and explains state while it happens \u2014 and every part below is running live, with its reduced-motion behavior written in.</p>'
      '<div class="motiongrid">' + _mt + '</div></section>')
    finalcta = ('<section class="lpsec finalcta"><h2>Start with one part.</h2>'
      '<p class="sub" style="margin-left:auto;margin-right:auto">Ninety seconds from now it can be on your page \u2014 tokens in, part pasted, shipped.</p>'
      '<p class="fc-cta"><a class="btn btn-pri btn-lg" href="#first-five">Copy your first part</a><a class="btn btn-ghost btn-lg" href="/pricing/">See what Pro adds</a></p></section>')
    _pro_chips_b = ''.join('<a class="prochip" href="/blocks/' + b['slug'] + '/">' + esc(b['meta']['title']) + '</a>' for b in load_blocks())
    _pro_chips_t = ''.join('<a class="prochip" href="/templates/' + t['slug'] + '/">' + esc(t['meta']['title']) + '</a>' for t in load_templates())
    _proster = ('<div class="proster"><p class="proster-h">EVERYTHING IN PRO \u2014 21 BLOCKS</p><div class="prochips">' + _pro_chips_b + '</div>'
      '<p class="proster-h">7 TEMPLATES</p><div class="prochips">' + _pro_chips_t + '</div>'
      '<p class="lpnote" style="margin-top:12px">Every one of them is a live page on this site \u2014 open any chip and inspect exactly what you would get.</p></div>')
    proband = ('<section class="lpsec proof" id="pro"><h2>Pro is assembled time.</h2>'
      '<p class="sub">The parts are free. What Pro sells is the hours you do not spend composing them \u2014 21 blocks and 7 templates, with source files and current static check results.</p>'
      '<div class="pronums"><div><b>&asymp;77 h</b><span>of assembly, done for you</span></div><div><b>$129</b><span>once \u2014 lifetime, every future block</span></div><div><b>$1.68</b><span>per hour of it</span></div></div>'
      '<div class="probars"><div class="probar"><span>Assemble it yourself</span><div class="track"><i style="width:100%;background:var(--ink)"></i></div><b>&asymp;77 h</b></div><div class="probar"><span>With Pro</span><div class="track"><i style="width:2%;background:var(--acc);min-width:10px"></i></div><b>minutes</b></div></div>'
      '<p class="lpnote" style="margin-top:16px">Founding 100: $99, plus two blocks that will never be sold separately \u2014 Help Center and Job Board.</p>'
      + _proster +
      '<p class="lpnote" style="margin-top:14px">Free is the finished product. Pro is for people who would rather not compose. <a href="/pricing/" style="color:var(--acc)">Pricing and the launch list</a></p></section>')
    pr_block = next((b for b in blocks if b['slug'] == 'pricing'), None)
    asmx = ''
    if pr_block:
        pr_uses = [u for u in pr_block['meta'].get('uses', []) if u in pv]
        pr_js = f'<script src="/blocks/pricing/pricing.js?v={_v(pr_block["js"])}"></script>' if pr_block.get('js') else ''
        asmx = ('<section class="lpsec asmx"><h2>Assembled, then taken apart</h2>'
          '<p class="asm-note">The Pricing block is not drawn \u2014 it is composed: ' + str(len(pr_uses)) + ' parts from this catalog, snapped into one section. Flip the switch and take it apart; every piece is a part you can copy on its own.</p>'
          '<label class="asm-switch"><span class="switch"><input type="checkbox" class="asm-tgl"><span class="tr"></span></span> Exploded view</label>'
          '<div class="asm-frame">' + pr_block['preview'] + '</div>'
          '<div class="showgrid asm-parts">' + ''.join(tile(u, pv[u]['meta']['title']) for u in pr_uses) + '</div>'
          + pr_js + '</section>')
    mstrip = ('<section class="lpsec"><h2>The motion shelf</h2><div class="mstrip">'
      + tile('word-rotate', 'Word Rotate') + tile('goo-tabs', 'Goo Tabs') + tile('dock', 'Dock') + '</div>'
      '<p class="framecap">Live parts, auto-playing: the Motion line itself, running on this page.</p></section>')
    lp_faq = ('<section class="k-faqb" style="max-width:640px"><div class="acc">' + '<details class="k-acc" open><summary>Can I use it with React?<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="square" stroke-linejoin="bevel" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg></summary><div class="k-acc-body">Yes. The parts are plain HTML, CSS and JS: markup pastes into JSX as-is, the CSS loads once, globally, and the JS parts mount as islands where a page needs them. The limits are written down, too \u2014 read the <a href="/docs/react/" style="color:var(--acc)">React guide</a>.</div></details><details class="k-acc"><summary>Will the free parts ever go paid?<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="square" stroke-linejoin="bevel" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg></summary><div class="k-acc-body">No. All 136 components are MIT \u2014 free for personal and commercial work, forever. Pro only ever adds assembled work on top: blocks and templates. It never reaches back for the parts.</div></details><details class="k-acc"><summary>How do I install a part?<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="square" stroke-linejoin="bevel" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg></summary><div class="k-acc-body">Open its page and copy the three files \u2014 or take the starter kit and pull parts with the CLI. The registry is machine-readable JSON, so your AI tools can fetch parts for you, too.</div></details><details class="k-acc"><summary>What does Pro add?<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="square" stroke-linejoin="bevel" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg></summary><div class="k-acc-body">The assembled shelf: 21 blocks and 7 page templates, plus every future block. Free is the finished product \u2014 Pro is for people who would rather not compose. One payment of $129, lifetime; sales open soon, and the waitlist gets exactly one email when they do.</div></details><details class="k-acc"><summary>Can I use it in client work?<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="square" stroke-linejoin="bevel" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg></summary><div class="k-acc-body">Yes \u2014 the MIT license covers components in client projects, and the Pro license covers blocks and templates the same way. Ship it, invoice it, keep the code.</div></details>' + '</div>'
              '<p class="more">Still stuck? <a href="/docs/">Read the docs</a> — or check the <a href="/docs/faq/">full FAQ</a>.</p></section>'
              '<link rel="stylesheet" href="/components/accordion/accordion.css">')
    _five = [next((c for c in comps if c['slug'] == sl), None) for sl in ('button', 'input', 'badge', 'tabs', 'toast')]
    _five = [c for c in _five if c]
    firstfive = ('<section class="lpsec" id="first-five"><h2>First five to copy</h2>'
      '<p class="lpnote">New here? These five cover most first screens \u2014 an action, a field, a status, a switch of views, a word of feedback. Copy them in order and the mold explains itself.</p>'
      '<div class="cards" style="margin-top:16px">' + ''.join(card(c) for c in _five) + '</div></section>')
    _ch = next((d for d in DOCS if d[0] == 'changelog'), None)
    _rows = ''
    if _ch:
        for _t, *_rest in _ch[3][:3]:
            _d, _, _ti = _t.partition(' \u2014 ')
            _rows += f'<a class="frow" href="/docs/changelog/"><span class="fdate">{esc(_d)}</span><span class="ftitle">{esc(_ti or _t)}</span></a>'
    fresh = ('<section class="lpsec"><h2>Fresh from the mold</h2><div class="fresh">' + _rows + '</div>'
      '<p class="lpnote">Every casting is recorded \u2014 <a href="/docs/changelog/">the full changelog</a>.</p></section>')
    faqsec = ('<section class="lpsec"><h2>Questions</h2><div style="margin-top:16px">' + lp_faq + '</div></section>')
    sc_block = next((b for b in blocks if b['slug'] == 'stat-cards'), None)
    kb_block = next((b for b in blocks if b['slug'] == 'kanban'), None)
    def ccell(href, label, html, wide=False):
        return ('<div class="collage-cell' + (' wide' if wide else '') + '"><div class="cap"><span>' + label.upper() + '</span><a href="' + href + '">Open part</a></div>' + html + '</div>')
    collage = ('<section class="collage-sec"><h2>Assembled from catalog parts.</h2>'
               '<p class="sub">This dashboard is not a screenshot. Every panel here is a live part from the catalog — the same code the copy button hands you, running on this page.</p>'
               '<div class="collage">'
               + (ccell('/blocks/stat-cards/', 'Stat Cards — Block', sc_block['preview'], True) if sc_block else '')
               + (ccell('/blocks/kanban/', 'Kanban \u2014 Block', kb_block['preview'], True) if kb_block else '')
               + ccell('/components/calendar/', 'Calendar', pv['calendar']['preview'])
               + ccell('/components/sparkline/', 'Sparkline', pv['sparkline']['preview'])
               + '</div></section>')
    showcase = ('<section class="showband"><h2>The showy shelf</h2><p class="sub">The Motion line and the ambient pieces — live on this page, in the dark they were designed for. Built to be stared at a little.</p>'
                '<div data-theme="dark"><div class="showgrid">'
                + tile('beam-border', 'Beam Border') + tile('glass-panel', 'Glass Panel') + tile('follow-frame', 'Follow Frame') + tile('jelly-buttons', 'Jelly Buttons') + tile('scramble', 'Scramble') + tile('bounce-letters', 'Bounce Letters') + tile('tilt-card', 'Tilt Card')
                + tile('reorder', 'Reorder', True) + tile('counter', 'Counter') + tile('marquee', 'Marquee')
                + '</div></div>' + show_scripts + '</section>')
    pv_chart = pv['bar-chart']['preview'] if pv.get('bar-chart') else ''
    pv_donut = pv['donut-chart']['preview'] if pv.get('donut-chart') else ''
    moldlive = ('<section class="lpsec proof" id="one-mold"><h2>One mold</h2>'
      '<p class="moldface">Two parts built months apart look built on the same day.</p>'
      '<p class="lpnote">Both were poured into the same mold: one file of tokens \u2014 color, radius, spacing, motion \u2014 that every part reads and no part overrides. Change the mold and the parts re-cast. Try it: nothing here is a picture.</p>'
      '<div class="castlive" data-theme="light" style="margin:18px 0 6px">'
      '<div class="cl-cap"><span>Live cast</span><span class="livechip"><i></i>LIVE</span><a href="#" id="cl-open">Open the Foundry deck</a></div>'
      '<div class="cl-row">'
      '<button class="btn btn-pri btn-md" type="button">Cast me</button>'
      '<span class="switch asagi"><input type="checkbox" checked aria-label="Live cast switch"><span class="tr"></span></span>'
      '<input class="input" type="text" placeholder="Tokens in, parts out" style="max-width:210px" aria-label="Live cast input">'
      '<span class="badge asagi"><i></i>Same mold</span>'
      '</div>'
      '<div class="k-card" style="margin-top:14px"><div class="k-card-h"><div><h3>Casting notes</h3><p>The same card, whatever the mold says.</p></div><span class="sp"><span class="badge asagi">Live</span></span></div><div class="k-card-b">A composed surface: cast below and the card, its badge and its button move with everything else on the page.</div><div class="k-card-f">Cast from tokens<span class="sp"><button class="btn btn-pri btn-sm" type="button">Open report</button></span></div></div><p class="speccap">Card \u00b7 Beta</p>'
      + '<div class="cl-grid2"><div>' + pv_chart + '<p class="speccap">Bar Chart \u00b7 Beta \u2014 it re-casts with everything else</p></div><div>' + pv_donut + '<p class="speccap">Donut Chart \u00b7 Beta</p></div></div>'
      '<div class="lpc">'
      '<div class="lpc-cap">Cast it yourself</div>'
      '<div class="lpc-row"><span>Accent</span><span class="ds-sws"><button type="button" data-lpc-accent="Asagi" style="background:#33A6B8" aria-label="Cast Asagi"></button><button type="button" data-lpc-accent="Ruri" style="background:#1E50A2" aria-label="Cast Ruri"></button><button type="button" data-lpc-accent="Edomurasaki" style="background:#745399" aria-label="Cast Edomurasaki"></button><button type="button" data-lpc-accent="Suo" style="background:#8E354A" aria-label="Cast Suo"></button><button type="button" data-lpc-accent="Kaki" style="background:#ED6D3D" aria-label="Cast Kaki"></button></span></div>'
      '<div class="lpc-row"><span>Radius</span><span class="ds-btns"><button type="button" data-lpc-radius="0">0</button><button type="button" data-lpc-radius="4">4</button><button type="button" data-lpc-radius="8">8 \u00b7 mold</button><button type="button" data-lpc-radius="12">12</button><button type="button" data-lpc-radius="16">16</button><button type="button" data-lpc-radius="20">20</button></span></div>'
      '<div class="lpc-row"><span>Motion</span><span class="ds-btns"><button type="button" data-lpc-motion="0.7">0.7&times;</button><button type="button" data-lpc-motion="1">1.0&times; \u00b7 mold</button><button type="button" data-lpc-motion="1.4">1.4&times;</button></span></div>'
      '<div class="lpc-row"><span>Mode</span><span class="ds-btns"><button type="button" data-lpc-mode="light">Light</button><button type="button" data-lpc-mode="dark">Dark</button></span></div>'
      '<p class="lpc-note">What you set here follows you across the whole site \u2014 the Foundry deck remembers.</p>'
      '</div></div>'
      '<p class="lpnote" style="margin-top:12px">Scroll on \u2014 the sections below have re-cast too.</p>'
      "<script>var clo=document.getElementById('cl-open');if(clo)clo.addEventListener('click',function(e){e.preventDefault();var f=document.getElementById('fdfab');if(f)f.click();});</script>"
      '<script>(function(){var root=document.documentElement;var PRESETS={Asagi:["#33A6B8","#165E83","#81C7D4"],Ruri:["#1E50A2","#223A70","#58B2DC"],Edomurasaki:["#745399","#592C63","#8B81C3"],Suo:["#8E354A","#64363C","#DC9FB4"],Kaki:["#ED6D3D","#95483F","#E2943B"]};function load(){try{return JSON.parse(localStorage.getItem("kata-fdeck")||"{}")}catch(e){return{}}}function save(S){try{localStorage.setItem("kata-fdeck",JSON.stringify(S))}catch(e){}}function dark(){return root.getAttribute("data-theme")==="dark"}function mark(){var S=load();document.querySelectorAll("[data-lpc-accent]").forEach(function(b){b.classList.toggle("on",b.dataset.lpcAccent===S.accentName)});document.querySelectorAll("[data-lpc-radius]").forEach(function(b){b.classList.toggle("on",+b.dataset.lpcRadius===(S.radius===undefined?8:S.radius))});document.querySelectorAll("[data-lpc-mode]").forEach(function(b){b.classList.toggle("on",(b.dataset.lpcMode==="dark")===dark())});document.querySelectorAll("[data-lpc-motion]").forEach(function(b){b.classList.toggle("on",+b.dataset.lpcMotion===(S.mscale||1))})}function accent(name){var pr=PRESETS[name];if(!pr)return;var S=load();S.accent=pr[0];S.accentInk=pr[1];S.darkInk=pr[2];S.accentName=name;root.style.setProperty("--k-accent",pr[0]);root.style.setProperty("--acc",pr[0]);root.style.removeProperty("--k-accent-ink");save(S);mark()}function radius(v){var S=load();S.radius=v;root.style.setProperty("--k-radius",v+"px");save(S);mark()}function motion(v){var S=load();S.mscale=v;root.style.setProperty("--k-mscale",v);save(S);mark()}function mode(d){var S=load();S.dark=d;if(d)root.setAttribute("data-theme","dark");else root.removeAttribute("data-theme");if(S.accentName&&PRESETS[S.accentName]){var pr=PRESETS[S.accentName];root.style.removeProperty("--k-accent-ink");mark()}document.querySelectorAll("[data-lpc-accent]").forEach(function(b){b.addEventListener("click",function(){accent(b.dataset.lpcAccent)})});document.querySelectorAll("[data-lpc-radius]").forEach(function(b){b.addEventListener("click",function(){radius(+b.dataset.lpcRadius)})});document.querySelectorAll("[data-lpc-mode]").forEach(function(b){b.addEventListener("click",function(){mode(b.dataset.lpcMode==="dark")})});document.querySelectorAll("[data-lpc-motion]").forEach(function(b){b.addEventListener("click",function(){motion(+b.dataset.lpcMotion)})});mark();})();</script>'
      '</section>')
    threeways = ('<section class="lpsec proof"><h2>Three ways in</h2>'
      '<p class="sub">However you work, there is a door at your height. All three end at the same place: the real part, in your project, owned by you.</p>'
      '<div class="steps">'
      '<div class="step"><span class="no">COPY-PASTE</span><h3>The part\u2019s page</h3><p>Open a part, copy its three files, done. Still the fastest way in for a single part \u2014 about ten seconds.</p><div class="term">&lt;button class="btn btn-pri btn-md"&gt;Save&lt;/button&gt;<br><span class="dim">button.html \u00b7 button.css \u00b7 button.js</span></div><p style="margin-top:10px"><a href="/components/button/" style="color:var(--acc)">Open Button \u2192</a></p></div>'
      '<div class="step"><span class="no">CLI</span><h3>One file, no install</h3><p>The CLI is a single script. It fetches the part \u2014 and the parts it depends on \u2014 and writes them where they belong:</p><div class="term">$ npx @kajisho5/kataui init<br><span class="dim">  + kata/tokens.css</span><br>$ npx @kajisho5/kataui add data-table<br><span class="dim">  + kata/components/badge/badge.css<br>  + kata/components/button/button.css</span><br>  + kata/components/data-table/data-table.css<br>  + kata/components/data-table/data-table.js<br><span class="dim">added data-table (component)</span></div><p style="margin-top:10px"><a href="/docs/cli/" style="color:var(--acc)">Get the CLI \u2192</a></p></div>'
      '<div class="step"><span class="no">REGISTRY &amp; SKILL</span><h3>Let your AI fetch</h3><p>The registry is machine-readable, and the Skill teaches your model the mold \u2014 tokens, heights, states \u2014 so it assembles instead of inventing.</p><div class="term">GET kata-ui.dev/registry.json<br><span class="dim">"Build this form from KATA UI parts \u2014<br> fetch each part from the registry,<br> unmodified."</span></div><p style="margin-top:10px"><a href="/docs/ai-prompts/" style="color:var(--acc)">AI prompts \u2192</a></p></div>'
      '</div>'
      '<div class="proofstrip">'
      '<div><span class="vs">AN AI, WRITING FROM SCRATCH</span><h3>A new dialect per prompt</h3><p>New class names, a new radius, spacing by mood. Screen one and screen ten drift apart \u2014 and every state it forgot is yours to find.</p></div>'
      '<div><span class="vs">AN AI, FETCHING KATA</span><h3>The same part, every time</h3><p>The registry includes each part&#39;s source and current static check results.</p></div>'
      '</div>'
      '<p class="proofline">Same prompt, two outcomes. Letting your AI fetch a mold-checked part is faster than reviewing its improvisation \u2014 and the registry includes source files and their current static check results.</p>'
      '</section>')
    _nav_m = re.search(r'<nav class="k-side".*?</nav>', pv['sidebar']['preview'], re.S) if pv.get('sidebar') else None
    _fld_m = re.search(r'<div class="field">.*?</div>', pv['input']['preview'], re.S) if pv.get('input') else None
    _sel_m = re.search(r'<label style="display:grid;gap:6px;font-size:12\.5px;font-weight:550">.*?</label>', pv['select']['preview'], re.S) if pv.get('select') else None
    _ps_nav = _nav_m.group(0) if _nav_m else ''
    _ps_fld = _fld_m.group(0) if _fld_m else ''
    _ps_sel = _sel_m.group(0) if _sel_m else ''
    _ps_chart = pv['line-chart']['preview'] if pv.get('line-chart') else ''
    _ps_table = pv['data-table']['preview'] if pv.get('data-table') else ''
    _mani = ''
    for _slug in ('sidebar', 'data-table', 'line-chart', 'input', 'select', 'switch', 'button', 'card'):
        _c = pv.get(_slug)
        if _c:
            _beta = '<i>BETA</i>' if _c['meta'].get('status') == 'beta' else ''
            _mani += f'<a class="pm" href="/components/{_slug}/">{_c["meta"]["title"]}{_beta}</a>'
    _tplrow = ''
    for _slug, _label in [('dashboard', 'Dashboard'), ('inbox', 'Inbox'), ('settings-page', 'Settings'), ('checkout', 'Checkout')]:
        _t = _tmap.get(_slug) if (_tmap := {t['slug']: t for t in (templates or [])}) else None
        if _t:
            _tplrow += f'<a href="/templates/{_slug}/demo/"><b>{_label}</b><span>{len(_t["meta"].get("uses", []))} parts composed \u00b7 open the live page \u2192</span></a>'
    demoband = ('<section class="lpsec proof"><h2>A working product screen</h2>'
      '<p class="sub">Sidebar, chart, form and data table \u2014 one screen, composed entirely from parts on this site, at the density a real product needs. Nothing here is a render: every control is live, and every part on this screen is copyable.</p>'
      '<div class="browser psframe">'
      '<span class="livechip on-dark framelive"><i></i>LIVE \u2014 this code is copyable</span>'
      '<span class="fann" style="left:4%;top:36%">Sidebar</span><span class="fann" style="left:47%;top:15%">Line Chart \u00b7 Beta</span><span class="fann" style="left:76%;top:15%">Form</span><span class="fann" style="left:52%;top:62%">Data Table \u00b7 Beta</span>'
      '<div class="browser-bar"><i></i><i></i><i></i><span class="url">your-app.com</span></div>'
      '<div class="pscreen"><div class="ps-side">' + _ps_nav + '</div>'
      '<div class="ps-main"><div class="ps-row"><div class="ps-chart">' + _ps_chart + '</div>'
      '<div class="k-card"><div class="k-card-h"><div><h3>Workspace settings</h3><p>Form parts, composed.</p></div></div><div class="k-card-b" style="display:grid;gap:12px">' + _ps_fld + _ps_sel + '</div><div class="k-card-f"><span class="switch asagi"><input type="checkbox" checked aria-label="Email notifications"><span class="tr"></span></span>&nbsp; Notifications<span class="sp"><button class="btn btn-pri btn-sm" type="button">Save</button></span></div></div></div>'
      '<div class="ps-table">' + _ps_table + '</div>'
      '</div></div></div>'
      '<div class="psmani"><span class="lead">ON THIS SCREEN</span>' + _mani + '</div>'
      '<p class="lpnote" style="margin-top:12px">Prefer whole pages? The templates are this, finished \u2014 each one a real page, running full-screen.</p>'
      '<div class="tplrow">' + _tplrow + '</div>'
      f'<script src="/components/sidebar/sidebar.js?v={_v(pv["sidebar"]["js"])}"></script>'
      f'<script src="/components/data-table/data-table.js?v={_v(pv["data-table"]["js"])}"></script>'
      '</section>') if _ps_nav else ''
    videoband = ('<section class="lpsec"><h2>Watch one get built</h2>'
      '<p class="lpnote">A settings page, assembled from catalog parts in one take \u2014 no cuts, nothing written on camera. Each element lands by pasting the part from its page, and the timer is the real one: sixteen seconds of pasting, because the styling was already done inside the parts.</p>'
      '<div style="margin-top:14px"><span class="livechip"><i></i>LIVE \u2014 this code is copyable</span></div>'
      '<div class="vidwrap"><video autoplay muted loop playsinline preload="metadata" poster="/media/build-settings-poster.jpg" aria-label="Screen recording: a settings page assembled from KATA parts in sixteen seconds"><source src="/media/build-settings.webm" type="video/webm"><source src="/media/build-settings.mp4" type="video/mp4"></video></div>'
      '<p class="lpnote" style="margin-top:12px">The finished page is the <a href="/templates/settings-page/demo/">Settings template, running live</a> \u2014 open it and take it apart.</p></section>')
    reactband = ('<section class="lpsec"><h2>On React? Cast anyway.</h2>'
      '<p class="lpnote">Framework-free is not framework-hostile. The markup pastes into JSX, the CSS loads once at your root, and the few JS parts mount where they land and enhance in place. React keeps the state; the mold keeps the look.</p>'
      '<div class="steps" style="margin-top:16px">'
      '<div class="step"><span class="no">JSX</span><h3>Paste the markup</h3><p>class becomes className, comments get braces — the rest of the part is already written.</p></div>'
      '<div class="step"><span class="no">CSS ONCE</span><h3>Load it at the root</h3><p>tokens.css and the part styles go in your layout or global stylesheet. No CSS-in-JS, no runtime.</p></div>'
      '<div class="step"><span class="no">ISLANDS</span><h3>Enhance in place</h3><p>Tabs, dialogs and menus read the DOM you server-render. No wrappers, no hydration contract.</p></div>'
      '</div>'
      '<p class="lpnote" style="margin-top:14px"><a href="/docs/react/" style="font-weight:600">The React field guide \u2192</a></p></section>')
    trust = ('<section class="lpsec"><p class="trustnote"><b>Public since November 1, 2026 \u2014 early days, on the record.</b> '
      'No customer logos yet, and this page will not invent any; the changelog above is the track record so far. '
      'Built something with KATA? <a href="/showcase/">Get it listed</a> \u00b7 <a href="https://github.com/kajisho5/KATA-UI">KATA on GitHub</a></p></section>')
    labhead = ('<section class="lpsec labsec"><h2>The Lab \u2014 Motion &amp; KATAYABURI</h2>'
      '<p class="lpnote">Showpieces, cast from the same mold. They prove the tokens can move; the production shelf is everything above this line.</p></section>')
    allband = ('<section class="lpsec"><div class="allband"><h2>All ' + str(n) + ' parts, one catalog</h2>'
      '<p class="lpnote" style="margin-left:auto;margin-right:auto">Every part with its live preview, its code and its mold check \u2014 searchable, and filterable by Stable and Beta.</p>'
      '<a class="allband-cta" href="/components/">Browse the catalog</a></div></section>')
    body = f"""
<div class="wrap lp">
<header class="hero3">
<p class="hero3-eyebrow">{n} components (<a href="/components/?status=stable">{status_split(comps)[0]} stable</a> · <a href="/components/?status=beta">{status_split(comps)[1]} beta</a>) · {nb} blocks · {nt} templates</p>
<h1>HTML, CSS and JavaScript<br><span class="dim">for the page you're building.</span></h1>
<p class="hero3-sub">Copy the files into your project. No framework, no build step.</p>
<div class="cta"><a class="btn btn-pri btn-lg" href="/components/">Browse components</a><a class="btn btn-ghost btn-lg" href="/docs/getting-started/">Get started</a></div>
<p class="herotrust">MIT · <a class="fmold" href="/audit/">{MOLD_STATUS.split(' · ')[0]}</a> · <a href="/audit/">Results</a></p>
</header>
<section class="lpsec"><h2>One mold: shared tokens</h2><p class="lpnote">Load tokens.css, then a component. Change a token; every part follows.</p></section>
<section class="lpsec"><h2>Five to start</h2><div class="cards cards-min">{''.join(card(c, compact=True) for c in _five)}</div></section>
<section class="lpsec"><h2>Install</h2><div class="term">npx @kajisho5/kataui init<br>npx @kajisho5/kataui add button</div><p class="lpnote">Or copy from any component page.</p></section>
<section class="lpsec"><h2>Templates</h2><p class="lpnote">Try a <a href="/templates/dashboard/demo/">dashboard</a>, <a href="/templates/inbox/demo/">inbox</a> or <a href="/templates/settings-page/demo/">settings page</a>.</p></section>
<section class="lpsec"><h2>AI tools</h2><p class="lpnote">The <a href="/registry.json">registry</a>, <a href="/docs/mcp-server/">MCP server</a> and <a href="/skill/SKILL.md">AI skill</a> serve the files you copy here.</p><p class="lpnote">Works with any HTML stack; React needs <a href="/docs/react/">a few markup changes</a>.</p></section>
<section class="lpsec"><h2>Components are free. Pro adds layouts.</h2><p class="lpnote">{nb} blocks, {nt} templates, $129 once. Not on sale yet. <a href="/pricing/">Pricing</a></p></section>
<section class="lpsec"><p class="lpnote">More: <a href="/lab/">Lab</a> · <a href="/showcase/">Showcase</a> · <a href="/compare/">Comparison</a> · <a href="https://github.com/kajisho5/KATA-UI">Report a problem</a></p></section>
</div>{plain_footer()}</body></html>"""
    extra = ('<link rel="stylesheet" href="/blocks/app-shell/app-shell.css">'
             + ''.join(f'<link rel="stylesheet" href="/components/{sl}/{sl}.css?v={_v(pv[sl]["css"])}">' for sl in ('sidebar', 'select', 'bar-chart', 'calendar', 'sparkline', 'card', 'aurora', 'follow-frame', 'spotlight', 'beam-border', 'marquee', 'text-reveal', 'counter', 'glass-panel', 'converge', 'reorder', 'word-rotate', 'goo-tabs', 'dock', 'jelly-buttons', 'scramble', 'bounce-letters', 'tilt-card', 'line-chart', 'donut-chart', 'data-table', 'button', 'switch', 'input', 'badge', 'separator') if pv.get(sl)) + (f'<link rel="stylesheet" href="/blocks/stat-cards/stat-cards.css?v={_v(sc_block["css"])}">' if sc_block else '') + (f'<link rel="stylesheet" href="/blocks/kanban/kanban.css?v={_v(kb_block["css"])}">' if kb_block else '') + (f'<link rel="stylesheet" href="/blocks/faq/faq.css?v={_v(faq_b["css"])}">' if faq_b else '') + (f'<link rel="stylesheet" href="/blocks/pricing/pricing.css?v={_v(pr_block["css"])}">' if pr_block else ''))
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
    for item in items:
        kind = {'registry:component':'components','registry:block':'blocks','registry:page':'templates'}.get(item['type'])
        if kind:
            item['audit'] = MOLD_ITEMS[kind + '/' + item['name']]
            item['requiresMold']=requires_component(kind,item['name'],ROOT)
        for file in item['files']:
            file['content'] = distribution_header(file['path'], file['content'])
    return json.dumps({'$schema': 'https://ui.shadcn.com/schema/registry.json', 'name': 'kata-ui', 'version': RELEASE_VERSION,
                       'moldVersion': MOLD_CONFIG['moldVersion'], 'moldInstruction': version_line(ROOT), 'homepage': 'https://kata-ui.dev', 'audit': audit_metadata(MOLD_REPORT), 'items': items}, ensure_ascii=False, indent=1)

def llms_txt(comps, blocks, n_icons, templates=None):
    lines = ['# KATA UI', '', summary_block(MOLD_REPORT), '', version_line(ROOT), '',
             'Copy a button, form or table into your project. Edit the files yourself. No framework, no build step.', '',
             'KATA is framework-free: parts drop into plain HTML, Astro, Laravel, Django, Rails and templates unchanged. Components depend on tokens.css (design tokens) being loaded once.', '',
             '## Docs', '',
             '- [Design System](https://kata-ui.dev/design-system/): shared design tokens (tokens.json is downloadable there)',
             f'- [Icons](https://kata-ui.dev/icons/): {n_icons} icons on one mold (24 grid, 1.7 stroke, square caps); click to copy the SVG',
             '- [Registry](https://kata-ui.dev/registry.json): every component and block with its full CSS/JS/HTML, in the shadcn registry format',
             '- [Themes](https://kata-ui.dev/themes/): accent presets as small CSS files; a theme redefines the five accent tokens only. The page also offers 50 traditional Japanese colors (dentou) as click-to-cast accent sources',
             '- [Getting Started](https://kata-ui.dev/docs/getting-started/): load tokens.css once, then copy parts',
             '- [Skill for AI assistants](https://kata-ui.dev/skill/SKILL.md): a packaged SKILL.md that teaches an assistant to build with KATA correctly',
             '- [CLI](https://kata-ui.dev/docs/cli/): a zero-dependency Node script that installs parts from the registry — npx @kajisho5/kataui add button',
             '- [Installation](https://kata-ui.dev/docs/installation/): four ways in, plus per-stack guides for Plain HTML (https://kata-ui.dev/docs/install-html/), Astro (https://kata-ui.dev/docs/install-astro/) Laravel (https://kata-ui.dev/docs/install-laravel/) and React & Next.js (https://kata-ui.dev/docs/react/)',
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
    out = ['# KATA UI — full text', '', summary_block(MOLD_REPORT), '', version_line(ROOT), '',
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


CATALOG_SCRIPT = "<script>\nconst catq = document.getElementById('catq');\ncatq.addEventListener('input', () => {\n  const q = catq.value.trim().toLowerCase();\n  let any = false;\n  document.querySelectorAll('.catsec').forEach(sec => {\n    let vis = 0;\n    sec.querySelectorAll('.card').forEach(cd => { const hit = (!q || (cd.dataset.q || '').includes(q)) && (!window.__stf || window.__stf === 'all' || cd.dataset.status === window.__stf); cd.style.display = hit ? '' : 'none'; if (hit) vis++; });\n    sec.style.display = vis ? '' : 'none';\n    if (vis) any = true;\n  });\n  document.getElementById('catnone').style.display = any ? 'none' : '';\n});\nconst kburi = document.querySelector('.catsec.kburi');\nif (kburi && 'IntersectionObserver' in window) {\n  const io = new IntersectionObserver(es => es.forEach(e => {\n    if (e.isIntersecting) { kburi.classList.add('break'); setTimeout(() => kburi.classList.remove('break'), 900); io.disconnect(); }\n  }), { threshold: 0.35 });\n  io.observe(kburi);\n}\n</script>"


def components_index(comps):
    body = f"""
<div class="wrap">
  <div class="hero" style="padding-bottom:0">
    <h1 style="font-size:36px">Components</h1>
    <p>Every part is a folder in the registry — preview, CSS and JS are the same files you copy.</p>
  </div>
  <div class="catsearch"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.5-4.5"/></svg><input id="catq" type="text" placeholder="Filter parts — try \u201cchart\u201d, \u201cdate\u201d, \u201cmenu\u201d\u2026" aria-label="Filter components"></div>
  <div class="seg catstat" role="group" aria-label="Filter by status"><button type="button" data-st="all" class="on">All</button><button type="button" data-st="stable">Stable</button><button type="button" data-st="beta">Beta</button></div>
  <p class="catnone" id="catnone" style="display:none">No parts match that word. Try something shorter.</p>
{catalog_sections(comps)}
{CATALOG_SCRIPT}
<script>document.querySelectorAll('.catstat button').forEach(b => b.addEventListener('click', () => {{ window.__stf = b.dataset.st; document.querySelectorAll('.catstat button').forEach(x => x.classList.toggle('on', x === b)); document.getElementById('catq').dispatchEvent(new Event('input')); }})); {{ const st = new URLSearchParams(location.search).get('status'); const b = st && document.querySelector('.catstat button[data-st="' + st + '"]'); if (b) b.click(); }}</script>
</div>
{FOOTER}
</body>
</html>"""
    _cssv = _v(''.join(Path(p).read_text(encoding='utf-8') for p in sorted(glob.glob(str(ROOT / 'components' / '*' / '*.css')) + glob.glob(str(ROOT / 'blocks' / '*' / '*.css')) + glob.glob(str(ROOT / 'templates' / '*' / '*.css')) + glob.glob(str(ROOT / 'tokens.css')))))
    _jsv = _v(''.join(Path(p).read_text(encoding='utf-8') for p in sorted(glob.glob(str(ROOT / 'components' / '*' / '*.js')) + glob.glob(str(ROOT / 'blocks' / '*' / '*.js')) + glob.glob(str(ROOT / 'templates' / '*' / '*.js')))))
    return head('Components — KATA UI', 'All KATA UI components.', '<link rel="stylesheet" href="/kata-ui.css?v=' + _cssv + '">') + body.replace('</body>', '<script src="/kata-ui.js?v=' + _jsv + '" defer></script></body>', 1)

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
    gs = ['introduction', 'getting-started', 'installation', 'install-html', 'install-astro', 'install-laravel', 'react', 'cli', 'registry', 'mcp', 'theming', 'dark-mode', 'accessibility', 'rtl', 'changelog']
    concepts = ['why-vanilla', 'the-mold', 'contributing', 'anatomy', 'forms', 'from-tailwind', 'vs-shadcn', 'ai-prompts']
    guides = [d[0] for d in DOCS if d[0].startswith('guide-')]
    doc = lambda slugs: ''.join(_nav_link('/docs/' + x + '/', _doc_title(x), current) for x in slugs)
    secs = [
        _sec('Getting Started', doc(gs)),
        _sec('Concepts', doc(concepts)),
        _sec('Guides', doc(guides)),
        sidebar(comps, active),
        _sec('Blocks', ''.join(_nav_link('/blocks/' + b['slug'] + '/', b['meta']['title'], current) for b in _all_blocks())),
        _sec('Templates', ''.join(_nav_link('/templates/' + t['slug'] + '/', t['meta']['title'], current) for t in load_templates())),
        _sec('Resources', ''.join(_nav_link(u, n, current) for u, n in [('/icons/', 'Icons'), ('/themes/', 'Themes'), ('/design-system/', 'Design System'), ('/pricing/', 'Pricing'), ('/skill/SKILL.md', 'AI Skill (SKILL.md)')])),
    ]
    if secs:
        secs[0] = secs[0].replace('class="side"', 'class="side sfirst"', 1)
    return secs


def nav_tree(comps, active, current):
    return '<div class="sidenav">' + ''.join(tree_sections(comps, active, current)) + '</div>'


DETAIL_JS = """<script>
  const stage = document.getElementById('stage');
  if (stage && window.matchMedia('(max-width: 719px)').matches) {
    stage.classList.add('narrow');
    document.querySelectorAll('[data-seg="width"] button').forEach(b => b.classList.toggle('on', b.dataset.v === 'mobile'));
  }
  document.querySelectorAll('[data-seg]').forEach(seg => {
    seg.querySelectorAll('button').forEach(btn => btn.addEventListener('click', () => {
      seg.querySelectorAll('button').forEach(b => b.classList.remove('on'));
      btn.classList.add('on');
      const v = btn.dataset.v;
      if (seg.dataset.seg === 'theme') { stage.setAttribute('data-theme', v); }
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
    btn.classList.remove('flash'); void btn.offsetWidth; btn.classList.add('flash');
    setTimeout(() => btn.textContent = 'Copy', 1600);
  }));
  document.querySelectorAll('[data-aiprompt]').forEach(btn => btn.addEventListener('click', () => {
    const txt = 'Add the KATA UI "' + btn.dataset.title + '" component to my project. Its files are in the registry at https://kata-ui.dev/registry.json (slug: ' + btn.dataset.aiprompt + '); the part page is https://kata-ui.dev/components/' + btn.dataset.aiprompt + '/ — take the HTML, CSS and JS from there, load tokens.css first, and keep the part unmodified: adjust tokens and leave the part as shipped.';
    if (navigator.clipboard) navigator.clipboard.writeText(txt);
    const old = btn.textContent; btn.textContent = 'Copied — paste it to your AI';
    btn.classList.remove('flash'); void btn.offsetWidth; btn.classList.add('flash');
    setTimeout(() => btn.textContent = old, 1800);
  }));
  document.querySelectorAll('[data-tok]').forEach(chip => {
    const name = chip.dataset.tok;
    const val = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    const slot = chip.querySelector('.tokval');
    if (slot && val) slot.textContent = val;
    chip.addEventListener('click', () => {
      if (navigator.clipboard) navigator.clipboard.writeText(name);
      chip.classList.remove('flash'); void chip.offsetWidth; chip.classList.add('flash');
    });
  });
  const calmBtn = document.getElementById('st-calm');
  if (calmBtn) calmBtn.addEventListener('click', () => {
    const st = document.getElementById('stage');
    const on = st.classList.toggle('calm');
    calmBtn.classList.toggle('on', on);
  });
  const focBtn = document.getElementById('st-focus');
  if (focBtn) focBtn.addEventListener('click', () => {
    const st = document.getElementById('stage');
    const el = st.querySelector('a[href], button, input, select, textarea, [tabindex]');
    if (el) el.focus();
  });
</script>"""

JA_DOCS = ['button', 'input', 'field', 'textarea', 'select', 'checkbox', 'radio', 'switch', 'modal', 'dropdown']
JA_CATEGORY = {'Form & Input': 'フォームと入力', 'Overlays & Dialogs': '重なる表示とダイアログ',
               'Layout & Navigation': 'レイアウトと移動', 'Feedback & Status': 'お知らせと状態', 'Display & Media': '表示とメディア'}
JA_STATUS = {'stable': 'stable', 'beta': 'beta'}
JA_DOC_STYLE = """<style>
html[lang="ja"] .detail{line-height:1.8}
.ja-nav{margin-bottom:22px}
.ja-nav .h{font-size:11px;font-weight:650;letter-spacing:.14em;color:var(--ink);margin:0 0 8px;padding-inline:10px}
.ja-nav a{display:flex;gap:8px;padding:5px 10px;border-radius:6px;font-size:13px;color:var(--ink2);text-decoration:none}
.ja-nav a span{color:var(--ink3)}
.ja-nav a[aria-current="page"]{background:var(--hair);color:var(--ink);font-weight:600}
.ja-nav a:focus-visible{outline:2px solid var(--ink);outline-offset:2px}
.ja-title .ja-en:focus-visible{outline:2px solid var(--ink);outline-offset:2px}
.ja-title{display:flex;flex-wrap:wrap;align-items:center;gap:10px}
.ja-title .ja-name{font-size:17px;font-weight:500;color:var(--ink2)}
.ja-title .ja-en{margin-inline-start:auto;font-size:13px;border:1px solid var(--hair);border-radius:8px;padding:5px 12px;text-decoration:none;color:var(--ink)}
.ja-keys{border-collapse:collapse;margin-top:10px;font-size:14px;min-width:min(100%,520px)}
.ja-keys th,.ja-keys td{text-align:start;padding:8px 14px;border-block-end:1px solid var(--hair)}
.ja-keys th{font-size:12.5px;color:var(--ink2);font-weight:600}
.ja-only{border:1px solid var(--hair);border-radius:12px;padding:14px 18px;background:var(--paper)}
.ja-src{margin-top:28px;padding-top:14px;border-top:1px solid var(--hair);font-size:12.5px;color:var(--ink3)}
</style>"""


def ja_docs():
    """Japanese copy for the parts in JA_DOCS, read from ja/components/<slug>.json."""
    out = {}
    for slug in JA_DOCS:
        path = ROOT / 'ja' / 'components' / f'{slug}.json'
        if path.exists():
            out[slug] = json.loads(path.read_text(encoding='utf-8'))
    return out


def ja_nav(docs, by_slug, current):
    CURRENT = ' aria-current="page"'
    links = ''.join(
        f'<a href="/ja/components/{sl}/"{CURRENT if sl == current else ""}>{esc(by_slug[sl]["meta"]["title"])}<span>{esc(docs[sl]["name_ja"])}</span></a>'
        for sl in JA_DOCS if sl in docs and sl in by_slug)
    return f'<nav class="ja-nav" aria-label="日本語ドキュメント"><p class="h">日本語ドキュメント</p>{links}</nav>'


def ja_detail(comps, idx, docs):
    """Japanese page for one part: same preview and code as detail(), translated prose."""
    c = comps[idx]
    m = c['meta']
    slug = c['slug']
    ja = docs[slug]
    by_slug = {x['slug']: x for x in comps}
    display_html = re.sub(r'\s*<link rel="stylesheet"[^>]*>', '', c['preview']).strip()
    tabs = [('HTML', display_html), ('CSS', c['css'])] + ([('JS', c['js'])] if c['js'] else [])
    on = ' class="on"'
    tab_btns = ''.join(f'<button data-tab="{name}"{on if i == 0 else ""}>{name}</button>' for i, (name, _) in enumerate(tabs))
    panes = ''.join(
        f'<div class="pane{" on" if i == 0 else ""}" data-pane="{name}"><pre>{esc(code)}</pre><div class="copyrow"><button class="copybtn">コピー</button></div></div>'
        for i, (name, code) in enumerate(tabs))
    stage_cls = 'stage col' if m.get('stage') == 'col' else 'stage'
    js_tag = f'<script src="/components/{slug}/{slug}.js?v={_v(c["js"])}"></script>' if c['js'] else ''
    js_step = ' この部品にはスクリプトがあります。HTML のあとで読み込むと、自分で動き始めます。' if c['js'] else ''
    deps = ''
    if c['deps']:
        names = '、'.join(f'<a href="/components/{d}/">{esc(by_slug[d]["meta"]["title"])}</a>' for d in c['deps'] if d in by_slug)
        deps = f'<p class="deps">この部品は {names} も使います。その CSS も一緒に読み込んでください。</p>'
    keys = ''.join(f'<tr><td><kbd>{esc(k)}</kbd></td><td>{esc(v)}</td></tr>' for k, v in ja.get('keys', []))
    keys_html = f'<table class="ja-keys"><thead><tr><th scope="col">キー</th><th scope="col">動き</th></tr></thead><tbody>{keys}</tbody></table>' if keys else ''
    status = m.get('status', 'stable')
    body = f"""
<div class="wrap dc">
  <div class="layout">
    <div class="sidenav">{ja_nav(docs, by_slug, slug)}{''.join(tree_sections(comps, slug, '/ja/components/' + slug + '/'))}</div>
    <main class="detail" lang="ja">
      <p class="crumb"><a href="/ja/">日本語ドキュメント</a> / {esc(JA_CATEGORY.get(m['category'], m['category']))} / {esc(m['title'])}</p>
      <div class="ja-title"><h1>{esc(m['title'])}</h1><span class="ja-name">{esc(ja['name_ja'])}</span><span class="st st-{esc(status)}">{esc(status)}</span><a class="ja-en" href="/components/{slug}/" hreflang="en" lang="en">English →</a></div>
      <p class="desc">{esc(ja['description'])}</p>
      <div class="stagebar">
        <span class="lbl">見本</span>
        <span class="seg" data-seg="width"><button data-v="desktop" class="on">Desktop</button><button data-v="mobile">Mobile</button></span>
        <span class="seg" data-seg="theme"><button data-v="light" class="on">Light</button><button data-v="dark">Dark</button></span>
      </div>
      <div class="dcols"><div class="dcol-l">
      <div class="{stage_cls}" id="stage" lang="en">
{c['preview']}
      </div>
      {deps}
      </div><div class="dcol-r">
      <div class="codebox" lang="en"><div class="codetabs">{tab_btns}</div>{panes}</div>
      </div></div>
      <section class="doc"><h2>導入</h2>
        <div class="codebox"><div class="pane on"><pre lang="en">npx @kajisho5/kataui add {slug}</pre><div class="copyrow"><button class="copybtn">コピー</button></div></div></div>
        <p class="anote">手動で入れる場合：</p>
        <ol class="instol">
          <li><code>tokens.css</code> をページで一度だけ読み込む</li>
          <li>CSS タブの中身を、自分のスタイルシートに貼る</li>
          <li>HTML タブの中身を、使いたい場所に貼る。{js_step}</li>
        </ol></section>
      <section class="doc"><h2>使いどころ</h2><p>{esc(ja['usage'])}</p></section>
      <section class="doc"><h2>アクセシビリティ</h2><p>{esc(ja['a11y'])}</p>{keys_html}</section>
      <section class="doc"><h2>英語版にだけある情報</h2><div class="ja-only"><p>静的チェックの結果・部品の構造（Anatomy）・読むトークン・使い方の例・関連する部品</p><p><a href="/components/{slug}/" hreflang="en">英語版の {esc(m['title'])} ページで見る →</a></p></div></section>
      <p class="ja-src">この訳は、英語版の {esc(ja['source']['date'])} の内容をもとにしています。英語版の文が変わると、テストで知らせます。</p>
    </main>
  </div>
</div>
{FOOTER}
{js_tag}
{DETAIL_JS}
</body>
</html>"""
    extra = JA_DOC_STYLE + f'<link rel="stylesheet" href="/components/{slug}/{slug}.css?v={_v(c["css"])}">' + ''.join(
        f'<link rel="stylesheet" href="/components/{d}/{d}.css?v={_v(by_slug[d]["css"])}">' for d in c['deps'] if d in by_slug)
    page = head(f"{m['title']}（{ja['name_ja']}）— KATA UI 日本語ドキュメント", ja['description'], extra) + body
    return page.replace('<html lang="en">', '<html lang="ja">', 1)


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
      <div class="codebox"><div class="pane on"><pre>npx @kajisho5/kataui add {slug}</pre><div class="copyrow"><button class="copybtn">Copy</button></div></div></div>
      <p class="anote">Writes the part\u2019s CSS{(' and JS' if c['js'] else '')} into your project.{dep_cli} New to the CLI? See the <a href="/docs/cli/">CLI doc</a>.</p>
      <h3 class="insth">Manual</h3>
      <ol class="instol">
        <li>Load <code>tokens.css</code> once, before any part.</li>
        <li>Copy the CSS tab into your stylesheet.</li>
        <li>Copy the HTML where it belongs.{js_step}</li>
      </ol></section>'''
    cls_seen, hooks = css_surface(c['css'])
    for src in (c['preview'], c['js'] or ''):
        for mm in re.finditer(r'data-[a-z0-9-]+', src):
            if mm.group(0) not in hooks:
                hooks.append(mm.group(0))
    arias = aria_surface(c['preview'])
    rows = ''
    for n in cls_seen[:14]:
        rows += f'<tr><td><code>.{esc(n)}</code></td><td>class</td></tr>'
    if len(cls_seen) > 14:
        rows += f'<tr><td><code>+{len(cls_seen) - 14} more</code></td><td>classes \u2014 see the CSS tab</td></tr>'
    for h in hooks:
        rows += f'<tr><td><code>{esc(h)}</code></td><td>data hook</td></tr>'
    for a in arias[:8]:
        rows += f'<tr><td><code>{esc(a)}</code></td><td>ARIA</td></tr>'
    anatomy_html = ''
    if rows:
        anatomy_html = ('<section class="doc"><h2>Anatomy</h2>'
                        '<p class="anote">The public surface of this part, read from its own source. Class names are the API \u2014 the CSS tab above is the full contract.</p>'
                        f'<table class="anatomy"><tbody>{rows}</tbody></table></section>')
    toks_used = []
    for mm in re.finditer(r'var\(--(k-[a-z0-9-]+)\)', c['css']):
        if mm.group(1) not in toks_used:
            toks_used.append(mm.group(1))
    token_html = ''
    if toks_used:
        chips = ''.join(f'<button class="tokchip" type="button" data-tok="--{esc(tk)}" title="Copy the token name">--{esc(tk)}<span class="tokval"></span></button>' for tk in toks_used)
        token_html = ('<section class="doc"><h2>Tokens it reads</h2>'
                      '<p class="anote">The decomposition view: every custom property this part\u2019s CSS actually reads, with its live value on this page right now. '
                      'Change one in the Foundry deck and the value \u2014 and the part \u2014 moves. Click a token to copy its name.</p>'
                      f'<div class="tokrow">{chips}</div></section>')
    siblings = [x for x in comps if x['meta']['category'] == m['category'] and x['slug'] != slug][:4]
    related = ''
    if siblings:
        related = '<section class="doc"><h2>Related parts</h2><div class="cards">' + ''.join(card(x) for x in siblings) + '</div></section>'
    used_in_blocks = [b for b in _all_blocks() if slug in b['meta'].get('uses', [])]
    used_in = ''
    if used_in_blocks:
        links = ''.join(f'<a class="card" href="/blocks/{b["slug"]}/"><h3>{esc(b["meta"]["title"])}</h3><p>{esc(b["meta"]["description"])}</p></a>' for b in used_in_blocks)
        used_in = f'<section class="doc"><h2>Used in these blocks</h2><div class="cards">{links}</div></section>'
    _co = {}
    for _b in used_in_blocks:
        for _u in _b['meta'].get('uses', []):
            if _u != slug:
                _co[_u] = _co.get(_u, 0) + 1
    cast_with = ''
    if _co:
        _top = [next((c for c in comps if c['slug'] == _s), None) for _s, _n in sorted(_co.items(), key=lambda kv: -kv[1])[:4]]
        _top = [c for c in _top if c]
        if _top:
            cast_with = '<section class="doc"><h2>Often cast with</h2><div class="cards">' + ''.join(card(x) for x in _top) + '</div></section>'
    combos_html = ''
    combo_css = ''
    combo_js = ''
    if c.get('combos'):
        by2 = {x['slug']: x for x in comps}
        out = []
        _union = []
        for title, note, cparts, html_c in c['combos']:
            for _p in cparts:
                if _p not in _union and _p != slug:
                    _union.append(_p)
            plinks = ', '.join(f'<a href="/components/{_p}/">{esc(by2[_p]["meta"]["title"])}</a>' for _p in cparts if _p in by2)
            out.append(f'<h3 class="exh">{esc(title)}</h3>' + (f'<p class="anote">{esc(note)}</p>' if note else '') + f'<div class="stage col exstage">{html_c}</div><div class="codebox"><div class="pane on"><pre>{esc(html_c)}</pre><div class="copyrow"><button class="copybtn">Copy</button></div></div></div>' + (f'<p class="deps">Parts in this scene: {plinks} \u2014 each brings its own CSS, named on its page.</p>' if plinks else ''))
        combos_html = '<section class="doc"><h2>Cast together</h2><p class="anote">Compositions: this part at work with others, running live on this page. Copy the whole scene \u2014 the mold is what makes the pieces agree.</p>' + ''.join(out) + '</section>'
        for _p in _union:
            if _p in by2:
                combo_css += f'<link rel="stylesheet" href="/components/{_p}/{_p}.css?v={_v(by2[_p]["css"])}">'
                if by2[_p]['js']:
                    combo_js += f'<script src="/components/{_p}/{_p}.js?v={_v(by2[_p]["js"])}"></script>'
    body = f"""
<div class="wrap dc">
  <div class="layout">
    {nav_tree(comps, slug, '/components/' + slug + '/')}
    <main class="detail">
      <p class="crumb"><a href="/components/">Components</a> / {esc(m['category'])} / {esc(m['title'])}</p>
      <h1>{esc(m['title'])} <span class="st st-{esc(m.get('status','stable'))}">{esc(m.get('status','stable'))}</span>{f' <a class="ja-link" href="/ja/components/{slug}/" hreflang="ja" lang="ja">日本語</a>' if (ROOT / 'ja' / 'components' / (slug + '.json')).exists() else ''}</h1>
      <div class="vrow"><span class="vchip"><i></i>{'Mold Verified — passed' if MOLD_ITEMS['components/' + slug]['passed'] else 'Mold check — failed'}</span><button class="aibtn" type="button" data-aiprompt="{slug}" data-title="{esc(m['title'])}">Pass this part to your AI</button></div>
      <p class="desc">{esc(m['description'])}</p>{'<p class="expnote">From the experimental line \u2014 a showpiece. The production shelf carries the same mold without the performance.</p>' if m.get('category') in ('Motion', 'KATAYABURI') else ''}
      <div class="stagebar">
        <span class="lbl">Preview</span>
        <span class="seg" data-seg="width"><button data-v="desktop" class="on">Desktop</button><button data-v="mobile">Mobile</button></span>
        <span class="seg" data-seg="theme"><button data-v="light" class="on">Light</button><button data-v="dark">Dark</button></span>
        <span class="segx"><button type="button" id="st-calm">Calm</button><button type="button" id="st-focus">Focus first control</button></span>
      </div>
      <div class="dcols"><div class="dcol-l">
      <div class="{stage_cls}" id="stage">
{c['preview']}
      </div>
      {deps_html}
      </div><div class="dcol-r">
      <div class="codebox">
        <div class="codetabs">{tab_btns}</div>
        {panes}
      </div>
      </div></div>
      {render_checks(MOLD_ITEMS['components/' + slug])}
    {install_html}
      {examples_html}
      <section class="doc"><h2>Usage</h2>{render_usage(m.get('usage',''))}</section>
      <section class="doc"><h2>Accessibility</h2><p>{esc(m.get('a11y',''))}</p></section>
      {anatomy_html}
      {token_html}
      {used_in}
      {cast_with}
      {combos_html}
      {related}
      <div class="prevnext">{prev_html}{next_html}</div>
    </main>
  </div>
</div>
{FOOTER}
{js_tag}
{combo_js}
{DETAIL_JS}
</body>
</html>"""
    extra = f'<link rel="stylesheet" href="/components/{slug}/{slug}.css?v={_v(c["css"])}">'
    return head(f"{m['title']} — KATA UI", m['description'], extra + combo_css) + body


DS_STYLE = """<style>
.ds h1{font-size:32px;font-weight:600;letter-spacing:-.025em;margin-top:26px}
.ds .lead{margin-top:10px;color:var(--ink2);font-size:15px;line-height:1.85;max-width:64ch;letter-spacing:.012em}
.ds section{margin-top:46px}
.ds h2{font-size:19px;font-weight:600;letter-spacing:-.015em}
.ds .note{margin-top:7px;color:var(--ink2);font-size:13.5px;line-height:1.8;max-width:66ch;letter-spacing:.012em}
.swatches{margin-top:16px;display:grid;grid-template-columns:repeat(auto-fill,minmax(96px,1fr));gap:9px}
.sw{border:1px solid var(--hair);border-radius:10px;overflow:hidden;background:var(--paper)}
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
.motions .m{flex:1;min-width:150px;border:1px solid var(--hair);border-radius:12px;padding:14px;background:var(--paper);font-size:12.5px;color:var(--ink2)}
.motions .dot{width:16px;height:16px;border-radius:50%;background:var(--ink);margin-top:10px;transition:transform var(--dur) var(--k-ease)}
.motions .m:hover .dot{transform:translateX(56px)}
.dl{margin-top:16px;display:flex;gap:9px;flex-wrap:wrap}
.dl a{border:1px solid var(--hair);border-radius:8px;padding:9px 14px;font-size:13px;font-weight:500;text-decoration:none;background:var(--paper)}
.dl a:hover{background:var(--soft)}
</style>"""


ICONS_STYLE = """<style>
.ic h1{font-size:32px;font-weight:600;letter-spacing:-.025em;margin-top:26px}
.ic .lead{margin-top:10px;color:var(--ink2);font-size:15px;line-height:1.85;max-width:64ch;letter-spacing:.012em}
.icgrid{margin-top:26px;display:grid;grid-template-columns:repeat(auto-fill,minmax(104px,1fr));gap:9px}
.iccell{border:1px solid var(--hair);border-radius:12px;background:var(--paper);padding:16px 6px 11px;display:grid;justify-items:center;gap:9px;cursor:pointer;font:inherit;color:var(--ink)}
.iccell:hover{border-color:var(--ink3)}
.iccell .nm{font-family:var(--mono);font-size:10.5px;color:var(--ink2)}
.icstat{margin-top:14px;font-size:13px;color:var(--ink2);min-height:20px}
.icstat b{color:var(--acc);font-weight:600}
</style>"""

BRAND_GENRES = [
    ('Social & messaging', ['x', 'instagram', 'facebook', 'threads', 'tiktok', 'linkedin', 'slack', 'discord', 'telegram', 'whatsapp', 'line', 'messenger', 'reddit', 'bluesky', 'meta', 'pinterest', 'snapchat', 'signal', 'wechat', 'kakaotalk']),
    ('Video & audio', ['youtube', 'twitch', 'netflix', 'spotify', 'soundcloud', 'vimeo', 'niconico', 'pixiv', 'applemusic', 'youtubemusic']),
    ('AI', ['claude', 'gemini', 'openai', 'perplexity', 'mistral', 'anthropic', 'huggingface', 'ollama']),
    ('Development', ['github', 'gitlab', 'bitbucket', 'stackoverflow', 'codepen', 'docker', 'npm', 'git', 'vscode', 'jetbrains', 'vim', 'neovim', 'sublimetext', 'codesandbox', 'replit', 'postman', 'insomnia', 'graphql', 'prisma', 'appwrite', 'jenkins', 'circleci', 'githubactions']),
    ('Languages & runtimes', ['typescript', 'javascript', 'python', 'go', 'rust', 'ruby', 'php', 'swift', 'kotlin', 'dart', 'elixir', 'zig', 'r', 'lua', 'html5', 'css', 'deno', 'bun', 'nodejs']),
    ('Frameworks & site tools', ['react', 'vue', 'tailwind', 'wordpress', 'figma', 'notion', 'framer', 'linear', 'nextjs', 'nuxt', 'svelte', 'astro', 'angular', 'ember', 'jquery', 'threejs', 'vite', 'webpack', 'babel', 'eslint', 'prettier', 'storybook', 'gatsby', 'laravel', 'django', 'flask', 'rubyonrails', 'spring', 'dotnet', 'electron', 'tauri', 'flutter', 'ionic', 'expo', 'webflow', 'squarespace', 'wix', 'ghost']),
    ('Data & backend', ['postgresql', 'mysql', 'mongodb', 'redis', 'sqlite', 'mariadb', 'elasticsearch', 'kafka', 'rabbitmq', 'nginx', 'apache', 'planetscale', 'neon', 'clickhouse', 'snowflake']),
    ('Commerce & payments', ['shopify', 'stripe', 'paypal', 'mastercard', 'visa', 'americanexpress', 'applepay', 'googlepay', 'klarna', 'square', 'woocommerce', 'magento', 'gumroad', 'lemonsqueezy', 'paddle']),
    ('Platforms & browsers', ['apple', 'google', 'microsoft', 'android', 'chrome', 'safari', 'firefox', 'opera', 'brave', 'vivaldi', 'tor', 'ubuntu', 'debian', 'linux', 'raspberrypi']),
    ('Cloud & hosting', ['vercel', 'netlify', 'cloudflare', 'supabase', 'firebase', 'aws', 'googlecloud', 'azure', 'digitalocean', 'linode', 'vultr', 'heroku', 'render', 'railway', 'flyio', 'fastly', 'oracle', 'ibm', 'hetzner', 'cloudinary']),
    ('Productivity & SaaS', ['gmail', 'googledrive', 'dropbox', 'box', 'evernote', 'todoist', 'asana', 'trello', 'jira', 'confluence', 'miro', 'airtable', 'zapier', 'ifttt', 'hubspot', 'salesforce', 'mailchimp', 'sendgrid', 'twilio', 'intercom', 'zendesk', 'calendly', 'typeform', 'medium', 'substack', 'patreon', 'kofi']),
    ('Games & 3D', ['playstation', 'xbox', 'nintendo', 'steam', 'epicgames', 'itchio', 'unity', 'unrealengine', 'godot', 'blender']),
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
            gcells = ''.join(bmap[m] for m in members if m in bmap)
            for m in members:
                if m in bmap:
                    used.add(m)
            if gcells:
                groups.append('<h3 style="font-size:15px;font-weight:600;letter-spacing:-.01em;margin:28px 0 0">' + gname + '</h3><div class="icgrid" style="margin-top:12px">' + gcells + '</div>')
        rest = ''.join(bmap[k] for k in sorted(bmap) if k not in used)
        if rest:
            groups.append('<h3 style="font-size:15px;font-weight:600;letter-spacing:-.01em;margin:28px 0 0">More marks</h3><div class="icgrid" style="margin-top:12px">' + rest + '</div>')
        brand_section = ('<h2 style="font-size:21px;font-weight:600;letter-spacing:-.02em;margin-top:38px">Brand marks</h2>'
          '<p style="margin-top:8px;color:var(--ink2);font-size:13.5px;line-height:1.8;max-width:64ch;letter-spacing:.012em">' + str(len(bmap)) + ' marks, grouped by the job they do on a site: social links, sign-in buttons, integration grids, logo clouds. Brand marks belong to their owners and are here for nominative use only — using one does not imply endorsement, and they are never part of the KATA identity. They are also the one exception to the three-shape mold: a mark keeps its owner’s geometry.</p>'
          + ''.join(groups))
    guidenote = ('<div class="guidenote"><h3>Using the brand marks</h3>'
      '<p>Each mark belongs to its owner and is included so a part can name the service it connects to. Use a mark to refer to that service, and only that: do not recolor it into your own logo, do not place it where it implies the owner endorses your product, and follow the owner brand terms where they publish them. When in doubt, link with text instead.</p></div>') if brand_section else ''
    script = "<script>var ICONS=__DATA__;\ndocument.querySelectorAll('[data-icon]').forEach(function(b){b.addEventListener('click',function(){var n=b.dataset.icon;var done=function(){document.getElementById('icstat').innerHTML='<b>'+n+'</b> copied.';};if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(ICONS[n]).then(done,done);}else{done();}});});\n</script>".replace('__DATA__', _json.dumps(data))
    body = "\n<div class=\"wrap ic\">\n  <h1>Icons</h1>\n  <p class=\"lead\">One mold for icons, too: a 24 grid, a 1.7 stroke, square caps and bevel joins — a sharper cut than the usual round line icon. Every glyph is drawn from three shapes only — the circle, the 45° line, and the r2 corner — so the whole set reads as cut from one block. A few carry the KATA signature: a solid core at the center — the same vermillion that sits inside the Switch and the Radio. Click any icon to copy its SVG. For anything beyond this set, Lucide is the nearest kin (24 grid, round) and sits comfortably alongside.</p>\n  <p class=\"icstat\" id=\"icstat\">" + str(len(files)) + " icons. Every one is a single file in the registry.</p>\n  <div class=\"icgrid\">" + ''.join(cells) + "</div>" + brand_section + guidenote + "\n</div>\n" + FOOTER + "\n" + script + "\n</body>\n</html>"
    return head('Icons — KATA UI', 'The KATA icon set: 24 grid, 1.7 stroke, square caps, click to copy the SVG.', ICONS_STYLE) + body



PRICING_STYLE = """<style>
.inventory{margin-top:44px}
.inventory h2{font-size:20px;font-weight:650;letter-spacing:-.015em}
.inventory .rs{font-size:13.5px;color:var(--ink2);margin-top:8px;max-width:660px;line-height:1.7}
.invgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(168px,1fr));gap:10px;margin-top:18px}
.inv{border:1px solid var(--hair);border-radius:10px;padding:12px 14px;text-decoration:none;color:inherit;display:block;background:var(--paper)}
.inv b{font-size:13.5px;display:block;font-weight:600}
.inv span{font-size:11.5px;color:var(--ink3)}
.founding{margin-top:36px;border:1px solid var(--ink);border-radius:16px;padding:24px 26px;background:var(--paper)}
.founding h2{font-size:18px;font-weight:650}
.founding p{font-size:14px;color:var(--ink2);line-height:1.8;margin-top:8px;max-width:700px}
.afterbuy{margin-top:36px}
.afterbuy h2{font-size:18px;font-weight:650}
.ab-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:16px}
.ab-grid>div{border:1px solid var(--hair);border-radius:13px;padding:18px;background:var(--paper)}
.ab-grid .no{font-size:11px;font-weight:650;letter-spacing:.1em;color:var(--acc)}
.ab-grid h3{font-size:14.5px;margin:7px 0 5px}
.ab-grid p{font-size:13px;line-height:1.75;color:var(--ink2)}
@media (max-width:720px){.ab-grid{grid-template-columns:1fr}}
.rateband{margin-top:36px;border-top:1px solid var(--hair);padding-top:26px}
.rateband h3{font-size:16px;font-weight:620}
.rateband .rs{font-size:13px;color:var(--ink2);margin-top:6px;max-width:660px;line-height:1.7}
.rrow{display:grid;grid-template-columns:92px 1fr 84px;gap:12px;align-items:center;margin-top:12px;font-size:13px}
.rrow .rl{color:var(--ink2)}
.rrow .rv{text-align:right;font-weight:620;font-variant-numeric:tabular-nums}
.rtrack{height:14px;background:var(--soft);border-radius:4px;overflow:hidden}
.rbar{height:100%;background:#a1a1aa;border-radius:4px}
.rbar.pro{background:#eb471f}
.pr .tiers{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:30px}
.pr .tier{border:1px solid var(--hair);border-radius:16px;padding:26px;background:var(--paper)}
.pr .tier.pro{border-color:var(--ink);box-shadow:0 24px 50px -30px rgba(16,24,40,.35)}
.pr .tier h2{font-size:19px;display:flex;align-items:baseline;gap:10px}
.pr .price{font-size:34px;font-weight:700;letter-spacing:-.03em;margin:12px 0 2px}
.pr .per{color:var(--ink3);font-size:13px}
.pr .tier ul{list-style:none;margin:18px 0 0;padding:0;display:grid;gap:9px}
.pr .tier li{font-size:13.5px;color:var(--ink2);display:flex;gap:9px;line-height:1.6;letter-spacing:.012em}
.pr .tier li::before{content:"";flex:none;width:7px;height:7px;border-radius:50%;background:var(--ink);margin-top:7px}
.pr .tier.pro li::before{background:#eb471f}
.pr .cta{display:inline-flex;margin-top:22px;padding:10px 18px;border-radius:9px;background:var(--ink);color:var(--paper);font-weight:550;font-size:14px;text-decoration:none}
.pr .cta.ghost{background:var(--paper);color:var(--ink2);border:1px solid var(--hair);cursor:default}
.pr .note{margin-top:14px;font-size:12.5px;color:var(--ink3);line-height:1.7;letter-spacing:.01em}
.pr .qa{margin-top:44px;display:grid;gap:0}
.pr .qa div{border-top:1px solid var(--hair);padding:18px 2px}
.pr .qa h3{font-size:15px;margin-bottom:6px}
.pr .qa p{font-size:13.5px;color:var(--ink2);line-height:1.8;max-width:640px;letter-spacing:.012em}
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
  <p class="wl-done" hidden>{done}<span class="wl-stamp" aria-hidden="true">\u578b</span></p>
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

def inventory_html():
    cards = []
    for b in load_blocks():
        cards.append('<a class="inv" href="/blocks/' + b['slug'] + '/"><b>' + esc(b['meta']['title']) + '</b><span>Block \u00b7 ' + str(len(b['meta'].get('uses', []))) + (' part' if len(b['meta'].get('uses', [])) == 1 else ' parts') + '</span></a>')
    for t in load_templates():
        cards.append('<a class="inv" href="/templates/' + t['slug'] + '/"><b>' + esc(t['meta']['title']) + '</b><span>Template \u00b7 ' + str(len(t['meta'].get('uses', [])) + len(t['meta'].get('blocks', []))) + ' parts &amp; blocks</span></a>')
    return ''.join(cards)


def pricing_page():
    body = """
<div class="wrap pr"><h1>Pricing</h1>
<p class="lead">Components are free under MIT. Pro will bundle the blocks and templates for a one-time payment.</p>
<div class="tiers"><div class="tier"><h2>Free</h2><p class="price">$0</p><p class="per">MIT license. No account required.</p><ul><li>136 HTML, CSS and JavaScript components</li><li>150 icons and 220 brand marks</li><li>Themes and design tokens</li><li>CLI, registry, MCP server and AI skill</li><li>Documentation and examples</li></ul><a class="cta" href="/components/">Browse components</a></div>
<div class="tier pro"><h2>Pro</h2><p class="price">$129</p><p class="per">Planned price. One payment for lifetime access.</p><ul><li>21 blocks and 7 templates</li><li>Future blocks and templates included</li><li>Unlimited projects and seats</li></ul><p>Sales have not opened. Blocks and templates are currently available on this site.</p>__WAITLIST__</div></div>
<div class="inventory"><h2>Blocks and templates</h2><p class="rs">Open an item to see its preview, source and component list.</p><div class="invgrid">__INVENTORY__</div></div>
<div class="valueband"><h2>What you're paying for</h2><p>Pro groups components into page sections and complete layouts, with their styles and responsive structure.</p><p class="note">Our assembly estimate is 77 hours (21 blocks × 2 hours + 7 templates × 5 hours); $129 is about $1.68 per estimated hour. Your time will vary.</p></div>
<div class="founding"><h2>First 100 licenses</h2><p>The launch offer is $99 for the first 100 licenses, including Help Center and Job Board blocks and priority support. Join the list for the launch email.</p></div>
<div class="qa"><div><h3>Why charge for blocks?</h3><p>Components handle individual controls. Blocks and templates save you the work of arranging them into layouts. The component source stays free.</p></div><div><h3>What happens to code I've copied?</h3><p>You keep it under the license supplied with it. A later pricing change does not change that license.</p></div><div><h3>What still needs work?</h3><p>See the <a href="/mold-results.json">current check results</a> and each component's status. Test the components you use with your content and supported browsers.</p></div></div>
</div>""" + plain_footer() + "</body></html>"
    return (head('Pricing — KATA UI', 'Free MIT components. Pro blocks and templates: planned price $129 once.', PRICING_STYLE) + body).replace('__WAITLIST__', waitlist_form(note='One email when sales open.', done='You are on the list. We will email you when sales open.')).replace('__INVENTORY__', inventory_html())


def lab_page(comps):
    experiments = [c for c in comps if c['meta']['category'] in ('Motion', 'KATAYABURI')]
    content = ''.join(card(c, True) for c in experiments)
    return head('Lab — KATA UI', 'Motion and KATAYABURI experiments.', LP_STYLE + '<link rel="stylesheet" href="/kata-ui.css">') + '<div class="wrap"><h1>Lab</h1><p>Animated text, backgrounds and interaction experiments. Check each component before using it in a project.</p><div class="cards">' + content + '</div></div>' + plain_footer() + '<script src="/kata-ui.js"></script></body></html>'


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
.ja-step{border:1px solid var(--hair);border-radius:13px;padding:17px;background:var(--paper)}
.ja-step .no{font-size:11px;font-weight:650;letter-spacing:.14em;color:var(--acc)}
.ja-step h3{font-size:14.5px;margin:7px 0 5px;letter-spacing:.04em}
.ja-step p{font-size:13px;line-height:1.8;color:var(--ink2);letter-spacing:.04em}
.ja-cards{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:16px}
.ja-card{border:1px solid var(--hair);border-radius:13px;padding:19px;background:var(--paper);text-decoration:none;color:inherit;display:block}
.ja-card h3{font-size:15.5px;letter-spacing:.04em}
.ja-card p{font-size:13px;line-height:1.8;color:var(--ink2);margin-top:6px;letter-spacing:.04em}
.ja-card .go{font-size:12.5px;font-weight:600;color:var(--acc);margin-top:10px;display:inline-block}
.ja-wl{margin-top:44px;background:#101013;border-radius:16px;padding:26px;color:#f4f4f5}
.ja-wl h2{color:#f4f4f5}
.ja-wl p{color:#c9c9ce}
@media (max-width:720px){.ja-steps,.ja-cards{grid-template-columns:1fr}.ja-hero h1{font-size:27px}.ja-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:16px 18px}}
</style>"""

def ja_doc_cards():
    cards = []
    for slug, ja in ja_docs().items():
        title = json.loads((ROOT / 'components' / slug / 'meta.json').read_text(encoding='utf-8'))['title']
        cards.append(f'<a class="ja-card" href="/ja/components/{slug}/"><h3>{esc(title)}　{esc(ja["name_ja"])}</h3><p>{esc(ja["description"])}</p></a>')
    return ''.join(cards)


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
    <h2>日本語ドキュメント</h2>
    <p>よく使う部品から順に、説明・使いどころ・アクセシビリティを日本語で読めます。コードと見本は英語版と同じです。</p>
    <div class="ja-cards">""" + ja_doc_cards() + """</div>
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
    <h2>日本の型、和の部品</h2>
    <p>KATAのJapanジャンルは、海外向けの「和風っぽさ」ではなく、作図の型そのものです。和柄は幾何の構成から描き、落款は印として押し、金継ぎは壊れと修復の作法として部品になっています。</p>
    <div class="ja-cards">
      <a class="ja-card" href="/components/wagara/"><h3>和柄（Wagara）</h3><p>青海波・麻の葉・七宝など、連続文様だけを100柄。Canvasに作図で描くので、色はトークンから変わります。<span class="go">部品ページへ →</span></p></a>
      <a class="ja-card" href="/components/hanko/"><h3>落款（Hanko）</h3><p>送信完了や承認の印に押す、小さな朱の印。サイト内でもウェイトリスト登録の完了印として働いています。<span class="go">部品ページへ →</span></p></a>
    </div>
  </section>
  <section class="ja-sec">
    <h2>料金</h2>
    <p>コンポーネントとアイコンは永久無料（MIT）。有料の Pro は、組み上げ済みのブロックとテンプレートで、$129の買い切り・買い切り後の追加料金なし。販売は近日開始です。</p>
  </section>
  <section class="ja-sec">
    <h2>よくある質問</h2>
    <p><b>商用利用はできますか。</b><br>はい。コンポーネントとアイコンはMITライセンスで、商用・改変・再配布が自由です。クレジット表記も不要です。</p>
    <p><b>パーツが有料になることはありますか。</b><br>ありません。無料の線は永久で、有料なのは組み上げ済みのブロックとテンプレートだけです。すでにコピーしたコードの扱いが変わることもありません。</p>
    <p><b>Proはいくらですか。</b><br>$129の一回払いです（目安として約2万円）。サブスクリプションではなく、購入後の追加課金もありません。販売開始までは全ブロック・全テンプレートをこのサイトで公開しています。</p>
    <p><b>Reactのプロジェクトでも使えますか。</b><br>使えます。部品は素のHTMLなので、JSXに貼ってclassをclassNameに変えるだけです。手順は英語ドキュメントの React &amp; Next.js ページにあります。</p>
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
.sc-card{border:1px solid var(--hair);border-radius:14px;padding:20px;background:var(--paper);text-decoration:none;color:inherit;display:block}
.sc-card:hover{border-color:var(--ink3)}
.sc-card .k{font-size:11px;font-weight:650;letter-spacing:.14em;color:var(--acc);text-transform:uppercase}
.sc-card h3{font-size:16px;margin:7px 0 5px}
.sc-card p{font-size:13px;line-height:1.75;color:var(--ink2);letter-spacing:.01em}
.sc-card .go{font-size:12.5px;font-weight:600;margin-top:10px;display:inline-block}
@media (max-width:720px){.sc-grid{grid-template-columns:1fr}}
</style>"""

def showcase_page(templates, blocks):
    def _parts(tp):
        return len(tp['meta'].get('uses', [])) + len(tp['meta'].get('blocks', []))
    cards = ''.join(
        f'<div class="sc-card"><span class="k">Template — live page</span><h3>{esc(tp["meta"]["title"])}</h3><p>{esc(tp["meta"]["description"])}</p><p class="sc-meta">{_parts(tp)} parts &amp; blocks composed — about 5 hours by hand from free parts; minutes from the Pro download.</p><a class="go" href="/templates/{esc(tp["slug"])}/demo/">Open the full-page demo →</a><br><a class="go" href="/templates/{esc(tp["slug"])}/" style="font-weight:500">Parts &amp; code →</a></div>'
        for tp in templates)
    cards += ('<div class="sc-card"><span class="k">Built with KATA — open shelf</span><h3>Your page here</h3>'
              '<p>This shelf is first-party for now, and it says so. The first outside builds will not be logos we rented — they will be pages like these, live and take-apart-able. Built something? It joins by being real.</p>'
              '<a class="go" href="https://github.com/kajisho5/KATA-UI/issues">Get listed — open an issue →</a></div>')
    body = """
<div class="wrap sc">
  <h1>Showcase</h1>
  <p class="lead">No mockups. Every page below is assembled from the catalog itself — the same parts, blocks and tokens the copy button hands you — and rendered live, full-screen. Take any of them apart to see.</p>
  <div class="sc-grid">
    <a class="sc-card" href="/"><span class="k">This site</span><h3>kata-ui.dev itself</h3><p>The landing page's showcase and collage are not screenshots: the dashboard in the hero window, the stat cards and the charts are live parts running on the page.</p><span class="go">See it on the home page →</span></a>
    <a class="sc-card" href="/starter/kata-starter.zip"><span class="k">Starter kit</span><h3>The starter project</h3><p>Tokens, the one-file bundle and a first page, zipped. The fastest test of the mold: unzip, open, and everything on screen is a part.</p><span class="go">Download the starter →</span></a>
""" + cards + """
  </div>
  <p class="note" style="margin-top:20px;font-size:13px;color:var(--ink3);line-height:1.8;letter-spacing:.01em">Building something with KATA? The maker reads every issue on the repository — a link there is how a project joins this page.</p>
</div>
""" + FOOTER + """
</body>
</html>"""
    return head('Showcase — KATA UI', 'Live pages assembled from the KATA UI catalog itself: templates, the starter kit, and this site.', SC_STYLE) + body

CMP_STYLE = """<style>
.cmp h1{margin-top:32px}
.cmp .lead{max-width:760px;margin-top:8px}
.cmp-method{margin-top:20px;border:1px solid var(--hair);border-radius:14px;padding:18px 20px;background:var(--paper);font-size:13.5px;line-height:1.75;color:var(--ink2)}
.cmp-method b{color:var(--ink)}
.cmp-method ul{margin:6px 0 0;padding-inline-start:18px}
.cmp h2{font-size:22px;margin:40px 0 12px}
.cmp .ktable-wrap{margin-top:8px}
.cmp .ktable td.num,.cmp .ktable th.num{font-variant-numeric:tabular-nums;text-align:end;white-space:nowrap}
.cmp .diff{font-weight:700;color:var(--ink)}
.cmp-sec{margin-top:48px;scroll-margin-top:72px}
.cmp-head{display:flex;flex-wrap:wrap;align-items:baseline;gap:10px}
.cmp-head .no{font-family:var(--k-mono);font-size:12px;color:var(--ink3)}
.cmp-head h2{margin:0}
.cmp-shots{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:12px}
.cmp-shot{border:1px solid var(--hair);border-radius:12px;overflow:hidden;background:var(--paper);margin:0}
.cmp-shot figcaption{display:flex;justify-content:space-between;gap:8px;padding:9px 14px;font-size:12.5px;font-weight:600;border-block-end:1px solid var(--hair)}
.cmp-shot img{display:block;inline-size:100%;block-size:auto}
.cmp .tabpane{margin-block-start:10px}
.cmp .k-acc{margin-top:12px}
.cmp pre{white-space:pre-wrap;font-size:12.5px;line-height:1.7;margin:0}
.cmp .note{font-size:13px;color:var(--ink3);line-height:1.8;margin-top:28px}
@media (max-width:640px){.cmp-shots{grid-template-columns:1fr}}
</style>"""

CMP_ROWS = [('focusInvisible', 'Tab stops with no visible focus', 'verify_focus_ring rule'),
            ('unnamed', 'Controls with no accessible name', 'Chromium accessibility tree'),
            ('lowContrast', 'Text below 4.5:1, light', 'capture_text_contrast metric'),
            ('lowContrastDark', 'Text below 4.5:1, dark', 'capture_text_contrast metric'),
            ('overflow', 'Elements past a 390px viewport, dark + RTL', 'bounding boxes'),
            ('consoleErrors', 'Console errors on load', 'Chromium console'),
            ('buttonNoType', '&lt;button&gt; without type', 'source'),
            ('colors', 'Distinct colors', 'computed CSS'),
            ('spacings', 'Distinct spacing values', 'computed CSS'),
            ('bytes', 'File size (bytes)', 'file size')]
CMP_SUMMARY = ['focusInvisible', 'unnamed', 'lowContrastDark', 'overflow', 'consoleErrors', 'colors', 'spacings']


def compare_page():
    data = json.loads((ROOT / 'comparison' / 'results.json').read_text(encoding='utf-8'))
    screens = data['screens']
    labels = {k: t for k, t, _ in CMP_ROWS}
    chevron = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="square" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>'

    def pair(a, b):
        cls = ' class="diff"' if a != b else ''
        return f'<span{cls}>{a}</span> / <span{cls}>{b}</span>'

    head_cells = ''.join(f'<th scope="col" class="num">{labels[k]}<br><small>A / B</small></th>' for k in CMP_SUMMARY)
    rows = ''.join(
        f'<tr><td><a href="#cmp-{s["slug"]}">{i:02d} {esc(s["title"])}</a></td>'
        + ''.join(f'<td class="num">{pair(s["direct"][k], s["kata"][k])}</td>' for k in CMP_SUMMARY) + '</tr>'
        for i, s in enumerate(screens, 1))
    summary = ('<div class="ktable-wrap" role="region" aria-label="Summary, A then B" tabindex="0"><table class="ktable">'
               f'<thead><tr><th scope="col">Screen</th>{head_cells}</tr></thead><tbody>{rows}</tbody></table></div>')
    sections = []
    for i, s in enumerate(screens, 1):
        slug = s['slug']
        prompt = (ROOT / 'comparison' / slug / 'prompt.md').read_text(encoding='utf-8')
        prompt = re.sub(r'^# .*\n+', '', prompt)

        def shots(theme):
            return '<div class="cmp-shots">' + ''.join(
                f'<figure class="cmp-shot"><figcaption><span>{tag}</span><a href="/compare/{slug}/{file}">{file}</a></figcaption>'
                f'<img src="/compare/shots/{slug}-{draft}-{theme}.png" width="1280" height="900" loading="lazy" '
                f'alt="{esc(s["title"])}, draft {"B" if draft == "kata" else "A"}, {theme} theme"></figure>'
                for draft, file, tag in (('direct', 'direct.html', 'A · Prompt alone'), ('kata', 'kata.html', 'B · Assembled from KATA parts'))) + '</div>'
        table = ''.join(f'<tr><td>{t}</td><td class="num">{pair(s["direct"][k], s["kata"][k])}</td><td>{how}</td></tr>' for k, t, how in CMP_ROWS)
        sections.append(
            f'<section class="cmp-sec" id="cmp-{slug}" aria-labelledby="cmp-h-{slug}">'
            f'<div class="cmp-head"><span class="no" aria-hidden="true">{i:02d}</span><h2 id="cmp-h-{slug}">{esc(s["title"])}</h2></div>'
            f'<span class="tabs" data-tabs aria-label="{esc(s["title"])} screenshots"><span class="thumb"></span><button type="button" class="on">Light</button><button type="button">Dark</button></span>'
            f'<div class="tabpane" data-tabpane>{shots("light")}</div><div class="tabpane" data-tabpane>{shots("dark")}</div>'
            f'<div class="ktable-wrap" role="region" aria-label="{esc(s["title"])} measurements" tabindex="0"><table class="ktable">'
            f'<thead><tr><th scope="col">Measure</th><th scope="col" class="num">A / B</th><th scope="col">How</th></tr></thead><tbody>{table}</tbody></table></div>'
            f'<details class="k-acc"><summary>Prompts{chevron}</summary><div class="k-acc-body"><pre>{esc(prompt.strip())}</pre></div></details>'
            '</section>')
    body = f"""
<div class="wrap cmp">
  <h1>Ten screens, two ways</h1>
  <p class="lead">One prompt per screen. A: the prompt alone. B: the same prompt plus one sentence that points at the KATA registry. Every number below comes from <code>comparison/results.json</code>.</p>
  <div class="cmp-method"><b>Method</b><ul>
    <li>Agent: {esc(data['agent'])}, {esc(data['generated'])}. A and B were written by two separate agents with no earlier conversation; A could read only the prompts, B the prompts and kata-ui.dev.</li>
    <li>First output kept for all 20 drafts: no retries, no picking, no hand edits, nothing rendered before measuring.</li>
    <li>B adds this sentence to prompt A: “Fetch each part from kata-ui.dev/registry.json and use it unmodified.”</li>
    <li>Measured in Chromium by <a href="https://github.com/kajisho5/KATA-UI/blob/main/tools/measure_comparison.py">tools/measure_comparison.py</a>; prompts and raw files are in <a href="https://github.com/kajisho5/KATA-UI/tree/main/comparison">comparison/</a>. Differing values are set in bold.</li>
  </ul></div>
  <h2>Summary</h2>
  {summary}
  {''.join(sections)}
  <p class="note">One run, one agent, one date: another agent or day gives other numbers. Not verified: screen readers, Safari, Firefox, real devices.</p>
</div>
""" + FOOTER + """
</body>
</html>"""
    extra = (CMP_STYLE + ''.join(f'<link rel="stylesheet" href="/components/{sl}/{sl}.css?v={_v((ROOT / "components" / sl / (sl + ".css")).read_text(encoding="utf-8"))}">'
                                 for sl in ('table', 'tabs', 'accordion')))
    script = f'<script src="/components/tabs/tabs.js?v={_v((ROOT / "components/tabs/tabs.js").read_text(encoding="utf-8"))}"></script>'
    return head('Ten screens, two ways — KATA UI', 'Ten common screens drafted twice by an AI agent: from the prompt alone, and assembled from KATA registry parts. Prompts, raw files and measurements.', extra) + body.replace('</body>', script + '</body>', 1)


DS_CAST_TAG = "<script>" + "\n(function(){\n  var root=document.documentElement;\n  var PRESETS={Asagi:['#33A6B8','#165E83','#81C7D4'],Ruri:['#1E50A2','#223A70','#58B2DC'],Edomurasaki:['#745399','#592C63','#8B81C3'],Suo:['#8E354A','#64363C','#DC9FB4'],Kaki:['#ED6D3D','#95483F','#E2943B']};\n  function load(){try{return JSON.parse(localStorage.getItem('kata-fdeck')||'{}')}catch(e){return{}}}\n  function save(S){try{localStorage.setItem('kata-fdeck',JSON.stringify(S))}catch(e){}}\n  function stat(msg){var el=document.getElementById('ds-stat');if(el)el.textContent=msg;var card=document.getElementById('ds-floor');if(card){card.classList.remove('castflash');void card.offsetWidth;card.classList.add('castflash');}}\n  function castRadius(v){var S=load();S.radius=v;root.style.setProperty('--k-radius',v+'px');var sl=document.getElementById('fd-radius');if(sl){sl.value=v;var o=document.getElementById('fd-rv');if(o)o.textContent=v+'px';}save(S);stat('Cast \\u2014 radius '+v+'px. The parts above re-cast; the deck remembers it.');}\n  function castAccent(name){var p=PRESETS[name];if(!p)return;var S=load();S.accent=p[0];S.accentInk=p[1];S.darkInk=p[2];S.accentName=name;var dark=root.getAttribute('data-theme')==='dark';root.style.setProperty('--k-accent',p[0]);root.style.setProperty('--acc',p[0]);root.style.removeProperty('--k-accent-ink');save(S);document.querySelectorAll('[data-cast-accent]').forEach(function(b){b.classList.toggle('on',b.dataset.castAccent===name)});stat('Cast \\u2014 accent '+name+'.');}\n  function castMotion(v){var S=load();S.mscale=v;root.style.setProperty('--k-mscale',v);var sl=document.getElementById('fd-motion');if(sl)sl.value=v;save(S);stat('Cast \\u2014 motion '+v+'\\u00d7.');}\n  document.querySelectorAll('[data-cast-radius]').forEach(function(b){b.addEventListener('click',function(){castRadius(+b.dataset.castRadius)})});\n  document.querySelectorAll('[data-cast-accent]').forEach(function(b){b.addEventListener('click',function(){castAccent(b.dataset.castAccent)})});\n  document.querySelectorAll('[data-cast-motion]').forEach(function(b){b.addEventListener('click',function(){castMotion(+b.dataset.castMotion)})});\n  var S0=load();if(S0.accentName)document.querySelectorAll('[data-cast-accent]').forEach(function(b){b.classList.toggle('on',b.dataset.castAccent===S0.accentName)});\n})();\n" + "</script>\n"


def design_system_page(tokens):
    def swatches(scale_name, scale):
        cells = ''.join(
            f'<div class="sw"><div class="fill" style="background:{v}"></div><div class="meta"><b>{scale_name+"-" if scale_name else ""}{k}</b><br>{v}</div></div>'
            for k, v in scale.items())
        return f'<div class="swatches">{cells}</div>'
    elevation_rows=''.join(f'<div class="row"><b>--k-shadow-{name}</b><code>{esc(pair["light"])}</code><small>Dark: {esc(pair["dark"])}</small></div>' for name,pair in tokens['elevation']['shadows'].items())
    elevation_rows+='<div class="row"><b>--k-shadow-overlay</b><code>var(--k-shadow-pop)</code></div>'
    elevation_rows+=''.join(f'<div class="row"><b>--k-ring-{name}</b><code>{esc(value)}</code></div>' for name,value in tokens['elevation']['rings'].items())
    elevation_rows+=f'<div class="row"><b>--k-backdrop</b><code>{esc(tokens["elevation"]["backdrop"]["light"])}</code><small>Dark: {esc(tokens["elevation"]["backdrop"]["dark"])}</small></div>'
    motion_rows=''.join(f'<div class="row"><b>--k-ease{"-"+name if name else ""}</b><code>{esc(value)}</code></div>' for name,value in {'':tokens['motion']['easing'],**tokens['motion']['easings']}.items())
    roles = ''.join(f'<div><b>--k-{k}</b> — {esc(v)}</div>' for k, v in tokens['color']['roles'].items())
    semantic_rows=''.join(f'<div><b>{esc(name)}</b> — light: <code>{esc(tokens["semanticColors"]["light"].get(name,"inherited"))}</code>; dark: <code>{esc(tokens["semanticColors"]["dark"].get(name,"inherited"))}</code></div>' for name in sorted(set(tokens.get('semanticColors',{}).get('light',{})) | set(tokens.get('semanticColors',{}).get('dark',{}))))
    specs = ''.join(
        f'<div class="row"><span class="tag">{k} · {v}px</span><span class="sample" style="font-size:{v}px">Design, cast in a mold</span></div>'
        for k, v in tokens['typeScalePx'].items())
    bars = ''.join(
        f'<div class="row"><span style="width:64px">space-{k}</span><span class="bar" style="width:{v}px"></span><span>{v}px</span></div>'
        for k, v in tokens['spacePx'].items())
    _ct = {}
    for _c in load_components():
        _ct[_c['slug']] = (_c['meta']['title'], '/components/')
    for _b in load_blocks():
        _ct[_b['slug']] = (_b['meta']['title'], '/blocks/')
    for _t in load_templates():
        _ct[_t['slug']] = (_t['meta']['title'], '/templates/')
    _hits, _seen = [], set()
    for _kind in ('components', 'blocks', 'templates'):
        for _f in sorted(glob.glob(str(ROOT / _kind / '*' / '*.css'))):
            _slug = Path(_f).parent.name
            if _slug in _ct and _slug not in _seen and '--k-core' in Path(_f).read_text(encoding='utf-8'):
                _seen.add(_slug)
                _hits.append((_slug, _ct[_slug][0], _ct[_slug][1]))
    _chips = ''.join(f'<a class="corechip" href="{_b}{_s}/">{esc(_t)}</a>' for _s, _t, _b in _hits)
    core_map = ('<section><h2>The vermillion, mapped</h2>'
      '<p class="note">--k-core, the vermillion at the center of the mark, appears in exactly these parts -- and in a short list of site moments: the lower-right quarter of the logo, the Hanko seal, the copy flash, the Foundry deck dot, the waitlist stamp. This list is generated from the CSS at build time, so it cannot drift from the truth. Everywhere else, the accent speaks.</p>'
      '<div class="corechips">' + _chips + '</div></section>')
    radii = ''.join(
        (f'<button type="button" class="box castable" data-cast-radius="{v}" style="border-radius:var(--k-radius-{k})" title="Cast this radius">{k} · {v}</button>' if k != 'full'
         else f'<div class="box" style="border-radius:var(--k-radius-{k})">{k} · {v}</div>')
        for k, v in tokens['radiusPx'].items())
    body = f"""
<div class="wrap ds">
  <h1>Design System</h1>
  <p class="lead">The foundation every KATA component is cast from: color, type, spacing, radius, motion. One accent, hairline borders, flat surfaces — and tokens for everything, so the system survives every theme.</p>
  <section class="dsfloor" id="ds-floor"><h2>One token, everything moves</h2>
    <p class="note">This page is a casting bench: every control below changes the whole system at once. Cast an accent, a radius or a motion scale, and the real parts below re-cast at once. The Foundry deck (bottom right) remembers it across the site.</p>
    <div class="ds-live">
      <button class="btn btn-pri btn-md" type="button">Cast me</button>
      <span class="switch asagi"><input type="checkbox" checked aria-label="Foundry floor switch"><span class="tr"></span></span>
      <input class="input" type="text" placeholder="Tokens in, parts out" style="max-width:200px" aria-label="Foundry floor input">
      <span class="badge asagi"><i></i>Same mold</span>
    </div>
    <div class="ds-casts">
      <div class="ds-castrow"><span>Accent</span><span class="ds-sws"><button type="button" data-cast-accent="Asagi" style="background:#33A6B8" aria-label="Cast Asagi"></button><button type="button" data-cast-accent="Ruri" style="background:#1E50A2" aria-label="Cast Ruri"></button><button type="button" data-cast-accent="Edomurasaki" style="background:#745399" aria-label="Cast Edomurasaki"></button><button type="button" data-cast-accent="Suo" style="background:#8E354A" aria-label="Cast Suo"></button><button type="button" data-cast-accent="Kaki" style="background:#ED6D3D" aria-label="Cast Kaki"></button></span></div>
      <div class="ds-castrow"><span>Radius</span><span class="ds-btns"><button type="button" data-cast-radius="0">0</button><button type="button" data-cast-radius="4">4</button><button type="button" data-cast-radius="8">8 \u00b7 mold</button><button type="button" data-cast-radius="12">12</button><button type="button" data-cast-radius="16">16</button><button type="button" data-cast-radius="20">20</button></span></div>
      <div class="ds-castrow"><span>Motion</span><span class="ds-btns"><button type="button" data-cast-motion="0.7">0.7\u00d7</button><button type="button" data-cast-motion="1">1.0\u00d7 \u00b7 mold</button><button type="button" data-cast-motion="1.4">1.4\u00d7</button></span></div>
    </div>
    <div class="ds-live2">
      <div class="k-card"><div class="k-card-h"><div><h3>Casting notes</h3><p>The same card, whatever the mold says.</p></div><span class="sp"><span class="badge asagi">Live</span></span></div><div class="k-card-b">Its badge answers the accent, and the controls above answer every cast \u2014 radius, accent, motion. The frame was cast from the same tokens when this page loaded; nothing here was re-styled by hand.</div><div class="k-card-f">Cast from tokens<span class="sp"><button class="btn btn-pri btn-sm" type="button">Open report</button></span></div></div>
      <div class="ds-prog"><div class="ds-prog-cap"><span>Deploy queue</span><span>68%</span></div><div class="k-progress" data-tone="accent" role="progressbar" aria-valuenow="68" aria-valuemin="0" aria-valuemax="100"><div class="k-progress-bar" style="width:68%"></div></div><p class="note" style="margin-top:10px">The bar wears the accent outright. Cast Ruri above and watch it turn \u2014 no reload, no re-style.</p></div>
    </div>
    <p class="ds-stat" id="ds-stat" role="status"></p>
  </section>
  <div class="dl">
    <a href="/tokens.css">tokens.css</a>
    <a href="/design-system/tokens.json">tokens.json</a>
    <a href="/components/">Browse components</a>
  </div>
  <section><h2>Fixed traditional palette</h2>{swatches("", tokens["color"].get("fixed",{}))}</section>
  <section><h2>Color — Zinc</h2><p class="note">The dominant scale. Interfaces are built from zinc first; color is the exception.</p>{swatches('zinc', tokens['color']['zinc'])}</section>
  <section><h2>Color — Asagi (the one accent)</h2><p class="note">A single accent, used sparingly: links, highlights, the core of the mark. If everything is asagi, nothing is.</p>{swatches('asagi', tokens['color']['asagi'])}</section>
  <section><h2>Color — Roles</h2><div class="roles">{roles}</div><div class="roles">{semantic_rows}</div></section>
  <section><h2>Typography</h2><p class="note">Sans: {esc(tokens['font']['sans'])}<br>Mono: {esc(tokens['font']['mono'])}<br>Tracking: {esc(tokens['font']['tracking'])}<br>Leading: {esc(tokens['font']['leading'])}</p><div class="spec">{specs}</div></section>
  <section><h2>Spacing</h2><p class="note">A 4px base. If a gap is not on this scale, it is a mistake.</p><div class="bars">{bars}</div></section>
  <section><h2>Radius</h2><p class="note">xs / sm / md / lg / xl follow --k-radius. Full stays 999px for pills; circular geometry stays circular.</p><div class="radii">{radii}</div></section>
  <section><h2>Heights</h2><p class="note">Controls come in three heights — 32 / 38 / 44px. Shared heights are what make separate components look like one system.</p></section>
  <section><h2>Motion</h2><p class="note">{esc(tokens['motion']['rule'])} Hover the cards. Fast / base / slow all follow the Foundry multiplier; reduced motion stops them.</p>
    <div class="motions">
      <div class="m" style="--dur:var(--k-dur-fast)">fast · 130ms<div class="dot"></div></div>
      <div class="m" style="--dur:var(--k-dur-base)">base · 180ms<div class="dot"></div></div>
      <div class="m" style="--dur:var(--k-dur-slow)">slow · 220ms<div class="dot"></div></div>
    </div><p class="note">--k-ease: entrance / general (out) · --k-ease-in-out: repositioning / exit · --k-ease-spring: gentle overshoot · --k-ease-bounce: pronounced overshoot (Lab). Numbered duration tokens remain aliases. The old ease-out name is a deprecated alias for ease-in-out.</p>{motion_rows}</section>
  <section><h2>Elevation</h2><p class="note">{esc(tokens['elevation']['rule'])}</p><div class="spec">{elevation_rows}</div></section>
  {core_map}
  <section><h2>Breakage — Kintsugi</h2><p class="note">Errors, empty states and loading wear one seam: a jagged line of yamabuki gold, the Kintsugi Card's vein. Breakage is shown and mended visibly — never hidden behind a spinner and never dressed as success. It is the seam on the 404 plate and the state line in \u2318K search.</p>
    <p class="kin-demo"><span class="kin-seam" aria-hidden="true"></span>Casting a preview\u2026</p>
    <p class="note">The part that carries the language: <a href="/components/kintsugi-card/">Kintsugi Card</a>.</p></section>
</div>
{FOOTER}
</body>
</html>"""
    ds_links = ''.join(f'<link rel="stylesheet" href="/components/{sl}/{sl}.css">' for sl in ('button', 'switch', 'input', 'badge', 'card', 'progress'))
    return head('Design System — KATA UI', 'The KATA design system: color, type, spacing, radius and motion tokens.', DS_STYLE + ds_links) + body.replace('</body>', DS_CAST_TAG + '</body>', 1)


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
.bcard{border:1px solid var(--hair);border-radius:14px;background:var(--paper);padding:18px;text-decoration:none;color:var(--ink);display:block}
.bcard:hover{border-color:var(--ink3)}
.bcard h3{font-size:15.5px;font-weight:600;display:flex;align-items:center;gap:8px}
.bcard p{margin-top:7px;font-size:13px;color:var(--ink2);line-height:1.75;letter-spacing:.01em}
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
      <div class="codebox"><div class="pane on"><pre>npx @kajisho5/kataui add {slug}</pre><div class="copyrow"><button class="copybtn">Copy</button></div></div></div>
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
    {render_checks(MOLD_ITEMS['blocks/' + slug])}
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
.tplcard{border:1px solid var(--hair);border-radius:14px;background:var(--paper);color:var(--ink);display:block;overflow:hidden;position:relative}
.tplcard .tplmeta h3 a{color:inherit;text-decoration:none}
.tplcard .tplmeta h3 a::after{content:"";position:absolute;inset:0}
.tplcard:hover{border-color:var(--ink3)}
.tplthumb{height:190px;overflow:hidden;border-bottom:1px solid var(--hair);position:relative;background:var(--soft)}
.tplscale{width:1080px;transform:scale(.306);transform-origin:top left;pointer-events:none}
.tplmeta{padding:16px 18px 18px}
.tplmeta h3{font-size:15.5px;font-weight:600;display:flex;align-items:center;gap:8px}
.tplmeta p{margin-top:7px;font-size:13px;color:var(--ink2);line-height:1.75;letter-spacing:.01em}
.tplmeta .uses{margin-top:12px;display:flex;gap:5px;flex-wrap:wrap}
.tplmeta .uses span{font-family:var(--mono);font-size:10.5px;color:var(--ink2);border:1px solid var(--hair);border-radius:99px;padding:2px 8px}
.tplframe{border:1px solid var(--hair);border-radius:14px;overflow:hidden;background:var(--paper)}
.tplbar{display:flex;align-items:center;gap:10px;padding:9px 12px;border-bottom:1px solid var(--hair);background:var(--soft)}
.tpldots{display:flex;gap:6px}
.tpldots i{width:10px;height:10px;border-radius:50%;background:var(--hair);display:block}
.tplurl{font-family:var(--mono);font-size:11.5px;color:var(--ink2);background:var(--paper);border:1px solid var(--hair);border-radius:7px;padding:3px 12px}
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


def template_demo(t, comps, blocks):
    slug = t['slug']
    m = t['meta']
    by_slug = {x['slug']: x for x in comps}
    blk_by_slug = {x['slug']: x for x in blocks}
    css_links = '<link rel="stylesheet" href="/tokens.css">'
    for u in m.get('uses', []):
        if u in by_slug:
            css_links += f'\n<link rel="stylesheet" href="/components/{u}/{u}.css?v={_v(by_slug[u]["css"])}">'
    for u in m.get('blocks', []):
        if u in blk_by_slug:
            css_links += f'\n<link rel="stylesheet" href="/blocks/{u}/{u}.css?v={_v(blk_by_slug[u]["css"])}">'
    css_links += f'\n<link rel="stylesheet" href="/templates/{slug}/{slug}.css?v={_v(t["css"])}">'
    markup = re.sub(r'\s*<link rel="stylesheet"[^>]*>', '', t['preview']).strip()
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
    badge = (f'<a href="/templates/{slug}/" style="position:fixed;left:14px;bottom:14px;z-index:60;display:inline-flex;align-items:center;gap:8px;'
             'background:#18181b;color:#f4f4f5;border:1px solid rgba(255,255,255,.2);padding:9px 15px;border-radius:999px;'
             'font:500 12.5px Inter,system-ui,sans-serif;letter-spacing:.01em;text-decoration:none;box-shadow:0 12px 32px -12px rgba(0,0,0,.5)">'
             '<span style="width:7px;height:7px;border-radius:50%;background:#eb471f;display:inline-block"></span>'
             'Built with KATA UI — this page is a template. Get it &rarr;</a>')
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<script src="/color-roles.js"></script>
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>(function(){{function apply(){{try{{var st=JSON.parse(localStorage.getItem("kata-fdeck")||"{{}}");var r=document.documentElement;var d=("dark" in st)?!!st.dark:(window.matchMedia&&matchMedia("(prefers-color-scheme: dark)").matches);if(d)r.setAttribute("data-theme","dark");else r.removeAttribute("data-theme");if(st.radius!==undefined){{r.style.setProperty("--k-radius",st.radius+"px");}}if(st.accent){{r.style.setProperty("--k-accent",st.accent);r.style.setProperty("--acc",st.accent);r.style.removeProperty("--k-accent-ink");}}}}catch(e){{}}}}apply();window.addEventListener("storage",function(e){{if(e.key==="kata-fdeck")apply();}});}})();</script>
<title>{esc(m['title'])} — live demo · KATA UI</title>
<meta name="description" content="{esc(m['description'])}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">
{css_links}
<style>html,body{{margin:0;padding:0}}body{{background:var(--k-bg);color:var(--k-ink);font-family:var(--k-font)}}</style>
</head>
<body>
{markup}
{badge}
{scripts}
</body>
</html>"""


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
      <a href="/templates/{slug}/demo/" style="font-size:12.5px;font-weight:600;color:var(--acc);text-decoration:none;margin-left:auto">Open the full-page demo &#8599;</a>
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
    {render_checks(MOLD_ITEMS['templates/' + slug])}
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
    from tools.color_roles import theme_css as export_roles
    import json
    return export_roles(t['accent'], json.loads((ROOT/'system/tokens.json').read_text())['contrast'])

THEME_STYLE = """<style>
.th h1{font-size:32px;font-weight:600;letter-spacing:-.025em;margin-top:26px}
.th .lead{margin-top:10px;color:var(--ink2);font-size:15px;line-height:1.85;max-width:64ch;letter-spacing:.012em}
.thgrid{margin-top:24px;display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:10px}
.thcard{border:1px solid var(--hair);border-radius:12px;background:var(--paper);padding:14px;text-align:left;cursor:pointer;font:inherit;color:var(--ink)}
.thcard:hover{border-color:var(--ink3)}
.thcard.on{border-color:var(--ink);box-shadow:0 0 0 1px var(--ink)}
.thcard .sw{display:flex;gap:5px;margin-bottom:11px}
.thcard .sw i{width:22px;height:22px;border-radius:7px;display:block;border:1px solid var(--hair)}
.thcard .nm{font-size:14px;font-weight:600}
.thcard .nt{font-size:12px;color:var(--ink2);margin-top:3px;line-height:1.6}
.thdemo{margin-top:22px;border:1px solid var(--hair);border-radius:14px;background:var(--paper);padding:22px;display:flex;gap:22px;align-items:center;flex-wrap:wrap}
.thdemo .lbl{font-family:var(--mono);font-size:11px;color:var(--ink3);letter-spacing:.06em;width:100%}
.thcode{margin-top:16px;border:1px solid var(--hair);border-radius:12px;overflow:hidden}
.thcode pre{margin:0;padding:16px;overflow:auto;font-family:var(--mono);font-size:12px;line-height:1.75;background:var(--soft)}
.thcode .bar{display:flex;gap:8px;align-items:center;padding:9px 12px;border-bottom:1px solid var(--hair);background:var(--paper)}
.thcode .bar b{font-size:12.5px;margin-right:auto}
.thcode .bar a,.thcode .bar button{font:inherit;font-size:12px;border:1px solid var(--hair);background:var(--paper);border-radius:7px;padding:5px 11px;cursor:pointer;color:var(--ink);text-decoration:none}
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
.dtpv{margin-top:18px;border:1px solid var(--hair);border-radius:14px;background:var(--paper);padding:16px 18px;display:flex;gap:14px;align-items:center;flex-wrap:wrap}
.dtpv .lbl{font-family:var(--mono);font-size:11px;color:var(--ink3);letter-spacing:.06em;width:100%}
.dtpv .dtstatus{font-size:12.5px;color:var(--ink2)}
.dtfam{font-size:12.5px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:var(--ink2);margin:28px 0 10px;display:flex;gap:12px;align-items:baseline}
.dtfam span{font-family:"Yuji Syuku","Hiragino Mincho ProN","Yu Mincho",serif;letter-spacing:.25em;color:var(--ink3);font-size:13px;text-transform:none;font-weight:400}
.dtgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(218px,1fr));gap:12px}
.dtcard{border:1px solid var(--hair);border-radius:12px;background:var(--paper);padding:0;text-align:left;cursor:pointer;overflow:hidden;font:inherit;color:var(--ink);display:flex;flex-direction:column;width:100%}
.dtcard .dsw{height:88px;display:block;border-bottom:1px solid var(--hair);flex:none}
.dtcard:hover{border-color:var(--ink3)}
.dtcard.on{border-color:var(--ink);box-shadow:0 0 0 1px var(--ink)}
.dtcard .dsw{height:88px;display:block;border-bottom:1px solid var(--hair)}
.dtcard .dbd{display:block;padding:13px 15px 14px}
.dtcard .dkj{font-family:"Yuji Syuku","Hiragino Mincho ProN","Yu Mincho",serif;font-size:27px;line-height:1.3;display:block;letter-spacing:.06em}
.dtcard .drm{font-size:12.5px;font-weight:600;margin-top:3px;display:flex;flex-wrap:wrap;column-gap:6px;align-items:baseline;letter-spacing:.01em}
.dtcard .drm i{font-style:normal;font-weight:400;color:var(--ink3);font-size:11.5px;letter-spacing:.05em;white-space:nowrap}
.dtcard .dhx{font-family:var(--mono);font-size:11.5px;color:var(--ink2);margin-top:5px;display:flex;justify-content:space-between;align-items:center;letter-spacing:.03em}
.dtcard .dhx .cp{font-size:10.5px;color:var(--ink3);border:1px solid var(--hair);border-radius:6px;padding:2px 7px}
.dtcard .dnt{font-size:12.5px;color:var(--ink2);line-height:1.65;margin-top:6px;display:block;letter-spacing:.01em}
.dtcast{margin-left:auto;font:inherit;font-size:11.5px;font-weight:600;letter-spacing:.02em;text-transform:none;color:var(--ink);border:1px solid var(--hair);background:var(--paper);border-radius:8px;padding:6px 12px;cursor:pointer}
.dtcast:hover{border-color:var(--ink3)}
.dtmini{border:1px solid var(--k-accent-line);background:var(--k-accent-bg);color:var(--k-accent-ink);border-radius:10px;padding:10px 13px;font-size:12.5px;line-height:1.55;max-width:300px}
.dtmini b{display:block;font-size:13px}
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
    <button class="btn btn-accent btn-md">Accent button</button>
    <span class="switchrow"><label class="switch asagi"><input type="checkbox" checked><span class="tr"></span></label>Notifications</span>
    <span class="badge asagi"><i></i>Live</span>
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
        _lead = f['colors'][0]
        _lslug = _lead['romaji'].lower().replace('\u016b', 'u').replace('\u014d', 'o')
        _cast = ('<button class="dtcast" type="button" data-cast-family data-hex="' + _lead['hex'] + '" data-name="' + _lead['romaji'] + '" data-slug="' + _lslug + '" data-kanji="' + _lead['kanji'] + '">Cast this theme \u00b7 ' + _lead['romaji'] + '</button>')
        fams.append('<h3 class="dtfam">' + f['family'] + '<span>' + f['family_jp'] + '</span>' + _cast + '</h3><div class="dtgrid">' + ''.join(dcards) + '</div>')
    palette = """
<section class="dentou" id="dentou">
  <span class="dtk">伝統色</span>
  <h2>Traditional colors of Japan</h2>
  <p class="lead" style="margin-top:8px">Fifty colors that began as dyes, pigments and plants \u2014 indigo, safflower, gardenia, pine soot. Click one and it is cast into the same demo and the same CSS as any theme above: the button, the switch and the badge take the color, under its own name (ai.css, yamabuki.css). The hex values follow the common references (NIPPON COLORS and the JIS customary color names); colors older than hex itself are approximations.</p>
  <div class="dtpv" id="dtpv">
    <span class="lbl">CASTING \u2014 TRADITIONAL COLORS</span>
    <button class="btn btn-accent btn-md" type="button">Accent button</button>
    <span class="badge asagi"><i></i><span id="dtpvname">Asagi</span></span>
    <label class="switch asagi"><input type="checkbox" checked><span class="tr"></span></label>
    <div class="dtmini"><b id="dtmininame">Asagi</b>A whole card dyed by one cast \u2014 border, wash and ink all follow the color.</div>
    <span class="dtstatus" id="dtstatus">Pick a color below \u2014 it lands here, in the demo above, and in the CSS.</span>
  </div>
""" + ''.join(fams) + """
</section>
"""
    dentou_script = r"""<script>
function applyDentou(hex,romaji,slug,kanji){
  var rgb=h2r(hex);
  [demo,document.getElementById('dtpv')].forEach(function(el){
    el.style.setProperty('--k-accent',hex);document.dispatchEvent(new CustomEvent('kata:color-roles',{detail:{accent:hex,element:el}}));

    el.style.setProperty('--k-accent-bg','rgba('+rgb.join(',')+',.08)');
    el.style.setProperty('--k-accent-bg-strong','rgba('+rgb.join(',')+',.1)');
    el.style.setProperty('--k-accent-line','rgba('+rgb.join(',')+',.18)');
  });
  var css='';document.dispatchEvent(new CustomEvent('kata:color-roles',{detail:{accent:hex,receive:function(result){css=result.css;}}}));
  document.getElementById('thcss').textContent=css;
  document.getElementById('thname').textContent=slug+'.css';
  if(blobUrl)URL.revokeObjectURL(blobUrl);
  blobUrl=URL.createObjectURL(new Blob([css],{type:'text/css'}));
  var dl=document.getElementById('thdl');dl.href=blobUrl;dl.setAttribute('download',slug+'.css');
  document.getElementById('thhex').textContent=hex;
  document.getElementById('thcolor').value=hex.toLowerCase();
  document.getElementById('dtpvname').textContent=romaji;
  var mn=document.getElementById('dtmininame');if(mn)mn.textContent=romaji;
  document.getElementById('dtstatus').textContent=kanji+' '+romaji+' \u2014 '+hex.toUpperCase()+' is cast. The theme CSS above is now '+slug+'.css.';
  document.querySelectorAll('[data-theme-card]').forEach(function(c){c.classList.remove('on');});
}
document.querySelectorAll('[data-cast-family]').forEach(function(btn){
  btn.addEventListener('click',function(){
    applyDentou(btn.dataset.hex,btn.dataset.name,btn.dataset.slug,btn.dataset.kanji);
    document.querySelectorAll('[data-dentou]').forEach(function(c){c.classList.toggle('on',c.dataset.hex.toLowerCase()===btn.dataset.hex.toLowerCase());});
    var css=document.getElementById('thcss').textContent;
    if(navigator.clipboard)navigator.clipboard.writeText(css);
    var t=btn.textContent;btn.textContent='Copied \u2014 '+btn.dataset.slug+'.css';
    setTimeout(function(){btn.textContent=t;},1600);
  });
});
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
  demo.style.setProperty('--k-accent',t.accent);document.dispatchEvent(new CustomEvent('kata:color-roles',{detail:{accent:t.accent,element:demo}}));

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
  var rgb=h2r(hex);
  demo.style.setProperty('--k-accent',hex);document.dispatchEvent(new CustomEvent('kata:color-roles',{detail:{accent:hex,element:demo}}));

  demo.style.setProperty('--k-accent-bg','rgba('+rgb.join(',')+',.08)');
  demo.style.setProperty('--k-accent-bg-strong','rgba('+rgb.join(',')+',.1)');
  demo.style.setProperty('--k-accent-line','rgba('+rgb.join(',')+',.18)');
  var css='';document.dispatchEvent(new CustomEvent('kata:color-roles',{detail:{accent:hex,receive:function(result){css=result.css;}}}));
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
applyTheme('asagi');
</script>"""
    body = """
<div class="wrap th">
  <h1>Themes</h1>
  <p class="lead">A theme moves one thing: the accent. Neutrals stay zinc, motion stays measured, and the vermillion core — the mark inside the Switch and the Radio — never changes. Pick a preset to see the same parts re-cast, then take the CSS. Or skip the presets \u2014 <a href="#dentou">fifty traditional colors of Japan</a> wait below, each ready to cast.</p>
  <div class="thgrid">""" + ''.join(cards) + """
  </div>
""" + demo + builder + """
  <div class="thcode">
    <div class="bar"><b id="thname">asagi.css</b><button id="thcopy" type="button">Copy CSS</button><a id="thdl" href="/themes/asagi.css" download>Download</a></div>
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
   [('A library you copy and keep', 'KATA UI is a catalog of interface parts — components, assembled blocks, and whole page templates — written in plain HTML, CSS and JavaScript. You take the code: by copy-paste from any part\u2019s page, or with the CLI. There is no framework to adopt, no build step to configure and no runtime to ship. After the copy, the code is yours; nothing updates itself and nothing phones home.', None, 'The catalog today: 136 parts, 21 blocks, 7 templates, 150 icons and 220 brand marks, 5 accent presets — every one free under MIT.'),
    ('Cast from a single mold', 'Every part is built to one written standard (the mold) and machine-checked against it before it ships: the same design tokens, the same spacing rhythm, the same states and focus rings, the same icon geometry. That sameness across all parts is the product. It is also why the parts compose: a Modal, a Command palette and a form built months apart sit together like they were made in one afternoon, because in the ways that show, they were.', None, 'The word kata is the Japanese discipline of the form: a pattern practiced until it disappears into the work.'),
    ('Three ways in', 'Copy-paste from the site is the front door — every part page shows its HTML, CSS and JS with a live preview. The CLI is the same catalog from a terminal. And because AI tools increasingly write the first draft, the whole catalog is published in machine-readable forms (registry.json, llms.txt, an installable Skill) so a model can fetch real parts instead of improvising lookalikes:', 'npx @kajisho5/kataui add sidebar calendar qr-code', 'Start at Getting Started for the three-step version, or open Components and take what you need.'),
    ('What it is not', 'Not a framework: there is no KATA way to fetch data, route pages or manage state — your stack keeps those jobs. No hosted service: the site is a catalog. And not a React library: the parts are deliberately framework-free, which is what lets them drop into Astro, Laravel, Rails, Django, WordPress or a single HTML file unchanged.', None, None)]),
  ('getting-started', 'Getting Started', 'From zero to a working part in three steps.',
   [('Start with the tokens', 'Every part reads its color, spacing, radius and motion from one file. Load it once, before anything else:', '<link rel="stylesheet" href="https://kata-ui.dev/tokens.css">', 'That file is the mold. Parts never hard-code a color, so this one link is what makes the whole catalog look like one product.'),
    ('Copy a part', 'Open the part in Components and copy its three files: the HTML from the preview, the CSS, and the JS when it has one. Paste them into your project as they are. There is no install step and no package to keep updated — the code becomes yours, which is the point.', None, 'If the part says "Uses:" under its preview, it builds on another part (a Modal on Buttons, a Command palette on Kbd). Include that part\u2019s CSS too; the page names it.'),
    ('Works anywhere HTML does', 'Plain HTML files, Astro, Laravel Blade, Django and Rails templates, WordPress themes. If it renders HTML, KATA parts drop in unchanged — no framework island, no build plugin, no runtime.', None, 'For AI tools and installers, the whole catalog is also published as registry.json in the shadcn registry format, and as llms.txt for models that read the web.')]),
  ('cli', 'CLI', 'Install parts from your terminal instead of copy-pasting.',
   [('Get the CLI', 'The CLI is a single Node file with no dependencies (Node 18+). Run it from npm, nothing to install:', 'npx @kajisho5/kataui list\nnpx @kajisho5/kataui add button', 'It reads the same registry.json this site publishes for AI tools — the CLI is a friendlier reader of the same catalog. Prefer a file you keep? The same CLI is one download \u2014 curl -fsSL https://kata-ui.dev/cli/kata-ui.mjs -o kata-ui.mjs \u2014 then run it with node.'),
    ('Add parts', 'init writes the design tokens. add writes a part — and everything it depends on — into ./kata by default:', 'npx @kajisho5/kataui init\nnpx @kajisho5/kataui add button select\nnpx @kajisho5/kataui add login', 'Blocks and templates install the same way: add dashboard writes the whole page. Theme presets too — add indigo writes the theme CSS. Pass --dir to choose another folder.'),
    ('Then load the files', 'Link tokens.css first, then the part CSS, and paste the HTML in as it is:', '<link rel="stylesheet" href="kata/tokens.css">\n<link rel="stylesheet" href="kata/components/button/button.css">', 'Nothing phones home and nothing updates itself afterwards: the files are yours, like a copy-paste that typed itself.')]),
  ('theming', 'Theming', 'Change the tokens; the parts follow.',
   [('One surface', 'Parts reference only var(--k-…) tokens. To restyle everything, redefine tokens after tokens.css loads — never edit a part\u2019s CSS. An accent change is five lines:', ':root{ --k-accent:#1e50a2; --k-accent-ink:#223a70; --k-accent-bg:rgba(30,80,162,.08); --k-accent-bg-strong:rgba(30,80,162,.1); --k-accent-line:rgba(30,80,162,.18); }', 'The Themes page ships five presets in exactly this form, each as a small CSS file you can download or copy.'),
    ('Shape and motion are tokens too', 'Radius (--k-radius, --k-radius-lg), durations (--k-dur-1…3) and the easing curve are tokens. Tighten the whole product by tightening the mold; loosen one part and it stops matching its siblings.', None, 'One token is off-limits by design: --k-core, the vermillion at the center of active controls. It is the signature and stays fixed.')]),
  ('dark-mode', 'Dark Mode', 'One attribute flips every part.',
   [('The attribute', 'Put data-theme="dark" on the root element — or on any container — and every part inside flips. The tokens carry both themes; parts do not know which one they are in:', '<section data-theme="dark"> …parts… </section>', 'The Light/Dark toggle on every component page is this attribute, applied to the preview stage.'),
    ('What flips, what holds', 'Backgrounds, ink, lines, tracks and the accent ink (brighter in the dark) are theme tokens. The zinc scale underneath stays the same family, so a dark page still reads as the same product.', None, 'There is no automatic prefers-color-scheme switch built in: which theme a page wears is the page\u2019s decision. Setting the attribute from a media query in your own CSS is one line.')]),
  ('accessibility', 'Accessibility', 'What the parts guarantee, and what stays yours.',
   [('Native first', 'Where the platform has the element, the part is the element: dialog for Modal and Drawer, details for Accordion, real radio inputs for Segmented and Radio. Focus traps, Escape handling and screen-reader semantics come from the browser; no script re-implements them.', None, 'Interactive parts document their keyboard behavior on their own page, under Accessibility.'),
    ('Focus, motion, contrast', 'Focus rings are a token (--k-ring), visible in both themes, and never removed without a replacement. The Motion line and the Drawer honor prefers-reduced-motion. Text colors come from the zinc scale at weights chosen to stay readable on their backgrounds.', None, 'Parts are a starting point: labels, heading order and the meaning of the page remain the page\u2019s responsibility. Test with a keyboard and a screen reader before shipping.')]),
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
   [('Fetch the parts with the CLI', 'Run the CLI into public/ so Astro serves the files as static assets:', 'curl -fsSL https://kata-ui.dev/cli/kata-ui.mjs -o kata-ui.mjs\nnpx @kajisho5/kataui init --dir public/kata\nnpx @kajisho5/kataui add button switch card --dir public/kata', 'init writes tokens.css; add writes each part’s CSS and JS next to it, dependencies included.'),
    ('Link them in your layout', 'In src/layouts/Layout.astro, load the tokens first, then the parts you use — once, for every page:', '<link rel="stylesheet" href="/kata/tokens.css">\n<link rel="stylesheet" href="/kata/button.css">\n<link rel="stylesheet" href="/kata/switch.css">', 'KATA CSS is global by design, which suits Astro: load it in the layout instead of a component’s scoped style block, and every page shares the same mold.'),
    ('Paste parts into pages', 'Copy a part’s HTML into any .astro file — frontmatter expressions work inside it like anywhere else. A part’s JS is a plain script: paste it into a script tag at the end of the page, or serve the file and reference it.', None, 'No island, no hydration, no client framework. The parts were never components in the framework sense; Astro’s HTML-first model is exactly the ground they were cast for.')]),
  ('install-laravel', 'Laravel', 'Blade templates are HTML with echoes — KATA parts drop in unchanged.',
   [('Fetch the parts with the CLI', 'Run the CLI into public/ so the files are served as static assets:', 'curl -fsSL https://kata-ui.dev/cli/kata-ui.mjs -o kata-ui.mjs\nnpx @kajisho5/kataui init --dir public/kata\nnpx @kajisho5/kataui add button switch data-table --dir public/kata', 'init writes tokens.css; add writes each part’s CSS and JS next to it, dependencies included.'),
    ('Link them in your layout Blade', 'In resources/views/layouts/app.blade.php, load the tokens first, then the parts — once, for every view:', '<link rel="stylesheet" href="{{ asset(\'kata/tokens.css\') }}">\n<link rel="stylesheet" href="{{ asset(\'kata/button.css\') }}">', 'Serve a part’s JS the same way, with the defer attribute, at the end of the layout.'),
    ('Paste parts into views', 'Copy a part’s HTML into any Blade view. Echoes and directives work inside the markup as usual — a @foreach over your models can stamp out cards, rows and list items from a single pasted part.', None, 'If the project builds front-end assets with Vite instead, the same files can live under resources/ and be imported unchanged; they are plain CSS and JS either way.')]),
  ('react', 'React & Next.js', 'KATA parts are plain HTML, CSS and JS \u2014 which means they paste into JSX like any other markup. That is the whole integration.',
   [('Paste it like markup', 'A KATA part is HTML, CSS and, when it behaves, one plain script. Inside a React component the HTML goes in as JSX: rename class to className, for to htmlFor, and camelCase the SVG attributes \u2014 the same renames as any pasted markup. Nothing else about the part changes, because there was never anything framework-specific in it.', 'export function EmptyState() {\n  return (\n    <div className="k-card">\n      <div className="k-card-h">No projects yet</div>\n      <div className="k-card-b">\n        <p>Your first project is one paste away.</p>\n        <button className="btn btn-pri btn-md" type="button">New project</button>\n      </div>\n    </div>\n  );\n}', 'The CSS is the other half of the part. It is global by design \u2014 import it once, at the app root, and every component shares the same mold.'),
    ('Load the CSS once', 'Tokens first, then the parts you use \u2014 or the one-file bundle while you are evaluating. Fetch the files with the CLI (add writes each part and its dependencies) or copy them from the part pages:', "import './kata/tokens.css';\nimport './kata/button.css';\nimport './kata/card.css';", 'Do not scope KATA CSS inside a component. The parts expect the tokens on the page, the way a stylesheet expects a document.'),
    ('The JS parts', 'A part\u2019s script finds its root by a data attribute and initializes what it finds, keeping its state in the DOM. The bundle does this for everything on the page at load, so parts rendered with the page initialize like anywhere else. A part that mounts later \u2014 a dialog opened after client-side navigation \u2014 needs its script run once its markup exists. The per-part files are small, plain and safe to run from an effect:', "useEffect(() => {\n  const s = document.createElement('script');\n  s.src = '/kata/dialog.js';\n  document.body.appendChild(s);\n}, []);", 'Most of the catalog needs no script at all: Accordion is native details, Switch and Rating are real inputs, the charts are SVG. The scripted parts are the overlays, pickers and rich inputs \u2014 and each names its no-JS fallback on its own page.'),
    ('Next.js, specifically', 'Server Components render KATA markup unchanged \u2014 it is HTML on its way to the browser. Load the CSS in the root layout, the bundle with next/script, and client components use the same parts wherever they render:', "// app/layout.tsx\nimport Script from 'next/script';\n\n<link rel=\"stylesheet\" href=\"/kata/tokens.css\" />\n<link rel=\"stylesheet\" href=\"/kata/kata-ui.css\" />\n<Script src=\"/kata/kata-ui.js\" strategy=\"afterInteractive\" />", 'App Router and Pages Router behave the same here, for the same reason: neither is doing anything to the markup.'),
    ('Islands are the natural fit', 'Astro\u2019s model \u2014 HTML first, JavaScript only where a part behaves \u2014 is the ground KATA was cast for: static parts ship zero JS and interactive ones carry their own small script. The Astro install guide walks it end to end. The same applies in miniature to islands inside other frameworks: a KATA part is an island that never needed the word.', None, None),
    ('Known limits', 'KATA is not a React library, and this page is not a claim that it replaces one. If a screen\u2019s state is the product \u2014 a spreadsheet grid, a shared canvas, a wizard whose every step depends on the last \u2014 a framework earns its keep, and you should use it, with KATA\u2019s tokens and CSS still welcome inside. Where React is ceremony around what is mostly a document \u2014 pages, forms, dashboards, settings, checkout \u2014 the parts paste in and the ceremony becomes optional.', None, 'A fair number of teams will run both: the framework inside the product, KATA on everything around it.')]),
  ('javascript', 'JavaScript', 'What the scripts do — and what still works without them.',
   [('Plain scripts, data hooks', 'A part’s JS is a single plain script: no imports, no framework, no build. It finds its root by a data attribute (data-dp, data-combo, data-tags…) and keeps its state in the DOM — classes and ARIA attributes you can inspect. Copy it next to the HTML and it runs.', None, 'In the one-file bundle each script is wrapped in its own function scope, so parts never collide with each other or with your code.'),
    ('What works with no JavaScript', 'More than you might expect. Accordion is native details. Rating and Segmented are radio inputs. Switch and Checkbox are checkboxes. Marquee, Aurora, Beam Border and the charts are CSS and SVG. These parts are complete with the script tag deleted.', None, 'Parts that do need JS say so by having a JS tab — and they degrade: Tag Input falls back to a plain text field, Combobox to a text input, the Date Picker to a text input.'),
    ('Behavior contracts', 'Interactive parts document their keyboard behavior on their own page, under Accessibility. The shared rules: Escape closes what is open and returns focus, arrows move within a part, and nothing ever traps the pointer. Motion parts check prefers-reduced-motion once and honor it.', None, 'If a part’s script fails to load, the page still renders — behavior is layered on markup, never generated by it (the Date Picker calendar grid is the one exception, and it is labelled as such).')]),
  ('guide-dashboard', 'Guide: Building a Dashboard', 'The parts, in the order a reader’s eyes take them.',
   [('Start with the frame', 'A dashboard is the App Shell block and then restraint. Sidebar navigation, a top bar, and a content column — the shell is already composed from the catalog’s own parts, so the page inherits the mold for free. Resist adding a second navigation pattern inside the content; one way to move is a feature.', None, 'Below 720px the shell hides its sidebar. Whatever your page adds must survive that: if a control only exists in the sidebar, it needs a second home.'),
    ('Numbers before charts', 'The first row is Stat Cards — three or four numbers with deltas, because most visits answer one question: is it up or down? Charts come second, and one chart per question. The Line Chart shows change, the Donut shows share, the Bar Chart compares. A dashboard with six charts answers nothing; it performs analysis instead of providing it.', None, 'Every chart in the catalog states its conclusion in its accessible label. Keep that habit in your own charts: the sentence first, the picture second.'),
    ('Tables carry the work', 'Below the fold, a Data Table with sortable columns and row selection does the actual job of the page. Keep rows to the fields people compare, put the row’s main action first, and let the footer paginate with real counts. If a table needs fourteen columns, use a detail page instead.', None, None)]),
  ('guide-settings', 'Guide: Building a Settings Page', 'Grouped switches, saves that report what they saved, and no settings that do nothing.',
   [('Group by consequence', 'Order groups by how much damage a wrong toggle does: profile, notifications, billing, danger. The Settings block ships this shape — a rail of groups on the left, forms on the right, and the destructive group last, in red, far from the save button it does not belong to.', None, 'A setting that takes effect immediately gets a Switch. A setting that needs a save gets inputs and a button. Mixing the two in one group teaches users that saving is optional, and they will believe you at the worst moment.'),
    ('The save contract', 'If the page has a Save button, it saves everything on the page or it says exactly what it did not save. Show the saved state — a Toast, a timestamp, a disabled button that wakes on the next edit. Never let a user wonder whether the click landed.', None, 'Validation belongs to the Field part: label, hint, error, in that order, with the error replacing the hint rather than pushing the layout down the page.'),
    ('Danger gets its own room', 'Delete-account, revoke-keys, cancel-plan: these live in their own group, behind an Alert Dialog that names the consequence in the button itself — “Delete workspace”, not “Yes”. The dialog is not friction; it is the feature.', None, None)]),
  ('guide-pricing', 'Guide: Building a Pricing Page', 'Three plans, one switch, and prices that survive the toggle.',
   [('The toggle is a Switch', 'Monthly/yearly is the Pricing block’s own composition: a Switch flips data attributes on the prices, so the numbers in the page are the numbers that were checked. Never compute prices in the browser from a formula nobody audited — write both prices down, in the markup, where a reviewer can diff them.', None, 'Yearly shows the monthly-equivalent price with the saving stated once, plainly. “Save 17%” is a claim; make sure it is arithmetically true on every plan, including the free one.'),
    ('One plan is the answer', 'Three plans, the middle one marked because it is the right default for the reader the page is for. The block’s .plan-hot and its badge exist for exactly one plan. Two highlighted plans is a page that refuses to recommend, and readers can tell.', None, 'Feature lists compare downward: every plan lists what it adds over the one before. A grid of forty checkmarks and crosses is a spreadsheet wearing a costume.'),
    ('Under the plans', 'The FAQ block answers the five questions pricing always raises — switching, refunds, seats, taxes, cancellation — and after it, one CTA Band. A pricing page that ends at the table assumes the reader decided; most have not, and the questions are the decision.', None, None)]),
  ('guide-auth', 'Guide: Sign-in & Account Pages', 'The smallest pages in the product, held to the highest standard.',
   [('One card, one job', 'The Login block is a Card with two fields and one primary button, and that is the whole page’s ambition. Every element added to a sign-in page — a banner, a testimonial, a “what’s new” — is measured against the only metric that matters here: does the person get in?', None, 'Errors on auth pages are written for someone who is already frustrated: say what failed and what to try, never which half of the credential was wrong. “Email or password did not match” is both kinder and safer.'),
    ('Password rules, stated before typing', 'If the account-creation form rejects passwords, the rules sit in the Field hint before the first keystroke. Length is the rule that matters; composition rules mostly manufacture Post-it notes.', None, 'Offer the platform’s help: autocomplete attributes (email, current-password, new-password, one-time-code) and the Input OTP part for codes. The browser and the password manager are part of your interface whether you design for them or not.'),
    ('After the door', 'Sign-in succeeds straight into the App Shell. If the session was heading somewhere — a deep link, an invite — it lands there. The welcome-back toast is the most that should mark the occasion.', None, None)]),
  ('guide-forms-pro', 'Guide: Forms, For Real', 'Validation timing, the submit path, and errors that teach — the unglamorous decisions that make a form trustworthy.',
   [('Start from the Field', 'Every control on the page is a Field: label, control, hint, error, in that order, always. The order is the accessibility contract — a screen reader meets the label before the control, and the hint is wired to the input with aria-describedby before any error exists. If a form needs a paragraph of instructions above it, the fields are under-labelled; move the words into the hints, where they are read at the moment of need.', None, 'Required is marked in the label before submit. Optional fields in a sea of required ones say "optional" — pick one convention and let the mold hold it.'),
    ('When to validate', 'On blur, for format; on submit, for everything; on input, only to clear an error already shown. Validating on the first keystroke punishes people mid-word, and validating only at submit makes them hunt. The error appears under the field it belongs to and replaces the hint rather than pushing the layout down — the page must not jump while someone is reading it.', None, 'A format the site can fix, it fixes silently: spaces in a card number, a phone number without its dashes. Correction without a scolding is the friendliest validation there is.'),
    ('The submit path', 'The click disables the button and changes its label to the verb in progress — "Saving…", in words next to any spinner. Success moves focus to the confirmation (a Toast for a small save, a new page for a big one) and failure keeps every value exactly where the user left it, with the summary at the top naming how many fields need attention and linking to each. A form that eats input on failure will be abandoned on the second failure, correctly.', None, 'Double-submit is a client bug before it is a server problem: the disabled state is part of the part.'),
    ('Errors that teach', 'An error names the field, the problem and the fix in one breath: "Expiry is in the past — enter a future date", never "Invalid input". Errors are written for someone already frustrated, possibly on a phone, possibly in a second language. Short, concrete, and free of blame are not softness; they are what makes the next attempt succeed.', None, None)]),
  ('guide-table', 'Guide: Data Tables That Survive Real Data', 'Sorting, filtering and pagination, wired end to end — and the line where a table stops being the right tool.',
   [('Sorting is a contract', 'A sortable column sorts the whole dataset, beyond the visible page, and says so: aria-sort on the header, the direction in the label, a stable order when values tie. One column sorts at a time unless the UI can explain two. Numbers sort as numbers, dates as dates, and names the way the locale expects — a table that sorts "10" before "9" has told the reader it cannot be trusted with their data.', None, 'The default sort is the order the reader would choose: newest first for logs, name for people, status for work queues. If the table needs a manual to open, the default is wrong.'),
    ('Filtering without a framework', 'A search input, a status select, and the table — three parts and forty lines of script. Debounce the input, filter the rows in the DOM for the sizes a page should carry, and let the count in the footer describe the filtered set. Filters are state the reader owns: keep them in the URL when the page is shareable, and never reset them on an unrelated action.', None, 'When a filter excludes everything, the empty state says what was excluded and offers the one click that clears it. An empty table with no explanation reads as data loss.'),
    ('Pagination', 'The footer counts what is shown out of what there is — "21–40 of 312" — and the page size is a choice the reader can change. Paginate the filtered set, keep the sort across pages, and if the data changes under the reader, say so rather than silently renumbering. Infinite scroll suits reading: a table someone acts on needs pages they can return to.', None, None),
    ('Ten thousand rows', 'The limit: a few thousand rows in the DOM is where a plain table stops being kind — layout, find-in-page and screen readers all pay. Past that, paginate on the server and let the part be the presentation of one page of data, which it does unchanged. A virtualized grid with cell editing and frozen panes is a different instrument; that is framework territory, and this guide will not pretend otherwise.', None, 'Most internal tables never get near the limit. Build for the data you have, and let the footer count tell you when the day comes.')]),
  ('ai-prompts', 'AI Prompts', 'Paste-ready prompts that make an assistant build with real KATA parts instead of lookalikes.',
   [('A new page from parts', 'The catalog is published for machines first in this workflow: registry.json carries every part with its files, and llms.txt indexes the docs. A prompt that names those sources gets real parts; one that does not gets an improvisation.', 'Build a settings page using only KATA UI parts from kata-ui.dev. Fetch the part list from https://kata-ui.dev/registry.json, use each part\u2019s own CSS unmodified, style nothing from scratch, and theme only through the tokens in tokens.css. Sections: profile, notifications, danger zone.', 'The same prompt works for dashboards, checkout and landing pages — change the sections, keep the sources.'),
    ('Convert a screenshot', 'Models are good at layout and bad at inventing design systems. Anchoring the conversion to the catalog turns a lookalike into the real parts, with names you can verify on their pages.', 'Recreate this screen with KATA UI parts from kata-ui.dev. For every element, name the part you used and where its code came from. If a piece has no KATA part, say so plainly instead of inventing one.', None),
    ('Restyle, do not rebuild', 'Because parts read tokens and nothing else, a restyle is a token diff. This is the fastest way to feel what the mold buys: the markup does not change at all.', 'Keep this page\u2019s markup exactly as it is. Re-theme it by changing only KATA UI tokens: accent to Ruri (#1E50A2), radius to 10px, dark mode on. Show me the token diff and nothing else.', None),
    ('Add the validation', 'Point the assistant at the forms guide and the Field contract, and the generated code inherits the decisions — timing, placement, wording — instead of re-deciding them per prompt.', 'Add validation to this form following https://kata-ui.dev/docs/guide-forms-pro/ exactly: validate on blur and submit, errors replace hints, the submit button disables with a progress label, and no input is lost on failure.', None),
    ('Make it dark', 'Dark mode in KATA is one attribute, which makes it a one-line prompt — and a good test of whether the assistant actually read the docs or is guessing.', 'Give this page a dark theme the KATA UI way: data-theme="dark" on the sections that need it, no color overrides in the parts. If any part looks wrong, name the token responsible instead of patching the part.', None),
    ('Audit against the mold', 'The mold is written down (KATA.md) and machine-checked (check.py) in the repository, so an assistant can audit foreign code against the same standard the catalog ships by.', 'Audit this code against the KATA UI mold in KATA.md: list every raw color that should be a token, every class used but not defined, and every interactive part missing its keyboard behavior. Do not fix anything yet — report first.', None)]),
  ('why-vanilla', 'Why Vanilla', 'What copy-paste gives you, and what it costs.',
   [('What you get', 'No runtime. A KATA page ships the HTML, CSS and JS you can read in the tab next to this one — nothing transpiles, nothing hydrates, and the dependency list is empty, so there is nothing to audit, patch or be broken by. The code is yours in the plainest sense: fork a part, rename its classes, delete the half you do not need. It will still be running, unchanged, in ten years, because nothing underneath it can be deprecated.', None, 'This is also why AI tools are good at KATA: a part is a complete, self-contained answer in one context window. The registry and llms.txt exist so the model copies the mold instead of improvising one.'),
    ('What it costs', 'No components in the framework sense: no props, no reactivity, no tree-shaking. State that spans many parts — a cart, a multi-step wizard with shared data — is yours to wire, and past a certain size a framework earns its keep. KATA’s bet is that most pages are not that size: they are forms, tables, dashboards and marketing sections, and for those the framework was never the point.', None, 'The line: if your app is a document with behavior, vanilla wins. If it is a program with a document attached, use the framework — and KATA’s tokens and CSS still drop into it unchanged.'),
    ('Why copy-paste', 'A package makes the library’s roadmap your roadmap: upgrades, breaking changes, abandonment. Copied code has no roadmap. shadcn proved the model for React; the trade is the same in vanilla — you own the code, including its bugs, and in exchange nobody can take it away, sunset it, or put it behind a pricing page.', None, None)]),
  ('the-mold', 'The Mold', 'How every part is made, and the checks it has to pass before it exists.',
   [('One mold', 'Kata — 型 — is the Japanese discipline of the form: the pattern from which things are cast, and the practice that keeps the casting true. Every KATA part is built to one production standard: same file layout, same tokens, same class grammar, same accessibility contract. The consistency is not a style guide people try to remember; it is a checklist a program enforces.', None, 'Two parts built months apart should look like they were built on the same day, by the same hand. The mold is how a library with one author keeps that promise.'),
    ('The checks', 'Before a part ships, a checker reads its files the way a casting inspector reads a mold. Required files present. Metadata complete. No raw color anywhere — tokens only, because a hard-coded hex is a part that will not survive a theme. Every class used in the preview actually defined. Icons drawn on the 24-grid at stroke 2, from three shapes: circle, 45-degree line, rounded corner. A part that fails does not ship; the count on the homepage only ever counts parts that passed.', None, 'The checker is in the repository (check.py) and the standard is written down (KATA.md), so anyone can inspect the mold.'),
    ('The signature', 'One color is reserved: a vermillion core, #EB471F, that appears only at the center of active controls — the dot inside a checked radio, the core of an on switch, the end point of a line chart, and one quarter of the logo itself. Never on a surface, never as text, never changed by a theme. It is how you can tell a KATA part at a glance, and how the parts tell you where the action is.', None, None)]),
  ('anatomy', 'Anatomy of a Part', 'What is inside every folder in the catalog.',
   [('The files', 'A part is a folder: preview.html (the markup, exactly as you copy it), the part’s CSS, a JS file when the part behaves, and meta.json. Examples, when a part has them, live in examples.html and render on the part’s page under the preview. What you see on the site is the part itself, loaded live.', 'components/button/\n  preview.html   the markup\n  button.css     the styles\n  button.js      the behavior (when any)\n  examples.html  variations (when any)\n  meta.json      title, category, usage, accessibility', 'Blocks are folders too, with one addition: meta.json names the parts they use, and their previews load those parts’ CSS — a block is a composition, never a re-implementation.'),
    ('The contract', 'Every part reads color, spacing, radius and motion from the tokens and nothing else. Classes follow one grammar. Interactive parts state their keyboard behavior and their no-JavaScript fallback in their metadata, and the part’s page prints both. If two parts disagree about anything, that is a bug in one of them, and the mold decides which.', None, 'Status is printed on every part: stable means the contract is settled; beta means the shape is right but the edges are still being filed. The catalog counts both, and labels both.')]),
  ('from-tailwind', 'Coming from Tailwind', 'For the largest group of visitors: what changes, what does not.',
   [('The mental shift', 'Tailwind puts the design system in your class attributes; KATA puts it in tokens and part CSS. You will write longer stylesheets and shorter markup. A card stops being eleven utilities and becomes .k-card — which means the design can be retuned in one place, and the HTML reads as structure instead of as styling.', None, 'They coexist fine: Tailwind for layout glue in a page, KATA parts for the components. The tokens are plain CSS variables, so a Tailwind config can point at the same values and the two systems stop arguing.'),
    ('Rough translations', 'A few mappings to start: bg-zinc-900 text-white becomes a part on a dark section (data-theme="dark" does the whole subtree). rounded-xl is --k-radius-lg. The accent button is .btn-pri or .btn-accent, one class in place of a recipe of bg-, hover: and focus: classes — hover and focus are in the part, tested once, everywhere. Arbitrary values like w-[340px] stay inline styles in KATA too; the mold is strict about color, relaxed about one-off geometry.', None, 'What you give up: the utility for the one weird case, answered inline. What you get back: a page whose markup a new hire (or a model) can read at a glance, and parts that look related because they are.')]),
  ('vs-shadcn', 'KATA vs shadcn/ui', 'A comparison written by the KATA side, with sources dated.',
   [('The short version', 'shadcn/ui and KATA start from the same conviction: you should own the code — copy it into your project, change it, never rent it back from a package. shadcn casts that idea for React. KATA casts it for everywhere else HTML renders: plain files, Astro, Laravel, Django, Rails, WordPress, email templates, the admin page nobody frameworks. If your product is a React app, shadcn is excellent and this page will tell you so twice. If your stack is anything else, the React door is simply not your door.', None, None),
    ('Where shadcn wins', 'The React ecosystem, first: thousands of projects, snippets, and answers already exist, and a team hiring React developers hires people who know it. Its primitives stand on Radix, whose accessibility engineering — focus management, aria patterns, edge cases in dialogs and menus — is deep and battle-tested. It is TypeScript-first in a way KATA, being plain files, does not try to be. And its design language is the current default for a reason: it is tasteful, consistent, and safe to choose in a meeting.', None, None),
    ('Where KATA wins', 'Adoption cost outside React: a KATA part is three files and no toolchain, so it lands in a ten-year-old Laravel app as easily as in a fresh Astro site. Range: the catalog carries shelves shadcn does not — a Motion line, the KATAYABURI shelf of deliberate showpieces, a Japan genre (wagara patterns constructed from their geometry, a hanko seal, a kintsugi card), charts, and 150 icons cut to one spec. Composed work: blocks and templates ship in this repository. And the machine surface: registry.json, an MCP server, and an installable AI Skill are published by the catalog itself, so an assistant asked for a sidebar installs this Sidebar instead of improvising one.', None, None),
    ('Summary', 'Framework: React and Tailwind, versus none at all. Runtime: React, versus nothing. Distribution: a CLI and registry, versus copy-paste, a CLI and a registry. License: MIT, versus MIT for every part (blocks and templates are the paid line here). Community: enormous, versus one maker and a mold. Neither list is an embarrassment — they are answers to different questions. Choose by the stack you actually ship.', None, 'A fair number of teams will run both: shadcn inside the product, KATA on the marketing site, the docs, and the pages that were never going to be React.')]),
  ('site-faq', 'FAQ', 'About the library itself — licensing, the Pro line, and what is not planned.',
   [('Licensing and Pro', 'Every component and icon in this catalog is MIT-licensed: copy it, ship it, sell what you build with it. Blocks and full templates are the commercial line — sold once, lifetime, no subscription — because composed screens are where the hours actually go. The parts will never move behind the paywall retroactively; a part that is free is free in every future version.', None, None),
    ('Is there a React version?', 'Not today. The parts paste into any stack that renders HTML, including inside React as plain markup for static sections. A native React port, in the shadcn registry format, is the most-requested item on the list and is under consideration — the registry file already published is the first step, since it describes every part in that format.', None, None),
    ('Why no npm package?', 'Because the package would become the product, and the product is the code in your repo. The one-file bundle and the starter kit cover the “just give me everything” case without a dependency. If a package ever ships, it will be a mirror of these files, never the source of truth.', None, None),
    ('Who makes this?', 'One person, in the open, with the mold as the second pair of hands. The repository holds the parts, the checker, and the standard they are built to — issues and corrections are welcome there.', None, None)]),
  ('registry', 'Registry', 'The whole catalog as one machine-readable file — what reads it, and how to mirror it.',
   [('One file, the whole catalog', 'registry.json, served at /registry.json, describes every part, block, template and theme in the shadcn registry format: its name, its type, its dependencies, and the complete contents of its files. Anything that can read JSON can install KATA UI — the file is the API.', None, 'It is regenerated on every build from the same sources as this site, so it can never drift from the pages you are reading.'),
    ('An item, up close', 'A trimmed excerpt of one entry. The files carry their full contents (the CSS below is shortened here for print); dependencies name other registry items the installer must bring along:', '{\n  "name": "sidebar",\n  "type": "registry:component",\n  "title": "Sidebar",\n  "dependencies": [],\n  "files": [\n    { "path": "components/sidebar/sidebar.css", "type": "registry:component", "content": "/* KATA Sidebar … */" },\n    { "path": "components/sidebar/sidebar.js", "type": "registry:component", "content": "// KATA Sidebar …" }\n  ]\n}', 'Types are registry:component for parts, registry:block for blocks, registry:page for templates and registry:theme for themes.'),
    ('Who reads it', 'Three readers ship today. The CLI (npx @kajisho5/kataui add …) resolves dependencies and writes files into your project. The AI Skill teaches coding models the catalog\u2019s shape, so an assistant asked for "a sidebar" installs this Sidebar instead of inventing one. And your own scripts are welcome to it — a generator, a company-internal installer, an audit that diffs the catalog against your codebase.', None, 'For language models that read prose rather than JSON, llms.txt and llms-full.txt mirror the same catalog as text.'),
    ('Mirror it', 'The registry is a static file and the parts inside it are complete, so a mirror works offline and forever: download /registry.json once, serve it anywhere, and point the CLI at it:', 'KATA_BASE=https://your-mirror.example npx @kajisho5/kataui add button', 'Pinning a mirror is also how a team freezes a catalog version while the public one moves on.')]),
  ('forms', 'Forms', 'How forms compose in KATA: the field wrapper, errors in words, and which part takes which job.',
   [('The shape of a field', 'Every control wears the same wrapper — the Field part: a label above, the control, then a hint or an error below, in that order, always. The wrapper is what makes a column of different controls read as one form:', '<div class="field" data-field>\n  <label for="email">Email</label>\n  <input class="input" id="email" type="email" autocomplete="email">\n  <p class="hint">The receipt goes here.</p>\n</div>', 'Labels are text, never placeholders doing double duty: a placeholder disappears exactly when the reader needs it most.'),
    ('Errors that say something', 'An error replaces the hint, in the danger color and in words: what is wrong and how to fix it ("Enter the address the receipt should go to", not "Invalid"). Three wirings make it real rather than decorative: the control carries aria-invalid="true"; the error paragraph has an id the control names in aria-describedby; and on submit, focus moves to a summary at the top listing the problems, each linked to its field.', '<div class="field" data-field>\n  <label for="email">Email</label>\n  <input class="input errb" id="email" type="email" aria-invalid="true" aria-describedby="email-err">\n  <p class="err" id="email-err">Enter the address the receipt should go to.</p>\n</div>', 'Never let color be the only signal: the words carry the error for everyone, the red just helps find them.'),
    ('Grouping and choosing', 'Choices that belong together get a fieldset with a legend — the Radio and Checkbox groups are built that way — because "how did you hear about us" is the label for the whole set. Which control takes the job: one short line is an Input, a paragraph is a Textarea, one of two-to-five visible options is Radio or Segmented, one of many is a Select or a Combobox, a date is a Date Picker, a time is a Time Picker, several values are a Tag Input, a path down a tree is a Cascader, and assigning many things at once is a Transfer.', None, 'Attached pieces stay attached: money gets an Input Group (the ¥ is part of the control), and the form\u2019s actions are a right-aligned row of Buttons — the primary one once, at the end.'),
    ('Required fields', 'Mark required fields in the label text ("Email (required)") or mark the optional ones — pick one convention per form and keep it. Star-only marking fails everyone who cannot see the star\u2019s legend, and there is always a legend nobody reads.', None, None)]),
  ('mcp', 'MCP Server', 'The catalog as an MCP server, so AI tools can browse and fetch real parts.',
   [('Why an MCP server', 'Models improvise interfaces when they cannot see real ones. The MCP server gives a connected AI tool the actual catalog — it can list what exists, search it, and fetch a part\u2019s real files (HTML, CSS, JS) with its dependencies, then write them into your project as they are. It is the registry, served over the Model Context Protocol, from one zero-dependency Node file.', None, None),
    ('Connect it', 'Download the server once, then point your MCP client at it. The configuration most clients accept:', 'curl -fsSL https://kata-ui.dev/mcp/kata-ui-mcp.mjs -o kata-ui-mcp.mjs', '{\n  "mcpServers": {\n    "kata-ui": {\n      "command": "node",\n      "args": ["/path/to/kata-ui-mcp.mjs"]\n    }\n  }\n}'),
    ('The tools', 'Three, deliberately. list_components returns the catalog (optionally one type: parts, blocks, templates, themes). search_components finds candidates by name, title and description. get_component returns one item complete — every file\u2019s full contents and the dependencies to bring along — which is the difference between a model describing a sidebar and installing this one.', None, 'The server is read-only: it serves the catalog and writes nothing, anywhere.'),
    ('Point it elsewhere', 'By default the server reads https://kata-ui.dev/registry.json at first use. Set KATA_BASE to a mirror, or pass --registry with a local file path, to serve a pinned or offline copy — the same mirror story as the CLI:', 'node kata-ui-mcp.mjs --registry ./registry.json', None)]),
  ('rtl', 'RTL', 'Right-to-left needs one attribute: set dir and the catalog follows.',
   [('One attribute', 'There is no RTL build, no .rtl variant and nothing to download twice. Write direction into the document and the same files lay out right-to-left:', '<html lang="ar" dir="rtl">', 'It works on any container, too — dir="rtl" on a section flips that section only, which is how mixed-direction pages are usually built.'),
    ('What mirrors', 'The site chrome and the structural parts are written with logical properties — inline-start and inline-end instead of left and right — so sidebars trade sides, menus open from their other edge, panels anchor to the new start, form groups and button seams join in the new direction, and breadcrumbs, pagination and navigation follow. Flex and grid layouts follow direction on their own; the Switch knob, which moves on a physical track, carries an explicit flip rule.', None, 'Text alignment follows too: start-aligned in LTR is start-aligned in RTL, and numeric columns align to the end in both.'),
    ('What deliberately does not', 'The showpieces keyed to physical coordinates stay physical: the Spotlight beam follows a cursor, the Comparison seam divides a picture, the Aurora washes drift where they drift, and the Drawer slides from the side it was built for. Direction changes reading order; effects keep their choreography. Directional icons — arrows, chevrons, the little plane on a send button — are glyphs, and flipping a glyph is a design decision left to the page.', None, 'The vermillion core sits at the center of active controls. Centers have no direction, so the signature survives the flip untouched.')]),
  ('contributing', 'Contributing', 'Add a part without breaking the mold.', [('The mold is the application form', 'A contribution to KATA is a part cast from the same mold as every other part. There is no separate review aesthetic: if the part passes the checker and follows the written standard, it belongs. The standard is KATA.md in the repository and the checker is check.py; both are public, so a part can be finished \u2014 really finished \u2014 before a maintainer ever sees it.', None, 'Parts that fail the checker do not ship. That is not gatekeeping; it is the product.'), ('Start from the template', 'Every part is a folder: meta.json, preview.html, the part CSS, and JS only when the part moves. Copy the template folder, name it, and build inside it:', 'cp -r template/ components/my-part\npython3 check.py', 'The preview is the documentation: if the preview cannot show every state of the part, the part is not ready.'), ('What the checker reads', 'Tokens only \u2014 no raw color anywhere, because a hard-coded hex is a part that will not survive a theme. Every class in the preview defined. Icons on the 24 grid, stroke 1.7, three shapes only. All states finished: hover, active, focus-visible, disabled, empty, overflow. Motion between 130 and 220ms with no bounce, and a prefers-reduced-motion answer for anything that moves. The vermillion core appears only where it already lives; a new part does not invent a new place for it.', None, 'The full standard, including the fine-detail rules, is section 0.6 of KATA.md.'), ('Then open the pull request', 'Describe the job the part does and the screens it serves. The issue and pull request templates ask the mold questions up front \u2014 tokens, states, motion \u2014 so review starts from answers instead of questions. One part per pull request keeps the casting inspectable.', None, 'A part that needs a new token starts as a token proposal in an issue: tokens change the whole mold.')]),
  ('changelog', 'Changelog', 'What shipped, newest first.',
   [(
 'November 3, 2026 \u2014 Pro, itemized', '<p>The Pro band on the front page talked about hours and hourly rates and never named a single thing it sells. It now lists the whole shelf \u2014 all 21 blocks and 7 templates, each a chip linking to its live page, so the offer can be inspected piece by piece before it can be bought. The email form leaves the front page with it: the launch list lives on the pricing page now, next to the terms it belongs with.</p>', None, None),
    (
 'November 3, 2026 \u2014 Nothing on the front page twice', '<p>The front page was showing some parts three and four times over \u2014 the same line chart in the casting bench, the product screen and the Lab collage, the same ambient tiles in the Motion band and both shelves below it. Each part now holds one stage: the bench casts a Bar Chart and the Donut, the product screen keeps the Line Chart and the Data Table, the collage is Stat Cards, a Kanban board, a Calendar and a Sparkline, and the Lab shelves trade in parts the band is not already showing. The swap surfaced a real defect, too: a tile is a dark panel wherever it sits, but its token scope followed the page around it, so preview text written in part tokens rendered dark-on-dark on the light page. Every tile now carries its dark scope with it. And the two Beams \u2014 two parts that share one class name \u2014 are never loaded on the same page again.</p>', None, None),
    (
 'November 3, 2026 \u2014 The front page, rebuilt around the message', '<p>The hero now leads with the only two sentences that matter \u2014 \u201cVanilla HTML, CSS and JS\u201d and \u201cCopy the code. Own the design\u201d \u2014 with the counts demoted to a footnote line, the pattern backdrop retired, and the casting bench directly underneath: accent, radius, motion and mode re-cast real Buttons, Inputs, a Card and two Charts (the beta parts are labeled, here as everywhere). \u201cThree ways in\u201d shows copy-paste, the one-file CLI (real output, dependencies and all) and the registry side by side, with the honest comparison: an AI improvising drifts; an AI fetching checked parts does not. The showcase is no longer four framed pages but one composed product screen \u2014 sidebar, chart, form and a sortable data table, every control live, every part on the screen named in the manifest below it. The comparison table gained its third column and the two rows that decide it: AI friendliness, and quality without React.</p>', None, None),
    (
 'November 3, 2026 \u2014 Dark mode, repaired where it was actually broken', '<p>Two honest defects, found by looking. The template demo pages carried no theme script at all, so they rendered light forever \u2014 inside the front page\u2019s new live tabs that meant a white slab in a dark page. Demos now read the same cast state as the rest of the site, fall back to your system preference when no cast exists, and follow live when the mold is re-cast in the parent page. And the casting controls inside the light stage on the front page read the site\u2019s chrome tokens, which do not re-scope \u2014 their pills went black-on-white; they now read the part tokens, like everything else in the stage.</p>', None, None),
    (
 'November 3, 2026 \u2014 Whole pages, a bigger motion shelf, and time priced out loud', '<p>The template cards become four live tabs \u2014 Dashboard, Inbox, Settings, Checkout, each the real template running in the page, loaded only when opened, captioned without apology: not a screenshot. Motion steps up the page as four large live tiles under one argument, <b>Motion, on duty</b>. The comparison now closes on a billboard \u2014 KATA is for everywhere else \u2014 with a two-column summary on phones. Pro states its arithmetic on the page: &asymp;77 hours of assembly, $129 once, $1.68 an hour, the do-it-yourself bar against the minutes bar. The FAQ leads with the two questions that actually block people \u2014 React, and whether free stays free \u2014 and the page ends on an action: Start with one part.</p>', None, None),
    (
 'November 3, 2026 \u2014 One mold, second on the page', '<p>The front page is re-sequenced around its proofs. The live-cast panel becomes <b>One mold</b>: the token file\u2019s promise as the headline, five specimens including a composed card, and the casting controls set into the section itself \u2014 accent, radius and mode, writing the same state the Foundry deck keeps, so what you cast here follows you across the site. How it works follows the showcases and shows the real token file in Step 1; the principles shed their first rule to the mold section and stand as two.</p>', None, None),
    (
 'November 3, 2026 \u2014 The front page, given a louder first three seconds', '<p>The hero headline steps up to 64px, the stats now count all 370 icons and marks, and the App Shell frame names itself LIVE \u2014 hover it and its panels answer with their part names, App Shell, Stat Cards, Data Table. A shared LIVE chip now marks every real, copyable surface on the page. Section headings step up a class, proof sections breathe at 96px, the two sumi panels agree on one black, and the mobile hero \u2014 eyebrow and CTAs \u2014 is measured and fixed at real width.</p>', None, None),
    (
 'November 3, 2026 \u2014 Sixteen seconds, one settings page', '<p>The front page now carries the proof as a recording: a settings page assembled from catalog parts in a single take \u2014 twelve pastes, a real on-screen timer, no cuts and no code written on camera. Sixteen seconds, because the styling was already done inside the parts. The finished page is the Settings template, which runs live one click away.</p>', None, None),
    (
 'November 3, 2026 \u2014 Cast together: compositions on the part pages', '<p>Eleven part pages grow a Cast together section: live compositions \u2014 a subscribe row, a scoped search, feature flags on a card, a rename dialog, a roster \u2014 each copyable as one scene, with the parts in it named. Building them exposed two single-instance assumptions, now fixed in the parts themselves: Modal and Toast each bind every opener and container on the page, not just the first.</p>', None, None),
    (
 'November 3, 2026 \u2014 Traditional colors, shown large', '<p>The fifty traditional colors of Japan get room to breathe: each card is now a full dye-band with its name set large, every family carries a Cast this theme button that casts its lead color and copies the whole token set as a ready theme file, and the casting strip at the top grows a switch and a small card dyed by the cast \u2014 border, wash and ink following the color you picked.</p>', None, None),
    (
 'November 3, 2026 \u2014 A door for React on the front page; the bench, promoted', '<p>The front page now speaks to React teams directly: framework-free is not framework-hostile \u2014 paste the markup into JSX, load the CSS once, mount the JS parts as islands \u2014 with the field guide one click away. The Design System bench takes the top of its page under its true name, One token, everything moves, and its specimen row grows a full card and a progress bar, so a single cast visibly re-casts a composed surface, not just loose controls.</p>', None, None),
    (
 'November 3, 2026 — Full-page demos, two guides, and the itemized shelf', '<p>Every template now runs full-screen at its own demo address — no site chrome, the real page, one click from its detail page. The showcase cards carry their composition (parts in; hours by hand versus minutes with Pro), and the shelf is openly first-party until outside builds join it. Two new guides go deep where pages actually fail: forms (validation timing, the submit path, errors that teach) and data tables (sorting as a contract, filtering, the honest limit at ten thousand rows) — plus an AI prompt library of six paste-ready prompts that make an assistant fetch real parts instead of improvising them. Pricing now itemizes all 28 Pro artifacts, states the Founding 100 terms, and walks the post-checkout path before asking for anything.</p>', None, None),
    ('November 3, 2026 — Vanilla, stated plainly; a door for React', '<p>Three changes aimed at the first five minutes. The homepage hero now leads with the whole proposition — <b>Vanilla HTML, CSS and JS. No framework. No build step.</b> — and the live mold demo sits directly under the hero, where a first visit meets it. A new docs page, <a href="/docs/react/">React &amp; Next.js</a>, shows the whole integration honestly: paste as JSX, load the CSS once, run a part\u2019s script when it mounts — and where a framework genuinely earns its keep instead. Pricing now draws its arithmetic: the composed shelf\u2019s ≈77 hours of assembly, priced at three hourly rates against $129 once.</p>', None, None),
    ('November 3, 2026 \u2014 One hundred, patterns only', '<p>Forty-two more patterns join the loom, every one a continuous field: staggered and diagonal checks, stone paving and rough stone walls, houndstooth, twill weave, basket weaves, nested hemp stars and nested seven treasures, abacus beads, crescent moons, linked squares and doubled lattices. The count is back to <b>one hundred</b> \u2014 and this time the hundred are all patterns, no pictures among them.</p>', None, None),
    ('November 3, 2026 \u2014 Patterns, only patterns', '<p>The loom is pruned from one hundred patterns to <b>fifty-eight</b>. The pictorial motifs \u2014 the crane, the rabbit, the butterflies and dragonflies, the flower medallions and gourds \u2014 are retired. What stays is what a wagara is: a continuous field that tiles without a seam or a centre. Tortoiseshell, hemp stars, thunder spirals, linked chains, diamond lattices, stone walls, mist, rain and willow. Fewer patterns, all of them patterns.</p>', None, None),
    ('November 2, 2026 \u2014 One hundred patterns on the loom', '<p>The Wagara loom goes from twenty-two patterns to <b>one hundred</b>. Waves and hemp stars now keep company with thunder spirals, linked manji and scale-weights, tortoiseshell with flowers inside, coins, chains and stone walls, mist, rain, willow and ripples \u2014 and a whole garden: chrysanthemum and plum, double cherry, iris and bellflower, peony and butterflies, cranes, dragonflies and rabbits. All seventy-eight additions are drawn from their constructions like the first twenty-two, and each was checked on contact sheets \u2014 the maple, the tomoe swirl and the quince took more than one pass to read true.</p>', None, None),
    ('November 2, 2026 \u2014 Twenty-two patterns on the loom', '<p>Wagara doubles its shelf: twelve more classical patterns, each still drawn from its construction, never pasted. Sayagata interlocks its silk fret so no line ever ends; Kagome is the true trihexagonal bamboo lattice; Karakusa curls are drawn as spirals joined by vine arcs; Ryusui flows in phased waves with eddies; Tatewaku stands its paired waves up; Yukwa rounds the snowflake into notched medallions; Ajiro weaves its strips over and under; Sankuzushi lays the counting rods down in alternating blocks; Higaki doubles its diagonal fence; Hanabishi sets a flower inside the diamond; Watsunagi links ring into ring; and Bishamon-kikko works its tortoiseshell hexagons with triangles, the way the guardian armor is drawn. Twenty-two patterns, three tones, the same tokens.</p>', None, None),
    ('November 2, 2026 \u2014 The front door, rebuilt', '<p>The homepage was re-sequenced around the first visit. The hero now carries the proposition, the two actions and the record \u2014 136 components, 0 dependencies, Mold Verified \u2014 and nothing that moves. How it works moved up to second place, the first five parts to copy sit under it, and the live re-casting demo moved down into its own section, The mold, live. The full catalog no longer rides on the homepage (307 KB became 98 KB); it lives on its own page, where it belongs. Motion and KATAYABURI now sit at the bottom in a marked experimental zone, The Lab, and their pages and catalog sections say so. The docs index opens with three starting pages and splits browsing by part from browsing by job. Pro is described the way it is: in preparation, behind a finished free product.</p>', None, None),
    ('November 2, 2026 \u2014 Relations, freshness, and the map', '<p>The catalog learned to point sideways. Part pages now show what a part is often cast with, computed from the blocks that use it, next to the blocks themselves. The components index filters by Stable and Beta. The homepage gained a First five to copy and a Fresh from the mold strip fed by this changelog. The footer carries the live mold-check count. The Design System page maps every place the vermillion core may appear \u2014 generated from the CSS, so the map cannot lie. The Icons page states the brand-mark rules plainly, and a Contributing doc plus mold-checked issue templates open the door to outside castings.</p>', None, None),
    ('November 2, 2026 \u2014 Cards, unnested', '<p>Ten catalog cards were quietly broken in every browser \u2014 Breadcrumbs, Pagination, Sidebar, Bottom Navigation, List and five more \u2014 showing an empty stage and no title. Their previews contain links, and the catalog card is itself a link: HTML forbids an anchor inside an anchor, so the parser closed each card at the first preview link and scattered the rest. The gallery stage is inert by design, so preview links are now cast as spans that keep their classes and their look, and the build asserts no anchor survives into a stage. The check that missed this is also fixed in kind: the catalog is now verified structurally \u2014 every card must arrive in the browser with its title and a populated stage \u2014 not just sampled.</p>', None, None),
    ('November 2, 2026 \u2014 The bundle learns to date itself', '<p>A reader\u2019s phone showed the catalog with several previews stripped bare \u2014 OTP boxes, radios, the calendar \u2014 while everything else wore its styles. The cause sat in the catalog page itself: every other stylesheet on the site carries a content-hash version, but the one file that changes most, the kata-ui.css bundle the gallery previews wear, was linked bare \u2014 so a phone could hold a stale copy indefinitely while the hashed files around it stayed fresh. The bundle and its JS now carry content versions like everything else. The same pass hardens the form controls for iOS Safari, which keeps its native white fields unless told otherwise twice: text inputs, the OTP boxes, checkboxes and the command input now declare \u2011webkit\u2011appearance alongside the standard property.</p>', None, None),
    ('November 2, 2026 \u2014 Two hundred and twenty marks', '<p>The brand shelf grows up. Every hand-drawn approximation among the marks \u2014 Spotify first, after a reader zoomed in and asked when it would be fixed, then the other twenty-one \u2014 is replaced by the owner\u2019s official glyph, drawn from the Simple Icons set, in the brand files and in every inline copy across the blocks and templates. And the shelf itself widens: 164 more marks join, 220 in all, filed under four new jobs \u2014 Languages &amp; runtimes, Data &amp; backend, Productivity &amp; SaaS, Games &amp; 3D. TypeScript to Zig, PostgreSQL to Snowflake, Gmail to Patreon, Steam to Blender: if a site links to it, signs in with it or pays through it, the mark is probably here \u2014 still nominative use only, still the one exception to the three-shape mold.</p>', None, None),
    ('November 2, 2026 \u2014 The audit, in full', '<p>Every page on the site \u2014 201 of them, both themes, at phone width, 182,000 text elements \u2014 measured for contrast, stray light surfaces, overflow and script errors, and every detail stage clicked through its Light and Dark scopes. One defect family kept surfacing: text paired to the wrong side of a flipping token. Pagination\u2019s current page, the Copy Field button, the Sidebar avatar and mark, and the Tooltip wore <i>on-color</i> white over an ink background that turns light in the dark \u2014 white on white. They now take their text from the page token, the same pairing the Button already used. The three template sidebars sat on a constant zinc-50 while their brand and account text flipped around them; they ride the soft-surface token now. The waitlist button keeps its contrast in the dark, the Live Cast cluster on the home page pins the light scope its card always had, and the Avatar\u2019s initials and the Comparison Slider\u2019s grip hold constant zinc pairs that read in both modes. Everything else the sweep flagged was measured again by eye and found innocent.</p>', None, None),
    ('November 2, 2026 \u2014 Dark, finished', '<p>Dark mode stops being a coat of paint and becomes a scope. The token sheet gains an explicit light scope next to the dark one, so a stage set to Light is actually light on a dark page \u2014 before, it inherited the page\u2019s dark tokens and the toggle changed nothing. Every fixed white in the chrome is tokenized now (cards, the drawer, filters, pricing tiers, template frames), catalog cards hydrate from the same JS bundle the copy button ships \u2014 calendars and cascaders render in the shelf instead of standing empty \u2014 and two block scripts learned to stay inert when their markup is not on the page. On a phone, detail pages open at Mobile stage width; the pricing call-to-action keeps its contrast in both modes; and the single-column detail layout can no longer be stretched past the screen by one long line of code. Audited page by page, in the dark, at phone width.</p>', None, None),
    ('November 2, 2026 \u2014 The mark, restored', '<p>The mark goes back to the four quadrants, on the maker\u2019s call: the three-shape recut from this afternoon is retired the same day it shipped. The restored mark \u2014 ink, an ichimatsu nested in the top-right, zinc, and the vermillion quarter \u2014 returns to the header, favicon, app icons and the OGP card, and the hero cast mark assembles its four quadrants again. One improvement survives the revert: the header mark\u2019s ink cells are currentColor now, driven by the same ink token as the wordmark, so the mark follows the theme instead of being patched for it.</p>', None, None),
    ('November 2, 2026 \u2014 Breakage, mended', '<p>Breakage gets a visual language: kintsugi. A seam of yamabuki gold \u2014 the same token the Kintsugi Card draws its veins with \u2014 now marks the broken and the in-between everywhere on the site. The 404 is a mended plate, its crack run across the panel in gold, with the house rule written under it: shown honestly, mended visibly. The \u2318K preview pane\u2019s casting and unavailable states wear the same seam, and the Design System documents the rule next to the tokens it comes from. Errors are not dressed as success here; they are repaired in the open.</p>', None, None),
    ('November 2, 2026 \u2014 Galleries, benches, taking things apart', '<p>The specimen stops posing and starts working. The <b>Components catalog is a gallery now</b>: every card carries its part live \u2014 the real preview, cast from the same files you copy \u2014 so the shelf is browsable by eye, not by name. Component pages go <b>two-column</b>: the live stage pinned on the left, the code on the right, on a wider canvas. The <b>Design System page is a casting bench</b> \u2014 a foundry floor with live parts and cast buttons for accent, radius and motion, wired to the same saved state as the Foundry deck; the radius specimens in the token tables cast too. And the landing page gains <b>Assembled, then taken apart</b>: the Pricing block composed live from Button, Badge, Switch and Separator, with a switch that explodes it back into its parts. Nothing here is a screenshot; if it looks cast, it was cast.</p>', None, None),
    ('November 2, 2026 \u2014 The mark, recast', '<p>The mark itself is recast. The four-quadrant logo gives way to the three shapes and nothing else: an r2-corner frame, a single 45\u00b0 cut, and the vermillion core sitting at the exact center \u2014 the same geometry the hero cast mark assembles, and the same 24-grid, 1.7-stroke discipline as the icon set. It ships everywhere the old mark lived: header, favicon, app icons, the OGP card. Around it, the specimen grows its second layer: component pages gain a <b>Tokens it reads</b> decomposition (every custom property in the part\u2019s CSS, with live values), stage toggles that demo calm (reduced motion) and keyboard focus in place, a wagara backdrop row in the Foundry deck (Seigaiha, Asanoha, Ichimatsu over the whole page), \u2318K search results that preview the highlighted part live from its own page, a KATAYABURI section that breaks its grid once as it scrolls in and re-forms, and a pricing page that shows its arithmetic: 28 assembled artifacts, 87 composed part-instances, roughly 77 hours of assembly behind the $129.</p>', None, None),
    ('November 2, 2026 \u2014 The living specimen', '<p>The site stops describing the mold and starts being it. A <b>Foundry deck</b> now sits on every page (bottom right): turn the radius, cast one of the five traditional-color accents, flip the whole page between washi light and sumi dark, slow the motion \u2014 every part on the page re-casts at once, because they all read the same tokens. The vermillion core is deliberately not on the deck; it never moves. The landing hero opens with a cast mark \u2014 the three shapes (circle, 45\u00b0 line, r2 corner) assembling around the core \u2014 over a live cluster of the real Button, Switch, Input and Badge, and the Motion line auto-plays below it. Component pages carry a <b>Mold verified</b> chip and a button that copies a ready-made prompt for your AI; joining the waitlist stamps a vermillion \u578b; copying code flashes the core color. The site chrome accent is Asagi now, too \u2014 the last of the old teal is gone.</p>', None, None),
    ('November 2, 2026 \u2014 Type, templated', '<p>Letter-spacing and line-height are fixed values now, not taste: a tracking table lives in the mold (KATA.md \u00a70.5), as --k-ls-* and --k-lh-* tokens, and on the Design System page. Body text takes +0.012em, CJK display +0.06em, CJK never goes negative, and kana readings wrap as whole words. The table exists because the traditional-colors section shipped with body tracking at zero \u2014 the kind of basic a mold is supposed to make impossible to forget. Applied site-wide the same day: every page lead, the docs body, the landing sub-texts and the Japanese page (CJK body +0.04em, headings +0.05em) now follow the table, and an audit of all 164 part stylesheets found their tracking already sitting inside the ramps \u2014 card titles, micro labels, vertical text \u2014 that the table now records explicitly.</p>', None, None),
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

next(d for d in DOCS if d[0]=='changelog')[3].insert(0, ('November 6, 2026 — Mold v5: spacing and type values enforced', 'UI parts now replace raw spacing (762 declarations), font sizes (433) and line heights (84) with the v4 scales, so spacing-values and type-values fail for UI parts; Lab parts keep them as warnings. v5 adds --k-text-code (.86em) for inline code that follows the surrounding text size. Command\'s top offset is now 64px instead of 12vh. No existing token value changes.', None, None))
next(d for d in DOCS if d[0]=='changelog')[3].insert(1, ('November 6, 2026 — Mold v4: complete spacing and type scales', 'The spacing scale gains 1px, 2px, 20px, 28px and 40px steps, the text scale exports 14px and 44px and adds 15px, and leading adds 1, 1.35 and 1.6 from the KATA.md type table. All scales are generated from system/tokens.json. No existing value changes. The next PRs replace 925 raw spacing values, 433 font sizes and 86 line heights in UI parts with these tokens.', None, None))
next(d for d in DOCS if d[0]=='changelog')[3].insert(2, ('November 6, 2026 — Mold v3: visible keyboard focus', 'A Chromium measurement of 444 Tab stops in 98 parts found 380 below 3:1 contrast in light and 156 in dark. --k-ring is now a 2px page-colored gap plus a 2px ink ring, and the tokens.css focus floor is a 2px ink outline; both reach 3:1 in both themes. Parts that use --k-ring require mold v3. JS-driven parts now work with several copies on one page: js-single-instance and js-global-bindings findings reached 0.', None, None))
next(d for d in DOCS if d[0]=='changelog')[3].insert(3, ('November 5, 2026 — Shared mold v2', 'Merged PRs #11 and #13–#22 added stricter checks, audit reporting and a CI ratchet. Recorded Mold Verified totals: '+ ' → '.join(str(x['passed'])+'/'+str(x['total']) for x in mold_history(ROOT)['auditMilestones']) + '; token-values reached 0. Combobox initialization and keyboard handling were rebuilt, shared text contrast was corrected, and reduced motion now leaves host application transitions intact. Mold v2 publishes token compatibility requirements.', None, None))

DOCS += [
 ('mold-changelog','Mold changelog','Versioned token API history, with git evidence.',[]),
 ('update-mold','Update your mold','Upgrade an existing tokens.css without losing your customizations.',[
  ('Check the installed version','Read the first line of your tokens.css, then compare it with the requires mold >= N header on the CSS or JS you are copying. A file without a mold header is legacy v1. Package version and mold version are separate.', 'head -n 1 path/to/tokens.css',None),
  ('Download and compare','Keep a backup. Download the current mold into a new temporary file; do not overwrite your working copy before reviewing the diff.', 'cp path/to/tokens.css path/to/tokens.css.backup\ncurl -fsSL https://kata-ui.dev/tokens.css -o /tmp/kata-tokens-new.css\ndiff -u path/to/tokens.css /tmp/kata-tokens-new.css',None),
  ('Preserve local changes','If you edited tokens by hand, compare against the exact upstream revision you originally copied. Apply your theme overrides after the new mold rather than copying an old :root over it. Review the mold changelog; numbered durations include the multiplier since v2, so remove an extra multiplication. Since v3, --k-ring is 4px wide (2px gap plus 2px ink); check focus rings inside containers that clip overflow. Do not restore removed combo/toast tokens at root. An unknown original revision needs a manual three-way review; do not guess.', 'git diff --no-index path/to/tokens.css.backup /tmp/kata-tokens-new.css',None),
  ('Replace and verify','After reviewing the diff, replace tokens.css and reapply reviewed overrides. Test light and dark, focus states, custom palettes, motion multiplier zero and reduced motion. Keep the backup until those checks pass. Reload uncached assets to avoid mixing old tokens with new components.', 'cp /tmp/kata-tokens-new.css path/to/tokens.css', 'CLI 1.1.0 warns when installed tokens are older than the selected parts require. add never replaces an existing tokens.css, even with --force. After reviewing your diff, use init --force --backup only if you explicitly want the new mold to replace it.')])]

DOC_STYLE = """<style>
.dc h1{font-size:32px;font-weight:600;letter-spacing:-.025em;margin-top:26px}
.dc .lead{margin-top:10px;color:var(--ink2);font-size:15px;line-height:1.85;max-width:64ch;letter-spacing:.012em}
.dc section{margin-top:36px;max-width:68ch}
.dc h2{font-size:18px;font-weight:600;letter-spacing:-.015em}
.dc p{margin-top:9px;font-size:14px;line-height:1.9;color:var(--ink2);letter-spacing:.012em}
.dc pre{margin-top:12px;border:1px solid var(--hair);border-radius:10px;background:var(--soft);padding:13px 15px;font-family:var(--mono);font-size:12px;line-height:1.75;overflow:auto;color:var(--ink)}
.mold-history{overflow:auto;max-inline-size:100%}\n.mold-history table{border-collapse:collapse;width:100%;font-size:var(--k-text-sm)}\n.mold-history th,.mold-history td{text-align:start;vertical-align:top;border-block-end:1px solid var(--k-line);padding:var(--k-space-2)}\n.mold-history code{white-space:normal;overflow-wrap:anywhere}\n.dcgrid{margin-top:24px;display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px}
.dccard{border:1px solid var(--hair);border-radius:12px;background:var(--paper);padding:17px;text-decoration:none;color:var(--ink);display:block}
.dccard:hover{border-color:var(--ink3)}
.dccard h3{font-size:15px;font-weight:600}
.dccard p{margin-top:6px;font-size:13px;color:var(--ink2);line-height:1.7;letter-spacing:.01em}
</style>"""

def docs_index():
    cards = ''.join(f'<a class="dccard" href="/docs/{s}/"><h3>{esc(t)}</h3><p>{esc(d)}</p></a>' for s, t, d, _ in DOCS)
    body = f"""
<div class="wrap dc">
  <h1>Docs</h1>
  <p class="lead">The short version of everything: how to start, how to theme, how dark mode works, and what the parts promise about accessibility. The long version lives on each part's own page.</p>
  <h2 class="dch">Start here — three pages</h2>
  <div class="dcgrid"><a class="dccard" href="/docs/introduction/"><h3>Introduction</h3><p>What KATA is, and what it refuses to be.</p></a><a class="dccard" href="/docs/getting-started/"><h3>Getting Started</h3><p>Tokens in, first part pasted, first screen running.</p></a><a class="dccard" href="/docs/the-mold/"><h3>The Mold</h3><p>Why 136 parts stay consistent: the written standard and the checker.</p></a></div>
  <div class="dcbrowse"><a href="/components/">Browse by part &rarr; Components</a><a href="/blocks/use-cases/">Browse by job &rarr; Use cases</a></div>
  <h2 class="dch">Everything</h2>
  <div class="dcgrid">{cards}</div>
</div>
{FOOTER}
</body>
</html>"""
    return head('Docs — KATA UI', 'Getting started, theming, dark mode and accessibility for KATA UI.', DOC_STYLE) + body

def doc_page(slug):
    entry = next(d for d in DOCS if d[0] == slug)
    _, title, desc, sections = entry
    secs = [changelog_html(ROOT)] if slug=='mold-changelog' else []
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
    shutil.copy(ROOT / 'docs' / 'ROADMAP.md', DIST / 'ROADMAP.md')
    (DIST / 'mold-results.json').write_text(json.dumps(MOLD_REPORT, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
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
    config = json.loads((ROOT / 'system/tokens.json').read_text())['contrast']
    (DIST / 'color-roles.js').write_text((ROOT / 'system/color-roles.js').read_text().replace('__KATA_COLOR_CONFIG__', json.dumps(config)))
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
    _md = ROOT / 'media'
    if _md.exists():
        (DIST / 'media').mkdir(exist_ok=True)
        for _f in _md.iterdir():
            if _f.is_file():
                shutil.copy(_f, DIST / 'media' / _f.name)
    (DIST / 'index.html').write_text(emit(landing(comps, blocks, n_icons, templates), comps, None), encoding='utf-8')
    auditdir = DIST / 'audit'
    auditdir.mkdir()
    (auditdir / 'index.html').write_text(emit(audit_page(), comps, None, '/audit/'), encoding='utf-8')
    labdir = DIST / 'lab'
    labdir.mkdir()
    (labdir / 'index.html').write_text(emit(lab_page(comps), comps, None, '/lab/', True), encoding='utf-8')
    cdir = DIST / 'components'
    cdir.mkdir()
    (cdir / 'index.html').write_text(emit(components_index(comps), comps, None, '/components/', True), encoding='utf-8')
    for i, c in enumerate(comps):
        src = ROOT / 'components' / c['slug']
        dst = cdir / c['slug']
        dst.mkdir()
        for f in src.iterdir():
            if f.is_file():
                if f.suffix in ('.css', '.js', '.html'):
                    (dst / f.name).write_text(distribution_header(f.relative_to(ROOT), f.read_text()), encoding='utf-8')
                else:
                    shutil.copy(f, dst / f.name)
        (dst / 'index.html').write_text(emit(detail(comps, i), comps, comps[i]['slug']), encoding='utf-8')
    jadocs = ja_docs()
    for i, c in enumerate(comps):
        if c['slug'] in jadocs:
            jdst = DIST / 'ja' / 'components' / c['slug']
            jdst.mkdir(parents=True, exist_ok=True)
            (jdst / 'index.html').write_text(emit(ja_detail(comps, i, jadocs), comps, c['slug']), encoding='utf-8')
    tokens = json.loads((ROOT / 'system' / 'tokens.json').read_text(encoding='utf-8'))
    dsdir = DIST / 'design-system'
    dsdir.mkdir()
    (dsdir / 'index.html').write_text(emit(design_system_page(tokens), comps, None, '/design-system/', True), encoding='utf-8')
    prdir = DIST / 'pricing'
    prdir.mkdir()
    (prdir / 'index.html').write_text(emit(pricing_page(), comps, None, '/pricing/', True), encoding='utf-8')
    jadir = DIST / 'ja'
    jadir.mkdir(exist_ok=True)
    (jadir / 'index.html').write_text(emit(ja_page(), comps, None, '/ja/', True), encoding='utf-8')
    scdir = DIST / 'showcase'
    scdir.mkdir()
    (scdir / 'index.html').write_text(emit(showcase_page(templates, blocks), comps, None, '/showcase/', True), encoding='utf-8')
    cmpdir = DIST / 'compare'
    shutil.copytree(ROOT / 'comparison', cmpdir, ignore=shutil.ignore_patterns('*.md', 'results.json'))
    (cmpdir / 'index.html').write_text(emit(compare_page(), comps, None, '/compare/', True), encoding='utf-8')
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
                if f.suffix in ('.css', '.js', '.html'):
                    (dst / f.name).write_text(distribution_header(f.relative_to(ROOT), f.read_text()), encoding='utf-8')
                else:
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
                if f.suffix in ('.css', '.js', '.html'):
                    (dst / f.name).write_text(distribution_header(f.relative_to(ROOT), f.read_text()), encoding='utf-8')
                else:
                    shutil.copy(f, dst / f.name)
        (dst / 'index.html').write_text(emit(template_detail(templates, i, comps, blocks), comps, None, '/templates/' + templates[i]['slug'] + '/', True), encoding='utf-8')
        demo_dir = dst / 'demo'
        demo_dir.mkdir(exist_ok=True)
        (demo_dir / 'index.html').write_text(template_demo(t, comps, blocks), encoding='utf-8')
    # Guard (added 2026-11-03 after the dark-mode incident): every template demo
    # must carry the theme script, or it renders light forever inside dark pages.
    for t in templates:
        _demo_html = (tpdir / t['slug'] / 'demo' / 'index.html').read_text(encoding='utf-8')
        assert 'kata-fdeck' in _demo_html, f'template demo {t["slug"]} is missing the theme script'
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
            _css.append('\n/* ===== component: ' + _c['slug'] + ' ===== */\n' + distribution_header(f"components/{_c['slug']}/{_c['slug']}.css", _c['css']))
    for _b in blocks:
        if _b.get('css'):
            _css.append('\n/* ===== block: ' + _b['slug'] + ' ===== */\n' + distribution_header(f"blocks/{_b['slug']}/{_b['slug']}.css", _b['css']))
    for _t in templates:
        if _t.get('css'):
            _css.append('\n/* ===== template: ' + _t['slug'] + ' ===== */\n' + distribution_header(f"templates/{_t['slug']}/{_t['slug']}.css", _t['css']))
    bundle_css = '\n'.join(_css)
    (DIST / 'kata-ui.css').write_text(bundle_css, encoding='utf-8')
    _js = ['/* KATA UI behavior bundle - each part in its own scope. Load at the end of <body>. Parts whose markup is absent stay inert. */']
    for _c in comps:
        if _c.get('js'):
            _js.append('\n/* ===== component: ' + _c['slug'] + ' ===== */\n(function(){\n' + distribution_header(f"components/{_c['slug']}/{_c['slug']}.js", _c['js']) + '\n})();')
    for _b in blocks:
        if _b.get('js'):
            _js.append('\n/* ===== block: ' + _b['slug'] + ' ===== */\n(function(){\n' + distribution_header(f"blocks/{_b['slug']}/{_b['slug']}.js", _b['js']) + '\n})();')
    for _t in templates:
        if _t.get('js'):
            _js.append('\n/* ===== template: ' + _t['slug'] + ' ===== */\n(function(){\n' + distribution_header(f"templates/{_t['slug']}/{_t['slug']}.js", _t['js']) + '\n})();')
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
    <svg class="nf-plate" width="320" height="120" viewBox="0 0 320 120" fill="none" aria-hidden="true" style="display:block;margin:18px auto 4px">
      <rect x="10" y="10" width="300" height="100" rx="14" stroke="var(--hair)" stroke-width="1.5"/>
      <path d="M10 64 L70 58 L104 70 L138 50 L176 66 L214 54 L252 68 L310 60" stroke="var(--k-yamabuki)" stroke-width="2.5" stroke-linejoin="bevel"/>
      <path d="M138 50 L150 30 L172 26" stroke="var(--k-yamabuki)" stroke-width="1.5" stroke-linejoin="bevel" opacity=".65"/>
      <path d="M214 54 L226 78 L248 84" stroke="var(--k-yamabuki)" stroke-width="1.5" stroke-linejoin="bevel" opacity=".65"/>
    </svg>
    <h1 style="font-size:40px;letter-spacing:-.025em">This part is not in the catalog.</h1>
    <p style="margin:14px auto 0;max-width:52ch;color:var(--ink2);line-height:1.85">The page moved, or it never existed. A crack, mended — that is the house way of handling breakage. The catalog search is the fastest way back — press the search button above, or start from a genre:</p>
    <div class="cta" style="justify-content:center;margin-top:22px;display:flex;gap:10px;flex-wrap:wrap">
      <a class="btn-p" href="/components/" style="display:inline-flex;align-items:center;height:42px;padding:0 20px;border-radius:9px;background:var(--ink);color:var(--paper);font-weight:500;font-size:14px;text-decoration:none">Browse components</a>
      <a href="/blocks/" style="display:inline-flex;align-items:center;height:42px;padding:0 20px;border-radius:9px;border:1px solid var(--hair);font-weight:500;font-size:14px;text-decoration:none;background:var(--paper);color:var(--ink)">See blocks</a>
      <a href="/docs/" style="display:inline-flex;align-items:center;height:42px;padding:0 20px;border-radius:9px;border:1px solid var(--hair);font-weight:500;font-size:14px;text-decoration:none;background:var(--paper);color:var(--ink)">Read the docs</a>
    </div>
  </div>
</div>
""" + FOOTER + """
</body>
</html>"""
    (DIST / '404.html').write_text(emit(nf, comps, None), encoding='utf-8')
    (DIST / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://kata-ui.dev/sitemap.xml\n', encoding='utf-8')
    urls = ['/audit/', '/lab/', '/', '/components/', '/design-system/', '/icons/', '/blocks/', '/templates/', '/themes/', '/docs/', '/pricing/', '/ja/', '/showcase/', '/compare/'] + [f"/ja/components/{s}/" for s in ja_docs()] + [f"/components/{c['slug']}/" for c in comps] + [f"/blocks/{b['slug']}/" for b in blocks] + [f"/templates/{t['slug']}/" for t in templates] + [f"/templates/{t['slug']}/demo/" for t in templates] + [f"/docs/{d[0]}/" for d in DOCS]
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
