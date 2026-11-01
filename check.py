#!/usr/bin/env python3
"""KATA UI — 型検品 (mold check). Verifies every component in the registry conforms to KATA.md.
Usage: python3 check.py [slug ...]   (no args = all components)
Exit code 0 = all pass, 1 = violations found."""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).parent
CATS = {'Form & Input', 'Layout & Navigation', 'Overlays & Dialogs', 'Feedback & Status', 'Display & Media', 'Motion'}
REQUIRED_META = ['title', 'category', 'description', 'tags', 'status', 'usage', 'a11y']
ALLOWED_RGBA = {(0, 0, 0), (255, 255, 255), (16, 24, 40), (24, 24, 27), (244, 244, 245)}
HEX = re.compile(r'#[0-9a-fA-F]{3,8}\b')
RGBA = re.compile(r'rgba?\((\d+),\s*(\d+),\s*(\d+)')

TOKENS_CSS = (ROOT / 'tokens.css').read_text(encoding='utf-8')
DEFINED_TOKENS = set(re.findall(r'(--k-[a-z0-9-]+)\s*:', TOKENS_CSS))

def check_component(d):
    slug = d.name
    errs = []
    meta_f = d / 'meta.json'
    prev_f = d / 'preview.html'
    css_f = d / f'{slug}.css'
    for f, label in [(meta_f, 'meta.json'), (prev_f, 'preview.html'), (css_f, f'{slug}.css')]:
        if not f.exists():
            errs.append(f'missing file: {label}')
    if errs:
        return errs
    try:
        meta = json.loads(meta_f.read_text(encoding='utf-8'))
    except Exception as e:
        return [f'meta.json is not valid JSON: {e}']
    for k in REQUIRED_META:
        if k not in meta or (isinstance(meta[k], (str, list)) and not meta[k]):
            errs.append(f'meta.{k} missing or empty')
    if meta.get('category') not in CATS:
        errs.append(f"meta.category must be one of {sorted(CATS)}")
    if meta.get('status') not in ('stable', 'beta'):
        errs.append('meta.status must be stable or beta')
    css = css_f.read_text(encoding='utf-8')
    for m in HEX.finditer(css):
        if m.group(0).lower() not in ('#000', '#000000', '#fff', '#ffffff'):
            errs.append(f'css: raw hex color {m.group(0)} — use a --k- token (only achromatic #000/#fff allowed, e.g. for masks)')
    for m in RGBA.finditer(css):
        if tuple(int(x) for x in m.groups()) not in ALLOWED_RGBA:
            errs.append(f'css: raw rgba color {m.group(0)}...) — hue must come from a --k- token')
    prev = prev_f.read_text(encoding='utf-8')
    ex_f = d / 'examples.html'
    if ex_f.exists():
        prev += '\n' + ex_f.read_text(encoding='utf-8')
    for m in HEX.finditer(prev):
        errs.append(f'preview: raw hex color {m.group(0)} — use currentColor / a --k- token')
    # the stroke rule binds icon glyphs (24-grid SVGs) only; chart/diagram SVGs use their own geometry
    for svg_m in re.finditer(r'<svg\b[^>]*>.*?</svg>', prev, re.S):
        if 'viewBox="0 0 24 24"' not in svg_m.group(0).split('>', 1)[0]:
            continue
        for m in re.finditer(r'stroke-width="([0-9.]+)"', svg_m.group(0)):
            if m.group(1) != '2':
                errs.append(f'preview: icon svg stroke-width {m.group(1)} — the icon mold is 2 (24 grid)')
    if re.search(r'<script', prev):
        errs.append('preview: <script> belongs in the .js file, not preview.html')
    # classes used in preview must be defined in own CSS or a linked dependency's CSS
    defined = set(re.findall(r'\.([a-zA-Z][\w-]*)', css))
    for href in re.findall(r'href="(?:\.\./|/components/)([a-z0-9-]+)/\1\.css"', prev):
        dep_css = ROOT / 'components' / href / f'{href}.css'
        if dep_css.exists():
            defined |= set(re.findall(r'\.([a-zA-Z][\w-]*)', dep_css.read_text(encoding='utf-8')))
    used = set()
    for attr in re.findall(r'class="([^"]+)"', prev):
        used |= set(attr.split())
    for cls in sorted(used - defined):
        errs.append(f'preview: class .{cls} is not defined in this component or its linked dependencies')
    for label, text in (('css', css), ('preview', prev)):
        local = DEFINED_TOKENS | set(re.findall(r'@property\s+(--k-[a-z0-9-]+)', css))
        for v in set(re.findall(r'var\((--k-[a-z0-9-]+)\)', text)):
            if v not in local:
                errs.append(f'{label}: var({v}) is not defined in tokens.css')
    js_f = d / f'{slug}.js'
    if js_f.exists():
        js = js_f.read_text(encoding='utf-8')
        if re.search(r'\bimport\b|require\(', js):
            errs.append('js: no imports — a component must be self-contained')
    return errs


REQUIRED_META_BLOCK = ['title', 'description', 'tags', 'status', 'uses', 'usage']

def check_block(d, comp_slugs):
    slug = d.name
    errs = []
    meta_f = d / 'meta.json'
    prev_f = d / 'preview.html'
    css_f = d / f'{slug}.css'
    for f, label in [(meta_f, 'meta.json'), (prev_f, 'preview.html'), (css_f, f'{slug}.css')]:
        if not f.exists():
            errs.append(f'missing file: {label}')
    if errs:
        return errs
    try:
        meta = json.loads(meta_f.read_text(encoding='utf-8'))
    except Exception as e:
        return [f'meta.json is not valid JSON: {e}']
    for k in REQUIRED_META_BLOCK:
        if k not in meta or (isinstance(meta[k], (str, list)) and not meta[k]):
            errs.append(f'meta.{k} missing or empty')
    if meta.get('status') not in ('stable', 'beta'):
        errs.append('meta.status must be stable or beta')
    for u in meta.get('uses', []):
        if u not in comp_slugs:
            errs.append(f'meta.uses: unknown component {u}')
    css = css_f.read_text(encoding='utf-8')
    for m in HEX.finditer(css):
        if m.group(0).lower() not in ('#000', '#000000', '#fff', '#ffffff'):
            errs.append(f'css: raw hex color {m.group(0)} — use a --k- token')
    for m in RGBA.finditer(css):
        if tuple(int(x) for x in m.groups()) not in ALLOWED_RGBA:
            errs.append(f'css: raw rgba color {m.group(0)}...) — hue must come from a --k- token')
    prev = prev_f.read_text(encoding='utf-8')
    for m in HEX.finditer(prev):
        errs.append(f'preview: raw hex color {m.group(0)} — use currentColor / a --k- token')
    # the stroke rule binds icon glyphs (24-grid SVGs) only; chart/diagram SVGs use their own geometry
    for svg_m in re.finditer(r'<svg\b[^>]*>.*?</svg>', prev, re.S):
        if 'viewBox="0 0 24 24"' not in svg_m.group(0).split('>', 1)[0]:
            continue
        for m in re.finditer(r'stroke-width="([0-9.]+)"', svg_m.group(0)):
            if m.group(1) != '2':
                errs.append(f'preview: icon svg stroke-width {m.group(1)} — the icon mold is 2 (24 grid)')
    if re.search(r'<script', prev):
        errs.append('preview: <script> belongs in the .js file, not preview.html')
    defined = set(re.findall(r'\.([a-zA-Z][\w-]*)', css))
    linked = re.findall(r'href="(?:\.\./|/components/)([a-z0-9-]+)/\1\.css"', prev)
    for href in linked:
        dep_css = ROOT / 'components' / href / f'{href}.css'
        if dep_css.exists():
            defined |= set(re.findall(r'\.([a-zA-Z][\w-]*)', dep_css.read_text(encoding='utf-8')))
    for u in meta.get('uses', []):
        if u not in linked:
            errs.append(f'meta.uses: {u} is used but its CSS is not linked in preview.html')
    used = set()
    for attr in re.findall(r'class="([^"]+)"', prev):
        used |= set(attr.split())
    for cls in sorted(used - defined):
        errs.append(f'preview: class .{cls} is not defined in this block or its linked components')
    for label, text in (('css', css), ('preview', prev)):
        local = DEFINED_TOKENS | set(re.findall(r'@property\s+(--k-[a-z0-9-]+)', css))
        for v in set(re.findall(r'var\((--k-[a-z0-9-]+)\)', text)):
            if v not in local:
                errs.append(f'{label}: var({v}) is not defined in tokens.css')
    js_f = d / f'{slug}.js'
    if js_f.exists():
        js = js_f.read_text(encoding='utf-8')
        if re.search(r'\bimport\b|require\(', js):
            errs.append('js: no imports — a block must be self-contained')
    return errs

def main():
    args = sys.argv[1:]
    dirs = [ROOT / 'components' / a for a in args] if args else sorted((ROOT / 'components').iterdir())
    bad = 0
    for d in dirs:
        if not d.is_dir():
            continue
        errs = check_component(d)
        if errs:
            bad += 1
            print(f'NG  {d.name}')
            for e in errs:
                print(f'    - {e}')
        else:
            print(f'OK  {d.name}')
    print(f'\n{len(dirs) - bad}/{len(dirs)} components pass the mold')
    bdir = ROOT / 'blocks'
    if bdir.exists() and not args:
        comp_slugs = {d.name for d in (ROOT / 'components').iterdir() if d.is_dir()}
        bdirs = sorted(bdir.iterdir())
        bbad = 0
        for d in bdirs:
            if not d.is_dir():
                continue
            errs = check_block(d, comp_slugs)
            if errs:
                bbad += 1
                print(f'NG  block:{d.name}')
                for e in errs:
                    print(f'    - {e}')
            else:
                print(f'OK  block:{d.name}')
        print(f'{len(bdirs) - bbad}/{len(bdirs)} blocks pass the mold')
        bad += bbad
    sys.exit(1 if bad else 0)

if __name__ == '__main__':
    main()
