#!/usr/bin/env python3
"""KATA UI — 型検品 (mold check). Verifies every component in the registry conforms to KATA.md.
Usage: python3 check.py [slug ...] [--json PATH|-]   (no args = all components)
Exit code 0 = all pass, 1 = violations found."""
import argparse, json, re, sys
from datetime import datetime
from zoneinfo import ZoneInfo
from tools.mold_rules import inspect
from pathlib import Path

ROOT = Path(__file__).parent
CATS = {'Form & Input', 'Layout & Navigation', 'Overlays & Dialogs', 'Feedback & Status', 'Display & Media', 'Motion', 'KATAYABURI', 'Japan'}
REQUIRED_META = ['title', 'category', 'description', 'tags', 'status', 'usage', 'a11y']
CONFIG = json.loads((ROOT / 'check.config.json').read_text())
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
        if 'data-brand' in svg_m.group(0).split('>', 1)[0]:
            continue
        for m in re.finditer(r'stroke-width="([0-9.]+)"', svg_m.group(0)):
            if m.group(1) != '1.7':
                errs.append(f'preview: icon svg stroke-width {m.group(1)} — the icon mold is 1.7 (24 grid)')
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
        local = DEFINED_TOKENS | set(re.findall(r'(--k-[a-z0-9-]+)\s*:', css)) | set(re.findall(r'@property\s+(--k-[a-z0-9-]+)', css))
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
REQUIRED_META_TEMPLATE = ['title', 'description', 'tags', 'status', 'uses', 'blocks', 'usage']

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
    prev = prev_f.read_text(encoding='utf-8')
    for m in HEX.finditer(prev):
        errs.append(f'preview: raw hex color {m.group(0)} — use currentColor / a --k- token')
    # the stroke rule binds icon glyphs (24-grid SVGs) only; chart/diagram SVGs use their own geometry
    for svg_m in re.finditer(r'<svg\b[^>]*>.*?</svg>', prev, re.S):
        if 'viewBox="0 0 24 24"' not in svg_m.group(0).split('>', 1)[0]:
            continue
        if 'data-brand' in svg_m.group(0).split('>', 1)[0]:
            continue
        for m in re.finditer(r'stroke-width="([0-9.]+)"', svg_m.group(0)):
            if m.group(1) != '1.7':
                errs.append(f'preview: icon svg stroke-width {m.group(1)} — the icon mold is 1.7 (24 grid)')
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
        local = DEFINED_TOKENS | set(re.findall(r'(--k-[a-z0-9-]+)\s*:', css)) | set(re.findall(r'@property\s+(--k-[a-z0-9-]+)', css))
        for v in set(re.findall(r'var\((--k-[a-z0-9-]+)\)', text)):
            if v not in local:
                errs.append(f'{label}: var({v}) is not defined in tokens.css')
    js_f = d / f'{slug}.js'
    if js_f.exists():
        js = js_f.read_text(encoding='utf-8')
        if re.search(r'\bimport\b|require\(', js):
            errs.append('js: no imports — a block must be self-contained')
    return errs

def check_template(d, comp_slugs, block_slugs):
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
    for k in REQUIRED_META_TEMPLATE:
        if k not in meta:
            errs.append(f'meta.{k} missing')
    if meta.get('status') not in ('stable', 'beta'):
        errs.append('meta.status must be stable or beta')
    for u in meta.get('uses', []):
        if u not in comp_slugs:
            errs.append(f'meta.uses: unknown component {u}')
    for u in meta.get('blocks', []):
        if u not in block_slugs:
            errs.append(f'meta.blocks: unknown block {u}')
    css = css_f.read_text(encoding='utf-8')
    prev = prev_f.read_text(encoding='utf-8')
    for m in HEX.finditer(prev):
        errs.append(f'preview: raw hex color {m.group(0)} — use currentColor / a --k- token')
    for svg_m in re.finditer(r'<svg\b[^>]*>.*?</svg>', prev, re.S):
        if 'viewBox="0 0 24 24"' not in svg_m.group(0).split('>', 1)[0]:
            continue
        if 'data-brand' in svg_m.group(0).split('>', 1)[0]:
            continue
        for m in re.finditer(r'stroke-width="([0-9.]+)"', svg_m.group(0)):
            if m.group(1) != '1.7':
                errs.append(f'preview: icon svg stroke-width {m.group(1)} — the icon mold is 1.7 (24 grid)')
    if re.search(r'<script', prev):
        errs.append('preview: <script> belongs in the .js file, not preview.html')
    defined = set(re.findall(r'\.([a-zA-Z][\w-]*)', css))
    linked = {}
    for m in re.finditer(r'href="(?:\.\./|/)(components|blocks)/([a-z0-9-]+)/\2\.css"', prev):
        kind, dep = m.group(1), m.group(2)
        linked[dep] = kind
        dep_css = ROOT / kind / dep / f'{dep}.css'
        if dep_css.exists():
            defined |= set(re.findall(r'\.([a-zA-Z][\w-]*)', dep_css.read_text(encoding='utf-8')))
    for u in meta.get('uses', []) + meta.get('blocks', []):
        if u not in linked:
            errs.append(f'meta: {u} is used but its CSS is not linked in preview.html')
    used = set()
    for attr in re.findall(r'class="([^"]+)"', prev):
        used |= set(attr.split())
    for cls in sorted(used - defined):
        errs.append(f'preview: class .{cls} is not defined in this template or its linked parts')
    for label, text in (('css', css), ('preview', prev)):
        local = DEFINED_TOKENS | set(re.findall(r'(--k-[a-z0-9-]+)\s*:', css)) | set(re.findall(r'@property\s+(--k-[a-z0-9-]+)', css))
        for v in set(re.findall(r'var\((--k-[a-z0-9-]+)\)', text)):
            if v not in local:
                errs.append(f'{label}: var({v}) is not defined in tokens.css')
    js_f = d / f'{slug}.js'
    if js_f.exists():
        js = js_f.read_text(encoding='utf-8')
        if re.search(r'\bimport\b|require\(', js):
            errs.append('js: no imports — a template must be self-contained')
    return errs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('slugs', nargs='*')
    parser.add_argument('--json', dest='json_path', help='Write structured report; use - for stdout')
    args = parser.parse_args()
    comp_slugs = {p.name for p in (ROOT / 'components').iterdir() if p.is_dir()}
    block_slugs = {p.name for p in (ROOT / 'blocks').iterdir() if p.is_dir()}
    items = []
    for kind in ('components','blocks','templates'):
        if args.slugs and kind != 'components': continue
        dirs = [ROOT/kind/name for name in args.slugs] if args.slugs else sorted(p for p in (ROOT/kind).iterdir() if p.is_dir())
        for d in dirs:
            if kind == 'components': errors = check_component(d)
            elif kind == 'blocks': errors = check_block(d, comp_slugs)
            else: errors = check_template(d, comp_slugs, block_slugs)
            checks = [{'id':'legacy-contract','status':'fail' if errors else 'pass','severity':'error','findings':errors}]
            checks += inspect(d, ROOT, CONFIG)
            passed = not any(c['status']=='fail' for c in checks)
            items.append({'id':f'{kind}/{d.name}','profile':next(c['profile'] for c in checks if c['id']=='token-values'),'passed':passed,'checks':checks})
    passed = sum(i['passed'] for i in items)
    report = {'updated_at':datetime.now(ZoneInfo('Asia/Tokyo')).date().isoformat(),'schema_version':2,'summary':{'passed':passed,'failed':len(items)-passed,'total':len(items), 'warnings':sum(c['status']=='warn' for i in items for c in i['checks'])},'items':items}
    report['summary']['findings'] = {name:sum(len(c['findings']) for i in items for c in i['checks'] if c['id']==name and c['status']!='pass') for name in sorted({c['id'] for i in items for c in i['checks']})}
    report['summary']['by_profile'] = {profile:{'passed':sum(i['passed'] for i in items if i['profile']==profile),'failed':sum(not i['passed'] for i in items if i['profile']==profile),'total':sum(i['profile']==profile for i in items)} for profile in ('ui','lab')}
    output = json.dumps(report, ensure_ascii=False, indent=2)+'\n'
    if args.json_path == '-': print(output, end='')
    else:
        for item in items:
            print(('OK  ' if item['passed'] else 'NG  ')+item['id'])
            for check in item['checks']:
                if check['status'] != 'pass':
                    for finding in check['findings']:print(f"    {check['status'].upper()} [{check['id']}] {finding}")
        print(f'Mold Verified {passed}/{len(items)}; failed {len(items)-passed}')
        if args.json_path: Path(args.json_path).write_text(output)
    return 1 if report['summary']['failed'] else 0

if __name__ == '__main__':
    sys.exit(main())
