"""Generate tests/torture.html: the Phase 1 parts, three instances each, on one page.

Usage: python3 -m tools.build_torture [--check]

The page reads each part's preview.html, so it follows the components without
hand edits. Radio group names get a -1/-2/-3 suffix so the three copies stay
independent groups. Direction and theme come from the URL (?dir=rtl&theme=dark)
so tools/verify_torture.py can open every condition directly.
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'tests' / 'torture.html'

# Phase 1: the 21 queued parts, then the remaining 19 (docs/HANDOFF.md, T4).
PARTS = [
    'button', 'input', 'field', 'textarea', 'select', 'checkbox', 'radio', 'switch',
    'modal', 'dropdown', 'popover', 'tooltip', 'toast', 'card', 'tabs', 'accordion',
    'badge', 'alert', 'table', 'pagination', 'breadcrumbs',
    'alert-dialog', 'drawer', 'combobox', 'date-picker', 'slider', 'toggle', 'segmented',
    'avatar', 'progress', 'skeleton', 'spinner', 'empty-state', 'separator', 'sidebar',
    'command', 'context-menu', 'hover-card', 'data-table', 'file-upload',
]
INSTANCES = 3
CHEVRON = ('<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
           'stroke-width="1.7" stroke-linecap="square" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>')

PAGE_CSS = """
body{margin:0;font-family:var(--k-font);background:var(--k-bg);color:var(--k-ink)}
.tt-bar{position:sticky;inset-block-start:0;z-index:50;display:flex;flex-wrap:wrap;align-items:center;gap:var(--k-space-3) var(--k-space-6);padding:var(--k-space-3) var(--k-space-6);background:var(--k-bg);border-block-end:1px solid var(--k-line)}
.tt-title{display:flex;align-items:baseline;gap:var(--k-space-3);margin:0;font-size:var(--k-text-lg);font-weight:650}
.tt-count{font-size:var(--k-text-sm);font-weight:400;color:var(--k-ink-2)}
.tt-ctl{display:flex;align-items:center;gap:var(--k-space-2);font-size:var(--k-text-xs);font-weight:600;letter-spacing:.04em;color:var(--k-ink-2)}
.tt-zoom{margin-inline-start:auto;font-size:var(--k-text-xs);color:var(--k-ink-2)}
.tt-main{max-inline-size:880px;margin-inline:auto;padding:var(--k-space-8) var(--k-space-6)}
.tt-part{padding-block:var(--k-space-8);border-block-end:1px solid var(--k-line);scroll-margin-block-start:var(--k-space-16)}
.tt-head{display:flex;flex-wrap:wrap;align-items:center;gap:var(--k-space-3)}
.tt-num{font-family:var(--k-mono);font-size:var(--k-text-sm);color:var(--k-ink-2)}
.tt-name{margin:0;font-size:var(--k-text-xl);font-weight:650}
.tt-link{margin-inline-start:auto;font-size:var(--k-text-sm);color:var(--k-accent-ink)}
.tt-note{margin:var(--k-space-1) 0 0;font-size:var(--k-text-sm);color:var(--k-ink-2)}
.tt-stage{position:relative;margin-block-start:var(--k-space-3);padding:var(--k-space-10) var(--k-space-6) var(--k-space-6);border:1px solid var(--k-line);border-radius:var(--k-radius-xl);background-color:var(--k-bg-soft);background-image:radial-gradient(var(--k-line) 1px,transparent 1px);background-size:14px 14px}
.tt-tag{position:absolute;inset-block-start:var(--k-space-3);inset-inline-start:var(--k-space-3);min-inline-size:24px;padding:0 var(--k-space-1);border:1px solid var(--k-line);border-radius:var(--k-radius-md);background:var(--k-bg);font-size:var(--k-text-xs);font-weight:650;line-height:20px;text-align:center;color:var(--k-ink-2)}
@media (max-width:640px){.tt-bar,.tt-main{padding-inline:var(--k-space-4)}.tt-stage{padding-inline:var(--k-space-4)}.tt-zoom{margin-inline-start:0}}
""".strip()

# Page script: no globals, safe to load twice, state lives in the URL.
PAGE_JS = """
(() => {
  'use strict';
  const root = document.documentElement;
  if (root.hasAttribute('data-tt-ready')) return;
  root.setAttribute('data-tt-ready', '');
  const params = new URLSearchParams(location.search);
  const apply = () => {
    root.dir = params.get('dir') === 'rtl' ? 'rtl' : 'ltr';
    root.dataset.theme = params.get('theme') === 'dark' ? 'dark' : 'light';
    document.querySelectorAll('[data-tt-set]').forEach(input => {
      input.checked = (params.get(input.name) || input.dataset.ttDefault) === input.value;
    });
  };
  apply();
  document.querySelectorAll('[data-tt-set]').forEach(input => input.addEventListener('change', () => {
    params.set(input.name, input.value);
    history.replaceState(null, '', '?' + params.toString());
    apply();
  }));
  const jump = document.querySelector('[data-tt-jump]');
  if (jump) jump.addEventListener('change', () => {
    const target = document.getElementById(jump.value);
    if (!target) return;
    target.scrollIntoView({ block: 'start' });
    target.querySelector('h2').focus({ preventScroll: true });
  });
})();
""".strip()


def preview(slug):
    text = (ROOT / 'components' / slug / 'preview.html').read_text(encoding='utf-8')
    deps = re.findall(r'href="/components/([^/"]+)/[^"]+\.css"', text)
    body = re.sub(r'<link[^>]*>\s*', '', re.sub(r'<!--.*?-->\s*', '', text, flags=re.S)).strip()
    return body, deps


def instance(body, n):
    # Each copy is its own radio group: name="x" becomes name="x-n".
    return re.sub(r'\bname="([^"]+)"', lambda m: f'name="{m.group(1)}-{n}"', body)


def segmented(name, label, options, default):
    items = ''.join(
        f'<label class="k-seg-item"><input type="radio" name="{name}" value="{value}" data-tt-set '
        f'data-tt-default="{default}"{" checked" if value == default else ""}><span>{text}</span></label>'
        for value, text in options)
    return (f'<div class="tt-ctl"><span id="tt-{name}-label">{label}</span>'
            f'<div class="k-seg" role="radiogroup" aria-labelledby="tt-{name}-label">{items}</div></div>')


def build():
    css, scripts, sections, jumps = [], [], [], []

    def add_css(slug):
        href = f'../components/{slug}/{slug}.css'
        if href not in css and (ROOT / 'components' / slug / f'{slug}.css').exists():
            css.append(href)

    for slug in ('segmented', 'select', 'badge'):
        add_css(slug)
    for index, slug in enumerate(PARTS, 1):
        meta = json.loads((ROOT / 'components' / slug / 'meta.json').read_text(encoding='utf-8'))
        body, deps = preview(slug)
        for dep in deps:
            add_css(dep)
        add_css(slug)
        if (ROOT / 'components' / slug / f'{slug}.js').exists():
            scripts.append(f'../components/{slug}/{slug}.js')
        title = html.escape(meta.get('title', slug))
        status = meta.get('status', 'beta')
        tone = 'asagi' if status == 'stable' else 'yamabuki'
        stages = ''.join(
            f'<section class="tt-stage" aria-label="{title} {n}"><span class="tt-tag" aria-hidden="true">{n}</span>'
            f'{instance(body, n)}</section>' for n in range(1, INSTANCES + 1))
        sections.append(
            f'<article class="tt-part" id="part-{slug}" aria-labelledby="h-{slug}">'
            f'<div class="tt-head"><span class="tt-num" aria-hidden="true">{index:02d}</span>'
            f'<h2 class="tt-name" id="h-{slug}" tabindex="-1">{title}</h2>'
            f'<span class="badge {tone}">{html.escape(status.capitalize())}</span>'
            f'<a class="tt-link" href="../components/{slug}/preview.html">Part source</a></div>'
            f'<p class="tt-note"><bdi>{INSTANCES} instances, same markup.</bdi></p>{stages}</article>')
        jumps.append(f'<option value="part-{slug}">{index:02d} {title}</option>')

    bar = (
        '<header class="tt-bar">'
        f'<h1 class="tt-title">Torture Test <bdi class="tt-count">{len(PARTS)} parts × {INSTANCES}</bdi></h1>'
        + segmented('dir', 'DIRECTION', [('ltr', 'LTR'), ('rtl', 'RTL')], 'ltr')
        + segmented('theme', 'THEME', [('light', 'Light'), ('dark', 'Dark')], 'light')
        + '<div class="tt-ctl"><label for="tt-jump">JUMP TO</label>'
        f'<span class="k-select"><select id="tt-jump" data-tt-jump>{"".join(jumps)}</select>{CHEVRON}</span></div>'
        '<p class="tt-zoom"><bdi>Zoom: browser 200% (Ctrl / ⌘ and +)</bdi></p>'
        '</header>')
    head = (
        '<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<title>Torture Test — KATA UI</title><link rel="icon" href="../logo/favicon.svg">'
        '<link rel="stylesheet" href="../tokens.css">'
        + ''.join(f'<link rel="stylesheet" href="{href}">' for href in css)
        + f'<style>{PAGE_CSS}</style></head>\n')
    body = (
        '<body>\n<!-- Generated by tools/build_torture.py. Do not edit by hand. -->\n'
        + bar + '\n<main class="tt-main">\n' + '\n'.join(sections) + '\n</main>\n'
        + ''.join(f'<script src="{src}"></script>' for src in scripts)
        + f'\n<script>{PAGE_JS}</script>\n</body></html>\n')
    return head + body


def main(argv):
    text = build()
    if '--check' in argv:
        if not OUT.exists() or OUT.read_text(encoding='utf-8') != text:
            print('tests/torture.html is out of date: run python3 -m tools.build_torture')
            return 1
        print(f'tests/torture.html is up to date ({len(PARTS)} parts × {INSTANCES})')
        return 0
    OUT.write_text(text, encoding='utf-8')
    print(f'wrote {OUT.relative_to(ROOT)} ({len(PARTS)} parts × {INSTANCES})')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
